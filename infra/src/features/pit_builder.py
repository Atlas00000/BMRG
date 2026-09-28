"""
Point-in-time L1 feature builder (INF-P3-T01).

Rules:
  - Features for an event may only use information available at/before entry_time
    (closed-bar as-of). Exit time / outcome must never enter the feature vector.
  - L1 does not skip or alter fire count.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any


DOW_NAMES = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]


def mt5_dow(ts: datetime) -> int:
    """MT5: 0=Sun … 6=Sat."""
    # Python: Mon=0 … Sun=6 → MT5
    return (ts.weekday() + 1) % 7


def session_id(hour: int) -> str:
    if 8 <= hour < 12:
        return "LON_AM"
    if 12 <= hour < 17:
        return "LON_NY"
    if 17 <= hour < 20:
        return "NY"
    if hour >= 20:
        return "POST_NY"
    return "ASIA"


def week_of_month(ts: datetime) -> int:
    return (ts.day - 1) // 7 + 1


def parse_ts(value: str | datetime) -> datetime:
    if isinstance(value, datetime):
        ts = value
    else:
        s = str(value).replace("T", " ").replace("Z", "").strip()
        # normalise dotted MT5 dates
        if len(s) >= 10 and s[4] == ".":
            s = s.replace(".", "-", 2)
        if len(s) == 16:  # YYYY-MM-DD HH:MM
            s = s + ":00"
        for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%dT%H:%M:%S"):
            try:
                ts = datetime.strptime(s[:19], fmt)
                break
            except ValueError:
                continue
        else:
            raise ValueError(f"unparsed timestamp: {value!r}")
    if ts.tzinfo is None:
        ts = ts.replace(tzinfo=timezone.utc)
    return ts.astimezone(timezone.utc)


@dataclass
class PitContext:
    """As-of snapshot at event open — no exit fields allowed."""

    entry_time: datetime
    symbol: str = "EURUSD"
    side: str = "NONE"
    spread_pts: float | None = None
    engine_magic: int = 8210204
    bb_dev_design: float = 2.2
    atr_pts: float | None = None
    bb_width_pct: float | None = None
    structure_id: str = "UNK"
    # Rolling history of prior (entry_time, spread) for terciles — must be strictly prior
    prior_spreads: list[float] | None = None


FORBIDDEN_FEATURE_KEYS = {
    "exit_time",
    "exit_reason",
    "y_lose",
    "pnl_gross_ccy",
    "pnl_net_ccy",
    "outcome",
    "hold_hours",
}


def tercile(value: float | None, history: list[float]) -> int | None:
    if value is None or len(history) < 9:
        return None
    xs = sorted(history)
    n = len(xs)
    t1, t2 = xs[n // 3], xs[(2 * n) // 3]
    if value <= t1:
        return 1
    if value <= t2:
        return 2
    return 3


def build_features(ctx: PitContext) -> dict[str, Any]:
    """Build aos_l1_v0+ feature dict PIT-correct at entry_time."""
    ts = ctx.entry_time
    hour = ts.hour
    dow = mt5_dow(ts)
    sess = session_id(hour)
    is_tue = dow == 2  # MT5 Tuesday
    cell_ids: list[str] = [f"SES_{sess}"]
    if is_tue:
        cell_ids.append("DOW_TUE")
    cell_ids.append(f"DOW_{DOW_NAMES[dow].upper()}")
    if ctx.side in {"BUY", "SELL"}:
        cell_ids.append(f"SIDE_{ctx.side}")

    prior = list(ctx.prior_spreads or [])
    # Strict PIT: only spreads from earlier events
    spread_terc = tercile(ctx.spread_pts, prior) if ctx.spread_pts is not None else None

    feats: dict[str, Any] = {
        "tape_schema": "aos_l1_v0",
        "t_close": ts.strftime("%Y.%m.%d %H:%M"),
        "t_close_iso": ts.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "symbol": ctx.symbol,
        "tf": "M5",
        "engine_magic": ctx.engine_magic,
        "hour_server": hour,
        "dow": dow,
        "dow_name": DOW_NAMES[dow],
        "session_id": sess,
        "is_tue": is_tue,
        "week_of_month": week_of_month(ts),
        "month": ts.month,
        "spread_pts": ctx.spread_pts,
        "spread_tercile": spread_terc,
        "side": ctx.side,
        "signal_hit": ctx.side in {"BUY", "SELL"},
        "structure_id": ctx.structure_id or "UNK",
        "trend_side": "unk",
        "er_tercile": None,
        "atr_pts": ctx.atr_pts,
        "atr_tercile": None,
        "bb_width_pct": ctx.bb_width_pct,
        "bb_width_tercile": None,
        "bb_dev_design": ctx.bb_dev_design,
        "event_flags": [],
        "in_blackout": False,
        "gap_flag": False,
        "swap_night_risk": True,  # overnight inventory possible on champ
        "cell_ids": cell_ids,
        "asof_ts": ts.strftime("%Y-%m-%dT%H:%M:%SZ"),
    }
    leaked = FORBIDDEN_FEATURE_KEYS.intersection(feats)
    if leaked:
        raise AssertionError(f"forbidden keys in features: {leaked}")
    return feats


def assert_pit_join(entry_time: datetime, feature_asof: datetime) -> None:
    """Join valid only if feature as-of ≤ entry."""
    if feature_asof > entry_time:
        raise AssertionError(
            f"PIT violation: feature asof {feature_asof.isoformat()} > entry {entry_time.isoformat()}"
        )


def leakage_probe(entry_time: datetime, exit_time: datetime, feats: dict[str, Any]) -> None:
    """Fail if any feature timestamp/value encodes the exit."""
    for k in FORBIDDEN_FEATURE_KEYS:
        if k in feats:
            raise AssertionError(f"leakage key present: {k}")
    asof = parse_ts(feats["asof_ts"])
    assert_pit_join(entry_time, asof)
    if asof >= exit_time and exit_time > entry_time:
        # asof must be at entry, not at/after exit
        if asof > entry_time:
            raise AssertionError("feature asof moved to/after exit")
