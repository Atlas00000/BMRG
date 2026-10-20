"""Compare AIOS vs engine-only and count AOS interventions in 8230921 chunks."""
from __future__ import annotations

import re
from pathlib import Path

LOG = Path(
    r"C:\Users\emili\AppData\Roaming\MetaQuotes\Terminal"
    r"\D0E8209F77C8CF37AD8BF550E51FF075\Tester\logs\20261008.log"
)
LOG7 = LOG.parent / "20261007.log"
OUT = Path(__file__).resolve().parent / "aos_effect.txt"


def load(path: Path) -> str:
    raw = path.read_bytes()
    if raw[:2] == b"\xff\xfe":
        return raw.decode("utf-16-le")
    return raw.decode("utf-8", errors="replace")


def main() -> None:
    lines: list[str] = []
    aos_kw = re.compile(
        r"AOS|HALT_|derisk|L2skip|WITHHOLD|kill.?switch|Below.frontier|size.?mod",
        re.I,
    )
    texts = [("20261008", load(LOG))]
    if LOG7.exists():
        texts.append(("20261007", load(LOG7)))

    for label, t in texts:
        starts = list(
            re.finditer(
                r"AUDUSD,M5: testing of Experts\\BMRG\\BMRG\.ex5 from (\S+) 00:00 to (\S+) 00:00 started with inputs:",
                t,
            )
        )
        for i, s in enumerate(starts):
            end = starts[i + 1].start() if i + 1 < len(starts) else len(t)
            c = t[s.start() : end]
            mag = re.search(r"InpMagic=(\d+)", c)
            if not mag:
                continue
            mval = mag.group(1)
            if mval not in ("8230921", "8230501", "8230901", "8230502"):
                continue
            aos = re.search(r"InpAOS_Enable=(true|false)", c)
            mode = re.search(r"InpAiOsMode=(\d+)", c)
            finals = re.findall(r"final balance ([\d.]+)", c)
            trades = len(re.findall(r"market (?:buy|sell) [\d.]+ AUDUSD sl:", c))
            hits = []
            for ln in c.splitlines():
                if aos_kw.search(ln) and "InpAOS" not in ln and "InpAi" not in ln:
                    hits.append(ln)
            lines.append(
                f"{label} [{i}] {s.group(1)}->{s.group(2)} mag={mval} "
                f"AOS={aos.group(1) if aos else '?'} mode={mode.group(1) if mode else '?'} "
                f"orders={trades} final={finals[-1] if finals else '?'} "
                f"aos_hits={len(hits)}"
            )
            for h in hits[:20]:
                lines.append("  " + h[:180])

    OUT.write_text("\n".join(lines), encoding="utf-8")
    print("wrote", OUT.name, "n_lines", len(lines))


if __name__ == "__main__":
    main()
