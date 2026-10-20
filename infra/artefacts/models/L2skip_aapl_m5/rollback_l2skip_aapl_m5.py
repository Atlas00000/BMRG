"""Rollback / pin control for AAPL M5 L2skip_aapl_m5 store.

Usage:
  python rollback_l2skip_aapl_m5.py status
  python rollback_l2skip_aapl_m5.py list
  python rollback_l2skip_aapl_m5.py rollback --to DISARM
  python rollback_l2skip_aapl_m5.py rollback --to L2skip_aapl_m5_p_prior_YYYYMMDD_HHMMSS
  python rollback_l2skip_aapl_m5.py drill
"""
from __future__ import annotations

import argparse
import json
import shutil
from datetime import datetime, timezone
from pathlib import Path

STORE = Path(__file__).resolve().parent
LATEST = STORE / "LATEST"
LOG = STORE / "ROLLBACK_LOG.jsonl"
PREFIX = "L2skip_aapl_m5_"
ARCHIVE_DRILL = (
    Path(__file__).resolve().parents[4]
    / "blotter"
    / "archive"
    / "AAPL-M5-AOS-P5"
    / "_drill"
)


def _utc() -> str:
    return datetime.now(timezone.utc).isoformat()


def _read_json(path: Path) -> dict:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def _append_log(event: dict) -> None:
    event = {"ts_utc": _utc(), **event}
    with LOG.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(event) + "\n")


def _versions() -> list[str]:
    return sorted(
        p.name for p in STORE.iterdir() if p.is_dir() and p.name.startswith(PREFIX)
    )


def status() -> dict:
    pin = _read_json(LATEST / "PIN.json")
    champ = _read_json(STORE / "CHAMP.json")
    chall = _read_json(STORE / "CHALLENGER.json")
    out = {
        "latest_pin": pin,
        "ai_champ": champ,
        "challenger": chall,
        "overlay_champ": "L2det_aapl_m5_v1b",
        "versions": _versions(),
    }
    print(json.dumps(out, indent=2))
    return out


def list_versions() -> None:
    for name in _versions():
        m = _read_json(STORE / name / "metrics.json")
        print(
            f"{name}  auc={m.get('auc_tip_oos')}  "
            f"best={(m.get('best_row') or {}).get('verdict')}"
        )


def _set_disarm(reason: str) -> dict:
    prev = _read_json(LATEST / "PIN.json")
    pin = {
        "semver": None,
        "mode": "DISARM",
        "role": "disarmed",
        "overlay_champ": "L2det_aapl_m5_v1b",
        "ai_champ": None,
        "updated_utc": _utc(),
        "disarm_reason": reason,
        "previous_semver": prev.get("semver"),
    }
    LATEST.mkdir(parents=True, exist_ok=True)
    (LATEST / "PIN.json").write_text(json.dumps(pin, indent=2), encoding="utf-8")
    (LATEST / "README.md").write_text(
        "# L2skip_aapl_m5 — DISARM\n\n"
        "AI pin cleared. Overlay champ `L2det_aapl_m5_v1b` unchanged.\n",
        encoding="utf-8",
    )
    _append_log({"action": "rollback_disarm", "from": prev, "to": pin})
    return pin


def _set_semver(semver: str, reason: str) -> dict:
    src = STORE / semver
    if not src.is_dir():
        raise SystemExit(f"unknown semver dir: {semver}")
    prev = _read_json(LATEST / "PIN.json")
    LATEST.mkdir(parents=True, exist_ok=True)
    for name in (
        "model.joblib",
        "metrics.json",
        "README.md",
        "META.json",
        "coef.npy",
        "intercept.npy",
        "scaler_mean.npy",
        "scaler_scale.npy",
    ):
        if (src / name).exists():
            shutil.copy2(src / name, LATEST / name)
    metrics = _read_json(src / "metrics.json")
    pin = {
        "semver": semver,
        "mode": "SHADOW_ONLY",
        "role": "shadow_artifact",
        "overlay_champ": "L2det_aapl_m5_v1b",
        "ai_champ": None,
        "updated_utc": _utc(),
        "restore_reason": reason,
        "previous_semver": prev.get("semver"),
        "auc_tip_oos": metrics.get("auc_tip_oos"),
        "best_verdict": (metrics.get("best_row") or {}).get("verdict"),
    }
    (LATEST / "PIN.json").write_text(json.dumps(pin, indent=2), encoding="utf-8")
    _append_log({"action": "rollback_to_semver", "from": prev, "to": pin})
    return pin


