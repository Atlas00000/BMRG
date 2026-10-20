"""List recent AUDUSD BMRG tester runs; score AIOS / champ magics."""
from __future__ import annotations

import json
import math
import re
import statistics as st
from collections import defaultdict
from datetime import datetime
from pathlib import Path

LOG_DIR = Path(
    r"C:\Users\emili\AppData\Roaming\MetaQuotes\Terminal"
    r"\D0E8209F77C8CF37AD8BF550E51FF075\Tester\logs"
)
OUT = Path(__file__).resolve().parent
POINT = 0.00001
SL_PTS = 300.0
DEPOSIT = 400.0


def load(path: Path) -> str:
    raw = path.read_bytes()
    if raw[:2] == b"\xff\xfe":
        return raw.decode("utf-16-le")
    return raw.decode("utf-8", errors="replace")


def latest_log() -> Path:
    logs = sorted(LOG_DIR.glob("*.log"), key=lambda x: x.stat().st_mtime, reverse=True)
    if not logs:
        raise SystemExit("no logs")
    return logs[0]


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
                "vol": float(m.group(3)),
                "sl": float(m.group(4)),
                "tp": float(m.group(5)),
                "spread_pts": (ask - bid) / POINT,
            }
            continue
        m = re.search(r"deal #\d+ (buy|sell) ([\d.]+) AUDUSD at ([\d.]+)", line)
        if m and open_rec and "entry" not in open_rec and m.group(1) == open_rec["side"]:
            open_rec["entry"] = float(m.group(3))
            continue
        # deal profit if present
        m_pnl = re.search(
            r"deal #\d+ (buy|sell) .* AUDUSD .* profit: ([-+\d.]+)",
            line,
        )
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
                    "t": open_rec["t"],
                    "ym": open_rec["t"].strftime("%Y-%m"),
                    "yq": f"{open_rec['t'].year}-Q{(open_rec['t'].month - 1) // 3 + 1}",
                    "vol": open_rec["vol"],
                }
            )
            open_rec = None
    return trades


def score(trades: list[dict], final: float | None) -> dict:
    n = len(trades)
    if n == 0:
        return {"n": 0}
    wr = sum(1 for t in trades if t["win"]) / n
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
    c_r_mean = st.mean([t["c_r"] for t in trades])
    leak_pp = 100 * c_r_mean / (R + 1)
    ef_pp = bm_pp - leak_pp
    z = 1.96
    m_pp = (
        100
        * (z / (1 + z * z / n))
        * math.sqrt(wr * (1 - wr) / n + z * z / (4 * n * n))
    )
    zone = "Negative" if ef_pp <= 0 else ("Fragile" if ef_pp <= m_pp else "Robust")
    pnl = (final - DEPOSIT) if final is not None else None

    # Rough $ per 1R from RR1 geometry: with risk% 0.5 on ~400, ~$2/R if sized that way;
    # better: from pnl / sum(pnl_r) if pnl known
    sum_r = sum(t["pnl_r"] for t in trades)
    usd_per_r = (pnl / sum_r) if pnl is not None and abs(sum_r) > 1e-9 else None

    by_m: dict[str, list] = defaultdict(list)
    by_q: dict[str, list] = defaultdict(list)
    for t in trades:
        by_m[t["ym"]].append(t)
        by_q[t["yq"]].append(t)

    def pack(groups: dict[str, list]) -> dict:
        out = {}
        for k, ts in sorted(groups.items()):
            nm = len(ts)
            wins = sum(1 for x in ts if x["win"])
            losses = nm - wins
            sum_r_g = sum(x["pnl_r"] for x in ts)
            e_n_g = sum_r_g / nm
            wr_g = wins / nm
            usd = (usd_per_r * sum_r_g) if usd_per_r is not None else None
            # loss exposure if month/quarter is negative: sum of losing trade R (and $)
            loss_r = sum(x["pnl_r"] for x in ts if not x["win"])  # negative
            win_r = sum(x["pnl_r"] for x in ts if x["win"])
            out[k] = {
                "n": nm,
                "wins": wins,
                "losses": losses,
                "WR": round(100 * wr_g, 1),
                "E_N": round(e_n_g, 3),
                "sum_R": round(sum_r_g, 2),
                "win_R": round(win_r, 2),
                "loss_R": round(loss_r, 2),
                "pnl_usd_est": round(usd, 2) if usd is not None else None,
                "condition": "WIN_MONTH" if sum_r_g > 0 else ("FLAT" if abs(sum_r_g) < 1e-9 else "LOSS_MONTH"),
            }
        return out

    months = pack(by_m)
    quarters = pack(by_q)
    # rename conditions for quarters
    for k, v in quarters.items():
        if v["condition"] == "WIN_MONTH":
            v["condition"] = "WIN_QUARTER"
        elif v["condition"] == "LOSS_MONTH":
            v["condition"] = "LOSS_QUARTER"

    neg_months = {k: v for k, v in months.items() if v["sum_R"] < 0}
    neg_quarters = {k: v for k, v in quarters.items() if v["sum_R"] < 0}
    worst_m = min(months.values(), key=lambda x: x["sum_R"]) if months else None
    worst_q = min(quarters.values(), key=lambda x: x["sum_R"]) if quarters else None

    return {
        "n": n,
        "WR": round(100 * wr, 2),
        "R": round(R, 3),
        "BWR": 50.0,
        "BM_pp": round(bm_pp, 2),
        "Leak_pp": round(leak_pp, 2),
        "EF_pp": round(ef_pp, 2),
        "M_pp": round(m_pp, 2),
        "E_N": round(e_n, 3),
        "pnl": round(pnl, 2) if pnl is not None else None,
        "usd_per_R_est": round(usd_per_r, 2) if usd_per_r is not None else None,
        "zone": zone,
        "months": months,
        "quarters": quarters,
        "neg_months": neg_months,
        "neg_quarters": neg_quarters,
        "worst_month": worst_m,
        "worst_quarter": worst_q,
        "max_loss_streak_R": None,  # filled below
    }


