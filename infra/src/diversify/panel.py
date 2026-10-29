"""Build calendar daily R panel from trade events."""
from __future__ import annotations

from datetime import date, timedelta

import pandas as pd

from .load import TradeEvent


def daily_panel(events: dict[str, list[TradeEvent]]) -> pd.DataFrame:
    """Close-date sum of pnl_R per asset; missing days → 0."""
    frames: list[pd.DataFrame] = []
    for aid, rows in events.items():
        if not rows:
            continue
        s = (
            pd.DataFrame(
                {"date": [r.close_date for r in rows], "pnl_R": [r.pnl_R for r in rows]}
            )
            .groupby("date", as_index=True)["pnl_R"]
            .sum()
            .rename(aid)
        )
        frames.append(s)
    if not frames:
        return pd.DataFrame()
    panel = pd.concat(frames, axis=1).sort_index()
    # full calendar between global min/max
    d0 = panel.index.min()
    d1 = panel.index.max()
    all_days = pd.date_range(d0, d1, freq="D")
    # keep as date index
    panel.index = pd.to_datetime(panel.index)
    panel = panel.reindex(all_days).fillna(0.0)
    panel.index = panel.index.date
    panel.index.name = "date"
    return panel


def overlap_window(panel: pd.DataFrame, min_active_sleeves: int = 2) -> tuple[date, date]:
    """First/last date where at least min_active_sleeves have non-zero history started."""
    # Use full panel span; callers may slice later
    idx = list(panel.index)
    return idx[0], idx[-1]


def active_mask(panel: pd.DataFrame) -> pd.DataFrame:
    return panel != 0.0
