"""Live-book sleeve → historical fire-tape proxy mapping (DIV-P0)."""
from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]  # Experts/BMRG


@dataclass(frozen=True)
class SleeveSource:
    asset_id: str
    live_symbol: str
    live_magic: int
    live_preset: str
    tape_rel: str
    tape_kind: str  # fire_tape | harvest_labeled
    caveat: str

    @property
    def tape_path(self) -> Path:
        return REPO / self.tape_rel


SLEEVES: tuple[SleeveSource, ...] = (
    SleeveSource(
        asset_id="EURUSD",
        live_symbol="EURUSD",
        live_magic=8210204,
        live_preset="INF-LIVE_WITHHOLD_Harvest_long_ddl30.set",
        tape_rel="blotter/archive/AOS-P2-T03/harvest_long_labeled.csv",
        tape_kind="harvest_labeled",
        caveat="M5 Harvest TP/SL → ±1R design; engine path for live INF magic",
    ),
    SleeveSource(
        asset_id="AUDUSD",
        live_symbol="AUDUSD",
        live_magic=8230931,
        live_preset="AUDUSD-AIOS_SCALE_Risk3_champ_G0.set",
        tape_rel="blotter/archive/AUDUSD-AOS-P1/audusd_m15_tip_long_fire_tape.csv",
        tape_kind="fire_tape",
        caveat="M15 research tape proxy for live M5 SCALE 8230931 — TF mismatch",
    ),
    SleeveSource(
        asset_id="AAPL",
        live_symbol="Apple",
        live_magic=26162017,
        live_preset="AAPL_5m_stack.set",
        tape_rel="blotter/archive/AAPL-M5-AOS-P1/aapl_m5_long_fire_tape.csv",
        tape_kind="fire_tape",
        caveat="Engine Balanced magic 26102011 on tape; OS magic 26162017 on live",
    ),
    SleeveSource(
        asset_id="UK100",
        live_symbol="UK100",
        live_magic=26121907,
        live_preset="UK100_5m_stack.set",
        tape_rel="blotter/archive/UK100-M5-AOS-P1/uk100_m5_long_fire_tape.csv",
        tape_kind="fire_tape",
        caveat="Engine P0 M5 long; ends ~2026-08",
    ),
    SleeveSource(
        asset_id="JP225",
        live_symbol="JPN225",
        live_magic=26161907,
        live_preset="JPN225_5m_stack.set",
        tape_rel="blotter/archive/JP225-M5-AOS-P1/jp225_m5_ytd_fire_tape.csv",
        tape_kind="fire_tape",
        caveat="YTD M5 Growth engine tape",
    ),
    SleeveSource(
        asset_id="DE40",
        live_symbol="DE30",
        live_magic=26151907,
        live_preset="DE40_5m_stack.set",
        tape_rel="blotter/archive/DE40-M5-AOS-P1/de40_m5_ytd_fire_tape.csv",
        tape_kind="fire_tape",
        caveat="YTD M5 Balanced engine tape",
    ),
    SleeveSource(
        asset_id="USDJPY",
        live_symbol="USDJPY",
        live_magic=26131807,
        live_preset="USDJPYstack.set",
        tape_rel="blotter/archive/USDJPY-AOS-P1/usdjpy_long_fire_tape.csv",
        tape_kind="fire_tape",
        caveat="M15 Balanced engine long; OS magic on live",
    ),
)


def manifest_dict() -> dict:
    return {
        "version": "0.1.0",
        "repo_root": str(REPO),
        "sleeves": [asdict(s) for s in SLEEVES],
    }
