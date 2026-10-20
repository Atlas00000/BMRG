"""Build USDJPY-AOS-P7 promotion_packet.json."""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

OUT = Path(__file__).resolve().parent
BMRG = OUT.parents[2]


def main() -> None:
    p4 = json.loads(
        (BMRG / "blotter/archive/USDJPY-AOS-P4/P4_STACK.json").read_text(encoding="utf-8")
    )
    p6 = json.loads(
        (BMRG / "blotter/archive/USDJPY-AOS-P6/P6_HARDEN.json").read_text(encoding="utf-8")
    )
    p2 = json.loads(
        (BMRG / "blotter/archive/USDJPY-AOS-P2/P2_CF.json").read_text(encoding="utf-8")
    )
    base = p2["P2_T02_tip"]["baseline"]
    arm = p4["stacks"]["det_arm_v1c"]

    ledger_path = BMRG / "blotter/archive/USDJPY-AOS-P4/ledger_det_arm_v1c.csv"
    sample = {}
    if ledger_path.exists():
        import pandas as pd

        df = pd.read_csv(ledger_path)
        sample = {
            "ledger_path": str(ledger_path),
            "source": "offline_P4_tip_v1c_shadow",
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
        "aos_task": "USDJPY-AOS-P7",
        "packet_id": "USDJPY_M15_AOS_RESEARCH_v1",
        "preset_alias": "USDJPYstack",
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "framework_unified": "1.0",
        "framework_usdjpy": "0.1.0",
        "canvas": "display_only",
        "scope": {
            "sleeve": "USDJPY M15 expansion research OS",
            "not": [
                "AUDUSD / EURUSD / UK100 / DE40 live book replace",
                "PRODUCTION-WORTHY full G0–G5 admit",
                "L2 AI LIVE_WITHHOLD",
                "geometry retune (SL/TP/BB) / Tokyo reopen / ATR lift",
                "Jul LIVE (HOLD only — protect FP)",
                "Thu LIVE (DISARM — path-flip)",
            ],
        },
        "identity": {
            "engine_magic": 26101828,
            "research_os_magic": 26131807,
            "research_os_magic_p4_pre_hitl": 26131804,
            "ea_version_min": "compile with AOS_L2det_usdjpy.mqh",
            "preset_armed": "USDJPYstack.set",
            "preset_armed_alias": "BMRG-M15-USDJPY-6M-P7_research_OS_ARMED.set",
            "preset_engine": "BMRG-M15-USDJPY-6M-P0_balanced_chart.set",
            "symbol": "USDJPY",
            "asset": "USDJPY",
            "tf": "M15",
            "tester_paths": [
                "Presets/USDJPYstack.set",
                "Presets/BMRG-M15-USDJPY-6M-P7_research_OS_ARMED.set",
                "Profiles/Tester/BMRG/USDJPY/USDJPYstack.set",
                "Profiles/Tester/BMRG/USDJPY/BMRG-M15-USDJPY-6M-P7_research_OS_ARMED.set",
            ],
        },
        "armed_stack": {
            "engine": "Balanced P0 G0 FIXED_RR RR1.20 BB2.2 session12–20 skipTue ATR70",
            "L2det": "L2det_usdjpy_v1c LIVE_WITHHOLD (nearATR@0.9×70 OR H16)",
            "L2AI": "DISARM (AUC≈0.47 · BUY FP on tip CF)",
            "L3": "ON DD25% / BELOW halt",
            "L4": "ON size mod · W50",
            "L6": "ledger ON",
            "L8": "advise-only session-sleeve (not live abort)",
            "L9": "H14/spread/Jul HOLD_SHADOW — not LIVE in this packet",
            "ATR_max": 70,
            "Leak_source": "prior_11.4pp_until_deals",
            "Leak_pp": 11.4,
            "lot": 0.01,
            "risk_pct": 0.5,
        },
        "baseline_ref": "USDJPY_AOS_BASELINE_v1",
        "health_cf": {
            "engine_tip_path": {
                "n": base["n"],
                "WR": base["WR"],
                "E_N": base["E_N"],
                "EF_prior_pp": base["EF_prior_pp"],
                "note": "path tip n=46 (dedicated tip n=56 — path dependency)",
            },
            "offline_v1c_tip": {
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
                "Tester EA ledger for magic 26131807 not yet run — offline P4 tip "
                "v1c stack is the CF basis for HITL. Run USDJPYstack.set in Strategy Tester next."
            ),
        },
        "gates_edge_framework": {
            "G0_identity": "PASS — magic/preset locked; G0 MaxLevels=1",
            "expansion_EF": "PASS tip OS EF>0 under prior Leak 11.4 pp after v1c",
            "G3_regime_filtered": "PASS — session+skipTue+ATR70 declared (P6-T03)",
            "G4_MC": "DEFERRED — expansion research; not production admit",
            "G5_stress": "PARTIAL — L2 ±10% PASS_WITH_NOTES (P6); SL/TP not stressed",
            "Leak_measured": "OPEN — prior 11.4 pp (deal-measured preferred before capital)",
            "L2AI": "DISARM — tip AUC 0.471 · CHALLENGER EMPTY",
            "verdict_ladder": "EXPANSION_OS_ARMED — not PRODUCTION-WORTHY · not live FX replace",
        },
        "p6_harden_summary": {
            "L9": "no_LIVE — H14 DISARM · spread HOLD · Jul HOLD",
            "L2_stress": p6["P6_T02_L2_stress"]["verdict"],
            "ATR_G3": p6["P6_T03_ATR_G3"]["verdict"],
            "nearATR_keep": "0.9 / 70 + H16",
        },
        "ledger_sample": sample,
        "rollback": {
            "ai_pin": "python infra/artefacts/models/L2skip_usdjpy/rollback_l2skip_usdjpy.py rollback --to DISARM",
            "ea_det_off": "InpAOS_USDJPY_L2detEnable=false",
            "ea_aos_off": "InpAOS_Enable=false → load P0 balanced chart set",
            "kill_switch": "InpAiKillSwitch=true",
        },
        "hitl": {
            "status": "SIGNED",
            "signed_utc": datetime.now(timezone.utc).isoformat(),
            "signed_local": "2026-10-19T17:10:00+01:00",
            "signer": "operator (chat HITL confirmation — proceed with P7 + USDJPYstack)",
            "decision": "ARM_RESEARCH_OS",
            "acknowledged": [
                "Not AUD/EUR/UK/DE live book replace",
                "Not production G0–G5 admit",
                "Leak still prior 11.4 pp (measured OPEN)",
                "L2 AI remains DISARM",
                "L9 H14/spread/Jul shadow only — not LIVE",
                "Expansion sleeve only · USDJPYstack name",
                "Do not reopen Tokyo / lift ATR max",
            ],
        },
        "verdict": "ACCEPT_ARM_RESEARCH_OS",
    }
    (OUT / "promotion_packet.json").write_text(
        json.dumps(packet, indent=2), encoding="utf-8"
    )
    print(
        json.dumps(
            {"verdict": packet["verdict"], "magic": 26131807, "preset": "USDJPYstack"},
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
