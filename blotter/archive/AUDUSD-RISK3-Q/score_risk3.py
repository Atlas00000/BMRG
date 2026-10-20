"""Quarterly / scaling runs: extract Risk% + lots + survival signals."""
from __future__ import annotations

import re
from collections import Counter
from pathlib import Path

LOG = Path(
    r"C:\Users\emili\AppData\Roaming\MetaQuotes\Terminal"
    r"\D0E8209F77C8CF37AD8BF550E51FF075\Tester\logs\20261008.log"
)


def load(path: Path) -> str:
    raw = path.read_bytes()
    if raw[:2] == b"\xff\xfe":
        return raw.decode("utf-16-le")
    return raw.decode("utf-8", errors="replace")


def main() -> None:
    text = load(LOG)
    starts = list(
        re.finditer(
            r"AUDUSD,M5: testing of Experts\\BMRG\\BMRG\.ex5 from (\S+) 00:00 to (\S+) 00:00 started with inputs:",
            text,
        )
    )
    print(f"total starts: {len(starts)}")
    print(
        f"{'i':>3} {'window':28} {'Risk%':>6} {'pnl':>8} {'ord':>4} "
        f"{'lot_avg':>7} {'lot_max':>7} {'halt':>6} {'f_mix':20} tag"
    )

    for i, s in enumerate(starts):
        if i < 31:
            continue
        end = starts[i + 1].start() if i + 1 < len(starts) else len(text)
        c = text[s.start() : end]
        mag = re.search(r"InpMagic=(\d+)", c)
        if not mag or mag.group(1) != "8230921":
            continue
        risk = re.search(r"InpRiskPercent=([0-9.]+)", c)
        finals = re.findall(r"final balance ([\d.]+)", c)
        lots = [float(x) for x in re.findall(r"market (?:buy|sell) ([\d.]+) AUDUSD", c)]
        f_vals = Counter(re.findall(r" f=([\d.]+)", c))
        halt_vals = Counter(re.findall(r"halt=(\d+)", c))
        life = Counter(re.findall(r"life=(\w+)", c))
        final = float(finals[-1]) if finals else None
        dep_m = re.search(r"initial deposit[^\d]*([\d.]+)", c, re.I)
        dep = float(dep_m.group(1)) if dep_m else 400.0
        pnl = (final - dep) if final is not None else None
        lot_avg = sum(lots) / len(lots) if lots else 0.0
        lot_max = max(lots) if lots else 0.0
        halt_n = halt_vals.get("1", 0)
        f_mix = ",".join(f"{k}x{v}" for k, v in sorted(f_vals.items(), key=lambda x: -x[1]))
        window = f"{s.group(1)}->{s.group(2)}"
        # regime tag by known windows
        if window.startswith("2026.05.01") and "2026.08.31" in window:
            tag = "IN_REGIME"
        elif window.startswith("2026.01.01") and "2026.04.30" in window:
            tag = "OFF_Q1"
        elif window.startswith("2025.01.01") and "2025.04.30" in window:
            tag = "OFF_2025Q1"
        elif window.startswith("2025.05.01"):
            tag = "IN_2025"
        elif window.startswith("2025.08.01") and "2025.08.31" in window:
            tag = "OFF_AUG25"
        elif window.startswith("2025.09.01"):
            tag = "THIN_Q4"
        elif window.startswith("2026.01.01") and "2026.10.07" in window:
            tag = "LONG_MIX"
        elif window.startswith("2026.03.01"):
            tag = "MID_MIX"
        else:
            tag = "?"
        risk_s = risk.group(1) if risk else "?"
        life_s = "/".join(f"{k}{v}" for k, v in life.items())
        print(
            f"{i:3d} {window:28} {risk_s:>6} {pnl:8.2f} {len(lots):4d} "
            f"{lot_avg:7.3f} {lot_max:7.3f} {halt_n:6d} {f_mix:20} {tag} [{life_s}]"
        )


if __name__ == "__main__":
    main()
