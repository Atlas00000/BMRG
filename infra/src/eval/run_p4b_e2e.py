"""INF-P4b e2e: CF eval + L3/L4 sim."""
from __future__ import annotations

import json
import sys
from pathlib import Path

EVAL = Path(__file__).resolve().parent
sys.path.insert(0, str(EVAL))

from cf_eval import run_cf_eval  # noqa: E402
from l3_l4_sim import apply_l3_over_l2, sim_to_dict, simulate_l3_l4  # noqa: E402

INFRA = Path(__file__).resolve().parents[2]


def run() -> dict:
    cf = run_cf_eval()
    eng = cf["engine"]
    cfc = cf["counterfactual"]

    # Sim on engine path (pre-skip) and on CF path
    sim_engine = simulate_l3_l4(
        w250_ef_pp=eng["w250"].get("w250_ef_pp"),
        w250_e_n=eng["w250"].get("w250_e_n"),
        maxdd_pp=eng["maxdd_pp"],
        fires_90d=None,
    )
    sim_cf = simulate_l3_l4(
        w250_ef_pp=cfc["w250"].get("w250_ef_pp"),
        w250_e_n=cfc["w250"].get("w250_e_n"),
        maxdd_pp=cfc["maxdd_pp"],
        fires_90d=None,
    )

    # Prove L3 outranks: when halted, WOULD_SKIP is not the effective authority
    halt_demo = simulate_l3_l4(
        w250_ef_pp=-1.0,
        w250_e_n=-0.05,
        maxdd_pp=30.0,
        fires_90d=10,
        baseline_fires_90d=60,
    )
    over_skip = apply_l3_over_l2("WOULD_SKIP", halt_demo)
    over_fire = apply_l3_over_l2("WOULD_FIRE", halt_demo)
    l3_outranks_ok = over_skip["l3_outranks"] and over_skip["final_action"] == "HALT_NO_ENTRY"
    l3_outranks_ok = l3_outranks_ok and over_fire["final_action"] == "HALT_NO_ENTRY"

    report = {
        "task_ids": ["INF-P4-T04", "INF-P4-T05"],
        "recipe": "INF-P4-T04_cfEval_plus_INF-P4-T05_L3L4sim",
        "cf": cf,
        "l3_l4_sim": {
            "engine_path": sim_to_dict(sim_engine),
            "cf_path": sim_to_dict(sim_cf),
            "halt_demo": sim_to_dict(halt_demo),
            "apply_examples": {"on_would_skip": over_skip, "on_would_fire": over_fire},
            "l3_outranks_l2": l3_outranks_ok,
        },
        "verdict": "ACCEPT" if cf["verdict"] == "ACCEPT" and l3_outranks_ok else "REJECT",
    }

    reports = INFRA / "artefacts" / "reports"
    reports.mkdir(parents=True, exist_ok=True)
    path = reports / "INF-P4-T04_cf_scorecard.json"
    path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    (reports / "INF-P4-T05_l3l4_sim.json").write_text(
        json.dumps(report["l3_l4_sim"], indent=2), encoding="utf-8"
    )
    (reports / "LATEST_EVAL.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    return report


if __name__ == "__main__":
    r = run()
    print(
        json.dumps(
            {
                "verdict": r["verdict"],
                "cf_verdict": r["cf"]["verdict"],
                "engine_ef": r["cf"]["engine"]["health_vector"]["ef_pp"],
                "cf_ef": r["cf"]["counterfactual"]["health_vector"]["ef_pp"],
                "fires_kept_pct": r["cf"]["counterfactual"]["fires_kept_pct"],
                "deltas": r["cf"]["deltas"],
                "checks": r["cf"]["checks"],
                "warn": r["cf"]["warn"],
                "l3_outranks": r["l3_l4_sim"]["l3_outranks_l2"],
            },
            indent=2,
        )
    )
