"""Build EURUSD-AOS-P7 promotion_packet.json."""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

OUT = Path(__file__).resolve().parent
BMRG = OUT.parents[2]


def main() -> None:
    p4 = json.loads(
        (BMRG / "blotter/archive/EURUSD-AOS-P4/P4_STACK.json").read_text(encoding="utf-8")
    )
    p6 = json.loads(
        (BMRG / "blotter/archive/EURUSD-AOS-P6/P6_HARDEN.json").read_text(encoding="utf-8")
    )
    p2 = json.loads(
        (BMRG / "blotter/archive/EURUSD-AOS-P2/P2_CF.json").read_text(encoding="utf-8")
    )
    base = p2["P2_T02_dow_hour"]["baseline"]
    v1b = p4["stacks"]["det_v1b"]

    # Offline tip ledger sample (no Tester EA ledger yet for 26121807)
    ledger_path = (
        BMRG
        / "blotter/archive/EURUSD-AOS-P4/ledger_det_v1b.csv"
    )
    sample = {}
    if ledger_path.exists():
        import pandas as pd

        df = pd.read_csv(ledger_path)
        sample = {
            "ledger_path": str(ledger_path),
            "source": "offline_P4_tip_shadow",
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
        "aos_task": "EURUSD-AOS-P7",
        "packet_id": "EURUSD_M15_AOS_RESEARCH_v1",
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "framework_unified": "1.0",
        "framework_eurusd_m15": "0.1.0",
        "canvas": "display_only",
        "scope": {
            "sleeve": "EURUSD M15 expansion research OS",
            "not": [
                "EURUSD M5 Harvest live replace (8210xxx / 8399xxx)",
                "AUDUSD / UK100 / AAPL L2 pin reuse",
                "PRODUCTION-WORTHY full G0–G5 admit",
                "L2 AI LIVE_WITHHOLD",
                "geometry retune (SL/TP/BB/CD)",
            ],
        },
        "identity": {
            "engine_magic": 26101817,
            "research_os_magic": 26121807,
            "research_os_magic_p4_pre_hitl": 26121804,
            "ea_version_min": "compile with AOS_L2det_eur.mqh",
            "preset_armed": "BMRG-M15-EURUSD-6M-P7_research_OS_ARMED.set",
            "preset_engine": "BMRG-M15-EURUSD-6M-P2_light_selective_chart.set",
            "symbol": "EURUSD",
            "tf": "M15",
            "tester_paths": [
                "Presets/BMRG-M15-EURUSD-6M-P7_research_OS_ARMED.set",
                "Profiles/Tester/BMRG/EURUSD/BMRG-M15-EURUSD-6M-P7_research_OS_ARMED.set",
            ],
        },
        "armed_stack": {
            "engine": "P2 light G0 FIXED_RR RR1.25 BB2.3 CD3 session12–20 skipTue",
            "L2det": "L2det_eur_m15_v1b LIVE_WITHHOLD (Thu OR BUY∧nearATR@0.9×74)",
            "L2AI": "DISARM (chrono holdout)",
            "L3": "ON DD25% / BELOW halt",
            "L4": "ON size mod · W50",
            "L6": "ledger ON",
            "L8": "advise-only overnight-primary (not live abort)",
            "L9": "H19 ARM_SOFT approved shadow — not LIVE in this packet",
            "ATR_max": 74,
            "Leak_source": "journal_2x_entry_spread_median",
            "Leak_pp": 1.19,
            "lot": 0.01,
            "risk_pct": 0.5,
        },
        "baseline_ref": "EURUSD_AOS_BASELINE_v1",
        "health_cf": {
            "engine_tip_MayOct": {
                "n": base["n"],
                "WR": base["WR"],
                "E_N": base["E_N"],
                "EF_journal_pp": base["EF_proxy_pp"],
            },
            "offline_v1b_tip": {
                "n_fire": v1b["n_fire"],
                "n_skip": v1b["n_l2det_skip"],
                "WR": v1b["WR"],
                "E_N": v1b["E_N"],
                "EF_pp": v1b["EF_proxy_pp"],
                "delta_E_N_vs_engine": round(v1b["E_N"] - base["E_N"], 4),
                "fire_retention_pct": round(100.0 * v1b["n_fire"] / v1b["n_signals"], 1),
                "L3_halt": v1b["n_l3_halt"],
            },
            "note": (
                "Tester EA ledger for magic 26121807 not yet run — offline P4 tip "
                "stack is the CF basis for HITL. Run P7 .set in Strategy Tester next."
            ),
        },
        "gates_edge_framework": {
            "G0_identity": "PASS — magic/preset locked; G0 MaxLevels=1",
            "expansion_EF": "PASS tip OS EF>0 under journal Leak 1.19 pp",
            "G3_regime_filtered": "PASS — session+skipTue+ATR74 declared (P6-T03)",
            "G4_MC": "DEFERRED — expansion research; not production admit",
            "G5_stress": "PARTIAL — L2 ±10% PASS_WITH_NOTES (P6); SL/TP not stressed",
            "Leak_measured": "OPEN — journal proxy 1.19 pp (swap-aware deal export)",
            "L2AI": "DISARM — tip AUC 0.58 · chrono holdout DISARM",
            "verdict_ladder": "EXPANSION_OS_ARMED — not PRODUCTION-WORTHY · not M5 replace",
        },
        "p6_harden_summary": {
            "L9_H19": "ARM_SOFT_shadow",
            "L2_stress": p6["P6_T02_L2_stress"]["verdict"],
            "ATR_G3": p6["P6_T03_ATR_G3"]["verdict"],
            "nearATR_keep": "0.9 / 74",
        },
        "ledger_sample": sample,
        "rollback": {
            "ai_pin": "python infra/artefacts/models/L2skip_eur_m15/rollback_l2skip_eur_m15.py rollback --to DISARM",
            "ea_det_off": "InpAOS_EUR_L2detEnable=false",
            "ea_aos_off": "InpAOS_Enable=false → load P2 light chart set",
            "kill_switch": "InpAiKillSwitch=true",
        },
        "hitl": {
            "status": "SIGNED",
            "signed_utc": "2026-10-18T15:15:00+00:00",
            "signed_local": "2026-10-18T16:15:00+01:00",
            "signer": "operator (chat HITL confirmation — proceed with P7)",
            "decision": "ARM_RESEARCH_OS",
            "acknowledged": [
                "Not M5 Harvest live replace",
                "Not production G0–G5 admit",
                "Leak still journal proxy (measured+swap OPEN)",
                "L2 AI remains DISARM",
                "L9 H19 shadow only — not LIVE",
                "Expansion sleeve only",
            ],
        },
        "verdict": "ACCEPT_ARM_RESEARCH_OS",
    }
    (OUT / "promotion_packet.json").write_text(
        json.dumps(packet, indent=2), encoding="utf-8"
    )
    print(json.dumps({"verdict": packet["verdict"], "magic": 26121807}, indent=2))


if __name__ == "__main__":
    main()
