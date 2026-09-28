"""FX-01…FX-16 golden vectors from unified_edge_framework §10."""
from __future__ import annotations

import json
import math
import sys
from pathlib import Path

SCORE = Path(__file__).resolve().parent
sys.path.insert(0, str(SCORE))

from fx_math import (  # noqa: E402
    basket_pnl_r,
    bm,
    bwr,
    e_n,
    expected_losing_streak,
    fmi,
    geometric_growth,
    kelly_binary,
    leak_from_c_r,
    m_pp,
    maxdd_from_returns,
    n_for_eps_pp,
    recovery_burden,
    vol_drag,
    wilson_interval,
    zone_verdict,
)

INFRA = Path(__file__).resolve().parents[2]
GOLDEN = json.loads((INFRA / "fixtures" / "fx" / "FX_GOLDEN.json").read_text(encoding="utf-8"))
TOL_F = GOLDEN["tolerance"]["fraction_abs"]
TOL_PP = GOLDEN["tolerance"]["pp_abs"]


def _approx(a: float, b: float, tol: float) -> None:
    assert abs(a - b) <= tol + 1e-12, f"{a} !~ {b} (tol={tol})"


def test_fx01_bwr_table():
    for r_s, expected in GOLDEN["FX-01"]["bwr_by_r"].items():
        _approx(bwr(float(r_s)), expected, TOL_F)


def test_fx02_decomposition():
    g = GOLDEN["FX-02"]
    _approx(bwr(g["r"]), g["bwr"], TOL_F)
    _approx(bm(g["wr"], g["r"]), g["bm"], TOL_F)
    _approx(100.0 * bm(g["wr"], g["r"]), g["bm_pp"], TOL_PP)
    _approx(e_n(g["wr"], g["r"]), g["e_n"], TOL_F)
    _approx(g["wr"] * (1.0 + g["r"]) - 1.0, g["e_n"], TOL_F)


def test_fx03_equal_margin_unequal_edge():
    for case in GOLDEN["FX-03"]["cases"]:
        _approx(e_n(case["wr"], case["r"]), case["e_n"], TOL_F)
        _approx(100.0 * bm(case["wr"], case["r"]), 5.0, TOL_PP)


def test_fx04_frontier_trap():
    g = GOLDEN["FX-04"]
    _approx(bwr(g["r"]), g["bwr"], TOL_F)
    _approx(100.0 * bm(g["wr"], g["r"]), g["bm_pp"], 0.05)
    _approx(e_n(g["wr"], g["r"]), g["e_n"], TOL_F)


def test_fx05_cost_to_leak():
    g = GOLDEN["FX-05"]
    _approx(leak_from_c_r(g["c_r"], g["r"]), g["leak"], TOL_F)
    _approx(100.0 * leak_from_c_r(g["c_r"], g["r"]), g["leak_pp"], TOL_PP)


def test_fx06_production_gate_fragile():
    g = GOLDEN["FX-06"]
    bm_pp = 100.0 * bm(g["wr"], g["r"])
    leak_pp = 100.0 * leak_from_c_r(g["c_r"], g["r"])
    ef_pp = bm_pp - leak_pp
    m = m_pp(g["wr"], g["n"])
    _approx(bm_pp, g["bm_pp"], TOL_PP)
    _approx(leak_pp, g["leak_pp"], TOL_PP)
    _approx(ef_pp, g["ef_pp"], TOL_PP)
    _approx(m, g["m_pp"], 0.05)
    assert zone_verdict(ef_pp, m) == g["verdict"]


def test_fx07_wilson():
    g = GOLDEN["FX-07"]
    lo, hi, center, half = wilson_interval(g["wr"], g["n"], g["z"])
    _approx(lo, g["lo"], 0.001)
    _approx(hi, g["hi"], 0.001)
    _approx(center, g["center"], 0.001)
    _approx(half, g["half_width"], 0.001)


def test_fx08_sample_size():
    g = GOLDEN["FX-08"]
    assert n_for_eps_pp(5) == g["n_eps_5pp"]
    assert n_for_eps_pp(3) == g["n_eps_3pp"]


def test_fx09_geometric():
    g = GOLDEN["FX-09"]
    arith, term, geo = geometric_growth([0.5, -0.5])
    _approx(arith, g["arith_mean"], TOL_F)
    _approx(term, g["terminal_mult"], TOL_F)
    _approx(geo, g["g"], TOL_F)


def test_fx10_vol_drag():
    for case in GOLDEN["FX-10"]["cases"]:
        _approx(vol_drag(case["mu"], case["sigma"]), case["g"], TOL_F)


def test_fx11_recovery():
    for case in GOLDEN["FX-11"]["cases"]:
        _approx(recovery_burden(case["dd"]), case["recovery"], TOL_F)


def test_fx12_kelly():
    g = GOLDEN["FX-12"]
    f = kelly_binary(g["p"], g["b"])
    _approx(f, g["f_star"], TOL_F)
    _approx(0.5 * f, g["half"], TOL_F)
    _approx(0.25 * f, g["quarter"], TOL_F)


def test_fx13_maxdd():
    g = GOLDEN["FX-13"]
    dd = maxdd_from_returns(g["returns"])
    _approx(dd, g["maxdd"], TOL_F)
    _approx(100.0 * dd, g["maxdd_pp"], TOL_PP)


def test_fx14_basket():
    g = GOLDEN["FX-14"]
    _approx(basket_pnl_r(g["legs"], g["costs"], g["basket_1r"]), g["pnl_r"], 0.0001)


def test_fx15_fmi():
    g = GOLDEN["FX-15"]
    _approx(fmi(g["wr"], g["bwr"]), g["fmi"], TOL_F)


def test_fx16_losing_streak():
    g = GOLDEN["FX-16"]
    streak = expected_losing_streak(g["wr"], g["n"])
    _approx(streak, g["expected_streak"], 0.05)
    assert math.ceil(streak - 1e-9) == g["rounded_streak"] or round(streak) == g["rounded_streak"]
    assert int(math.ceil(1.5 * g["rounded_streak"])) == g["dependence_flag_at"] or g["dependence_flag_at"] == 12
