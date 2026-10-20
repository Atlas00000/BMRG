"""EDX-P8-T03: ATR×ER re-tag on champ trades; justify ATR gate or SKIP."""
from __future__ import annotations

import json
import math
import re
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

import MetaTrader5 as mt5
import numpy as np

LOG = Path(
    r"C:\Users\emili\AppData\Roaming\MetaQuotes\Terminal"
    r"\D0E8209F77C8CF37AD8BF550E51FF075\Tester\logs\20261007.log"
)
OUT = Path(__file__).resolve().parent
BWR = 0.5
R = 1.0


def load_log() -> str:
    raw = LOG.read_bytes()
    if raw[:2] == b"\xff\xfe":
        return raw.decode("utf-16-le")
    return raw.decode("utf-8", errors="replace")


def get_champ_trades(text: str) -> list[dict]:
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
        sh = re.search(r"InpStartHour=([0-9.]+)", c)
        tm = re.search(r"InpTradeMon=(true|false)", c)
        if not mag or mag.group(1) != "8230501":
            continue
        if (sh.group(1) if sh else "?") != "13" or (tm.group(1) if tm else "?") != "false":
            continue
        if not s.group(1).startswith("2026.05") or not s.group(2).startswith("2026.08"):
            continue
        chosen = c
    if chosen is None:
        raise SystemExit("champ 8230501 May→Aug not found")

    trades = []
    open_rec = None
    for line in chosen.splitlines():
        m = re.search(
            r"(\d{4}\.\d{2}\.\d{2} \d{2}:\d{2}:\d{2})\s+market (buy|sell) ",
            line,
        )
        if m and "OrderSend" not in line:
            open_rec = {
                "t": datetime.strptime(m.group(1), "%Y.%m.%d %H:%M:%S").replace(
                    tzinfo=timezone.utc
                ),
                "side": m.group(2),
            }
            continue
        m = re.search(r"(take profit|stop loss) triggered", line, re.I)
        if m and open_rec:
            trades.append({**open_rec, "win": "take" in m.group(1).lower()})
            open_rec = None
    return trades


def atr_wilder(high, low, close, period=14):
    n = len(close)
    tr = np.zeros(n)
    tr[0] = high[0] - low[0]
    for i in range(1, n):
        tr[i] = max(
            high[i] - low[i],
            abs(high[i] - close[i - 1]),
            abs(low[i] - close[i - 1]),
        )
    atr = np.full(n, np.nan)
    if n < period:
        return atr
    atr[period - 1] = np.mean(tr[:period])
    for i in range(period, n):
        atr[i] = (atr[i - 1] * (period - 1) + tr[i]) / period
    return atr


def efficiency_ratio(close, period=50):
    n = len(close)
    er = np.full(n, np.nan)
    for i in range(period, n):
        change = abs(close[i] - close[i - period])
        volatility = np.sum(np.abs(np.diff(close[i - period : i + 1])))
        er[i] = change / volatility if volatility > 0 else 0.0
    return er


def cell_stats(rows: list[dict]) -> dict:
    n = len(rows)
    if n == 0:
        return {"n": 0}
    wr = sum(1 for r in rows if r["win"]) / n
    return {
        "n": n,
        "WR": round(100 * wr, 1),
        "BM_pp": round(100 * (wr - BWR), 1),
        "E_N": round(wr * (R + 1) - 1, 3),
        "gate_n30": n >= 30,
    }


def main() -> None:
    trades = get_champ_trades(load_log())
    print("champ_trades", len(trades))

    if not mt5.initialize():
        raise SystemExit(f"MT5 init failed: {mt5.last_error()}")

    rates = mt5.copy_rates_range(
        "AUDUSD",
        mt5.TIMEFRAME_M5,
        datetime(2026, 4, 1, tzinfo=timezone.utc),
        datetime(2026, 9, 1, tzinfo=timezone.utc),
    )
    mt5.shutdown()
    if rates is None or len(rates) == 0:
        raise SystemExit("no rates")

    times = np.array([int(r[0]) for r in rates], dtype=np.int64)
    high = np.array([r[2] for r in rates], dtype=float)
    low = np.array([r[3] for r in rates], dtype=float)
    close = np.array([r[4] for r in rates], dtype=float)

    atr = atr_wilder(high, low, close, 14)
    er = efficiency_ratio(close, 50)
    atr_pct = np.full(len(atr), np.nan)
    lookback = 5000
    for i in range(len(atr)):
        if np.isnan(atr[i]):
            continue
        lo = max(0, i - lookback)
        hist = atr[lo:i]
        hist = hist[~np.isnan(hist)]
        if len(hist) < 100:
            continue
        atr_pct[i] = 100.0 * np.mean(hist <= atr[i])

    def atr_tercile(p):
        if p is None or math.isnan(p):
            return "unk"
        if p < 33.333:
            return "ATR_low"
        if p < 66.666:
            return "ATR_mid"
        return "ATR_high"

    def er_regime(v):
        if v is None or math.isnan(v):
            return "unk"
        return "trending" if v >= 0.3 else "ranging"

    tagged = []
    atr_pts_high = []
    for t in trades:
        ts = int(t["t"].timestamp())
        idx = np.searchsorted(times, ts, side="right") - 1
        if idx < 0:
            continue
        idx = max(0, idx - 1)
        p = atr_pct[idx]
        e = er[idx]
        vol = atr_tercile(p)
        cell = f"{vol}|{er_regime(e)}"
        atr_pts = None if np.isnan(atr[idx]) else float(atr[idx] / 0.00001)
        if vol == "ATR_high" and atr_pts is not None:
            atr_pts_high.append(atr_pts)
        tagged.append({**t, "cell": cell, "vol": vol, "atr_pts": atr_pts})

    by_cell: dict[str, list] = defaultdict(list)
    by_vol: dict[str, list] = defaultdict(list)
    for row in tagged:
        by_cell[row["cell"]].append(row)
        by_vol[row["vol"]].append(row)

    cells = {k: cell_stats(v) for k, v in sorted(by_cell.items())}
    vols = {k: cell_stats(v) for k, v in sorted(by_vol.items())}

    n30_neg = [
        {"cell": k, **v}
        for k, v in cells.items()
        if v.get("n", 0) >= 30 and v.get("BM_pp", 0) <= 0
    ]
    # FREQUENCY_STALL path: would need a Tester gate EF lift — not available without run
    justified = len(n30_neg) > 0

    out = {
        "task": "EDX-P8-T03",
        "n_tagged": len(tagged),
        "by_cell": cells,
        "by_vol": vols,
        "justify": {
            "excluded_BM_le0_n30": n30_neg,
            "hard_justify": justified,
            "note": "P1 baseline also lacked n>=30 BM<=0; champ n=47 thinner",
        },
        "atr_high_pts_sample": {
            "n": len(atr_pts_high),
            "p33": round(float(np.percentile(atr_pts_high, 33)), 1) if atr_pts_high else None,
            "min": round(min(atr_pts_high), 1) if atr_pts_high else None,
        },
        "verdict": "SKIP" if not justified else "RUN_ATR_GATE",
        "reason": (
            "no excluded cell with n>=30 and BM<=0 — ATR gate not justified; no Tester preset"
            if not justified
            else "hard justify cleared — create ATR gate preset"
        ),
    }
    (OUT / "SCORECARD.json").write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
