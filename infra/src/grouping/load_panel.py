"""Load tip fire tapes → daily R panel."""
from __future__ import annotations

import csv
from datetime import datetime
from pathlib import Path

import pandas as pd

from src.diversify.load import TradeEvent
from src.diversify.panel import daily_panel

from .universe import P2_SLEEVES, SLEEVES


def _parse_mt5_dt(s: str) -> datetime:
    s = (s or "").strip().strip('"')
    for fmt in ("%Y.%m.%d %H:%M:%S", "%Y.%m.%d %H:%M"):
        try:
            return datetime.strptime(s, fmt)
        except ValueError:
            continue
    raise ValueError(f"unparseable datetime: {s!r}")


def load_fire_tape(path: Path, asset_id: str) -> list[TradeEvent]:
    out: list[TradeEvent] = []
    with path.open(encoding="utf-8-sig", newline="") as f:
        for row in csv.DictReader(f):
            close_s = row.get("close_time") or row.get("open_time")
            if not close_s:
                continue
            close_dt = _parse_mt5_dt(close_s)
            open_dt = _parse_mt5_dt(row["open_time"]) if row.get("open_time") else None
            pnl = float(row["pnl_R_design"])
            out.append(
                TradeEvent(
                    asset_id=asset_id,
                    close_date=close_dt.date(),
                    open_dt=open_dt,
                    pnl_R=pnl,
                    win=pnl > 0,
                    regime_tag=None,
                )
            )
    return out


def load_tip_events(sleeves_dir: Path | None = None) -> dict[str, list[TradeEvent]]:
    root = sleeves_dir or P2_SLEEVES
    events: dict[str, list[TradeEvent]] = {}
    missing: list[str] = []
    for meta in SLEEVES:
        path = root / f"{meta.asset_id}_live_fire_tape.csv"
        if not path.exists():
            missing.append(meta.asset_id)
            continue
        events[meta.asset_id] = load_fire_tape(path, meta.asset_id)
    if missing:
        raise FileNotFoundError(
            f"Missing tip tapes in {root}: {', '.join(missing)}"
        )
    return events


def build_panel(sleeves_dir: Path | None = None) -> pd.DataFrame:
    events = load_tip_events(sleeves_dir)
    panel = daily_panel(events)
    # stable column order = universe order
    cols = [s.asset_id for s in SLEEVES if s.asset_id in panel.columns]
    return panel.loc[:, cols]


def sleeve_freq_map() -> dict[str, float]:
    return {s.asset_id: s.trades_per_30d for s in SLEEVES}


def sleeve_tier_map() -> dict[str, str]:
    return {s.asset_id: s.tier for s in SLEEVES}
