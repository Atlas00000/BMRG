"""UK100-AOS-P4 — L6 ledger + det/AI/L8 shadow stack on tip tape."""
from __future__ import annotations

import csv
import json
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd

TAPES = Path(
    r"C:\Users\emili\AppData\Roaming\MetaQuotes\Terminal"
    r"\D0E8209F77C8CF37AD8BF550E51FF075\MQL5\Experts\BMRG\doc\assets\UK100\tapes"
)
P2 = Path(
    r"C:\Users\emili\AppData\Roaming\MetaQuotes\Terminal"
    r"\D0E8209F77C8CF37AD8BF550E51FF075\MQL5\Experts\BMRG\blotter\archive\UK100-AOS-P2-REMAINING"
)
OUT = Path(__file__).resolve().parent
ASSETS = Path(
    r"C:\Users\emili\AppData\Roaming\MetaQuotes\Terminal"
    r"\D0E8209F77C8CF37AD8BF550E51FF075\MQL5\Experts\BMRG\doc\assets\UK100"
)

R = 1.25
BWR = 1.0 / (1.0 + R)
LEAK = 0.042667
DEPOSIT = 500.0
DD_LIMIT = 25.0
W15, W20 = 15, 20
BASELINE_EN = 0.1029

# EA-compatible ledger columns + UK100 extensions
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
    # extensions
    "event_id",
    "open_time",
    "exit_reason",
    "win",
    "pnl_R",
    "l2det_skip",
    "l2det_reason",
    "l8_advise",
    "final_permit",
    "stack",
]


def load_tip() -> pd.DataFrame:
    df = pd.read_csv(TAPES / "uk100_tip_fire_tape_v0.csv")
    df["open_dt"] = pd.to_datetime(df["open_time"], format="%Y.%m.%d %H:%M:%S")
    df = df.sort_values("open_dt").reset_index(drop=True)
    df["win"] = df["win"].astype(int)
    df["pnl"] = df["pnl_ccy_proxy"].astype(float)
    df["pnl_R"] = df["pnl_R_design"].astype(float)
    df["hold_h"] = df["hold_h"].astype(float)
    df["is_thu"] = df["cell_dow_thu"].astype(int)
    df["buy_near"] = (
        (df["side"] == "BUY") & (df["near_atr_cap"].astype(int) == 1)
    ).astype(int)
    df["is_jul"] = df["cell_month_jul"].astype(int)
    scored = P2 / "tip_l2ai_scored.csv"
    if scored.exists():
        ai = pd.read_csv(scored)
        ai["open_dt"] = pd.to_datetime(ai["open_time"], format="%Y.%m.%d %H:%M:%S")
        ai = ai.sort_values("open_dt").reset_index(drop=True)
        df["ai_proba"] = ai["p_lose"].astype(float)
        df["ai_would_skip"] = ai["would_skip"].astype(int)
    else:
        df["ai_proba"] = np.nan
        df["ai_would_skip"] = 0
    return df


def en(wins: np.ndarray) -> float:
    if len(wins) == 0:
        return float("nan")
    return float(wins.mean() * (R + 1) - 1)


def ef_pp(wins: np.ndarray) -> float:
    if len(wins) == 0:
        return float("nan")
    return float((wins.mean() - BWR - LEAK) * 100)


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


def det_reason(row) -> tuple[bool, str]:
    reasons = []
    if row["is_thu"] == 1:
        reasons.append("L2DET_SKIP_THU")
    if row["buy_near"] == 1:
        reasons.append("L2DET_SKIP_BUY_NEAR_ATR")
    if row["is_jul"] == 1:
        reasons.append("L2DET_SKIP_JUL")
    # v1b primary = Thu OR buy_near; Jul optional — include Jul in stack_v1b_jul
    return bool(reasons), "|".join(reasons) if reasons else "FIRE_OK"


def l8_advise(row) -> str:
    """Shadow MAE abort advisor — no tick MAE; use fast-SL fingerprint."""
    # Fast adverse resolution into SL under stress ATR
    if (
        row["win"] == 0
        and row["hold_h"] < 1.0
        and int(row["near_atr_cap"]) == 1
    ):
        return "L8_ADVISE_ABORT_FAST_SL"
    if row["win"] == 0 and row["hold_h"] < 0.25:
        return "L8_ADVISE_ABORT_FLASH_SL"
    return "L8_HOLD"


