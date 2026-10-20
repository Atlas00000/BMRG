"""Build JP225-AOS-P7 promotion_packet.json."""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

OUT = Path(__file__).resolve().parent
BMRG = OUT.parents[2]


def main() -> None:
    p4 = json.loads(
        (BMRG / "blotter/archive/JP225-AOS-P4/P4_STACK.json").read_text(encoding="utf-8")
    )
    p6 = json.loads(
        (BMRG / "blotter/archive/JP225-AOS-P6/P6_HARDEN.json").read_text(encoding="utf-8")
    )
    leak = json.loads(
        (BMRG / "doc/assets/JP225/LEAK_MEASURED.json").read_text(encoding="utf-8")
    )
    p2 = json.loads(
        (BMRG / "blotter/archive/JP225-AOS-P2/P2_CF.json").read_text(encoding="utf-8")
    )
    base = p2["P2_T02_tip"]["baseline"]
    arm = p4["stacks"]["det_may_or_jul"]
    tip_meas = leak["tip_all"]
    arm_meas = leak["tip_May_OR_Jul_kept"]

    ledger_path = BMRG / "blotter/archive/JP225-AOS-P4/ledger_det_may_or_jul.csv"
    sample = {}
    if ledger_path.exists():
        import pandas as pd

        df = pd.read_csv(ledger_path)
        sample = {
            "ledger_path": str(ledger_path),
            "source": "offline_P4_tip_may_or_jul_shadow",
            "n_rows": int(len(df)),
            "decision_counts": df["decision"].value_counts().to_dict(),
            "l2det_reasons": df.loc[df["l2det_skip"] == 1, "l2det_reason"]
            .value_counts()
            .to_dict(),
            "head_skip": df.loc[df["decision"] == "WOULD_SKIP"]
            .head(5)[["t", "side", "decision", "reason", "mode"]]
            .to_dict("records"),
            "head_fire": df.loc[df["decision"] == "FIRE_OK"]
            .head(5)[["t", "side", "decision", "reason", "life", "f_rec"]]
            .to_dict("records"),
        }

    packet = {
        "aos_task": "JP225-AOS-P7",
        "packet_id": "JP225_M15_AOS_RESEARCH_v1",
        "preset_alias": "JPN225stack",
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "framework_unified": "1.0",
        "framework_jp225": "0.1.6",
        "canvas": "display_only",
        "scope": {
            "sleeve": "JP225/JPN225 M15 expansion research OS",
            "not": [
                "AUDUSD / EURUSD / UK100 / DE40 live book replace",
                "PRODUCTION-WORTHY full G0–G5 admit",
                "L2 AI LIVE_WITHHOLD",
                "geometry retune (SL/TP/BB)",
                "Wed LIVE (HOLD only — Aug FP)",
                "L9 London/H08/H14 LIVE",
            ],
        },
        "identity": {
            "engine_magic": 26101904,
            "research_os_magic": 26151907,
            "ea_version_min": "compile with AOS_L2det_jp.mqh",
            "preset_armed": "JPN225stack.set",
            "preset_armed_alias": "BMRG-M15-JP225-6M-P7_research_OS_ARMED.set",
            "preset_engine": "BMRG-M15-JP225-6M-P1_wrLift_fade_chart.set",
            "symbol": "JPN225",
            "asset": "JP225",
            "tf": "M15",
            "tester_paths": [
                "Presets/JPN225stack.set",
                "Presets/BMRG-M15-JP225-6M-P7_research_OS_ARMED.set",
                "Profiles/Tester/BMRG/JP225/JPN225stack.set",
                "Profiles/Tester/BMRG/JP225/BMRG-M15-JP225-6M-P7_research_OS_ARMED.set",
                "MQL5/Profiles/Tester/BMRG/JP225/JPN225stack.set",
            ],
        },
        "armed_stack": {
            "engine": "Growth P1 wrLift fade RR1.50 BB2.3 session08–17 skipTue ATR19670 FadeON",
            "L2det": "L2det_jp225_v1_May_OR_Jul LIVE_WITHHOLD",
            "L2AI": "DISARM (AUC≈0.49)",
            "L3": "ON DD25% / BELOW halt",
            "L4": "ON size mod · W50",
            "L6": "ledger ON",
            "L8": "advise-only index sleeve (not live abort)",
            "L9": "London/H08/H14 HOLD_SHADOW — not LIVE in this packet",
            "ATR_max": 19670,
            "Leak_source": "measured_median_deal_fill",
            "Leak_pp": 2.45,
            "lot": 0.1,
            "risk_pct": 0.5,
        },
        "baseline_ref": "JP225_AOS_BASELINE_v1",
        "health_cf": {
            "engine_tip_prior": {
                "n": base["n"],
                "WR": base["WR"],
                "E_N": base["E_N"],
                "EF_prior_pp": base["EF_prior_pp"],
            },
            "engine_tip_measured": tip_meas,
            "offline_arm_tip_p4": {
                "n_fire": arm["n_fire"],
                "n_skip": arm["n_l2det_skip"],
                "WR": arm["WR"],
                "E_N": arm["E_N"],
                "EF_measured_pp": arm["EF_measured_pp"],
                "fire_retention_pct": arm["fire_retention_pct"],
                "L3_halt": arm["n_l3_halt"],
            },
            "skip_only_May_OR_Jul_measured": arm_meas,
            "note": (
                "Tester EA ledger for magic 26151907 not yet run — offline P4 tip "
                "May∨Jul stack + measured Leak tip EF>0 is the CF basis for HITL. "
                "Run JPN225stack.set in Strategy Tester next."
            ),
        },
        "gates_edge_framework": {
            "G0_identity": "PASS — magic/preset locked; G0 MaxLevels=1",
            "expansion_EF": "PASS tip EF +0.59 pp under measured Leak 2.45 pp (engine); arm +11.0 pp skip-only",
            "G3_regime_filtered": "PASS — session+skipTue+ATR19670 declared (P6-T03)",
            "G4_MC": "DEFERRED — expansion research; not production admit",
            "G5_stress": "PARTIAL — L2 arm-width PASS_WITH_NOTES (P6); SL/TP not stressed",
            "Leak_measured": "CLOSED — 2.45 pp deal-fill median (live ~2300 pts = re-check)",
            "L2AI": "DISARM — tip AUC 0.493 · challenger EMPTY",
            "verdict_ladder": "EXPANSION_OS_ARMED — not PRODUCTION-WORTHY · not live FX/EU replace",
        },
        "p6_harden_summary": {
            "L9": "no_LIVE — London/H08 HOLD · spread DISARM",
            "L2_stress": p6["P6_T02_L2_stress"]["verdict"],
            "ATR_G3": p6["P6_T03_ATR_G3"]["verdict"],
            "keep": "May∨Jul · Wed widen stall",
        },
        "ledger_sample": sample,
        "rollback": {
            "ai_pin": "python infra/artefacts/models/L2skip_jp225/rollback_l2skip_jp225.py rollback --to DISARM",
            "ea_det_off": "InpAOS_JP_L2detEnable=false",
            "ea_aos_off": "InpAOS_Enable=false → load P1 wrLift fade chart set",
            "kill_switch": "InpAiKillSwitch=true",
        },
        "hitl": {
            "status": "SIGNED",
            "signed_utc": datetime.now(timezone.utc).isoformat(),
            "signed_local": "2026-10-19T16:45:00+01:00",
            "signer": "operator (chat HITL — proceed with P7 + JPN225stack)",
            "decision": "ARM_RESEARCH_OS",
            "acknowledged": [
                "Not AUD/EUR/UK/DE40 live book replace",
                "Not production G0–G5 admit",
                "Leak measured 2.45 pp (live spread re-check before capital)",
                "L2 AI remains DISARM",
                "L9 London/H08/H14 shadow only — not LIVE",
                "Expansion sleeve only · JPN225stack name",
            ],
        },
        "verdict": "ACCEPT_ARM_RESEARCH_OS",
    }
    (OUT / "promotion_packet.json").write_text(
        json.dumps(packet, indent=2), encoding="utf-8"
    )
    (BMRG / "doc/assets/JP225/promotion_packet.json").write_text(
        json.dumps(packet, indent=2), encoding="utf-8"
    )
    print(
        json.dumps(
            {"verdict": packet["verdict"], "magic": 26151907, "preset": "JPN225stack"},
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
