"""Build AUDUSD-AOS-P7 promotion_packet.json."""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

OUT = Path(__file__).resolve().parent
BMRG = OUT.parents[2]


def main() -> None:
    p4 = json.loads(
        (BMRG / "blotter/archive/AUDUSD-AOS-P4/P4_STACK.json").read_text(encoding="utf-8")
    )
    p6 = json.loads(
        (BMRG / "blotter/archive/AUDUSD-AOS-P6/P6_HARDEN.json").read_text(encoding="utf-8")
    )
    p2 = json.loads(
        (BMRG / "blotter/archive/AUDUSD-AOS-P2/P2_CF.json").read_text(encoding="utf-8")
    )
    p3 = json.loads(
        (BMRG / "blotter/archive/AUDUSD-AOS-P3/P3_L3L4.json").read_text(encoding="utf-8")
    )
    base = p2["P2_T02_dow_month"]["baseline"]
    v1 = p4["stacks"]["det_v1"]
    v1_health = p3["sims"]["v1_BUY_May_kept"]

    ledger_path = BMRG / "blotter/archive/AUDUSD-AOS-P4/ledger_det_v1.csv"
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
        "aos_task": "AUDUSD-AOS-P7",
        "packet_id": "AUDUSD_M15_AOS_RESEARCH_v1",
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "framework_unified": "1.0",
        "framework_audusd": "0.1.0",
        "canvas": "display_only",
        "scope": {
            "sleeve": "AUDUSD CHAMP M15 research OS",
            "not": [
                "Live M5 SCALE replace (8230931)",
                "FT twin replace (8230921)",
                "EURUSD / UK100 / DE40 / AAPL L2 pin reuse",
                "PRODUCTION-WORTHY full G0–G5 admit",
                "L2 AI LIVE_WITHHOLD (challenger SHADOW only)",
                "geometry retune (SL/TP/BB/session/weekday)",
            ],
        },
        "identity": {
            "engine_magic": 8230901,
            "research_os_magic": 8231941,
            "ea_version_min": "compile with AOS_L2det_aud.mqh",
            "preset_armed": "AUDUSD_stack.set",
            "preset_armed_alias": "BMRG-M15-AUDUSD-6M-P7_research_OS_ARMED.set",
            "preset_engine": "AUDUSD-CHAMP_Harvest_start13_skipMon_G0.set",
            "symbol": "AUDUSD",
            "tf": "M15",
            "tester_paths": [
                "Presets/AUDUSD_stack.set",
                "Presets/BMRG-M15-AUDUSD-6M-P7_research_OS_ARMED.set",
                "Profiles/Tester/BMRG/AUDUSD/AUDUSD_stack.set",
                "Profiles/Tester/BMRG/AUDUSD/BMRG-M15-AUDUSD-6M-P7_research_OS_ARMED.set",
                "doc/presets/AUDUSD_stack.set",
            ],
        },
        "armed_stack": {
            "engine": "CHAMP Harvest G0 FIXED_RR RR1 BB2.2 CD3 Start13–20 skipMon/Tue SL/TP300/300 ATR OFF",
            "L2det": "L2det_aud_m15_v1 LIVE_WITHHOLD (BUY ∧ month==May)",
            "L2AI": "OFF in EA · challenger SHADOW store (HITL …145303) — not LIVE_WITHHOLD",
            "L3": "ON DD25% / BELOW halt",
            "L4": "ON size mod · W50",
            "L6": "ledger ON",
            "L8": "advise-only overnight-primary (not live abort)",
            "L9": "BUY∧Thu ARM_SOFT shadow — not LIVE (SkipBuyThu=false)",
            "ATR_max": "OFF (P8-T03 SKIP)",
            "Leak_source": "journal_2x_entry_spread_median",
            "Leak_pp": 5.0,
            "lot": 0.01,
            "risk_pct": 0.5,
        },
        "baseline_ref": "AUDUSD_AOS_BASELINE_v1",
        "health_cf": {
            "engine_tip_MayAug": {
                "n": base["n"],
                "WR": base["WR"],
                "E_N": base["E_N"],
                "EF_journal_pp": base["EF_proxy_pp"],
            },
            "offline_v1_tip": {
                "n_fire": v1["n_fire"],
                "n_skip": v1["n_l2det_skip"],
                "WR": v1["WR"],
                "E_N": v1["E_N"],
                "EF_pp": v1["EF_proxy_pp"],
                "delta_E_N_vs_engine": round(v1["E_N"] - base["E_N"], 4),
                "fire_retention_pct": v1["fire_retention_pct"],
                "L3_halt": v1["n_l3_halt"],
                "skip_precision_losers": v1["skip_precision_losers"],
            },
            "p3_health_v1": {
                "max_dd_peak_pct": v1_health["max_dd_peak_pct"],
                "trip_count": v1_health["trip_count"],
                "last_en20": v1_health["last_en20"],
                "max_loss_streak": v1_health["max_loss_streak"],
            },
            "note": (
                "Tester EA ledger for magic 8231941 not yet run — offline P4 tip "
                "stack is the CF basis for HITL. Run AUDUSD_stack / P7 .set in Strategy Tester next."
            ),
        },
        "gates_edge_framework": {
            "G0_identity": "PASS — magic/preset locked; G0 MaxLevels=1",
            "expansion_EF": "PASS tip OS EF>0 under journal Leak 5.0 pp",
            "G3_regime_filtered": "PASS — session+skipMon/Tue + geometry freeze (P6-T03); ATR OFF by design",
            "G4_MC": "DEFERRED — expansion research; not production admit",
            "G5_stress": "PASS — L2 calendar/AI thr stress (P6); SL/TP not stressed",
            "Leak_measured": "OPEN — journal proxy 5.0 pp (swap-aware deal export)",
            "L2AI": "SHADOW challenger only — tip AUC 0.60 · chrono HOLD · not LIVE_WITHHOLD",
            "verdict_ladder": "EXPANSION_OS_ARMED — not PRODUCTION-WORTHY · not M5 SCALE replace",
        },
        "p6_harden_summary": {
            "L9_BUY_Thu": "ARM_SOFT_shadow_off_on_stack",
            "L2_stress": p6["P6_T02_L2_stress"]["verdict"],
            "geometry_freeze": p6["P6_T03_geometry_freeze"]["verdict"],
            "SkipBuyMay": True,
            "SkipBuyThu": False,
        },
        "ledger_sample": sample,
        "rollback": {
            "ai_pin": "python infra/artefacts/models/L2skip_aud_m15/rollback_l2skip_aud_m15.py rollback --to DISARM",
            "ea_det_off": "InpAOS_AUD_L2detEnable=false",
            "ea_aos_off": "InpAOS_Enable=false → load AUDUSD-CHAMP_Harvest_start13_skipMon_G0.set",
            "kill_switch": "InpAiKillSwitch=true",
            "never": "do not load AUDUSD_stack on live M5 SCALE 8230931",
        },
        "hitl": {
            "status": "SIGNED",
            "signed_utc": "2026-10-19T15:15:00+00:00",
            "signed_local": "2026-10-19T16:15:00+01:00",
            "signer": "operator (chat — proceed with P7 and provide the preset)",
            "prior_hitl": "P5 challenger pin 2026-10-19 · P6 AUDUSD_stack arm",
            "decision": "ARM_RESEARCH_OS",
            "acknowledged": [
                "Not live M5 SCALE 8230931 replace",
                "Not production G0–G5 admit",
                "Leak still journal proxy 5.0 pp (measured+swap OPEN)",
                "L2 AI remains OFF in EA (challenger SHADOW store only)",
                "L9 BUY∧Thu shadow only — SkipBuyThu=false on stack",
                "M15 research sleeve only · geometry frozen",
            ],
        },
        "verdict": "ACCEPT_ARM_RESEARCH_OS",
    }
    (OUT / "promotion_packet.json").write_text(
        json.dumps(packet, indent=2), encoding="utf-8"
    )
    print(json.dumps({"verdict": packet["verdict"], "magic": 8231941}, indent=2))


if __name__ == "__main__":
    main()
