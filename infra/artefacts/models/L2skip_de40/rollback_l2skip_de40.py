"""Rollback / pin control for DE40 L2skip_de40 store.

Usage:
  python rollback_l2skip_de40.py status
  python rollback_l2skip_de40.py list
  python rollback_l2skip_de40.py rollback --to DISARM
  python rollback_l2skip_de40.py rollback --to L2skip_de40_p_pretip_YYYYMMDD_HHMMSS
  python rollback_l2skip_de40.py drill
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
PREFIX = "L2skip_de40_"
OVERLAY = "L2det_de40_v1_BUY_near_atr"


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
        "overlay_champ": OVERLAY,
        "overlay_mqh": False,
        "versions": _versions(),
    }
    print(json.dumps(out, indent=2))
    return out


def list_versions() -> None:
    for name in _versions():
        m = _read_json(STORE / name / "metrics.json")
        chrono = ((m.get("chrono_holdout") or {}).get("report") or {}).get("verdict")
        print(
            f"{name}  auc={m.get('auc_tip_oos')}  "
            f"best={(m.get('best_row') or {}).get('verdict')}  chrono={chrono}"
        )


def _set_disarm(reason: str) -> dict:
    prev = _read_json(LATEST / "PIN.json")
    pin = {
        "semver": None,
        "mode": "DISARM",
        "role": "disarmed",
        "overlay_champ": OVERLAY,
        "ai_champ": None,
        "updated_utc": _utc(),
        "disarm_reason": reason,
        "previous_semver": prev.get("semver"),
    }
    LATEST.mkdir(parents=True, exist_ok=True)
    (LATEST / "PIN.json").write_text(json.dumps(pin, indent=2), encoding="utf-8")
    (LATEST / "README.md").write_text(
        f"# L2skip_de40 — DISARM\n\n"
        f"AI pin cleared. Overlay champ `{OVERLAY}` unchanged (offline CF).\n",
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
    for name in ("model.joblib", "metrics.json", "README.md", "META.json"):
        if (src / name).exists():
            shutil.copy2(src / name, LATEST / name)
    metrics = _read_json(src / "metrics.json")
    pin = {
        "semver": semver,
        "mode": "SHADOW_ONLY",
        "role": "shadow_artifact",
        "overlay_champ": OVERLAY,
        "ai_champ": None,
        "updated_utc": _utc(),
        "restore_reason": reason,
        "previous_semver": prev.get("semver"),
        "auc_tip_oos": metrics.get("auc_tip_oos"),
        "best_verdict": (metrics.get("best_row") or {}).get("verdict"),
        "chrono_holdout_verdict": (
            (metrics.get("chrono_holdout") or {}).get("report") or {}
        ).get("verdict"),
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
    drill_dir = STORE / "_drill" / datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    drill_dir.mkdir(parents=True, exist_ok=True)
    before = _read_json(LATEST / "PIN.json")
    (drill_dir / "PIN_BEFORE.json").write_text(
        json.dumps(before, indent=2), encoding="utf-8"
    )

    mid = _set_disarm("P5-T03_rollback_drill")
    (drill_dir / "PIN_DISARM.json").write_text(
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
    (drill_dir / "PIN_AFTER.json").write_text(
        json.dumps(after, indent=2), encoding="utf-8"
    )

    blotter_drill = (
        STORE.parents[3]
        / "blotter"
        / "archive"
        / "DE40-AOS-P5"
        / "_drill"
        / drill_dir.name
    )
    blotter_drill.mkdir(parents=True, exist_ok=True)
    for name in ("PIN_BEFORE.json", "PIN_DISARM.json", "PIN_AFTER.json"):
        shutil.copy2(drill_dir / name, blotter_drill / name)

    report = {
        "task": "DE40-AOS-P5-T03",
        "drill_utc": _utc(),
        "steps": ["snapshot", "DISARM", "restore_shadow_pin"],
        "before": before,
        "disarm": mid,
        "after": after,
        "pass": after.get("mode") in ("SHADOW_ONLY", "DISARM")
        and mid.get("mode") == "DISARM",
        "note": (
            f"Overlay champ `{OVERLAY}` is offline CF only (no AOS_L2det_de.mqh). "
            "AI pin rollback does not change engine geometry. "
            "Research P4 .set uses L3/L4/ledger with AiOsMode=OFF."
        ),
        "ea_rollback_checklist": [
            "InpAiKillSwitch=true  OR  InpAiOsMode=OFF → L2 AI off",
            "Foreign L2det maps stay false (EUR/UK/AUD/AAPL)",
            "InpAOS_Enable=false → full AOS off (Balanced P0 engine)",
            "Reload Presets/BMRG-M15-DE40-6M-P0_balanced_chart.set",
        ],
    }
    (drill_dir / "DRILL_REPORT.json").write_text(
        json.dumps(report, indent=2), encoding="utf-8"
    )
    (blotter_drill / "DRILL_REPORT.json").write_text(
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