def rollback(to: str, reason: str) -> None:
    if to.upper() == "DISARM":
        pin = _set_disarm(reason)
    else:
        pin = _set_semver(to, reason)
    print(json.dumps(pin, indent=2))


def drill() -> None:
    """P5-T03: snapshot → DISARM → restore → report."""
    stamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    drill_dir = STORE / "_drill" / stamp
    drill_dir.mkdir(parents=True, exist_ok=True)
    ARCHIVE_DRILL.mkdir(parents=True, exist_ok=True)
    arch = ARCHIVE_DRILL / stamp
    arch.mkdir(parents=True, exist_ok=True)

    before = _read_json(LATEST / "PIN.json")
    for d in (drill_dir, arch):
        (d / "PIN_BEFORE.json").write_text(
            json.dumps(before, indent=2), encoding="utf-8"
        )

    mid = _set_disarm("P5-T03_rollback_drill")
    for d in (drill_dir, arch):
        (d / "PIN_DISARM.json").write_text(
            json.dumps(mid, indent=2), encoding="utf-8"
        )
    assert mid.get("mode") == "DISARM"

    target = before.get("semver") or before.get("previous_semver")
    versions = _versions()
    if not target and versions:
        target = versions[-1]
    if target:
        after = _set_semver(target, "P5-T03_rollback_drill_restore")
    else:
        after = _set_disarm("P5-T03_no_semver_to_restore")
    for d in (drill_dir, arch):
        (d / "PIN_AFTER.json").write_text(
            json.dumps(after, indent=2), encoding="utf-8"
        )

    report = {
        "task": "AAPL-M5-AOS-P5-T03",
        "drill_utc": _utc(),
        "steps": ["snapshot", "DISARM", "restore_shadow_pin"],
        "before": before,
        "disarm": mid,
        "after": after,
        "pass": after.get("mode") in ("SHADOW_ONLY", "DISARM")
        and mid.get("mode") == "DISARM",
        "note": (
            "EA research OS uses L2det_aapl_m5_v1b — AI pin rollback does not change "
            "InpAOS_AAPL_M5_L2detEnable. Kill-switch / AiOsMode still control L2 AI path."
        ),
        "ea_rollback_checklist": [
            "InpAiKillSwitch=true  OR  InpAiOsMode=OFF → L2 AI off",
            "InpAOS_AAPL_M5_L2detEnable=false → M5 det map off (engine only)",
            "InpAOS_Enable=false → full AOS off (Balanced M5 P0)",
            "Reload BMRG-M5-AAPL-6M-Balanced_TPgtSL.set",
        ],
    }
    for d in (drill_dir, arch):
        (d / "DRILL_REPORT.json").write_text(
            json.dumps(report, indent=2), encoding="utf-8"
        )
    _append_log({"action": "drill", "report_path": str(drill_dir)})
    print(json.dumps(report, indent=2))


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["status", "list", "rollback", "drill"])
    ap.add_argument("--to", default="DISARM")
    ap.add_argument("--reason", default="manual")
    args = ap.parse_args()
    if args.cmd == "status":
        status()
    elif args.cmd == "list":
        list_versions()
    elif args.cmd == "rollback":
        rollback(args.to, args.reason)
    else:
        drill()


if __name__ == "__main__":
    main()
