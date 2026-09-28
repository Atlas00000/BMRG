"""Structured JSONL logging with correlation ids (INF-P5-T01)."""
from __future__ import annotations

import json
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

INFRA = Path(__file__).resolve().parents[2]
LOG_DIR = INFRA / "artefacts" / "logs"
SERVICES = frozenset({"ingest", "features", "trainer", "scorer", "eval", "obs"})


def new_run_id(prefix: str = "inf") -> str:
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    return f"{prefix}_{stamp}_{uuid.uuid4().hex[:8]}"


def log_path_for(run_id: str) -> Path:
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    return LOG_DIR / f"{run_id}.jsonl"


def emit(
    *,
    run_id: str,
    service: str,
    stage: str,
    msg: str,
    level: str = "INFO",
    event_id: str | None = None,
    model_semver: str | None = None,
    reason_code: str | None = None,
    decision: str | None = None,
    extra: dict[str, Any] | None = None,
    path: Path | None = None,
) -> dict:
    if service not in SERVICES:
        raise ValueError(f"unknown service: {service}")
    rec = {
        "ts": datetime.now(timezone.utc).isoformat(),
        "run_id": run_id,
        "service": service,
        "stage": stage,
        "level": level,
        "msg": msg,
        "event_id": event_id,
        "model_semver": model_semver,
        "reason_code": reason_code,
        "decision": decision,
        "extra": extra or {},
    }
    out = path or log_path_for(run_id)
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(rec, ensure_ascii=False) + "\n")
    latest = LOG_DIR / "LATEST_CORRELATION.jsonl"
    if path is None or path.resolve() != latest.resolve():
        with latest.open("a", encoding="utf-8") as fh:
            fh.write(json.dumps(rec, ensure_ascii=False) + "\n")
    return rec


def read_jsonl(path: Path) -> list[dict]:
    if not path.exists():
        return []
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def trace_event(path: Path, event_id: str, run_id: str | None = None) -> list[dict]:
    rows = read_jsonl(path)
    out = [r for r in rows if r.get("event_id") == event_id]
    if run_id:
        out = [r for r in out if r.get("run_id") == run_id]
    return out


def stages_for_event(path: Path, event_id: str, run_id: str | None = None) -> list[str]:
    return [r["stage"] for r in trace_event(path, event_id, run_id)]
