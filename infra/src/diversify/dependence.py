"""Pairwise correlation and co-loss on daily R panel."""
from __future__ import annotations

import itertools
from typing import Any

import numpy as np
import pandas as pd


def corr_full(panel: pd.DataFrame) -> pd.DataFrame:
    return panel.corr(method="pearson").round(4)


def corr_active(panel: pd.DataFrame) -> pd.DataFrame:
    """Pairwise corr using only days where at least one of the pair is active."""
    assets = list(panel.columns)
    mat = pd.DataFrame(np.nan, index=assets, columns=assets, dtype=float)
    for a, b in itertools.product(assets, repeat=2):
        if a == b:
            mat.loc[a, b] = 1.0
            continue
        sub = panel[[a, b]]
        mask = (sub[a] != 0) | (sub[b] != 0)
        sub = sub.loc[mask]
        if len(sub) < 5:
            mat.loc[a, b] = np.nan
        else:
            mat.loc[a, b] = float(sub[a].corr(sub[b]))
    return mat.round(4)


def pairwise_coloss(panel: pd.DataFrame) -> list[dict[str, Any]]:
    """P(both lose | both active) and related dependence stats."""
    assets = list(panel.columns)
    rows: list[dict[str, Any]] = []
    for a, b in itertools.combinations(assets, 2):
        both = panel[(panel[a] != 0) & (panel[b] != 0)]
        n_both = int(len(both))
        if n_both == 0:
            rows.append(
                {
                    "a": a,
                    "b": b,
                    "n_both_active": 0,
                    "co_loss_rate": None,
                    "co_win_rate": None,
                    "same_sign_rate": None,
                    "corr_active": None,
                }
            )
            continue
        co_loss = float(((both[a] < 0) & (both[b] < 0)).mean())
        co_win = float(((both[a] > 0) & (both[b] > 0)).mean())
        same = float((np.sign(both[a]) == np.sign(both[b])).mean())
        corr = float(both[a].corr(both[b])) if n_both >= 5 else None
        rows.append(
            {
                "a": a,
                "b": b,
                "n_both_active": n_both,
                "co_loss_rate": round(co_loss, 4),
                "co_win_rate": round(co_win, 4),
                "same_sign_rate": round(same, 4),
                "corr_active": None if corr is None or np.isnan(corr) else round(corr, 4),
            }
        )
    rows.sort(key=lambda r: (-(r["co_loss_rate"] or -1), -(r["n_both_active"])))
    return rows


def do_not_combine(
    coloss: list[dict[str, Any]],
    *,
    min_n: int = 8,
    co_loss_floor: float = 0.35,
    known_twins: tuple[tuple[str, str], ...] = (
        ("EURUSD", "AUDUSD"),
        ("UK100", "DE40"),
    ),
) -> list[dict[str, Any]]:
    """Flag high co-loss pairs and known twin hypotheses."""
    flagged: list[dict[str, Any]] = []
    twin_set = {frozenset(p) for p in known_twins}
    for row in coloss:
        key = frozenset((row["a"], row["b"]))
        reasons: list[str] = []
        if key in twin_set:
            reasons.append("known_twin_hypothesis")
        if (
            row["n_both_active"] >= min_n
            and row["co_loss_rate"] is not None
            and row["co_loss_rate"] >= co_loss_floor
        ):
            reasons.append(f"co_loss>={co_loss_floor}")
        if reasons:
            flagged.append({**row, "reasons": reasons})
    return flagged


def filter_panel_by_mask(panel: pd.DataFrame, mask: pd.Series) -> pd.DataFrame:
    m = mask.reindex(panel.index).fillna(False).astype(bool)
    return panel.loc[m]


def conditioned_dependence(
    panel: pd.DataFrame,
    book_reg: pd.Series,
    *,
    regimes: tuple[str, ...] = ("MISMATCH", "FRAGILE"),
    stress_mask: pd.Series | None = None,
) -> dict[str, Any]:
    """
    Full vs regime-conditioned vs stress-day dependence snapshots.
    """
    out: dict[str, Any] = {
        "full": {
            "n_days": int(len(panel)),
            "corr_active": corr_active(panel).where(pd.notnull(corr_active(panel)), None).to_dict(),
            "coloss": pairwise_coloss(panel),
        }
    }
    br = book_reg.reindex(panel.index).fillna("UNTAGGED")
    for reg in regimes:
        sub = filter_panel_by_mask(panel, br == reg)
        out[f"regime_{reg}"] = {
            "n_days": int(len(sub)),
            "corr_active": (
                corr_active(sub).where(pd.notnull(corr_active(sub)), None).to_dict()
                if len(sub) >= 5
                else None
            ),
            "coloss": pairwise_coloss(sub) if len(sub) >= 1 else [],
        }
    # adverse = MISMATCH or FRAGILE
    adverse = br.isin(("MISMATCH", "FRAGILE"))
    sub_a = filter_panel_by_mask(panel, adverse)
    out["regime_ADVERSE"] = {
        "n_days": int(len(sub_a)),
        "definition": "MISMATCH | FRAGILE",
        "corr_active": (
            corr_active(sub_a).where(pd.notnull(corr_active(sub_a)), None).to_dict()
            if len(sub_a) >= 5
            else None
        ),
        "coloss": pairwise_coloss(sub_a) if len(sub_a) >= 1 else [],
    }
    if stress_mask is not None:
        sub_s = filter_panel_by_mask(panel, stress_mask)
        out["stress_calendar"] = {
            "n_days": int(len(sub_s)),
            "corr_active": (
                corr_active(sub_s).where(pd.notnull(corr_active(sub_s)), None).to_dict()
                if len(sub_s) >= 5
                else None
            ),
            "coloss": pairwise_coloss(sub_s) if len(sub_s) >= 1 else [],
        }
    return out


def coloss_delta(
    full: list[dict[str, Any]], conditioned: list[dict[str, Any]]
) -> list[dict[str, Any]]:
    """Compare co_loss_rate full vs conditioned for overlapping pairs."""
    fmap = {(r["a"], r["b"]): r for r in full}
    out: list[dict[str, Any]] = []
    for r in conditioned:
        key = (r["a"], r["b"])
        base = fmap.get(key) or fmap.get((r["b"], r["a"]))
        if not base or r["co_loss_rate"] is None or base["co_loss_rate"] is None:
            continue
        out.append(
            {
                "a": r["a"],
                "b": r["b"],
                "co_loss_full": base["co_loss_rate"],
                "co_loss_cond": r["co_loss_rate"],
                "delta": round(r["co_loss_rate"] - base["co_loss_rate"], 4),
                "n_both_cond": r["n_both_active"],
                "n_both_full": base["n_both_active"],
            }
        )
    out.sort(key=lambda x: -(x["delta"] or 0))
    return out
