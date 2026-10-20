"""Score EDX-P3 filter presets vs P0-T01."""
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

P0 = {"n": 58, "WR": 62.07, "E_N": 0.241, "EF_pp": 4.57, "BM_pp": 12.07, "pnl": 44.39}

P3 = {
    "8230301": "EDX-P3-T01_skipMon",
    "8230302": "EDX-P3-T02_startHour13",
    "8230303": "EDX-P3-T03_BBDev2.5",
    "8230304": "EDX-P3-T04_cooldown6",
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
                pnl_r = (reward / risk) if win and risk > 0 else -1.0
            trades.append({"win": win, "pnl_r": pnl_r, "hour": open_rec["t"].hour, "dow": open_rec["t"].strftime("%a")})
            open_rec = None

    n = len(trades)
    wins = [t for t in trades if t["win"]]
    losses = [t for t in trades if not t["win"]]
    wr = len(wins) / n if n else 0.0
    aw = st.mean([t["pnl_r"] for t in wins]) if wins else 0.0
    al = st.mean([abs(t["pnl_r"]) for t in losses]) if losses else 1.0
    R = aw / al if al else 0.0
    sl_pts = float(meta["sl"]) if meta["sl"] != "?" else 300.0
    tp_pts = float(meta["tp"]) if meta["tp"] != "?" else 300.0
    RR = tp_pts / sl_pts if sl_pts else 1.0
    bwr = 1 / (1 + R) if R > 0 else 1.0
    bm_pp = 100 * (wr - bwr)
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
    c_r = (3.0 * med_spread) / sl_pts
    leak_pp = 100 * c_r / (R + 1) if R >= 0 else 0
    ef_pp = bm_pp - leak_pp
    z = 1.96
    half = (
        (z / (1 + z * z / n)) * math.sqrt(wr * (1 - wr) / n + z * z / (4 * n * n))
        if n
        else 0
    )
    m_pp = 100 * half
    zone = "Negative" if ef_pp <= 0 else ("Fragile" if ef_pp <= m_pp else "Robust")
    final = meta["final"]
    pnl = (final - meta["deposit"]) if final is not None else None

    freq_ok = n >= 0.5 * P0["n"]
    beat_en = e_n >= P0["E_N"] - 1e-12
    beat_ef = ef_pp >= P0["EF_pp"] - 1e-12
    wr_up_en_down = (wr * 100 > P0["WR"]) and (e_n < P0["E_N"])

    if n == 0:
        verdict, reason = "INVALID", "no trades / init fail"
    elif not freq_ok:
        verdict, reason = "REJECT", "FREQUENCY_STALL n<50% P0"
    elif wr_up_en_down:
        verdict, reason = "REJECT", "WR up E_N down"
    elif beat_en and beat_ef:
        verdict, reason = "ACCEPT", "E_N and EF >= P0"
    elif e_n > 0 and wr > bwr and (e_n > P0["E_N"] or ef_pp > P0["EF_pp"]):
        verdict, reason = "ACCEPT_SOFT", "improves one of E_N/EF, other close, admission OK"
    elif e_n > 0 and wr > bwr:
        verdict, reason = "POOL_KEEP", "alive but does not beat P0"
    else:
        verdict, reason = "REJECT", "fails E_N>0 or WR>BWR"

    # filter sanity
    hour12 = sum(1 for t in trades if t["hour"] == 12)
    mon = sum(1 for t in trades if t["dow"] == "Mon")

    return {
        "task": P3[meta["magic"]],
        "magic": meta["magic"],
        "window": f"{meta['from']}->{meta['to']}",
        "sl_tp": f"{meta['sl']}/{meta['tp']}",
        "bb": meta.get("bb"),
        "start_hour": meta.get("start"),
        "trade_mon": meta.get("mon"),
        "cooldown": meta.get("cd"),
        "n": n,
        "WR": round(100 * wr, 2),
        "R": round(R, 3),
        "RR": round(RR, 3),
        "BM_pp": round(bm_pp, 2),
        "Leak_pp": round(leak_pp, 2),
        "EF_pp": round(ef_pp, 2),
        "M_pp": round(m_pp, 2),
        "E_N": round(e_n, 3),
        "pnl": round(pnl, 2) if pnl is not None else None,
        "final": final,
        "zone": zone,
        "n_hour12": hour12,
        "n_Mon": mon,
        "freq_vs_P0": round(n / P0["n"], 2) if P0["n"] else None,
        "delta_vs_P0": {
            "E_N": round(e_n - P0["E_N"], 3),
            "EF_pp": round(ef_pp - P0["EF_pp"], 2),
            "WR": round(100 * wr - P0["WR"], 2),
            "pnl": round((pnl or 0) - P0["pnl"], 2),
            "n": n - P0["n"],
        },
        "verdict": verdict,
        "reason": reason,
    }


def main() -> None:
    text = load(LOG)
    print("log_bytes", LOG.stat().st_size, "mtime", LOG.stat().st_mtime)
    starts = list(
        re.finditer(
            r"AUDUSD,M5: testing of Experts\\BMRG\\BMRG\.ex5 from (\S+) 00:00 to (\S+) 00:00 started with inputs:",
            text,
        )
    )
    print("runs", len(starts))
    seen = {}
    for i, s in enumerate(starts):
        end = starts[i + 1].start() if i + 1 < len(starts) else len(text)
        c = text[s.start() : end]
        mag = re.search(r"InpMagic=(\d+)", c)
        mval = mag.group(1) if mag else "?"
        sl = re.search(r"InpSL_Points=([0-9.]+)", c)
        tp = re.search(r"InpTP_Points=([0-9.]+)", c)
        bb = re.search(r"InpBBDev=([0-9.]+)", c)
        sh = re.search(r"InpStartHour=([0-9.]+)", c)
        mon = re.search(r"InpTradeMon=(true|false)", c)
        cd = re.search(r"InpCooldownBars=([0-9.]+)", c)
        finals = re.findall(r"final balance ([\d.]+)", c)
        dep = re.search(r"initial deposit ([\d.]+)", c)
        print(
            f"[{i}] {s.group(1)}->{s.group(2)} mag={mval} "
            f"SL/TP={(sl.group(1) if sl else '?')}/{(tp.group(1) if tp else '?')} "
            f"BB={(bb.group(1) if bb else '?')} Start={(sh.group(1) if sh else '?')} "
            f"Mon={(mon.group(1) if mon else '?')} CD={(cd.group(1) if cd else '?')} "
            f"final={finals[-1] if finals else '?'}"
        )
        if mval not in P3:
            continue
        seen[mval] = {
            "from": s.group(1),
            "to": s.group(2),
            "magic": mval,
            "sl": sl.group(1) if sl else "?",
            "tp": tp.group(1) if tp else "?",
            "bb": bb.group(1) if bb else "?",
            "start": sh.group(1) if sh else "?",
            "mon": mon.group(1) if mon else "?",
            "cd": cd.group(1) if cd else "?",
            "final": float(finals[-1]) if finals else None,
            "deposit": float(dep.group(1)) if dep else 400.0,
            "chunk": c,
        }

    results = []
    for mval in ("8230301", "8230302", "8230303", "8230304"):
        if mval not in seen:
            print("MISSING", mval)
            continue
        sc = score_chunk(seen[mval]["chunk"], seen[mval])
        results.append(sc)
        print(
            f"{sc['task']}: n={sc['n']} WR={sc['WR']}% E_N={sc['E_N']:+.3f} "
            f"EF={sc['EF_pp']:+.2f} pnl={sc['pnl']} h12={sc['n_hour12']} Mon={sc['n_Mon']} "
            f"-> {sc['verdict']} ({sc['reason']})"
        )

    (OUT / "SCORECARD.json").write_text(json.dumps(results, indent=2), encoding="utf-8")
    print("wrote", len(results), "P3 results")


if __name__ == "__main__":
    main()
