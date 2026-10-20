"""Score EDX-P1 session + DOW cells from latest AUDUSD Harvest G0 runs."""
from __future__ import annotations

import json
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
R = 1.0  # FIXED_RR confirmed
BWR = 0.5


def load(path: Path) -> str:
    raw = path.read_bytes()
    if raw[:2] == b"\xff\xfe":
        return raw.decode("utf-16-le")
    return raw.decode("utf-8", errors="replace")


def parse_trades(chunk: str) -> list[dict]:
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
            }
            continue
        m = re.search(
            r"(\d{4}\.\d{2}\.\d{2} \d{2}:\d{2}:\d{2})\s+(take profit|stop loss) triggered",
            line,
        )
        if m and open_rec:
            win = "take" in m.group(2)
            trades.append(
                {
                    **open_rec,
                    "win": win,
                    "hour": open_rec["t"].hour,
                    "dow": open_rec["t"].strftime("%a"),
                    "month": open_rec["t"].strftime("%Y-%m"),
                }
            )
            open_rec = None
    return trades


def cell_stats(trades: list[dict]) -> dict:
    n = len(trades)
    if n == 0:
        return {"n": 0}
    wr = sum(1 for t in trades if t["win"]) / n
    bm = wr - BWR
    e_n = wr * (R + 1) - 1
    return {
        "n": n,
        "WR": round(100 * wr, 1),
        "BM_pp": round(100 * bm, 1),
        "E_N": round(e_n, 3),
        "gate_n30": n >= 30,
    }


def session_bucket(hour: int) -> str:
    # Within champ filter 12-20 server; also label overlaps loosely
    if 12 <= hour < 14:
        return "12-14_LON_open"
    if 14 <= hour < 17:
        return "14-17_LON-NY_overlap"
    if 17 <= hour < 20:
        return "17-20_NY"
    if 0 <= hour < 7:
        return "Asia_hold_exit_only"
    if 7 <= hour < 12:
        return "LON_pre_filter"
    return "other"


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
    p1_magics = {"8230111", "8230112", "8230101", "8230151"}
    runs = []
    for i, s in enumerate(starts):
        end = starts[i + 1].start() if i + 1 < len(starts) else len(text)
        c = text[s.start() : end]
        mag = re.search(r"InpMagic=(\d+)", c)
        mval = mag.group(1) if mag else "?"
        finals = re.findall(r"final balance ([\d.]+)", c)
        print(
            f"[{i}] {s.group(1)}->{s.group(2)} mag={mval} "
            f"final={finals[-1] if finals else '?'}"
        )
        runs.append(
            {
                "i": i,
                "from": s.group(1),
                "to": s.group(2),
                "magic": mval,
                "chunk": c,
                "final": float(finals[-1]) if finals else None,
            }
        )

    # Prefer dedicated P1 magics; else P0/P05 May-Aug Harvest
    chosen = None
    for want in ("8230111", "8230112", "8230151", "8230101"):
        for r in reversed(runs):
            if r["magic"] == want and r["to"].startswith("2026.08"):
                chosen = r
                break
        if chosen:
            break
    if chosen is None:
        for r in reversed(runs):
            if r["magic"] in p1_magics:
                chosen = r
                break
    if chosen is None:
        raise SystemExit("no suitable run")

    print("scoring mag", chosen["magic"], chosen["from"], "->", chosen["to"])
    trades = parse_trades(chosen["chunk"])
    print("n_trades", len(trades))

    by_hour = defaultdict(list)
    by_sess = defaultdict(list)
    by_dow = defaultdict(list)
    for t in trades:
        by_hour[t["hour"]].append(t)
        by_sess[session_bucket(t["hour"])].append(t)
        by_dow[t["dow"]].append(t)

    hours = {f"{h:02d}": cell_stats(by_hour[h]) for h in sorted(by_hour)}
    sessions = {k: cell_stats(v) for k, v in sorted(by_sess.items())}
    dows = {}
    for d in ("Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"):
        dows[d] = cell_stats(by_dow.get(d, []))

    # Rank edge vs loss by E_N among cells with n>=5 (provisional; n>=30 gated)
    def rank(cells: dict) -> list:
        rows = [(k, v) for k, v in cells.items() if v.get("n", 0) >= 5]
        rows.sort(key=lambda x: x[1]["E_N"], reverse=True)
        return [{"cell": k, **v} for k, v in rows]

    # BM_worst among n>=30 else note provisional
    def bm_worst(cells: dict) -> dict:
        qual = {k: v for k, v in cells.items() if v.get("n", 0) >= 30}
        if not qual:
            # provisional worst among n>=8
            pool = {k: v for k, v in cells.items() if v.get("n", 0) >= 8}
            if not pool:
                return {"note": "no cells n>=8"}
            worst = min(pool.items(), key=lambda x: x[1]["BM_pp"])
            return {
                "cell": worst[0],
                **worst[1],
                "note": "provisional (no cell n>=30)",
            }
        worst = min(qual.items(), key=lambda x: x[1]["BM_pp"])
        return {"cell": worst[0], **worst[1], "note": "n>=30"}

    # concentration: share of total E_N from best cell (using n-weighted)
    def concentration(cells: dict) -> dict:
        pos = [(k, v) for k, v in cells.items() if v.get("n", 0) >= 5 and v["E_N"] > 0]
        if not pos:
            return {"best": None, "share": None}
        # approximate E_N contribution as n * E_N
        contrib = {k: v["n"] * v["E_N"] for k, v in pos}
        total = sum(contrib.values())
        best_k = max(contrib, key=contrib.get)
        return {
            "best": best_k,
            "share": round(contrib[best_k] / total, 3) if total else None,
            "flag": (contrib[best_k] / total > 0.7) if total else False,
        }

    out = {
        "source_magic": chosen["magic"],
        "window": f"{chosen['from']}->{chosen['to']}",
        "n": len(trades),
        "overall": cell_stats(trades),
        "by_hour": hours,
        "by_session": sessions,
        "by_dow": dows,
        "rank_session": rank(sessions),
        "rank_hour": rank(hours),
        "rank_dow": rank(dows),
        "BM_worst_session": bm_worst(sessions),
        "BM_worst_hour": bm_worst(hours),
        "BM_worst_dow": bm_worst(dows),
        "concentration_session": concentration(sessions),
        "p1_runs_present": [r["magic"] for r in runs if r["magic"] in ("8230111", "8230112")],
        "all_magics_tail": [r["magic"] for r in runs[-8:]],
    }
    (OUT / "SCORECARD.json").write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
