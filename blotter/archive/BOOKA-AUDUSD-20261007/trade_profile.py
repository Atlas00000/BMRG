"""Trade-profile extract for AUDUSD system_profile.md."""
from __future__ import annotations

from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path
import re
import statistics as st

LOG = Path(
    r"C:\Users\emili\AppData\Roaming\MetaQuotes\Terminal"
    r"\D0E8209F77C8CF37AD8BF550E51FF075\Tester\logs\20261007.log"
)


def load(path: Path) -> str:
    raw = path.read_bytes()
    if raw[:2] in (b"\xff\xfe", b"\xfe\xff") or (len(raw) > 2 and raw[1] == 0):
        return raw.decode("utf-16")
    return raw.decode("utf-8", errors="replace")


def first_run(text: str) -> str:
    parts = re.split(r"BMRG init OK \|", text)
    chunk = parts[1]
    m = re.search(r'Tester\t"BMRG\\BMRG\.ex5"', chunk)
    return chunk[: m.start()] if m else chunk


def main() -> None:
    chunk = first_run(load(LOG))
    trades = []
    open_rec = None
    for line in chunk.splitlines():
        m = re.search(
            r"(\d{4}\.\d{2}\.\d{2} \d{2}:\d{2}:\d{2})\s+market (buy|sell) "
            r"([\d.]+) AUDUSD sl: ([\d.]+) tp: ([\d.]+)",
            line,
        )
        if m and "OrderSend" not in line:
            open_rec = {
                "t": datetime.strptime(m.group(1), "%Y.%m.%d %H:%M:%S"),
                "side": m.group(2),
                "lot": float(m.group(3)),
            }
            continue
        m = re.search(
            r"(\d{4}\.\d{2}\.\d{2} \d{2}:\d{2}:\d{2})\s+(take profit|stop loss) triggered",
            line,
        )
        if m and open_rec:
            ct = datetime.strptime(m.group(1), "%Y.%m.%d %H:%M:%S")
            win = "take" in m.group(2)
            hold_h = (ct - open_rec["t"]).total_seconds() / 3600.0
            trades.append(
                {
                    **open_rec,
                    "close": ct,
                    "win": win,
                    "hold_h": hold_h,
                    "dow": open_rec["t"].strftime("%a"),
                    "hour": open_rec["t"].hour,
                    "month": open_rec["t"].strftime("%Y-%m"),
                }
            )
            open_rec = None

    n = len(trades)
    wins = [t for t in trades if t["win"]]
    losses = [t for t in trades if not t["win"]]
    print(f"n={n} wins={len(wins)} losses={len(losses)} WR={100*len(wins)/n:.1f}%")

    # Side x outcome
    print("\n## side x outcome")
    for side in ("buy", "sell"):
        sub = [t for t in trades if t["side"] == side]
        w = sum(1 for t in sub if t["win"])
        print(f"  {side}: n={len(sub)} WR={100*w/len(sub):.1f}% E_N={2*w/len(sub)-1:+.3f}R")

    # Hold winners vs losers
    print("\n## hold hours")
    for label, subset in (("W", wins), ("L", losses), ("all", trades)):
        hh = [t["hold_h"] for t in subset]
        print(
            f"  {label}: med={st.median(hh):.1f} mean={st.mean(hh):.1f} "
            f"p10={sorted(hh)[max(0,int(0.1*(len(hh)-1)))]:.1f} "
            f"p90={sorted(hh)[int(0.9*(len(hh)-1))]:.1f}"
        )

    # DOW
    print("\n## DOW (entry)")
    for dow in ("Mon", "Tue", "Wed", "Thu", "Fri"):
        sub = [t for t in trades if t["dow"] == dow]
        if not sub:
            print(f"  {dow}: n=0 (filtered)")
            continue
        w = sum(1 for t in sub if t["win"])
        print(f"  {dow}: n={len(sub):2} WR={100*w/len(sub):5.1f}% E_N={2*w/len(sub)-1:+.3f}R")

    # Hour buckets (entry)
    print("\n## entry hour")
    by_h = defaultdict(list)
    for t in trades:
        by_h[t["hour"]].append(t["win"])
    for h in sorted(by_h):
        xs = by_h[h]
        wr = 100 * sum(xs) / len(xs)
        print(f"  {h:02d}: n={len(xs):2} WR={wr:5.1f}%")

    # Streaks
    print("\n## streaks")
    streak = 0
    kind = None
    max_w = max_l = cur_w = cur_l = 0
    for t in trades:
        if t["win"]:
            cur_w += 1
            cur_l = 0
            max_w = max(max_w, cur_w)
        else:
            cur_l += 1
            cur_w = 0
            max_l = max(max_l, cur_l)
    print(f"  max win streak={max_w} max loss streak={max_l}")

    # Rolling trade windows W20 / W30
    print("\n## rolling trade windows")
    outcomes = [1 if t["win"] else 0 for t in trades]
    for wsize in (15, 20, 30):
        print(f"  W{wsize}:")
        for i in range(0, max(1, n - wsize + 1), max(1, wsize // 2)):
            win = outcomes[i : i + wsize]
            if len(win) < wsize:
                break
            wr = 100 * sum(win) / len(win)
            en = 2 * sum(win) / len(win) - 1
            print(f"    trades[{i}:{i+wsize}] WR={wr:5.1f}% E_N={en:+.3f}R")

    # Approx $ per R at 0.01 lot: pnl/net from R
    # With R=1 fixed, E_N * n * ~$ per R ≈ pnl
    # 0.241 * 58 * x = 44.39 → x ≈ 3.18 USD per R
    print("\n## $ proxy")
    en = 2 * len(wins) / n - 1
    usd_per_r = 44.39 / (en * n) if en else 0
    print(f"  implied USD/R ≈ {usd_per_r:.2f} (from PnL/E_N/n)")
    print(f"  sum R winners=+{len(wins)} losers=-{len(losses)} net_R={len(wins)-len(losses):+d}")
    print(f"  E_N={en:+.3f}R  BM={100*(len(wins)/n - 0.5):+.2f}pp  BWR=50%")

    # Leak proxy note: no deal costs isolated; skip
    # Frequency
    first, last = trades[0]["t"], trades[-1]["close"]
    days = (last - first).total_seconds() / 86400
    print(f"\n## frequency")
    print(f"  span_days≈{days:.0f}  trades/30d≈{n*30/days:.1f}  opens/month≈{n*30.44/days:.1f}")


if __name__ == "__main__":
    main()
