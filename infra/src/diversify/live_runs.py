"""DIV-P2 live-preset run cards — what to re-test for the diversify panel."""
from __future__ import annotations

from dataclasses import asdict, dataclass


@dataclass(frozen=True)
class LiveRunCard:
    asset_id: str
    broker_symbol: str
    tf: str
    magic: int
    preset: str
    sl_pts: float
    tp_pts: float
    designed_rr: float
    leak_pp: float
    bwr: float
    session: str
    window_hint: str  # recommended Tester from→to
    notes: str
    risk_pct: float = 0.5  # live InpRiskPercent — portfolio live-risk weighting
    deploy: str = "SHADOW"  # live L2 posture: SHADOW (skips logged) or CURRENT (skips enforced)


# First live book — run each as a separate long Tester pass (every tick, ACCOUNT CURRENCY).
LIVE_RUNS: tuple[LiveRunCard, ...] = (
    LiveRunCard(
        asset_id="EURUSD",
        broker_symbol="EURUSD",
        tf="M5",
        magic=8210204,
        preset="LIVE-SHADOW_EURUSD_M5.set",
        sl_pts=300,
        tp_pts=300,
        designed_rr=1.0,
        leak_pp=2.2,
        bwr=50.0,
        session="12–20 skip Tue",
        window_hint="2026.05.01 → 2026.10.20 (tip 6m primary)",
        notes="Production INF",
    ),
    LiveRunCard(
        asset_id="AUDUSD",
        broker_symbol="AUDUSD",
        tf="M5",
        magic=8230931,
        preset="LIVE-SHADOW_AUDUSD_M5.set",
        sl_pts=300,
        tp_pts=300,
        designed_rr=1.0,
        leak_pp=2.4,
        bwr=50.0,
        session="13–20 skip Mon/Tue",
        window_hint="2026.05.01 → 2026.10.20 (tip 6m primary)",
        notes="SCALE Risk 3% — not FT twin 8230921",
        risk_pct=3.0,
    ),
    LiveRunCard(
        asset_id="AAPL",
        broker_symbol="Apple",
        tf="M5",
        magic=26162017,
        preset="AAPL_5m_stack.set",
        sl_pts=190,
        tp_pts=280,
        designed_rr=1.47,
        leak_pp=15.3,
        bwr=40.4,
        session="14–20 skip Tue",
        window_hint="2026.05.01 → 2026.10.20 (tip 6m primary)",
        notes="Research OS · Leak profile authority",
        deploy="CURRENT",
    ),
    LiveRunCard(
        asset_id="UK100",
        broker_symbol="UK100",
        tf="M5",
        magic=26121907,
        preset="LIVE-SHADOW_UK100_M5.set",
        sl_pts=1800,
        tp_pts=2250,
        designed_rr=1.25,
        leak_pp=5.93,
        bwr=44.4,
        session="08–17 skip Tue",
        window_hint="2026.05.01 → 2026.10.20 (tip 6m primary)",
        notes="Research OS",
    ),
    LiveRunCard(
        asset_id="JP225",
        broker_symbol="JPN225",
        tf="M5",
        magic=26161907,
        preset="JPN225_5m_stack.set",
        sl_pts=25000,
        tp_pts=50000,
        designed_rr=2.0,
        leak_pp=3.3,
        bwr=33.3,
        session="08–17 skip Tue",
        window_hint="2026.05.01 → 2026.10.20 (tip 6m primary)",
        notes="Research OS · Growth RR2",
        deploy="CURRENT",
    ),
    LiveRunCard(
        asset_id="DE40",
        broker_symbol="DE30",
        tf="M5",
        magic=26151907,
        preset="LIVE-SHADOW_DE30_M5.set",
        sl_pts=7000,
        tp_pts=8750,
        designed_rr=1.25,
        leak_pp=7.0,
        bwr=44.4,
        session="08–17 skip Tue",
        window_hint="2026.05.01 → 2026.10.20 (tip 6m primary)",
        notes="Research OS · broker DE30",
    ),
    LiveRunCard(
        asset_id="USDJPY",
        broker_symbol="USDJPY",
        tf="M15",
        magic=26131807,
        preset="USDJPYstack.set",
        sl_pts=100,
        tp_pts=120,
        designed_rr=1.2,
        leak_pp=11.4,
        bwr=45.5,
        session="12–20 skip Tue",
        window_hint="2026.05.01 → 2026.10.20 (tip 6m primary)",
        notes="Only M15 sleeve",
        deploy="CURRENT",
    ),
)


def by_magic() -> dict[int, LiveRunCard]:
    return {c.magic: c for c in LIVE_RUNS}


def by_asset() -> dict[str, LiveRunCard]:
    return {c.asset_id: c for c in LIVE_RUNS}


def by_broker_symbol() -> dict[str, LiveRunCard]:
    return {c.broker_symbol: c for c in LIVE_RUNS}


def cards_dict() -> dict:
    return {"version": "0.1.0", "runs": [asdict(c) for c in LIVE_RUNS]}
