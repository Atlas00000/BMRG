"""Split the day's Tester journal into one log per variant (SHADOW / CURRENT), last complete run per symbol.

Usage: python _split_runs.py <start_byte_offset> <suffix>
Variant is read from the run's printed inputs: InpAiOsMode=1 -> SHADOW, 2 -> CURRENT.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
LOG = HERE.parents[5] / "Tester" / "logs" / "20261029.log"
START = re.compile(r"\tTester\t(\S+?),(M\d+) \(.*\): testing of ")


def main() -> None:
    offset, suffix = int(sys.argv[1]), sys.argv[2]
    raw = LOG.read_bytes()[offset:]
    text = raw.decode("utf-16-le", "replace").lstrip("\ufeff")
    runs: list[tuple[str, list[str]]] = []
    for line in text.splitlines():
        m = START.search(line)
        if m:
            runs.append((m.group(1), [line]))
        elif runs:
            runs[-1][1].append(line)

    keep: dict[tuple[str, str], list[str]] = {}
    for sym, lines in runs:
        body = "\n".join(lines)
        if "final balance" not in body:
            continue
        mode = re.search(r"InpAiOsMode=(\d)", body)
        variant = {"1": "SHADOW", "2": "CURRENT"}.get(mode.group(1) if mode else "", "OTHER")
        keep[(variant, sym)] = lines  # last complete run wins

    for variant in ("SHADOW", "CURRENT"):
        chunks = [lines for (v, _), lines in keep.items() if v == variant]
        out = HERE / f"tester_{variant}_{suffix}.log"
        out.write_bytes(("\r\n".join(l for c in chunks for l in c) + "\r\n").encode("utf-16"))
        print(variant, sorted(s for (v, s) in keep if v == variant), "->", out.name)


if __name__ == "__main__":
    main()
