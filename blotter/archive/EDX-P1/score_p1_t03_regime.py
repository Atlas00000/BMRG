"""EDX-P1-T03: ATR tercile x ER regime tags on AUDUSD P0/P1 trades."""
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


def get_p1_trades(text: str) -> list[dict]:
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
        if mag and mag.group(1) == "8230111":
            chosen = c
            break
    if chosen is None:
        raise SystemExit("8230111 not found")

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
    trades = get_p1_trades(load_log())
    print("trades", len(trades))

    if not mt5.initialize():
        raise SystemExit(f"MT5 init failed: {mt5.last_error()}")

    # Pull M5 from Apr 2026 (warmup) through Aug 2026
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

    # ATR percentile using expanding prior window (no lookahead): at each bar,
    # percentile of current ATR among prior 5000 bars with valid ATR
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
    for t in trades:
        ts = int(t["t"].timestamp())
        # find last closed bar at or before entry (shift-1 style: bar open time <= entry)
        idx = np.searchsorted(times, ts, side="right") - 1
        if idx < 0:
            continue
        # use prior bar for closed-bar signal alignment
        idx = max(0, idx - 1)
        p = atr_pct[idx]
        e = er[idx]
        cell = f"{atr_tercile(p)}|{er_regime(e)}"
        tagged.append(
            {
                **t,
                "atr": None if np.isnan(atr[idx]) else float(atr[idx]),
                "atr_pct": None if np.isnan(p) else float(p),
                "er": None if np.isnan(e) else float(e),
                "vol": atr_tercile(p),
                "trend": er_regime(e),
                "cell": cell,
            }
        )

    by_cell = defaultdict(list)
    by_vol = defaultdict(list)
    by_trend = defaultdict(list)
    for row in tagged:
        by_cell[row["cell"]].append(row)
        by_vol[row["vol"]].append(row)
        by_trend[row["trend"]].append(row)

    cells = {k: cell_stats(v) for k, v in sorted(by_cell.items())}
    vols = {k: cell_stats(v) for k, v in sorted(by_vol.items())}
    trends = {k: cell_stats(v) for k, v in sorted(by_trend.items())}

    # BM_worst among n>=30; else provisional n>=8
    def bm_worst(d: dict) -> dict:
        qual = {k: v for k, v in d.items() if v.get("n", 0) >= 30}
        note = "n>=30"
        if not qual:
            qual = {k: v for k, v in d.items() if v.get("n", 0) >= 8}
            note = "provisional n>=8 (no cell n>=30)"
        if not qual:
            return {"note": "insufficient cells"}
        k, v = min(qual.items(), key=lambda x: x[1]["BM_pp"])
        return {"cell": k, **v, "note": note}

    # concentration of positive E_N mass
    pos = {k: v for k, v in cells.items() if v.get("n", 0) >= 5 and v.get("E_N", 0) > 0}
    contrib = {k: v["n"] * v["E_N"] for k, v in pos.items()}
    total = sum(contrib.values()) or 1.0
    best = max(contrib, key=contrib.get) if contrib else None
    share = contrib[best] / total if best else None

    # E_N share of total absolute positive expectancy mass
    out = {
        "task": "EDX-P1-T03",
        "n_tagged": len(tagged),
        "rates_bars": len(rates),
        "by_cell": cells,
        "by_vol": vols,
        "by_trend": trends,
        "BM_worst_cell": bm_worst(cells),
        "BM_worst_vol": bm_worst(vols),
        "BM_worst_trend": bm_worst(trends),
        "concentration": {
            "best_cell": best,
            "share": round(share, 3) if share is not None else None,
            "REGIME_CONCENTRATED": bool(share and share > 0.7),
        },
        "rank_cells": sorted(
            [{"cell": k, **v} for k, v in cells.items() if v.get("n", 0) >= 5],
            key=lambda x: x["E_N"],
            reverse=True,
        ),
        "method": {
            "ATR": "Wilder 14; percentile vs prior 5000 bars (no lookahead)",
            "ER": "50-bar efficiency ratio; trending if ER>=0.3",
            "entry_bar": "closed bar prior to entry (shift-1)",
            "source": "MT5 copy_rates_range AUDUSD M5 + log mag 8230111",
        },
    }
    (OUT / "P1-T03_SCORECARD.json").write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
