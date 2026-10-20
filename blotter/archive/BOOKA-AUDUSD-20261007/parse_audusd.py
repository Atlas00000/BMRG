"""Parse AUDUSD BOOKA tester log (20261007) for expansion review."""
from __future__ import annotations

from collections import defaultdict
from datetime import datetime, timedelta
from pathlib import Path
import re
import statistics as st

LOG = Path(
    r"C:\Users\emili\AppData\Roaming\MetaQuotes\Terminal"
    r"\D0E8209F77C8CF37AD8BF550E51FF075\Tester\logs\20261007.log"
)
LOG06 = Path(
    r"C:\Users\emili\AppData\Roaming\MetaQuotes\Terminal"
    r"\D0E8209F77C8CF37AD8BF550E51FF075\Tester\logs\20261006.log"
)


def load(path: Path) -> str:
    raw = path.read_bytes()
    if raw[:2] in (b"\xff\xfe", b"\xfe\xff") or (len(raw) > 2 and raw[1] == 0):
        return raw.decode("utf-16")
    return raw.decode("utf-8", errors="replace")


def score_chunk(chunk: str, label: str) -> dict:
    opens = len(re.findall(r"\[BMRG\]\[TRADE\] OPEN", chunk))
    mkt = len(re.findall(r"market (?:buy|sell) ", chunk))
    buys = len(re.findall(r"market buy ", chunk))
    sells = len(re.findall(r"market sell ", chunk))
    tp_dates = re.findall(r"(\d{4}\.\d{2}\.\d{2}).*?take profit triggered", chunk)
    sl_dates = re.findall(r"(\d{4}\.\d{2}\.\d{2}).*?stop loss triggered", chunk)
    closes = [(d, 1) for d in tp_dates] + [(d, 0) for d in sl_dates]
    closes.sort(key=lambda x: x[0])
    n = len(tp_dates) + len(sl_dates)
    wr = 100.0 * len(tp_dates) / n if n else 0.0
    en = (2.0 * len(tp_dates) / n - 1.0) if n else None
    finals = re.findall(r"final balance ([\d.]+)", chunk)
    deps = re.findall(r"initial deposit ([\d.]+)", chunk)
    deposit = float(deps[0]) if deps else 400.0
    final = float(finals[-1]) if finals else None
    pnl = (final - deposit) if final is not None else None

    # hold times
    hold_hours = []
    open_t = None
    for line in chunk.splitlines():
        m = re.search(r"(\d{4}\.\d{2}\.\d{2} \d{2}:\d{2}:\d{2})\s+market (buy|sell)", line)
        if m:
            open_t = datetime.strptime(m.group(1), "%Y.%m.%d %H:%M:%S")
            continue
        m = re.search(
            r"(\d{4}\.\d{2}\.\d{2} \d{2}:\d{2}:\d{2})\s+(take profit|stop loss) triggered",
            line,
        )
        if m and open_t:
            ct = datetime.strptime(m.group(1), "%Y.%m.%d %H:%M:%S")
            hold_hours.append((ct - open_t).total_seconds() / 3600.0)
            open_t = None

    by_month: dict[str, dict[str, int]] = defaultdict(lambda: {"tp": 0, "sl": 0})
    for d in tp_dates:
        by_month[d[:7]]["tp"] += 1
    for d in sl_dates:
        by_month[d[:7]]["sl"] += 1

    events = [
        (datetime.strptime(d, "%Y.%m.%d"), w)
        for d, w in [(d, 1) for d in tp_dates] + [(d, 0) for d in sl_dates]
    ]
    events.sort(key=lambda x: x[0])

    rolls = []
    if events:
        cur = events[0][0]
        end = events[-1][0]
        while cur <= end:
            wend = cur + timedelta(days=30)
            win = [(dt, w) for dt, w in events if cur <= dt < wend]
            if win:
                nn = len(win)
                tpn = sum(w for _, w in win)
                rolls.append(
                    {
                        "from": cur.date().isoformat(),
                        "to": wend.date().isoformat(),
                        "n": nn,
                        "wr": 100.0 * tpn / nn,
                        "en": 2.0 * tpn / nn - 1.0,
                    }
                )
            cur += timedelta(days=15)

    return {
        "label": label,
        "opens_tag": opens,
        "mkt": mkt,
        "buys": buys,
        "sells": sells,
        "tp": len(tp_dates),
        "sl": len(sl_dates),
        "n": n,
        "wr": wr,
        "en": en,
        "final": final,
        "deposit": deposit,
        "pnl": pnl,
        "hold_hours": hold_hours,
        "by_month": dict(by_month),
        "rolls": rolls,
    }


