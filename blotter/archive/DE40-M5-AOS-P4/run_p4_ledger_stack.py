"""DE40-M5-AOS-P4 — L6 ledger + det/AI/L8 shadow stack on M5 tip tape."""
from __future__ import annotations

import csv
import json
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler

TAPES = Path(
    r"C:\Users\emili\AppData\Roaming\MetaQuotes\Terminal"
    r"\D0E8209F77C8CF37AD8BF550E51FF075\MQL5\Experts\BMRG\doc\assets\DE40\tapes"
)
OUT = Path(__file__).resolve().parent
ASSETS = Path(
    r"C:\Users\emili\AppData\Roaming\MetaQuotes\Terminal"
    r"\D0E8209F77C8CF37AD8BF550E51FF075\MQL5\Experts\BMRG\doc\assets\DE40"
)

R = 1.25
BWR = 1.0 / (1.0 + R)
LEAK = 0.07  # prior authority
DEPOSIT = 500.0
DD_LIMIT = 25.0
W15, W20, W50 = 15, 20, 50
BASELINE_EN = 0.207317
MAGIC = 26151904
AI_THR = 0.55  # P2 best thr (DISARM)

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
    "l2det_skip",
    "l2det_reason",
    "l8_advise",
    "final_permit",
    "stack",
]


def load_tip() -> pd.DataFrame:
    df = pd.read_csv(TAPES / "de40_m5_tip_fire_tape_v0.csv")
    prior = pd.read_csv(TAPES / "de40_m5_prior_fire_tape_v0.csv")
    df["open_dt"] = pd.to_datetime(df["open_time"], format="%Y.%m.%d %H:%M:%S")
    df = df.sort_values("open_dt").reset_index(drop=True)
    for c in (
        "win",
        "near_atr_cap",
        "cell_month_feb",
        "cell_month_may",
        "cell_mismatch",
        "cell_fragile",
        "cell_buy",
        "cell_sell",
        "y_lose",
        "hour",
        "spread_pts",
    ):
        df[c] = df[c].astype(int)
        if c in prior.columns:
            prior[c] = prior[c].astype(int)
    df["atr_pts"] = df["atr_pts"].astype(float)
    prior["atr_pts"] = prior["atr_pts"].astype(float)
    df["pnl"] = df["pnl_ccy_proxy"].astype(float)
    df["pnl_R"] = df["pnl_R_design"].astype(float)
    df["hold_h"] = df["hold_h"].astype(float)
    df["month"] = df["month"].astype(str)

    buy_h14_16 = (df["cell_buy"] == 1) & (df["hour"].isin([14, 16]))
    buy_oct = (df["cell_buy"] == 1) & (df["month"] == "2026-10")
    df["buy_h14_16"] = buy_h14_16.astype(int)
    df["buy_oct"] = buy_oct.astype(int)
    df["v1b_skip"] = (buy_h14_16 | buy_oct).astype(int)
    df["oct_all"] = (df["month"] == "2026-10").astype(int)

    feat_cols = [
        "hour",
        "spread_pts",
        "atr_pts",
        "near_atr_cap",
        "cell_month_feb",
        "cell_month_may",
        "cell_mismatch",
        "cell_fragile",
        "cell_buy",
        "cell_sell",
    ]
    for c in feat_cols:
        prior[c] = prior[c].astype(float)
        df[c] = df[c].astype(float)
    # hour flags for AI feat parity with P2
    prior["hour_14"] = (prior["hour"].astype(int) == 14).astype(float)
    prior["hour_16"] = (prior["hour"].astype(int) == 16).astype(float)
    df["hour_14"] = (df["hour"].astype(int) == 14).astype(float)
    df["hour_16"] = (df["hour"].astype(int) == 16).astype(float)
    feats = feat_cols + ["hour_14", "hour_16"]

    Xp = prior[feats].to_numpy()
    yp = prior["y_lose"].astype(int).to_numpy()
    Xt = df[feats].to_numpy()
    scaler = StandardScaler()
    clf = LogisticRegression(class_weight="balanced", C=0.5, max_iter=500)
    clf.fit(scaler.fit_transform(Xp), yp)
    proba = clf.predict_proba(scaler.transform(Xt))[:, 1]
    df["ai_proba"] = proba
    df["ai_would_skip"] = (proba >= AI_THR).astype(int)
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
    # Tip lose med hold ~1.6h — advise on fast SL / near-ATR losers
    if (
        row["win"] == 0
        and row["hold_h"] < 1.5
        and int(row["near_atr_cap"]) == 1
    ):
        return "L8_ADVISE_ABORT_FAST_SL"
    if row["win"] == 0 and row["hold_h"] < 0.5:
        return "L8_ADVISE_ABORT_FLASH_SL"
    return "L8_HOLD"


