"""Score EDX-P5-T02 tip stack vs P0-T04 and P5-T01."""
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

# Tip baseline (P0-T04) and MayAug stack (P5-T01)
P0_TIP = {"n": 73, "WR": 56.16, "E_N": 0.123, "EF_pp": -1.34, "pnl": 27.80}
P5_T01 = {"n": 47, "WR": 70.2, "E_N": 0.404, "EF_pp": 13.21, "pnl": 57.10}


def load(path: Path) -> str:
    raw = path.read_bytes()
    if raw[:2] == b"\xff\xfe":
        return raw.decode("utf-16-le")
    return raw.decode("utf-8", errors="replace")


def parse_trades(c: str, sl_fallback: float) -> tuple[list[dict], float]:
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

    spreads = []
    for line in c.splitlines():
        m = re.search(
            r"market (?:buy|sell) [\d.]+ AUDUSD sl: [\d.]+ tp: [\d.]+ \(([\d.]+) / ([\d.]+)",
            line,
        )
        if m and "OrderSend" not in line:
            spreads.append(round((float(m.group(2)) - float(m.group(1))) / 0.00001))
    med_spread = st.median(spreads) if spreads else 15.0
    return trades, med_spread


def score(trades: list[dict], med_spread: float, sl_pts: float, final: float | None) -> dict:
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
    pnl = (final - 400.0) if final is not None else None

    by_m: dict[str, list] = defaultdict(list)
    for t in trades:
        by_m[t["ym"]].append(t)
    months = {}
    for ym, ts in sorted(by_m.items()):
        nm = len(ts)
        wrm = sum(1 for t in ts if t["win"]) / nm
        enm = sum(t["pnl_r"] for t in ts) / nm
        months[ym] = {
            "n": nm,
            "WR": round(100 * wrm, 1),
            "E_N": round(enm, 3),
        }

    return {
        "n": n,
        "WR": round(100 * wr, 2),
        "R": round(R, 3),
        "BM_pp": round(bm_pp, 2),
        "Leak_pp": round(leak_pp, 2),
        "EF_pp": round(ef_pp, 2),
        "M_pp": round(m_pp, 2),
        "E_N": round(e_n, 3),
        "pnl": round(pnl, 2) if pnl is not None else None,
        "zone": zone,
        "n_hour12": sum(1 for t in trades if t["hour"] == 12),
        "n_Mon": sum(1 for t in trades if t["dow"] == "Mon"),
        "months": months,
        "med_spread": med_spread,
    }


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
        if mval in ("8230501", "8230502", "8230104"):
            print(
                f"[{i}] {s.group(1)}->{s.group(2)} mag={mval} "
                f"Start={sh.group(1) if sh else '?'} Mon={mon.group(1) if mon else '?'} "
                f"SL/TP={(sl.group(1) if sl else '?')}/{(tp.group(1) if tp else '?')} "
                f"final={finals[-1] if finals else '?'}"
            )
        if mval != "8230502":
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
        raise SystemExit("8230502 not found")
    print(
        "scoring run",
        chosen["i"],
        "Start",
        chosen["start"],
        "Mon",
        chosen["mon"],
        "final",
        chosen["final"],
        "window",
        f"{chosen['from']}->{chosen['to']}",
    )

    sl_pts = float(chosen["sl"]) if chosen["sl"] != "?" else 300.0
    trades, med_spread = parse_trades(chosen["chunk"], sl_pts)
    hv = score(trades, med_spread, sl_pts, chosen["final"])

    e_n = hv["E_N"]
    ef_pp = hv["EF_pp"]
    n = hv["n"]
    pnl = hv["pnl"] or 0.0
    sep = hv["months"].get("2026-09", {})
    sep_wipe = sep.get("E_N", 0) < -0.3 if sep else False
    wipeout = e_n <= -0.2 or (pnl is not None and pnl < -50)

    # Accept: not wipeout; prefer E_N>0; tip improvement vs P0-T04 valued
    beat_tip_en = e_n > P0_TIP["E_N"]
    beat_tip_ef = ef_pp > P0_TIP["EF_pp"]
    positive = e_n > 0

    if wipeout:
        verdict = "REJECT"
        reason = "tip wipeout / severe loss"
    elif positive and (beat_tip_en or beat_tip_ef):
        verdict = "ACCEPT_TIP"
        reason = "E_N>0 and improves tip vs P0-T04; L3 cells noted if present"
    elif positive:
        verdict = "ACCEPT_TIP_HOLD"
        reason = "E_N>0 on tip (class survives); no clear beat of P0 tip EF"
    else:
        verdict = "ACCEPT_L3_ONLY"
        reason = "tip E_N<=0 — L3 regime leak; MayAug stack still champion if primary held"

    out = {
        "task": "EDX-P5-T02",
        "identity": {
            "magic": "8230502",
            "StartHour": chosen["start"],
            "TradeMon": chosen["mon"],
            "SL_TP": f"{chosen['sl']}/{chosen['tp']}",
            "window": f"{chosen['from']}->{chosen['to']}",
        },
        **hv,
        "final": chosen["final"],
        "delta_vs_P0_TIP": {
            "E_N": round(e_n - P0_TIP["E_N"], 3),
            "EF_pp": round(ef_pp - P0_TIP["EF_pp"], 2),
            "pnl": round(pnl - P0_TIP["pnl"], 2),
            "n": n - P0_TIP["n"],
        },
        "delta_vs_P5_T01": {
            "E_N": round(e_n - P5_T01["E_N"], 3),
            "EF_pp": round(ef_pp - P5_T01["EF_pp"], 2),
            "pnl": round(pnl - P5_T01["pnl"], 2),
            "n": n - P5_T01["n"],
        },
        "sep_L3": sep_wipe,
        "verdict": verdict,
        "reason": reason,
        "champion_sleeve": "P5 stack Start13+skipMon SL300/300 (MayAug primary; tip L3 OK)",
    }
    (OUT / "SCORECARD.json").write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
