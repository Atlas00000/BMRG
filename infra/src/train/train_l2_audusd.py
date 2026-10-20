"""Train AUDUSD-native L2skip + export Include/AOS_L2skip_aud.mqh."""
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
BMRG = INFRA.parent
TAPE = INFRA / "artefacts" / "tape" / "AUDUSD_CHAMP_AIOS_TAPE.parquet"
MODELS = INFRA / "artefacts" / "models" / "L2skip_aud"
MQH_OUT = BMRG / "Include" / "AOS_L2skip_aud.mqh"

CAT = ["session_id", "side", "dow_name"]
NUM = ["hour_server", "spread_pts", "month", "week_of_month", "is_mon", "is_fri", "side_buy", "spread_hi"]
# Fixed OHE layout → matches AOS.mqh AUD predict (same indices as INF)
CAT_LISTS = [["LON_NY", "NY"], ["BUY", "SELL"], ["Fri", "Mon", "Thu", "Wed"]]


def _prepare(df: pd.DataFrame) -> pd.DataFrame:
    d = df.copy()
    d = d[d["y_lose"].isin([0, 1])].reset_index(drop=True)
    # Map OTHER session → LON_NY for champ Start13 (rare)
    d.loc[~d["session_id"].isin(["LON_NY", "NY"]), "session_id"] = "LON_NY"
    d["is_mon"] = (d["dow_name"] == "Mon").astype(int)
    d["is_fri"] = (d["dow_name"] == "Fri").astype(int)
    d["side_buy"] = (d["side"] == "BUY").astype(int)
    d["spread_hi"] = (d["spread_pts"] >= d["spread_pts"].median()).astype(int)
    return d


