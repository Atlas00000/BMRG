"""Re-rank P0 groups with ban penalties + adverse-month hits (GRP-P1)."""
from __future__ import annotations

import itertools
from typing import Any

import pandas as pd

from .stress import (
    conditioned_period_hit,
    stress_day_mask,
    tip_adverse_day_mask,
)


# Penalty weights for composite stress_score (higher = worse)
PEN_HARD = 100.0  # exclusion
PEN_SOFT_PAIR = 8.0
PEN_SOFT_FLAG = 3.0
PEN_ADVERSE_HIT_MISS = 12.0  # tip Sep/Oct month_hit < 0.5
PEN_STRESS_NEG = 6.0  # curated stress sum_R < 0
PEN_HIGH_COLOSS = 5.0  # group max pair co_loss >= soft floor


def group_pair_hits(
    members: list[str],
    matrix: dict[str, Any],
) -> dict[str, Any]:
    hard_hits: list[list[str]] = []
    soft_hits: list[list[str]] = []
    for a, b in itertools.combinations(members, 2):
        key = frozenset((a, b))
        for h in matrix["hard_bans"]:
            if frozenset((h["a"], h["b"])) == key:
                hard_hits.append(sorted((a, b)))
        for s in matrix["soft_penalties"]:
            if frozenset((s["a"], s["b"])) == key:
                soft_hits.append(sorted((a, b)))
    return {"hard_hits": hard_hits, "soft_hits": soft_hits}


def max_pair_coloss(members: list[str], coloss: list[dict]) -> float | None:
    best = None
    mset = set(members)
    for row in coloss:
        if row["a"] in mset and row["b"] in mset and row.get("co_loss_rate") is not None:
            best = row["co_loss_rate"] if best is None else max(best, row["co_loss_rate"])
    return best


def enrich_group(
    group: dict[str, Any],
    panel: pd.DataFrame,
    matrix: dict[str, Any],
    *,
    tip_mask: pd.Series,
    stress_mask: pd.Series,
) -> dict[str, Any]:
    members = list(group["members"])
    hits = group_pair_hits(members, matrix)
    tip_c = conditioned_period_hit(panel, tuple(members), tip_mask, freq="ME")
    str_c = conditioned_period_hit(panel, tuple(members), stress_mask, freq="ME")
    mx = max_pair_coloss(members, matrix.get("coloss") or [])

    pen = 0.0
    tags: list[str] = []
    excluded = False
    if hits["hard_hits"]:
        pen += PEN_HARD
        tags.append("hard_ban_pair")
        excluded = True
    pen += PEN_SOFT_PAIR * len(hits["soft_hits"])
    if hits["soft_hits"]:
        tags.append("soft_penalty_pair")
    for f in group.get("soft_flags") or []:
        pen += PEN_SOFT_FLAG
        tags.append(f"flag:{f}")

    tip_hit = tip_c.get("hit_rate")
    if tip_hit is not None and tip_hit < 0.5 and tip_c.get("n_periods", 0) >= 1:
        pen += PEN_ADVERSE_HIT_MISS
        tags.append("tip_adverse_month_hit<0.5")
    if str_c.get("sum_R") is not None and str_c["sum_R"] < 0 and str_c.get("n_days", 0) >= 5:
        pen += PEN_STRESS_NEG
        tags.append("curated_stress_sum_R<0")
    soft_floor = (matrix.get("thresholds") or {}).get("co_loss_soft", 0.30)
    if mx is not None and mx >= soft_floor:
        pen += PEN_HIGH_COLOSS
        tags.append(f"max_pair_coloss>={soft_floor}")

    # stress resilience score: prefer high tip adverse hit, low pen
    resilience = None
    if tip_hit is not None:
        resilience = round(tip_hit - 0.05 * pen, 4)

    return {
        **group,
        "p1_hard_hits": hits["hard_hits"],
        "p1_soft_hits": hits["soft_hits"],
        "p1_max_pair_coloss": mx,
        "p1_tip_adverse": tip_c,
        "p1_curated_stress": {k: v for k, v in str_c.items() if k != "periods"},
        "p1_penalty": round(pen, 2),
        "p1_tags": sorted(set(tags)),
        "p1_excluded": excluded,
        "p1_resilience": resilience,
    }


def rerank_groups(
    groups: list[dict[str, Any]],
    panel: pd.DataFrame,
    matrix: dict[str, Any],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    tip_mask = tip_adverse_day_mask(panel)
    curated = stress_day_mask(panel)
    enriched = [
        enrich_group(g, panel, matrix, tip_mask=tip_mask, stress_mask=curated)
        for g in groups
    ]
    kept = [g for g in enriched if not g.get("p1_excluded")]
    dropped = [g for g in enriched if g.get("p1_excluded")]

    def key(g: dict[str, Any]) -> tuple:
        return (
            -(g.get("p1_penalty") or 0.0),  # lower penalty first when reverse
            g.get("p1_tip_adverse", {}).get("hit_rate") or 0.0,
            g.get("month_hit") or 0.0,
            g.get("quarter_hit") or 0.0,
            g.get("E_month") or 0.0,
            g.get("sum_R") or 0.0,
        )

    # sort: low penalty, high tip adverse hit, …
    kept.sort(
        key=lambda g: (
            g.get("p1_penalty") or 0.0,
            -(g.get("p1_tip_adverse", {}).get("hit_rate") or 0.0),
            -(g.get("month_hit") or 0.0),
            -(g.get("quarter_hit") or 0.0),
            -(g.get("E_month") or 0.0),
            -(g.get("sum_R") or 0.0),
        )
    )
    dropped.sort(key=lambda g: -(g.get("sum_R") or 0))
    return kept, dropped