def run_stack(df: pd.DataFrame, stack: str, use_jul: bool, use_ai: bool) -> list[dict]:
    return _rerun_with_permitted_health(df, stack, use_jul, use_ai)


def _rerun_with_permitted_health(
    df: pd.DataFrame, stack: str, use_jul: bool, use_ai: bool
) -> list[dict]:
    equity = DEPOSIT
    peak = DEPOSIT
    permitted_wins: list[int] = []
    en15_hist: list[float | None] = []
    compress_streak = 0
    halt_latched = False
    rows_out = []

    for i, row in df.iterrows():
        skip_thu = row["is_thu"] == 1
        skip_bn = row["buy_near"] == 1
        skip_jul = use_jul and row["is_jul"] == 1
        l2det = skip_thu or skip_bn or skip_jul
        reasons = []
        if skip_thu:
            reasons.append("L2DET_SKIP_THU")
        if skip_bn:
            reasons.append("L2DET_SKIP_BUY_NEAR_ATR")
        if skip_jul:
            reasons.append("L2DET_SKIP_JUL")
        l2det_reason = "|".join(reasons) if reasons else "FIRE_OK"

        ai_skip = bool(row["ai_would_skip"]) if use_ai else False
        ai_p = float(row["ai_proba"]) if not np.isnan(row["ai_proba"]) else None

        w15 = np.array(permitted_wins[-W15:], dtype=float)
        w20 = np.array(permitted_wins[-W20:], dtype=float)
        en15 = en(w15) if len(w15) >= W15 else float("nan")
        ef15 = ef_pp(w15) if len(w15) >= W15 else float("nan")
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
        elif l2det:
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
            f"26101201-UK100-{row['side']}-"
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
                "model": "L2skip_uk_DISARM" if use_ai else "none",
                "halt": int(halt),
                "derisk": int(derisk),
                "mode": "SHADOW",
                "event_id": event_id,
                "open_time": ot,
                "exit_reason": row["exit_reason"],
                "win": int(row["win"]),
                "pnl_R": float(row["pnl_R"]),
                "l2det_skip": int(l2det),
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
            # update en15 hist from new permitted window
            w15b = np.array(permitted_wins[-W15:], dtype=float)
            en15b = en(w15b) if len(w15b) >= W15 else float("nan")
            en15_hist.append(None if np.isnan(en15b) else en15b)
        else:
            en15_hist.append(prev)

    return rows_out


def score_ledger(rows: list[dict]) -> dict:
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
    ef = (wr - BWR - LEAK) * 100
    return {
        "n_signals": len(rows),
        "n_fire": n,
        "n_l2det_skip": len(skips),
        "n_l2ai_shadow_skip": len(ai_shadow),
        "n_l3_halt": len(halts),
        "n_l8_advise": len(l8),
        "WR": round(wr * 100, 2),
        "E_N": round(en_v, 4),
        "EF_proxy_pp": round(ef, 3),
        "skip_precision_losers": round(
            sum(1 for r in skips if r["win"] == 0) / len(skips), 4
        )
        if skips
        else None,
        "l8_on_losers": sum(1 for r in l8 if r["win"] == 0),
        "l8_on_winners": sum(1 for r in l8 if r["win"] == 1),
    }


def write_ledger(rows: list[dict], path: Path) -> None:
    with path.open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=LEDGER_COLS, extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)


def main() -> None:
    tip = load_tip()
    stacks = {
        "det_v1b": (False, False),  # no jul, no ai
        "det_v1b_jul": (True, False),
        "det_v1b_plus_ai_shadow": (False, True),
        "det_v1b_jul_plus_ai_shadow": (True, True),
    }
    report = {
        "task": "UK100-AOS-P4",
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "stacks": {},
    }
    for name, (use_jul, use_ai) in stacks.items():
        rows = run_stack(tip, name, use_jul, use_ai)
        write_ledger(rows, OUT / f"ledger_{name}.csv")
        report["stacks"][name] = score_ledger(rows)

    # canonical stack for docs = det_v1b
    write_ledger(
        run_stack(tip, "det_v1b", False, False),
        ASSETS / "tapes" / "uk100_tip_ledger_v1b_shadow.csv",
    )

    (OUT / "P4_STACK.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
