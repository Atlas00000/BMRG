"""
Lightweight surrogate: features → predicted month_hit (GRP-P4-T02).

Uses ridge regression on tip groups (OOS-stable + failed) for fragility flags.
Not a substitute for the cycle simulator — scale-up / diagnostic only.
"""
from __future__ import annotations

from typing import Any

import numpy as np

from .universe import by_id


FEATURE_NAMES = (
    "k",
    "n_core",
    "n_watch",
    "n_caution",
    "has_eur",
    "has_aud",
    "has_uk",
    "has_aapl",
    "mean_freq",
    "freq_spread",
    "max_tail",
    "max_coloss",
    "mean_corr",
)


def _tier_counts(members: list[str]) -> tuple[int, int, int]:
    n_core = n_watch = n_caution = 0
    for m in members:
        t = by_id[m].tier if m in by_id else "watch"
        if t == "core":
            n_core += 1
        elif t == "caution":
            n_caution += 1
        else:
            n_watch += 1
    return n_core, n_watch, n_caution


def featurize(
    members: list[str],
    *,
    max_tail: float | None,
    max_coloss: float | None,
    mean_corr: float | None,
) -> np.ndarray:
    n_core, n_watch, n_caution = _tier_counts(members)
    freqs = [by_id[m].trades_per_30d for m in members if m in by_id]
    mean_f = float(np.mean(freqs)) if freqs else 0.0
    spread = float(np.max(freqs) - np.min(freqs)) if len(freqs) >= 2 else 0.0
    return np.array(
        [
            len(members),
            n_core,
            n_watch,
            n_caution,
            1.0 if "EURUSD" in members else 0.0,
            1.0 if "AUDUSD" in members else 0.0,
            1.0 if "UK100" in members else 0.0,
            1.0 if "AAPL" in members else 0.0,
            mean_f,
            spread,
            float(max_tail or 0.0),
            float(max_coloss or 0.0),
            float(mean_corr or 0.0),
        ],
        dtype=float,
    )


def ridge_fit(
    X: np.ndarray,
    y: np.ndarray,
    *,
    l2: float = 1.0,
) -> np.ndarray:
    """Return coefficients including intercept as last... actually first: [b0, b]."""
    n, p = X.shape
    Xb = np.column_stack([np.ones(n), X])
    A = Xb.T @ Xb + l2 * np.eye(p + 1)
    A[0, 0] -= l2  # don't shrink intercept
    beta = np.linalg.solve(A, Xb.T @ y)
    return beta


def ridge_predict(beta: np.ndarray, X: np.ndarray) -> np.ndarray:
    Xb = np.column_stack([np.ones(len(X)), X])
    return Xb @ beta


def leave_one_out_r2(X: np.ndarray, y: np.ndarray, *, l2: float = 1.0) -> float:
    preds = np.empty(len(y))
    for i in range(len(y)):
        mask = np.ones(len(y), dtype=bool)
        mask[i] = False
        beta = ridge_fit(X[mask], y[mask], l2=l2)
        preds[i] = ridge_predict(beta, X[i : i + 1])[0]
    ss_res = float(np.sum((y - preds) ** 2))
    ss_tot = float(np.sum((y - y.mean()) ** 2))
    if ss_tot < 1e-12:
        return 0.0
    return 1.0 - ss_res / ss_tot


def fit_surrogate(rows: list[dict[str, Any]]) -> dict[str, Any]:
    """
    rows need: members, month_hit, max_tail_dep, max_coloss, mean_pair_corr
    """
    X_list = []
    y_list = []
    ids = []
    for r in rows:
        members = list(r["members"])
        y = r.get("month_hit")
        if y is None:
            continue
        x = featurize(
            members,
            max_tail=r.get("max_tail_dep"),
            max_coloss=r.get("max_coloss"),
            mean_corr=r.get("mean_pair_corr"),
        )
        X_list.append(x)
        y_list.append(float(y))
        ids.append(r.get("group_id"))
    if len(y_list) < 5:
        return {"ok": False, "reason": "insufficient_rows", "n": len(y_list)}

    X = np.vstack(X_list)
    y = np.array(y_list)
    # standardize features (not target)
    mu = X.mean(axis=0)
    sd = X.std(axis=0)
    sd = np.where(sd < 1e-8, 1.0, sd)
    Xs = (X - mu) / sd
    beta = ridge_fit(Xs, y, l2=1.0)
    loo = leave_one_out_r2(Xs, y, l2=1.0)
    pred = ridge_predict(beta, Xs)
    resid = y - pred

    scored = []
    for i, gid in enumerate(ids):
        scored.append(
            {
                "group_id": gid,
                "month_hit_obs": round(float(y[i]), 4),
                "month_hit_pred": round(float(pred[i]), 4),
                "residual": round(float(resid[i]), 4),
                # fragile if observed << predicted? or predicted low
                "fragile_flag": bool(pred[i] < 0.7 and y[i] >= 0.8),
                "optimistic_flag": bool(y[i] - pred[i] > 0.15),
            }
        )

    coef = {
        name: round(float(beta[i + 1]), 4) for i, name in enumerate(FEATURE_NAMES)
    }
    return {
        "ok": True,
        "n": len(y_list),
        "intercept": round(float(beta[0]), 4),
        "coefficients": coef,
        "loo_r2": round(float(loo), 4),
        "rmse": round(float(np.sqrt(np.mean(resid**2))), 4),
        "feature_scale_mean": mu.tolist(),
        "feature_scale_std": sd.tolist(),
        "predictions": scored,
    }
