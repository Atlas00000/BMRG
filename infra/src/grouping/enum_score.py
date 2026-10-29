"""Exhaustive k=2…5 group scoring + provisional admission."""
from __future__ import annotations

import itertools
from typing import Any

import pandas as pd

from src.diversify.score import (
    cvar,
    fuse_days,
    max_drawdown,
    portfolio_series,
)

from .universe import (
    CVAR_TOLERANCE_R,
    EUR_HIT_SLACK,
    HARD_BAN_PAIRS,
    KS,
    MONTH_HIT_FLOOR,
    QUARTER_HIT_FLOOR,
    SOFT_PENALTY_PAIRS,
    by_id,
)


def _period_sums(r: pd.Series, freq: str) -> pd.Series:
    s = r.copy()
    s.index = pd.to_datetime(s.index)
    out = s.resample(freq).sum()
    return out[out.abs() > 1e-12]


def co_loss_share(panel: pd.DataFrame, members: tuple[str, ...]) -> float:
    """Share of days with any activity where ≥2 members lose."""
    sub = panel.loc[:, list(members)]
    active = (sub != 0).any(axis=1)
    if int(active.sum()) == 0:
        return 0.0
    n_lose = (sub < 0).sum(axis=1)
    return float(((n_lose >= 2) & active).sum() / active.sum())


def freq_flags(members: tuple[str, ...]) -> dict[str, Any]:
    freqs = [by_id[m].trades_per_30d for m in members if m in by_id]
    if not freqs:
        return {"freq_min": None, "freq_max": None, "freq_all_high": False, "freq_all_low": False}
    return {
        "freq_min": round(min(freqs), 2),
        "freq_max": round(max(freqs), 2),
        "freq_all_high": all(f > 20 for f in freqs),
        "freq_all_low": all(f < 10 for f in freqs),
    }


def tier_flags(members: tuple[str, ...]) -> dict[str, Any]:
    tiers = [by_id[m].tier for m in members if m in by_id]
    return {
        "tiers": tiers,
        "caution_only": bool(tiers) and all(t == "caution" for t in tiers),
        "n_core": sum(1 for t in tiers if t == "core"),
        "n_watch": sum(1 for t in tiers if t == "watch"),
        "n_caution": sum(1 for t in tiers if t == "caution"),
    }


def banned_hit(members: tuple[str, ...], bans: frozenset[frozenset[str]]) -> list[list[str]]:
    m = set(members)
    hits = []
    for pair in bans:
        if pair <= m:
            hits.append(sorted(pair))
    return hits


def score_group(panel: pd.DataFrame, members: tuple[str, ...]) -> dict[str, Any]:
    rp = portfolio_series(panel, members)
    monthly = _period_sums(rp, "ME")
    quarterly = _period_sums(rp, "QE")
    yearly = _period_sums(rp, "YE")
    cum = rp.cumsum()
    m_hit = float((monthly > 0).mean()) if len(monthly) else None
    q_hit = float((quarterly > 0).mean()) if len(quarterly) else None
    y_hit = float((yearly > 0).mean()) if len(yearly) else None
    hard = banned_hit(members, HARD_BAN_PAIRS)
    soft = banned_hit(members, SOFT_PENALTY_PAIRS)
    ff = freq_flags(members)
    tf = tier_flags(members)
    soft_flags = []
    if soft:
        soft_flags.append("eu_index_twin")
    if ff["freq_all_high"]:
        soft_flags.append("freq_all_high")
    if ff["freq_all_low"]:
        soft_flags.append("freq_all_low")
    if tf["caution_only"]:
        soft_flags.append("caution_only")

    return {
        "members": list(members),
        "group_id": "+".join(members),
        "k": len(members),
        "n_days": int(len(rp)),
        "active_days": int((rp != 0).sum()),
        "sum_R": round(float(rp.sum()), 4),
        "mean_daily_R": round(float(rp.mean()), 6),
        "month_hit": None if m_hit is None else round(m_hit, 4),
        "n_months": int(len(monthly)),
        "quarter_hit": None if q_hit is None else round(q_hit, 4),
        "n_quarters": int(len(quarterly)),
        "year_hit": None if y_hit is None else round(y_hit, 4),
        "n_years": int(len(yearly)),
        "E_month": round(float(monthly.mean()), 4) if len(monthly) else None,
        "E_quarter": round(float(quarterly.mean()), 4) if len(quarterly) else None,
        "CVaR_m20": None if cvar(monthly) is None else round(cvar(monthly), 4),  # type: ignore
        "worst_month": round(float(monthly.min()), 4) if len(monthly) else None,
        "best_month": round(float(monthly.max()), 4) if len(monthly) else None,
        "maxDD": round(max_drawdown(cum), 4),
        "fuse_days": fuse_days(panel, members),
        "co_loss": round(co_loss_share(panel, members), 4),
        "hard_ban": bool(hard),
        "hard_ban_pairs": hard,
        "soft_flags": soft_flags,
        "soft_penalty_pairs": soft,
        **ff,
        **tf,
        "period_M": {
            str(i.date()) if hasattr(i, "date") else str(i)[:10]: round(float(v), 4)
            for i, v in monthly.items()
        },
        "period_Q": {
            str(i.date()) if hasattr(i, "date") else str(i)[:10]: round(float(v), 4)
            for i, v in quarterly.items()
        },
    }


