"""Parity check: INF L2 sklearn vs MQL feature formula."""
from __future__ import annotations

import json
import sys
from pathlib import Path

import joblib
import numpy as np
import pandas as pd

TRAIN = Path(__file__).resolve().parent
sys.path.insert(0, str(TRAIN))
from train_l2shadow import CAT, NUM, _prepare  # noqa: E402

INFRA = Path(__file__).resolve().parents[2]
PIN = INFRA / "artefacts" / "models" / "L2skip" / "LATEST_LIVE" / "PIN.json"
TAPE = INFRA / "artefacts" / "tape" / "LATEST_REGIME_TAPE.parquet"

MEAN = np.array(
    [14.2641509434, 5.5018867925, 5.3490566038, 2.7471698113, 0.2283018868, 0.2396226415, 0.4886792453, 0.5528301887]
)
SCALE = np.array(
    [2.2474383186, 2.9609082343, 3.0295477364, 1.2798295543, 0.4197381747, 0.4268531729, 0.4998718241, 0.4972011375]
)
COEF = np.array(
    [
        0.0324841372,
        -0.0428968683,
        -0.0089619545,
        -0.0014507766,
        -0.0239938683,
        -0.0104442551,
        0.0058568245,
        0.0181685677,
        0.0777826792,
        -0.1195008926,
        0.1515953197,
        0.1239043813,
        -0.0192191452,
        -0.0503656608,
        -0.0077489242,
        0.1715089275,
    ]
)
INTERCEPT = -0.0127389095


def mql_proba(row: pd.Series) -> float:
    x = np.zeros(16)
    x[0] = 1.0 if row["session_id"] == "LON_NY" else 0.0
    x[1] = 1.0 if row["session_id"] == "NY" else 0.0
    x[2] = 1.0 if row["side"] == "BUY" else 0.0
    x[3] = 1.0 if row["side"] == "SELL" else 0.0
    for j, d in enumerate(["Fri", "Mon", "Thu", "Wed"]):
        if row["dow_name"] == d:
            x[4 + j] = 1.0
    raw = np.array(
        [
            row["hour_server"],
            row["spread_pts"],
            row["month"],
            row["week_of_month"],
            row["is_mon"],
            row["is_fri"],
            row["side_buy"],
            row["spread_hi"],
        ],
        dtype=float,
    )
    x[8:] = (raw - MEAN) / SCALE
    z = INTERCEPT + COEF.dot(x)
    return float(1.0 / (1.0 + np.exp(-z)))


def main() -> None:
    pin = json.loads(PIN.read_text(encoding="utf-8"))
    pipe = joblib.load(Path(pin["path"]) / "model.joblib")
    df = _prepare(pd.read_parquet(TAPE))
    proba = pipe.predict_proba(df[CAT + NUM])[:, 1]
    manual = np.array([mql_proba(df.iloc[i]) for i in range(len(df))])
    max_abs = float(np.max(np.abs(proba - manual)))
    ok = max_abs < 1e-6
    report = {
        "semver": pin["live_semver"],
        "n": int(len(df)),
        "max_abs_delta": max_abs,
        "parity_ok": ok,
    }
    out = INFRA / "artefacts" / "reports" / "INF_EA_LIVE_WITHHOLD_parity.json"
    out.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps(report, indent=2))
    if not ok:
        raise SystemExit(1)


def test_l2_mql_parity():
    pin = json.loads(PIN.read_text(encoding="utf-8"))
    pipe = joblib.load(Path(pin["path"]) / "model.joblib")
    df = _prepare(pd.read_parquet(TAPE))
    proba = pipe.predict_proba(df[CAT + NUM])[:, 1]
    manual = np.array([mql_proba(df.iloc[i]) for i in range(len(df))])
    assert float(np.max(np.abs(proba - manual))) < 1e-6


if __name__ == "__main__":
    main()
