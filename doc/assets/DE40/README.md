# DE40 asset docs

Index-CFD expansion research for **DE40** (Germany 40 / DAX · MT5 **DE30** · Point=0.01 · Digits=2). Separate from AUDUSD / EURUSD live books, UK100 / USDJPY research OS, and root `system_profile.md`.

| Doc | Role |
| --- | --- |
| [`edge_framework.md`](./edge_framework.md) | **Normative** DE40 binding of `unified_edge_framework.md` |
| [`system_profile.md`](./system_profile.md) | **M15** class · edge · trade · rolling · performance |
| [`system_profile_M5.md`](./system_profile_M5.md) | **M5** class · edge · trade · rolling · performance (expansion) |
| [`aios_roadmap.md`](./aios_roadmap.md) | **AIOS plan** P0–P7 · weekly table · iteration bar (**M15** · HITL closed) |
| [`aios_roadmap_M5.md`](./aios_roadmap_M5.md) | **AIOS plan** P0–P7 · weekly table · iteration bar (**M5** · HITL closed) |
| [`AIOS_SIGNOFF_M5.md`](./AIOS_SIGNOFF_M5.md) | **HITL** M5 research OS arm · **DE40_5m_stack** · magic **26151907** |
| [`aos_l2_policy_M5.md`](./aos_l2_policy_M5.md) | M5 L2det v1b ARM map (P2) |
| [`aos_l3l4_policy_M5.md`](./aos_l3l4_policy_M5.md) | M5 L3 halt / L4 health bus (P3) |
| [`aos_l6_ledger_M5.md`](./aos_l6_ledger_M5.md) | M5 L6 ledger + det stack (P4) |
| [`aos_l5_retrain_M5.md`](./aos_l5_retrain_M5.md) | M5 L5 retrain / rollback (P5) |
| [`aos_p6_harden_M5.md`](./aos_p6_harden_M5.md) | M5 L9 soft veto · L2 ±10% · ATR G3 (P6) |
| [`DE40_M5_AOS_BASELINE_v1.md`](./DE40_M5_AOS_BASELINE_v1.md) | M5 frozen baseline · tip May→Oct authority |
| [`aos_bad_cells_M5.md`](./aos_bad_cells_M5.md) | M5 L2det seeds (Feb / Oct / H14–16 / BUY caution · P1) |
| [`aos_cost_policy_M5.md`](./aos_cost_policy_M5.md) | M5 Leak prior **7.0 pp** · measured OPEN |
| [`aos_l1_tape_contract_M5.md`](./aos_l1_tape_contract_M5.md) | M5 L1 feature schema v0 |
| [`tapes/`](./tapes/) | M15 + **M5** fire tapes |
| [`DE40_AOS_BASELINE_v1.md`](./DE40_AOS_BASELINE_v1.md) | Frozen engine baseline for OS Δ (P0-T01) |
| [`aos_bad_cells.md`](./aos_bad_cells.md) | L2det seeds (Feb / H13 / MISMATCH / … · P1-updated) |
| [`aos_cost_policy.md`](./aos_cost_policy.md) | Leak prior 9.8 pp · journal proxy · measured OPEN |
| [`aos_l1_tape_contract.md`](./aos_l1_tape_contract.md) | L1 feature schema v0 |
| [`aos_l2_policy.md`](./aos_l2_policy.md) | L2det / L2AI ARM map (P2) |
| [`aos_l2_size_table.md`](./aos_l2_size_table.md) | f multipliers (spec) |
| [`aos_l3l4_policy.md`](./aos_l3l4_policy.md) | L3 halt / L4 health bus (P3) |
| [`aos_l6_ledger.md`](./aos_l6_ledger.md) | L6 ledger + stack CF (P4) |
| [`aos_l5_retrain.md`](./aos_l5_retrain.md) | L5 retrain store · champ/challenger · rollback (P5) |
| [`aos_p6_harden.md`](./aos_p6_harden.md) | L9 soft veto · L2 ±10% stress · ATR G3 (P6) |
| [`AIOS_SIGNOFF.md`](./AIOS_SIGNOFF.md) | **HITL** research OS arm · **DE40stack** · magic **26141907** |
| [`tapes/`](./tapes/) | Tip (77) · YTD (147) · ledger shadow |
| Chart preset card | `doc/BMRG_M15_DE40_6M_chart_preset.md` |
| Blotter | `DE40-P0-CHART/` · `DE40-AOS-P1/`…`P7/` |

**Presets:** `MQL5/Profiles/Tester/BMRG/DE40/` · also `Experts/BMRG/Presets/`  
**Parent maths:** `doc/unified_edge_framework.md` · layer vocab `doc/ai_OS.md`  
**Benchmark:** score under [`edge_framework.md`](./edge_framework.md) — Canvas display only.  
**Scope:** asset-list **expansion** · **Balanced P0 AOS OFF** · **not** a live replace.  
**AIOS:** **P7 HITL SIGNED** — **`DE40stack`** armed · magic **26141907** · L2 AI DISARM · measured Leak OPEN.

| Sleeve | Preset | Magic | RR | BWR | Pool |
| --- | --- | ---: | ---: | ---: | --- |
| **Balanced P0 ★** | `BMRG-M15-DE40-6M-P0_balanced_chart.set` | **26101902** | 1.25 | 44.4% | **EXPANSION_KEEP** · OS baseline |
| Research OS P4 | `BMRG-M15-DE40-6M-P4_research_OS_W50.set` | **26141904** | 1.25 | 44.4% | pre-HITL L3/L4/ledger |
| **DE40stack ★** | **`DE40stack.set`** (= P7 ARMED) | **26141907** | 1.25 | 44.4% | **HITL research OS** |
| **M5 Balanced P0** | `BMRG-M5-DE40-6M-P0_balanced_chart.set` | **26101903** | 1.25 | 44.4% | Expansion engine |
| M5 research OS P4 | `BMRG-M5-DE40-6M-P4_research_OS_W50.set` | **26151904** | 1.25 | 44.4% | pre-HITL L2det v1b |
| **DE40_5m_stack ★** | **`DE40_5m_stack.set`** (= P7 ARMED) | **26151907** | 1.25 | 44.4% | **HITL research OS M5** |

Evidence (M15): Tester `logs/20261019.log` DE30 chunks (scored 2026-10-19). Broker tip from **2025.06.05**. Live spread ≈1020 pts → prior Leak 9.8 pp (journal proxy understates).  
Evidence (M5): Tester `logs/20261020.log` · Jan→Aug · Leak prior **7.0 pp** · see [`system_profile_M5.md`](./system_profile_M5.md) · blotter `DE40-M5-P0/`.
