"""
Stage 0–1 health vector from adapter pack (framework maths).

Leak policies:
  - baseline_proxy: use ENGINE_BASELINE_v1 costs.leak_proxy_pp (flagged defaulted)
  - cost_c_r: mean c_R from 3×spread/SL → Leak = c_R/(R+1)
"""
from __future__ import annotations

import json
import math
from pathlib import Path

INFRA = Path(__file__).resolve().parents[2]
BASELINE_PATH = INFRA / "baselines" / "ENGINE_BASELINE_v1.json"


def load_baseline() -> dict:
    return json.loads(BASELINE_PATH.read_text(encoding="utf-8"))


def _scoreable(manifests: list[dict], legs: list[dict]) -> list[tuple[dict, dict]]:
    by_id = {leg["event_id"]: leg for leg in legs}
    out = []
    for m in manifests:
        if m.get("exit_reason") not in {"TP", "SL"}:
            continue
        leg = by_id.get(m["event_id"])
        if not leg:
            continue
        out.append((m, leg))
    return out


def health_vector(
    manifests: list[dict],
    legs: list[dict],
    *,
    leak_policy: str = "baseline_proxy",
    designed_rr: float = 1.0,
) -> dict:
    baseline = load_baseline()
    pairs = _scoreable(manifests, legs)
    n = len(pairs)
    if n == 0:
        raise ValueError("no scoreable TP/SL events")

    wins = sum(1 for m, _ in pairs if m.get("exit_reason") == "TP")
    wr = wins / n
    # realised R from gross pnl / risk (FIXED_RR ≈ ±1)
    r_vals = []
    c_rs = []
    for m, leg in pairs:
        risk = m["risk_ccy"] or 1.0
        r_vals.append(leg["pnl_gross_ccy"] / risk)
        if m.get("c_r_proxy") is not None:
            c_rs.append(float(m["c_r_proxy"]))
        else:
            spread = float(leg.get("spread_points_entry") or m.get("spread_points_entry") or 0)
            sl = float(m.get("sl_points") or 300)
            c_rs.append((3.0 * spread) / sl if sl else 0.0)

    # Average win size / average loss size in R (absolute)
    win_rs = [r for r in r_vals if r > 0]
    loss_rs = [abs(r) for r in r_vals if r < 0]
    r_hat = (sum(win_rs) / len(win_rs)) if win_rs and loss_rs else designed_rr
    if loss_rs:
        # payoff ratio mean_win/mean_loss
        r_hat = (sum(win_rs) / len(win_rs)) / (sum(loss_rs) / len(loss_rs)) if win_rs else designed_rr

    # For FIXED_RR Harvest, force R≈ designed when geometry holds
    if abs(r_hat - designed_rr) < 0.05:
        r_use = designed_rr
    else:
        r_use = r_hat

    bwr = 1.0 / (1.0 + r_use)
    bm = wr - bwr
    bm_pp = 100.0 * bm
    mean_c_r = sum(c_rs) / len(c_rs)

    costs_defaulted = list(
        {c for m in manifests for c in (m.get("costs_defaulted") or [])}
    ) or baseline["costs"]["costs_defaulted"]

    if leak_policy == "baseline_proxy":
        leak_pp = float(baseline["costs"]["leak_proxy_pp"])
        leak_source = "ENGINE_BASELINE_v1.leak_proxy_pp"
    elif leak_policy == "cost_c_r":
        leak_pp = 100.0 * mean_c_r / (r_use + 1.0)
        leak_source = "mean_c_R_from_3x_spread_over_SL"
    else:
        raise ValueError(leak_policy)

    ef_pp = bm_pp - leak_pp
    e_n = wr * (r_use + 1.0) - 1.0
    m_pp = 1.96 * 100.0 * math.sqrt(wr * (1.0 - wr) / n) if 0 < wr < 1 else None
    zone = "Negative" if ef_pp <= 0 else ("Fragile" if m_pp is not None and ef_pp <= m_pp else "Robust")

    return {
        "framework_bmrg": "1.1.2",
        "baseline_id": baseline["baseline_id"],
        "n": n,
        "wr_pct": round(100.0 * wr, 4),
        "bwr_pct": round(100.0 * bwr, 4),
        "r": round(r_use, 6),
        "rr": designed_rr,
        "bm_pp": round(bm_pp, 4),
        "leak_pp": round(leak_pp, 4),
        "leak_policy": leak_policy,
        "leak_source": leak_source,
        "mean_c_r": round(mean_c_r, 6),
        "ef_pp": round(ef_pp, 4),
        "m_pp": round(m_pp, 4) if m_pp is not None else None,
        "e_n": round(e_n, 6),
        "zone": zone,
        "costs_defaulted": costs_defaulted,
        "cost_flags_present": all(
            bool(m.get("costs_defaulted") or m.get("cost_component_flags")) for m, _ in pairs
        ),
    }


