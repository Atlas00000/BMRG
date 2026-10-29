"""Block bootstrap of period returns → hit-rate bands (GRP-P2)."""
from __future__ import annotations

from typing import Any

import numpy as np
import pandas as pd

from src.diversify.score import portfolio_series


def period_returns(panel: pd.DataFrame, members: tuple[str, ...], freq: str) -> pd.Series:
    rp = portfolio_series(panel, members)
    s = rp.copy()
    s.index = pd.to_datetime(s.index)
    out = s.resample(freq).sum()
    return out[out.abs() > 1e-12]


def bootstrap_hit(
    periods: pd.Series,
    *,
    n_boot: int = 1000,
    seed: int = 42,
) -> dict[str, Any]:
    """
    Resample period returns with replacement (same length), compute hit-rate
    each draw. Returns mean / p10 / p50 / p90 of hit-rate and of sum_R.
    """
    x = periods.dropna().to_numpy(dtype=float)
    n = len(x)
    if n < 2:
        hit = float((x > 0).mean()) if n else None
        return {
            "n_periods": n,
            "obs_hit": hit,
            "obs_sum_R": round(float(x.sum()), 4) if n else None,
            "n_boot": 0,
            "hit_mean": hit,
            "hit_p10": hit,
            "hit_p50": hit,
            "hit_p90": hit,
            "sum_mean": round(float(x.sum()), 4) if n else None,
            "sum_p10": round(float(x.sum()), 4) if n else None,
        }
    rng = np.random.default_rng(seed)
    hits = np.empty(n_boot, dtype=float)
    sums = np.empty(n_boot, dtype=float)
    for i in range(n_boot):
        draw = rng.choice(x, size=n, replace=True)
        hits[i] = float((draw > 0).mean())
        sums[i] = float(draw.sum())
    obs_hit = float((x > 0).mean())
    return {
        "n_periods": n,
        "obs_hit": round(obs_hit, 4),
        "obs_sum_R": round(float(x.sum()), 4),
        "n_boot": n_boot,
        "hit_mean": round(float(hits.mean()), 4),
        "hit_p10": round(float(np.quantile(hits, 0.10)), 4),
        "hit_p50": round(float(np.quantile(hits, 0.50)), 4),
        "hit_p90": round(float(np.quantile(hits, 0.90)), 4),
        "sum_mean": round(float(sums.mean()), 4),
        "sum_p10": round(float(np.quantile(sums, 0.10)), 4),
        "sum_p50": round(float(np.quantile(sums, 0.50)), 4),
        "sum_p90": round(float(np.quantile(sums, 0.90)), 4),
    }


def bootstrap_group(
    panel: pd.DataFrame,
    members: tuple[str, ...],
    *,
    n_boot: int = 1000,
    seed: int = 42,
) -> dict[str, Any]:
    monthly = period_returns(panel, members, "ME")
    weekly = period_returns(panel, members, "W-FRI")
    return {
        "month": bootstrap_hit(monthly, n_boot=n_boot, seed=seed),
        "week": bootstrap_hit(weekly, n_boot=n_boot, seed=seed + 1),
    }
