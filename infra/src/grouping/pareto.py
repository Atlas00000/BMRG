"""Multi-objective Pareto front over group metrics (GRP-P4-T01)."""
from __future__ import annotations

from typing import Any, Callable


# Objectives: maximize first three, minimize last two (stored as costs)
# We convert all to "higher is better" scores for domination.


def _higher_better(row: dict[str, Any]) -> tuple[float, ...]:
    hit_m = float(row.get("month_hit") or 0.0)
    hit_q = float(row.get("quarter_hit") or 0.0)
    e_m = float(row.get("E_month") or row.get("sum_R") or 0.0)
    # prefer less negative CVaR / maxDD / fuse / tail
    cvar = float(row.get("CVaR_m20") if row.get("CVaR_m20") is not None else 0.0)
    maxdd = float(row.get("maxDD") if row.get("maxDD") is not None else 0.0)
    fuse = float(row.get("fuse_days") or 0.0)
    tail = float(row.get("max_tail_dep") if row.get("max_tail_dep") is not None else 0.0)
    return (
        hit_m,
        hit_q,
        e_m,
        cvar,  # higher (closer to 0) better
        -abs(maxdd),
        -fuse,
        -tail,
    )


def dominates(a: tuple[float, ...], b: tuple[float, ...]) -> bool:
    """a dominates b if a >= b in all objs and > in at least one."""
    ge = all(x >= y for x, y in zip(a, b))
    gt = any(x > y for x, y in zip(a, b))
    return ge and gt


def pareto_front(
    rows: list[dict[str, Any]],
    *,
    score_fn: Callable[[dict[str, Any]], tuple[float, ...]] | None = None,
) -> list[dict[str, Any]]:
    score_fn = score_fn or _higher_better
    scored = [(score_fn(r), r) for r in rows]
    front: list[dict[str, Any]] = []
    for i, (si, ri) in enumerate(scored):
        dominated = False
        for j, (sj, _) in enumerate(scored):
            if i == j:
                continue
            if dominates(sj, si):
                dominated = True
                break
        if not dominated:
            out = dict(ri)
            out["pareto"] = True
            out["pareto_score"] = [round(x, 6) for x in si]
            front.append(out)
    # stable sort: hit_m, sum_R
    front.sort(
        key=lambda r: (
            r.get("month_hit") or 0,
            r.get("sum_R") or 0,
            -(r.get("max_tail_dep") or 0),
        ),
        reverse=True,
    )
    return front


def label_policies(front: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Tag frontier members with simple policy labels for ops."""
    if not front:
        return front
    by_sum = max(front, key=lambda r: r.get("sum_R") or 0)
    by_cvar = max(
        front,
        key=lambda r: r.get("CVaR_m20") if r.get("CVaR_m20") is not None else -999,
    )
    by_dd = max(front, key=lambda r: -(abs(r.get("maxDD") or 0)))
    by_tail = min(
        front,
        key=lambda r: r.get("max_tail_dep") if r.get("max_tail_dep") is not None else 999,
    )
    by_val = max(front, key=lambda r: r.get("val_sum_R") if r.get("val_sum_R") is not None else -999)

    tags = {
        by_sum.get("group_id"): "max_sum_R",
        by_cvar.get("group_id"): "best_CVaR",
        by_dd.get("group_id"): "min_maxDD",
        by_tail.get("group_id"): "min_tail",
        by_val.get("group_id"): "max_holdout_val",
    }
    out = []
    for r in front:
        gid = r.get("group_id")
        label = tags.get(gid)
        rr = dict(r)
        rr["policy_label"] = label
        out.append(rr)
    return out
