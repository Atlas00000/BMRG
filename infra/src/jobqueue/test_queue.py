"""INF-P5-T04 queue worker tests."""
from __future__ import annotations

import json
import sys
from pathlib import Path

QUEUE = Path(__file__).resolve().parent
sys.path.insert(0, str(QUEUE))

from worker import run_local  # noqa: E402

INFRA = Path(__file__).resolve().parents[2]


def test_local_p4_eval_job_writes_artefact():
    r = run_local("p4_eval")
    assert r["status"] == "ok"
    assert r["tester_required"] is False
    assert r["result"]["verdict"] == "ACCEPT"
    latest = INFRA / "artefacts" / "queue" / "LATEST_JOB.json"
    assert latest.exists()
    data = json.loads(latest.read_text(encoding="utf-8"))
    assert data["job"] == "p4_eval"
