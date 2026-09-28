"""Landing zone: inbox → staging (checksum) or quarantine."""
from __future__ import annotations

import hashlib
import json
import shutil
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path

INFRA_ROOT = Path(__file__).resolve().parents[2]
LANDING = INFRA_ROOT / "landing"
INBOX = LANDING / "inbox"
STAGING = LANDING / "staging"
QUARANTINE = LANDING / "quarantine"
MANIFEST_NAME = "landing_manifest.jsonl"


@dataclass
class LandingRecord:
    filename: str
    sha256: str
    bytes: int
    status: str
    dest: str
    landed_at: str
    note: str = ""


def _sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def _append_manifest(rec: LandingRecord) -> None:
    STAGING.mkdir(parents=True, exist_ok=True)
    with (STAGING / MANIFEST_NAME).open("a", encoding="utf-8") as f:
        f.write(json.dumps(asdict(rec), sort_keys=True) + "\n")


def _known_hashes() -> set[str]:
    path = STAGING / MANIFEST_NAME
    if not path.exists():
        return set()
    out: set[str] = set()
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        row = json.loads(line)
        if row.get("status") == "staged":
            out.add(row["sha256"])
    return out


def land_file(src: Path, *, min_bytes: int = 1) -> LandingRecord:
    """Process one file from inbox (or explicit path). Idempotent on sha256."""
    INBOX.mkdir(parents=True, exist_ok=True)
    STAGING.mkdir(parents=True, exist_ok=True)
    QUARANTINE.mkdir(parents=True, exist_ok=True)

    src = Path(src)
    if not src.is_file():
        raise FileNotFoundError(src)

    now = datetime.now(timezone.utc).isoformat()
    size = src.stat().st_size
    digest = _sha256(src)

    if size < min_bytes:
        dest = QUARANTINE / f"{src.stem}.{digest[:12]}{src.suffix}.empty"
        shutil.copy2(src, dest)
        rec = LandingRecord(src.name, digest, size, "quarantine", str(dest), now, "too_small")
        _append_manifest(rec)
        return rec

    if digest in _known_hashes():
        rec = LandingRecord(src.name, digest, size, "idempotent_skip", "", now, "sha256_already_staged")
        _append_manifest(rec)
        return rec

    dest = STAGING / f"{src.stem}.{digest[:12]}{src.suffix}"
    shutil.copy2(src, dest)
    rec = LandingRecord(src.name, digest, size, "staged", str(dest), now)
    _append_manifest(rec)
    return rec


def process_inbox() -> list[LandingRecord]:
    INBOX.mkdir(parents=True, exist_ok=True)
    results: list[LandingRecord] = []
    for path in sorted(INBOX.iterdir()):
        if path.is_file() and path.name != ".gitkeep":
            results.append(land_file(path))
    return results


if __name__ == "__main__":
    rows = process_inbox()
    for r in rows:
        print(json.dumps(asdict(r)))
    if not rows:
        print("inbox empty")