def max_loss_streak(trades: list[dict]) -> dict:
    streak = 0
    best = 0
    sum_r = 0.0
    best_sum = 0.0
    for t in trades:
        if not t["win"]:
            streak += 1
            sum_r += t["pnl_r"]
            if streak > best:
                best = streak
                best_sum = sum_r
        else:
            streak = 0
            sum_r = 0.0
    return {"max_streak": best, "sum_R": round(best_sum, 2)}


def main() -> None:
    log = latest_log()
    text = load(log)
    print("log", log.name, "bytes", log.stat().st_size)
    starts = list(
        re.finditer(
            r"AUDUSD,M5: testing of Experts\\BMRG\\BMRG\.ex5 from (\S+) 00:00 to (\S+) 00:00 started with inputs:",
            text,
        )
    )
    print("starts", len(starts))
    runs = []
    for i, s in enumerate(starts):
        end = starts[i + 1].start() if i + 1 < len(starts) else len(text)
        c = text[s.start() : end]
        mag = re.search(r"InpMagic=(\d+)", c)
        if not mag:
            continue
        mval = mag.group(1)
        aos = re.search(r"InpAOS_Enable=(true|false)", c)
        mode = re.search(r"InpAiOsMode=(\d+)", c)
        sh = re.search(r"InpStartHour=([0-9.]+)", c)
        mon = re.search(r"InpTradeMon=(true|false)", c)
        finals = re.findall(r"final balance ([\d.]+)", c)
        # focus last 20 and any AIOS/champ magics
        if i < len(starts) - 20 and mval not in ("8230921", "8230901", "8230501", "8230502", "8230601", "8230801", "8230802", "8230803"):
            continue
        print(
            f"[{i}] {s.group(1)}->{s.group(2)} mag={mval} "
            f"AOS={aos.group(1) if aos else '?'} mode={mode.group(1) if mode else '?'} "
            f"Start={sh.group(1) if sh else '?'} Mon={mon.group(1) if mon else '?'} "
            f"final={finals[-1] if finals else '?'}"
        )
        if mval in ("8230921", "8230901") or (
            mval in ("8230501", "8230502", "8230601")
            and (sh.group(1) if sh else "") == "13"
            and (mon.group(1) if mon else "") == "false"
        ):
            runs.append(
                {
                    "i": i,
                    "magic": mval,
                    "from": s.group(1),
                    "to": s.group(2),
                    "aos": aos.group(1) if aos else "?",
                    "mode": mode.group(1) if mode else "?",
                    "start": sh.group(1) if sh else "?",
                    "mon": mon.group(1) if mon else "?",
                    "final": float(finals[-1]) if finals else None,
                    "chunk": c,
                }
            )

    # Prefer latest 8230921 runs; else latest champ-stack
    scored = []
    for run in runs:
        trades = parse_trades(run["chunk"])
        hv = score(trades, run["final"])
        hv["max_loss_streak"] = max_loss_streak(trades)
        scored.append(
            {
                "run_i": run["i"],
                "magic": run["magic"],
                "window": f"{run['from']}->{run['to']}",
                "AOS": run["aos"],
                "AiOsMode": run["mode"],
                "StartHour": run["start"],
                "TradeMon": run["mon"],
                "final": run["final"],
                **hv,
            }
        )

    # Keep latest per magic+window
    best: dict[str, dict] = {}
    for s in scored:
        key = f"{s['magic']}|{s['window']}"
        if key not in best or s["run_i"] > best[key]["run_i"]:
            best[key] = s
    out = {"log": log.name, "runs": list(best.values())}
    (OUT / "REVIEW.json").write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
