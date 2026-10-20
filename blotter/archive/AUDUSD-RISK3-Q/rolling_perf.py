"""Extract rolling WR / EF / EN / DD from Risk3 quarterly journal runs."""
from __future__ import annotations

import re
from collections import Counter
from pathlib import Path

LOG = Path(
    r"C:\Users\emili\AppData\Roaming\MetaQuotes\Terminal"
    r"\D0E8209F77C8CF37AD8BF550E51FF075\Tester\logs\20261008.log"
)

# representative Risk 3% runs from score_risk3.py
FOCUS = {32, 36, 38, 40, 41, 42, 43, 44, 46}


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
    print(f"starts={len(starts)}")

    # dump unique AOS-ish line shapes from first focus run
    sample_i = next((i for i in FOCUS if i < len(starts)), None)
    if sample_i is not None:
        end = starts[sample_i + 1].start() if sample_i + 1 < len(starts) else len(text)
        c = text[starts[sample_i].start() : end]
        print("\n--- sample line shapes run", sample_i, "---")
        for line in c.splitlines():
            if any(
                k in line
                for k in (
                    "AOS close",
                    "W250",
                    "W50",
                    "W20",
                    "WR=",
                    "EF=",
                    "EN=",
                    "DD",
                    "drawdown",
                    "life=",
                    "ledger",
                )
            ):
                print(line[:200])
                # only first 25 informative
                if sum(1 for _ in []) >= 0:
                    pass
        # count patterns
        print("AOS close count", len(re.findall(r"AOS close", c)))

    print("\n=== RISK 3% rolling / path summary ===")
    hdr = f"{'i':>3} {'window':28} {'pnl':>8} {'n':>4} {'WR%':>6} {'W250EF':>8} {'W250EN':>8} {'halt':>5} {'f_min':>5}"
    print(hdr)
    for i, s in enumerate(starts):
        if i not in FOCUS:
            continue
        end = starts[i + 1].start() if i + 1 < len(starts) else len(text)
        c = text[s.start() : end]
        risk = re.search(r"InpRiskPercent=([0-9.]+)", c)
        if not risk or float(risk.group(1)) != 3.0:
            # still show if in focus but note risk
            pass
        finals = re.findall(r"final balance ([\d.]+)", c)
        final = float(finals[-1]) if finals else None
        pnl = (final - 400.0) if final is not None else None

        # per-close AOS stats
        closes = re.findall(
            r"AOS close (TP|SL) \| n=(\d+) life=(\w+) f=([\d.]+) W250 EF=([-\d.]+) EN=([-\d.]+) halt=(\d+)",
            c,
        )
        # alternate formats
        if not closes:
            closes_alt = re.findall(
                r"AOS close (TP|SL)[^\n]*",
                c,
            )
            print(f"{i:3d} alt_close_n={len(closes_alt)} ex={closes_alt[-1][:160] if closes_alt else 'none'}")
            # try looser
            closes = re.findall(
                r"AOS close (TP|SL).*?n=(\d+).*?life=(\w+).*?f=([\d.]+).*?W250 EF=([-\d.]+) EN=([-\d.]+).*?halt=(\d+)",
                c,
            )

        tps = sum(1 for x in closes if x[0] == "TP")
        sls = sum(1 for x in closes if x[0] == "SL")
        n = len(closes)
        wr = 100.0 * tps / n if n else 0.0
        # last W250 (may be 0 until filled)
        last_ef = float(closes[-1][4]) if closes else None
        last_en = float(closes[-1][5]) if closes else None
        # any non-zero W250 during run
        nonzero = [(float(x[4]), float(x[5]), int(x[1])) for x in closes if float(x[4]) != 0 or float(x[5]) != 0]
        halt_any = any(int(x[6]) == 1 for x in closes)
        f_min = min(float(x[3]) for x in closes) if closes else None
        f_vals = Counter(x[3] for x in closes)

        # equity path proxy from balance comments if any
        bals = [float(x) for x in re.findall(r"balance[^\d]*([\d.]+)", c, re.I)]
        # market closes sometimes print profit
        # Relative DD from tester footer
        dd_rel = re.search(r"Relative Drawdown.*?([\d.]+)\s*%", c, re.I | re.S)
        dd_abs = re.search(r"Absolute Drawdown.*?([\d.]+)", c, re.I | re.S)
        # equity curve from AOS ledger equity if present
        eqs = [float(x) for x in re.findall(r"equity=([\d.]+)", c)]
        if not eqs:
            eqs = [float(x) for x in re.findall(r"eq=([\d.]+)", c)]

        peak = 400.0
        max_dd_pct = 0.0
        if eqs:
            for e in eqs:
                if e > peak:
                    peak = e
                if peak > 0:
                    max_dd_pct = max(max_dd_pct, 100.0 * (peak - e) / peak)
        elif bals:
            for e in bals:
                if e > peak:
                    peak = e
                if peak > 0:
                    max_dd_pct = max(max_dd_pct, 100.0 * (peak - e) / peak)

        window = f"{s.group(1)}->{s.group(2)}"
        risk_s = risk.group(1) if risk else "?"
        print(
            f"{i:3d} {window:28} {pnl:8.2f} {n:4d} {wr:5.1f}% "
            f"{(last_ef if last_ef is not None else float('nan')):8.2f} "
            f"{(last_en if last_en is not None else float('nan')):8.3f} "
            f"{'Y' if halt_any else 'N':>5} {(f_min if f_min is not None else float('nan')):5.2f} "
            f"risk={risk_s} f={dict(f_vals)} nzW250={len(nonzero)}"
        )
        if dd_rel or dd_abs or max_dd_pct:
            print(
                f"     DD_rel={dd_rel.group(1)+'%' if dd_rel else 'n/a'} "
                f"DD_abs={dd_abs.group(1) if dd_abs else 'n/a'} "
                f"path_DD~{max_dd_pct:.1f}% (from equity/balance lines n={len(eqs) or len(bals)})"
            )
        # rolling W20-ish from last 20 closes if we have TP/SL sequence
        if n >= 20:
            seq = closes[-20:]
            wr20 = 100.0 * sum(1 for x in seq if x[0] == "TP") / 20
            print(f"     rolling last20 WR={wr20:.1f}%  last5={''.join('W' if x[0]=='TP' else 'L' for x in closes[-5:])}")
        elif n:
            print(f"     path={''.join('W' if x[0]=='TP' else 'L' for x in closes)}")


if __name__ == "__main__":
    main()
