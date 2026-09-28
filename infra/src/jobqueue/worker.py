"""
INF box worker: BLPOP bmrg:jobs, run one heavy job, write artefacts.

Designed for concurrency=1 on the interim 24 GB host (see BOX.md).
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

QUEUE = Path(__file__).resolve().parent
sys.path.insert(0, str(QUEUE))

from jobs import run_job  # noqa: E402

INFRA = Path(__file__).resolve().parents[2]
QUEUE_KEY = "bmrg:jobs"
DEFAULT_REDIS = os.environ.get("BMRG_REDIS_URL", "redis://localhost:6379/0")
OUT = INFRA / "artefacts" / "queue"


def process_one(*, redis_url: str = DEFAULT_REDIS, timeout: int = 5) -> dict | None:
    import redis

    r = redis.from_url(redis_url)
    item = r.blpop(QUEUE_KEY, timeout=timeout)
    if not item:
        return None
    _, raw = item
    payload = json.loads(raw)
    started = datetime.now(timezone.utc).isoformat()
    t0 = time.perf_counter()
    try:
        result = run_job(payload["job"])
        status = "ok"
        err = None
    except Exception as exc:  # noqa: BLE001 — surface to artefact
        result = {}
        status = "error"
        err = repr(exc)
    elapsed = round(time.perf_counter() - t0, 3)
    report = {
        "job_id": payload.get("job_id"),
        "job": payload.get("job"),
        "enqueued_at": payload.get("enqueued_at"),
        "started_at": started,
        "finished_at": datetime.now(timezone.utc).isoformat(),
        "elapsed_s": elapsed,
        "status": status,
        "error": err,
        "result": result,
        "tester_required": False,
        "box_note": "heavy job on INF box; Strategy Tester idle",
    }
    OUT.mkdir(parents=True, exist_ok=True)
    path = OUT / f"{payload.get('job_id', 'job')}.json"
    path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    (OUT / "LATEST_JOB.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    return report


def run_local(job: str) -> dict:
    """Bypass Redis — same artefact contract (CI / no-daemon prove)."""
    started = datetime.now(timezone.utc).isoformat()
    t0 = time.perf_counter()
    result = run_job(job)
    report = {
        "job_id": f"local_{job}",
        "job": job,
        "started_at": started,
        "finished_at": datetime.now(timezone.utc).isoformat(),
        "elapsed_s": round(time.perf_counter() - t0, 3),
        "status": "ok",
        "error": None,
        "result": result,
        "tester_required": False,
        "via": "local_bypass",
    }
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "LATEST_JOB.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    return report


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--once", action="store_true", help="process one job then exit")
    ap.add_argument("--local", metavar="JOB", help="run job without Redis")
    ap.add_argument("--redis", default=DEFAULT_REDIS)
    ap.add_argument("--timeout", type=int, default=5)
    args = ap.parse_args()
    if args.local:
        print(json.dumps(run_local(args.local), indent=2))
        return
    if args.once:
        report = process_one(redis_url=args.redis, timeout=args.timeout)
        print(json.dumps(report or {"status": "empty"}, indent=2))
        return
    while True:
        report = process_one(redis_url=args.redis, timeout=args.timeout)
        if report:
            print(json.dumps({"job_id": report["job_id"], "status": report["status"]}, indent=2))


if __name__ == "__main__":
    main()
