# UK100 asset docs

Index-CFD expansion research for **UK100** (FTSE 100 · Point=0.01 · Digits=2). Separate from AUDUSD / EURUSD live books and from root `system_profile.md`.

| Doc | Role |
| --- | --- |
| [`edge_framework.md`](./edge_framework.md) | **Normative** UK100 binding of `unified_edge_framework.md` (gates, gaps, canvas caveat) |
| [`system_profile.md`](./system_profile.md) | **M15** class · edge · trade · rolling · performance · key metrics |
| [`system_profile_M5.md`](./system_profile_M5.md) | **M5** Balanced P0 system profile (expansion · AOS OFF) |
| [`aios_roadmap.md`](./aios_roadmap.md) | **M15 AIOS** P0–P7 · HITL ARMED |
| [`aios_roadmap_M5.md`](./aios_roadmap_M5.md) | **M5 AIOS** P0–P7 · **HITL ARMED** |
| [`AIOS_SIGNOFF_M5.md`](./AIOS_SIGNOFF_M5.md) | **HITL** M5 research OS · `UK100_5m_stack` · magic **26121907** |
| [`aos_l5_retrain_M5.md`](./aos_l5_retrain_M5.md) | M5 L5 store · champ/challenger · rollback |
| [`aos_p6_harden_M5.md`](./aos_p6_harden_M5.md) | M5 P6 L9 · bound stress · ATR G3 |
| [`aos_l3l4_policy_M5.md`](./aos_l3l4_policy_M5.md) | M5 L3 halt / L4 W20–W50 bus (P3) |
| [`aos_l6_ledger_M5.md`](./aos_l6_ledger_M5.md) | M5 L6 ledger · P4 research OS `.set` |
| [`aos_l1_tape_contract_M5.md`](./aos_l1_tape_contract_M5.md) | M5 L1 feature schema v0 |
| [`aos_l2_policy_M5.md`](./aos_l2_policy_M5.md) | M5 L2 — **v1b** (Mon∧H12)∨(SELL∧H12) ARM_SOFT |
| [`aos_l2_size_table_M5.md`](./aos_l2_size_table_M5.md) | M5 L2size f table (spec) |
| [`tapes/`](./tapes/) | M15 + **M5** fire tapes (`uk100_m5_*_v0.csv`) |
| [`UK100_AOS_BASELINE_v1.md`](./UK100_AOS_BASELINE_v1.md) | M15 frozen engine baseline for OS Δ |
| [`UK100_M5_AOS_BASELINE_v1.md`](./UK100_M5_AOS_BASELINE_v1.md) | M5 frozen engine baseline for OS Δ |
| [`aos_bad_cells.md`](./aos_bad_cells.md) | M15 L2det seed registry (Thu / H08 / Jul / …) |
| [`aos_bad_cells_M5.md`](./aos_bad_cells_M5.md) | M5 L2det seed registry (Mon / H12–13 / Aug / …) |
| [`aos_cost_policy.md`](./aos_cost_policy.md) | M15 Leak policy · journal proxy 4.27 pp |
| [`aos_cost_policy_M5.md`](./aos_cost_policy_M5.md) | M5 Leak · journal proxy **5.93 pp** · measured OPEN |
| [`aos_l1_tape_contract.md`](./aos_l1_tape_contract.md) | M15 L1 feature schema v0 |
| [`aos_l2_policy.md`](./aos_l2_policy.md) | M15 L2 P2 complete — **v1b stack** ARM · L2AI DISARM |
| [`aos_l2_size_table.md`](./aos_l2_size_table.md) | L2size f multipliers |
| [`aos_l3l4_policy.md`](./aos_l3l4_policy.md) | L3 halt / L4 health bus (P3 signed) |
| [`aos_l6_ledger.md`](./aos_l6_ledger.md) | L6 ledger schema · stack CF · research `.set` (P4 signed) |
| [`aos_l5_retrain.md`](./aos_l5_retrain.md) | L5 retrain store · champ/challenger · rollback (P5 signed) |
| [`aos_p6_harden.md`](./aos_p6_harden.md) | P6 L9 session · L2 ±10% stress · ATR G3 (signed) |
| [`AIOS_SIGNOFF.md`](./AIOS_SIGNOFF.md) | **HITL** research OS arm · magic **26111307** (P7) |
| Chart preset card | `doc/BMRG_M15_UK100_6M_chart_preset.md` |
| Blotter review | `blotter/archive/UK100-P0-CHART/REVIEW.md` |

**Presets (inputs only):** `MQL5/Profiles/Tester/BMRG/UK100/` · also `Experts/BMRG/Presets/`  
**Parent maths:** `doc/unified_edge_framework.md` · layer vocab `doc/ai_OS.md`  
**Benchmark:** score under [`edge_framework.md`](./edge_framework.md) — Canvas / chat charts are display only.  
**Scope:** asset-list **expansion** · **Balanced P0 AOS OFF** · **not** a live replace.  
**AIOS M15:** **P7 HITL SIGNED** — magic **26111307** · not FX live replace · L2 AI DISARM.  
**AIOS M5:** **P7 HITL SIGNED** — **`UK100_5m_stack.set`** · magic **26121907** · L2det_uk_m5_v1b · not FX live replace · L2 AI DISARM.

| Sleeve | Preset | Magic | RR | BWR | Pool |
| --- | --- | ---: | ---: | ---: | --- |
| **Balanced P0 M15** | `BMRG-M15-UK100-6M-P0_balanced_chart.set` | **26101201** | 1.25 | 44.4% | **EXPANSION_KEEP** |
| **Balanced P0 M5** | `BMRG-M5-UK100-6M-P0_balanced_chart.set` | **26101905** | 1.25 | 44.4% | **EXPANSION_KEEP** · AOS OFF |
| **M5 Research OS P4** | `BMRG-M5-UK100-6M-P4_research_OS_W50.set` | **26121904** | 1.25 | 44.4% | Tester twin |
| **M5 Research OS P7 ★** | **`UK100_5m_stack.set`** | **26121907** | 1.25 | 44.4% | **HITL ARM** L2det_uk_m5_v1b · L3/L4/W50 |
| **Research OS P7 ★** | `BMRG-M15-UK100-6M-P7_research_OS_ARMED.set` | **26111307** | 1.25 | 44.4% | **HITL ARM** L2det v1b · L3/L4/W50 |
| Research OS P4 (pre-HITL) | `BMRG-M15-UK100-6M-P4_research_OS_W50.set` | 26111304 | 1.25 | 44.4% | Tester twin |

Evidence M15: Tester `logs/20261012.log` (scored 2026-10-12). Broker history tip begins **2025.12.17** — “2024→…” long runs are truncated.  
Evidence M5: Tester `logs/20261020.log` · tip May→Aug · see [`system_profile_M5.md`](./system_profile_M5.md) · blotter `UK100-M5-P0-CHART`.
