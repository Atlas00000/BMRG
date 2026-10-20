"""Score quarterly / OOS AUDUSD champ-stack runs (magic 8230601)."""
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
DEPOSIT = 400.0
BWR = 0.50  # RR=1


def load(path: Path) -> str:
    raw = path.read_bytes()
    if raw[:2] == b"\xff\xfe":
        return raw.decode("utf-16-le")
    return raw.decode("utf-8", errors="replace")


def score_chunk(c: str, sl_pts: float, final: float | None) -> dict:
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
    c_r = (3.0 * med_spread) / sl_pts
    leak_pp = 100 * c_r / (R + 1) if R >= 0 else 0.0
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
    pnl = (final - DEPOSIT) if final is not None else None

    by_m: dict[str, list] = defaultdict(list)
    for t in trades:
        by_m[t["ym"]].append(t)
    months = {}
    for ym, ts in sorted(by_m.items()):
        nm = len(ts)
        wrm = sum(1 for t in ts if t["win"]) / nm
        enm = sum(t["pnl_r"] for t in ts) / nm
        months[ym] = {"n": nm, "WR": round(100 * wrm, 1), "E_N": round(enm, 3)}

    # max equity drawdown from cumulative R path (approx)
    eq = 0.0
    peak = 0.0
    max_dd_r = 0.0
    streak = 0
    max_loss_streak = 0
    for t in trades:
        eq += t["pnl_r"]
        peak = max(peak, eq)
        max_dd_r = max(max_dd_r, peak - eq)
        if not t["win"]:
            streak += 1
            max_loss_streak = max(max_loss_streak, streak)
        else:
            streak = 0

    return {
        "n": n,
        "WR": round(100 * wr, 2),
        "R": round(R, 3),
        "BWR": round(100 * bwr, 2),
        "BM_pp": round(bm_pp, 2),
        "Leak_pp": round(leak_pp, 2),
        "EF_pp": round(ef_pp, 2),
        "M_pp": round(m_pp, 2),
        "E_N": round(e_n, 3),
        "pnl": round(pnl, 2) if pnl is not None else None,
        "zone": zone,
        "max_dd_R": round(max_dd_r, 2),
        "max_loss_streak": max_loss_streak,
        "months": months,
        "med_spread": med_spread,
    }


def survive_label(hv: dict, window: str) -> str:
    """Survivability for expansion sleeve (not production G1)."""
    n = hv["n"]
    e_n = hv["E_N"]
    wr = hv["WR"]
    pnl = hv["pnl"] or 0.0
    if n < 8:
        return "THIN"
    if pnl <= -50 or e_n <= -0.25:
        return "WIPEOUT"
    if e_n <= 0 or wr < 50:
        return "FAIL"
    if e_n < 0.05:
        return "MARGINAL"
    return "SURVIVE"


def main() -> None:
    text = load(LOG)
    starts = list(
        re.finditer(
            r"AUDUSD,M5: testing of Experts\\BMRG\\BMRG\.ex5 from (\S+) 00:00 to (\S+) 00:00 started with inputs:",
            text,
        )
    )
    # OOS / quarter candidates: index >= 28 with champ stack
    rows = []
    for i, s in enumerate(starts):
        if i < 28:
            continue
        end = starts[i + 1].start() if i + 1 < len(starts) else len(text)
        c = text[s.start() : end]
        mag = re.search(r"InpMagic=(\d+)", c)
        sh = re.search(r"InpStartHour=([0-9.]+)", c)
        mon = re.search(r"InpTradeMon=(true|false)", c)
        sl = re.search(r"InpSL_Points=([0-9.]+)", c)
        tp = re.search(r"InpTP_Points=([0-9.]+)", c)
        finals = re.findall(r"final balance ([\d.]+)", c)
        if not mag or mag.group(1) != "8230601":
            continue
        if not sh or sh.group(1) != "13":
            continue
        if not mon or mon.group(1) != "false":
            continue
        final = float(finals[-1]) if finals else None
        sl_pts = float(sl.group(1)) if sl else 300.0
        win = f"{s.group(1)}->{s.group(2)}"
        hv = score_chunk(c, sl_pts, final)
        label = survive_label(hv, win)
        # tag IS vs OOS
        role = "IS_primary" if s.group(1) == "2026.05.01" and s.group(2).startswith("2026.08") else "OOS"
        if s.group(1).startswith("2026.01"):
            role = "OOS_2026_Q1"
        row = {
            "run": i,
            "window": win,
            "role": role,
            "magic": "8230601",
            "identity_ok": True,
            **hv,
            "final": final,
            "survive": label,
        }
        rows.append(row)
        print(
            f"[{i}] {win} n={hv['n']} WR={hv['WR']}% E_N={hv['E_N']} "
            f"EF={hv['EF_pp']} pnl={hv['pnl']} ddR={hv['max_dd_R']} -> {label}"
        )

    # summary
    oos = [r for r in rows if r["survive"] != "THIN" or True]
    survive_n = sum(1 for r in rows if r["survive"] in ("SURVIVE", "MARGINAL") and "2026.05" not in r["window"][:10] or (r["role"] != "IS_primary" and r["survive"] in ("SURVIVE", "MARGINAL")))
    oos_only = [r for r in rows if r["role"] != "IS_primary"]
    n_oos = len(oos_only)
    n_ok = sum(1 for r in oos_only if r["survive"] in ("SURVIVE", "MARGINAL"))
    n_fail = sum(1 for r in oos_only if r["survive"] in ("FAIL", "WIPEOUT"))
    n_thin = sum(1 for r in oos_only if r["survive"] == "THIN")

    out = {
        "task": "AUDUSD-CHAMP-OOS-quarters",
        "stack": "Start13+skipMon+skipTue SL300/TP300 (freeze magic 8230601)",
        "BWR_designed": 50.0,
        "runs": rows,
        "survivability": {
            "oos_quarters": n_oos,
            "SURVIVE_or_MARGINAL": n_ok,
            "FAIL_or_WIPEOUT": n_fail,
            "THIN": n_thin,
            "positive_E_N_share": round(
                sum(1 for r in oos_only if r["E_N"] > 0) / n_oos, 2
            )
            if n_oos
            else None,
            "verdict": None,
        },
    }
    # Verdict logic
    if n_fail >= 2 and n_ok <= 1:
        verdict = "WEAK_SURVIVAL — multiple OOS quarters fail; tip/regime sensitive"
    elif n_ok >= max(2, n_oos - 1) and n_fail == 0:
        verdict = "SURVIVES_OOS — most quarters E_N>0 / not wipeout"
    elif n_ok >= 1 and n_fail >= 1:
        verdict = "MIXED — some quarters hold, some fail (regime_filtered / L3 OK for expansion)"
    else:
        verdict = "INCONCLUSIVE"
    out["survivability"]["verdict"] = verdict

    (OUT / "SCORECARD.json").write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(json.dumps(out["survivability"], indent=2))


if __name__ == "__main__":
    main()
