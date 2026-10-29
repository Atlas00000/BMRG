"""
Account daily-loss fuse stub (GRP-P2).

Heuristic (not calibrated to live ddl %):
  If on day t, ≥2 members lose AND equal-weight R_p < thresh_R,
  suppress the next calendar day in the panel (all member R → 0).
Models a shared halt that kills the following session after a multi-sleeve hit.
"""
from __future__ import annotations

from typing import Any

import pandas as pd

from src.diversify.score import max_drawdown, portfolio_series


DEFAULT_THRESH_R = -1.0
DEFAULT_MIN_LOSERS = 2


def apply_fuse(
    panel: pd.DataFrame,
    members: tuple[str, ...],
    *,
    thresh_R: float = DEFAULT_THRESH_R,
    min_losers: int = DEFAULT_MIN_LOSERS,
) -> tuple[pd.DataFrame, dict[str, Any]]:
    """
    Return a copy of panel[members] with next-day suppression after fuse trips.
    Other sleeves untouched (returned frame is members-only).
    """
    sub = panel.loc[:, list(members)].copy()
    rp = portfolio_series(panel, members)
    n_lose = (sub < 0).sum(axis=1)
    trigger = (n_lose >= min_losers) & (rp < thresh_R)
    trigger_idx = [i for i, t in enumerate(trigger.tolist()) if t]

    suppressed = 0
    dates = list(sub.index)
    for i in trigger_idx:
        j = i + 1
        if j >= len(dates):
            continue
        # only suppress if not already zero
        if float(sub.iloc[j].abs().sum()) > 1e-12:
            sub.iloc[j, :] = 0.0
            suppressed += 1

    meta = {
        "thresh_R": thresh_R,
        "min_losers": min_losers,
        "n_trigger_days": int(trigger.sum()),
        "n_days_suppressed": suppressed,
        "trigger_dates": [str(dates[i]) for i in trigger_idx[:20]],
    }
    return sub, meta


def score_with_fuse(
    panel: pd.DataFrame,
    members: tuple[str, ...],
    *,
    thresh_R: float = DEFAULT_THRESH_R,
) -> dict[str, Any]:
    fused, meta = apply_fuse(panel, members, thresh_R=thresh_R)
    # rebuild a mini panel for portfolio stats
    rp = fused.mean(axis=1)  # equal weight = mean when all present
    # more precisely equal weight of members:
    rp = fused.sum(axis=1) / len(members)
    base_rp = portfolio_series(panel, members)
    s = rp.copy()
    s.index = pd.to_datetime(s.index)
    monthly = s.resample("ME").sum()
    monthly = monthly[monthly.abs() > 1e-12]
    m_hit = float((monthly > 0).mean()) if len(monthly) else None

    b = base_rp.copy()
    b.index = pd.to_datetime(b.index)
    b_monthly = b.resample("ME").sum()
    b_monthly = b_monthly[b_monthly.abs() > 1e-12]
    b_hit = float((b_monthly > 0).mean()) if len(b_monthly) else None

    return {
        "fuse": meta,
        "sum_R_fused": round(float(rp.sum()), 4),
        "sum_R_base": round(float(base_rp.sum()), 4),
        "sum_R_delta": round(float(rp.sum() - base_rp.sum()), 4),
        "month_hit_fused": None if m_hit is None else round(m_hit, 4),
        "month_hit_base": None if b_hit is None else round(b_hit, 4),
        "maxDD_fused": round(max_drawdown(rp.cumsum()), 4),
        "maxDD_base": round(max_drawdown(base_rp.cumsum()), 4),
    }