def run_stack(
    df: pd.DataFrame,
    stack: str,
    use_oct_all: bool,
    use_ai: bool,
    allow_unlatch: bool = True,
) -> list[dict]:
    equity = DEPOSIT
    peak = DEPOSIT
    # Health path = L2det-passed fires (even while L3 halt blocks permit) for unlatch
    health_wins: list[int] = []
    en15_hist: list[float | None] = []
    compress_streak = 0
    halt_latched = False
    en20_pos_streak = 0
    rows_out = []

    for _, row in df.iterrows():
        skip_v1b = int(row["v1b_skip"]) == 1
        skip_oct = use_oct_all and int(row["oct_all"]) == 1
        l2det = skip_v1b or skip_oct
        reasons = []
        if int(row["buy_h14_16"]) == 1:
            reasons.append("L2DET_SKIP_BUY_H14_16")
        if int(row["buy_oct"]) == 1:
            reasons.append("L2DET_SKIP_BUY_OCT")
        if skip_oct and int(row["buy_oct"]) == 0:
            reasons.append("L2DET_SKIP_OCT")
        l2det_reason = "|".join(reasons) if reasons else "FIRE_OK"

        ai_skip = bool(row["ai_would_skip"]) if use_ai else False
        ai_p = float(row["ai_proba"])

        # Pre-update life from existing health (before this fire)
        w15 = np.array(health_wins[-W15:], dtype=float)
        w20 = np.array(health_wins[-W20:], dtype=float)
        w50 = np.array(health_wins[-W50:], dtype=float)
        en15 = en(w15) if len(w15) >= W15 else float("nan")
        ef15 = ef_pp(w15) if len(w15) >= W15 else float("nan")
        en20 = en(w20) if len(w20) >= W20 else float("nan")
        en50 = en(w50) if len(w50) >= W50 else float("nan")
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

        # Trip BELOW on health path
        if len(w20) >= W20 and life == "BELOW":
            halt_latched = True

        # P3 unlatch on health W20 (continues while halted)
        if allow_unlatch and halt_latched and len(w20) >= W20:
            if (not np.isnan(en20)) and en20 > 0 and dd_peak < 20.0:
                en20_pos_streak += 1
            else:
                en20_pos_streak = 0
            if en20_pos_streak >= 2:
                halt_latched = False
                en20_pos_streak = 0

        halt = halt_latched or (dd_peak >= DD_LIMIT)

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
            f"{MAGIC}-DE30-M5-{row['side']}-"
            f"{ot.replace('.', '').replace(':', '').replace(' ', '')}"
        )

        w_ef = ef15
        w_en = en50 if not np.isnan(en50) else en15

        rows_out.append(
            {
                "t": ot[:16],
                "side": row["side"],
                "layer": layer,
                "decision": decision,
                "reason": reason,
                "life": life,
                "f_rec": round(f, 2),
                "w250_EF": "" if np.isnan(w_ef) else round(w_ef, 2),
                "w250_EN": "" if np.isnan(w_en) else round(w_en, 4),
                "ai_proba": round(ai_p, 4),
                "ai_skip": int(ai_skip),
                "model": "L2skip_de40_m5_DISARM" if use_ai else "none",
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

        # Equity only on permitted fires
        if final == 1:
            equity += float(row["pnl"])
            peak = max(peak, equity)

        # Health continues on L2det-passed signals (incl. HALT) for unlatch/life
        if not l2det:
            health_wins.append(int(row["win"]))
            w15b = np.array(health_wins[-W15:], dtype=float)
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
        "EF_prior_pp": round(ef, 3),
        "skip_precision_losers": round(
            sum(1 for r in skips if r["win"] == 0) / len(skips), 4
        )
        if skips
        else None,
        "l8_on_losers": sum(1 for r in l8 if r["win"] == 0),
        "l8_on_winners": sum(1 for r in l8 if r["win"] == 1),
        "final_life": fires[-1]["life"] if fires else None,
        "halt_latched_any": any(r["halt"] for r in rows),
        "ΔE_N_vs_baseline": round(en_v - BASELINE_EN, 4),
    }


def write_ledger(rows: list[dict], path: Path) -> None:
    with path.open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=LEDGER_COLS, extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)


def main() -> None:
    tip = load_tip()
    stacks = {
        "det_v1b": (False, False),
        "det_v1b_oct_all": (True, False),
        "det_v1b_plus_ai_shadow": (False, True),
        "det_v1b_oct_all_plus_ai_shadow": (True, True),
    }
    report = {
        "task": "DE40-M5-AOS-P4",
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "tf": "M5",
        "v1b_rule": "(BUY AND hour in {14,16}) OR (BUY AND month==Oct)",
        "Leak_prior_pp": LEAK * 100,
        "baseline_E_N": BASELINE_EN,
        "magic_research": MAGIC,
        "unlatch": "W20_EN>0 x2 and dd_peak<20%",
        "stacks": {},
    }
    for name, (use_oct, use_ai) in stacks.items():
        rows = run_stack(tip, name, use_oct, use_ai, allow_unlatch=True)
        write_ledger(rows, OUT / f"ledger_{name}.csv")
        report["stacks"][name] = score_ledger(rows)

    # Forever-latch diagnostic (P3 conservative)
    latch_rows = run_stack(tip, "det_v1b_forever_latch", False, False, allow_unlatch=False)
    write_ledger(latch_rows, OUT / "ledger_det_v1b_forever_latch.csv")
    report["stacks"]["det_v1b_forever_latch"] = score_ledger(latch_rows)

    write_ledger(
        run_stack(tip, "det_v1b", False, False, allow_unlatch=True),
        ASSETS / "tapes" / "de40_m5_tip_ledger_v1b_shadow.csv",
    )

    (OUT / "P4_STACK.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
