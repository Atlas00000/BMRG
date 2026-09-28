"""INF-P2 ingest / score tests."""
from __future__ import annotations

import json
import sys
from pathlib import Path

INFRA = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(INFRA / "src" / "ingest"))
sys.path.insert(0, str(INFRA / "src" / "score"))

from mt5_normalise import default_harvest_paths, normalise  # noqa: E402
from load_core import load_pack_dir  # noqa: E402
from health import score_pack_dir  # noqa: E402
from schema_validate import validate  # noqa: E402


def test_normalise_coverage_and_schema():
    log, train, out = default_harvest_paths()
    pack = normalise(log, train, out_dir=out)
    assert pack["stats"]["open_coverage"] >= 0.95
    assert pack["stats"]["n_opens"] >= 520
    m0 = {k: pack["manifests"][0][k] for k in (
        "event_id", "risk_ccy", "equity_at_open", "signal_tag", "exit_reason",
        "magic", "symbol", "side", "sl_points", "volume", "tick_value_per_point",
        "equity_source", "costs_defaulted",
    )}
    validate(m0, "event_manifest.schema.json")
    assert "spread_proxy_3x" in pack["manifests"][0]["costs_defaulted"]
    assert pack["manifests"][0]["cost_component_flags"]["cost_spread"].startswith("defaulted")


def test_idempotent_load():
    log, train, out = default_harvest_paths()
    normalise(log, train, out_dir=out)
    a = load_pack_dir(out)
    b = load_pack_dir(out)
    assert a["n_events"] == b["n_events"] == a["n_pack_manifest"]
    assert a["n_legs"] == b["n_legs"]
    assert b["landed_new"] is False


def test_scorecard_vs_baseline():
    log, train, out = default_harvest_paths()
    normalise(log, train, out_dir=out)
    scored = score_pack_dir(out, leak_policy="baseline_proxy")
    hv = scored["health_vector"]
    assert hv["n"] >= 520
    assert abs(hv["wr_pct"] - 54.5) <= 1.0
    assert abs(hv["r"] - 1.0) <= 0.05
    assert hv["cost_flags_present"] is True
    assert scored["verdict"] == "ACCEPT"
