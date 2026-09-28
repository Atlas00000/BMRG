"""INF-P1 contract + landing + rebuild tests (no live FT)."""
from __future__ import annotations

import json
import sys
import tempfile
from pathlib import Path

import pytest

INFRA = Path(__file__).resolve().parents[2]
SRC = INFRA / "src" / "ingest"
sys.path.insert(0, str(SRC))

from landing import land_file  # noqa: E402
from rebuild_events import rebuild, declared_1r  # noqa: E402
from schema_validate import assert_rejects, validate  # noqa: E402


GOLDEN_LEG = {
    "event_id": "8210204-EURUSD-BUY-20250102153000-2",
    "leg_id": "8210204-EURUSD-BUY-20250102153000-2-L0",
    "symbol": "EURUSD",
    "direction": "long",
    "entry_time": "2025-01-02T15:30:00Z",
    "entry_price": 1.02855,
    "entry_requested": None,
    "exit_time": "2025-01-02T16:03:00Z",
    "exit_price": 1.02555,
    "exit_requested": None,
    "initial_stop": 1.02555,
    "volume": 0.01,
    "pnl_gross_ccy": -3.0,
    "cost_spread_ccy": 0.12,
    "cost_commission_ccy": 0.0,
    "cost_swap_ccy": 0.0,
    "cost_slippage_ccy": 0.0,
    "pnl_net_ccy": -3.12,
    "exit_reason": "SL",
    "level_index": 0,
    "bb_dev": 2.2,
    "spread_points_entry": 4.0,
    "session_ok": True,
    "group_event_id": "8210204-EURUSD-BUY-20250102153000-2",
    "signal_tag": "BB_FADE",
    "costs_defaulted": ["spread_proxy_3x"],
}

GOLDEN_MANIFEST = {
    "event_id": "8210204-EURUSD-BUY-20250102153000-2",
    "risk_ccy": 3.0,
    "equity_at_open": 400.0,
    "signal_tag": "BB_FADE",
    "exit_reason": "SL",
    "magic": 8210204,
    "symbol": "EURUSD",
    "side": "BUY",
    "sl_points": 300.0,
    "volume": 0.01,
    "tick_value_per_point": 1.0,
    "equity_source": "deposit_ref_proxy",
    "costs_defaulted": ["spread_proxy_3x"],
}

GOLDEN_META = {
    "ea_name": "BMRG",
    "ea_version": "1.20",
    "designed_rr": 1.0,
    "risk_definition": "hard_stop_points",
    "regime_filtered": True,
    "baseline_frequency": 60,
    "costs_defaulted": ["spread_proxy_3x"],
    "preset_id": "EDX-P2-T04_SL300_TP300_RR1_champFilters_G0_long",
    "geometry_mode": "G0_SINGLE",
    "symbol": "EURUSD",
    "timeframe": "M5",
    "magic": 8210204,
    "pool_role": "Harvest",
    "sl_points": 300.0,
    "tp_points": 300.0,
}


def test_golden_leg_and_manifest_validate():
    validate(GOLDEN_LEG, "adapter_blotter.schema.json")
    validate(GOLDEN_MANIFEST, "event_manifest.schema.json")
    validate(GOLDEN_META, "ea_metadata.schema.json")


def test_manifest_rejects_missing_equity_and_risk():
    bad = dict(GOLDEN_MANIFEST)
    del bad["equity_at_open"]
    assert_rejects(bad, "event_manifest.schema.json", "equity_at_open")
    bad2 = dict(GOLDEN_MANIFEST)
    del bad2["risk_ccy"]
    assert_rejects(bad2, "event_manifest.schema.json", "risk_ccy")


def test_declared_1r_sl300_lot001():
    assert declared_1r(0.01) == 3.0


def test_landing_idempotent_and_quarantine(tmp_path, monkeypatch):
    import landing as landing_mod

    monkeypatch.setattr(landing_mod, "INBOX", tmp_path / "inbox")
    monkeypatch.setattr(landing_mod, "STAGING", tmp_path / "staging")
    monkeypatch.setattr(landing_mod, "QUARANTINE", tmp_path / "quarantine")
    monkeypatch.setattr(landing_mod, "LANDING", tmp_path)

    good = tmp_path / "inbox" / "sample.csv"
    good.parent.mkdir(parents=True)
    good.write_text("a,b\n1,2\n", encoding="utf-8")
    r1 = land_file(good)
    assert r1.status == "staged"
    r2 = land_file(good)
    assert r2.status == "idempotent_skip"

    empty = tmp_path / "inbox" / "empty.csv"
    empty.write_bytes(b"")
    r3 = land_file(empty)
    assert r3.status == "quarantine"


def test_harvest_rebuild_near_baseline():
    summary = rebuild()
    assert summary["n_manifest"] >= 520
    assert abs(summary["n_delta"]) <= 5  # 530 ±5
    assert summary["sl_points_match_pct"] >= 95.0
    assert 3.0 in summary["risk_ccy_unique"]
    assert summary["deterministic_check"] is True
    out = Path(summary["out_dir"])
    assert (out / "event_manifest.jsonl").exists()
    # spot-validate first lines
    first = json.loads((out / "event_manifest.jsonl").read_text(encoding="utf-8").splitlines()[0])
    validate(first, "event_manifest.schema.json")
    assert "equity_at_open" in first and first["risk_ccy"] > 0
