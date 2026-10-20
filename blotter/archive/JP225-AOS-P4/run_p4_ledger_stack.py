"""JP225-AOS-P4 — L6 ledger + det/AI/L8 shadow stack on tip tape (offline only).

No MQH wire · no research OS arm · L2AI DISARM · Leak = measured median.
Canonical L2det = May∨Jul (ARM_SOFT from P2).
"""
from __future__ import annotations

import csv
import json
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd

TAPES = Path(
    r"C:\Users\emili\AppData\Roaming\MetaQuotes\Terminal"
    r"\D0E8209F77C8CF37AD8BF550E51FF075\MQL5\Experts\BMRG\doc\assets\JP225\tapes"
)
OUT = Path(__file__).resolve().parent
ASSETS = Path(
    r"C:\Users\emili\AppData\Roaming\MetaQuotes\Terminal"
    r"\D0E8209F77C8CF37AD8BF550E51FF075\MQL5\Experts\BMRG\doc\assets\JP225"
)
LEAK_JSON = ASSETS / "LEAK_MEASURED.json"

R = 1.50
BWR = 1.0 / (1.0 + R)
# Authority: measured median deal-fill (JP225-AOS-LEAK)
LEAK = 0.024471
DEPOSIT = 500.0
DD_LIMIT = 25.0
W15, W20 = 15, 20
BASELINE_EN = 0.0759  # tip P1 pre-L2
MAGIC = "26101904"

LEDGER_COLS = [
    "t",
    "side",
    "layer",
    "decision",
    "reason",
    "life",
    "f_rec",
    "w250_EF",
    "w250_EN",
    "ai_proba",
    "ai_skip",
    "model",
    "halt",
    "derisk",
    "mode",
    "event_id",
    "open_time",
    "exit_reason",
    "win",
    "pnl_R",
    "nights_held",
    "l2det_skip",
    "l2det_reason",
    "l8_advise",
    "final_permit",
    "stack",
]


def load_leak() -> float:
    if LEAK_JSON.exists():
        pkt = json.loads(LEAK_JSON.read_text(encoding="utf-8"))
        return float(pkt["Leak_measured_median_pp"]) / 100.0
    return LEAK


def load_tip() -> pd.DataFrame:
    df = pd.read_csv(TAPES / "jp225_tip_fire_tape_v0.csv")
    df["open_dt"] = pd.to_datetime(df["open_time"], format="%Y.%m.%d %H:%M:%S")
    df = df.sort_values("open_dt").reset_index(drop=True)
    df["win"] = df["win"].astype(int)
    df["pnl"] = df["pnl_ccy_proxy"].astype(float)
    df["pnl_R"] = df["pnl_R_design"].astype(float)
    df["hold_h"] = df["hold_h"].astype(float)
    df["nights_held"] = df["nights_held"].astype(int)
    df["is_may"] = df["cell_month_may"].astype(int)
    df["is_jul"] = df["cell_month_jul"].astype(int)
    df["may_fragile"] = df["cell_may_fragile"].astype(int)
    df["near_atr"] = df["near_atr_cap"].astype(int)
    # L2AI DISARM — no tip_l2ai_scored; stub zeros
    df["ai_proba"] = np.nan
    df["ai_would_skip"] = 0
    return df


def en(wins: np.ndarray) -> float:
    if len(wins) == 0:
        return float("nan")
    return float(wins.mean() * (R + 1) - 1)


def ef_pp(wins: np.ndarray, leak: float) -> float:
    if len(wins) == 0:
        return float("nan")
    return float((wins.mean() - BWR - leak) * 100)


def lifecycle(en15, prev, en20, ef15) -> str:
    if np.isnan(en15):
        return "WARMUP"
    if (not np.isnan(en20)) and en20 <= 0 and ef15 <= 0:
        return "BELOW"
    if ef15 <= 1.0 or en15 < 0:
        return "NEAR"
    if prev is not None and not np.isnan(prev) and en15 < prev - 1e-9:
        return "COMPRESSING_CAND"
    if en15 > BASELINE_EN and (prev is None or en15 >= prev - 1e-9):
        return "EXPANDING"
    if en15 >= 0:
        return "STABLE"
    return "NEAR"


