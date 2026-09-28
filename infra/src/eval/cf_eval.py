"""
Counterfactual blotter eval: remove WOULD_SKIP events, rescore vs engine baseline.

Shadow invariant: ledger decisions only; engine fire count unchanged in reality.
CF applies skips offline to measure protect-don't-overfilter bar.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import pandas as pd

SCORE = Path(__file__).resolve().parents[1] / "score"
sys.path.insert(0, str(SCORE))
from health import health_vector, load_baseline  # noqa: E402

INFRA = Path(__file__).resolve().parents[2]
FIXTURE = INFRA / "fixtures" / "blotter" / "harvest_long_v1"
PIN = INFRA / "artefacts" / "models" / "L2skip" / "LATEST_SHADOW" / "PIN.json"


def _load_jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def load_oos_skips(model_dir: Path) -> set[str]:
    ledger = pd.read_csv(model_dir / "shadow_ledger_oos.csv")
    return set(ledger.loc[ledger["decision"] == "WOULD_SKIP", "event_id"].astype(str))


def equity_path_and_maxdd(pairs: list[tuple[dict, dict]], start_equity: float = 400.0) -> dict:
    eq = start_equity
    peak = eq
    maxdd = 0.0
    path = []
    for m, leg in pairs:
        eq = round(eq + float(leg["pnl_net_ccy"]), 6)
        peak = max(peak, eq)
        dd = (peak - eq) / peak if peak > 0 else 0.0
        maxdd = max(maxdd, dd)
        path.append(eq)
    return {
        "final_equity": eq,
        "maxdd_frac": round(maxdd, 6),
        "maxdd_pp": round(100.0 * maxdd, 4),
        "n_path": len(path),
    }


def rolling_w250_ef(pairs: list[tuple[dict, dict]], leak_pp: float = 2.2, designed_rr: float = 1.0) -> dict:
    """Terminal W250 EF on chronological pairs (last 250 events)."""
    if len(pairs) < 100:
        return {"w250_ef_pp": None, "w250_n": len(pairs), "lifecycle": "thin"}
    window = pairs[-250:] if len(pairs) >= 250 else pairs
    manifests = [m for m, _ in window]
    legs = [leg for _, leg in window]
    # rebuild minimal for health_vector
    hv = health_vector(manifests, legs, leak_policy="baseline_proxy", designed_rr=designed_rr)
    # crude lifecycle vs prior 250 if available
    lifecycle = "Stable"
    if len(pairs) >= 500:
        prev = pairs[-500:-250]
        hv_prev = health_vector(
            [m for m, _ in prev],
            [leg for _, leg in prev],
            leak_policy="baseline_proxy",
            designed_rr=designed_rr,
        )
        delta = hv["ef_pp"] - hv_prev["ef_pp"]
        if hv["e_n"] <= 0:
            lifecycle = "Below frontier"
        elif hv["ef_pp"] <= (hv["m_pp"] or 0):
            lifecycle = "Near frontier" if hv["ef_pp"] > 0 else "Below frontier"
        elif delta <= -1.0:
            lifecycle = "Compressing"
        elif delta >= 1.0:
            lifecycle = "Expanding"
        else:
            lifecycle = "Stable"
    elif hv["e_n"] <= 0:
        lifecycle = "Below frontier"
    return {
        "w250_ef_pp": hv["ef_pp"],
        "w250_e_n": hv["e_n"],
        "w250_n": hv["n"],
        "lifecycle": lifecycle,
    }


def run_cf_eval(
    *,
    fixture_dir: Path = FIXTURE,
    model_dir: Path | None = None,
) -> dict:
    pin = json.loads(PIN.read_text(encoding="utf-8"))
    model_dir = Path(model_dir or pin["path"])
    skip_ids = load_oos_skips(model_dir)

    manifests = _load_jsonl(fixture_dir / "event_manifest.jsonl")
    legs = _load_jsonl(fixture_dir / "blotter_legs.jsonl")
    meta = json.loads((fixture_dir / "ea_metadata.json").read_text(encoding="utf-8"))
    designed_rr = meta.get("designed_rr", 1.0)

    # Chronological scoreable pairs
    by_leg = {leg["event_id"]: leg for leg in legs}
    pairs = []
    for m in manifests:
        if m.get("exit_reason") not in {"TP", "SL"}:
            continue
        leg = by_leg.get(m["event_id"])
        if not leg:
            continue
        pairs.append((m, leg))
    pairs.sort(key=lambda x: x[1]["entry_time"])

    engine_hv = health_vector(
        [m for m, _ in pairs],
        [leg for _, leg in pairs],
        leak_policy="baseline_proxy",
        designed_rr=designed_rr,
    )
    engine_dd = equity_path_and_maxdd(pairs)
    engine_w250 = rolling_w250_ef(pairs, designed_rr=designed_rr)

    # CF: drop WOULD_SKIP (OOS ledger). Train-prefix events without ledger stay.
    kept = [(m, leg) for m, leg in pairs if m["event_id"] not in skip_ids]
    skipped = [(m, leg) for m, leg in pairs if m["event_id"] in skip_ids]

    cf_hv = health_vector(
        [m for m, _ in kept],
        [leg for _, leg in kept],
        leak_policy="baseline_proxy",
        designed_rr=designed_rr,
    )
    cf_dd = equity_path_and_maxdd(kept)
    cf_w250 = rolling_w250_ef(kept, designed_rr=designed_rr)

    n_engine = len(pairs)
    n_cf = len(kept)
    fires_kept_pct = 100.0 * n_cf / max(n_engine, 1)
    skip_rate = 100.0 * len(skipped) / max(n_engine, 1)

    # Protect-don't-overfilter iteration bar vs engine replay (identity EF)
    baseline_doc = load_baseline()["windows"]["long"]
    ef_floor = engine_hv["ef_pp"] - 1.0
    maxdd_cap = (engine_dd["maxdd_pp"] or 0) + 2.0

    payoff_trap = (cf_hv["wr_pct"] > engine_hv["wr_pct"]) and (
        cf_hv["e_n"] < engine_hv["e_n"] or cf_hv["ef_pp"] < engine_hv["ef_pp"]
    )

    checks = {
        "n_remaining_ge_100": n_cf >= 100,
        "w250_ef_hold": (cf_w250["w250_ef_pp"] is not None)
        and (cf_w250["w250_ef_pp"] >= ef_floor - 0.01),
        "long_ef_hold": cf_hv["ef_pp"] >= ef_floor,
        "maxdd_ok": cf_dd["maxdd_pp"] <= maxdd_cap + 1e-6,
        "fires_ge_50pct": fires_kept_pct >= 50,
        "fires_ge_70pct": fires_kept_pct >= 70,
        "no_payoff_trap": not payoff_trap,
        "e_n_not_worse_unless_ef_up": not (
            cf_hv["e_n"] + 1e-9 < engine_hv["e_n"] and cf_hv["ef_pp"] + 1e-9 < engine_hv["ef_pp"]
        ),
    }
    accept = all(
        [
            checks["n_remaining_ge_100"],
            checks["long_ef_hold"],
            checks["maxdd_ok"],
            checks["fires_ge_50pct"],
            checks["no_payoff_trap"],
        ]
    )
    warn = []
    if not checks["fires_ge_70pct"]:
        warn.append("FREQUENCY_WARN_below_70pct")
    if not checks["fires_ge_50pct"]:
        warn.append("FREQUENCY_STALL")
    if n_cf < 385:
        warn.append("n_lt_385")

    report = {
        "task_id": "INF-P4-T04",
        "recipe": "INF-P4-T04_train_cfEval_L2shadow_vsBaseline",
        "model_semver": pin["shadow_semver"],
        "engine": {
            "health_vector": engine_hv,
            "maxdd_pp": engine_dd["maxdd_pp"],
            "w250": engine_w250,
            "n": n_engine,
        },
        "counterfactual": {
            "health_vector": cf_hv,
            "maxdd_pp": cf_dd["maxdd_pp"],
            "w250": cf_w250,
            "n": n_cf,
            "n_skipped": len(skipped),
            "skip_rate_pct": round(skip_rate, 4),
            "fires_kept_pct": round(fires_kept_pct, 4),
        },
        "deltas": {
            "n": n_cf - n_engine,
            "wr_pct": round(cf_hv["wr_pct"] - engine_hv["wr_pct"], 4),
            "bm_pp": round(cf_hv["bm_pp"] - engine_hv["bm_pp"], 4),
            "ef_pp": round(cf_hv["ef_pp"] - engine_hv["ef_pp"], 4),
            "e_n": round(cf_hv["e_n"] - engine_hv["e_n"], 6),
            "maxdd_pp": round(cf_dd["maxdd_pp"] - engine_dd["maxdd_pp"], 4),
        },
        "bars": {
            "ef_floor": ef_floor,
            "maxdd_cap": maxdd_cap,
            "engine_baseline_doc_ef": baseline_doc["ef_pp"],
        },
        "checks": checks,
        "warn": warn,
        "payoff_trap": payoff_trap,
        "verdict": "ACCEPT" if accept else "REJECT",
    }
    return report


if __name__ == "__main__":
    print(json.dumps(run_cf_eval(), indent=2))
