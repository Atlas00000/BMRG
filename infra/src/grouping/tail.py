"""Lower-tail co-loss / dependence beyond Pearson (GRP-P4-T03)."""
from __future__ import annotations

import itertools
from typing import Any

import numpy as np
import pandas as pd


def lower_tail_dep(
    x: np.ndarray,
    y: np.ndarray,
    *,
    q: float = 0.2,
) -> float | None:
    """
    P(Y below its q-quantile | X below its q-quantile) on active-ish samples.
    Returns None if too few points in the conditioning set.
    """
    if len(x) < 8:
        return None
    qx = np.quantile(x, q)
    qy = np.quantile(y, q)
    mask = x <= qx
    n = int(mask.sum())
    if n < 3:
        return None
    return float(np.mean(y[mask] <= qy))


def pairwise_tail(
    panel: pd.DataFrame,
    *,
    q: float = 0.2,
    min_n: int = 8,
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for a, b in itertools.combinations(list(panel.columns), 2):
        both = panel[(panel[a] != 0) & (panel[b] != 0)]
        n_both = int(len(both))
        if n_both < min_n:
            rows.append(
                {
                    "a": a,
                    "b": b,
                    "n_both_active": n_both,
                    "co_loss_rate": None,
                    "tail_dep_q": None,
                    "corr": None,
                    "joint_neg_days": 0,
                }
            )
            continue
        xa = both[a].to_numpy(dtype=float)
        xb = both[b].to_numpy(dtype=float)
        co_loss = float(((xa < 0) & (xb < 0)).mean())
        corr = float(np.corrcoef(xa, xb)[0, 1]) if n_both >= 5 else None
        if corr is not None and np.isnan(corr):
            corr = None
        td_ab = lower_tail_dep(xa, xb, q=q)
        td_ba = lower_tail_dep(xb, xa, q=q)
        # symmetric summary = mean of both directions when available
        tds = [t for t in (td_ab, td_ba) if t is not None]
        tail = float(np.mean(tds)) if tds else None
        # exceedance: both below joint empirical 20% of min(Ra,Rb) style
        joint = np.minimum(xa, xb)
        jq = np.quantile(joint, q)
        joint_neg = int(((xa < 0) & (xb < 0)).sum())
        rows.append(
            {
                "a": a,
                "b": b,
                "n_both_active": n_both,
                "co_loss_rate": round(co_loss, 4),
                "tail_dep_q": None if tail is None else round(tail, 4),
                "tail_dep_ab": None if td_ab is None else round(td_ab, 4),
                "tail_dep_ba": None if td_ba is None else round(td_ba, 4),
                "corr": None if corr is None else round(corr, 4),
                "joint_neg_days": joint_neg,
                "joint_q_threshold": round(float(jq), 4),
            }
        )
    rows.sort(
        key=lambda r: (
            -(r["tail_dep_q"] if r["tail_dep_q"] is not None else -1),
            -(r["co_loss_rate"] if r["co_loss_rate"] is not None else -1),
        )
    )
    return rows


def escalate_from_tail(
    tail_rows: list[dict[str, Any]],
    *,
    soft_pairs: set[frozenset[str]],
    hard_pairs: set[frozenset[str]],
    tail_hard: float = 0.55,
    tail_soft: float = 0.45,
    min_n: int = 8,
) -> dict[str, Any]:
    """
    Propose soft→hard escalations and new soft flags from tail dependence.
    Does not mutate seed hard bans.
    """
    escalate: list[dict[str, Any]] = []
    new_soft: list[dict[str, Any]] = []
    for r in tail_rows:
        key = frozenset((r["a"], r["b"]))
        td = r.get("tail_dep_q")
        n = r.get("n_both_active") or 0
        if td is None or n < min_n:
            continue
        if key in hard_pairs:
            continue
        if td >= tail_hard:
            escalate.append(
                {
                    **r,
                    "action": "escalate_hard",
                    "reason": f"tail_dep_q>={tail_hard}",
                    "was_soft": key in soft_pairs,
                }
            )
        elif td >= tail_soft and key not in soft_pairs:
            new_soft.append(
                {
                    **r,
                    "action": "new_soft",
                    "reason": f"tail_dep_q>={tail_soft}",
                }
            )
    return {
        "thresholds": {"tail_hard": tail_hard, "tail_soft": tail_soft, "min_n": min_n},
        "escalate_hard": escalate,
        "new_soft": new_soft,
    }


def group_max_tail(
    members: list[str],
    tail_rows: list[dict[str, Any]],
) -> float | None:
    mset = set(members)
    best = None
    for r in tail_rows:
        if r["a"] in mset and r["b"] in mset and r.get("tail_dep_q") is not None:
            best = r["tail_dep_q"] if best is None else max(best, r["tail_dep_q"])
    return best
