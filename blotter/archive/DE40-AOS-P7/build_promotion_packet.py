"""Build DE40-AOS-P7 promotion_packet.json."""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

OUT = Path(__file__).resolve().parent
BMRG = OUT.parents[2]


def main() -> None:
    p4 = json.loads(
        (BMRG / "blotter/archive/DE40-AOS-P4/P4_STACK.json").read_text(encoding="utf-8")
    )
    p6 = json.loads(
        (BMRG / "blotter/archive/DE40-AOS-P6/P6_HARDEN.json").read_text(encoding="utf-8")
    )
    p2 = json.loads(
        (BMRG / "blotter/archive/DE40-AOS-P2/P2_CF.json").read_text(encoding="utf-8")
    )
    base = p2["P2_T02_tip"]["baseline"]
    arm = p4["stacks"]["det_arm_BUY_near_atr"]

    ledger_path = BMRG / "blotter/archive/DE40-AOS-P4/ledger_det_arm_BUY_near_atr.csv"
    sample = {}
    if ledger_path.exists():
        import pandas as pd

        df = pd.read_csv(ledger_path)
        sample = {
            "ledger_path": str(ledger_path),
            "source": "offline_P4_tip_arm_shadow",
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
        "aos_task": "DE40-AOS-P7",
        "packet_id": "DE40_M15_AOS_RESEARCH_v1",
        "preset_alias": "DE40stack",
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "framework_unified": "1.0",
        "framework_de40": "0.1.0",
        "canvas": "display_only",
        "scope": {
            "sleeve": "DE40/DE30 M15 expansion research OS",
            "not": [
                "AUDUSD / EURUSD / UK100 live book replace",
                "PRODUCTION-WORTHY full G0–G5 admit",
                "L2 AI LIVE_WITHHOLD",
                "geometry retune (SL/TP/BB)",
                "H13 LIVE (HOLD only — Aug FP)",
            ],
        },
        "identity": {
            "engine_magic": 26101902,
            "research_os_magic": 26141907,
            "research_os_magic_p4_pre_hitl": 26141904,
            "ea_version_min": "compile with AOS_L2det_de.mqh",
            "preset_armed": "DE40stack.set",
            "preset_armed_alias": "BMRG-M15-DE40-6M-P7_research_OS_ARMED.set",
            "preset_engine": "BMRG-M15-DE40-6M-P0_balanced_chart.set",
            "symbol": "DE30",
            "asset": "DE40",
            "tf": "M15",
            "tester_paths": [
                "Presets/DE40stack.set",
                "Presets/BMRG-M15-DE40-6M-P7_research_OS_ARMED.set",
                "Profiles/Tester/BMRG/DE40/DE40stack.set",
                "Profiles/Tester/BMRG/DE40/BMRG-M15-DE40-6M-P7_research_OS_ARMED.set",
            ],
        },
        "armed_stack": {
            "engine": "Balanced P0 G0 FIXED_RR RR1.25 BB2.2 session08–17 skipTue ATR4070",
            "L2det": "L2det_de40_v1_BUY_near_atr LIVE_WITHHOLD (BUY∧nearATR@0.9×4070)",
            "L2AI": "DISARM (AUC≈0.52 · chrono FREQ_STALL)",
            "L3": "ON DD25% / BELOW halt",
            "L4": "ON size mod · W50",
            "L6": "ledger ON",
            "L8": "advise-only cash-sleeve (not live abort)",
            "L9": "Frank/H08/H13 HOLD_SHADOW — not LIVE in this packet",
            "ATR_max": 4070,
            "Leak_source": "prior_9.8pp_until_deals",
            "Leak_pp": 9.8,
            "lot": 0.1,
            "risk_pct": 0.5,
        },
        "baseline_ref": "DE40_AOS_BASELINE_v1",
        "health_cf": {
            "engine_tip_MayOct": {
                "n": base["n"],
                "WR": base["WR"],
                "E_N": base["E_N"],
                "EF_prior_pp": base["EF_prior_pp"],
            },
            "offline_arm_tip": {
                "n_fire": arm["n_fire"],
                "n_skip": arm["n_l2det_skip"],
                "WR": arm["WR_pct"],
                "E_N": arm["E_N"],
                "EF_pp": arm["EF_prior_pp"],
                "delta_E_N_vs_engine": round(arm["E_N"] - base["E_N"], 4),
                "fire_retention_pct": arm["fire_retention_pct"],
                "L3_halt": arm["n_l3_halt"],
            },
            "note": (
                "Tester EA ledger for magic 26141907 not yet run — offline P4 tip "
                "ARM stack is the CF basis for HITL. Run DE40stack.set in Strategy Tester next."
            ),
        },
        "gates_edge_framework": {
            "G0_identity": "PASS — magic/preset locked; G0 MaxLevels=1",
            "expansion_EF": "PASS tip OS EF>0 under prior Leak 9.8 pp",
            "G3_regime_filtered": "PASS — session+skipTue+ATR4070 declared (P6-T03)",
            "G4_MC": "DEFERRED — expansion research; not production admit",
            "G5_stress": "PARTIAL — L2 ±10% PASS_WITH_NOTES (P6); SL/TP not stressed",
            "Leak_measured": "OPEN — prior 9.8 pp (deal-measured preferred before capital)",
            "L2AI": "DISARM — tip AUC 0.519 · chrono REJECT_FREQUENCY_STALL",
            "verdict_ladder": "EXPANSION_OS_ARMED — not PRODUCTION-WORTHY · not live FX/UK replace",
        },
        "p6_harden_summary": {
            "L9": "no_LIVE — Frank/H08 HOLD · spread DISARM",
            "L2_stress": p6["P6_T02_L2_stress"]["verdict"],
            "ATR_G3": p6["P6_T03_ATR_G3"]["verdict"],
            "nearATR_keep": "0.9 / 4070",
        },
        "ledger_sample": sample,
        "rollback": {
            "ai_pin": "python infra/artefacts/models/L2skip_de40/rollback_l2skip_de40.py rollback --to DISARM",
            "ea_det_off": "InpAOS_DE_L2detEnable=false",
            "ea_aos_off": "InpAOS_Enable=false → load P0 balanced chart set",
            "kill_switch": "InpAiKillSwitch=true",
        },
        "hitl": {
            "status": "SIGNED",
            "signed_utc": datetime.now(timezone.utc).isoformat(),
            "signed_local": "2026-10-19T16:10:00+01:00",
            "signer": "operator (chat HITL confirmation — proceed with P7 + DE40stack)",
            "decision": "ARM_RESEARCH_OS",
            "acknowledged": [
                "Not AUD/EUR/UK live book replace",
                "Not production G0–G5 admit",
                "Leak still prior 9.8 pp (measured OPEN)",
                "L2 AI remains DISARM",
                "L9 Frankfurt/H08/H13 shadow only — not LIVE",
                "Expansion sleeve only · DE40stack name",
            ],
        },
        "verdict": "ACCEPT_ARM_RESEARCH_OS",
    }
    (OUT / "promotion_packet.json").write_text(
        json.dumps(packet, indent=2), encoding="utf-8"
    )
    print(json.dumps({"verdict": packet["verdict"], "magic": 26141907, "preset": "DE40stack"}, indent=2))


if __name__ == "__main__":
    main()
