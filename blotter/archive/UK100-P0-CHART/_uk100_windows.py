"""Side/DOW/streak for dedicated UK100 tip + prior tester runs."""
from __future__ import annotations

from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path
import re
import statistics

LOG = Path(
    r"C:\Users\emili\AppData\Roaming\MetaQuotes\Terminal"
    r"\D0E8209F77C8CF37AD8BF550E51FF075\Tester\logs\20261012.log"
)

WINDOWS = [
    ("TIP", "from 2026.05.01 00:00 to 2026.08.31 00:00 started with inputs"),
    ("PRIOR", "from 2026.01.01 00:00 to 2026.04.30 00:00 started with inputs"),
]

re_open = re.compile(
    r"(\d{4}\.\d{2}\.\d{2} \d{2}:\d{2}:\d{2}).*\[BMRG\]\[TRADE\] OPEN "
    r"(BUY|SELL) lot=([0-9.]+) price=([0-9.]+) sl=([0-9.]+) tp=([0-9.]+)"
)
re_tp = re.compile(
    r"(\d{4}\.\d{2}\.\d{2} \d{2}:\d{2}:\d{2}).*take profit triggered.*UK100"
)
re_sl = re.compile(
    r"(\d{4}\.\d{2}\.\d{2} \d{2}:\d{2}:\d{2}).*stop loss triggered.*UK100"
)
re_eot = re.compile(
    r"(\d{4}\.\d{2}\.\d{2} \d{2}:\d{2}:\d{2}).*position closed due end of test.*UK100"
)
re_pass = re.compile(r"UK100,M15: .* Test passed")
R = 1.25


def parse_dt(s: str) -> datetime:
    return datetime.strptime(s, "%Y.%m.%d %H:%M:%S")


def score(subset, label):
    n = len(subset)
    if not n:
        print(label, "empty")
        return
    wins = sum(1 for t in subset if t["win"])
    wr = wins / n
    EN = wr * (R + 1) - 1
    BM = wr - 1 / (1 + R)
    print(f"\n## {label} n={n} WR={wr*100:.1f}% BM={BM*100:+.1f}pp E_N={EN:+.3f}R")
    wh = [t["hold_h"] for t in subset if t["win"]]
    lh = [t["hold_h"] for t in subset if not t["win"]]
    if wh:
        print(f"  win hold med={statistics.median(wh):.1f}h")
    if lh:
        print(f"  loss hold med={statistics.median(lh):.1f}h")
    for key in ("side", "dow", "month", "hour"):
        bag = defaultdict(list)
        for t in subset:
            bag[t[key]].append(t)
        print(f"  by {key}:")
        for k in sorted(bag, key=lambda x: (isinstance(x, str), x)):
            rows = bag[k]
            if key == "hour" and len(rows) < 3:
                continue
            w = sum(1 for t in rows if t["win"])
            en = (w / len(rows)) * (R + 1) - 1
            print(f"    {k}: n={len(rows)} WR={w/len(rows)*100:.1f}% E_N={en:+.3f}R")
    # streaks
    mw = ml = sw = sl = 0
    for t in subset:
        if t["win"]:
            sw += 1
            sl = 0
            mw = max(mw, sw)
        else:
            sl += 1
            sw = 0
            ml = max(ml, sl)
    print(f"  streaks W/L max={mw}/{ml} exits={Counter(t['exit'] for t in subset)}")
    overnight = sum(1 for t in subset if t["hold_h"] >= 12)
    print(f"  hold>=12h {overnight}/{n}")
    for W in (10, 15, 20):
        if n < W:
            continue
        path = []
        for i in range(W - 1, n):
            window = subset[i - W + 1 : i + 1]
            ww = sum(1 for t in window if t["win"]) / W
            path.append(ww * (R + 1) - 1)
        print(
            f"  W{W}: avgE_N={statistics.mean(path):+.3f}R "
            f"min={min(path):+.3f} max={max(path):+.3f}"
        )


def extract(mark: str):
    in_run = False
    open_side = open_dt = None
    trades = []
    with LOG.open("r", encoding="utf-16", errors="replace") as f:
        for line in f:
            if mark in line:
                in_run = True
                open_side = None
                continue
            if not in_run:
                continue
            if re_pass.search(line):
                break
            mo = re_open.search(line)
            if mo:
                open_dt = parse_dt(mo.group(1))
                open_side = mo.group(2)
                continue
            for kind, rx in (("TP", re_tp), ("SL", re_sl), ("EOT", re_eot)):
                mc = rx.search(line)
                if mc and open_side is not None:
                    close_dt = parse_dt(mc.group(1))
                    if kind != "EOT":
                        trades.append(
                            {
                                "side": open_side,
                                "exit": kind,
                                "win": kind == "TP",
                                "hold_h": (close_dt - open_dt).total_seconds() / 3600.0,
                                "dow": open_dt.strftime("%a"),
                                "hour": open_dt.hour,
                                "month": open_dt.strftime("%Y-%m"),
                            }
                        )
                    open_side = None
                    break
    return trades


def main():
    for label, mark in WINDOWS:
        score(extract(mark), label)


if __name__ == "__main__":
    main()
