"""Heavy jobs runnable on INF box (tester idle)."""
from __future__ import annotations

import json
import sys
from pathlib import Path

INFRA = Path(__file__).resolve().parents[2]
QUEUE_OUT = INFRA / "artefacts" / "queue"


def job_p4_eval() -> dict:
    """INF-P4 CF replay — primary heavy prove job for W08."""
    eval_dir = INFRA / "src" / "eval"
    sys.path.insert(0, str(eval_dir))
    from run_p4b_e2e import run  # noqa: E402

    r = run()
    # Preserve CF artefact under queue/; do not leave LATEST_EVAL as the week pointer
    reports = INFRA / "artefacts" / "reports"
    cf_path = reports / "INF-P4-T04_cf_scorecard.json"
    queue_copy = QUEUE_OUT / "p4_eval_scorecard.json"
    QUEUE_OUT.mkdir(parents=True, exist_ok=True)
    if cf_path.exists():
        queue_copy.write_text(cf_path.read_text(encoding="utf-8"), encoding="utf-8")
    return {
        "job": "p4_eval",
        "verdict": r.get("verdict"),
        "cf_ef": r["cf"]["counterfactual"]["health_vector"]["ef_pp"],
        "engine_ef": r["cf"]["engine"]["health_vector"]["ef_pp"],
        "scorecard": str(queue_copy),
    }


def job_p2_ingest() -> dict:
    sys.path.insert(0, str(INFRA / "src" / "ingest"))
    from run_p2_e2e import run  # noqa: E402

    r = run()
    return {"job": "p2_ingest", "verdict": r.get("verdict")}


def job_p5a_obs() -> dict:
    sys.path.insert(0, str(INFRA / "src" / "obs"))
    from run_p5a_e2e import run  # noqa: E402

    r = run()
    return {"job": "p5a_obs", "verdict": r.get("verdict")}


def job_features_tape() -> dict:
    sys.path.insert(0, str(INFRA / "src" / "features"))
    from build_l1_tape import build_tape  # noqa: E402

    r = build_tape()
    return {"job": "features_tape", "n_tape_rows": r.get("n_tape_rows"), "accept": r.get("accept")}


JOBS = {
    "p4_eval": job_p4_eval,
    "p2_ingest": job_p2_ingest,
    "p5a_obs": job_p5a_obs,
    "features_tape": job_features_tape,
}


def run_job(name: str) -> dict:
    if name not in JOBS:
        raise KeyError(f"unknown job: {name}; allowed={sorted(JOBS)}")
    result = JOBS[name]()
    QUEUE_OUT.mkdir(parents=True, exist_ok=True)
    return result
