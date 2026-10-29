"""Hard-ban / soft-penalty matrix from tip co-loss + known twins (GRP-P1)."""
from __future__ import annotations

from typing import Any

from src.diversify.dependence import corr_active, corr_full, do_not_combine, pairwise_coloss

from .universe import HARD_BAN_PAIRS, SOFT_PENALTY_PAIRS


# Measured thresholds (tip panel)
CO_LOSS_HARD = 0.40  # escalate to hard ban
CO_LOSS_SOFT = 0.30  # soft penalty
MIN_N_BOTH = 6


KNOWN_TWINS: tuple[tuple[str, str], ...] = (
    ("EURUSD", "AUDUSD"),
    ("UK100", "DE40"),
)


def build_ban_matrix(panel) -> dict[str, Any]:
    coloss = pairwise_coloss(panel)
    c_full = corr_full(panel)
    c_act = corr_active(panel)
    flagged = do_not_combine(
        coloss,
        min_n=MIN_N_BOTH,
        co_loss_floor=CO_LOSS_SOFT,
        known_twins=KNOWN_TWINS,
    )

    hard: list[dict[str, Any]] = []
    soft: list[dict[str, Any]] = []
    seed_hard = {frozenset(p) for p in HARD_BAN_PAIRS}
    seed_soft = {frozenset(p) for p in SOFT_PENALTY_PAIRS}

    # index coloss
    cmap = {frozenset((r["a"], r["b"])): r for r in coloss}

    # Seed hard + soft always present
    for pair in seed_hard:
        a, b = sorted(pair)
        row = cmap.get(pair, {"a": a, "b": b, "co_loss_rate": None, "n_both_active": 0})
        hard.append(
            {
                "a": a,
                "b": b,
                "level": "hard",
                "reasons": ["seed_hard_ban", "usd_fade_twin"],
                "co_loss_rate": row.get("co_loss_rate"),
                "n_both_active": row.get("n_both_active"),
                "corr_active": row.get("corr_active"),
            }
        )
    for pair in seed_soft:
        a, b = sorted(pair)
        row = cmap.get(pair, {"a": a, "b": b, "co_loss_rate": None, "n_both_active": 0})
        reasons = ["seed_soft_penalty", "eu_index_twin"]
        level = "soft"
        cl = row.get("co_loss_rate")
        n = row.get("n_both_active") or 0
        if cl is not None and n >= MIN_N_BOTH and cl >= CO_LOSS_HARD:
            level = "hard"
            reasons.append(f"co_loss>={CO_LOSS_HARD}_escalate")
        entry = {
            "a": a,
            "b": b,
            "level": level,
            "reasons": reasons,
            "co_loss_rate": cl,
            "n_both_active": n,
            "corr_active": row.get("corr_active"),
        }
        if level == "hard":
            hard.append(entry)
        else:
            soft.append(entry)

    # Measured extras
    seen = {frozenset((h["a"], h["b"])) for h in hard} | {
        frozenset((s["a"], s["b"])) for s in soft
    }
    for row in flagged:
        key = frozenset((row["a"], row["b"]))
        if key in seen:
            continue
        cl = row.get("co_loss_rate")
        n = row.get("n_both_active") or 0
        reasons = list(row.get("reasons") or [])
        if cl is not None and n >= MIN_N_BOTH and cl >= CO_LOSS_HARD:
            hard.append(
                {
                    "a": row["a"],
                    "b": row["b"],
                    "level": "hard",
                    "reasons": reasons + [f"measured_co_loss>={CO_LOSS_HARD}"],
                    "co_loss_rate": cl,
                    "n_both_active": n,
                    "corr_active": row.get("corr_active"),
                }
            )
            seen.add(key)
        elif cl is not None and n >= MIN_N_BOTH and cl >= CO_LOSS_SOFT:
            soft.append(
                {
                    "a": row["a"],
                    "b": row["b"],
                    "level": "soft",
                    "reasons": reasons + [f"measured_co_loss>={CO_LOSS_SOFT}"],
                    "co_loss_rate": cl,
                    "n_both_active": n,
                    "corr_active": row.get("corr_active"),
                }
            )
            seen.add(key)

    hard_set = {frozenset((h["a"], h["b"])) for h in hard}
    soft_set = {frozenset((s["a"], s["b"])) for s in soft}

    return {
        "thresholds": {
            "co_loss_hard": CO_LOSS_HARD,
            "co_loss_soft": CO_LOSS_SOFT,
            "min_n_both": MIN_N_BOTH,
        },
        "hard_bans": hard,
        "soft_penalties": soft,
        "hard_ban_pairs": [sorted(p) for p in hard_set],
        "soft_penalty_pairs": [sorted(p) for p in soft_set],
        "coloss": coloss,
        "corr_full": c_full.where(c_full.notnull(), None).to_dict(),
        "corr_active": c_act.where(c_act.notnull(), None).to_dict(),
        "do_not_combine_raw": flagged,
    }


def pair_level(a: str, b: str, matrix: dict[str, Any]) -> str | None:
    key = frozenset((a, b))
    for h in matrix["hard_bans"]:
        if frozenset((h["a"], h["b"])) == key:
            return "hard"
    for s in matrix["soft_penalties"]:
        if frozenset((s["a"], s["b"])) == key:
            return "soft"
    return None
