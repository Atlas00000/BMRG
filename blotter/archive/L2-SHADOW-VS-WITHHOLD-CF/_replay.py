"""Offline CF: L2 AI LIVE_WITHHOLD vs SHADOW (all fire) on unfiltered engine tapes.

WITHHOLD_IS  = pinned model.joblib on its own training tape (in-sample, optimistic for withhold).
WITHHOLD_OOS = walk-forward shadow_ledger_oos.csv decisions (honest), compared on the same OOS rows.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import joblib
import numpy as np
import pandas as pd

BMRG = Path(__file__).resolve().parents[3]
INFRA = BMRG / "infra"
OUT = Path(__file__).resolve().parent
sys.path.insert(0, str(INFRA / "src" / "train"))

import train_l2_audusd as AUD  # noqa: E402
import train_l2shadow as EUR  # noqa: E402

BOOKS = {
    "EURUSD": {
        "prep": EUR._prepare, "cat": EUR.CAT, "num": EUR.NUM,
        "tape": INFRA / "artefacts/tape/LATEST_REGIME_TAPE.parquet",
        "model": INFRA / "artefacts/models/L2skip/L2skip_inf_p92_20260927_223519",
    },
    "AUDUSD": {
        "prep": AUD._prepare, "cat": AUD.CAT, "num": AUD.NUM,
        "tape": INFRA / "artefacts/tape/AUDUSD_CHAMP_AIOS_TAPE.parquet",
        "model": INFRA / "artefacts/models/L2skip_aud/L2skip_aud_p90_20261008_122523",
    },
}
BWR = 50.0  # RR = 1 on both tapes


def metrics(r: pd.Series, t: pd.Series) -> dict:
    r = r.astype(float).reset_index(drop=True)
    if r.empty:
        return {"n": 0}
    eq = r.cumsum()
    dd = float((eq - eq.cummax()).min())
    month = pd.to_datetime(t.reset_index(drop=True)).dt.strftime("%Y-%m")
    m = r.groupby(month).sum()
    out = {
        "n": int(len(r)),
        "WR": round(100 * float((r > 0).mean()), 1),
        "sum_R": round(float(r.sum()), 2),
        "E_N": round(float(r.mean()), 3),
        "maxDD_R": round(dd, 2),
        "month_hit": round(float((m > 0).mean()), 3),
        "worst_month_R": round(float(m.min()), 2),
    }
    for w in (50, 250):
        if len(r) >= w:
            ef = (r > 0).rolling(w).mean() * 100 - BWR
            en = r.rolling(w).mean()
            out[f"W{w}_EF_min"] = round(float(ef.min()), 1)
            out[f"W{w}_EF_last"] = round(float(ef.iloc[-1]), 1)
            out[f"W{w}_EN_min"] = round(float(en.min()), 3)
            out[f"W{w}_EN_last"] = round(float(en.iloc[-1]), 3)
            out[f"W{w}_pct_below"] = round(100 * float((ef.dropna() <= 0).mean()), 1)
    return out


def run_book(sym: str, cfg: dict) -> tuple[dict, pd.DataFrame]:
    df = cfg["prep"](pd.read_parquet(cfg["tape"]))
    meta = json.loads((cfg["model"] / "META.json").read_text(encoding="utf-8"))
    pipe = joblib.load(cfg["model"] / "model.joblib")
    thr, band = float(meta["thr_full_ref"]), float(meta.get("uncertain_band", 0.03))
    df["p_lose"] = pipe.predict_proba(df[cfg["cat"] + cfg["num"]])[:, 1]
    df["skip_IS"] = df["p_lose"] >= thr + band

    oos = pd.read_csv(cfg["model"] / "shadow_ledger_oos.csv")
    df = df.merge(oos[["event_id", "would_skip"]].rename(columns={"would_skip": "skip_OOS"}),
                  on="event_id", how="left")
    df = df.sort_values("entry_time").reset_index(drop=True)
    t, r = df["entry_time"], df["pnl_r"]
    o = df["skip_OOS"].notna()

    res = {
        "tape_window": [str(t.min()), str(t.max())],
        "thr_skip": round(thr + band, 4),
        "SHADOW_all": metrics(r, t),
        "WITHHOLD_IS": metrics(r[~df["skip_IS"]], t[~df["skip_IS"]]),
        "skip_rate_IS": round(100 * float(df["skip_IS"].mean()), 1),
        "skipped_IS_WR": round(100 * float((r[df["skip_IS"]] > 0).mean()), 1) if df["skip_IS"].any() else None,
        "OOS_rows": int(o.sum()),
        "SHADOW_oos_rows": metrics(r[o], t[o]),
        "WITHHOLD_OOS": metrics(r[o & ~df["skip_OOS"].astype(bool)], t[o & ~df["skip_OOS"].astype(bool)]),
        "skip_rate_OOS": round(100 * float(df.loc[o, "skip_OOS"].astype(bool).mean()), 1),
    }
    q4 = pd.to_datetime(t).dt.month >= 10
    if q4.any():
        res["Q4_skip_rate_IS"] = round(100 * float(df.loc[q4, "skip_IS"].mean()), 1)
        res["Q4_SHADOW"] = metrics(r[q4], t[q4])
        res["Q4_WITHHOLD_IS"] = metrics(r[q4 & ~df["skip_IS"]], t[q4 & ~df["skip_IS"]])

    df["month"] = pd.to_datetime(t).dt.strftime("%Y-%m")
    monthly = df.groupby("month").apply(
        lambda g: pd.Series({
            "n": len(g),
            "R_shadow": g["pnl_r"].sum(),
            "R_withhold_IS": g.loc[~g["skip_IS"], "pnl_r"].sum(),
            "skips_IS": int(g["skip_IS"].sum()),
        }), include_groups=False)
    monthly.insert(0, "symbol", sym)
    return res, monthly.reset_index()


def main() -> None:
    card, months = {}, []
    for sym, cfg in BOOKS.items():
        card[sym], m = run_book(sym, cfg)
        months.append(m)
    (OUT / "SCORECARD.json").write_text(json.dumps(card, indent=2), encoding="utf-8")
    pd.concat(months).to_csv(OUT / "MONTHLY.csv", index=False)
    print(json.dumps(card, indent=1))


if __name__ == "__main__":
    main()
