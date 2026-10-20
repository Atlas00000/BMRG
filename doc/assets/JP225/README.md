# JP225 / JPN225 asset docs (M15 chart expansion)

Nikkei index-CFD expansion research for **JP225** (MT5 **JPN225** · Point=0.01 · Digits=2). Separate from AUDUSD / EURUSD live books, UK100 / DE40 / USDJPY research OS, and root `system_profile.md`.

| Doc | Role |
| --- | --- |
| [`edge_framework.md`](./edge_framework.md) | **Normative** JP225 M15 binding of `unified_edge_framework.md` |
| [`system_profile.md`](./system_profile.md) | M15 class · edge · trade · rolling · performance |
| [`system_profile_M5.md`](./system_profile_M5.md) | **M5** Growth P0 system profile (expansion) |
| [`aios_roadmap.md`](./aios_roadmap.md) | **M15** AIOS plan P0–P7 (closed · `JPN225stack`) |
| [`aios_roadmap_M5.md`](./aios_roadmap_M5.md) | **M5** AIOS plan P0–P7 · tip EF>0 · MATCH tax / OFFHOME protect |
| [`JP225_M5_AOS_BASELINE_v1.md`](./JP225_M5_AOS_BASELINE_v1.md) | M5 frozen engine baseline (P0-T01) |
| [`aos_bad_cells_M5.md`](./aos_bad_cells_M5.md) | M5 L2det seeds (Aug–Sep MATCH · protect Jul) |
| [`aos_cost_policy_M5.md`](./aos_cost_policy_M5.md) | M5 Leak prior **3.3 pp** · measured OPEN |
| [`aos_l1_tape_contract_M5.md`](./aos_l1_tape_contract_M5.md) | M5 L1 feature schema v0 |
| [`aos_l2_policy_M5.md`](./aos_l2_policy_M5.md) | M5 L2det v1c ARM · L2AI DISARM |
| [`aos_l2_size_table_M5.md`](./aos_l2_size_table_M5.md) | M5 f multipliers (spec) |
| [`aos_l3l4_policy_M5.md`](./aos_l3l4_policy_M5.md) | M5 L3 halt / L4 health bus (SIGNED) |
| [`aos_l6_ledger_M5.md`](./aos_l6_ledger_M5.md) | M5 L6 ledger + det_v1c stack (SIGNED) |
| [`aos_l5_retrain_M5.md`](./aos_l5_retrain_M5.md) | M5 L5 retrain / rollback (AI DISARM) |
| [`aos_p6_harden_M5.md`](./aos_p6_harden_M5.md) | M5 L9 / L2 stress / ATR G3 (P6) |
| [`AIOS_SIGNOFF_M5.md`](./AIOS_SIGNOFF_M5.md) | M5 HITL research OS arm · **`JPN225_5m_stack`** |
| [`tapes/`](./tapes/) | M15 + **M5** tip/YTD/MATCH/OFFHOME fire tapes |
| [`JP225_AOS_BASELINE_v1.md`](./JP225_AOS_BASELINE_v1.md) | Frozen engine baseline for OS Δ (P0-T01) |
| [`aos_bad_cells.md`](./aos_bad_cells.md) | L2det seed registry (May FRAGILE / Jul–Oct MISMATCH / …) |
| [`aos_cost_policy.md`](./aos_cost_policy.md) | Leak **measured 2.45 pp** |
| [`LEAK_MEASURED.json`](./LEAK_MEASURED.json) | Deal-fill Leak packet |
| [`aos_l1_tape_contract.md`](./aos_l1_tape_contract.md) | L1 feature schema v0 |
| [`aos_l2_policy.md`](./aos_l2_policy.md) | L2det / L2AI ARM map (P2) |
| [`aos_l2_size_table.md`](./aos_l2_size_table.md) | f multipliers (spec) |
| [`aos_l3l4_policy.md`](./aos_l3l4_policy.md) | L3 halt / L4 health / recommend bus |
| [`aos_l6_ledger.md`](./aos_l6_ledger.md) | L6 schema + P4 stack (offline) |
| [`aos_l5_retrain.md`](./aos_l5_retrain.md) | L5 retrain / champ–challenger / rollback |
| [`aos_p6_harden.md`](./aos_p6_harden.md) | L9 / L2 stress / ATR G3 |
| [`tapes/`](./tapes/) | Tip 79 · Jan–Aug 143 · long 360 · May∨Jul ledger |
| Chart preset card | `doc/BMRG_M15_JP225_6M_chart_preset.md` |
| Blotter | `JP225-P1-REVIEW/` · `JP225-AOS-P1…P6/` · `JP225-AOS-LEAK/` |

**Presets:** `MQL5/Profiles/Tester/BMRG/JP225/` · also `Experts/BMRG/Presets/`  
**Parent maths:** `doc/unified_edge_framework.md` · layer vocab `doc/ai_OS.md`  
**Benchmark:** score under [`edge_framework.md`](./edge_framework.md) — Canvas display only.  
**Scope:** asset-list **expansion** · **Growth P1 AOS OFF** · **not** a live replace.  
**AIOS:** **P7 COMPLETE** — HITL · **`JPN225stack`** magic **26151907** · May∨Jul LIVE_WITHHOLD · L2AI DISARM · expansion not live.

| Sleeve | Preset | Magic | RR | BWR | Pool |
| --- | --- | ---: | ---: | ---: | --- |
| P0 growth | `BMRG-M15-JP225-6M-P0_growth_chart.set` | 26101903 | 1.50 | 40.0% | tip EF −1.9 pp · superseded |
| **P1 wrLift fade ★** | `BMRG-M15-JP225-6M-P1_wrLift_fade_chart.set` | **26101904** | 1.50 | 40.0% | **EXPAND_CANDIDATE** · OS baseline |
| P1.5 light (alt) | `BMRG-M15-JP225-6M-P1p5_light_chart.set` | 26101905 | 1.50 | 40.0% | untested · re-freeze if Stage-1 win |
| **Research OS ★** | **`JPN225stack.set`** | **26151907** | 1.50 | 40.0% | **ARMED** HITL 2026-10-19 |
| **M5 Growth P0 ★** | `BMRG-M5-JP225-6M-P0_growth_chart.set` | **26101906** | **2.00** | 33.3% | expansion KEEP · OS baseline · `aios_roadmap_M5.md` |
| **M5 Research OS P4** | `BMRG-M5-JP225-6M-P4_research_OS_W50.set` | **26161904** | 2.00 | 33.3% | Tester precursor · magic 26161904 |
| **M5 Research OS ★** | **`JPN225_5m_stack.set`** | **26161907** | 2.00 | 33.3% | **ARMED** HITL 2026-10-20 · alias P7_ARMED |

Evidence: M15 — Tester `logs/20261019.log` (Leak measured **2.45 pp**). M5 — `logs/20261020.log` tip n=94 · EF_prior **+4.9 pp** (Leak prior 3.3 pp until deals). M5 AIOS **P7 ARMED** 2026-10-20 · `JPN225_5m_stack` · magic **26161907**.
