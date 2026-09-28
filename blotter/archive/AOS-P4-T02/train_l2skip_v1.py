"""AOS-P4 offline: labelled matrix + walk-forward L2skip_v1 + shadow CF."""
from __future__ import annotations
import json
from pathlib import Path
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics import precision_score, recall_score, roc_auc_score

ROOT = Path(r"C:\Users\emili\AppData\Roaming\MetaQuotes\Terminal\D0E8209F77C8CF37AD8BF550E51FF075\MQL5\Experts\BMRG")
SRC = ROOT / "blotter/archive/AOS-P2-T03/harvest_long_labeled.csv"
T01 = ROOT / "blotter/archive/AOS-P4-T01"
T02 = ROOT / "blotter/archive/AOS-P4-T02"
T03 = ROOT / "blotter/archive/AOS-P4-T03"
BWR, LEAK, R = 50.0, 2.2, 1.0
BASE_EF = 1.77
BASE_N = 530

def score(outcomes: np.ndarray) -> dict:
    n = len(outcomes)
    if n == 0:
        return dict(n=0, WR=None, BM=None, E_N=None, EF=None, M=None, zone=None)
    tp = int((outcomes == "TP").sum())
    wr = 100.0 * tp / n
    bm = wr - BWR
    en = (wr / 100.0) * (R + 1) - 1
    ef = bm - LEAK
    m = 100 * 1.96 * np.sqrt((wr / 100) * (1 - wr / 100) / n)
    zone = "Below" if ef <= 0 else ("Fragile" if ef <= m else "Robust")
    return dict(n=n, WR=round(wr, 2), BM=round(bm, 2), E_N=round(en, 4), EF=round(ef, 2), M=round(m, 2), zone=zone)

