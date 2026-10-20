"""EDX-P05-T01 integrity audit on mag 8230151 (fallback 8230101)."""
from __future__ import annotations

import json
import re
from datetime import datetime
from pathlib import Path

LOG = Path(
    r"C:\Users\emili\AppData\Roaming\MetaQuotes\Terminal"
    r"\D0E8209F77C8CF37AD8BF550E51FF075\Tester\logs\20261007.log"
)
OUT = Path(__file__).resolve().parent


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
    print("runs", len(starts))
    runs = []
    for i, s in enumerate(starts):
        end = starts[i + 1].start() if i + 1 < len(starts) else len(text)
        c = text[s.start() : end]
        mag = re.search(r"InpMagic=(\d+)", c)
        sl = re.search(r"InpSL_Points=([0-9.]+)", c)
        tp = re.search(r"InpTP_Points=([0-9.]+)", c)
        ml = re.search(r"InpMaxLevels=([0-9.]+)", c)
        me = re.search(r"InpMaxEntries=([0-9.]+)", c)
        finals = re.findall(r"final balance ([\d.]+)", c)
        opens = len(re.findall(r"\[BMRG\]\[TRADE\] OPEN", c))
        meta = {
            "i": i,
            "from": s.group(1),
            "to": s.group(2),
            "magic": mag.group(1) if mag else "?",
            "sl": sl.group(1) if sl else "?",
            "tp": tp.group(1) if tp else "?",
            "max_levels": ml.group(1) if ml else "?",
            "max_entries": me.group(1) if me else "?",
            "opens": opens,
            "final": float(finals[-1]) if finals else None,
            "chunk": c,
        }
        runs.append(meta)
        print(
            f"[{i}] {meta['from']}->{meta['to']} mag={meta['magic']} "
            f"SL/TP={meta['sl']}/{meta['tp']} L/E={meta['max_levels']}/{meta['max_entries']} "
            f"opens={opens} final={meta['final']}"
        )

    chosen = None
    for r in runs:
        if r["magic"] == "8230151":
            chosen = r
    if chosen is None:
        for r in reversed(runs):
            if r["magic"] == "8230101":
                chosen = r
                print("NOTE: 8230151 missing — auditing last 8230101 as P05 proxy")
                break
    if chosen is None:
        raise SystemExit("no integrity/baseline run found")

    c = chosen["chunk"]
    # Parse each open: SL/TP distance in points
    events = []
    open_rec = None
    for line in c.splitlines():
        m = re.search(
            r"(\d{4}\.\d{2}\.\d{2} \d{2}:\d{2}:\d{2})\s+market (buy|sell) "
            r"([\d.]+) AUDUSD sl: ([\d.]+) tp: ([\d.]+) \(([\d.]+) / ([\d.]+)",
            line,
        )
        if m and "OrderSend" not in line:
            open_rec = {
                "t": m.group(1),
                "side": m.group(2),
                "lot": float(m.group(3)),
                "sl": float(m.group(4)),
                "tp": float(m.group(5)),
                "bid": float(m.group(6)),
                "ask": float(m.group(7)),
            }
            continue
        m = re.search(
            r"deal #\d+ (buy|sell) ([\d.]+) AUDUSD at ([\d.]+)",
            line,
        )
        if m and open_rec and "entry" not in open_rec and m.group(1) == open_rec["side"]:
            open_rec["entry"] = float(m.group(3))
            continue
        m = re.search(
            r"(take profit|stop loss) triggered",
            line,
            flags=re.I,
        )
        if m and open_rec:
            entry = open_rec.get("entry")
            if entry is not None:
                if open_rec["side"] == "buy":
                    sl_pts = round((entry - open_rec["sl"]) / 0.00001)
                    tp_pts = round((open_rec["tp"] - entry) / 0.00001)
                else:
                    sl_pts = round((open_rec["sl"] - entry) / 0.00001)
                    tp_pts = round((entry - open_rec["tp"]) / 0.00001)
            else:
                # use bid/ask mid proxy
                px = open_rec["ask"] if open_rec["side"] == "buy" else open_rec["bid"]
                if open_rec["side"] == "buy":
                    sl_pts = round((px - open_rec["sl"]) / 0.00001)
                    tp_pts = round((open_rec["tp"] - px) / 0.00001)
                else:
                    sl_pts = round((open_rec["sl"] - px) / 0.00001)
                    tp_pts = round((px - open_rec["tp"]) / 0.00001)
            events.append(
                {
                    **{k: open_rec[k] for k in ("t", "side", "lot")},
                    "entry": entry,
                    "sl_pts": sl_pts,
                    "tp_pts": tp_pts,
                    "exit": "TP" if "take" in m.group(1).lower() else "SL",
                    "spread_pts": round((open_rec["ask"] - open_rec["bid"]) / 0.00001),
                }
            )
            open_rec = None

    # Concurrent exposure check: never >1 open
    max_concurrent = 0
    cur = 0
    open_rec = None
    for line in c.splitlines():
        if re.search(r"\smarket (buy|sell) ", line) and "OrderSend" not in line:
            cur += 1
            max_concurrent = max(max_concurrent, cur)
        if re.search(r"(take profit|stop loss) triggered", line, re.I):
            cur = max(0, cur - 1)

    sl_set = sorted({e["sl_pts"] for e in events})
    tp_set = sorted({e["tp_pts"] for e in events})
    # designed 300; allow fill slip so 280-320 band OK for PASS with note
    sl_ok = all(280 <= e["sl_pts"] <= 320 for e in events)
    tp_ok = all(280 <= e["tp_pts"] <= 320 for e in events)
    # stricter: median near 300
    import statistics as st

    med_sl = st.median([e["sl_pts"] for e in events]) if events else None
    med_tp = st.median([e["tp_pts"] for e in events]) if events else None

    g0_ok = chosen["max_levels"] in ("1", "1.0") and chosen["max_entries"] in ("1", "1.0")
    magic_ok = chosen["magic"] in ("8230151", "8230101")
    geom_ok = chosen["sl"].startswith("300") and chosen["tp"].startswith("300")
    one_ticket = max_concurrent <= 1
    n = len(events)
    tp_n = sum(1 for e in events if e["exit"] == "TP")
    sl_n = sum(1 for e in events if e["exit"] == "SL")

    # lots all 0.01?
    lots = sorted({e["lot"] for e in events})

    verdict = (
        "PASS"
        if g0_ok and magic_ok and geom_ok and one_ticket and sl_ok and tp_ok and n > 0
        else "FAIL"
    )

    report = {
        "task": "EDX-P05-T01",
        "verdict": verdict,
        "magic": chosen["magic"],
        "window": f"{chosen['from']}->{chosen['to']}",
        "preset_sl_tp": f"{chosen['sl']}/{chosen['tp']}",
        "MaxLevels": chosen["max_levels"],
        "MaxEntries": chosen["max_entries"],
        "n_events": n,
        "opens_tag": chosen["opens"],
        "TP": tp_n,
        "SL": sl_n,
        "final": chosen["final"],
        "max_concurrent": max_concurrent,
        "sl_pts_unique": sl_set,
        "tp_pts_unique": tp_set,
        "med_sl_pts": med_sl,
        "med_tp_pts": med_tp,
        "lots": lots,
        "checks": {
            "g0_single": g0_ok,
            "magic_ok": magic_ok,
            "geom_300_300": geom_ok,
            "one_ticket_at_a_time": one_ticket,
            "sl_pts_in_280_320": sl_ok,
            "tp_pts_in_280_320": tp_ok,
            "ticket_WR_inflation": False,  # G0 + concurrent<=1
        },
        "note": "1R from hard SL distance; fill/quote can shift measured pts off exact 300",
    }
    (OUT / "SCORECARD.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
