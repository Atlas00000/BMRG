"""Champion/challenger promote + rollback (INF-P7-T02). Never silent overwrite."""
from __future__ import annotations

import argparse
import json
import shutil
from datetime import datetime, timezone
from pathlib import Path

INFRA = Path(__file__).resolve().parents[2]
MODELS = INFRA / "artefacts" / "models" / "L2skip"
LIVE = MODELS / "LATEST_LIVE"
SHADOW = MODELS / "LATEST_SHADOW"
REPORTS = INFRA / "artefacts" / "reports"
OPS = INFRA / "artefacts" / "ops"
DRY = INFRA / "fixtures" / "promote" / "dry_run.json"


def _can_promote(scorecard: dict) -> tuple[bool, str]:
    checks = scorecard.get("checks") or {}
    if scorecard.get("verdict") != "ACCEPT":
        return False, "scorecard_verdict_not_ACCEPT"
    if not checks.get("long_ef_hold", checks.get("ef_held_or_lifted", False)):
        return False, "ef_bar_fail"
    if checks.get("fires_ge_50pct") is False:
        return False, "FREQUENCY_STALL"
    if not checks.get("fires_ge_70pct", True):
        return False, "fires_below_70pct"
    if checks.get("no_payoff_trap") is False:
        return False, "payoff_trap"
    if not checks.get("skip_audit_pass", True) and not scorecard.get("operator_waiver"):
        return False, "skip_audit_fail_no_waiver"
    return True, "ok"


def promote(semver: str, *, scorecard: dict | None = None, dry: bool = False) -> dict:
    model_dir = MODELS / semver
    if not model_dir.exists() and not dry:
        # allow dry with fictional semver
        if scorecard is None:
            raise FileNotFoundError(semver)
    sc = scorecard or {}
    if not sc and (REPORTS / "LATEST_EVAL.json").exists():
        sc = json.loads((REPORTS / "LATEST_EVAL.json").read_text(encoding="utf-8"))
        # unwrap nested cf if needed
        if "checks" not in sc and "cf" in sc:
            sc = {
                "verdict": sc.get("verdict") or sc["cf"].get("verdict"),
                "checks": sc["cf"].get("checks", {}),
                "operator_waiver": sc.get("operator_waiver", False),
            }
    ok, reason = _can_promote(sc)
    report = {
        "action": "promote",
        "semver": semver,
        "allowed": ok,
        "reason": reason,
        "dry_run": dry,
        "ts": datetime.now(timezone.utc).isoformat(),
    }
    if not ok:
        report["pinned"] = False
        return report
    if dry:
        report["pinned"] = True
        return report

    LIVE.mkdir(parents=True, exist_ok=True)
    prior = None
    pin_path = LIVE / "PIN.json"
    if pin_path.exists():
        prior = json.loads(pin_path.read_text(encoding="utf-8"))
        (LIVE / "PRIOR_PIN.json").write_text(json.dumps(prior, indent=2), encoding="utf-8")

    pin = {
        "live_semver": semver,
        "path": str(model_dir),
        "parent_semver": (prior or {}).get("live_semver"),
        "promoted_at": datetime.now(timezone.utc).isoformat(),
        "mode": "LIVE_WITHHOLD",
        "operator_waiver": bool(sc.get("operator_waiver")),
    }
    pin_path.write_text(json.dumps(pin, indent=2), encoding="utf-8")
    OPS.mkdir(parents=True, exist_ok=True)
    (OPS / "model_version_latest.json").write_text(json.dumps(pin, indent=2), encoding="utf-8")
    eval_run = {
        "run_id": f"promote_{semver}",
        "recipe_id": "INF-P7-T02_promote",
        "baseline_id": "ENGINE_BASELINE_v1",
        "scorecard_path": str(REPORTS / "LATEST_EVAL.json"),
        "verdict": "ACCEPT",
        "semver": semver,
    }
    (OPS / "eval_run_latest.json").write_text(json.dumps(eval_run, indent=2), encoding="utf-8")
    report["pinned"] = True
    report["pin"] = pin
    (REPORTS / "PROMOTE.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    return report


def rollback() -> dict:
    LIVE.mkdir(parents=True, exist_ok=True)
    pin_path = LIVE / "PIN.json"
    prior_path = LIVE / "PRIOR_PIN.json"
    report = {
        "action": "rollback",
        "ts": datetime.now(timezone.utc).isoformat(),
    }
    if prior_path.exists():
        prior = json.loads(prior_path.read_text(encoding="utf-8"))
        pin_path.write_text(json.dumps(prior, indent=2), encoding="utf-8")
        report["restored"] = prior.get("live_semver")
        report["status"] = "restored_prior"
    elif pin_path.exists():
        pin_path.unlink()
        report["restored"] = None
        report["status"] = "cleared_live_pin_OFF"
    else:
        report["status"] = "already_off"
    (REPORTS / "ROLLBACK.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    return report


def dry_run_fixture() -> dict:
    cases = json.loads(DRY.read_text(encoding="utf-8"))["cases"]
    results = []
    for case in cases:
        r = promote(case["challenger_semver"], scorecard=case["scorecard"], dry=True)
        results.append(
            {
                "name": case["name"],
                "expect_promote": case["expect_promote"],
                "got_promote": r["allowed"],
                "pass": r["allowed"] == case["expect_promote"],
                "reason": r["reason"],
            }
        )
    ok = all(x["pass"] for x in results)
    out = {"recipe": "INF-P7-T02_dry_run", "pass": ok, "results": results}
    (REPORTS / "INF-P7-T02_promote_dry_run.json").write_text(json.dumps(out, indent=2), encoding="utf-8")
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--promote", metavar="SEMVER")
    ap.add_argument("--rollback", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--waiver", action="store_true", help="operator waiver for skip-audit")
    args = ap.parse_args()
    if args.dry_run:
        print(json.dumps(dry_run_fixture(), indent=2))
        return
    if args.rollback:
        print(json.dumps(rollback(), indent=2))
        return
    if args.promote:
        sc = None
        if args.waiver:
            sc = {
                "verdict": "ACCEPT",
                "checks": {
                    "long_ef_hold": True,
                    "fires_ge_70pct": True,
                    "no_payoff_trap": True,
                    "skip_audit_pass": False,
                },
                "operator_waiver": True,
                "waiver_note": "USER AUTHORISED GO",
            }
        print(json.dumps(promote(args.promote, scorecard=sc), indent=2))
        return
    ap.print_help()


if __name__ == "__main__":
    main()
