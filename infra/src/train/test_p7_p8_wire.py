"""INF-P7/P8 promote + retrain loop tests."""
from __future__ import annotations

import json
import sys
from pathlib import Path

TRAIN = Path(__file__).resolve().parent
sys.path.insert(0, str(TRAIN))

from promote import dry_run_fixture, promote, rollback  # noqa: E402
from retrain_loop import run_p7_p8_e2e, write_wire_authorisation  # noqa: E402

INFRA = Path(__file__).resolve().parents[2]


def test_promote_dry_run_fixture():
    r = dry_run_fixture()
    assert r["pass"]


def test_failed_challenger_never_pins():
    r = promote(
        "nope",
        scorecard={
            "verdict": "REJECT",
            "checks": {
                "long_ef_hold": False,
                "fires_ge_70pct": False,
                "fires_ge_50pct": False,
                "no_payoff_trap": True,
                "skip_audit_pass": True,
            },
        },
        dry=True,
    )
    assert r["allowed"] is False


def test_w10_w11_e2e():
    s = run_p7_p8_e2e()
    assert s["verdict"] == "ACCEPT"
    assert s["live_ai_gate_shipped"] is False
    assert s["failed_challenger_blocked"] is True
    assert (INFRA.parent / "doc" / "infra_wiring_plan.md").exists()
    assert (INFRA / "artefacts" / "models" / "L2skip" / "LATEST_LIVE" / "PIN.json").exists()
    assert (INFRA / "artefacts" / "ops" / "WIRE_AUTHORISATION.json").exists()
    exp = INFRA.parents[2] / "Profiles" / "Tester" / "BMRG" / "EXP-P7-T03_export_Harvest_long.set"
    assert exp.exists()
    pin = json.loads(
        (INFRA / "artefacts" / "models" / "L2skip" / "LATEST_LIVE" / "PIN.json").read_text(encoding="utf-8")
    )
    assert pin.get("mode") == "LIVE_WITHHOLD"
    assert pin.get("operator_waiver") is True
