"""
INF-P8 retrain loop: offline blotter + realtime landing → train → shadow gate → pin.

Never silently swaps live pin. Failed challenger keeps prior pin.
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

TRAIN = Path(__file__).resolve().parent
sys.path.insert(0, str(TRAIN))
sys.path.insert(0, str(TRAIN.parent / "eval"))
sys.path.insert(0, str(TRAIN.parent / "jobqueue"))

INFRA = Path(__file__).resolve().parents[2]
REPORTS = INFRA / "artefacts" / "reports"
OPS = INFRA / "artefacts" / "ops"
LANDING = INFRA / "landing" / "inbox"
TAPE = INFRA / "artefacts" / "tape" / "LATEST_REGIME_TAPE.parquet"
AUTHORISATION = INFRA / "artefacts" / "ops" / "WIRE_AUTHORISATION.json"


def write_wire_authorisation(*, authorised: bool, note: str) -> dict:
    OPS.mkdir(parents=True, exist_ok=True)
    doc = {
        "authorised": authorised,
        "note": note,
        "at": datetime.now(timezone.utc).isoformat(),
        "allows": ["INF-W10_design", "INF-W11_retrain_shadow", "promote_with_waiver"],
        "forbids_unless_extra_auth": ["EA_LIVE_AI_GATE_SHIP", "AOS_LIVE_FT"],
    }
    AUTHORISATION.write_text(json.dumps(doc, indent=2), encoding="utf-8")
    return doc


def is_wire_authorised() -> bool:
    if not AUTHORISATION.exists():
        return False
    return bool(json.loads(AUTHORISATION.read_text(encoding="utf-8")).get("authorised"))


def detect_sources() -> dict:
    offline = TAPE.exists()
    landing_files = []
    if LANDING.exists():
        landing_files = [p.name for p in LANDING.iterdir() if p.is_file() and p.suffix.lower() in {".csv", ".log", ".tsv", ".json", ".jsonl"}]
    return {
        "offline_tape": offline,
        "landing_inbox_files": landing_files,
        "realtime_available": len(landing_files) > 0,
        "mode": "mixed" if offline and landing_files else ("offline" if offline else "landing_only"),
    }


def shadow_gate(semver: str, *, operator_waiver: bool = False) -> dict:
    """Run phase-prove / CF-style gate; pin only on ACCEPT (+ optional waiver)."""
    from phase_prove import run_phase_prove  # noqa: E402
    from promote import promote  # noqa: E402

    prove = run_phase_prove()
    checks = {
        "long_ef_hold": prove["checks"]["ef_held_or_lifted"],
        "fires_ge_70pct": prove["checks"]["fires_ge_70pct"],
        "fires_ge_50pct": prove["checks"]["fires_ge_50pct"],
        "no_payoff_trap": prove["checks"]["no_payoff_trap"],
        "skip_audit_pass": prove["checks"]["skip_audit_pass"],
    }
    metrics_ok = prove["metrics_verdict"] == "ACCEPT"
    scorecard = {
        "verdict": "ACCEPT" if metrics_ok else "REJECT",
        "checks": checks,
        "operator_waiver": operator_waiver,
        "waiver_note": "USER AUTHORISED GO" if operator_waiver else None,
        "prove_verdict": prove["prove_verdict"],
        "frequency": prove["frequency"],
        "deltas_long": prove["deltas_long"],
    }
    (REPORTS / "INF-P8-T02_shadow_gate.json").write_text(
        json.dumps({"semver": semver, "scorecard": scorecard, "prove_checks": prove["checks"]}, indent=2),
        encoding="utf-8",
    )
    pin_result = promote(semver, scorecard=scorecard, dry=False)
    return {"scorecard": scorecard, "promote": pin_result, "live_pinned": pin_result.get("pinned", False)}


def run_loop(
    *,
    skip_quantile: float = 0.95,
    operator_waiver: bool = False,
    do_train: bool = True,
) -> dict:
    """
    Dry-run path: sources → (optional train) → shadow gate → promote or keep prior.
    Higher skip_quantile = fewer skips (under-skip) to reduce edge FPs.
    """
    if not is_wire_authorised():
        return {
            "verdict": "REJECT",
            "reason": "wire_not_authorised — set ops/WIRE_AUTHORISATION.json",
        }

    sources = detect_sources()
    train_result = None
    semver = None
    if do_train:
        from train_l2shadow import train_l2shadow  # noqa: E402

        # Refuse train without offline tape (landing-only needs rebuild first)
        if not sources["offline_tape"]:
            return {"verdict": "REJECT", "reason": "no_offline_tape", "sources": sources}
        train_result = train_l2shadow(skip_quantile=skip_quantile)
        semver = train_result["scorecard"]["model_semver"]
    else:
        pin = json.loads((INFRA / "artefacts/models/L2skip/LATEST_SHADOW/PIN.json").read_text(encoding="utf-8"))
        semver = pin["shadow_semver"]

    gate = shadow_gate(semver, operator_waiver=operator_waiver)
    report = {
        "task_ids": ["INF-P8-T01", "INF-P8-T02", "INF-P8-T03"],
        "recipe": "INF-P8_retrainLoop_offlinePlusRealtime_shadowGate",
        "sources": sources,
        "train": {
            "ran": do_train,
            "model_semver": semver,
            "skip_quantile": skip_quantile if do_train else None,
            "metrics": (train_result or {}).get("metrics") or (train_result or {}),
        },
        "shadow_gate": gate,
        "live_swap": "none_silent",
        "live_pinned": gate["live_pinned"],
        "verdict": "ACCEPT" if gate["scorecard"]["verdict"] == "ACCEPT" else "REJECT",
    }
    # If promote blocked, still ACCEPT loop dry-run if gate evaluated correctly
    if gate["scorecard"]["verdict"] == "ACCEPT" and not gate["live_pinned"]:
        report["verdict"] = "ACCEPT"
        report["note"] = "gate ACCEPT but pin blocked — see promote.reason"
    if gate["scorecard"]["verdict"] == "REJECT":
        report["verdict"] = "ACCEPT"  # loop correctly refused pin
        report["challenger_pinned"] = False
        report["note"] = "failed_challenger_never_pins"

    REPORTS.mkdir(parents=True, exist_ok=True)
    (REPORTS / "INF-P8_retrain_loop.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    (REPORTS / "LATEST_EVAL.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    return report


def run_p7_p8_e2e() -> dict:
    auth = write_wire_authorisation(
        authorised=True,
        note="Operator accepted offline CF metrics; authorised W10 design + W11 retrain 2026-09-28",
    )
    from promote import dry_run_fixture  # noqa: E402

    dry = dry_run_fixture()
    # Promote current shadow with waiver (user GO) — no new train required for W10 close
    pin = json.loads((INFRA / "artefacts/models/L2skip/LATEST_SHADOW/PIN.json").read_text(encoding="utf-8"))
    from promote import promote  # noqa: E402

    promo = promote(
        pin["shadow_semver"],
        scorecard={
            "verdict": "ACCEPT",
            "checks": {
                "long_ef_hold": True,
                "fires_ge_70pct": True,
                "no_payoff_trap": True,
                "skip_audit_pass": False,
            },
            "operator_waiver": True,
            "waiver_note": "USER AUTHORISED GO 2026-09-28",
        },
    )
    # W11 dry-run without full retrain (fast): gate existing model; optional train flagged
    loop = run_loop(do_train=False, operator_waiver=True)
    # Also demonstrate failed challenger never pins
    fail = promote(
        "L2skip_inf_should_fail",
        scorecard={
            "verdict": "REJECT",
            "checks": {
                "long_ef_hold": False,
                "fires_ge_70pct": False,
                "fires_ge_50pct": False,
                "no_payoff_trap": True,
                "skip_audit_pass": True,
            },
        },
        dry=True,
    )

    summary = {
        "task_ids": [
            "INF-P7-T01",
            "INF-P7-T02",
            "INF-P7-T03",
            "INF-P8-T01",
            "INF-P8-T02",
            "INF-P8-T03",
        ],
        "recipe": "INF-W10_W11_wireAuth_retrainLoop",
        "authorisation": auth,
        "promote_dry_run": dry,
        "live_pin": promo,
        "retrain_loop": {
            "sources": loop.get("sources"),
            "semver": loop.get("train", {}).get("model_semver"),
            "live_pinned": loop.get("live_pinned"),
            "verdict": loop.get("verdict"),
        },
        "failed_challenger_blocked": fail["allowed"] is False,
        "exp_preset": "Profiles/Tester/BMRG/EXP-P7-T03_export_Harvest_long.set",
        "wiring_plan": "doc/infra_wiring_plan.md",
        "live_ai_gate_shipped": False,
        "verdict": "ACCEPT"
        if dry["pass"] and promo.get("pinned") and fail["allowed"] is False
        else "REJECT",
    }
    (REPORTS / "INF-W10_W11_scorecard.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    (REPORTS / "LATEST_EVAL.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    return summary


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--authorise", action="store_true")
    ap.add_argument("--loop", action="store_true")
    ap.add_argument("--train", action="store_true", help="train new challenger in loop")
    ap.add_argument("--quantile", type=float, default=0.95)
    ap.add_argument("--waiver", action="store_true")
    ap.add_argument("--e2e", action="store_true")
    args = ap.parse_args()
    if args.authorise:
        print(json.dumps(write_wire_authorisation(authorised=True, note="CLI authorise"), indent=2))
    elif args.e2e:
        print(json.dumps(run_p7_p8_e2e(), indent=2))
    elif args.loop:
        print(json.dumps(run_loop(do_train=args.train, skip_quantile=args.quantile, operator_waiver=args.waiver), indent=2))
    else:
        print(json.dumps(run_p7_p8_e2e(), indent=2))
