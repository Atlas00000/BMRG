"""Parse VPS hosting logs for live book inventory."""
from __future__ import annotations

import re
from collections import defaultdict
from pathlib import Path

BASE = Path(
    r"C:\Users\emili\AppData\Roaming\MetaQuotes\Terminal"
    r"\D0E8209F77C8CF37AD8BF550E51FF075\logs"
)


def load(path: Path) -> str:
    raw = path.read_bytes()
    if raw[:2] == b"\xff\xfe":
        return raw.decode("utf-16-le")
    return raw.decode("utf-8", errors="replace")


chart_pat = re.compile(r"BMRG \(([^,]+),([^)]+)\)")
magic_pat = re.compile(r"magic[=:\s]+(\d+)", re.I)

files = []
for d in ["hosting.6917926.experts", "hosting.6917926.terminal"]:
    for day in ["20261019", "20261020", "20261021"]:
        p = BASE / d / f"{day}.log"
        if p.exists():
            files.append(p)

symbols: dict[str, dict] = defaultdict(
    lambda: {"magics": set(), "init_lines": [], "trade_lines": []}
)

print("=== TERMINAL ATTACH / EXPERT LINES ===")
for p in files:
    if "terminal" not in p.parts[-2]:
        continue
    text = load(p)
    for ln in text.splitlines():
        low = ln.lower()
        if any(
            k in low
            for k in (
                "expert",
                "bmrg",
                "loaded",
                "initialized",
                "removed",
                "inputs",
                "chart",
                "set file",
            )
        ) and any(
            k in low
            for k in (
                "bmrg",
                "expert",
                "loaded",
                "initialized",
                "removed",
                "apple",
                "eurusd",
                "audusd",
                "uk100",
                "jpn225",
                "usdjpy",
                "de30",
            )
        ):
            if "ping" in low or "ram:" in low:
                continue
            print(f"{p.name}|{ln.strip()[:300]}")

print("\n=== EXPERTS MAGIC / INIT / TRADE ===")
for p in files:
    if "experts" not in p.parts[-2]:
        continue
    text = load(p)
    for ln in text.splitlines():
        m = chart_pat.search(ln)
        if not m:
            continue
        sym, tf = m.group(1), m.group(2)
        key = f"{sym},{tf}"
        mm = magic_pat.search(ln)
        if mm:
            symbols[key]["magics"].add(mm.group(1))
        low = ln.lower()
        keep = any(
            k in low
            for k in (
                "initialized",
                "inpmagic",
                "magic=",
                "magic ",
                "inprisk",
                "risk%",
                "live_withhold",
                "l2skip",
                "semver",
                "aos mode",
                "aos_mode",
                "[bmrg][trade]",
                "aos close",
                "withhold",
                "risk=",
                "f=",
                "ddl",
                "stack",
                "harvest",
                "scale",
            )
        )
        if keep and len(symbols[key]["init_lines"]) < 50:
            symbols[key]["init_lines"].append(f"{p.name}|{ln.strip()[:280]}")
        if "[BMRG][TRADE]" in ln or "AOS close" in ln:
            if len(symbols[key]["trade_lines"]) < 15:
                symbols[key]["trade_lines"].append(f"{p.name}|{ln.strip()[:280]}")

for k in sorted(symbols):
    s = symbols[k]
    print(f"\n## {k}")
    print(f"  magics={sorted(s['magics']) or '?'}")
    for ln in s["init_lines"][:20]:
        print(" ", ln)
    for ln in s["trade_lines"][:8]:
        print("  TRADE", ln)

today = load(BASE / "hosting.6917926.experts" / "20261021.log")
print("\n=== TODAY UNIQUE CHARTS ===")
print(sorted(set(chart_pat.findall(today))))

print("\n=== TODAY FILTERED INIT-LIKE ===")
for ln in today.splitlines():
    if not chart_pat.search(ln):
        continue
    if re.search(
        r"magic|initialized|Risk|LIVE_WITHHOLD|L2skip|semver|AOS_|withhold|Inp|stack|Harvest|SCALE|f=0",
        ln,
        re.I,
    ):
        print(ln[:300])
