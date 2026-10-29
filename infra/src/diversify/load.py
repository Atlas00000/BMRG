"""Load sleeve trade events from fire tapes / harvest labeled CSVs."""
from __future__ import annotations

import csv
from dataclasses import dataclass
from datetime import date, datetime
from pathlib import Path

from .manifest import SLEEVES, SleeveSource


@dataclass
class TradeEvent:
    asset_id: str
    close_date: date
    open_dt: datetime | None
    pnl_R: float
    win: bool
    regime_tag: str | None


def _parse_mt5_dt(s: str) -> datetime:
    s = (s or "").strip().strip('"')
    for fmt in ("%Y.%m.%d %H:%M:%S", "%Y.%m.%d %H:%M"):
        try:
            return datetime.strptime(s, fmt)
        except ValueError:
            continue
    raise ValueError(f"unparseable datetime: {s!r}")


def _load_fire_tape(src: SleeveSource) -> list[TradeEvent]:
    path = src.tape_path
    out: list[TradeEvent] = []
    with path.open(encoding="utf-8-sig", newline="") as f:
        for row in csv.DictReader(f):
            close_s = row.get("close_time") or row.get("open_time")
            if not close_s:
                continue
            close_dt = _parse_mt5_dt(close_s)
            open_dt = _parse_mt5_dt(row["open_time"]) if row.get("open_time") else None
            pnl = float(row["pnl_R_design"])
            regime = row.get("regime_tag") or row.get("ouroboros_tag") or None
            out.append(
                TradeEvent(
                    asset_id=src.asset_id,
                    close_date=close_dt.date(),
                    open_dt=open_dt,
                    pnl_R=pnl,
                    win=pnl > 0,
                    regime_tag=regime,
                )
            )
    return out


def _load_harvest_labeled(src: SleeveSource) -> list[TradeEvent]:
    """EURUSD Harvest: outcome TP → +1R, SL → −1R; attribute to exit_t date."""
    path = src.tape_path
    out: list[TradeEvent] = []
    with path.open(encoding="utf-8-sig", newline="") as f:
        for row in csv.DictReader(f):
            outcome = (row.get("outcome") or "").upper()
            if outcome not in ("TP", "SL"):
                continue
            exit_s = row.get("exit_t") or row.get("t")
            exit_dt = _parse_mt5_dt(exit_s)
            open_dt = _parse_mt5_dt(row["t"]) if row.get("t") else None
            pnl = 1.0 if outcome == "TP" else -1.0
            out.append(
                TradeEvent(
                    asset_id=src.asset_id,
                    close_date=exit_dt.date(),
                    open_dt=open_dt,
                    pnl_R=pnl,
                    win=pnl > 0,
                    regime_tag=None,
                )
            )
    return out


def load_sleeve(src: SleeveSource) -> list[TradeEvent]:
    if not src.tape_path.exists():
        raise FileNotFoundError(src.tape_path)
    if src.tape_kind == "harvest_labeled":
        return _load_harvest_labeled(src)
    if src.tape_kind == "fire_tape":
        return _load_fire_tape(src)
    raise ValueError(f"unknown tape_kind {src.tape_kind}")


def load_all(sleeves: tuple[SleeveSource, ...] = SLEEVES) -> dict[str, list[TradeEvent]]:
    return {s.asset_id: load_sleeve(s) for s in sleeves}


def sleeve_summaries(events: dict[str, list[TradeEvent]]) -> dict[str, dict]:
    summary = {}
    for aid, rows in events.items():
        if not rows:
            summary[aid] = {"n": 0}
            continue
        pnls = [r.pnl_R for r in rows]
        dates = [r.close_date for r in rows]
        summary[aid] = {
            "n": len(rows),
            "E_N": round(sum(pnls) / len(pnls), 4),
            "WR": round(sum(1 for r in rows if r.win) / len(rows), 4),
            "date_min": min(dates).isoformat(),
            "date_max": max(dates).isoformat(),
        }
    return summary
