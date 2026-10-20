"""Score EDX-P5-T01 stack vs P0 and P3-T02."""
from __future__ import annotations

import json
import math
import re
import statistics as st
from datetime import datetime
from pathlib import Path

LOG = Path(
    r"C:\Users\emili\AppData\Roaming\MetaQuotes\Terminal"
    r"\D0E8209F77C8CF37AD8BF550E51FF075\Tester\logs\20261007.log"
)
OUT = Path(__file__).resolve().parent

P0 = {"n": 58, "WR": 62.07, "E_N": 0.241, "EF_pp": 4.57, "pnl": 44.39}
T02 = {"n": 57, "WR": 68.42, "E_N": 0.368, "EF_pp": 11.42, "pnl": 62.90}


def load(path: Path) -> str:
    raw = path.read_bytes()
    if raw[:2] == b"\xff\xfe":
        return raw.decode("utf-16-le")
    return raw.decode("utf-8", errors="replace")


def main() -> None:
    text = load(LOG)
    print("log_bytes", LOG.stat().st_size)
    starts = list(
        re.finditer(
            r"AUDUSD,M5: testing of Experts\\BMRG\\BMRG\.ex5 from (\S+) 00:00 to (\S+) 00:00 started with inputs:",
            text,
        )
    )
    chosen = None
    for i, s in enumerate(starts):
        end = starts[i + 1].start() if i + 1 < len(starts) else len(text)
        c = text[s.start() : end]
        mag = re.search(r"InpMagic=(\d+)", c)
        if not mag:
            continue
        mval = mag.group(1)
        sh = re.search(r"InpStartHour=([0-9.]+)", c)
        mon = re.search(r"InpTradeMon=(true|false)", c)
        sl = re.search(r"InpSL_Points=([0-9.]+)", c)
        tp = re.search(r"InpTP_Points=([0-9.]+)", c)
        finals = re.findall(r"final balance ([\d.]+)", c)
        print(
            f"[{i}] {s.group(1)}->{s.group(2)} mag={mval} "
            f"Start={sh.group(1) if sh else '?'} Mon={mon.group(1) if mon else '?'} "
            f"SL/TP={(sl.group(1) if sl else '?')}/{(tp.group(1) if tp else '?')} "
            f"final={finals[-1] if finals else '?'}"
        )
        if mval == "8230501":
            cand = {
                "from": s.group(1),
                "to": s.group(2),
                "start": sh.group(1) if sh else "?",
                "mon": mon.group(1) if mon else "?",
                "sl": sl.group(1) if sl else "?",
                "tp": tp.group(1) if tp else "?",
                "final": float(finals[-1]) if finals else None,
                "chunk": c,
                "i": i,
            }
            # Prefer correct stack identity: StartHour=13 + TradeMon=false
            if cand["start"] == "13" and cand["mon"] == "false":
                chosen = cand
            elif chosen is None:
                chosen = cand

    if not chosen:
        raise SystemExit("8230501 not found")
    print(
        "scoring run",
        chosen.get("i"),
        "Start",
        chosen["start"],
        "Mon",
        chosen["mon"],
        "final",
        chosen["final"],
    )

    c = chosen["chunk"]
    trades = []
    open_rec = None
    for line in c.splitlines():
        m = re.search(
            r"(\d{4}\.\d{2}\.\d{2} \d{2}:\d{2}:\d{2})\s+market (buy|sell) "
            r"([\d.]+) AUDUSD sl: ([\d.]+) tp: ([\d.]+)",
            line,
        )
        if m and "OrderSend" not in line:
            open_rec = {
                "t": datetime.strptime(m.group(1), "%Y.%m.%d %H:%M:%S"),
                "side": m.group(2),
                "sl": float(m.group(4)),
                "tp": float(m.group(5)),
            }
            continue
        m = re.search(r"deal #\d+ (buy|sell) ([\d.]+) AUDUSD at ([\d.]+)", line)
        if m and open_rec and "entry" not in open_rec and m.group(1) == open_rec["side"]:
            open_rec["entry"] = float(m.group(3))
            continue
        m = re.search(
            r"(\d{4}\.\d{2}\.\d{2} \d{2}:\d{2}:\d{2})\s+(take profit|stop loss) triggered",
            line,
        )
        if m and open_rec:
            win = "take" in m.group(2)
            entry = open_rec.get("entry")
            if entry is None:
                pnl_r = 1.0 if win else -1.0
            else:
                if open_rec["side"] == "buy":
                    risk = abs(entry - open_rec["sl"])
                    reward = abs(open_rec["tp"] - entry)
                else:
                    risk = abs(open_rec["sl"] - entry)
                    reward = abs(entry - open_rec["tp"])
                pnl_r = (reward / risk) if win and risk > 0 else -1.0
            trades.append(
                {
                    "win": win,
                    "pnl_r": pnl_r,
                    "hour": open_rec["t"].hour,
                    "dow": open_rec["t"].strftime("%a"),
                }
            )
            open_rec = None

    n = len(trades)
    wr = sum(1 for t in trades if t["win"]) / n if n else 0.0
    aw = st.mean([t["pnl_r"] for t in trades if t["win"]]) if any(t["win"] for t in trades) else 0.0
    al = (
        st.mean([abs(t["pnl_r"]) for t in trades if not t["win"]])
        if any(not t["win"] for t in trades)
        else 1.0
    )
    R = aw / al if al else 0.0
    bwr = 1 / (1 + R) if R > 0 else 1.0
    bm_pp = 100 * (wr - bwr)
    e_n = wr * (R + 1) - 1
    spreads = []
    for line in c.splitlines():
        m = re.search(
            r"market (?:buy|sell) [\d.]+ AUDUSD sl: [\d.]+ tp: [\d.]+ \(([\d.]+) / ([\d.]+)",
            line,
        )
        if m and "OrderSend" not in line:
            spreads.append(round((float(m.group(2)) - float(m.group(1))) / 0.00001))
    med_spread = st.median(spreads) if spreads else 15.0
    sl_pts = float(chosen["sl"]) if chosen["sl"] != "?" else 300.0
    c_r = (3.0 * med_spread) / sl_pts
    leak_pp = 100 * c_r / (R + 1)
    ef_pp = bm_pp - leak_pp
    z = 1.96
    m_pp = (
        100
        * (z / (1 + z * z / n))
        * math.sqrt(wr * (1 - wr) / n + z * z / (4 * n * n))
        if n
        else 0
    )
    zone = "Negative" if ef_pp <= 0 else ("Fragile" if ef_pp <= m_pp else "Robust")
    pnl = (chosen["final"] - 400.0) if chosen["final"] is not None else None

    beat_p0 = e_n >= P0["E_N"] and ef_pp >= P0["EF_pp"] and n >= 0.5 * P0["n"]
    beat_t02 = e_n >= T02["E_N"] - 1e-12
    interaction_tax = e_n < T02["E_N"] - 1e-12

    if not beat_p0:
        verdict = "REJECT"
        reason = "fails vs P0"
    elif beat_t02:
        verdict = "ACCEPT_STACK"
        reason = "beats P0 and P3-T02 alone"
    elif interaction_tax:
        verdict = "ACCEPT_P0_ONLY"
        reason = "beats P0 but interaction tax vs T02 — prefer T02 alone as champion filter"
    else:
        verdict = "ACCEPT"
        reason = "beats P0"

    out = {
        "task": "EDX-P5-T01",
        "identity": {
            "magic": "8230501",
            "StartHour": chosen["start"],
            "TradeMon": chosen["mon"],
            "SL_TP": f"{chosen['sl']}/{chosen['tp']}",
            "window": f"{chosen['from']}->{chosen['to']}",
        },
        "n": n,
        "WR": round(100 * wr, 2),
        "R": round(R, 3),
        "BM_pp": round(bm_pp, 2),
        "Leak_pp": round(leak_pp, 2),
        "EF_pp": round(ef_pp, 2),
        "M_pp": round(m_pp, 2),
        "E_N": round(e_n, 3),
        "pnl": round(pnl, 2) if pnl is not None else None,
        "final": chosen["final"],
        "zone": zone,
        "n_hour12": sum(1 for t in trades if t["hour"] == 12),
        "n_Mon": sum(1 for t in trades if t["dow"] == "Mon"),
        "delta_vs_P0": {
            "E_N": round(e_n - P0["E_N"], 3),
            "EF_pp": round(ef_pp - P0["EF_pp"], 2),
            "pnl": round((pnl or 0) - P0["pnl"], 2),
            "n": n - P0["n"],
        },
        "delta_vs_T02": {
            "E_N": round(e_n - T02["E_N"], 3),
            "EF_pp": round(ef_pp - T02["EF_pp"], 2),
            "pnl": round((pnl or 0) - T02["pnl"], 2),
            "n": n - T02["n"],
        },
        "verdict": verdict,
        "reason": reason,
        "champion_filter": "stack" if beat_t02 else ("T02_startHour13" if beat_p0 else "P0"),
    }
    (OUT / "SCORECARD.json").write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
