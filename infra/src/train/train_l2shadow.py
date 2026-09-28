"""
Train L2 shadow challenger with LOW skip bar (prefer under-skipping).

Skip if P(lose) >= train quantile threshold (default p92 → ~8% skips).
Near-threshold band → ALLOW_UNCERTAIN (still fire in shadow).
Never overwrites prior model_semver artefacts.
"""
from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

_TRAIN = Path(__file__).resolve().parent
sys.path.insert(0, str(_TRAIN))
from walkforward import assert_no_fit_only_on_decay, expanding_folds, folds_to_jsonable  # noqa: E402

INFRA = Path(__file__).resolve().parents[2]
TAPE = INFRA / "artefacts" / "tape" / "LATEST_REGIME_TAPE.parquet"
MODELS = INFRA / "artefacts" / "models" / "L2skip"

CAT = ["session_id", "side", "dow_name"]
NUM = ["hour_server", "spread_pts", "month", "week_of_month", "is_mon", "is_fri", "side_buy", "spread_hi"]


def _prepare(df: pd.DataFrame) -> pd.DataFrame:
    d = df.copy()
    d = d[d["y_lose"].isin([0, 1])].reset_index(drop=True)
    d["is_mon"] = (d["dow_name"] == "Mon").astype(int)
    d["is_fri"] = (d["dow_name"] == "Fri").astype(int)
    d["side_buy"] = (d["side"] == "BUY").astype(int)
    d["spread_hi"] = (d["spread_pts"] >= d["spread_pts"].median()).astype(int)
    d["hour_bucket"] = pd.cut(
        d["hour_server"], bins=[-1, 13, 16, 19, 24], labels=["H12_13", "H14_16", "H17_19", "H20p"]
    ).astype(str)
    return d


def _pipeline() -> Pipeline:
    pre = ColumnTransformer(
        [
            ("cat", OneHotEncoder(handle_unknown="ignore"), CAT),
            ("num", StandardScaler(), NUM),
        ]
    )
    clf = LogisticRegression(
        class_weight="balanced",
        C=0.5,
        max_iter=500,
        solver="lbfgs",
    )
    return Pipeline([("pre", pre), ("clf", clf)])


def _decision(proba: float, thr: float, uncertain_band: float = 0.03) -> str:
    if proba >= thr + uncertain_band:
        return "WOULD_SKIP"
    if proba >= thr - uncertain_band:
        return "ALLOW_UNCERTAIN"
    return "WOULD_FIRE"


