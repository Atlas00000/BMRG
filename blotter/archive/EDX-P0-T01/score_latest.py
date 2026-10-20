"""Score latest AUDUSD tester run from 20261007.log (robust)."""
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


def load(path: Path) -> str:
    raw = path.read_bytes()
    if raw[:2] == b"\xff\xfe":
        return raw.decode("utf-16-le")
    if raw[:2] == b"\xfe\xff":
        return raw.decode("utf-16-be")
    if len(raw) > 2 and raw[1] == 0:
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
        chunk = text[s.start() : end]
        # stop at connection closed / thread finished of next if present early
        mag = re.search(r"InpMagic=(\d+)", chunk)
        sl = re.search(r"InpSL_Points=([0-9.]+)", chunk)
        tp = re.search(r"InpTP_Points=([0-9.]+)", chunk)
        bb = re.search(r"InpBBDev=([0-9.]+)", chunk)
        init = re.search(r"BMRG init OK \| ([^\r\n]+)", chunk)
        opens = len(re.findall(r"\[BMRG\]\[TRADE\] OPEN", chunk))
        finals = re.findall(r"final balance ([\d.]+)", chunk)
        tpc = len(re.findall(r"take profit triggered", chunk, flags=re.I))
        slc = len(re.findall(r"stop loss triggered", chunk, flags=re.I))
        dep = re.search(r"initial deposit ([\d.]+)", chunk)
        runs.append(
            {
                "i": i,
                "from": s.group(1),
                "to": s.group(2),
                "magic": mag.group(1) if mag else "?",
                "sl": sl.group(1) if sl else "?",
                "tp": tp.group(1) if tp else "?",
                "bb": bb.group(1) if bb else "?",
                "init": init.group(1) if init else "?",
                "opens": opens,
                "tp_n": tpc,
                "sl_n": slc,
                "final": float(finals[-1]) if finals else None,
                "deposit": float(dep.group(1)) if dep else 400.0,
                "chunk": chunk,
            }
        )
        print(
            f"[{i}] {s.group(1)}->{s.group(2)} mag={runs[-1]['magic']} "
            f"SL/TP={runs[-1]['sl']}/{runs[-1]['tp']} BB={runs[-1]['bb']} "
            f"opens={opens} tp={tpc} sl={slc} final={runs[-1]['final']}"
        )

    # Prefer 8230101; else last run
    chosen = None
    for r in runs:
        if r["magic"] == "8230101":
            chosen = r
    if chosen is None:
        chosen = runs[-1]
        print("NOTE: EDX magic 8230101 not found; scoring LAST run")

    chunk = chosen["chunk"]
    # parse trades
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
        m = re.search(
            r"deal #\d+ (buy|sell) ([\d.]+) AUDUSD at ([\d.]+)",
            line,
        )
        if m and open_rec and "entry" not in open_rec and m.group(1) == open_rec["side"]:
            open_rec["entry"] = float(m.group(3))
            continue
        m = re.search(
            r"(\d{4}\.\d{2}\.\d{2} \d{2}:\d{2}:\d{2})\s+(take profit|stop loss) triggered",
            line,
        )
        if m and open_rec:
            ct = datetime.strptime(m.group(1), "%Y.%m.%d %H:%M:%S")
            win = "take" in m.group(2)
            entry = open_rec.get("entry")
            if entry is None:
                pnl_r = 1.0 if win else -1.0
                rr_i = abs(open_rec["tp"] - open_rec["sl"])  # unused
            else:
                if open_rec["side"] == "buy":
                    risk = abs(entry - open_rec["sl"])
                    reward = abs(open_rec["tp"] - entry)
                else:
                    risk = abs(open_rec["sl"] - entry)
                    reward = abs(entry - open_rec["tp"])
                if risk <= 0:
                    pnl_r = 1.0 if win else -1.0
                else:
                    pnl_r = (reward / risk) if win else -1.0
            trades.append(
                {
                    **open_rec,
                    "close": ct,
                    "win": win,
                    "pnl_r": pnl_r,
                    "hold_h": (ct - open_rec["t"]).total_seconds() / 3600.0,
                }
            )
            open_rec = None

    n = len(trades)
    wins = [t for t in trades if t["win"]]
    losses = [t for t in trades if not t["win"]]
    wr = len(wins) / n if n else 0.0
    aw = st.mean([t["pnl_r"] for t in wins]) if wins else 0.0
    al = st.mean([abs(t["pnl_r"]) for t in losses]) if losses else 1.0
    R = aw / al if al else 0.0
    designed_sl = float(chosen["sl"]) if chosen["sl"] != "?" else 300.0
    designed_tp = float(chosen["tp"]) if chosen["tp"] != "?" else 300.0
    RR = designed_tp / designed_sl if designed_sl else 1.0
    bwr = 1.0 / (1.0 + R) if R > 0 else 1.0
    bm = wr - bwr
    fmi = bm / bwr if bwr else 0.0
    e_n = wr * (R + 1) - 1
    pf = (wr * aw) / ((1 - wr) * al) if (1 - wr) * al > 0 else float("inf")

    spreads = []
    for line in chunk.splitlines():
        m = re.search(
            r"market (?:buy|sell) [\d.]+ AUDUSD sl: [\d.]+ tp: [\d.]+ \(([\d.]+) / ([\d.]+)",
            line,
        )
        if m and "OrderSend" not in line:
            spreads.append(round((float(m.group(2)) - float(m.group(1))) / 0.00001))
    med_spread = st.median(spreads) if spreads else 10.0
    c_r = (3.0 * med_spread) / designed_sl
    leak = c_r / (R + 1)
    leak_pp = leak * 100
    bm_pp = bm * 100
    ef_pp = bm_pp - leak_pp
    z = 1.96
    center = (wr + z * z / (2 * n)) / (1 + z * z / n) if n else 0
    half = (
        (z / (1 + z * z / n)) * math.sqrt(wr * (1 - wr) / n + z * z / (4 * n * n))
        if n
        else 0
    )
    m_wilson_pp = half * 100
    m_norm_pp = 1.96 * 100 * math.sqrt(wr * (1 - wr) / n) if n else 0

    if ef_pp <= 0:
        zone = "Negative"
    elif ef_pp <= m_wilson_pp:
        zone = "Fragile"
    else:
        zone = "Robust"
    tier = "Insufficient" if n < 100 else ("Provisional" if n < 385 else "Standard")

    if abs(RR - R) < 0.2 and 0.85 <= al <= 1.15:
        side = "WR-side"
        r_claim = "REJECTED (R~RR; AL~1R)"
    elif R < RR - 0.25 or (aw and al > aw * 1.2):
        side = "R-side"
        r_claim = "SUPPORTED"
    else:
        side = "both / inconclusive"
        r_claim = "OPEN"

    # identity check for EDX-P0-T01 AUDUSD
    expected = {
        "magic": "8230101",
        "sl": "300",
        "tp": "300",
        "bb": "2.2",
    }
    identity_ok = (
        chosen["magic"] == expected["magic"]
        and chosen["sl"].startswith("300")
        and chosen["tp"].startswith("300")
    )

    monthly = {}
    for t in trades:
        mo = t["t"].strftime("%Y-%m")
        monthly.setdefault(mo, {"w": 0, "l": 0})
        monthly[mo]["w" if t["win"] else "l"] += 1

    max_l = cur = 0
    for t in trades:
        if not t["win"]:
            cur += 1
            max_l = max(max_l, cur)
        else:
            cur = 0
    exp_streak = math.log(n) / math.log(1 / (1 - wr)) if 0 < wr < 1 else 0

    w20 = []
    outcomes = [1 if t["win"] else 0 for t in trades]
    for i in range(0, max(1, n - 19), 10):
        win = outcomes[i : i + 20]
        if len(win) < 20:
            break
        wrr = sum(win) / 20
        w20.append({"i": i, "wr": wrr, "e_n": wrr * (R + 1) - 1})

    final = chosen["final"]
    deposit = chosen["deposit"]
    pnl = (final - deposit) if final is not None else None

    score = {
        "task": "EDX-P0-T01",
        "identity_ok": identity_ok,
        "expected_preset": "EDX-P0-T01_baseline_G0_AUDUSD-M5_MayAug.set",
        "expected_magic": "8230101",
        "observed_magic": chosen["magic"],
        "observed_sl_tp": f"{chosen['sl']}/{chosen['tp']}",
        "observed_bb": chosen["bb"],
        "window": f"{chosen['from']}->{chosen['to']}",
        "n": n,
        "WR": round(wr * 100, 2),
        "AW": round(aw, 3),
        "AL": round(al, 3),
        "R": round(R, 3),
        "RR": round(RR, 3),
        "RR_R": round(RR - R, 3),
        "BWR": round(bwr * 100, 2),
        "BM_pp": round(bm_pp, 2),
        "FMI": round(fmi, 3),
        "med_spread_pts": med_spread,
        "c_R": round(c_r, 3),
        "Leak_pp": round(leak_pp, 2),
        "EF_pp": round(ef_pp, 2),
        "M_wilson_pp": round(m_wilson_pp, 2),
        "M_normal_pp": round(m_norm_pp, 2),
        "E_N": round(e_n, 3),
        "PF": round(pf, 3),
        "final": final,
        "pnl": round(pnl, 2) if pnl is not None else None,
        "zone": zone,
        "tier": tier,
        "side": side,
        "al_claim": r_claim,
        "max_loss_streak": max_l,
        "expected_worst_streak": round(exp_streak, 1),
        "monthly": {
            mo: {
                "n": v["w"] + v["l"],
                "WR": round(100 * v["w"] / (v["w"] + v["l"]), 1),
                "E_N": round((v["w"] / (v["w"] + v["l"])) * (R + 1) - 1, 3),
            }
            for mo, v in sorted(monthly.items())
        },
        "W20": w20,
        "init": chosen["init"],
    }
    (OUT / "SCORECARD.json").write_text(json.dumps(score, indent=2), encoding="utf-8")
    print(json.dumps(score, indent=2))


if __name__ == "__main__":
    main()
