"""Extract UK100 trade profile + rolling windows from 20261012 Tester log."""
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

# Focus on the longest UK100 run (starts ~line 276366)
START_MARK = "from 2024.01.01 00:00 to 2026.08.31 00:00 started with inputs"
TIP_FROM = datetime(2026, 5, 1)
PRIOR_TO = datetime(2026, 4, 30, 23, 59, 59)

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


def parse_dt(s: str) -> datetime:
    return datetime.strptime(s, "%Y.%m.%d %H:%M:%S")


def main():
    in_run = False
    open_side = None
    open_dt = None
    open_px = None
    trades = []

    with LOG.open("r", encoding="utf-16", errors="replace") as f:
        for line in f:
            if START_MARK in line:
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
                open_px = float(mo.group(4))
                continue

            for kind, rx in (("TP", re_tp), ("SL", re_sl), ("EOT", re_eot)):
                mc = rx.search(line)
                if mc and open_side is not None:
                    close_dt = parse_dt(mc.group(1))
                    hold_h = (close_dt - open_dt).total_seconds() / 3600.0
                    win = kind == "TP"
                    # designed R units
                    r = 1.25 if win else (-1.0 if kind == "SL" else 0.0)
                    # rough $ at 0.1 lot: index pts * $0.10/pt (UK100 CFD proxy)
                    if kind == "TP":
                        pnl = 31.25 * 0.10  # 3125 pts * 0.01 = 31.25 idx
                    elif kind == "SL":
                        pnl = -25.0 * 0.10
                    else:
                        # EOT: small residual from open
                        pnl = None
                    trades.append(
                        {
                            "open": open_dt,
                            "close": close_dt,
                            "side": open_side,
                            "exit": kind,
                            "hold_h": hold_h,
                            "win": win if kind != "EOT" else None,
                            "r": r if kind != "EOT" else None,
                            "pnl": pnl,
                            "dow": open_dt.strftime("%a"),
                            "hour": open_dt.hour,
                            "month": open_dt.strftime("%Y-%m"),
                        }
                    )
                    open_side = None
                    break

    closed = [t for t in trades if t["exit"] != "EOT"]
    print(f"total trades={len(trades)} closed={len(closed)} eot={len(trades)-len(closed)}")

    def score(subset, label):
        if not subset:
            print(f"\n## {label}: empty")
            return
        n = len(subset)
        wins = sum(1 for t in subset if t["win"])
        losses = n - wins
        wr = wins / n
        R = 1.25
        BWR = 1 / (1 + R)
        BM = wr - BWR
        EN = wr * (R + 1) - 1
        leak = 0.029
        EF = BM - leak
        avg_r = sum(t["r"] for t in subset) / n
        pnl = sum(t["pnl"] for t in subset if t["pnl"] is not None)
        wh = [t["hold_h"] for t in subset if t["win"]]
        lh = [t["hold_h"] for t in subset if not t["win"]]
        print(f"\n## {label}")
        print(
            f"n={n} WR={wr*100:.1f}% W/L={wins}/{losses} "
            f"BM={BM*100:+.1f}pp E_N={EN:+.3f}R EF≈{EF*100:+.1f}pp "
            f"avgR={avg_r:+.3f} pnl≈${pnl:+.2f}"
        )
        if wh:
            print(f"  win hold med={statistics.median(wh):.1f}h mean={statistics.mean(wh):.1f}h")
        if lh:
            print(f"  loss hold med={statistics.median(lh):.1f}h mean={statistics.mean(lh):.1f}h")

        by_side = defaultdict(list)
        for t in subset:
            by_side[t["side"]].append(t)
        for side, rows in sorted(by_side.items()):
            w = sum(1 for t in rows if t["win"])
            en = (w / len(rows)) * (R + 1) - 1
            print(f"  {side}: n={len(rows)} WR={w/len(rows)*100:.1f}% E_N={en:+.3f}R")

        by_dow = defaultdict(list)
        for t in subset:
            by_dow[t["dow"]].append(t)
        order = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        for d in order:
            rows = by_dow.get(d, [])
            if not rows:
                continue
            w = sum(1 for t in rows if t["win"])
            en = (w / len(rows)) * (R + 1) - 1
            print(f"  {d}: n={len(rows)} WR={w/len(rows)*100:.1f}% E_N={en:+.3f}R")

        by_mo = defaultdict(list)
        for t in subset:
            by_mo[t["month"]].append(t)
        print("  months:")
        for mo in sorted(by_mo):
            rows = by_mo[mo]
            w = sum(1 for t in rows if t["win"])
            en = (w / len(rows)) * (R + 1) - 1
            print(f"    {mo}: n={len(rows)} WR={w/len(rows)*100:.1f}% E_N={en:+.3f}R")

        # streaks
        streak_w = streak_l = max_w = max_l = 0
        for t in subset:
            if t["win"]:
                streak_w += 1
                streak_l = 0
                max_w = max(max_w, streak_w)
            else:
                streak_l += 1
                streak_w = 0
                max_l = max(max_l, streak_l)
        print(f"  max win streak={max_w} max loss streak={max_l}")

        # exit mix
        exits = Counter(t["exit"] for t in subset)
        print(f"  exits={dict(exits)}")

        # overnight share (>=12h)
        overnight = sum(1 for t in subset if t["hold_h"] >= 12)
        print(f"  hold>=12h: {overnight}/{n} ({overnight/n*100:.0f}%)")

        # hour buckets of entry
        by_h = defaultdict(list)
        for t in subset:
            by_h[t["hour"]].append(t)
        print("  entry hours (n>=3):")
        for h in sorted(by_h):
            rows = by_h[h]
            if len(rows) < 3:
                continue
            w = sum(1 for t in rows if t["win"])
            en = (w / len(rows)) * (R + 1) - 1
            print(f"    H{h:02d}: n={len(rows)} WR={w/len(rows)*100:.1f}% E_N={en:+.3f}R")

        # rolling W10/W15/W20 path averages
        print("  rolling path:")
        for W in (10, 15, 20, 30):
            if n < W:
                print(f"    W{W}: n too small")
                continue
            path_wr = []
            path_en = []
            for i in range(W - 1, n):
                window = subset[i - W + 1 : i + 1]
                ww = sum(1 for t in window if t["win"]) / W
                path_wr.append(ww)
                path_en.append(ww * (R + 1) - 1)
            print(
                f"    W{W}: avgWR={statistics.mean(path_wr)*100:.1f}% "
                f"avgE_N={statistics.mean(path_en):+.3f}R "
                f"minE_N={min(path_en):+.3f}R maxE_N={max(path_en):+.3f}R"
            )

    tip = [t for t in closed if t["open"] >= TIP_FROM]
    prior = [t for t in closed if t["open"] <= PRIOR_TO]
    score(closed, "LONG (hist tip Dec2025-Aug2026)")
    score(tip, "TIP May-Aug 2026")
    score(prior, "PRIOR Jan-Apr 2026 (+Dec residue in long)")

    # path equity approx for MaxDD
    eq = 500.0
    peak = eq
    maxdd = 0.0
    for t in closed:
        if t["pnl"] is None:
            continue
        eq += t["pnl"]
        peak = max(peak, eq)
        dd = (peak - eq) / peak
        maxdd = max(maxdd, dd)
    print(f"\nApprox path MaxDD (fixed $2.5/R proxy)={maxdd*100:.2f}% final≈{eq:.2f}")


if __name__ == "__main__":
    main()
