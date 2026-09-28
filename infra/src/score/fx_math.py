"""Unified Edge Framework §10 numeric helpers (FX-01…FX-16)."""
from __future__ import annotations

import math


def bwr(r: float) -> float:
    return 1.0 / (1.0 + r)


def bm(wr: float, r: float) -> float:
    return wr - bwr(r)


def e_n(wr: float, r: float) -> float:
    return wr * (1.0 + r) - 1.0


def leak_from_c_r(c_r: float, r: float) -> float:
    return c_r / (1.0 + r)


def m_pp(wr: float, n: int, z: float = 1.96) -> float:
    """Normal approx margin half-width in percentage points."""
    return 100.0 * z * math.sqrt(wr * (1.0 - wr) / n)


def zone_verdict(ef_pp: float, m_pp_val: float) -> str:
    if ef_pp <= 0:
        return "BELOW_FRONTIER"
    if ef_pp < m_pp_val:
        return "FRAGILE"
    return "ROBUST"


def wilson_interval(wr: float, n: int, z: float = 1.96) -> tuple[float, float, float, float]:
    """Return (lo, hi, center, half_width)."""
    phat = wr
    z2 = z * z
    denom = 1.0 + z2 / n
    center = (phat + z2 / (2 * n)) / denom
    half = (z / denom) * math.sqrt(phat * (1 - phat) / n + z2 / (4 * n * n))
    return center - half, center + half, center, half


def n_for_eps_pp(eps_pp: float) -> int:
    """n ≥ 3.8416 * 0.25 / ε² with ε as fraction."""
    eps = eps_pp / 100.0
    return int(math.ceil(3.8416 * 0.25 / (eps * eps)))


def geometric_growth(returns: list[float]) -> tuple[float, float, float]:
    """arith mean, terminal mult, G per period."""
    n = len(returns)
    arith = sum(returns) / n
    term = 1.0
    for r in returns:
        term *= 1.0 + r
    g = term ** (1.0 / n) - 1.0
    return arith, term, g


def vol_drag(mu: float, sigma: float) -> float:
    return mu - 0.5 * sigma * sigma


def recovery_burden(dd: float) -> float:
    return dd / (1.0 - dd)


def kelly_binary(p: float, b: float) -> float:
    return (p * (b + 1.0) - 1.0) / b


def maxdd_from_returns(returns: list[float], start: float = 1.0) -> float:
    eq = start
    peak = eq
    maxdd = 0.0
    for r in returns:
        eq *= 1.0 + r
        peak = max(peak, eq)
        maxdd = max(maxdd, 1.0 - eq / peak)
    return maxdd


def basket_pnl_r(legs: list[float], costs: float, basket_1r: float) -> float:
    return (sum(legs) - costs) / basket_1r


def fmi(wr: float, bwr_val: float) -> float:
    return (wr - bwr_val) / bwr_val


def expected_losing_streak(wr: float, n: int) -> float:
    return math.log(n) / math.log(1.0 / (1.0 - wr))
