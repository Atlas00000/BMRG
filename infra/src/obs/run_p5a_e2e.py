"""INF-P5a e2e: correlation JSONL + metrics surface + compose lock check."""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

OBS = Path(__file__).resolve().parent
sys.path.insert(0, str(OBS))

from correlation_replay import run_correlation_replay  # noqa: E402
from metrics import REQUIRED_METRIC_KEYS, build_metrics, metrics_keys_ok  # noqa: E402

INFRA = Path(__file__).resolve().parents[2]
IMAGE_LOCK = INFRA / "IMAGE_LOCK.json"
CF_SCORECARD = INFRA / "artefacts" / "reports" / "INF-P4-T04_cf_scorecard.json"


def _compose_smoke() -> dict:
    """Postgres health + image lock + local service tags present."""
    lock = {}
    if IMAGE_LOCK.exists():
        lock = json.loads(IMAGE_LOCK.read_text(encoding="utf-8"))
    pinned = bool(lock.get("images"))
    tags = [
        lock.get("images", {}).get(k, {}).get("tag")
        for k in ("bmrg_ingest", "bmrg_features", "bmrg_trainer", "bmrg_scorer", "bmrg_eval")
    ]
    tags = [t for t in tags if t]
    images_present = {}
    for tag in tags:
        try:
            r = subprocess.run(
                ["docker", "image", "inspect", tag],
                capture_output=True,
                text=True,
                timeout=30,
                check=False,
            )
            images_present[tag] = r.returncode == 0
        except (FileNotFoundError, subprocess.TimeoutExpired):
            images_present[tag] = False
    pg_ok = False
    compose_cmd = None
    for cmd in (
        ["docker-compose", "ps", "-q", "postgres"],
        ["docker", "compose", "ps", "-q", "postgres"],
    ):
        try:
            r = subprocess.run(
                cmd,
                cwd=str(INFRA),
                capture_output=True,
                text=True,
                timeout=30,
                check=False,
            )
            if r.returncode == 0:
                compose_cmd = " ".join(cmd[:2] if cmd[0] == "docker" else cmd[:1])
                pg_ok = bool(r.stdout.strip())
                break
        except (FileNotFoundError, subprocess.TimeoutExpired):
            continue
    dockerfiles_ok = all(
        (INFRA / "images" / svc / "Dockerfile").exists()
        for svc in ("ingest", "features", "trainer", "scorer", "eval")
    )
    all_images = bool(images_present) and all(images_present.values())
    return {
        "image_lock_present": pinned,
        "image_lock_path": str(IMAGE_LOCK),
        "dockerfiles_ok": dockerfiles_ok,
        "images_present": images_present,
        "postgres_up": pg_ok,
        "compose_cli": compose_cmd,
        "smoke_ok": pinned and dockerfiles_ok and all_images,
    }


def run() -> dict:
    corr = run_correlation_replay()
    metrics = build_metrics()
    compose = _compose_smoke()

    prior_cf = None
    if CF_SCORECARD.exists():
        prior_cf = json.loads(CF_SCORECARD.read_text(encoding="utf-8"))

    keys_ok = metrics_keys_ok(metrics)
    accept = corr["trace_ok"] and keys_ok and compose["smoke_ok"]

    report = {
        "task_ids": ["INF-P5-T01", "INF-P5-T02", "INF-P5-T03"],
        "recipe": "INF-P5a_obs_metrics_compose",
        "correlation": corr,
        "metrics": metrics,
        "required_metric_keys": list(REQUIRED_METRIC_KEYS),
        "compose": compose,
        "prior_cf_ref": "artefacts/reports/INF-P4-T04_cf_scorecard.json",
        "prior_cf_verdict": (prior_cf or {}).get("verdict"),
        "verdict": "ACCEPT" if accept else "REJECT",
    }

    reports = INFRA / "artefacts" / "reports"
    reports.mkdir(parents=True, exist_ok=True)
    (reports / "INF-P5-T01_correlation.json").write_text(
        json.dumps(corr, indent=2), encoding="utf-8"
    )
    (reports / "INF-P5-T02_metrics.json").write_text(
        json.dumps(metrics, indent=2), encoding="utf-8"
    )
    (reports / "INF-P5-T03_compose_smoke.json").write_text(
        json.dumps(compose, indent=2), encoding="utf-8"
    )
    (reports / "INF-P5a_scorecard.json").write_text(
        json.dumps(report, indent=2), encoding="utf-8"
    )
    (reports / "LATEST_EVAL.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    return report


if __name__ == "__main__":
    r = run()
    print(
        json.dumps(
            {
                "verdict": r["verdict"],
                "trace_ok": r["correlation"]["trace_ok"],
                "event_id": r["correlation"]["event_id"],
                "run_id": r["correlation"]["run_id"],
                "metrics_keys": {k: k in r["metrics"] for k in REQUIRED_METRIC_KEYS},
                "FREQUENCY_STALL": r["metrics"]["FREQUENCY_STALL"],
                "fires_kept_pct": r["metrics"]["fires_kept_pct"],
                "feature_null_pct": r["metrics"]["feature_null_pct"],
                "compose": r["compose"],
            },
            indent=2,
        )
    )
