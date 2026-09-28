"""INF-P4a tests: WF harness + low-threshold L2 shadow."""
from __future__ import annotations

import json
import sys
from pathlib import Path

import pandas as pd
import pytest

TRAIN = Path(__file__).resolve().parent
sys.path.insert(0, str(TRAIN))

from walkforward import assert_no_fit_only_on_decay, expanding_folds  # noqa: E402
from train_l2shadow import MODELS, train_l2shadow  # noqa: E402


def test_expanding_folds_no_decay_only():
    folds = expanding_folds(530, min_train=150, test_block=80)
    assert len(folds) >= 4
    for f in folds:
        assert_no_fit_only_on_decay(f)
        assert f.train_start == 0
        assert f.test_start == f.train_end
        assert f.train_n >= 150


def test_train_shadow_low_skip_and_ledger(tmp_path, monkeypatch):
    # Redirect model root to temp so repeated test runs don't collide
    import train_l2shadow as mod

    monkeypatch.setattr(mod, "MODELS", tmp_path / "L2skip")
    r = mod.train_l2shadow(model_semver="L2skip_test_p92")
    sc = r["scorecard"]
    assert sc["verdict"] == "ACCEPT"
    assert sc["fires_kept_pct_oos"] >= 70  # under-skip preference
    assert sc["skip_rate_oos"] < 0.35
    out = Path(r["out_dir"])
    assert (out / "model.joblib").exists()
    assert (out / "META.json").exists()
    ledger = pd.read_csv(out / "shadow_ledger_oos.csv")
    assert set(ledger["decision"]).issubset({"WOULD_SKIP", "WOULD_FIRE", "ALLOW_UNCERTAIN"})
    assert ledger["shadow_fire"].all()
    # refuse overwrite
    with pytest.raises(FileExistsError):
        mod.train_l2shadow(model_semver="L2skip_test_p92")
