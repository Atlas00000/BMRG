"""Deal-level score for M15 expansion Tester log (AOS OFF)."""
from __future__ import annotations

import json
import re
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path

LOG = Path(
    r"C:\Users\emili\AppData\Roaming\MetaQuotes\Terminal"
    r"\D0E8209F77C8CF37AD8BF550E51FF075\Tester\logs\20261019.log"
)
OUT = Path(__file__).resolve().parent
DEPOSIT = 400.0
BWR = 50.0


def load(path: Path) -> str:
    raw = path.read_bytes()
    if raw[:2] == b"\xff\xfe":
        return raw.decode("utf-16-le")
    return raw.decode("utf-8", errors="replace")


START_RE = re.compile(
    r"([A-Z0-9.]+),(M\d+|H\d+|D1): testing of Experts\\BMRG\\BMRG\.ex5 "
    r"from (\S+) 00:00 to (\S+) 00:00 started with inputs:",
)

# take profit triggered #2 sell 0.01 AUDUSD ...
TP_RE = re.compile(
    r"(\d{4}\.\d{2}\.\d{2} \d{2}:\d{2}:\d{2})\s+take profit triggered"
)
SL_RE = re.compile(
    r"(\d{4}\.\d{2}\.\d{2} \d{2}:\d{2}:\d{2})\s+stop loss triggered"
)
# also stop out / stop triggered variants
SL2_RE = re.compile(
    r"(\d{4}\.\d{2}\.\d{2} \d{2}:\d{2}:\d{2})\s+stop (?:loss )?triggered",
    re.I,
)


def inp(c: str, key: str) -> str | None:
    m = re.search(rf"{key}=([^\s|]+)", c)
    return m.group(1) if m else None


def roll_wr(outcomes: list[int], k: int):
    if len(outcomes) < k:
        return None
    series = [
        100.0 * sum(1 for x in outcomes[j - k : j] if x > 0) / k
        for j in range(k, len(outcomes) + 1)
    ]
    return {"min": min(series), "last": series[-1], "max": max(series)}


def score(c: str, sym: str, tf: str, a: str, b: str, i: int) -> dict:
    events = []
    for m in TP_RE.finditer(c):
        events.append((m.start(), datetime.strptime(m.group(1), "%Y.%m.%d %H:%M:%S"), 1))
    for m in SL_RE.finditer(c):
        events.append((m.start(), datetime.strptime(m.group(1), "%Y.%m.%d %H:%M:%S"), -1))
    # dedupe: SL_RE and SL2 may double — use only SL_RE if both match same
    events.sort(key=lambda x: x[0])
    outcomes = [e[2] for e in events]
    times = [e[1] for e in events]
    n = len(outcomes)
    wins = sum(1 for o in outcomes if o > 0)
    wr = 100.0 * wins / n if n else None

    # monthly
    by_m: dict[str, list[int]] = defaultdict(list)
    for t, o in zip(times, outcomes):
        by_m[t.strftime("%Y-%m")].append(o)
    months = {}
    for mk, seq in sorted(by_m.items()):
        w = sum(1 for x in seq if x > 0)
        months[mk] = {
            "n": len(seq),
            "wr": round(100.0 * w / len(seq), 1),
            "en_proxy": round((2 * w / len(seq) - 1), 3),  # RR=1: E≈2WR-1
        }

    finals = re.findall(r"final balance ([\d.]+)", c)
    final = float(finals[-1]) if finals else None
    pnl = (final - DEPOSIT) if final is not None else None

    # equity path at fixed 0.5%*f — without L4 f=1 for AOS off
    eq = DEPOSIT
    peak = eq
    maxdd = 0.0
    risk = float(inp(c, "InpRiskPercent") or 0.5) / 100.0
    for o in outcomes:
        eq *= 1 + o * risk
        if eq > peak:
            peak = eq
        maxdd = max(maxdd, 100.0 * (peak - eq) / peak if peak else 0)

    max_l = 0
    streak = 0
    for o in outcomes:
        if o < 0:
            streak += 1
            max_l = max(max_l, streak)
        else:
            streak = 0

    # tip vs primary for AUDUSD-like
    tip_months = [m for m in months if m >= "2026-09"]
    tip_soft = any(months[m]["wr"] < BWR for m in tip_months)

    return {
        "i": i,
        "sym": sym,
        "tf": tf,
        "window": f"{a}->{b}",
        "magic": inp(c, "InpMagic"),
        "risk": inp(c, "InpRiskPercent"),
        "aos": inp(c, "InpAOS_Enable"),
        "start": inp(c, "InpStartHour"),
        "end": inp(c, "InpEndHour"),
        "mon": inp(c, "InpTradeMon"),
        "tue": inp(c, "InpTradeTue"),
        "sl": inp(c, "InpSL_Points"),
        "tp": inp(c, "InpTP_Points"),
        "bb": inp(c, "InpBBDev"),
        "n": n,
        "wr": round(wr, 1) if wr is not None else None,
        "en_proxy": round(2 * wr / 100 - 1, 3) if wr is not None else None,
        "pnl": round(pnl, 2) if pnl is not None else None,
        "final": final,
        "w10": roll_wr(outcomes, 10),
        "w20": roll_wr(outcomes, 20),
        "w30": roll_wr(outcomes, 30),
        "max_loss_streak": max_l,
        "path_dd_pct": round(maxdd, 1),
        "months": months,
        "tip_soft": tip_soft,
        "geom_ok": (
            inp(c, "InpSL_Points") == "300"
            and inp(c, "InpTP_Points") == "300"
            and inp(c, "InpStartHour") == "13"
            and inp(c, "InpTradeMon") == "false"
            and inp(c, "InpTradeTue") == "false"
        )
        if sym == "AUDUSD"
        else None,
    }


