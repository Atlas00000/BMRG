"""INF-P2 e2e: normalise → fixture → load×2 → scorecard."""
from __future__ import annotations

import json
import sys
from pathlib import Path

INFRA = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(INFRA / "src" / "ingest"))
sys.path.insert(0, str(INFRA / "src" / "score"))

from load_core import load_pack_dir  # noqa: E402
from mt5_normalise import default_harvest_paths, normalise  # noqa: E402
from health import score_pack_dir  # noqa: E402


def run() -> dict:
    log, train, out = default_harvest_paths()
    pack = normalise(log, train, out_dir=out)
    assert pack["stats"]["open_coverage"] >= 0.95, pack["stats"]

    load1 = load_pack_dir(out)
    load2 = load_pack_dir(out)
    idempotent = (
        load1["n_events"] == load2["n_events"] == pack["stats"]["n_manifest"]
        and load1["n_legs"] == load2["n_legs"]
        and load2["landed_new"] is False
    )

    scored = score_pack_dir(out, leak_policy="baseline_proxy")
    scored_cr = score_pack_dir(out, leak_policy="cost_c_r")

    report = {
        "task_id": "INF-P2-T04",
        "recipe": "INF-P2-T04_data_e2eReplay_HarvestLong_2025-2026",
        "fixture": str(out),
        "normalise_stats": pack["stats"],
        "load": {"first": load1, "second": load2, "idempotent": idempotent},
        "scorecard_baseline_proxy": scored,
        "scorecard_cost_c_r": scored_cr,
        "verdict": "ACCEPT"
        if pack["stats"]["open_coverage"] >= 0.95 and idempotent and scored["verdict"] == "ACCEPT"
        else "REJECT",
    }

    reports = INFRA / "artefacts" / "reports"
    reports.mkdir(parents=True, exist_ok=True)
    path = reports / "INF-P2-T04_scorecard.json"
    path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    (reports / "LATEST_EVAL.json").write_text(json.dumps(report, indent=2), encoding="utf-8")

    # optional: write score.health_vector style sidecar
    hv_path = out / "health_vector.json"
    hv_path.write_text(json.dumps(scored["health_vector"], indent=2), encoding="utf-8")
    return report


if __name__ == "__main__":
    r = run()
    print(json.dumps({"verdict": r["verdict"], "idempotent": r["load"]["idempotent"], "hv": r["scorecard_baseline_proxy"]["health_vector"], "vs": r["scorecard_baseline_proxy"]["vs_baseline"]}, indent=2))