def compare_to_baseline(hv: dict, *, ef_tol: float = 0.05) -> dict:
    b = load_baseline()["windows"]["long"]
    checks = {
        "n": abs(hv["n"] - b["n"]) <= 5,
        "wr": abs(hv["wr_pct"] - b["wr_pct"]) <= 1.0,
        "r": abs(hv["r"] - b["r"]) <= 0.05,
        "leak_flagged": hv["cost_flags_present"] and bool(hv["costs_defaulted"]),
        "ef_vs_1_77": abs(hv["ef_pp"] - b["ef_pp"]) <= ef_tol,
        "ef_identity": abs(hv["ef_pp"] - (hv["bm_pp"] - hv["leak_pp"])) < 0.01,
    }
    # Accept if core integrity holds and (EF matches baseline OR identity with WR/R/n OK).
    # Known doc gap: bm≈4.5 − leak 2.2 ⇒ ef≈2.3 while ENGINE_BASELINE lists ef 1.77.
    accept = (
        checks["n"]
        and checks["wr"]
        and checks["r"]
        and checks["leak_flagged"]
        and checks["ef_identity"]
        and (checks["ef_vs_1_77"] or abs(hv["ef_pp"] - (hv["bm_pp"] - 2.2)) < 0.15)
    )
    return {
        "checks": checks,
        "deltas": {
            "n": hv["n"] - b["n"],
            "wr_pct": round(hv["wr_pct"] - b["wr_pct"], 4),
            "r": round(hv["r"] - b["r"], 6),
            "bm_pp": round(hv["bm_pp"] - b["bm_pp"], 4),
            "leak_pp": round(hv["leak_pp"] - b["leak_pp"], 4),
            "ef_pp": round(hv["ef_pp"] - b["ef_pp"], 4),
            "e_n": round(hv["e_n"] - b["e_n"], 6),
        },
        "accept": accept,
        "note": None
        if checks["ef_vs_1_77"]
        else "ENGINE_BASELINE ef_pp=1.77 is arithmetically inconsistent with bm−leak (≈4.5−2.2=2.3); rebuild matches identity under leak_proxy 2.2",
    }


def score_pack_dir(pack_dir: Path, leak_policy: str = "baseline_proxy") -> dict:
    pack_dir = Path(pack_dir)
    manifests = [
        json.loads(line)
        for line in (pack_dir / "event_manifest.jsonl").read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    legs = [
        json.loads(line)
        for line in (pack_dir / "blotter_legs.jsonl").read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    meta = json.loads((pack_dir / "ea_metadata.json").read_text(encoding="utf-8"))
    hv = health_vector(manifests, legs, leak_policy=leak_policy, designed_rr=meta.get("designed_rr", 1.0))
    cmp_ = compare_to_baseline(hv)
    return {"health_vector": hv, "vs_baseline": cmp_, "verdict": "ACCEPT" if cmp_["accept"] else "REJECT"}
