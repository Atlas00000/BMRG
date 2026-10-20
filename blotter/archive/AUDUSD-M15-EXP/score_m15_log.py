"""Score Tester 20261019.log for M15 expansion runs (champ geometry / multi-asset)."""
from __future__ import annotations

import re
from collections import Counter, defaultdict
from pathlib import Path

LOG = Path(
    r"C:\Users\emili\AppData\Roaming\MetaQuotes\Terminal"
    r"\D0E8209F77C8CF37AD8BF550E51FF075\Tester\logs\20261019.log"
)
OUT = Path(__file__).resolve().parent


def load(path: Path) -> str:
    raw = path.read_bytes()
    if raw[:2] == b"\xff\xfe":
        return raw.decode("utf-16-le")
    return raw.decode("utf-8", errors="replace")


START_RE = re.compile(
    r"([A-Z0-9.]+),(M\d+|H\d+|D1): testing of Experts\\BMRG\\BMRG\.ex5 "
    r"from (\S+) 00:00 to (\S+) 00:00 started with inputs:",
)


def score_chunk(c: str, deposit: float = 400.0) -> dict:
    mag = re.search(r"InpMagic=(\d+)", c)
    risk = re.search(r"InpRiskPercent=([0-9.]+)", c)
    aos = re.search(r"InpAOS_Enable=(true|false)", c)
    sh = re.search(r"InpStartHour=([0-9.]+)", c)
    mon = re.search(r"InpTradeMon=(true|false)", c)
    tue = re.search(r"InpTradeTue=(true|false)", c)
    sl = re.search(r"InpSL_Points=([0-9.]+)", c)
    tp = re.search(r"InpTP_Points=([0-9.]+)", c)
    bb = re.search(r"InpBBDev=([0-9.]+)", c)
    finals = re.findall(r"final balance ([\d.]+)", c)
    final = float(finals[-1]) if finals else None
    pnl = (final - deposit) if final is not None else None

    closes = re.findall(
        r"AOS close (TP|SL) \| n=(\d+) life=(\w+) f=([\d.]+) W250 EF=([-\d.]+) EN=([-\d.]+) halt=(\d+)",
        c,
    )
    # engine-only may not have AOS close — use market + deal pattern
    opens = re.findall(r"market (buy|sell) ([\d.]+) ([A-Z0-9.]+) sl:", c)
    # TP/SL from journal without AOS
    tp_sl = re.findall(r"\[BMRG\].*?(take profit|stop loss|TP|SL)", c, re.I)

    # Prefer AOS close if present
    if closes:
        outcomes = [1 if x[0] == "TP" else -1 for x in closes]
        n = len(outcomes)
    else:
        # reconstruct from deal close lines if present
        deal_closes = re.findall(
            r"(take profit|stop loss|sl|tp).*?([\-\d.]+)",
            c,
            re.I,
        )
        # fallback: count market opens only
        n = len(opens)
        outcomes = []

    wr = None
    if closes:
        wr = 100.0 * sum(1 for o in outcomes if o > 0) / n if n else None

    def roll_wr(k: int):
        if not closes or n < k:
            return None
        seq = [1 if x[0] == "TP" else 0 for x in closes]
        series = [100.0 * sum(seq[j - k : j]) / k for j in range(k, n + 1)]
        return (min(series), series[-1], max(series))

    # longest loss streak
    max_l = 0
    streak = 0
    if closes:
        for x in closes:
            if x[0] == "SL":
                streak += 1
                max_l = max(max_l, streak)
            else:
                streak = 0

    # relative drawdown from tester summary
    dd_rel = re.search(r"Relative Drawdown[^\d]*([\d.]+)\s*%", c, re.I | re.S)
    # profit factor
    pf = re.search(r"Profit Factor[^\d]*([\d.]+)", c, re.I)
    # total net from summary
    total_net = re.search(r"Total Net Profit[^\d\-]*([-\d.]+)", c, re.I)

    life = Counter(re.findall(r"life=(\w+)", c))
    return {
        "magic": mag.group(1) if mag else "?",
        "risk": risk.group(1) if risk else "?",
        "aos": aos.group(1) if aos else "?",
        "start": sh.group(1) if sh else "?",
        "mon": mon.group(1) if mon else "?",
        "tue": tue.group(1) if tue else "?",
        "sl": sl.group(1) if sl else "?",
        "tp": tp.group(1) if tp else "?",
        "bb": bb.group(1) if bb else "?",
        "final": final,
        "pnl": pnl,
        "n_aos": len(closes),
        "n_mkt": len(opens),
        "wr": wr,
        "w10": roll_wr(10),
        "w20": roll_wr(20),
        "max_l": max_l,
        "dd_rel": dd_rel.group(1) if dd_rel else None,
        "pf": pf.group(1) if pf else None,
        "total_net": total_net.group(1) if total_net else None,
        "life": dict(life),
    }


