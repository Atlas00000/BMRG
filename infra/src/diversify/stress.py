"""
Known stress months from asset aos_bad_cells / profile docs (DIV-P1-T03).

Month is calendar month 1..12. These are research stress overlays — not auto L2 arms.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass

import pandas as pd


@dataclass(frozen=True)
class StressMonth:
    asset_id: str
    month: int  # 1..12
    label: str
    source: str


# Curated from doc/assets/*/aos_bad_cells*.md + profiles (2026-10)
STRESS_MONTHS: tuple[StressMonth, ...] = (
    # AUDUSD — May soft · Feb/Mar soft (edge_framework / bad cells)
    StressMonth("AUDUSD", 2, "Feb soft", "AUDUSD aos_bad_cells / profile"),
    StressMonth("AUDUSD", 3, "Mar soft", "AUDUSD aos_bad_cells / profile"),
    StressMonth("AUDUSD", 5, "May soft", "AUDUSD aos_bad_cells"),
    # AAPL M5 — May · Jul cells (aos_bad_cells_M5)
    StressMonth("AAPL", 5, "May cell", "AAPL aos_bad_cells_M5"),
    StressMonth("AAPL", 7, "Jul cell", "AAPL aos_bad_cells_M5"),
    # UK100 M5 — tip softness often Sep (profile / P1 notes)
    StressMonth("UK100", 9, "Sep tip soft", "UK100 M5 profile / P1"),
    # DE40 — Feb PRIMARY · Mar FRAGILE
    StressMonth("DE40", 2, "Feb stress-month", "DE40 aos_bad_cells"),
    StressMonth("DE40", 3, "Mar FRAGILE", "DE40 aos_bad_cells"),
    # JP225 M5 — Aug/Sep MATCH tax · Feb/Apr soft
    StressMonth("JP225", 2, "Feb soft", "JP225 aos_bad_cells_M5"),
    StressMonth("JP225", 4, "Apr soft", "JP225 aos_bad_cells_M5"),
    StressMonth("JP225", 8, "Aug MATCH tax", "JP225 aos_bad_cells_M5"),
    StressMonth("JP225", 9, "Sep MATCH tax", "JP225 aos_bad_cells_M5"),
    # USDJPY — prior stress months (thin; Jul often gated)
    StressMonth("USDJPY", 7, "Jul sleeve caution", "USDJPY aos_bad_cells / P6"),
    # EURUSD Harvest — Sep historically soft on ticket proxies
    StressMonth("EURUSD", 9, "Sep soft proxy", "EURUSD edge / historical tip"),
)


def stress_index() -> dict[str, list[dict]]:
    out: dict[str, list[dict]] = {}
    for s in STRESS_MONTHS:
        out.setdefault(s.asset_id, []).append(asdict(s))
    return out


def day_stress_flags(panel: pd.DataFrame) -> pd.DataFrame:
    """
    Boolean frame: asset × day True if calendar month is a stress month for that asset
    AND the sleeve is active that day (R != 0). Also book_stress = any active stress.
    """
    assets = [c for c in panel.columns]
    idx = list(panel.index)
    flags = pd.DataFrame(False, index=idx, columns=assets)
    month_map = {(s.asset_id, s.month) for s in STRESS_MONTHS}
    for d in idx:
        m = d.month if hasattr(d, "month") else pd.Timestamp(d).month
        for a in assets:
            if (a, m) in month_map and float(panel.loc[d, a]) != 0.0:
                flags.loc[d, a] = True
    flags["book_stress"] = flags[assets].any(axis=1)
    return flags


def stress_day_mask(panel: pd.DataFrame) -> pd.Series:
    return day_stress_flags(panel)["book_stress"].rename("stress")
