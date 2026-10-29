"""Adverse / stress overlays for tip-panel group scoring (GRP-P1)."""
from __future__ import annotations

from typing import Any

import pandas as pd

from src.diversify.score import portfolio_series
from src.diversify.stress import STRESS_MONTHS, day_stress_flags, stress_day_mask


# Tip-observed soft months (sleeve review) — always tagged adverse for holdout preview
TIP_ADVERSE_MONTHS: frozenset[int] = frozenset({9, 10})  # Sep, Oct 2026 tip fade


def month_of(d) -> int:
    return d.month if hasattr(d, "month") else pd.Timestamp(d).month


def tip_adverse_day_mask(panel: pd.DataFrame) -> pd.Series:
    """Days in tip soft months Sep/Oct (calendar), regardless of activity."""
    idx = list(panel.index)
    return pd.Series(
        [month_of(d) in TIP_ADVERSE_MONTHS for d in idx],
        index=idx,
        name="tip_adverse",
    )


def book_neg_month_mask(panel: pd.DataFrame, members: tuple[str, ...] | None = None) -> pd.Series:
    """
    Days belonging to calendar months where equal-weight book (all sleeves or
    members) has sum_R < 0.
    """
    cols = list(members) if members else list(panel.columns)
    rp = portfolio_series(panel, tuple(cols))
    s = rp.copy()
    s.index = pd.to_datetime(s.index)
    monthly = s.resample("ME").sum()
    bad_months = {pd.Timestamp(i).to_period("M") for i, v in monthly.items() if v < 0}
    flags = []
    for d in panel.index:
        p = pd.Timestamp(d).to_period("M")
        flags.append(p in bad_months)
    return pd.Series(flags, index=panel.index, name="book_neg_month")


def stress_snapshot(panel: pd.DataFrame) -> dict[str, Any]:
    flags = day_stress_flags(panel)
    tip_adv = tip_adverse_day_mask(panel)
    curated = stress_day_mask(panel)
    return {
        "n_days": int(len(panel)),
        "n_tip_adverse_days": int(tip_adv.sum()),
        "n_curated_stress_days": int(curated.sum()),
        "tip_adverse_months": sorted(TIP_ADVERSE_MONTHS),
        "curated_stress_months": [
            {"asset_id": s.asset_id, "month": s.month, "label": s.label}
            for s in STRESS_MONTHS
            if s.asset_id in panel.columns
        ],
        "n_days_any_sleeve_stress": int(flags["book_stress"].sum()),
    }


def conditioned_period_hit(
    panel: pd.DataFrame,
    members: tuple[str, ...],
    day_mask: pd.Series,
    *,
    freq: str = "ME",
) -> dict[str, Any]:
    """
    Hit-rate of period sums using only days inside day_mask.
    Sparse conditioned panels may have fewer periods.
    """
    rp = portfolio_series(panel, members)
    m = day_mask.reindex(panel.index).fillna(False).astype(bool)
    sub = rp.loc[m]
    if len(sub) == 0 or float(sub.abs().sum()) < 1e-12:
        return {
            "n_days": 0,
            "sum_R": 0.0,
            "n_periods": 0,
            "hit_rate": None,
            "E_period": None,
            "worst_period": None,
        }
    s = sub.copy()
    s.index = pd.to_datetime(s.index)
    periods = s.resample(freq).sum()
    periods = periods[periods.abs() > 1e-12]
    if len(periods) == 0:
        return {
            "n_days": int(len(sub)),
            "sum_R": round(float(sub.sum()), 4),
            "n_periods": 0,
            "hit_rate": None,
            "E_period": None,
            "worst_period": None,
        }
    hit = float((periods > 0).mean())
    return {
        "n_days": int(len(sub)),
        "sum_R": round(float(sub.sum()), 4),
        "n_periods": int(len(periods)),
        "hit_rate": round(hit, 4),
        "E_period": round(float(periods.mean()), 4),
        "worst_period": round(float(periods.min()), 4),
        "periods": {
            str(i.date()) if hasattr(i, "date") else str(i)[:10]: round(float(v), 4)
            for i, v in periods.items()
        },
    }
