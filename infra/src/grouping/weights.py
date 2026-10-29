"""Portfolio weights inside a group: equal · inv-vol · risk-parity · HRP."""
from __future__ import annotations

from typing import Any

import numpy as np
import pandas as pd
from scipy.cluster.hierarchy import leaves_list, linkage
from scipy.spatial.distance import squareform

from src.diversify.score import cvar, max_drawdown


EPS = 1e-12


def _active_cov(panel: pd.DataFrame, members: list[str]) -> tuple[np.ndarray, list[str]]:
    """Covariance of daily R (full calendar; zeros included as flat days)."""
    sub = panel.loc[:, members].astype(float)
    # drop all-zero columns (no activity)
    keep = [m for m in members if float(sub[m].abs().sum()) > EPS]
    if not keep:
        keep = list(members)
    x = sub[keep].to_numpy()
    if len(x) < 2:
        cov = np.eye(len(keep))
    else:
        cov = np.cov(x, rowvar=False)
        if cov.ndim == 0:
            cov = np.array([[float(cov)]])
        # ridge for singular
        cov = cov + np.eye(len(keep)) * 1e-8
    return cov, keep


def _vol(cov: np.ndarray) -> np.ndarray:
    v = np.sqrt(np.clip(np.diag(cov), EPS, None))
    return np.maximum(v, EPS)


def weights_equal(n: int) -> np.ndarray:
    return np.ones(n) / n


def weights_inv_vol(cov: np.ndarray) -> np.ndarray:
    inv = 1.0 / _vol(cov)
    return inv / inv.sum()


def weights_risk_parity(cov: np.ndarray, *, iters: int = 500, tol: float = 1e-8) -> np.ndarray:
    """
    Long-only risk parity via iterative proportional update.
    Target: risk contribution_i ≈ 1/n.
    """
    n = cov.shape[0]
    w = weights_inv_vol(cov)
    for _ in range(iters):
        sig = float(np.sqrt(w @ cov @ w))
        if sig < EPS:
            return weights_equal(n)
        mrc = cov @ w  # marginal
        rc = w * mrc
        # target equal RC
        target = sig**2 / n
        # avoid div0
        adj = np.sqrt(np.clip(target / np.maximum(rc, EPS), 0.1, 10.0))
        w_new = w * adj
        w_new = np.maximum(w_new, EPS)
        w_new = w_new / w_new.sum()
        if np.max(np.abs(w_new - w)) < tol:
            w = w_new
            break
        w = w_new
    return w


def _corr_from_cov(cov: np.ndarray) -> np.ndarray:
    v = _vol(cov)
    d = np.outer(v, v)
    return cov / np.maximum(d, EPS)


def weights_hrp(cov: np.ndarray) -> np.ndarray:
    """Hierarchical Risk Parity (Lopez de Prado recursive bisection)."""
    n = cov.shape[0]
    if n == 1:
        return np.array([1.0])
    corr = np.clip(_corr_from_cov(cov), -1.0, 1.0)
    # distance
    dist = np.sqrt(0.5 * (1.0 - corr))
    np.fill_diagonal(dist, 0.0)
    # ensure symmetry
    dist = (dist + dist.T) / 2.0
    condensed = squareform(dist, checks=False)
    link = linkage(condensed, method="single")
    order = list(leaves_list(link))

    def _cluster_var(cov_s: np.ndarray, ix: list[int]) -> float:
        c = cov_s[np.ix_(ix, ix)]
        w = weights_inv_vol(c)
        return float(w @ c @ w)

    def _rec_bisect(ix: list[int]) -> np.ndarray:
        if len(ix) == 1:
            return np.array([1.0])
        # split by seriation: first half / second half of ordered subset
        # find split in linkage order
        sorted_ix = [i for i in order if i in ix]
        split = max(1, len(sorted_ix) // 2)
        left = sorted_ix[:split]
        right = sorted_ix[split:]
        if not right:
            right = [left.pop()]
        w_l = _rec_bisect(left)
        w_r = _rec_bisect(right)
        v_l = _cluster_var(cov, left)
        v_r = _cluster_var(cov, right)
        a = 1.0 - v_l / (v_l + v_r + EPS)
        w = np.zeros(len(ix))
        # map back to ix positions
        pos = {asset: j for j, asset in enumerate(ix)}
        for j, asset in enumerate(left):
            w[pos[asset]] = a * w_l[j]
        for j, asset in enumerate(right):
            w[pos[asset]] = (1.0 - a) * w_r[j]
        return w

    w_ord = _rec_bisect(list(range(n)))
    # _rec_bisect used indices 0..n-1 matching cov rows
    return w_ord / w_ord.sum()


SCHEMES = ("equal", "inv_vol", "risk_parity", "hrp")


def compute_weights(
    panel: pd.DataFrame,
    members: list[str],
    scheme: str,
) -> dict[str, Any]:
    cov, keep = _active_cov(panel, members)
    if scheme == "equal":
        w = weights_equal(len(keep))
    elif scheme == "inv_vol":
        w = weights_inv_vol(cov)
    elif scheme == "risk_parity":
        w = weights_risk_parity(cov)
    elif scheme == "hrp":
        w = weights_hrp(cov)
    else:
        raise ValueError(f"unknown scheme {scheme}")
    # map to full member list (zeros for inactive dropped)
    out = {m: 0.0 for m in members}
    for m, wi in zip(keep, w):
        out[m] = float(wi)
    # renormalize if some dropped
    s = sum(out.values())
    if s > EPS:
        out = {m: round(v / s, 6) for m, v in out.items()}
    return {"scheme": scheme, "weights": out, "assets_used": keep}


def portfolio_path(
    panel: pd.DataFrame,
    weights: dict[str, float],
) -> pd.Series:
    members = [m for m, w in weights.items() if w > EPS]
    if not members:
        return pd.Series(0.0, index=panel.index)
    w = np.array([weights[m] for m in members])
    x = panel.loc[:, members].to_numpy()
    return pd.Series(x @ w, index=panel.index, name="R_p")


def score_weighted(
    panel: pd.DataFrame,
    weights: dict[str, float],
) -> dict[str, Any]:
    rp = portfolio_path(panel, weights)
    s = rp.copy()
    s.index = pd.to_datetime(s.index)
    monthly = s.resample("ME").sum()
    monthly = monthly[monthly.abs() > 1e-12]
    quarterly = s.resample("QE").sum()
    quarterly = quarterly[quarterly.abs() > 1e-12]
    m_hit = float((monthly > 0).mean()) if len(monthly) else None
    q_hit = float((quarterly > 0).mean()) if len(quarterly) else None
    return {
        "sum_R": round(float(rp.sum()), 4),
        "mean_daily_R": round(float(rp.mean()), 6),
        "month_hit": None if m_hit is None else round(m_hit, 4),
        "n_months": int(len(monthly)),
        "quarter_hit": None if q_hit is None else round(q_hit, 4),
        "E_month": round(float(monthly.mean()), 4) if len(monthly) else None,
        "CVaR_m20": None if cvar(monthly) is None else round(cvar(monthly), 4),  # type: ignore
        "maxDD": round(max_drawdown(rp.cumsum()), 4),
        "worst_month": round(float(monthly.min()), 4) if len(monthly) else None,
        "best_month": round(float(monthly.max()), 4) if len(monthly) else None,
    }
