"""EDX-P8-T02: tip + long survival with P8-T01 Leak policy."""
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
POINT = 0.00001
SL_PTS = 300.0
P8_T01 = {"n": 47, "E_N": 0.404, "EF_pp": 17.78, "Leak_pp": 2.44, "pnl": 57.10}


def load(path: Path) -> str:
    raw = path.read_bytes()
    if raw[:2] == b"\xff\xfe":
        return raw.decode("utf-16-le")
    return raw.decode("utf-8", errors="replace")


def find_run(text: str, magics: list[str], from_p: str, to_p: str) -> dict:
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
        if not mag or mag.group(1) not in magics:
            continue
        sh = re.search(r"InpStartHour=([0-9.]+)", c)
        tm = re.search(r"InpTradeMon=(true|false)", c)
        if (sh.group(1) if sh else "?") != "13" or (tm.group(1) if tm else "?") != "false":
            continue
        if not s.group(1).startswith(from_p) or not s.group(2).startswith(to_p):
            continue
        finals = re.findall(r"final balance ([\d.]+)", c)
        cand = {
            "i": i,
            "magic": mag.group(1),
            "from": s.group(1),
            "to": s.group(2),
            "final": float(finals[-1]) if finals else None,
            "chunk": c,
        }
        if chosen is None or i > chosen["i"]:
            chosen = cand
    if not chosen:
        raise SystemExit(f"missing {magics} {from_p}->{to_p}")
    return chosen


def parse_trades(c: str) -> list[dict]:
    trades = []
    open_rec = None
    for line in c.splitlines():
        m = re.search(
            r"(\d{4}\.\d{2}\.\d{2} \d{2}:\d{2}:\d{2})\s+market (buy|sell) "
            r"([\d.]+) AUDUSD sl: ([\d.]+) tp: ([\d.]+) \(([\d.]+) / ([\d.]+)",
            line,
        )
        if m and "OrderSend" not in line:
            bid, ask = float(m.group(6)), float(m.group(7))
            open_rec = {
                "t": datetime.strptime(m.group(1), "%Y.%m.%d %H:%M:%S"),
                "side": m.group(2),
                "sl": float(m.group(4)),
                "tp": float(m.group(5)),
                "spread_pts": (ask - bid) / POINT,
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
                    "c_r": open_rec["spread_pts"] / SL_PTS,
                    "ym": open_rec["t"].strftime("%Y-%m"),
                }
            )
            open_rec = None
    return trades


def score(trades: list[dict], final: float | None) -> dict:
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
    c_r_mean = st.mean([t["c_r"] for t in trades]) if trades else 0.0
    leak_pp = 100 * c_r_mean / (R + 1)
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
    by_m: dict[str, list] = defaultdict(list)
    for t in trades:
        by_m[t["ym"]].append(t)
    months = {
        ym: {
            "n": len(ts),
            "WR": round(100 * sum(1 for x in ts if x["win"]) / len(ts), 1),
            "E_N": round(sum(x["pnl_r"] for x in ts) / len(ts), 3),
        }
        for ym, ts in sorted(by_m.items())
    }
    return {
        "n": n,
        "WR": round(100 * wr, 2),
        "R": round(R, 3),
        "BM_pp": round(bm_pp, 2),
        "c_R_mean": round(c_r_mean, 4),
        "Leak_pp": round(leak_pp, 2),
        "EF_pp": round(ef_pp, 2),
        "M_pp": round(m_pp, 2),
        "E_N": round(e_n, 3),
        "pnl": round(final - 400.0, 2) if final is not None else None,
        "zone": zone,
        "months": months,
        "G1_proxy": "PASS" if ef_pp > m_pp else "FAIL",
    }


def main() -> None:
    text = load(LOG)
    tip = find_run(text, ["8230802", "8230502"], "2026.05", "2026.10")
    long = find_run(text, ["8230803", "8230601"], "2026.03", "2026.09")
    tip_hv = score(parse_trades(tip["chunk"]), tip["final"])
    long_hv = score(parse_trades(long["chunk"]), long["final"])

    tip_ok = tip_hv["E_N"] > 0 and tip_hv["E_N"] > -0.2
    long_ok = long_hv["E_N"] > 0
    if tip_ok and long_ok:
        verdict = "ACCEPT_SURVIVAL"
        label = "WATCH" if tip_hv["zone"] != "Robust" or tip_hv["months"].get("2026-09", {}).get("E_N", 0) < 0 else "EXPANSION_KEEP"
    elif tip_ok or long_ok:
        verdict = "ACCEPT_SURVIVAL_PARTIAL"
        label = "WATCH"
    else:
        verdict = "REJECT"
        label = "DROP"

    out = {
        "task": "EDX-P8-T02",
        "leak_policy": "P8-T01 entry_spread c_R = spread_pts/SL",
        "tip": {
            "magic": tip["magic"],
            "window": f"{tip['from']}->{tip['to']}",
            **tip_hv,
            "delta_vs_P8_T01": {
                "E_N": round(tip_hv["E_N"] - P8_T01["E_N"], 3),
                "EF_pp": round(tip_hv["EF_pp"] - P8_T01["EF_pp"], 2),
                "n": tip_hv["n"] - P8_T01["n"],
            },
        },
        "long": {
            "magic": long["magic"],
            "window": f"{long['from']}->{long['to']}",
            **long_hv,
            "delta_vs_P8_T01": {
                "E_N": round(long_hv["E_N"] - P8_T01["E_N"], 3),
                "EF_pp": round(long_hv["EF_pp"] - P8_T01["EF_pp"], 2),
                "n": long_hv["n"] - P8_T01["n"],
            },
        },
        "pool_label": label,
        "verdict": verdict,
        "reason": "tip+long E_N>0 under measured Leak; Sep L3 expected",
    }
    (OUT / "SCORECARD.json").write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
