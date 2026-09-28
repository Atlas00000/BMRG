"""INF-P4b CF + L3/L4 sim tests."""
from __future__ import annotations

import sys
from pathlib import Path

EVAL = Path(__file__).resolve().parent
sys.path.insert(0, str(EVAL))

from cf_eval import run_cf_eval  # noqa: E402
from l3_l4_sim import apply_l3_over_l2, simulate_l3_l4  # noqa: E402
from run_p4b_e2e import run  # noqa: E402


def test_l3_outranks_l2():
    sim = simulate_l3_l4(w250_ef_pp=-1, w250_e_n=-0.1, maxdd_pp=30, fires_90d=None)
    assert sim.halted
    assert apply_l3_over_l2("WOULD_SKIP", sim)["final_action"] == "HALT_NO_ENTRY"
    assert apply_l3_over_l2("WOULD_FIRE", sim)["l3_outranks"] is True


def test_cf_eval_protect_bar():
    r = run_cf_eval()
    assert r["engine"]["n"] >= 520
    assert r["counterfactual"]["fires_kept_pct"] >= 70
    assert r["checks"]["long_ef_hold"]
    assert r["checks"]["no_payoff_trap"]
    assert r["verdict"] == "ACCEPT"


def test_p4b_e2e():
    r = run()
    assert r["verdict"] == "ACCEPT"
    assert r["l3_l4_sim"]["l3_outranks_l2"] is True
