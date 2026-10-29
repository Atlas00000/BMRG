"""Equal-risk subset enumeration + cycle / CVaR / fuse scorecard."""
from __future__ import annotations

import itertools
from typing import Any

import numpy as np
import pandas as pd


def portfolio_series(panel: pd.DataFrame, members: tuple[str, ...]) -> pd.Series:
    w = 1.0 / len(members)
    return (panel.loc[:, list(members)] * w).sum(axis=1)


def _period_sums(r: pd.Series, freq: str) -> pd.Series:
    s = r.copy()
    s.index = pd.to_datetime(s.index)
    return s.resample(freq).sum()


def max_drawdown(cum: pd.Series) -> float:
    peak = cum.cummax()
    dd = cum - peak
    return float(dd.min()) if len(dd) else 0.0


def cvar(returns: pd.Series, alpha: float = 0.2) -> float | None:
    """Mean of worst alpha fraction (α=0.2 → worst 20%)."""
    x = returns.dropna()
    if len(x) < 3:
        return None
    k = max(1, int(np.ceil(alpha * len(x))))
    worst = x.nsmallest(k)
    return float(worst.mean())


def fuse_days(panel: pd.DataFrame, members: tuple[str, ...], thresh: float = -1.0) -> int:
    """Days with ≥2 sleeve losses and portfolio R < thresh (equal-risk)."""
    sub = panel.loc[:, list(members)]
    rp = portfolio_series(panel, members)
    n_lose = (sub < 0).sum(axis=1)
    return int(((n_lose >= 2) & (rp < thresh)).sum())


def score_cluster(panel: pd.DataFrame, members: tuple[str, ...]) -> dict[str, Any]:
    rp = portfolio_series(panel, members)
    monthly = _period_sums(rp, "ME")
    quarterly = _period_sums(rp, "QE")
    # drop empty trailing periods with all zeros from sparse start
    monthly = monthly[monthly.abs() > 1e-12]
    quarterly = quarterly[quarterly.abs() > 1e-12]
    cum = rp.cumsum()
    m_hit = float((monthly > 0).mean()) if len(monthly) else None
    q_hit = float((quarterly > 0).mean()) if len(quarterly) else None
    return {
        "members": list(members),
        "k": len(members),
        "n_days": int(len(rp)),
        "sum_R": round(float(rp.sum()), 4),
        "mean_daily_R": round(float(rp.mean()), 6),
        "month_hit": None if m_hit is None else round(m_hit, 4),
        "n_months": int(len(monthly)),
        "quarter_hit": None if q_hit is None else round(q_hit, 4),
        "n_quarters": int(len(quarterly)),
        "CVaR_m20": None if cvar(monthly) is None else round(cvar(monthly), 4),  # type: ignore
        "worst_month": round(float(monthly.min()), 4) if len(monthly) else None,
        "best_month": round(float(monthly.max()), 4) if len(monthly) else None,
        "maxDD": round(max_drawdown(cum), 4),
        "fuse_days": fuse_days(panel, members),
        "active_days": int((rp != 0).sum()),
    }


def enumerate_clusters(
    panel: pd.DataFrame,
    *,
    ks: tuple[int, ...] = (1, 2, 3),
) -> list[dict[str, Any]]:
    assets = list(panel.columns)
    scored: list[dict[str, Any]] = []
    for k in ks:
        for combo in itertools.combinations(assets, k):
            scored.append(score_cluster(panel, combo))
    return scored


def _contains_banned(
    members: list[str],
    banned_pairs: set[frozenset[str]],
) -> bool:
    m = set(members)
    return any(pair <= m for pair in banned_pairs)


def rank_clusters(
    scored: list[dict[str, Any]],
    *,
    min_months: int = 4,
    prefer_k: tuple[int, ...] = (2, 3),
    banned_pairs: set[frozenset[str]] | None = None,
) -> list[dict[str, Any]]:
    """Rank by month_hit then sum_R; demote clusters containing banned twin pairs."""
    banned_pairs = banned_pairs or set()
    eligible = [
        s
        for s in scored
        if s["k"] in prefer_k
        and s["n_months"] >= min_months
        and s["month_hit"] is not None
    ]
    for s in eligible:
        s["contains_banned_pair"] = _contains_banned(s["members"], banned_pairs)

    def key(s: dict[str, Any]) -> tuple:
        return (
            0 if s.get("contains_banned_pair") else 1,  # clean first
            s["month_hit"] or 0.0,
            s["quarter_hit"] or 0.0,
            s["sum_R"],
            -(s["fuse_days"] or 0),
            -(abs(s["CVaR_m20"] or 0)),
        )

    return sorted(eligible, key=key, reverse=True)


def baseline_eur(panel: pd.DataFrame) -> dict[str, Any] | None:
    if "EURUSD" not in panel.columns:
        return None
    return score_cluster(panel, ("EURUSD",))