def l8_advise(row) -> str:
    """Secondary for cash/index sleeve — overnight + fast-SL fingerprints only."""
    if row["win"] == 0 and int(row["nights_held"]) >= 1 and row["hold_h"] >= 12.0:
        return "L8_ADVISE_ABORT_OVERNIGHT_SL"
    if row["win"] == 0 and row["hold_h"] < 1.0 and int(row["near_atr"]) == 1:
        return "L8_ADVISE_ABORT_FAST_SL_NEAR_ATR"
    if row["win"] == 0 and row["hold_h"] < 0.25:
        return "L8_ADVISE_ABORT_FLASH_SL"
    return "L8_HOLD"


def run_stack(
    df: pd.DataFrame, stack: str, policy: str, use_ai: bool, leak: float
) -> list[dict]:
    equity = DEPOSIT
    peak = DEPOSIT
    permitted_wins: list[int] = []
    en15_hist: list[float | None] = []
    compress_streak = 0
    halt_latched = False
    rows_out: list[dict] = []

    for _, row in df.iterrows():
        if policy == "may_or_jul":
            skip = (row["is_may"] == 1) or (row["is_jul"] == 1)
            reasons = []
            if row["is_may"] == 1:
                reasons.append("L2DET_SKIP_MAY")
            if row["is_jul"] == 1:
                reasons.append("L2DET_SKIP_JUL")
        elif policy == "may_only":
            skip = row["may_fragile"] == 1 or row["is_may"] == 1
            reasons = ["L2DET_SKIP_MAY_FRAGILE"] if skip else []
        else:
            skip = False
            reasons = []
        l2det_reason = "|".join(reasons) if reasons else "FIRE_OK"

        ai_skip = bool(row["ai_would_skip"]) if use_ai else False
        ai_p = float(row["ai_proba"]) if not np.isnan(row["ai_proba"]) else None

        w15 = np.array(permitted_wins[-W15:], dtype=float)
        w20 = np.array(permitted_wins[-W20:], dtype=float)
        en15 = en(w15) if len(w15) >= W15 else float("nan")
        ef15 = ef_pp(w15, leak) if len(w15) >= W15 else float("nan")
        en20 = en(w20) if len(w20) >= W20 else float("nan")
        prev = en15_hist[-1] if en15_hist else None
        life = lifecycle(en15, prev, en20, ef15)
        if (
            not np.isnan(en15)
            and prev is not None
            and not np.isnan(prev)
            and en15 < prev - 1e-9
        ):
            compress_streak += 1
        else:
            compress_streak = 0
        if life == "COMPRESSING_CAND" and compress_streak >= 2:
            life = "COMPRESSING"
        elif life == "COMPRESSING_CAND":
            life = "STABLE" if en15 >= 0 else "NEAR"

        dd_peak = (peak - equity) / peak * 100.0 if peak > 0 else 0.0
        derisk = dd_peak >= 0.8 * DD_LIMIT
        halt = halt_latched or (dd_peak >= DD_LIMIT)
        if len(w20) >= W20 and life == "BELOW":
            halt = True
            halt_latched = True

        f_table = {
            "EXPANDING": 1.0,
            "STABLE": 1.0,
            "COMPRESSING": 0.5,
            "NEAR": 0.25,
            "BELOW": 0.0,
            "WARMUP": 1.0,
        }
        f = 0.0 if halt else f_table.get(life, 1.0)
        if derisk:
            f = min(f, 0.5)

        l8 = l8_advise(row)

        if halt:
            decision, layer, reason = "HALT", "L3", "HALT_LATCHED_OR_DD_OR_BELOW"
            final = 0
        elif skip:
            decision, layer, reason = "WOULD_SKIP", "L2DET", l2det_reason
            final = 0
        elif use_ai and ai_skip:
            decision, layer, reason = "WOULD_SKIP_SHADOW", "L2AI", "L2AI_PLOSE_GE_THR"
            final = 1  # DISARM
        else:
            decision, layer, reason = "FIRE_OK", "ENGINE", "FIRE_OK"
            final = 1

        if l8.startswith("L8_ADVISE"):
            reason = f"{reason}|{l8}"

        ot = row["open_time"]
        event_id = (
            f"{MAGIC}-JPN225-{row['side']}-"
            f"{ot.replace('.', '').replace(':', '').replace(' ', '')}"
        )

        rows_out.append(
            {
                "t": ot[:16],
                "side": row["side"],
                "layer": layer,
                "decision": decision,
                "reason": reason,
                "life": life,
                "f_rec": round(f, 2),
                "w250_EF": "" if np.isnan(ef15) else round(ef15, 2),
                "w250_EN": "" if np.isnan(en15) else round(en15, 4),
                "ai_proba": "" if ai_p is None else round(ai_p, 4),
                "ai_skip": int(ai_skip),
                "model": "L2skip_jp225_DISARM" if use_ai else "none",
                "halt": int(halt),
                "derisk": int(derisk),
                "mode": "SHADOW",
                "event_id": event_id,
                "open_time": ot,
                "exit_reason": row["exit_reason"],
                "win": int(row["win"]),
                "pnl_R": float(row["pnl_R"]),
                "nights_held": int(row["nights_held"]),
                "l2det_skip": int(skip),
                "l2det_reason": l2det_reason,
                "l8_advise": l8,
                "final_permit": final,
                "stack": stack,
            }
        )

        if final == 1:
            equity += float(row["pnl"])
            peak = max(peak, equity)
            permitted_wins.append(int(row["win"]))
            w15b = np.array(permitted_wins[-W15:], dtype=float)
            en15b = en(w15b) if len(w15b) >= W15 else float("nan")
            en15_hist.append(None if np.isnan(en15b) else en15b)
        else:
            en15_hist.append(prev)

    return rows_out


