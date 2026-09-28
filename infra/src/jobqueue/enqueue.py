"""Enqueue INF box jobs onto Redis list bmrg:jobs."""
from __future__ import annotations

import argparse
import json
import os
import uuid
from datetime import datetime, timezone
from pathlib import Path

INFRA = Path(__file__).resolve().parents[2]
QUEUE_KEY = "bmrg:jobs"
DEFAULT_REDIS = os.environ.get("BMRG_REDIS_URL", "redis://localhost:6379/0")


def enqueue(job: str, *, redis_url: str = DEFAULT_REDIS) -> dict:
    import redis

    payload = {
        "job_id": f"job_{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}_{uuid.uuid4().hex[:8]}",
        "job": job,
        "enqueued_at": datetime.now(timezone.utc).isoformat(),
    }
    r = redis.from_url(redis_url)
    r.rpush(QUEUE_KEY, json.dumps(payload))
    out = INFRA / "artefacts" / "queue"
    out.mkdir(parents=True, exist_ok=True)
    (out / "LATEST_ENQUEUE.json").write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return payload


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--job", default="p4_eval", choices=["p4_eval", "p2_ingest", "p5a_obs", "features_tape"])
    ap.add_argument("--redis", default=DEFAULT_REDIS)
    args = ap.parse_args()
    print(json.dumps(enqueue(args.job, redis_url=args.redis), indent=2))


if __name__ == "__main__":
    main()