def print_score(s: dict) -> None:
    en_s = f"{s['en']:+.3f}R" if s["en"] is not None else "—"
    pnl_s = f"{s['pnl']:+.2f}" if s["pnl"] is not None else "—"
    print("=" * 72)
    print(s["label"])
    print(
        f"  opens_tag={s['opens_tag']} market={s['mkt']} "
        f"(buy={s['buys']} sell={s['sells']})"
    )
    print(
        f"  n={s['n']} TP={s['tp']} SL={s['sl']} "
        f"WR={s['wr']:.1f}% E_N={en_s} final={s['final']} pnl={pnl_s}"
    )
    if s["hold_hours"]:
        hh = s["hold_hours"]
        ov = sum(1 for h in hh if h >= 12)
        print(
            f"  hold med={st.median(hh):.1f}h mean={st.mean(hh):.1f}h "
            f"p90={sorted(hh)[int(0.9 * (len(hh) - 1))]:.1f}h "
            f">=12h={ov}/{len(hh)} ({100 * ov / len(hh):.0f}%)"
        )
    print("  monthly:")
    for mo in sorted(s["by_month"]):
        t = s["by_month"][mo]
        nn = t["tp"] + t["sl"]
        wr = 100.0 * t["tp"] / nn if nn else 0.0
        en = 2.0 * t["tp"] / nn - 1.0 if nn else 0.0
        print(f"    {mo}: n={nn:3} TP={t['tp']:3} SL={t['sl']:3} WR={wr:5.1f}% E_N={en:+.3f}R")
    print("  rolling 30d / step 15d:")
    for r in s["rolls"]:
        flag = ""
        if r["wr"] < 45:
            flag = "  << soft-stress fail / regime"
        elif r["en"] < 0:
            flag = "  << negative E_N"
        print(
            f"    {r['from']}->{r['to']}: n={r['n']:3} "
            f"WR={r['wr']:5.1f}% E_N={r['en']:+.3f}R{flag}"
        )


def geometry_check(chunk: str) -> None:
    samples = re.findall(
        r"market (buy|sell) [\d.]+\s+AUDUSD sl: ([\d.]+) tp: ([\d.]+) \(([\d.]+)",
        chunk,
    )
    # Prefer bare market lines (not OrderSend) — regex above matches both; unique ok
    pts = []
    for side, sl, tp, px in samples:
        sl_f, tp_f, px_f = float(sl), float(tp), float(px)
        if side == "buy":
            d_sl = round((px_f - sl_f) / 0.00001)
            d_tp = round((tp_f - px_f) / 0.00001)
        else:
            d_sl = round((sl_f - px_f) / 0.00001)
            d_tp = round((px_f - tp_f) / 0.00001)
        pts.append((d_sl, d_tp))
    if pts:
        sl_set = sorted({p[0] for p in pts})
        tp_set = sorted({p[1] for p in pts})
        print(f"  geometry samples={len(pts)} SL_pts={sl_set} TP_pts={tp_set}")
    init = re.search(r"AUDUSD PERIOD_M5 \| ([^\r\n]+)", chunk)
    if init:
        print(f"  init: {init.group(0)[:160]}")
    for pat in [
        r"loss streak",
        r"FailPause",
        r"equity halt",
        r"daily loss",
        r"GATE",
        r"blocked",
    ]:
        print(f"  keyword '{pat}': {len(re.findall(pat, chunk, flags=re.I))}")


def main() -> None:
    text = load(LOG)
    parts = re.split(r"BMRG init OK \|", text)
    print(f"20261007 inits={len(parts)-1} chars={len(text)}")
    # First run only (duplicate second run same result)
    if len(parts) >= 2:
        chunk = parts[1]
        # trim if another tester restart mid-chunk without init (keep until next Expert load)
        m = re.search(r'Tester\t"BMRG\\BMRG\.ex5"', chunk)
        if m:
            chunk = chunk[: m.start()]
        print_score(score_chunk(chunk, "AUDUSD 2026.05.01 -> 2026.08.31 (log 20261007)"))
        geometry_check(chunk)

    if LOG06.exists():
        t6 = load(LOG06)
        headers = list(
            re.finditer(
                r"Tester\t(\w+),M5 \(YWO-Trade\): testing of Experts\\BMRG\\BMRG\.ex5 "
                r"from (\S+) 00:00 to (\S+) 00:00",
                t6,
            )
        )
        print("\n--- prior AUDUSD from 20261006 ---")
        for i, h in enumerate(headers):
            if h.group(1) != "AUDUSD":
                continue
            start = h.start()
            end = headers[i + 1].start() if i + 1 < len(headers) else len(t6)
            chunk = t6[start:end]
            label = f"AUDUSD {h.group(2)} -> {h.group(3)} (log 20261006)"
            print_score(score_chunk(chunk, label))


if __name__ == "__main__":
    main()
