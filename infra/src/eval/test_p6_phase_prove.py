"""INF-P6 phase-prove tests."""
from __future__ import annotations

import sys
from pathlib import Path

EVAL = Path(__file__).resolve().parent
sys.path.insert(0, str(EVAL))

from phase_prove import run, run_phase_prove  # noqa: E402

INFRA = Path(__file__).resolve().parents[2]
DOC = INFRA.parent / "doc"


def test_phase_prove_windows_and_metrics():
    r = run_phase_prove()
    assert r["engine"]["n_events"] >= 520
    assert not r["engine"]["w250"].get("thin")
    assert not r["engine"]["w500"].get("thin")
    assert r["frequency"]["fires_kept_pct"] >= 70
    assert r["checks"]["no_payoff_trap"]
    assert r["metrics_verdict"] == "ACCEPT"
    # prove_verdict may REJECT if skip audit finds edge-cell FPs


def test_skip_audit_flags_or_passes():
    r = run_phase_prove()
    assert r["skip_audit"]["n_clusters"] >= 1
    for c in r["skip_audit"]["clusters"]:
        joined = " ".join(c["justification"]).lower()
        if c["justified"]:
            assert "unjustified" not in joined
        else:
            assert "unjustified" in joined


def test_p6_e2e_writes_eligibility():
    s = run()
    assert s["verdict"] == "ACCEPT"
    assert s["wiring_eligibility"] in {"GO", "NO-GO"}
    assert (INFRA / "artefacts" / "reports" / "INF-P6-T01_phaseProve.json").exists()
    assert (INFRA / "artefacts" / "reports" / "INF-P6-T02_skip_audit.md").exists()
    assert (DOC / "infra_wiring_eligibility.md").exists()
    elig = (DOC / "infra_wiring_eligibility.md").read_text(encoding="utf-8")
    assert "FORBIDDEN" in elig
    if s["wiring_eligibility"] == "NO-GO":
        assert "NO-GO" in elig
        assert s["unjustified"]  # expect documented clusters when NO-GO from audit