def train_l2shadow(
    *,
    tape_path: Path = TAPE,
    skip_quantile: float = 0.92,
    uncertain_band: float = 0.03,
    model_semver: str | None = None,
) -> dict:
    """
    skip_quantile high → fewer skips (protect-don't-overfilter).
    Default 0.92 ≈ top 8% lose-proba on train.
    """
    df = _prepare(pd.read_parquet(tape_path))
    n = len(df)
    folds = expanding_folds(n, min_train=150, test_block=80)
    for f in folds:
        assert_no_fit_only_on_decay(f)

    oos_rows: list[dict] = []
    fold_metrics: list[dict] = []
    feature_cols = CAT + NUM

    for f in folds:
        train = df.iloc[f.train_start : f.train_end]
        test = df.iloc[f.test_start : f.test_end]
        pipe = _pipeline()
        pipe.fit(train[feature_cols], train["y_lose"].astype(int))
        proba_tr = pipe.predict_proba(train[feature_cols])[:, 1]
        thr = float(np.quantile(proba_tr, skip_quantile))
        proba_te = pipe.predict_proba(test[feature_cols])[:, 1]
        y_te = test["y_lose"].astype(int).to_numpy()
        try:
            auc = float(roc_auc_score(y_te, proba_te)) if len(np.unique(y_te)) > 1 else float("nan")
        except ValueError:
            auc = float("nan")

        skips = proba_te >= thr
        skip_rate = float(skips.mean())
        if skips.any():
            loser_recall = float(((skips) & (y_te == 1)).sum() / max((y_te == 1).sum(), 1))
            loser_precision = float(((skips) & (y_te == 1)).sum() / max(skips.sum(), 1))
        else:
            loser_recall = 0.0
            loser_precision = 0.0

        fold_metrics.append(
            {
                "fold": f.fold_id,
                "train_n": f.train_n,
                "test_n": f.test_n,
                "thr": thr,
                "skip_rate": skip_rate,
                "loser_recall": loser_recall,
                "loser_precision": loser_precision,
                "auc": auc,
            }
        )

        for i, (idx, row) in enumerate(test.iterrows()):
            p = float(proba_te[i])
            decision = _decision(p, thr, uncertain_band)
            # Shadow: engine still fires always
            oos_rows.append(
                {
                    "event_id": row["event_id"],
                    "fold_id": f.fold_id,
                    "y_lose": int(row["y_lose"]),
                    "p_lose": p,
                    "thr": thr,
                    "decision": decision,
                    "would_skip": decision == "WOULD_SKIP",
                    "shadow_fire": True,
                    "reason_code": (
                        "P_LOSE_GE_THR"
                        if decision == "WOULD_SKIP"
                        else "NEAR_THR_ALLOW"
                        if decision == "ALLOW_UNCERTAIN"
                        else "P_LOSE_LT_THR"
                    ),
                }
            )

    # Fit final model on all scoreable rows for artefact (shadow challenger)
    pipe_full = _pipeline()
    pipe_full.fit(df[feature_cols], df["y_lose"].astype(int))
    proba_full = pipe_full.predict_proba(df[feature_cols])[:, 1]
    thr_full = float(np.quantile(proba_full, skip_quantile))

    # Full-sample shadow ledger (for LATEST) using full thr — report OOS ledger separately
    ledger_all = []
    for pos in range(len(df)):
        row = df.iloc[pos]
        p = float(proba_full[pos])
        decision = _decision(p, thr_full, uncertain_band)
        ledger_all.append(
            {
                "event_id": row["event_id"],
                "y_lose": int(row["y_lose"]),
                "p_lose": p,
                "thr": thr_full,
                "decision": decision,
                "would_skip": decision == "WOULD_SKIP",
                "shadow_fire": True,
                "reason_code": (
                    "P_LOSE_GE_THR"
                    if decision == "WOULD_SKIP"
                    else "NEAR_THR_ALLOW"
                    if decision == "ALLOW_UNCERTAIN"
                    else "P_LOSE_LT_THR"
                ),
                "split": "full_ref",
            }
        )

    oos_df = pd.DataFrame(oos_rows)
    skip_rate_oos = float(oos_df["would_skip"].mean()) if len(oos_df) else 0.0
    n_oos = len(oos_df)
    y_oos = oos_df["y_lose"].to_numpy()
    p_oos = oos_df["p_lose"].to_numpy()
    auc_oos = float(roc_auc_score(y_oos, p_oos)) if len(np.unique(y_oos)) > 1 else float("nan")
    skips_oos = oos_df["would_skip"].to_numpy()
    loser_recall_oos = float((skips_oos & (y_oos == 1)).sum() / max((y_oos == 1).sum(), 1))
    loser_precision_oos = float((skips_oos & (y_oos == 1)).sum() / max(skips_oos.sum(), 1)) if skips_oos.any() else 0.0

    fires_kept_pct = 100.0 * (1.0 - skip_rate_oos)
    semver = model_semver or f"L2skip_inf_p92_{datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')}"
    out_dir = MODELS / semver
    if out_dir.exists():
        raise FileExistsError(f"refuse overwrite: {out_dir}")
    out_dir.mkdir(parents=True)

    joblib.dump(pipe_full, out_dir / "model.joblib")
    meta = {
        "model_semver": semver,
        "layer": "L2",
        "mode": "shadow",
        "skip_quantile": skip_quantile,
        "uncertain_band": uncertain_band,
        "thr_full_ref": thr_full,
        "algo": "LogisticRegression balanced C=0.5 + OHE",
        "features_cat": CAT,
        "features_num": NUM,
        "n_train_full": n,
        "n_oos": n_oos,
        "skip_rate_oos": skip_rate_oos,
        "fires_kept_pct_oos": fires_kept_pct,
        "loser_recall_oos": loser_recall_oos,
        "loser_precision_oos": loser_precision_oos,
        "auc_oos": auc_oos,
        "folds": fold_metrics,
        "wf": folds_to_jsonable(folds),
        "created_at": datetime.now(timezone.utc).isoformat(),
        "parent_semver": None,
        "policy": "default_allow; skip only when p_lose >= thr; near-thr ALLOW_UNCERTAIN",
    }
    (out_dir / "META.json").write_text(json.dumps(meta, indent=2), encoding="utf-8")
    (out_dir / "metrics.json").write_text(json.dumps(meta, indent=2), encoding="utf-8")
    oos_df.to_csv(out_dir / "shadow_ledger_oos.csv", index=False)
    pd.DataFrame(ledger_all).to_csv(out_dir / "shadow_ledger_full.csv", index=False)
    with (out_dir / "shadow_ledger_oos.jsonl").open("w", encoding="utf-8") as f:
        for row in oos_rows:
            f.write(json.dumps(row) + "\n")

    # Agent-facing latest pointers (copy metrics, do not overwrite model dir)
    latest_dir = MODELS / "LATEST_SHADOW"
    latest_dir.mkdir(parents=True, exist_ok=True)
    (latest_dir / "PIN.json").write_text(
        json.dumps({"shadow_semver": semver, "path": str(out_dir)}, indent=2), encoding="utf-8"
    )
    (latest_dir / "metrics.json").write_text(json.dumps(meta, indent=2), encoding="utf-8")
    oos_df.to_csv(latest_dir / "shadow_ledger_oos.csv", index=False)

    reports = INFRA / "artefacts" / "reports"
    reports.mkdir(parents=True, exist_ok=True)
    scorecard = {
        "task_id": "INF-P4-T02",
        "recipe": "INF-P4-T02_train_L2shadow_skipRangeHighVol_harvest",
        "model_semver": semver,
        "skip_rate_oos": skip_rate_oos,
        "fires_kept_pct_oos": fires_kept_pct,
        "auc_oos": auc_oos,
        "n_oos": n_oos,
        "n_remaining_if_skip": int(n_oos * (1 - skip_rate_oos)),
        "protect_bar": {
            "prefer_under_skip": True,
            "warn_fires_below_70pct": fires_kept_pct < 70,
            "stall_fires_below_50pct": fires_kept_pct < 50,
        },
        "folds": fold_metrics,
        "verdict": "ACCEPT"
        if fires_kept_pct >= 50 and meta["n_oos"] >= 100
        else "REJECT",
    }
    (out_dir / "train_scorecard.json").write_text(json.dumps(scorecard, indent=2), encoding="utf-8")
    (reports / "INF-P4-T02_train_scorecard.json").write_text(json.dumps(scorecard, indent=2), encoding="utf-8")
    return {"meta": meta, "scorecard": scorecard, "out_dir": str(out_dir)}


if __name__ == "__main__":
    r = train_l2shadow()
    print(json.dumps(r["scorecard"], indent=2))
