"""Segment a long trade stream into month / quarter / year / trailing metrics.

Each bucket is a full metrics pack for diversify / stress / cluster work —
not just hit/miss.
"""
from __future__ import annotations

import math
import statistics as st
from collections import defaultdict
from datetime import date, timedelta
from typing import Any, Iterable

from .live_runs import LiveRunCard, by_asset
from .tester_parse import ParsedTrade


def _period_key(d: date, freq: str) -> str:
    if freq == "M":
        return f"{d.year:04d}-{d.month:02d}"
    if freq == "Q":
        q = (d.month - 1) // 3 + 1
        return f"{d.year:04d}-Q{q}"
    if freq == "Y":
        return f"{d.year:04d}"
    raise ValueError(freq)


def _safe_mean(xs: list[float]) -> float | None:
    return round(st.mean(xs), 6) if xs else None


def _safe_median(xs: list[float]) -> float | None:
    return round(st.median(xs), 6) if xs else None


def _safe_stdev(xs: list[float]) -> float | None:
    if len(xs) < 2:
        return None
    return round(st.pstdev(xs), 6)


def _wilson_lower(wr: float, n: int, z: float = 1.96) -> float | None:
    if n <= 0:
        return None
    denom = 1 + z * z / n
    centre = wr + z * z / (2 * n)
    spread = z * math.sqrt(wr * (1 - wr) / n + z * z / (4 * n * n))
    return round((centre - spread) / denom, 4)


def _max_drawdown_R(pnls_chrono: list[float]) -> float:
    """Max peak-to-trough drawdown on cumulative designed R."""
    if not pnls_chrono:
        return 0.0
    cum = 0.0
    peak = 0.0
    max_dd = 0.0
    for r in pnls_chrono:
        cum += r
        peak = max(peak, cum)
        max_dd = min(max_dd, cum - peak)
    return round(max_dd, 4)


def _streaks(pnls_chrono: list[float]) -> dict[str, int]:
    max_loss = max_win = cur_loss = cur_win = 0
    for r in pnls_chrono:
        if r < 0:
            cur_loss += 1
            cur_win = 0
            max_loss = max(max_loss, cur_loss)
        elif r > 0:
            cur_win += 1
            cur_loss = 0
            max_win = max(max_win, cur_win)
        else:
            cur_loss = cur_win = 0
    return {"max_loss_streak": max_loss, "max_win_streak": max_win}


def _hold_hours(t: ParsedTrade) -> float:
    return (t.close_time - t.open_time).total_seconds() / 3600.0


def _ef_zone(ef_pp: float | None) -> str | None:
    if ef_pp is None:
        return None
    if ef_pp > 3.0:
        return "Strong"
    if ef_pp > 0:
        return "Fragile"
    return "Below"


