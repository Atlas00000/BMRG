"""Frozen live book + seed tiers / bans for GRP-P0."""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
P2_SLEEVES = REPO / "infra" / "artefacts" / "diversify" / "P2_LATEST" / "sleeves"
OUT_LATEST = REPO / "infra" / "artefacts" / "grouping" / "LATEST"
ARCHIVE = REPO / "blotter" / "archive" / "GRP-P0-T01"


@dataclass(frozen=True)
class SleeveMeta:
    asset_id: str
    broker: str
    tf: str
    magic: int
    tier: str  # core | watch | caution
    trades_per_30d: float  # tip panel


SLEEVES: tuple[SleeveMeta, ...] = (
    SleeveMeta("EURUSD", "EURUSD", "M5", 8210204, "core", 19.5),
    SleeveMeta("JP225", "JPN225", "M5", 26161907, "core", 12.8),
    SleeveMeta("DE40", "DE30", "M5", 26151907, "core", 20.6),
    SleeveMeta("AUDUSD", "AUDUSD", "M5", 8230931, "watch", 11.2),
    SleeveMeta("USDJPY", "USDJPY", "M15", 26131807, "watch", 9.5),
    SleeveMeta("UK100", "UK100", "M5", 26121907, "caution", 28.6),
    SleeveMeta("AAPL", "Apple", "M5", 26162017, "caution", 8.4),
)

by_id = {s.asset_id: s for s in SLEEVES}

# Hard ban at full equal weight (GRP-P0)
HARD_BAN_PAIRS: frozenset[frozenset[str]] = frozenset(
    {
        frozenset({"EURUSD", "AUDUSD"}),
    }
)

# Soft penalty pairs (flag; do not auto-exclude unless stress fails later)
SOFT_PENALTY_PAIRS: frozenset[frozenset[str]] = frozenset(
    {
        frozenset({"UK100", "DE40"}),
    }
)

# Admission thresholds (tip panel · provisional until GRP-P2 bootstrap)
MONTH_HIT_FLOOR = 0.67
QUARTER_HIT_FLOOR = 0.67
EUR_HIT_SLACK = 0.10  # month_hit may be < 0.67 if within slack of EUR-only
CVAR_TOLERANCE_R = 2.0  # CVaR_m20 >= EUR_CVaR - tolerance (less negative OK within tol)

KS = (2, 3, 4, 5)
