"""Ops metrics surface for LATEST_EVAL.json (INF-P5-T02)."""
from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

INFRA = Path(__file__).resolve().parents[2]
BASELINE = INFRA / "baselines" / "ENGINE_BASELINE_v1.json"
SKIP_LEDGER = INFRA / "artefacts" / "reports" / "skip_ledger" / "LATEST_SKIP_LEDGER.csv"
TAPE_MANIFEST = INFRA / "artefacts" / "tape" / "LATEST_REGIME_TAPE.manifest.json"
CF_SCORECARD = INFRA / "artefacts" / "reports" / "INF-P4-T04_cf_scorecard.json"
JOINED = INFRA / "artefacts" / "tape" / "harvest_event_features.parquet"


def _feature_null_pct(joined: Path = JOINED) -> dict:
    if not joined.exists():
        return {"feature_null_pct": None, "n_rows": 0, "n_null_cells": 0, "n_cells": 0}
    df = pd.read_parquet(joined)
    n_cells = int(df.shape[0] * df.shape[1])
    n_null = int(df.isna().sum().sum())
    pct = 100.0 * n_null / max(n_cells, 1)
    return {
        "feature_null_pct": round(pct, 4),
        "n_rows": int(len(df)),
        "n_null_cells": n_null,
        "n_cells": n_cells,
    }


def build_metrics(
    *,
    baseline_fires_90d: int = 60,
    fires_90d: int | None = None,
) -> dict:
    """
    Required keys: fire/skip, nulls, stall, cost drift (+ lag placeholder).
    """
    baseline = json.loads(BASELINE.read_text(encoding="utf-8"))
    leak_base = float(
        baseline.get("costs", {}).get("leak_proxy_pp")
        or baseline.get("windows", {}).get("long", {}).get("leak_pp")
        or 2.2
    )

    skip_rate = None
    fires_kept = None
    fire_count = None
    skip_count = None
    model_semver = None
    if SKIP_LEDGER.exists():
        led = pd.read_csv(SKIP_LEDGER)
        n = len(led)
        skip_count = int((led["decision"] == "WOULD_SKIP").sum()) if "decision" in led.columns else 0
        fire_count = n - skip_count
        skip_rate = round(100.0 * skip_count / max(n, 1), 4)
        fires_kept = round(100.0 * fire_count / max(n, 1), 4)
        if "model_semver" in led.columns and len(led):
            model_semver = str(led["model_semver"].iloc[0])

    cf_ef = None
    engine_ef = None
    leak_pp = leak_base
    if CF_SCORECARD.exists():
        cf = json.loads(CF_SCORECARD.read_text(encoding="utf-8"))
        engine_ef = cf["cf"]["engine"]["health_vector"]["ef_pp"]
        cf_ef = cf["cf"]["counterfactual"]["health_vector"]["ef_pp"]
        leak_pp = float(cf["cf"]["engine"]["health_vector"]["leak_pp"])
        if fires_kept is None:
            fires_kept = cf["cf"]["counterfactual"]["fires_kept_pct"]
            skip_rate = cf["cf"]["counterfactual"]["skip_rate_pct"]
            fire_count = cf["cf"]["counterfactual"]["n"]
            skip_count = cf["cf"]["counterfactual"]["n_skipped"]
            model_semver = cf["cf"]["model_semver"]

    nulls = _feature_null_pct()
    tape = {}
    if TAPE_MANIFEST.exists():
        tape = json.loads(TAPE_MANIFEST.read_text(encoding="utf-8"))

    # FREQUENCY_STALL: fires_90d < 50% baseline; use OOS fire share proxy when unset
    if fires_90d is None:
        fires_90d = fire_count
    stall = fires_90d is not None and fires_90d < 0.5 * baseline_fires_90d
    cost_drift_ratio = round(leak_pp / max(leak_base, 1e-9), 6)
    cost_drift_halt = cost_drift_ratio > 1.5

    return {
        "recipe": "INF-P5-T02_obs_metricsSurface_evalJson",
        "model_semver": model_semver,
        "fire_count": fire_count,
        "skip_count": skip_count,
        "skip_rate_pct": skip_rate,
        "fires_kept_pct": fires_kept,
        "feature_null_pct": nulls["feature_null_pct"],
        "n_null_cells": nulls["n_null_cells"],
        "lag_ms_p50": None,
        "lag_note": "host clock delta not instrumented in INF-P5a; key reserved",
        "cost_drift_ratio": cost_drift_ratio,
        "cost_drift_halt": cost_drift_halt,
        "leak_pp": leak_pp,
        "leak_baseline_pp": leak_base,
        "FREQUENCY_STALL": stall,
        "fires_90d": fires_90d,
        "baseline_fires_90d": baseline_fires_90d,
        "engine_ef_pp": engine_ef,
        "cf_ef_pp": cf_ef,
        "tape_coverage": tape.get("coverage"),
        "tape_skips_applied": tape.get("skips_applied", 0),
    }


REQUIRED_METRIC_KEYS = (
    "fire_count",
    "skip_count",
    "fires_kept_pct",
    "feature_null_pct",
    "FREQUENCY_STALL",
    "cost_drift_ratio",
    "lag_ms_p50",
)


def metrics_keys_ok(metrics: dict) -> bool:
    return all(k in metrics for k in REQUIRED_METRIC_KEYS)