def _score_bucket(trades: list[ParsedTrade], card: LiveRunCard | None) -> dict[str, Any]:
    """Detailed metrics for one window (full / month / quarter / year / trailing)."""
    n = len(trades)
    if n == 0:
        return {"n": 0}

    rows = sorted(trades, key=lambda x: x.close_time)
    pnls = [t.pnl_R_design for t in rows]
    wins = [t for t in rows if t.pnl_R_design > 0]
    losses = [t for t in rows if t.pnl_R_design < 0]
    scratches = [t for t in rows if t.pnl_R_design == 0]
    win_rs = [t.pnl_R_design for t in wins]
    loss_rs = [abs(t.pnl_R_design) for t in losses]

    wr = len(wins) / n
    e_n = sum(pnls) / n
    sum_r = sum(pnls)
    aw = st.mean(win_rs) if win_rs else 0.0
    al = st.mean(loss_rs) if loss_rs else 0.0
    # realised payoff ratio (avg win R / avg |loss| R); designed RR from card
    R_real = (aw / al) if al > 0 else None
    designed_rr = card.designed_rr if card else None

    bwr = (card.bwr / 100.0) if card else (1.0 / (1.0 + designed_rr) if designed_rr else 0.5)
    leak = (card.leak_pp / 100.0) if card else 0.0
    bm = wr - bwr
    ef = bm - leak
    ef_pp = ef * 100.0
    m_wilson = _wilson_lower(wr, n)

    streaks = _streaks(pnls)
    max_dd = _max_drawdown_R(pnls)

    # exit mix
    exits = defaultdict(int)
    for t in rows:
        exits[t.exit_reason.upper()] += 1

    # side mix
    buys = [t for t in rows if t.side.upper() == "BUY"]
    sells = [t for t in rows if t.side.upper() == "SELL"]
    buy_wr = (sum(1 for t in buys if t.pnl_R_design > 0) / len(buys)) if buys else None
    sell_wr = (sum(1 for t in sells if t.pnl_R_design > 0) / len(sells)) if sells else None
    buy_en = (sum(t.pnl_R_design for t in buys) / len(buys)) if buys else None
    sell_en = (sum(t.pnl_R_design for t in sells) / len(sells)) if sells else None

    # hold / spread
    holds = [_hold_hours(t) for t in rows]
    spreads = [float(t.spread_pts) for t in rows if t.spread_pts is not None]

    # daily aggregation inside window
    by_day: dict[date, float] = defaultdict(float)
    for t in rows:
        by_day[t.close_time.date()] += t.pnl_R_design
    day_rs = list(by_day.values())
    active_days = len(by_day)
    neg_days = sum(1 for r in day_rs if r < 0)
    pos_days = sum(1 for r in day_rs if r > 0)
    flat_days = sum(1 for r in day_rs if r == 0)
    # consecutive negative close-days
    day_chrono = [by_day[d] for d in sorted(by_day)]
    max_neg_days = 0
    cur_neg = 0
    for r in day_chrono:
        if r < 0:
            cur_neg += 1
            max_neg_days = max(max_neg_days, cur_neg)
        else:
            cur_neg = 0

    d0, d1 = min(by_day), max(by_day)
    calendar_days = (d1 - d0).days + 1
    trades_per_active_day = n / active_days if active_days else None
    trades_per_30d = (n / calendar_days * 30.0) if calendar_days > 0 else None

    # dow / hour concentration (close time)
    dow_counts: dict[str, int] = defaultdict(int)
    hour_counts: dict[int, int] = defaultdict(int)
    dow_names = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    for t in rows:
        dow_counts[dow_names[t.close_time.weekday()]] += 1
        hour_counts[t.close_time.hour] += 1

    # profit factor on designed R
    gross_win = sum(win_rs)
    gross_loss = sum(loss_rs)
    pf = (gross_win / gross_loss) if gross_loss > 0 else None

    return {
        # identity / span
        "n": n,
        "wins": len(wins),
        "losses": len(losses),
        "scratches": len(scratches),
        "date_min": d0.isoformat(),
        "date_max": d1.isoformat(),
        "calendar_days": calendar_days,
        "active_days": active_days,
        "positive_cycle": bool(sum_r > 0),
        # expectancy core
        "WR": round(wr, 4),
        "WR_pct": round(wr * 100, 2),
        "WR_wilson_low": m_wilson,
        "E_N": round(e_n, 4),
        "sum_R": round(sum_r, 4),
        "median_R": _safe_median(pnls),
        "std_R": _safe_stdev(pnls),
        "best_trade_R": round(max(pnls), 4),
        "worst_trade_R": round(min(pnls), 4),
        "avg_win_R": round(aw, 4) if win_rs else None,
        "avg_loss_R": round(al, 4) if loss_rs else None,
        "R_realised": None if R_real is None else round(R_real, 4),
        "designed_RR": designed_rr,
        "profit_factor_R": None if pf is None else round(pf, 4),
        "gross_win_R": round(gross_win, 4),
        "gross_loss_R": round(gross_loss, 4),
        # edge vs barrier
        "BWR": round(bwr * 100, 2),
        "BM_pp": round(bm * 100, 3),
        "Leak_pp": round(leak * 100, 3) if card else None,
        "EF_pp": round(ef_pp, 3) if card else None,
        "EF_zone": _ef_zone(ef_pp if card else None),
        "EF_gt_0": bool(ef_pp > 0) if card else None,
        "WR_wilson_gt_BWR": (
            bool(m_wilson > bwr) if m_wilson is not None else None
        ),
        # path / streaks
        "maxDD_R": max_dd,
        "max_loss_streak": streaks["max_loss_streak"],
        "max_win_streak": streaks["max_win_streak"],
        "max_neg_day_streak": max_neg_days,
        "pos_days": pos_days,
        "neg_days": neg_days,
        "flat_active_days": flat_days,
        "day_hit_rate": round(pos_days / active_days, 4) if active_days else None,
        "best_day_R": round(max(day_rs), 4) if day_rs else None,
        "worst_day_R": round(min(day_rs), 4) if day_rs else None,
        "mean_day_R": _safe_mean(day_rs),
        "std_day_R": _safe_stdev(day_rs),
        "CVaR_day_20": (
            round(st.mean(sorted(day_rs)[: max(1, int(math.ceil(0.2 * len(day_rs))))]), 4)
            if len(day_rs) >= 3
            else None
        ),
        # frequency
        "trades_per_active_day": (
            round(trades_per_active_day, 3) if trades_per_active_day is not None else None
        ),
        "trades_per_30d": round(trades_per_30d, 2) if trades_per_30d is not None else None,
        # exits / sides / friction
        "exit_TP": exits.get("TP", 0),
        "exit_SL": exits.get("SL", 0),
        "exit_MID": exits.get("MID", 0),
        "exit_TP_pct": round(100 * exits.get("TP", 0) / n, 2),
        "exit_SL_pct": round(100 * exits.get("SL", 0) / n, 2),
        "n_buy": len(buys),
        "n_sell": len(sells),
        "buy_WR": None if buy_wr is None else round(buy_wr, 4),
        "sell_WR": None if sell_wr is None else round(sell_wr, 4),
        "buy_E_N": None if buy_en is None else round(buy_en, 4),
        "sell_E_N": None if sell_en is None else round(sell_en, 4),
        "hold_h_mean": _safe_mean(holds),
        "hold_h_median": _safe_median(holds),
        "hold_h_p90": (
            round(sorted(holds)[int(0.9 * (len(holds) - 1))], 3) if holds else None
        ),
        "spread_pts_median": _safe_median(spreads),
        "spread_pts_p90": (
            round(sorted(spreads)[int(0.9 * (len(spreads) - 1))], 1) if spreads else None
        ),
        "dow_close_counts": dict(dow_counts),
        "hour_close_top": sorted(
            ((h, c) for h, c in hour_counts.items()), key=lambda x: -x[1]
        )[:5],
    }