def score_ledger(rows: list[dict], leak: float) -> dict:
    fires = [r for r in rows if r["final_permit"] == 1]
    skips = [r for r in rows if r["decision"] == "WOULD_SKIP"]
    ai_shadow = [r for r in rows if r["decision"] == "WOULD_SKIP_SHADOW"]
    halts = [r for r in rows if r["decision"] == "HALT"]
    l8 = [r for r in rows if str(r["l8_advise"]).startswith("L8_ADVISE")]
    n = len(fires)
    if n == 0:
        return {"n_fire": 0}
    wr = sum(r["win"] for r in fires) / n
    en_v = wr * (R + 1) - 1
    ef = (wr - BWR - leak) * 100
    return {
        "n_signals": len(rows),
        "n_fire": n,
        "n_l2det_skip": len(skips),
        "n_l2ai_shadow_skip": len(ai_shadow),
        "n_l3_halt": len(halts),
        "n_l8_advise": len(l8),
        "fire_retention_pct": round(100.0 * n / len(rows), 1),
        "WR": round(wr * 100, 2),
        "E_N": round(en_v, 4),
        "EF_measured_pp": round(ef, 3),
        "tip_EF_cleared": bool(ef > 0),
        "skip_precision_losers": round(
            sum(1 for r in skips if r["win"] == 0) / len(skips), 4
        )
        if skips
        else None,
        "l8_on_losers": sum(1 for r in l8 if r["win"] == 0),
        "l8_on_winners": sum(1 for r in l8 if r["win"] == 1),
        "l8_overnight": sum(
            1 for r in l8 if r["l8_advise"] == "L8_ADVISE_ABORT_OVERNIGHT_SL"
        ),
    }


def write_ledger(rows: list[dict], path: Path) -> None:
    with path.open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=LEDGER_COLS, extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)


def main() -> None:
    leak = load_leak()
    tip = load_tip()
    stacks = {
        "det_may_or_jul": ("may_or_jul", False),
        "det_may_only": ("may_only", False),
        "det_may_or_jul_plus_ai_shadow": ("may_or_jul", True),
        "baseline_no_l2": ("none", False),
    }
    report = {
        "task": "JP225-AOS-P4",
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "window": "2026.05.01-2026.08.31",
        "magic": int(MAGIC),
        "Leak_measured_pp": round(leak * 100, 4),
        "Leak_source": "measured_median_deal_fill",
        "mqh_wire": False,
        "research_os_arm": False,
        "l2ai_mode": "DISARM",
        "canonical_stack": "det_may_or_jul",
        "stacks": {},
    }
    for name, (policy, use_ai) in stacks.items():
        rows = run_stack(tip, name, policy, use_ai, leak)
        write_ledger(rows, OUT / f"ledger_{name}.csv")
        report["stacks"][name] = score_ledger(rows, leak)

    # canonical doc copy
    write_ledger(
        run_stack(tip, "det_may_or_jul", "may_or_jul", False, leak),
        TAPES / "jp225_tip_ledger_may_or_jul_shadow.csv",
    )

    (OUT / "P4_STACK.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
