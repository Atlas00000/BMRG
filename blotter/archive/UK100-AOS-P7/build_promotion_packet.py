"""Build UK100-AOS-P7 promotion_packet.json."""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

OUT = Path(__file__).resolve().parent
BMRG = OUT.parents[2]
LEDGER = Path(
    r"C:\Users\emili\AppData\Roaming\MetaQuotes\Terminal\Common\Files"
    r"\BMRG_AOS_ledger_26111304.csv"
)


def main() -> None:
    tester = json.loads(
        (BMRG / "blotter/archive/UK100-AOS-P4/TESTER_LOG_REVIEW_2026.json").read_text(
            encoding="utf-8"
        )
    )
    p6 = json.loads(
        (BMRG / "blotter/archive/UK100-AOS-P6/P6_HARDEN.json").read_text(encoding="utf-8")
    )
    sample = {}
    if LEDGER.exists():
        df = pd.read_csv(LEDGER)
        sample = {
            "ledger_path": str(LEDGER),
            "n_rows": int(len(df)),
            "decision_counts": df["decision"].value_counts().to_dict(),
            "skip_reasons": df.loc[df["decision"] == "SKIP", "reason"]
            .value_counts()
            .to_dict(),
            "head_skip": df.loc[df["decision"] == "SKIP"].head(5)[
                ["t", "side", "decision", "reason", "mode"]
            ].to_dict("records"),
            "head_fire": df.loc[df["decision"] == "FIRE"].head(5)[
                ["t", "side", "decision", "reason", "life", "f_rec"]
            ].to_dict("records"),
        }

    packet = {
        "aos_task": "UK100-AOS-P7",
        "packet_id": "UK100_AOS_RESEARCH_v1",
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "framework_unified": "1.0",
        "framework_uk100": "0.1.0",
        "canvas": "display_only",
        "scope": {
            "sleeve": "UK100 expansion research OS",
            "not": [
                "EURUSD/AUDUSD live replace",
                "PRODUCTION-WORTHY full G0–G5 admit",
                "L2 AI LIVE_WITHHOLD",
                "geometry retune",
            ],
        },
        "identity": {
            "engine_magic": 26101201,
            "research_os_magic": 26111307,
            "ea_version_min": "1.23",
            "preset_armed": "BMRG-M15-UK100-6M-P7_research_OS_ARMED.set",
            "preset_engine": "BMRG-M15-UK100-6M-P0_balanced_chart.set",
            "symbol": "UK100",
            "tf": "M15",
            "hist_from": "2025.12.17",
        },
        "armed_stack": {
            "engine": "Balanced P0 G0 FIXED_RR RR1.25",
            "L2det": "L2det_uk_v1b LIVE_WITHHOLD (Thu OR BUY∧nearATR@0.9×1470)",
            "L2AI": "DISARM",
            "L3": "ON DD25% / BELOW halt",
            "L4": "ON size mod · W50",
            "L6": "ledger ON",
            "L8": "advise-only (not live abort)",
            "L9": "BUY∧H08 ARM_SOFT approved shadow — not LIVE in this packet",
            "ATR_max": 1470,
            "Leak_source": "journal_2x_entry_spread_median",
            "Leak_pp": 4.27,
        },
        "baseline_ref": "UK100_AOS_BASELINE_v1",
        "health_cf": {
            "engine_tip_MayAug": {
                "n": 51,
                "WR": 49.0,
                "E_N": 0.103,
                "EF_journal_pp": 0.31,
            },
            "offline_v1b_tip": {
                "n_fire": 33,
                "WR": 60.61,
                "E_N": 0.3636,
                "EF_pp": 11.9,
                "delta_E_N_vs_engine": 0.261,
            },
            "tester_OS_2026_JanOct": {
                "magic": 26111304,
                "FIRE": tester["ledger"]["FIRE"],
                "SKIP": tester["ledger"]["SKIP"],
                "FIRE_Thu": 0,
                "closed_full": tester["closed_book_full"],
                "closed_tip_MayAug": tester["closed_book_tip_MayAug"],
                "final_balance_usd": tester["final_balance_usd"],
                "L3_halt_rows": 0,
            },
        },
        "gates_edge_framework": {
            "G0_identity": "PASS — magic/preset locked; G0 MaxLevels=1",
            "expansion_EF": "PASS tip OS EF>0 under journal Leak",
            "G3_regime_filtered": "PASS — session+skipTue+ATR1470 declared (P6-T03)",
            "G4_MC": "DEFERRED — expansion research; not production admit",
            "G5_stress": "PARTIAL — L2 ±10% PASS_WITH_NOTES (P6); SL/TP not stressed",
            "Leak_measured": "OPEN — journal proxy 4.27 pp",
            "L2AI": "DISARM — AUC~0.39",
            "verdict_ladder": "EXPANSION_OS_ARMED — not PRODUCTION-WORTHY",
        },
        "p6_harden_summary": {
            "L9_BUY_H08": "ARM_SOFT_shadow",
            "L2_stress": p6["P6_T02_L2_stress"]["verdict"],
            "ATR_G3": p6["P6_T03_ATR_G3"]["verdict"],
        },
        "ledger_sample": sample,
        "rollback": {
            "ai_pin": "python infra/artefacts/models/L2skip_uk/rollback_l2skip_uk.py rollback --to DISARM",
            "ea_det_off": "InpAOS_UK_L2detEnable=false",
            "ea_aos_off": "InpAOS_Enable=false → load P0 balanced chart set",
            "kill_switch": "InpAiKillSwitch=true",
        },
        "hitl": {
            "status": "SIGNED",
            "signed_utc": "2026-10-12T23:03:00+00:00",
            "signed_local": "2026-10-13T00:03:00+01:00",
            "signer": "operator (chat HITL confirmation)",
            "decision": "ARM_RESEARCH_OS",
            "acknowledged": [
                "Not FX live replace",
                "Not production G0–G5 admit",
                "Leak still journal proxy",
                "L2 AI remains DISARM",
                "Truncated hist_from 2025.12.17",
            ],
        },
        "verdict": "ACCEPT_ARM_RESEARCH_OS",
    }
    (OUT / "promotion_packet.json").write_text(
        json.dumps(packet, indent=2), encoding="utf-8"
    )
    print(json.dumps({"verdict": packet["verdict"], "magic": 26111307}, indent=2))


if __name__ == "__main__":
    main()