def _period_rollup(scored: dict[str, dict[str, Any]]) -> dict[str, Any]:
    """Aggregate across month/quarter/year buckets for one sleeve."""
    hit = [b for b in scored.values() if b.get("n", 0) > 0]
    if not hit:
        return {
            "buckets": scored,
            "n_periods": 0,
            "hit_rate": None,
        }
    sum_rs = [b["sum_R"] for b in hit]
    e_ns = [b["E_N"] for b in hit]
    wrs = [b["WR"] for b in hit]
    efs = [b["EF_pp"] for b in hit if b.get("EF_pp") is not None]
    dds = [b["maxDD_R"] for b in hit]
    ns = [b["n"] for b in hit]
    loss_streaks = [b["max_loss_streak"] for b in hit]
    worst = min(hit, key=lambda b: b["sum_R"])
    best = max(hit, key=lambda b: b["sum_R"])
    # CVaR of period sum_R (worst 20%)
    k = max(1, int(math.ceil(0.2 * len(sum_rs))))
    cvar = st.mean(sorted(sum_rs)[:k])
    return {
        "buckets": scored,
        "n_periods": len(hit),
        "hit_rate": round(sum(1 for b in hit if b["positive_cycle"]) / len(hit), 4),
        "mean_E_N": round(st.mean(e_ns), 4),
        "median_E_N": round(st.median(e_ns), 4),
        "mean_WR": round(st.mean(wrs), 4),
        "mean_EF_pp": round(st.mean(efs), 3) if efs else None,
        "mean_sum_R": round(st.mean(sum_rs), 4),
        "sum_R_total": round(sum(sum_rs), 4),
        "std_sum_R": round(st.pstdev(sum_rs), 4) if len(sum_rs) > 1 else None,
        "CVaR_period_20": round(cvar, 4),
        "worst_period_id": None,  # filled by caller with period key
        "worst_period_sum_R": worst["sum_R"],
        "worst_period_E_N": worst["E_N"],
        "worst_period_n": worst["n"],
        "best_period_sum_R": best["sum_R"],
        "best_period_E_N": best["E_N"],
        "mean_maxDD_R": round(st.mean(dds), 4),
        "worst_maxDD_R": round(min(dds), 4),
        "mean_n": round(st.mean(ns), 2),
        "mean_max_loss_streak": round(st.mean(loss_streaks), 2),
        "pct_EF_gt_0": round(sum(1 for e in efs if e > 0) / len(efs), 4) if efs else None,
        "pct_below_frontier": (
            round(sum(1 for b in hit if b.get("EF_zone") == "Below") / len(hit), 4)
        ),
    }


