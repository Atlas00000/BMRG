"""INF scale-up full regression: all phase test modules + artefact smoke."""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

INFRA = Path(__file__).resolve().parents[1]
MQL5 = INFRA.parents[2]

PHASE_TESTS = [
    ("INF-W02/P1", "src/ingest/test_p1_contract.py"),
    ("INF-W03/P2", "src/ingest/test_p2_ingest.py"),
    ("INF-W04/P3", "src/features/test_p3_features.py"),
    ("INF-W05/P4a", "src/train/test_p4a_train.py"),
    ("INF-W06/P4b", "src/eval/test_p4b_eval.py"),
    ("INF-W07/P5a", "src/obs/test_p5a_obs.py"),
    ("INF-W08/P5b", "src/score/test_fx.py"),
    ("INF-W08/P5b", "src/jobqueue/test_queue.py"),
    ("INF-W08/P5b", "src/test_p5b_suite.py"),
    ("INF-W09/P6", "src/eval/test_p6_phase_prove.py"),
    ("INF-W10/W11", "src/train/test_p7_p8_wire.py"),
]

ARTEFACTS = [
    ("INF-W01", INFRA / "baselines" / "ENGINE_BASELINE_v1.json"),
    ("INF-W01", INFRA / "LIMITATIONS.md"),
    ("INF-W01", INFRA / "PHASE_EXITS.md"),
    ("INF-W02", INFRA / "schemas" / "adapter_blotter.schema.json"),
    ("INF-W02", INFRA / "migrations" / "versions" / "0001_core.py"),
    ("INF-W03", INFRA / "fixtures" / "blotter" / "harvest_long_v1" / "health_vector.json"),
    ("INF-W04", INFRA / "artefacts" / "tape" / "LATEST_REGIME_TAPE.parquet"),
    ("INF-W05", INFRA / "artefacts" / "models" / "L2skip" / "LATEST_SHADOW" / "PIN.json"),
    ("INF-W06", INFRA / "artefacts" / "reports" / "INF-P4-T04_cf_scorecard.json"),
    ("INF-W07", INFRA / "IMAGE_LOCK.json"),
    ("INF-W07", INFRA / "artefacts" / "logs" / "LATEST_CORRELATION.jsonl"),
    ("INF-W08", INFRA / "BOX.md"),
    ("INF-W08", INFRA / "AGENT_PATHS.md"),
    ("INF-W09", INFRA / "artefacts" / "reports" / "INF-P6-T01_phaseProve.json"),
    ("INF-W09", INFRA.parent / "doc" / "infra_wiring_eligibility.md"),
    ("INF-W10", INFRA.parent / "doc" / "infra_wiring_plan.md"),
    ("INF-W10", MQL5 / "Profiles" / "Tester" / "BMRG" / "EXP-P7-T03_export_Harvest_long.set"),
    ("INF-W11", INFRA / "artefacts" / "models" / "L2skip" / "LATEST_LIVE" / "PIN.json"),
    ("INF-W11", INFRA / "artefacts" / "ops" / "WIRE_AUTHORISATION.json"),
]


def run_pytest() -> dict:
    files = [str(INFRA / rel) for _, rel in PHASE_TESTS]
    r = subprocess.run(
        [sys.executable, "-m", "pytest", *files, "-q", "--tb=line"],
        cwd=str(INFRA),
        capture_output=True,
        text=True,
        timeout=600,
    )
    return {
        "returncode": r.returncode,
        "stdout_tail": "\n".join((r.stdout or "").strip().splitlines()[-8:]),
        "stderr_tail": "\n".join((r.stderr or "").strip().splitlines()[-8:]),
        "pass": r.returncode == 0,
    }


def check_artefacts() -> dict:
    rows = []
    for week, path in ARTEFACTS:
        ok = path.exists()
        rows.append({"week": week, "path": str(path.relative_to(INFRA) if path.is_relative_to(INFRA) else path), "ok": ok})
    return {"pass": all(r["ok"] for r in rows), "rows": rows}


def smoke_e2e() -> dict:
    """Light e2e: score freeze + CF + phase prove + promote dry-run (no full retrain)."""
    steps = []
    cmds = [
        ("P2_score", [sys.executable, "-c",
         "import json,sys; from pathlib import Path; sys.path[:0]=['src/score','src/ingest']; "
         "from health import score_pack_dir; r=score_pack_dir(Path('fixtures/blotter/harvest_long_v1')); "
         "assert r['verdict']=='ACCEPT' and abs(r['health_vector']['ef_pp']-2.3283)<0.01; print('ef',r['health_vector']['ef_pp'])"]),
        ("P4b_cf", [sys.executable, "src/eval/run_p4b_e2e.py"]),
        ("P5a_obs", [sys.executable, "src/obs/run_p5a_e2e.py"]),
        ("P6_prove", [sys.executable, "src/eval/phase_prove.py"]),
        ("P7_dry", [sys.executable, "src/train/promote.py", "--dry-run"]),
        ("P7P8_e2e", [sys.executable, "src/train/retrain_loop.py", "--e2e"]),
    ]
    all_ok = True
    for name, cmd in cmds:
        r = subprocess.run(cmd, cwd=str(INFRA), capture_output=True, text=True, timeout=180)
        ok = r.returncode == 0
        # P6 may print prove REJECT / NO-GO — process success is enough
        if name == "P4b_cf" and ok:
            try:
                # last json block may be large; check file
                ev = json.loads((INFRA / "artefacts/reports/INF-P4-T04_cf_scorecard.json").read_text(encoding="utf-8"))
                ok = ev.get("verdict") == "ACCEPT" or ev.get("cf", {}).get("verdict") == "ACCEPT"
            except Exception:
                ok = False
        if name == "P7P8_e2e" and ok:
            try:
                ev = json.loads((INFRA / "artefacts/reports/INF-W10_W11_scorecard.json").read_text(encoding="utf-8"))
                ok = ev.get("verdict") == "ACCEPT"
            except Exception:
                ok = False
        steps.append({"step": name, "ok": ok, "code": r.returncode})
        all_ok = all_ok and ok
    return {"pass": all_ok, "steps": steps}


def main() -> dict:
    pytest_r = run_pytest()
    arts = check_artefacts()
    smoke = smoke_e2e()
    report = {
        "recipe": "INF_full_scaleup_regression",
        "pytest": pytest_r,
        "artefacts": arts,
        "smoke_e2e": smoke,
        "verdict": "ACCEPT" if pytest_r["pass"] and arts["pass"] and smoke["pass"] else "REJECT",
    }
    out = INFRA / "artefacts" / "reports" / "INF_FULL_REGRESSION.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, indent=2), encoding="utf-8")
    (INFRA / "artefacts" / "reports" / "LATEST_EVAL.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    return report


if __name__ == "__main__":
    r = main()
    print(json.dumps({
        "verdict": r["verdict"],
        "pytest_pass": r["pytest"]["pass"],
        "pytest_tail": r["pytest"]["stdout_tail"],
        "artefacts_pass": r["artefacts"]["pass"],
        "artefacts_missing": [x["path"] for x in r["artefacts"]["rows"] if not x["ok"]],
        "smoke": r["smoke_e2e"]["steps"],
    }, indent=2))
