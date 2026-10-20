"""EDX-P8-T01: measured Leak on champ May→Aug (journal spreads; deal CSV optional)."""
from __future__ import annotations

import csv
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
INBOX = OUT.parents[1] / "inbox"
POINT = 0.00001
SL_PTS = 300.0


def load(path: Path) -> str:
    raw = path.read_bytes()
    if raw[:2] == b"\xff\xfe":
        return raw.decode("utf-16-le")
    return raw.decode("utf-8", errors="replace")


def find_inbox_deals() -> Path | None:
    if not INBOX.exists():
        return None
    for name in ("deals.csv", "blotter.csv", "ReportTester-*.csv"):
        hits = list(INBOX.glob(name if "*" not in name else name))
        if hits:
            return hits[0]
    for p in INBOX.iterdir():
        if p.is_file() and p.suffix.lower() in {".csv", ".jsonl"} and p.name.lower() != "readme.md":
            return p
    return None


def parse_run(
    text: str,
    *,
    magic_prefer: list[str],
    win_from_prefix: str,
    win_to_prefix: str,
    start: str = "13",
    mon: str = "false",
) -> dict:
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
        tm = re.search(r"InpTradeMon=(true|false)", c)
        finals = re.findall(r"final balance ([\d.]+)", c)
        if mval not in magic_prefer:
            continue
        if not s.group(1).startswith(win_from_prefix):
            continue
        if not s.group(2).startswith(win_to_prefix):
            continue
        if (sh.group(1) if sh else "?") != start:
            continue
        if (tm.group(1) if tm else "?") != mon:
            continue
        cand = {
            "i": i,
            "magic": mval,
            "from": s.group(1),
            "to": s.group(2),
            "final": float(finals[-1]) if finals else None,
            "chunk": c,
        }
        # prefer earlier magics in list (task-specific first)
        if chosen is None or magic_prefer.index(mval) < magic_prefer.index(chosen["magic"]):
            chosen = cand
        elif chosen and mval == chosen["magic"] and i > chosen["i"]:
            chosen = cand  # latest same magic
    if not chosen:
        raise SystemExit(
            f"no run magic={magic_prefer} window {win_from_prefix}*->{win_to_prefix}* Start={start} Mon={mon}"
        )
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
            spread_pts = (ask - bid) / POINT
            open_rec = {
                "t": datetime.strptime(m.group(1), "%Y.%m.%d %H:%M:%S"),
                "side": m.group(2),
                "sl": float(m.group(4)),
                "tp": float(m.group(5)),
                "spread_pts": spread_pts,
                "commission": 0.0,
                "swap": 0.0,
                "slippage_pts": 0.0,
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
            # Round-turn spread approx: entry spread in points / SL (commission/swap/slip=0)
            c_r = open_rec["spread_pts"] / SL_PTS
            trades.append(
                {
                    "win": win,
                    "pnl_r": pnl_r,
                    "c_r": c_r,
                    "spread_pts": open_rec["spread_pts"],
                    "ym": open_rec["t"].strftime("%Y-%m"),
                    "t": open_rec["t"],
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
    c_r_med = st.median([t["c_r"] for t in trades]) if trades else 0.0
    leak_pp = 100 * c_r_mean / (R + 1) if R >= 0 else 0.0
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
    months = {}
    from collections import defaultdict

    by_m: dict[str, list] = defaultdict(list)
    for t in trades:
        by_m[t["ym"]].append(t)
    for ym, ts in sorted(by_m.items()):
        nm = len(ts)
        months[ym] = {
            "n": nm,
            "WR": round(100 * sum(1 for x in ts if x["win"]) / nm, 1),
            "E_N": round(sum(x["pnl_r"] for x in ts) / nm, 3),
        }
    return {
        "n": n,
        "WR": round(100 * wr, 2),
        "R": round(R, 3),
        "BWR": round(100 * bwr, 2),
        "BM_pp": round(bm_pp, 2),
        "c_R_mean": round(c_r_mean, 4),
        "c_R_median": round(c_r_med, 4),
        "Leak_pp": round(leak_pp, 2),
        "EF_pp": round(ef_pp, 2),
        "M_pp": round(m_pp, 2),
        "E_N": round(e_n, 3),
        "pnl": round(pnl, 2) if pnl is not None else None,
        "zone": zone,
        "months": months,
        "spread_pts_median": round(st.median([t["spread_pts"] for t in trades]), 1) if trades else None,
    }


def main() -> None:
    inbox = find_inbox_deals()
    cost_source = "journal_entry_spread"
    gaps = ["commission_absent", "swap_absent", "slippage_absent", "no_deal_csv_export"]
    if inbox:
        gaps = ["deal_csv_present_but_parser_uses_journal_primary"]
        # keep journal primary; note path
        cost_source = f"journal_entry_spread+inbox:{inbox.name}"

    text = load(LOG)
    # Champ identity May→Aug: prefer 8230801, else 8230501 / 8230901 stack
    run = None
    for magics in (["8230801"], ["8230501", "8230901"]):
        try:
            run = parse_run(
                text,
                magic_prefer=magics,
                win_from_prefix="2026.05",
                win_to_prefix="2026.08",
            )
            break
        except SystemExit:
            continue
    if run is None:
        raise SystemExit("champ May→Aug stack run not found")

    trades = parse_trades(run["chunk"])
    hv = score(trades, run["final"])
    # vs prior proxy Leak 7.0–7.5pp (3×spread/SL)
    proxy_leak = 100 * (3.0 * (hv["spread_pts_median"] or 14) / SL_PTS) / (hv["R"] + 1)

    out = {
        "task": "EDX-P8-T01",
        "identity": {
            "magic_scored": run["magic"],
            "champ_authority": "8230901",
            "window": f"{run['from']}->{run['to']}",
            "StartHour": "13",
            "TradeMon": "false",
            "SL_TP": "300/300",
        },
        "cost_model": {
            "source": cost_source,
            "formula": "c_R = entry_spread_pts / SL_pts; Leak = c_R/(R+1)",
            "gaps": gaps,
            "vs_costs_defaulted_3x_spread": {
                "proxy_Leak_pp": round(proxy_leak, 2),
                "measured_Leak_pp": hv["Leak_pp"],
            },
        },
        **hv,
        "final": run["final"],
        "G1_proxy": "PASS" if hv["EF_pp"] > hv["M_pp"] else "FAIL",
        "verdict": "ACCEPT_LEAK_PARTIAL",
        "reason": "entry-spread Leak measured; commission/swap/slippage absent — not full deal blotter",
    }
    (OUT / "SCORECARD.json").write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
