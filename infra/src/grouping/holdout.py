"""May–Aug fit / Sep–Oct validate holdout (GRP-P2)."""
from __future__ import annotations

from typing import Any

import pandas as pd

from src.diversify.score import cvar, max_drawdown, portfolio_series


FIT_MONTHS = frozenset({5, 6, 7, 8})  # May–Aug
VAL_MONTHS = frozenset({9, 10})  # Sep–Oct tip soft


def _month(d) -> int:
    return d.month if hasattr(d, "month") else pd.Timestamp(d).month


def slice_months(panel: pd.DataFrame, months: frozenset[int]) -> pd.DataFrame:
    mask = [_month(d) in months for d in panel.index]
    return panel.loc[mask]


def _score_slice(panel: pd.DataFrame, members: tuple[str, ...]) -> dict[str, Any]:
    if panel.empty:
        return {
            "n_days": 0,
            "sum_R": 0.0,
            "month_hit": None,
            "n_months": 0,
            "E_month": None,
            "CVaR_m20": None,
            "maxDD": 0.0,
            "worst_month": None,
        }
    rp = portfolio_series(panel, members)
    s = rp.copy()
    s.index = pd.to_datetime(s.index)
    monthly = s.resample("ME").sum()
    monthly = monthly[monthly.abs() > 1e-12]
    m_hit = float((monthly > 0).mean()) if len(monthly) else None
    return {
        "n_days": int(len(rp)),
        "sum_R": round(float(rp.sum()), 4),
        "month_hit": None if m_hit is None else round(m_hit, 4),
        "n_months": int(len(monthly)),
        "E_month": round(float(monthly.mean()), 4) if len(monthly) else None,
        "CVaR_m20": None if cvar(monthly) is None else round(cvar(monthly), 4),  # type: ignore
        "maxDD": round(max_drawdown(rp.cumsum()), 4),
        "worst_month": round(float(monthly.min()), 4) if len(monthly) else None,
        "best_month": round(float(monthly.max()), 4) if len(monthly) else None,
        "periods": {
            str(i.date()) if hasattr(i, "date") else str(i)[:10]: round(float(v), 4)
            for i, v in monthly.items()
        },
    }


def holdout_group(panel: pd.DataFrame, members: tuple[str, ...]) -> dict[str, Any]:
    fit = slice_months(panel, FIT_MONTHS)
    val = slice_months(panel, VAL_MONTHS)
    fit_s = _score_slice(fit, members)
    val_s = _score_slice(val, members)
    # OOS pass heuristics (declared in run_bootstrap)
    return {
        "fit_months": sorted(FIT_MONTHS),
        "val_months": sorted(VAL_MONTHS),
        "fit": {k: v for k, v in fit_s.items() if k != "periods"},
        "val": {k: v for k, v in val_s.items() if k != "periods"},
        "fit_periods": fit_s.get("periods"),
        "val_periods": val_s.get("periods"),
        "val_sum_R": val_s.get("sum_R"),
        "val_month_hit": val_s.get("month_hit"),
        "fit_month_hit": fit_s.get("month_hit"),
    }
