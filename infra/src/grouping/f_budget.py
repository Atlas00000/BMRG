"""
f / capital budget hints inside a group (GRP-P3).

Not live attach policy — suggests weight caps so production EURUSD does not
cede the book, and research sleeves stay light.
"""
from __future__ import annotations

from typing import Any

from .universe import by_id

PRODUCTION = "EURUSD"
# Caps on portfolio weight (sum w = 1)
PROD_WEIGHT_CAP = 0.50
PROD_WEIGHT_FLOOR = 0.25  # if EURUSD in group, keep at least this after renormalize attempt
RESEARCH_WEIGHT_CAP = 0.40
CAUTION_WEIGHT_CAP = 0.25


def tier_of(asset_id: str) -> str:
    meta = by_id.get(asset_id)
    return meta.tier if meta else "research"


def apply_f_budget(weights: dict[str, float]) -> dict[str, Any]:
    """
    Clip weights by tier caps then renormalize. Returns clipped weights + notes.
    """
    w = dict(weights)
    notes: list[str] = []
    # clip research / caution
    for a, wi in list(w.items()):
        tier = tier_of(a)
        if a == PRODUCTION:
            if wi > PROD_WEIGHT_CAP:
                w[a] = PROD_WEIGHT_CAP
                notes.append(f"{a} clipped to prod_cap {PROD_WEIGHT_CAP}")
        elif tier == "caution":
            if wi > CAUTION_WEIGHT_CAP:
                w[a] = CAUTION_WEIGHT_CAP
                notes.append(f"{a} clipped to caution_cap {CAUTION_WEIGHT_CAP}")
        else:
            if wi > RESEARCH_WEIGHT_CAP:
                w[a] = RESEARCH_WEIGHT_CAP
                notes.append(f"{a} clipped to research_cap {RESEARCH_WEIGHT_CAP}")

    s = sum(w.values())
    if s <= 0:
        n = len(w) or 1
        w = {a: 1.0 / n for a in w}
        notes.append("fallback_equal")
    else:
        w = {a: v / s for a, v in w.items()}

    # enforce production floor if present
    if PRODUCTION in w and w[PRODUCTION] < PROD_WEIGHT_FLOOR:
        deficit = PROD_WEIGHT_FLOOR - w[PRODUCTION]
        others = [a for a in w if a != PRODUCTION]
        other_sum = sum(w[a] for a in others)
        if others and other_sum > deficit:
            scale = (other_sum - deficit) / other_sum
            for a in others:
                w[a] *= scale
            w[PRODUCTION] = PROD_WEIGHT_FLOOR
            notes.append(f"{PRODUCTION} raised to prod_floor {PROD_WEIGHT_FLOOR}")
            s2 = sum(w.values())
            w = {a: v / s2 for a, v in w.items()}

    w = {a: round(v, 6) for a, v in w.items()}
    return {
        "weights": w,
        "notes": notes,
        "caps": {
            "prod_cap": PROD_WEIGHT_CAP,
            "prod_floor": PROD_WEIGHT_FLOOR,
            "research_cap": RESEARCH_WEIGHT_CAP,
            "caution_cap": CAUTION_WEIGHT_CAP,
            "production": PRODUCTION,
        },
        "budget_mix": {
            "production_w": w.get(PRODUCTION, 0.0),
            "research_w": round(
                sum(v for a, v in w.items() if a != PRODUCTION and tier_of(a) != "caution"),
                6,
            ),
            "caution_w": round(
                sum(v for a, v in w.items() if tier_of(a) == "caution"),
                6,
            ),
        },
    }
