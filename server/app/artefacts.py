"""OpenAPI-aligned artefact map (mirrors client/api/fs_bridge.ts)."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class ArtefactRef:
    root: str  # infra | bmrg | client
    parts: tuple[str, ...]
    kind: str = "json"  # json | text | csv | md | jsonl


ARTEFACT_FILES: dict[str, ArtefactRef] = {
    "/api/baseline": ArtefactRef("infra", ("baselines", "ENGINE_BASELINE_v1.json")),
    "/api/health/latest": ArtefactRef("infra", ("artefacts", "reports", "LATEST_EVAL.json")),
    "/api/pin": ArtefactRef("infra", ("artefacts", "models", "L2skip", "LATEST_LIVE", "PIN.json")),
    "/api/pin/shadow": ArtefactRef(
        "infra", ("artefacts", "models", "L2skip", "LATEST_SHADOW", "PIN.json")
    ),
    "/api/pin/prior": ArtefactRef(
        "infra", ("artefacts", "models", "L2skip", "LATEST_LIVE", "PRIOR_PIN.json")
    ),
    "/api/jobs": ArtefactRef("infra", ("artefacts", "queue", "LATEST_JOB.json")),
    "/api/auth": ArtefactRef("infra", ("artefacts", "ops", "WIRE_AUTHORISATION.json")),
    "/api/prove/cf": ArtefactRef("infra", ("artefacts", "reports", "INF-P4-T04_cf_scorecard.json")),
    "/api/prove/skip-audit": ArtefactRef("infra", ("INF-P6-T02_skip_audit.md",), "md"),
    "/api/ledger": ArtefactRef(
        "infra", ("artefacts", "reports", "skip_ledger", "LATEST_SKIP_LEDGER.csv"), "csv"
    ),
    "/api/live/journal": ArtefactRef("client", ("fixtures", "live", "demo_journal.json")),
    "/api/live/status": ArtefactRef("client", ("fixtures", "live", "demo_status.json")),
    "/api/ops/promote/dry-run": ArtefactRef("infra", ("fixtures", "promote", "dry_run.json")),
    "/api/ops/correlation": ArtefactRef(
        "infra", ("artefacts", "logs", "LATEST_CORRELATION.jsonl"), "jsonl"
    ),
    "/api/blotter/current": ArtefactRef("bmrg", ("blotter", "CURRENT.md"), "md"),
    "/api/blotter/index": ArtefactRef("client", ("fixtures", "blotter", "archive_index.json")),
}


def resolve_bmrg_root(explicit: str | None = None) -> Path:
    if explicit:
        return Path(explicit).resolve()
    # server/ is one level under Experts/BMRG
    return Path(__file__).resolve().parents[2]


def resolve_path(bmrg_root: Path, ref: ArtefactRef) -> Path:
    if ref.root == "infra":
        return bmrg_root / "infra" / Path(*ref.parts)
    if ref.root == "client":
        return bmrg_root / "client" / Path(*ref.parts)
    return bmrg_root / Path(*ref.parts)


def content_type(kind: str) -> str:
    if kind == "csv":
        return "text/csv; charset=utf-8"
    if kind == "md":
        return "text/markdown; charset=utf-8"
    if kind == "jsonl":
        return "application/x-ndjson; charset=utf-8"
    return "application/json; charset=utf-8"
