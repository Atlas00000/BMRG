"""Parse VPS hosting logs for AUDUSD live attach (8230931)."""
from __future__ import annotations

import re
from pathlib import Path

BASE = Path(
    r"C:\Users\emili\AppData\Roaming\MetaQuotes\Terminal"
    r"\D0E8209F77C8CF37AD8BF550E51FF075\logs"
)
EXP = BASE / "hosting.6917926.experts" / "20261008.log"
TER = BASE / "hosting.6917926.terminal" / "20261008.log"
LOCAL = BASE / "20261008.log"


def load(path: Path) -> str:
    raw = path.read_bytes()
    if raw[:2] == b"\xff\xfe":
        return raw.decode("utf-16-le")
    return raw.decode("utf-8", errors="replace")


def show(label: str, path: Path, keys: tuple[str, ...]) -> None:
    if not path.exists():
        print(f"MISSING {label} {path}")
        return
    t = load(path)
    lines = t.splitlines()
    hit = [ln for ln in lines if any(k.lower() in ln.lower() for k in keys)]
    print(f"\n==== {label} ({path.name}) lines={len(lines)} hits={len(hit)} ====")
    for ln in hit[-150:]:
        print(ln[:240])


def main() -> None:
    keys = (
        "BMRG",
        "AUDUSD",
        "EURUSD",
        "8230931",
        "8230921",
        "AOS",
        "Risk",
        "InpRisk",
        "balance",
        "equity",
        "error",
        "Error",
        "fail",
        "init",
        "magic",
        "migrat",
        "account",
        "lot",
        "trade",
        "position",
        "Expert",
        "initialized",
        "removed",
        "loaded",
        "semver",
        "L2skip",
        "halt",
        "deposit",
    )
    show("VPS experts", EXP, keys)
    show("VPS terminal", TER, keys)
    show("Local terminal", LOCAL, ("AUDUSD", "BMRG", "Virtual Hosting", "28435", "migrat", "VPS"))


if __name__ == "__main__":
    main()