def main() -> None:
    text = load(LOG)
    starts = list(START_RE.finditer(text))
    rows = []
    for i, s in enumerate(starts):
        end = starts[i + 1].start() if i + 1 < len(starts) else len(text)
        c = text[s.start() : end]
        rows.append(score(c, s.group(1), s.group(2), s.group(3), s.group(4), i))

    print(
        f"{'i':>2} {'sym':6} {'tf':3} {'window':26} {'mag':>8} "
        f"{'SL/TP':>9} {'St':>2} {'n':>3} {'WR':>5} {'E~':>6} {'pnl':>7} "
        f"{'W20':>11} {'DD~':>5} {'Lstr':>4} geom"
    )
    for r in rows:
        w20 = r["w20"]
        w20s = f"{w20['min']:.0f}->{w20['last']:.0f}" if w20 else "-"
        if r["geom_ok"]:
            geom = "CHAMP"
        elif r["sym"] == "AUDUSD" and r["geom_ok"] is False:
            geom = "MISMATCH"
        else:
            geom = "xfer"
        wr_s = f"{r['wr']:.1f}" if r["wr"] is not None else "-"
        en_s = f"{r['en_proxy']:+.2f}" if r["en_proxy"] is not None else "-"
        pnl_s = f"{r['pnl']:+.1f}" if r["pnl"] is not None else "-"
        print(
            f"{r['i']:2d} {r['sym']:6} {r['tf']:3} {r['window']:26} "
            f"{(r['magic'] or '?'):>8} {(r['sl'] or '?')}/{(r['tp'] or '?'):>4} "
            f"{(r['start'] or '?'):>2} {r['n']:3d} "
            f"{wr_s:>5} {en_s:>6} {pnl_s:>7} "
            f"{w20s:>11} {r['path_dd_pct']:5.1f} {r['max_loss_streak']:4d} {geom}"
        )

    print("\n--- monthly (champ AUDUSD + DE30 primary) ---")
    for r in rows:
        if r["i"] in (0, 1, 7, 8) or (r["sym"] == "AUDUSD" and r["geom_ok"]):
            print(f"\n#{r['i']} {r['sym']} {r['window']} n={r['n']} WR={r['wr']}")
            for mk, v in r["months"].items():
                flag = " <<" if v["wr"] < BWR else ""
                print(f"  {mk} n={v['n']:3d} WR={v['wr']:5.1f}% E~={v['en_proxy']:+.3f}{flag}")

    (OUT / "DEAL_SCORE.json").write_text(json.dumps(rows, indent=2, default=str), encoding="utf-8")
    print("\nwrote", OUT / "DEAL_SCORE.json")


if __name__ == "__main__":
    main()