def segment(
    trades: Iterable[ParsedTrade],
    *,
    freqs: tuple[str, ...] = ("M", "Q", "Y"),
) -> dict[str, Any]:
    """Per-asset full + detailed period buckets + trailing windows."""
    by_aid: dict[str, list[ParsedTrade]] = defaultdict(list)
    for t in trades:
        by_aid[t.asset_id].append(t)

    cards = by_asset()
    out: dict[str, Any] = {}
    for aid, rows in sorted(by_aid.items()):
        rows = sorted(rows, key=lambda x: x.close_time)
        card = cards.get(aid)
        sleeve: dict[str, Any] = {
            "asset_id": aid,
            "magic": rows[0].magic if rows else None,
            "symbol": rows[0].symbol if rows else None,
            "tf": rows[0].tf if rows else None,
            "n_trades": len(rows),
            "card": {
                "preset": card.preset if card else None,
                "leak_pp": card.leak_pp if card else None,
                "bwr": card.bwr if card else None,
                "designed_rr": card.designed_rr if card else None,
                "sl_pts": card.sl_pts if card else None,
                "tp_pts": card.tp_pts if card else None,
            },
            "full": _score_bucket(rows, card),
            "periods": {},
        }
        for freq in freqs:
            buckets: dict[str, list[ParsedTrade]] = defaultdict(list)
            for t in rows:
                buckets[_period_key(t.close_time.date(), freq)].append(t)
            scored = {k: _score_bucket(v, card) for k, v in sorted(buckets.items())}
            rollup = _period_rollup(scored)
            # attach worst/best period ids
            if scored:
                worst_id = min(scored.items(), key=lambda kv: kv[1].get("sum_R", 0))[0]
                best_id = max(scored.items(), key=lambda kv: kv[1].get("sum_R", 0))[0]
                rollup["worst_period_id"] = worst_id
                rollup["best_period_id"] = best_id
                rollup["worst_period"] = scored[worst_id]
                rollup["best_period"] = scored[best_id]
            sleeve["periods"][freq] = rollup

        if rows:
            last = rows[-1].close_time.date()
            trail_specs = (
                (30, "trailing_30d"),
                (60, "trailing_60d"),
                (90, "trailing_90d"),
                (180, "trailing_180d"),
                (365, "trailing_365d"),
            )
            for days, label in trail_specs:
                cut = last - timedelta(days=days)
                sub = [t for t in rows if t.close_time.date() >= cut]
                sleeve[label] = _score_bucket(sub, card)
        out[aid] = sleeve
    return out


def hit_matrix(
    rolling: dict[str, Any],
    freq: str = "M",
    *,
    value: str = "rich",
) -> dict[str, Any]:
    """Asset × period matrix.

    value='bool' → positive_cycle only
    value='rich' → {positive_cycle, sum_R, E_N, WR, EF_pp, n, maxDD_R, max_loss_streak}
    """
    periods: set[str] = set()
    for sleeve in rolling.values():
        periods.update(
            sleeve.get("periods", {}).get(freq, {}).get("buckets", {}).keys()
        )
    cols = sorted(periods)
    matrix: dict[str, Any] = {}
    for aid, sleeve in rolling.items():
        buckets = sleeve.get("periods", {}).get(freq, {}).get("buckets", {})
        row: dict[str, Any] = {}
        for p in cols:
            b = buckets.get(p)
            if not b or not b.get("n"):
                row[p] = None
            elif value == "bool":
                row[p] = bool(b.get("positive_cycle"))
            else:
                row[p] = {
                    "positive_cycle": bool(b.get("positive_cycle")),
                    "n": b.get("n"),
                    "sum_R": b.get("sum_R"),
                    "E_N": b.get("E_N"),
                    "WR": b.get("WR"),
                    "EF_pp": b.get("EF_pp"),
                    "EF_zone": b.get("EF_zone"),
                    "maxDD_R": b.get("maxDD_R"),
                    "max_loss_streak": b.get("max_loss_streak"),
                    "trades_per_30d": b.get("trades_per_30d"),
                    "worst_day_R": b.get("worst_day_R"),
                }
        matrix[aid] = row
    return {"freq": freq, "value": value, "periods": cols, "assets": matrix}


def flatten_period_rows(rolling: dict[str, Any], freq: str = "M") -> list[dict[str, Any]]:
    """One row per (asset, period) for CSV / notebooks."""
    rows: list[dict[str, Any]] = []
    skip = {"dow_close_counts", "hour_close_top"}
    for aid, sleeve in rolling.items():
        buckets = sleeve.get("periods", {}).get(freq, {}).get("buckets", {})
        for pid, b in buckets.items():
            if not b.get("n"):
                continue
            row = {
                "asset_id": aid,
                "magic": sleeve.get("magic"),
                "period": pid,
                "freq": freq,
            }
            for k, v in b.items():
                if k in skip:
                    continue
                if isinstance(v, (dict, list)):
                    continue
                row[k] = v
            rows.append(row)
    return rows
