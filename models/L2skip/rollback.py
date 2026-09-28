#!/usr/bin/env python3
"""Pin rollback for models/L2skip. Usage: python rollback.py [to_version]"""
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

STORE = Path(__file__).resolve().parent


def main() -> None:
    to = sys.argv[1] if len(sys.argv) > 1 else "L2skip_v0_engine"
    live = json.loads((STORE / "LIVE.json").read_text(encoding="utf-8"))
    fr = live.get("pinned_version")
    if not (STORE / "versions" / to).exists():
        raise SystemExit(f"missing version {to}")
    live["rollback_of"] = fr
    live["pinned_version"] = to
    live["pinned_at"] = datetime.now(timezone.utc).isoformat()
    live["note"] = f"Rollback {fr} -> {to}"
    (STORE / "LIVE.json").write_text(json.dumps(live, indent=2), encoding="utf-8")
    entry = {"ts": live["pinned_at"], "action": "ROLLBACK", "from": fr, "to": to}
    with (STORE / "rollback_log.jsonl").open("a", encoding="utf-8") as f:
        f.write(json.dumps(entry) + "\n")
    print(json.dumps(live, indent=2))


if __name__ == "__main__":
    main()
