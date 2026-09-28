"""INF-P5b e2e: box queue job + suite pointer."""
from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

QUEUE = Path(__file__).resolve().parent
sys.path.insert(0, str(QUEUE))

from worker import process_one, run_local  # noqa: E402

INFRA = Path(__file__).resolve().parents[2]


def _redis_up() -> bool:
    try:
        import redis

        url = os.environ.get("BMRG_REDIS_URL", "redis://localhost:6379/0")
        r = redis.from_url(url, socket_connect_timeout=2)
        return bool(r.ping())
    except Exception:
        return False


def run() -> dict:
    redis_ok = _redis_up()
    mode = "redis" if redis_ok else "local_bypass"
    if redis_ok:
        # enqueue then process
        from enqueue import enqueue  # noqa: E402

        enq = enqueue("p4_eval")
        job = process_one(timeout=30)
        if job is None:
            job = run_local("p4_eval")
            mode = "local_fallback_empty_queue"
    else:
        enq = {"job": "p4_eval", "note": "redis down — local_bypass"}
        job = run_local("p4_eval")

    box = (INFRA / "BOX.md").read_text(encoding="utf-8")
    report = {
        "task_ids": ["INF-P5-T04", "INF-P5-T05", "INF-P5-T06"],
        "recipe": "INF-P5b_box_tests_agentAccess",
        "queue": {
            "mode": mode,
            "redis_up": redis_ok,
            "enqueue": enq,
            "job": {
                "job_id": (job or {}).get("job_id"),
                "status": (job or {}).get("status"),
                "tester_required": (job or {}).get("tester_required"),
                "result_verdict": ((job or {}).get("result") or {}).get("verdict"),
                "elapsed_s": (job or {}).get("elapsed_s"),
            },
        },
        "box_md_present": "vCPU" in box or "CPU" in box,
        "agent_paths_present": (INFRA / "AGENT_PATHS.md").exists(),
        "verdict": "ACCEPT"
        if (job or {}).get("status") == "ok"
        and ((job or {}).get("result") or {}).get("verdict") == "ACCEPT"
        and (INFRA / "BOX.md").exists()
        and (INFRA / "AGENT_PATHS.md").exists()
        else "REJECT",
    }
    reports = INFRA / "artefacts" / "reports"
    reports.mkdir(parents=True, exist_ok=True)
    (reports / "INF-P5b_scorecard.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    (reports / "LATEST_EVAL.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    return report


if __name__ == "__main__":
    print(json.dumps(run(), indent=2))
