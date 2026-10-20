"""Score JPN225 M5 P0 growth (magic 26101906) from Tester log."""
from __future__ import annotations

import json
import re
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

LOG = Path(
    r"C:\Users\emili\AppData\Roaming\MetaQuotes\Terminal"
    r"\D0E8209F77C8CF37AD8BF550E51FF075\Tester\logs\20261020.log"
)
OUT = Path(__file__).resolve().parent

R = 2.00
BWR = 1.0 / (1.0 + R)  # 0.333...
LEAK = 0.033  # prior stub from preset
DEP = 500.0
MAGIC = "26101906"
SL = 25000.0
TP = 50000.0

# Rough ccy proxy at lot 0.1 (same style as M15 JP reviews)
WIN_CCY = 3.333  # ~TP path
LOSS_CCY = -1.667

START = re.compile(
    r"JPN225,M5: testing of Experts\\BMRG\\BMRG\.ex5 "
    r"from (\S+) 00:00 to (\S+) 00:00 started with inputs:"
)

OURO = {
    "2026-01": "?",
    "2026-02": "?",
    "2026-03": "?",
    "2026-04": "?",
    "2026-05": "FRAGILE",
    "2026-06": "FRAGILE",
    "2026-07": "MISMATCH",
    "2026-08": "MATCH",
    "2026-09": "MATCH",
    "2026-10": "MISMATCH",
}


def load() -> str:
    raw = LOG.read_bytes()
    if not raw:
        raise SystemExit("log empty")
    if raw[:2] == b"\xff\xfe":
        return raw.decode("utf-16-le")
    return raw.decode("utf-8", errors="replace")


def extract_trades(chunk: str) -> list[dict]:
    trades = []
    pending = None
    for ln in chunk.splitlines():
        mo = re.search(
            r"(\d{4}\.\d{2}\.\d{2} \d{2}:\d{2}:\d{2}).*\[BMRG\]\[TRADE\] OPEN "
            r"(BUY|SELL).*spread=(\d+)",
            ln,
        )
        if mo:
            pending = {
                "open_time": mo.group(1),
                "side": mo.group(2),
                "spread": int(mo.group(3)),
                "month": mo.group(1)[:7].replace(".", "-"),
            }
            continue
        if not pending:
            continue
        if "take profit triggered" in ln and "JPN225" in ln:
            pending["win"] = 1
            pending["exit"] = "TP"
            trades.append(pending)
            pending = None
            continue
        if "stop loss triggered" in ln and "JPN225" in ln:
            pending["win"] = 0
            pending["exit"] = "SL"
            trades.append(pending)
            pending = None
    return trades


def book(trades: list[dict], label: str) -> dict:
    n = len(trades)
    fb_m = None
    # filled by caller
    if n == 0:
        return {"label": label, "n": 0}
    wins = [t["win"] for t in trades]
    wr = sum(wins) / n
    equity = DEP
    peak = DEP
    maxdd = 0.0
    for w in wins:
        equity += WIN_CCY if w else LOSS_CCY
        peak = max(peak, equity)
        maxdd = max(maxdd, (peak - equity) / peak * 100.0)
    return {
        "label": label,
        "n": n,
        "wins": sum(wins),
        "losses": n - sum(wins),
        "WR": round(wr * 100, 2),
        "R": R,
        "BWR": round(BWR * 100, 2),
        "BM_pp": round((wr - BWR) * 100, 3),
        "Leak_prior_pp": LEAK * 100,
        "EF_prior_pp": round((wr - BWR - LEAK) * 100, 3),
        "E_N": round(wr * (R + 1) - 1, 4),
        "tip_EF_cleared": bool(wr - BWR - LEAK > 0),
        "MaxDD_proxy_pct": round(maxdd, 2),
        "buy_n": sum(1 for t in trades if t["side"] == "BUY"),
        "sell_n": sum(1 for t in trades if t["side"] == "SELL"),
        "spread_med": sorted(t["spread"] for t in trades)[n // 2],
    }


def monthly(trades: list[dict]) -> list[dict]:
    by = defaultdict(list)
    for t in trades:
        by[t["month"]].append(t)
    rows = []
    for m in sorted(by):
        b = book(by[m], m)
        b["ouroboros"] = OURO.get(m, "?")
        rows.append(b)
    return rows


def main() -> None:
    text = load()
    runs = []
    for m in START.finditer(text):
        end = text.find("final balance", m.start())
        chunk = text[m.start() : end + 1200 if end > 0 else m.start() + 5_000_000]
        if f"InpMagic={MAGIC}" not in chunk[:15000]:
            continue
        trades = extract_trades(chunk)
        fb = re.search(r"final balance ([\d.\-]+)", chunk)
        label = f"{m.group(1)}->{m.group(2)}"
        row = book(trades, label)
        row["final"] = float(fb.group(1)) if fb else None
        row["delta"] = round(row["final"] - DEP, 2) if row["final"] is not None else None
        row["window_from"] = m.group(1)
        row["window_to"] = m.group(2)
        row["monthly"] = monthly(trades)
        # geometry check from OPEN lines
        geos = re.findall(
            r"\[BMRG\]\[TRADE\] OPEN (BUY|SELL).*price=([0-9.]+) sl=([0-9.]+) tp=([0-9.]+)",
            chunk,
        )
        tp_lt_sl = 0
        rs = []
        for side, px, sl, tp in geos:
            px, sl, tp = float(px), float(sl), float(tp)
            if side == "BUY":
                slp, tpp = abs(px - sl) / 0.01, abs(tp - px) / 0.01
            else:
                slp, tpp = abs(sl - px) / 0.01, abs(px - tp) / 0.01
            if tpp + 1e-6 < slp:
                tp_lt_sl += 1
            if slp > 0:
                rs.append(tpp / slp)
        row["geometry"] = {
            "design_SL": SL,
            "design_TP": TP,
            "design_RR": R,
            "opens_parsed": len(geos),
            "tp_lt_sl": tp_lt_sl,
            "realised_R_med": round(sorted(rs)[len(rs) // 2], 3) if rs else None,
        }
        # MATCH / OFFHOME slices on tip-ish months if present
        match = [t for t in trades if OURO.get(t["month"]) == "MATCH"]
        off = [
            t
            for t in trades
            if OURO.get(t["month"]) in ("FRAGILE", "MISMATCH")
        ]
        row["slice_MATCH"] = book(match, "MATCH") if match else None
        row["slice_OFFHOME"] = book(off, "OFFHOME") if off else None
        runs.append(row)

    packet = {
        "task": "JP225-M5-P0-REVIEW",
        "dated": datetime.now(timezone.utc).isoformat(),
        "magic": int(MAGIC),
        "preset": "BMRG-M5-JP225-6M-P0_growth_chart.set",
        "scope": "expansion_candidate_not_live_replace",
        "AOS": "OFF",
        "tf": "M5",
        "symbol": "JPN225",
        "runs": runs,
    }
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "SCORECARD.json").write_text(json.dumps(packet, indent=2), encoding="utf-8")
    print(json.dumps(packet, indent=2))


if __name__ == "__main__":
    main()