def _pipeline() -> Pipeline:
    pre = ColumnTransformer(
        [
            (
                "cat",
                OneHotEncoder(categories=CAT_LISTS, handle_unknown="ignore"),
                CAT,
            ),
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


def export_mqh(pipe: Pipeline, semver: str, thr: float, uncertain: float, spread_med: float) -> None:
    pre = pipe.named_steps["pre"]
    clf = pipe.named_steps["clf"]
    scaler = pre.named_transformers_["num"]
    coef = clf.coef_[0]
    lines = [
        f"// Auto-generated AUDUSD L2 — {semver} — infra/src/train/train_l2_audusd.py",
        "#ifndef AOS_L2SKIP_AUD_MQH",
        "#define AOS_L2SKIP_AUD_MQH",
        "",
        f'#define AOS_L2AUD_SEMVER      "{semver}"',
        f"#define AOS_L2AUD_THR         {float(thr):.10f}",
        f"#define AOS_L2AUD_UNCERTAIN   {float(uncertain):.10f}",
        f"#define AOS_L2AUD_INTERCEPT   {float(clf.intercept_[0]):.10f}",
        f"#define AOS_L2AUD_N_FEAT      {len(coef)}",
        f"#define AOS_L2AUD_SPREAD_MED  {spread_med:.1f}",
        "",
        "const double AOS_L2AUD_COEF[AOS_L2AUD_N_FEAT] =",
        "  {",
    ]
    for i in range(0, len(coef), 4):
        chunk = ", ".join(f"{c: .10f}" for c in coef[i : i + 4])
        comma = "," if i + 4 < len(coef) else ""
        lines.append(f"   {chunk}{comma}")
    lines += [
        "  };",
        "",
        "const double AOS_L2AUD_NUM_MEAN[8] =",
        "  {",
        "   " + ", ".join(f"{v:.10f}" for v in scaler.mean_) + ",",
        "  };",
        "",
        "const double AOS_L2AUD_NUM_SCALE[8] =",
        "  {",
        "   " + ", ".join(f"{v:.10f}" for v in scaler.scale_) + ",",
        "  };",
        "",
        "#endif // AOS_L2SKIP_AUD_MQH",
        "",
    ]
    MQH_OUT.write_text("\n".join(lines), encoding="utf-8")


def train(
    *,
    skip_quantile: float = 0.90,
    uncertain_band: float = 0.03,
    min_train: int = 50,
    test_block: int = 25,
) -> dict:
    df = _prepare(pd.read_parquet(TAPE))
    n = len(df)
    if n < min_train + test_block:
        raise SystemExit(f"tape too small n={n}; need >= {min_train + test_block}")

    folds = expanding_folds(n, min_train=min_train, test_block=test_block)
    for f in folds:
        assert_no_fit_only_on_decay(f)

    feature_cols = CAT + NUM
    fold_metrics = []
    oos_rows = []
    for f in folds:
        train_df = df.iloc[f.train_start : f.train_end]
        test_df = df.iloc[f.test_start : f.test_end]
        pipe = _pipeline()
        pipe.fit(train_df[feature_cols], train_df["y_lose"].astype(int))
        thr = float(np.quantile(pipe.predict_proba(train_df[feature_cols])[:, 1], skip_quantile))
        proba_te = pipe.predict_proba(test_df[feature_cols])[:, 1]
        y_te = test_df["y_lose"].astype(int).to_numpy()
        try:
            auc = float(roc_auc_score(y_te, proba_te)) if len(np.unique(y_te)) > 1 else float("nan")
        except ValueError:
            auc = float("nan")
        skips = proba_te >= thr
        fold_metrics.append(
            {
                "fold": f.fold_id,
                "train_n": f.train_n,
                "test_n": f.test_n,
                "thr": thr,
                "skip_rate": float(skips.mean()),
                "loser_recall": float((skips & (y_te == 1)).sum() / max((y_te == 1).sum(), 1)),
                "auc": auc,
            }
        )
        for i, (_, row) in enumerate(test_df.iterrows()):
            p = float(proba_te[i])
            d = _decision(p, thr, uncertain_band)
            oos_rows.append(
                {
                    "event_id": row["event_id"],
                    "fold_id": f.fold_id,
                    "y_lose": int(row["y_lose"]),
                    "p_lose": p,
                    "decision": d,
                    "would_skip": d == "WOULD_SKIP",
                }
            )

    pipe_full = _pipeline()
    pipe_full.fit(df[feature_cols], df["y_lose"].astype(int))
    proba_full = pipe_full.predict_proba(df[feature_cols])[:, 1]
    thr_full = float(np.quantile(proba_full, skip_quantile))
    spread_med = float(df["spread_pts"].median())

    oos_df = pd.DataFrame(oos_rows)
    y_oos = oos_df["y_lose"].to_numpy()
    p_oos = oos_df["p_lose"].to_numpy()
    skips_oos = oos_df["would_skip"].to_numpy()
    auc_oos = float(roc_auc_score(y_oos, p_oos)) if len(np.unique(y_oos)) > 1 else float("nan")
    skip_rate_oos = float(skips_oos.mean()) if len(oos_df) else 0.0
    fires_kept = 100.0 * (1.0 - skip_rate_oos)

    semver = f"L2skip_aud_p90_{datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')}"
    out_dir = MODELS / semver
    out_dir.mkdir(parents=True, exist_ok=False)
    joblib.dump(pipe_full, out_dir / "model.joblib")

    meta = {
        "model_semver": semver,
        "symbol": "AUDUSD",
        "layer": "L2",
        "skip_quantile": skip_quantile,
        "uncertain_band": uncertain_band,
        "thr_full_ref": thr_full,
        "n_train_full": n,
        "n_oos": len(oos_df),
        "skip_rate_oos": skip_rate_oos,
        "fires_kept_pct_oos": fires_kept,
        "loser_recall_oos": float((skips_oos & (y_oos == 1)).sum() / max((y_oos == 1).sum(), 1)),
        "auc_oos": auc_oos,
        "folds": fold_metrics,
        "wf": folds_to_jsonable(folds),
        "tape": str(TAPE),
        "created_at": datetime.now(timezone.utc).isoformat(),
        "note": "Small-n AUDUSD FT model; W50 AOS window companion; not EUR INF replace",
    }
    (out_dir / "META.json").write_text(json.dumps(meta, indent=2), encoding="utf-8")
    (out_dir / "metrics.json").write_text(json.dumps(meta, indent=2), encoding="utf-8")
    oos_df.to_csv(out_dir / "shadow_ledger_oos.csv", index=False)

    pin = {"aud_semver": semver, "path": str(out_dir)}
    latest = MODELS / "LATEST"
    latest.mkdir(parents=True, exist_ok=True)
    (latest / "PIN.json").write_text(json.dumps(pin, indent=2), encoding="utf-8")
    (latest / "metrics.json").write_text(json.dumps(meta, indent=2), encoding="utf-8")

    export_mqh(pipe_full, semver, thr_full, uncertain_band, spread_med)

    scorecard = {
        "task": "AUDUSD-L2-TRAIN",
        "semver": semver,
        "n": n,
        "n_oos": len(oos_df),
        "auc_oos": auc_oos,
        "skip_rate_oos": skip_rate_oos,
        "fires_kept_pct_oos": fires_kept,
        "mqh": str(MQH_OUT),
        "verdict": "ACCEPT_FT"
        if fires_kept >= 50 and len(oos_df) >= 40
        else "WATCH_THIN",
    }
    (out_dir / "train_scorecard.json").write_text(json.dumps(scorecard, indent=2), encoding="utf-8")
    return {"meta": meta, "scorecard": scorecard, "semver": semver}


if __name__ == "__main__":
    r = train()
    print(json.dumps(r["scorecard"], indent=2))
