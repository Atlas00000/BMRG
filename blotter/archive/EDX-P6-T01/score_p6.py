"""Score EDX-P6-T01 freeze candidate on long window."""
from __future__ import annotations

import json
import math
import re
import statistics as st
from collections import defaultdict
from datetime import datetime
from pathlib import Path

LOG = Path(
    r"C:\Users\emili\AppData\Roaming\MetaQuotes\Terminal"
    r"\D0E8209F77C8CF37AD8BF550E51FF075\Tester\logs\20261007.log"
)
OUT = Path(__file__).resolve().parent

P5_MAY = {"n": 47, "WR": 70.2, "E_N": 0.404, "EF_pp": 13.21, "pnl": 57.10}
P5_TIP = {"n": 61, "WR": 60.66, "E_N": 0.213, "EF_pp": 3.16, "pnl": 39.10}
P0 = {"n": 58, "WR": 62.07, "E_N": 0.241, "EF_pp": 4.57, "pnl": 44.39}


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
    print("starts", len(starts))
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
        if mval in ("8230601", "8230502", "8230501"):
            print(
                f"[{i}] {s.group(1)}->{s.group(2)} mag={mval} "
                f"Start={sh.group(1) if sh else '?'} Mon={mon.group(1) if mon else '?'} "
                f"SL/TP={(sl.group(1) if sl else '?')}/{(tp.group(1) if tp else '?')} "
                f"final={finals[-1] if finals else '?'}"
            )
        if mval != "8230601":
            continue
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
        if cand["start"] == "13" and cand["mon"] == "false":
            chosen = cand
        elif chosen is None:
            chosen = cand

    if not chosen:
        raise SystemExit("8230601 not found")

    # Identity checks
    ok_win = chosen["from"].startswith("2026.03") and chosen["to"].startswith("2026.09")
    ok_stack = chosen["start"] == "13" and chosen["mon"] == "false"
    print(
        "scoring",
        chosen["i"],
        "window",
        f"{chosen['from']}->{chosen['to']}",
        "ok_win",
        ok_win,
        "ok_stack",
        ok_stack,
        "final",
        chosen["final"],
    )

    if not ok_stack:
        out = {
            "task": "EDX-P6-T01",
            "verdict": "INVALID",
            "reason": "stack identity fail",
            "identity": chosen,
        }
        (OUT / "SCORECARD.json").write_text(json.dumps(out, indent=2), encoding="utf-8")
        print(json.dumps(out, indent=2))
        return

    if not ok_win:
        out = {
            "task": "EDX-P6-T01",
            "verdict": "INVALID",
            "reason": f"wrong window {chosen['from']}->{chosen['to']}; expect 2026.03.23->2026.09.21",
            "identity": {
                "magic": "8230601",
                "StartHour": chosen["start"],
                "TradeMon": chosen["mon"],
                "window": f"{chosen['from']}->{chosen['to']}",
            },
        }
        (OUT / "SCORECARD.json").write_text(json.dumps(out, indent=2), encoding="utf-8")
        print(json.dumps(out, indent=2))
        return

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
                    "ym": open_rec["t"].strftime("%Y-%m"),
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

    by_m: dict[str, list] = defaultdict(list)
    for t in trades:
        by_m[t["ym"]].append(t)
    months = {}
    for ym, ts in sorted(by_m.items()):
        nm = len(ts)
        wrm = sum(1 for t in ts if t["win"]) / nm
        enm = sum(t["pnl_r"] for t in ts) / nm
        months[ym] = {"n": nm, "WR": round(100 * wrm, 1), "E_N": round(enm, 3)}

    n_tier = (
        "Insufficient"
        if n < 100
        else ("Thin" if n < 200 else ("Adequate" if n < 400 else "Solid"))
    )
    g1_ready = ef_pp > m_pp and e_n > 0
    positive = e_n > 0

    if not positive:
        verdict = "REJECT"
        reason = "long-window E_N<=0"
    elif n < 30:
        verdict = "REJECT"
        reason = "n too thin for freeze"
    else:
        verdict = "ACCEPT_FREEZE"
        reason = f"E_N>0 · n_tier={n_tier} · ready for G1 checklist (G1_proxy={'PASS' if g1_ready else 'FAIL Fragile'})"

    out = {
        "task": "EDX-P6-T01",
        "identity": {
            "magic": "8230601",
            "StartHour": chosen["start"],
            "TradeMon": chosen["mon"],
            "SL_TP": f"{chosen['sl']}/{chosen['tp']}",
            "window": f"{chosen['from']}->{chosen['to']}",
        },
        "n": n,
        "n_tier": n_tier,
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
        "G1_proxy": "PASS" if g1_ready else "FAIL",
        "n_hour12": sum(1 for t in trades if t["hour"] == 12),
        "n_Mon": sum(1 for t in trades if t["dow"] == "Mon"),
        "months": months,
        "delta_vs_P5_MAY": {
            "E_N": round(e_n - P5_MAY["E_N"], 3),
            "EF_pp": round(ef_pp - P5_MAY["EF_pp"], 2),
            "n": n - P5_MAY["n"],
        },
        "delta_vs_P0": {
            "E_N": round(e_n - P0["E_N"], 3),
            "EF_pp": round(ef_pp - P0["EF_pp"], 2),
            "n": n - P0["n"],
        },
        "verdict": verdict,
        "reason": reason,
    }
    (OUT / "SCORECARD.json").write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