def enumerate_groups(panel: pd.DataFrame, ks: tuple[int, ...] = KS) -> list[dict[str, Any]]:
    assets = [c for c in panel.columns]
    scored: list[dict[str, Any]] = []
    for k in ks:
        for combo in itertools.combinations(assets, k):
            scored.append(score_group(panel, combo))
    return scored


def admit_provisional(
    scored: list[dict[str, Any]],
    eur: dict[str, Any] | None,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    """
    Tip-panel admission (rules 1–4). Rule 5 (bootstrap) deferred to GRP-P2 —
    accepted sets are marked provisional_pending_bootstrap=True.
    """
    eur_hit = (eur or {}).get("month_hit") or 0.0
    eur_cvar = (eur or {}).get("CVaR_m20")
    accepted: list[dict[str, Any]] = []
    rejected: list[dict[str, Any]] = []

    for s in scored:
        reasons: list[str] = []
        if s.get("hard_ban"):
            reasons.append("hard_ban_pair")
        m_hit = s.get("month_hit")
        q_hit = s.get("quarter_hit")
        if m_hit is None or s.get("n_months", 0) < 3:
            reasons.append("insufficient_months")
        else:
            ok_m = m_hit >= MONTH_HIT_FLOOR or m_hit >= (eur_hit - EUR_HIT_SLACK)
            if not ok_m:
                reasons.append(
                    f"month_hit={m_hit}<{MONTH_HIT_FLOOR} and below EUR slack"
                )
        if q_hit is None or s.get("n_quarters", 0) < 1:
            reasons.append("insufficient_quarters")
        elif q_hit < QUARTER_HIT_FLOOR:
            reasons.append(f"quarter_hit={q_hit}<{QUARTER_HIT_FLOOR}")
        cvar_m = s.get("CVaR_m20")
        if eur_cvar is not None and cvar_m is not None:
            # CVaR is negative; "worse" = more negative
            if cvar_m < (eur_cvar - CVAR_TOLERANCE_R):
                reasons.append(
                    f"CVaR_m20={cvar_m}<EUR({eur_cvar})-{CVAR_TOLERANCE_R}"
                )
        elif cvar_m is None:
            reasons.append("missing_CVaR")

        row = {
            **s,
            "reject_reasons": reasons,
            "provisional_pending_bootstrap": True,
            "beats_eur_month_hit": (
                m_hit is not None and m_hit > eur_hit
            ),
        }
        if reasons:
            rejected.append(row)
        else:
            accepted.append(row)

    def rank_key(r: dict[str, Any]) -> tuple:
        # reverse=True → higher first: soft-clean (1) before flagged (0)
        return (
            1 if not r.get("soft_flags") else 0,
            r.get("month_hit") or 0.0,
            r.get("quarter_hit") or 0.0,
            r.get("E_month") or 0.0,
            -(abs(r.get("CVaR_m20") or 0.0)),
            r.get("sum_R") or 0.0,
            -(r.get("fuse_days") or 0),
        )

    accepted.sort(key=rank_key, reverse=True)
    # soft-clean preferred among equals already via key
    rejected.sort(key=lambda r: (r.get("month_hit") or 0), reverse=True)
    return accepted, rejected


def period_table_rows(scored: list[dict[str, Any]], freq: str) -> list[dict[str, Any]]:
    key = "period_M" if freq == "M" else "period_Q"
    rows = []
    for s in scored:
        for pid, val in (s.get(key) or {}).items():
            rows.append(
                {
                    "group_id": s["group_id"],
                    "k": s["k"],
                    "members": "|".join(s["members"]),
                    "period": pid,
                    "freq": freq,
                    "sum_R": val,
                    "positive_cycle": val > 0,
                    "month_hit": s.get("month_hit"),
                    "quarter_hit": s.get("quarter_hit"),
                    "hard_ban": s.get("hard_ban"),
                    "soft_flags": "|".join(s.get("soft_flags") or []),
                }
            )
    return rows
