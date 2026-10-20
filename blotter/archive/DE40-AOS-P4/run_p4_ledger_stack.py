"""DE40-AOS-P4 — L6 ledger + det/AI/L8 shadow stack on tip tape."""
from __future__ import annotations

import csv
import json
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd

try:
    import joblib
except ImportError:  # pragma: no cover
    joblib = None

TAPES = Path(
    r"C:\Users\emili\AppData\Roaming\MetaQuotes\Terminal"
    r"\D0E8209F77C8CF37AD8BF550E51FF075\MQL5\Experts\BMRG\doc\assets\DE40\tapes"
)
MODEL = Path(
    r"C:\Users\emili\AppData\Roaming\MetaQuotes\Terminal"
    r"\D0E8209F77C8CF37AD8BF550E51FF075\MQL5\Experts\BMRG\infra\artefacts\models"
    r"\L2skip_de40\LATEST\model.joblib"
)
OUT = Path(__file__).resolve().parent
ASSETS = Path(
    r"C:\Users\emili\AppData\Roaming\MetaQuotes\Terminal"
    r"\D0E8209F77C8CF37AD8BF550E51FF075\MQL5\Experts\BMRG\doc\assets\DE40"
)

R = 1.25
BWR = 1.0 / (1.0 + R)
LEAK = 0.098  # prior authority
DEPOSIT = 500.0
DD_LIMIT = 25.0
W15, W20 = 15, 20
BASELINE_EN = 0.3149
AI_THR = 0.55  # shadow thr from P2 (DISARM regardless)
MAGIC = 26101902

FEATS = [
    "side_buy",
    "is_h13",
    "is_feb",
    "is_mar",
    "is_mismatch",
    "is_fragile",
    "near_atr_cap",
    "hour",
    "atr_z",
    "is_wed",
    "is_mon",
    "is_fri",
    "is_aug",
]

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
    "hold_h",
    "l2det_skip",
    "l2det_reason",
    "l8_advise",
    "final_permit",
    "stack",
]


def load_tip() -> pd.DataFrame:
    df = pd.read_csv(TAPES / "de40_tip_fire_tape_v0.csv")
    df["open_dt"] = pd.to_datetime(df["open_time"], format="%Y.%m.%d %H:%M:%S")
    df = df.sort_values("open_dt").reset_index(drop=True)
    df["win"] = df["win"].astype(int)
    df["pnl"] = df["pnl_ccy_proxy"].astype(float)
    df["pnl_R"] = df["pnl_R_design"].astype(float)
    df["hold_h"] = df["hold_h"].astype(float)
    df["nights_held"] = df["nights_held"].astype(int)
    df["near_atr_cap"] = df["near_atr_cap"].astype(int)
    df["hour"] = df["hour"].astype(int)
    df["side_buy"] = (df["side"] == "BUY").astype(int)
    df["buy_near"] = ((df["side"] == "BUY") & (df["near_atr_cap"] == 1)).astype(int)
    df["is_h13"] = (df["hour"] == 13).astype(int)
    df["is_feb"] = (df["month"] == "2026-02").astype(int)
    df["is_mar"] = (df["month"] == "2026-03").astype(int)
    df["is_aug"] = (df["month"] == "2026-08").astype(int)
    df["is_mismatch"] = (df["ouroboros_tag"] == "MISMATCH").astype(int)
    df["is_fragile"] = (df["ouroboros_tag"] == "FRAGILE").astype(int)
    df["is_wed"] = (df["dow"] == "Wed").astype(int)
    df["is_mon"] = (df["dow"] == "Mon").astype(int)
    df["is_fri"] = (df["dow"] == "Fri").astype(int)
    atr = df["atr_pts"].astype(float)
    df["atr_z"] = (atr - atr.mean()) / (atr.std() + 1e-9)

    # AI shadow scores
    df["ai_proba"] = np.nan
    df["ai_would_skip"] = 0
    if joblib is not None and MODEL.exists():
        blob = joblib.load(MODEL)
        X = df[FEATS].fillna(0).to_numpy()
        p = blob["clf"].predict_proba(blob["scaler"].transform(X))[:, 1]
        df["ai_proba"] = p
        df["ai_would_skip"] = (p >= AI_THR).astype(int)
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


