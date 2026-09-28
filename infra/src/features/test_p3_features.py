"""INF-P3 PIT / L1 tape tests."""
from __future__ import annotations

import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pandas as pd
import pytest

FEAT = Path(__file__).resolve().parent
sys.path.insert(0, str(FEAT))

from pit_builder import (  # noqa: E402
    PitContext,
    assert_pit_join,
    build_features,
    leakage_probe,
    parse_ts,
    session_id,
)
from build_l1_tape import OUT_TAPE, build_tape  # noqa: E402


def test_session_algorithm():
    assert session_id(10) == "LON_AM"
    assert session_id(15) == "LON_NY"
    assert session_id(18) == "NY"
    assert session_id(21) == "POST_NY"
    assert session_id(3) == "ASIA"


def test_pit_join_rejects_future():
    entry = datetime(2025, 1, 2, 15, 30, tzinfo=timezone.utc)
    assert_pit_join(entry, entry)
    assert_pit_join(entry, entry - timedelta(minutes=5))
    with pytest.raises(AssertionError):
        assert_pit_join(entry, entry + timedelta(minutes=5))


def test_features_forbid_exit_fields_and_asof():
    entry = datetime(2025, 1, 2, 15, 30, tzinfo=timezone.utc)
    exit_t = entry + timedelta(hours=1)
    feats = build_features(
        PitContext(entry_time=entry, side="BUY", spread_pts=4.0, prior_spreads=[3, 4, 5] * 5)
    )
    leakage_probe(entry, exit_t, feats)
    assert feats["session_id"] == "LON_NY"
    assert feats["is_tue"] is False
    assert "y_lose" not in feats
    assert "exit_reason" not in feats


def test_shifted_label_would_break_naive_future_join():
    """Simulated bug: joining features from exit bar must fail PIT check."""
    entry = datetime(2025, 6, 3, 14, 0, tzinfo=timezone.utc)  # Tuesday
    exit_t = entry + timedelta(hours=2)
    bad_asof = exit_t
    with pytest.raises(AssertionError):
        assert_pit_join(entry, bad_asof)
    feats = build_features(PitContext(entry_time=entry, side="SELL", spread_pts=5.0))
    assert feats["is_tue"] is True


def test_build_tape_accept_bars():
    man = build_tape()
    assert man["accept"]["coverage_ge_0_95"]
    assert man["accept"]["tue_eq_0"]
    assert man["accept"]["session_ge_0_95"]
    assert man["accept"]["no_skips"]
    assert man["n_tape_rows"] == man["n_events_source"]
    assert man["skips_applied"] == 0
    latest = OUT_TAPE / "LATEST_REGIME_TAPE.parquet"
    assert latest.exists()
    df = pd.read_parquet(latest)
    assert len(df) == man["n_joined"]
    assert df["skip_applied"].eq(False).all()
