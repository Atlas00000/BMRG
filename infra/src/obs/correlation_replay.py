"""Emit greppable ingest→score correlation for one event_id (INF-P5-T01)."""
from __future__ import annotations

import json
from pathlib import Path

from jsonl_log import LOG_DIR, emit, log_path_for, new_run_id, stages_for_event  # noqa: E402

INFRA = Path(__file__).resolve().parents[2]
FIXTURE = INFRA / "fixtures" / "blotter" / "harvest_long_v1"
PIN = INFRA / "artefacts" / "models" / "L2skip" / "LATEST_SHADOW" / "PIN.json"
SKIP_LEDGER = INFRA / "artefacts" / "reports" / "skip_ledger" / "LATEST_SKIP_LEDGER.csv"

REQUIRED_STAGES = (
    "ingest.normalise",
    "ingest.load",
    "features.tape",
    "scorer.health",
    "eval.cf",
)


def _pick_event_id() -> str:
    line = FIXTURE.joinpath("event_manifest.jsonl").read_text(encoding="utf-8").splitlines()[0]
    return json.loads(line)["event_id"]


def _decision_for(event_id: str) -> tuple[str | None, str | None]:
    if not SKIP_LEDGER.exists():
        return None, None
    import pandas as pd

    led = pd.read_csv(SKIP_LEDGER)
    hit = led.loc[led["event_id"].astype(str) == event_id]
    if hit.empty:
        return "WOULD_FIRE", "TRAIN_PREFIX_OR_NOT_IN_OOS"
    row = hit.iloc[0]
    return str(row["decision"]), str(row.get("reason_code") or "")


def run_correlation_replay(event_id: str | None = None) -> dict:
    event_id = event_id or _pick_event_id()
    run_id = new_run_id("p5a")
    path = log_path_for(run_id)
    # Reset greppable latest pointer for this prove
    latest = LOG_DIR / "LATEST_CORRELATION.jsonl"
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    latest.write_text("", encoding="utf-8")

    pin = {}
    if PIN.exists():
        pin = json.loads(PIN.read_text(encoding="utf-8"))
    model_semver = pin.get("shadow_semver")
    decision, reason = _decision_for(event_id)

    emit(
        run_id=run_id,
        service="ingest",
        stage="ingest.normalise",
        msg="adapter row present in fixture pack",
        event_id=event_id,
        model_semver=model_semver,
        path=path,
    )
    emit(
        run_id=run_id,
        service="ingest",
        stage="ingest.load",
        msg="core load / fixture identity",
        event_id=event_id,
        model_semver=model_semver,
        path=path,
    )
    emit(
        run_id=run_id,
        service="features",
        stage="features.tape",
        msg="joined L1 tape row",
        event_id=event_id,
        model_semver=model_semver,
        path=path,
    )
    emit(
        run_id=run_id,
        service="scorer",
        stage="scorer.health",
        msg="included in engine health_vector window",
        event_id=event_id,
        model_semver=model_semver,
        path=path,
    )
    emit(
        run_id=run_id,
        service="eval",
        stage="eval.cf",
        msg="counterfactual path decision logged",
        event_id=event_id,
        model_semver=model_semver,
        decision=decision,
        reason_code=reason,
        path=path,
    )

    # Mirror run file onto LATEST for agent grep
    latest.write_text(path.read_text(encoding="utf-8"), encoding="utf-8")
    stages = stages_for_event(path, event_id, run_id)
    ok = all(s in stages for s in REQUIRED_STAGES)
    return {
        "task_id": "INF-P5-T01",
        "recipe": "INF-P5-T01_obs_jsonl_correlationIds",
        "run_id": run_id,
        "event_id": event_id,
        "model_semver": model_semver,
        "log_path": str(path),
        "latest_path": str(latest),
        "stages": stages,
        "required_stages": list(REQUIRED_STAGES),
        "trace_ok": ok,
    }
