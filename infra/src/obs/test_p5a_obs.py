"""INF-P5a observability + compose lock tests."""
from __future__ import annotations

import json
import sys
from pathlib import Path

OBS = Path(__file__).resolve().parent
sys.path.insert(0, str(OBS))

from correlation_replay import REQUIRED_STAGES, run_correlation_replay  # noqa: E402
from jsonl_log import stages_for_event  # noqa: E402
from metrics import REQUIRED_METRIC_KEYS, build_metrics, metrics_keys_ok  # noqa: E402
from run_p5a_e2e import run  # noqa: E402

INFRA = Path(__file__).resolve().parents[2]


def test_correlation_ingest_to_score():
    r = run_correlation_replay()
    assert r["trace_ok"]
    stages = stages_for_event(Path(r["log_path"]), r["event_id"], r["run_id"])
    for s in REQUIRED_STAGES:
        assert s in stages
    latest = INFRA / "artefacts" / "logs" / "LATEST_CORRELATION.jsonl"
    text = latest.read_text(encoding="utf-8")
    assert r["event_id"] in text
    assert r["run_id"] in text


def test_metrics_surface_keys():
    m = build_metrics()
    assert metrics_keys_ok(m)
    for k in REQUIRED_METRIC_KEYS:
        assert k in m
    assert m["FREQUENCY_STALL"] is False or m["FREQUENCY_STALL"] is True
    assert m["fires_kept_pct"] is not None and m["fires_kept_pct"] >= 50


def test_p5a_e2e_and_image_lock():
    lock = INFRA / "IMAGE_LOCK.json"
    assert lock.exists()
    data = json.loads(lock.read_text(encoding="utf-8"))
    assert "postgres" in data["images"]
    assert "python_base" in data["images"]
    for svc in ("ingest", "features", "trainer", "scorer", "eval"):
        assert (INFRA / "images" / svc / "Dockerfile").exists()
    r = run()
    assert r["verdict"] == "ACCEPT"
    latest = json.loads((INFRA / "artefacts" / "reports" / "LATEST_EVAL.json").read_text(encoding="utf-8"))
    assert "metrics" in latest
    assert "FREQUENCY_STALL" in latest["metrics"]