def enrich(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    out["t"] = pd.to_datetime(out["t"], format="%Y.%m.%d %H:%M")
    out["exit_t"] = pd.to_datetime(out["exit_t"], format="%Y.%m.%d %H:%M")
    out["hour"] = out["hour"].astype(int)
    out["spread"] = out["spread"].astype(int)
    out["y_lose"] = (out["outcome"] == "SL").astype(int)
    out["month"] = out["t"].dt.month
    out["week_of_month"] = ((out["t"].dt.day - 1) // 7) + 1
    out["hold_hours"] = (out["exit_t"] - out["t"]).dt.total_seconds() / 3600.0
    out["same_day_exit"] = (out["t"].dt.date == out["exit_t"].dt.date).astype(int)
    out["hour_bucket"] = pd.cut(out["hour"], bins=[11, 14, 16, 18, 21], labels=["H12_14", "H14_16", "H16_18", "H18_20"], include_lowest=True).astype(str)
    out["spread_hi"] = (out["spread"] >= 8).astype(int)
    out["is_mon"] = (out["dow"] == "Mon").astype(int)
    out["is_fri"] = (out["dow"] == "Fri").astype(int)
    out["side_buy"] = (out["side"] == "BUY").astype(int)
    out["event_idx"] = np.arange(1, len(out) + 1)
    return out

def main():
    raw = pd.read_csv(SRC)
    df = enrich(raw)
    # --- T01 dataset ---
    feat_cols_entry = ["hour", "dow", "session", "side", "spread", "month", "week_of_month", "hour_bucket", "spread_hi", "is_mon", "is_fri", "side_buy"]
    keep = ["event_idx", "t", "exit_t", "outcome", "y_lose", "hold_hours", "same_day_exit"] + feat_cols_entry
    ds = df[keep].copy()
    ds.to_csv(T01 / "harvest_train_matrix.csv", index=False)
    bal = {
        "n": int(len(ds)),
        "n_TP": int((ds.outcome == "TP").sum()),
        "n_SL": int((ds.outcome == "SL").sum()),
        "lose_rate": round(float(ds.y_lose.mean()), 4),
        "win_rate": round(float(1 - ds.y_lose.mean()), 4),
        "side_counts": ds.side.value_counts().to_dict(),
        "session_counts": ds.session.value_counts().to_dict(),
        "dow_counts": ds.dow.value_counts().to_dict(),
        "baseline_n": BASE_N,
        "n_ge_baseline": bool(len(ds) >= BASE_N),
        "entry_features": feat_cols_entry,
        "note": "same_day_exit/hold_hours are labels-side diagnostics only — NOT used as entry skip features",
    }
    (T01 / "class_balance.json").write_text(json.dumps(bal, indent=2), encoding="utf-8")

    # --- T02 walk-forward ---
    # Entry-time model features only (no lookahead)
    cat = ["dow", "session", "side", "hour_bucket"]
    num = ["hour", "spread", "month", "week_of_month", "spread_hi", "is_mon", "is_fri", "side_buy"]
    X_all = df[cat + num]
    y_all = df["y_lose"].values
    outcomes = df["outcome"].values

    # Expanding WF: min train 150, test blocks of 80
    min_train, test_block = 150, 80
    folds = []
    start = min_train
    while start < len(df):
        end = min(start + test_block, len(df))
        folds.append((0, start, start, end))  # train 0:start, test start:end
        start = end

    oos_pred = np.full(len(df), np.nan)
    oos_proba = np.full(len(df), np.nan)
    fold_rows = []

    for fi, (tr0, tr1, te0, te1) in enumerate(folds):
        pipe = Pipeline([
            ("pre", ColumnTransformer([
                ("cat", OneHotEncoder(handle_unknown="ignore"), cat),
                ("num", "passthrough", num),
            ])),
            ("clf", LogisticRegression(max_iter=2000, class_weight="balanced", C=0.5)),
        ])
        pipe.fit(X_all.iloc[tr0:tr1], y_all[tr0:tr1])
        proba = pipe.predict_proba(X_all.iloc[te0:te1])[:, 1]
        # threshold: top-k skip ~15% of train predicted lose-prob
        tr_proba = pipe.predict_proba(X_all.iloc[tr0:tr1])[:, 1]
        thr = float(np.quantile(tr_proba, 0.85))  # skip top 15% riskiest
        pred = (proba >= thr).astype(int)
        oos_pred[te0:te1] = pred
        oos_proba[te0:te1] = proba
        yte = y_all[te0:te1]
        fold_rows.append({
            "fold": fi + 1,
            "train_n": tr1 - tr0,
            "test_n": te1 - te0,
            "thr": round(thr, 4),
            "skip_rate": round(float(pred.mean()), 4),
            "loser_recall": round(float(recall_score(yte, pred, zero_division=0)), 4),
            "loser_precision": round(float(precision_score(yte, pred, zero_division=0)), 4),
            "auc": round(float(roc_auc_score(yte, proba)), 4) if len(np.unique(yte)) > 1 else None,
            "test_EF_all": score(outcomes[te0:te1])["EF"],
            "test_EF_kept": score(outcomes[te0:te1][pred == 0])["EF"],
            "test_n_kept": int((pred == 0).sum()),
        })

    mask = ~np.isnan(oos_pred)
    y_oos = y_all[mask]
    p_oos = oos_pred[mask].astype(int)
    proba_oos = oos_proba[mask]
    overall = {
        "model": "L2skip_v1",
        "algo": "LogisticRegression balanced C=0.5 + OHE",
        "features_cat": cat,
        "features_num": num,
        "wf": f"expanding min_train={min_train} test_block={test_block}",
        "n_oos": int(mask.sum()),
        "skip_rate_oos": round(float(p_oos.mean()), 4),
        "loser_recall_oos": round(float(recall_score(y_oos, p_oos, zero_division=0)), 4),
        "loser_precision_oos": round(float(precision_score(y_oos, p_oos, zero_division=0)), 4),
        "auc_oos": round(float(roc_auc_score(y_oos, proba_oos)), 4),
        "folds": fold_rows,
    }

    # Final full-train model for artifact (shadow uses OOS preds only for CF fairness)
    pipe_full = Pipeline([
        ("pre", ColumnTransformer([
            ("cat", OneHotEncoder(handle_unknown="ignore"), cat),
            ("num", "passthrough", num),
        ])),
        ("clf", LogisticRegression(max_iter=2000, class_weight="balanced", C=0.5)),
    ])
    pipe_full.fit(X_all, y_all)
    tr_p = pipe_full.predict_proba(X_all)[:, 1]
    thr_full = float(np.quantile(tr_p, 0.85))
    overall["thr_full_ref"] = round(thr_full, 4)

    import joblib
    joblib.dump({"pipeline": pipe_full, "thr": thr_full, "cat": cat, "num": num, "meta": overall}, T02 / "L2skip_v1.joblib")
    (T02 / "L2skip_v1_metrics.json").write_text(json.dumps(overall, indent=2), encoding="utf-8")
    pd.DataFrame(fold_rows).to_csv(T02 / "wf_folds.csv", index=False)

    # --- T03 shadow counterfactual using OOS predictions only ---
    shadow = df.copy()
    shadow["shadow_skip"] = 0
    shadow.loc[mask, "shadow_skip"] = p_oos
    shadow["shadow_proba"] = np.nan
    shadow.loc[mask, "shadow_proba"] = proba_oos
    shadow["shadow_reason"] = np.where(shadow["shadow_skip"] == 1, "L2skip_v1", "FIRE_OK")
    # actual fires = all (shadow mode); CF = drop skipped
    base = score(outcomes)
    kept = outcomes[shadow["shadow_skip"].values == 0]
    cf = score(kept)
    # also OOS-only region CF
    oos_out = outcomes[mask]
    oos_skip = p_oos
    base_oos = score(oos_out)
    cf_oos = score(oos_out[oos_skip == 0])

    # AL proxy: average loss magnitude = 1R for SL; AL rate among fires
    def al_rate(outc):
        return float((outc == "SL").mean()) if len(outc) else None

    loose = {
        "remaining_n": cf["n"],
        "n_ok": cf["n"] >= 100,
        "EF_cf": cf["EF"],
        "EF_base_labeled": base["EF"],
        "EF_hold_vs_AOS_BASELINE": (cf["EF"] is not None) and (cf["EF"] >= BASE_EF - 1.0),
        "fires_kept_pct": round(100.0 * cf["n"] / BASE_N, 1),
        "freq_stall_warn": cf["n"] < 0.5 * BASE_N,
        "AL_base": round(al_rate(outcomes), 4),
        "AL_cf": round(al_rate(kept), 4),
        "AL_improved": al_rate(kept) < al_rate(outcomes),
        "payoff_trap": (cf["WR"] is not None and base["WR"] is not None and cf["WR"] > base["WR"] and cf["EF"] < base["EF"]),
    }
    shadow_report = {
        "mode": "shadow_counterfactual_OOS_skips",
        "baseline_all": base,
        "cf_apply_skips_all_tape": cf,
        "baseline_oos_region": base_oos,
        "cf_oos_region": cf_oos,
        "skip_count": int(shadow["shadow_skip"].sum()),
        "loose_bar": loose,
        "eligible_for_live_gate": bool(
            loose["n_ok"] and loose["EF_hold_vs_AOS_BASELINE"] and not loose["payoff_trap"] and loose["AL_improved"]
        ),
    }
    shadow.to_csv(T03 / "shadow_decisions.csv", index=False)
    (T03 / "shadow_counterfactual.json").write_text(json.dumps(shadow_report, indent=2), encoding="utf-8")

    print("=== T01 balance ===")
    print(json.dumps(bal, indent=2))
    print("=== T02 overall ===")
    print(json.dumps({k: overall[k] for k in overall if k != "folds"}, indent=2))
    print("=== T02 folds ===")
    print(pd.DataFrame(fold_rows).to_string(index=False))
    print("=== T03 shadow ===")
    print(json.dumps(shadow_report, indent=2))

if __name__ == "__main__":
    main()