def main() -> None:
    print("loading…", LOG, "size", LOG.stat().st_size)
    text = load(LOG)
    starts = list(START_RE.finditer(text))
    print(f"starts={len(starts)}")

    rows = []
    for i, s in enumerate(starts):
        end = starts[i + 1].start() if i + 1 < len(starts) else len(text)
        c = text[s.start() : end]
        sym, tf, a, b = s.group(1), s.group(2), s.group(3), s.group(4)
        sc = score_chunk(c)
        rows.append(
            {
                "i": i,
                "sym": sym,
                "tf": tf,
                "window": f"{a}->{b}",
                **sc,
            }
        )

    # print table
    print(
        f"{'i':>3} {'sym':8} {'tf':4} {'window':28} {'mag':>8} {'aos':5} "
        f"{'risk':>4} {'SL/TP':>7} {'pnl':>8} {'n':>4} {'WR%':>6} "
        f"{'W20min':>7} {'W20last':>7} {'maxL':>4} {'dd%':>6}"
    )
    by_sym = defaultdict(list)
    for r in rows:
        n = r["n_aos"] or r["n_mkt"]
        wr_s = f"{r['wr']:.1f}" if r["wr"] is not None else "—"
        w20 = r["w20"]
        w20min = f"{w20[0]:.0f}" if w20 else "—"
        w20last = f"{w20[1]:.0f}" if w20 else "—"
        pnl = r["pnl"]
        pnl_s = f"{pnl:.1f}" if pnl is not None else "—"
        dd = r["dd_rel"] or "—"
        print(
            f"{r['i']:3d} {r['sym']:8} {r['tf']:4} {r['window']:28} "
            f"{r['magic']:>8} {r['aos']:5} {r['risk']:>4} "
            f"{r['sl']}/{r['tp']:>3} {pnl_s:>8} {n:4d} {wr_s:>6} "
            f"{w20min:>7} {w20last:>7} {r['max_l']:4d} {dd:>6}"
        )
        by_sym[r["sym"]].append(r)

    # summary by symbol (best / latest longish windows)
    print("\n=== by symbol (all runs) ===")
    for sym, rs in sorted(by_sym.items()):
        pnls = [x["pnl"] for x in rs if x["pnl"] is not None]
        wrs = [x["wr"] for x in rs if x["wr"] is not None]
        tfs = Counter(x["tf"] for x in rs)
        print(
            f"{sym:8} runs={len(rs)} tf={dict(tfs)} "
            f"pnl_sum={sum(pnls):.1f} pnl_avg={sum(pnls)/len(pnls) if pnls else 0:.1f} "
            f"wr_avg={sum(wrs)/len(wrs) if wrs else float('nan'):.1f}"
        )

    # dump jsonlite
    import json

    (OUT / "SCORE_SUMMARY.json").write_text(
        json.dumps(rows, indent=2), encoding="utf-8"
    )
    print("wrote", OUT / "SCORE_SUMMARY.json")


if __name__ == "__main__":
    main()
