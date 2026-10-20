"""Score EDX-P0-T04 tip stress (prefer mag 8230104 + May->Oct)."""
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
P0 = {
    "n": 58,
    "WR": 62.07,
    "E_N": 0.241,
    "EF_pp": 4.57,
    "BM_pp": 12.07,
    "pnl": 44.39,
}


def load(path: Path) -> str:
    raw = path.read_bytes()
    if raw[:2] == b"\xff\xfe":
        return raw.decode("utf-16-le")
    return raw.decode("utf-8", errors="replace")


def score_chunk(chunk: str, meta: dict) -> dict:
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
                pnl_r = (reward / risk) if win and risk > 0 else (-1.0 if not win else 1.0)
            trades.append({**open_rec, "win": win, "pnl_r": pnl_r})
            open_rec = None

    n = len(trades)
    wins = [t for t in trades if t["win"]]
    losses = [t for t in trades if not t["win"]]
    wr = len(wins) / n if n else 0.0
    aw = st.mean([t["pnl_r"] for t in wins]) if wins else 0.0
    al = st.mean([abs(t["pnl_r"]) for t in losses]) if losses else 1.0
    R = aw / al if al else 0.0
    RR = float(meta["tp"]) / float(meta["sl"]) if meta.get("sl") not in (None, "?") else 1.0
    bwr = 1 / (1 + R) if R > 0 else 1.0
    bm = wr - bwr
    e_n = wr * (R + 1) - 1
    spreads = []
    for line in chunk.splitlines():
        m = re.search(
            r"market (?:buy|sell) [\d.]+ AUDUSD sl: [\d.]+ tp: [\d.]+ \(([\d.]+) / ([\d.]+)",
            line,
        )
        if m and "OrderSend" not in line:
            spreads.append(round((float(m.group(2)) - float(m.group(1))) / 0.00001))
    med_spread = st.median(spreads) if spreads else 15.0
    sl_pts = float(meta["sl"]) if meta.get("sl") not in (None, "?") else 300.0
    c_r = (3.0 * med_spread) / sl_pts
    leak_pp = 100 * c_r / (R + 1)
    bm_pp = 100 * bm
    ef_pp = bm_pp - leak_pp
    z = 1.96
    half = (
        (z / (1 + z * z / n)) * math.sqrt(wr * (1 - wr) / n + z * z / (4 * n * n))
        if n
        else 0
    )
    m_pp = 100 * half
    zone = "Negative" if ef_pp <= 0 else ("Fragile" if ef_pp <= m_pp else "Robust")
    tier = "Insufficient" if n < 100 else ("Provisional" if n < 385 else "Standard")

    monthly = {}
    for t in trades:
        mo = t["t"].strftime("%Y-%m")
        monthly.setdefault(mo, {"w": 0, "l": 0})
        monthly[mo]["w" if t["win"] else "l"] += 1
    monthly_out = {}
    for mo, v in sorted(monthly.items()):
        nn = v["w"] + v["l"]
        wrr = v["w"] / nn
        monthly_out[mo] = {
            "n": nn,
            "WR": round(100 * wrr, 1),
            "E_N": round(wrr * (R + 1) - 1, 3),
        }

    # Sep/Oct tip cells
    tip = {k: v for k, v in monthly_out.items() if k >= "2026-09"}

    final = meta["final"]
    deposit = meta["deposit"]
    pnl = (final - deposit) if final is not None else None

    side = "WR-side" if abs(RR - R) < 0.2 and 0.85 <= al <= 1.15 else "check"
    return {
        "task": "EDX-P0-T04",
        "window": f"{meta['from']}->{meta['to']}",
        "magic": meta["magic"],
        "sl_tp": f"{meta['sl']}/{meta['tp']}",
        "identity_ok": meta["magic"] == "8230104"
        and meta["from"].startswith("2026.05")
        and meta["to"] >= "2026.10",
        "n": n,
        "WR": round(100 * wr, 2),
        "AW": round(aw, 3),
        "AL": round(al, 3),
        "R": round(R, 3),
        "RR": round(RR, 3),
        "RR_R": round(RR - R, 3),
        "BWR": round(100 * bwr, 2),
        "BM_pp": round(bm_pp, 2),
        "Leak_pp": round(leak_pp, 2),
        "EF_pp": round(ef_pp, 2),
        "M_wilson_pp": round(m_pp, 2),
        "E_N": round(e_n, 3),
        "PF": round((wr * aw) / ((1 - wr) * al), 3) if (1 - wr) * al > 0 else None,
        "final": final,
        "pnl": round(pnl, 2) if pnl is not None else None,
        "zone": zone,
        "tier": tier,
        "side": side,
        "monthly": monthly_out,
        "tip_months": tip,
        "delta_vs_P0": {
            "E_N": round(e_n - P0["E_N"], 3),
            "EF_pp": round(ef_pp - P0["EF_pp"], 2),
            "WR": round(100 * wr - P0["WR"], 2),
            "pnl": round((pnl or 0) - P0["pnl"], 2),
            "n": n - P0["n"],
        },
        "med_spread_pts": med_spread,
        "init": meta.get("init"),
    }


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
        finals = re.findall(r"final balance ([\d.]+)", c)
        dep = re.search(r"initial deposit ([\d.]+)", c)
        init = re.search(r"BMRG init OK \| ([^\r\n]+)", c)
        meta = {
            "from": s.group(1),
            "to": s.group(2),
            "magic": mag.group(1) if mag else "?",
            "sl": sl.group(1) if sl else "?",
            "tp": tp.group(1) if tp else "?",
            "final": float(finals[-1]) if finals else None,
            "deposit": float(dep.group(1)) if dep else 400.0,
            "init": init.group(1) if init else "?",
            "chunk": c,
        }
        runs.append(meta)
        print(
            f"[{i}] {meta['from']}->{meta['to']} mag={meta['magic']} "
            f"SL/TP={meta['sl']}/{meta['tp']} final={meta['final']}"
        )

    # Prefer 8230104 with to >= 2026.10; else last 8230104; else last run
    chosen = None
    for r in runs:
        if r["magic"] == "8230104" and r["to"] >= "2026.10":
            chosen = r
    if chosen is None:
        for r in reversed(runs):
            if r["magic"] == "8230104":
                chosen = r
                break
    if chosen is None:
        chosen = runs[-1]
        print("NOTE: no 8230104 — scoring last run")

    score = score_chunk(chosen["chunk"], chosen)
    (OUT / "SCORECARD.json").write_text(json.dumps(score, indent=2), encoding="utf-8")
    print(json.dumps(score, indent=2))


if __name__ == "__main__":
    main()