def l8_advise(row) -> str:
    """Cash-sleeve MAE advisor — secondary; no tick MAE on tape."""
    if row["win"] == 0 and int(row["nights_held"]) == 1 and row["hold_h"] >= 12.0:
        return "L8_ADVISE_ABORT_OVERNIGHT_SL"
    if (
        row["win"] == 0
        and row["hold_h"] < 1.0
        and int(row["near_atr_cap"]) == 1
    ):
        return "L8_ADVISE_ABORT_FAST_SL_NEAR_ATR"
    if row["win"] == 0 and row["hold_h"] < 0.25:
        return "L8_ADVISE_ABORT_FLASH_SL"
    if row["win"] == 0 and row["hold_h"] < 1.0:
        return "L8_ADVISE_ABORT_FLASH_SL"
    return "L8_HOLD"


def run_stack(df: pd.DataFrame, stack: str, l2_mode: str, use_ai: bool) -> list[dict]:
    """l2_mode: none | arm | v1b"""
    equity = DEPOSIT
    peak = DEPOSIT
    permitted_wins: list[int] = []
    en15_hist: list[float | None] = []
    compress_streak = 0
    halt_latched = False
    rows_out = []

    for _, row in df.iterrows():
        skip_bn = row["buy_near"] == 1
        skip_h13 = row["is_h13"] == 1
        reasons = []
        if l2_mode == "arm":
            l2det = skip_bn
            if skip_bn:
                reasons.append("L2DET_SKIP_BUY_NEAR_ATR")
        elif l2_mode == "v1b":
            l2det = skip_bn or skip_h13
            if skip_h13:
                reasons.append("L2DET_SKIP_H13")
            if skip_bn:
                reasons.append("L2DET_SKIP_BUY_NEAR_ATR")
        else:
            l2det = False
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
            final = 1  # DISARM — log only
        else:
            decision, layer, reason = "FIRE_OK", "ENGINE", "FIRE_OK"
            final = 1

        if l8.startswith("L8_ADVISE"):
            reason = f"{reason}|{l8}"

        ot = row["open_time"]
        event_id = (
            f"{MAGIC}-DE30-{row['side']}-"
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
                "model": "L2skip_de40_DISARM" if use_ai else "none",
                "halt": int(halt),
                "derisk": int(derisk),
                "mode": "SHADOW",
                "event_id": event_id,
                "open_time": ot,
                "exit_reason": row["exit_reason"],
                "win": int(row["win"]),
                "pnl_R": float(row["pnl_R"]),
                "nights_held": int(row["nights_held"]),
                "hold_h": float(row["hold_h"]),
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
    ef_v = (wr - BWR - LEAK) * 100
    l8_losers = sum(1 for r in l8 if r["win"] == 0)
    l8_winners = sum(1 for r in l8 if r["win"] == 1)
    return {
        "n_fire": n,
        "n_l2det_skip": len(skips),
        "n_l2ai_shadow_skip": len(ai_shadow),
        "n_l3_halt": len(halts),
        "WR_pct": round(wr * 100, 2),
        "E_N": round(en_v, 4),
        "EF_prior_pp": round(ef_v, 3),
        "l8_advise_n": len(l8),
        "l8_advise_on_losers": l8_losers,
        "l8_advise_on_winners": l8_winners,
        "fire_retention_pct": round(100.0 * n / len(rows), 1),
    }


def write_ledger(rows: list[dict], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=LEDGER_COLS, extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)


def main() -> None:
    tip = load_tip()
    stacks = {
        "P0_engine": ("none", False),
        "det_arm_BUY_near_atr": ("arm", False),
        "det_hold_v1b": ("v1b", False),
        "det_arm_plus_ai_shadow": ("arm", True),
    }
    report = {
        "task": "DE40-AOS-P4",
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "Leak_prior_pp": LEAK * 100,
        "AI_thr_shadow": AI_THR,
        "stacks": {},
    }
    ledgers = {}
    for name, (l2, ai) in stacks.items():
        rows = run_stack(tip, name, l2, ai)
        ledgers[name] = rows
        write_ledger(rows, OUT / f"ledger_{name}.csv")
        report["stacks"][name] = score_ledger(rows)

    # Canonical tip ledger = armed det stack
    write_ledger(
        ledgers["det_arm_BUY_near_atr"],
        ASSETS / "tapes" / "de40_tip_ledger_arm_shadow.csv",
    )
    (OUT / "P4_STACK.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
