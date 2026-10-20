# USDJPY asset docs (M15 chart expansion)

Yen-major expansion research for **USDJPY** (Point≈0.001 · Digits=3). Separate from EURUSD M5 Harvest / M15 OS, AUDUSD LIVE, UK100 research OS, and root `system_profile.md`.

| Doc | Role |
| --- | --- |
| [`edge_framework.md`](./edge_framework.md) | **Normative** USDJPY M15 binding of `unified_edge_framework.md` (gates, gaps, canvas caveat) |
| [`system_profile.md`](./system_profile.md) | Class · edge · trade · rolling · performance · key metrics (descriptive) |
| [`aios_roadmap.md`](./aios_roadmap.md) | **AIOS plan** P0–P7 · weekly table · iteration bar |
| [`USDJPY_AOS_BASELINE_v1.md`](./USDJPY_AOS_BASELINE_v1.md) | Frozen engine baseline for OS Δ (P0-T01) |
| [`aos_bad_cells.md`](./aos_bad_cells.md) | L2det seed registry (Thu / H14 / Jul / SELL∧near_atr / …) |
| [`aos_cost_policy.md`](./aos_cost_policy.md) | Leak policy · prior 11.4 pp · measured OPEN |
| [`aos_l1_tape_contract.md`](./aos_l1_tape_contract.md) | L1 feature schema v0 (P1-T01) |
| [`aos_l2_policy.md`](./aos_l2_policy.md) | L2det / L2AI ARM map (P2) |
| [`aos_l2_size_table.md`](./aos_l2_size_table.md) | Lifecycle f multipliers (spec · wire after L4) |
| [`aos_l3l4_policy.md`](./aos_l3l4_policy.md) | L3 halt + L4 health bus (P3) |
| [`aos_l6_ledger.md`](./aos_l6_ledger.md) | L6 ledger + det stack CF (P4) |
| [`aos_l5_retrain.md`](./aos_l5_retrain.md) | L5 retrain / champ–challenger / rollback (P5) |
| [`aos_p6_harden.md`](./aos_p6_harden.md) | L9 / L2 stress / ATR G3 (P6) |
| [`AIOS_SIGNOFF.md`](./AIOS_SIGNOFF.md) | HITL research OS arm — **USDJPYstack** (P7) |
| [`tapes/`](./tapes/) | Tip / YTD fire tapes v0 (after re-smoke) |
| Chart preset card | `doc/BMRG_M15_USDJPY_6M_chart_preset.md` |
| Blotter review | `blotter/archive/USDJPY-P0-CHART/` · `…-P1/` … `…-P7/` |

**Presets (inputs only):** `MQL5/Profiles/Tester/BMRG/USDJPY/` · also `Experts/BMRG/Presets/`  
**Parent maths:** `doc/unified_edge_framework.md` · layer vocab `doc/ai_OS.md`  
**Benchmark:** score under [`edge_framework.md`](./edge_framework.md) — Canvas / chat charts are display only.  
**Scope:** asset-list **expansion** · **Balanced P0 AOS OFF** · **not** a live replace.  
**AIOS:** **P7 HITL SIGNED** — **`USDJPYstack`** · magic **26131807** · v1c LIVE_WITHHOLD · L2AI DISARM · measured Leak OPEN.

| Sleeve | Preset | Magic | RR | BWR | Pool |
| --- | --- | ---: | ---: | ---: | --- |
| **Balanced P0 ★** | `BMRG-M15-USDJPY-6M-P0_balanced_chart.set` | **26101828** | 1.20 | 45.5% | **EXPAND_CANDIDATE** · OS baseline |
| P0 exact RR1.25 (alt) | — | 26101829 | 1.25 | 44.4% | design alt · not Tester-scored |
| P0 fire-count BB2.0 (alt) | — | 26101830 | 1.20 | 45.5% | design alt · not Tester-scored |
| Research OS P4 (L3/L4/ledger) | `BMRG-M15-USDJPY-6M-P4_research_OS_W50.set` | **26131804** | 1.20 | 45.5% | L2det offline · Tester OK |
| **Research OS P7 ★** | **`USDJPYstack.set`** | **26131807** | 1.20 | 45.5% | **HITL ARMED** · v1c LIVE_WITHHOLD |

Evidence: Tester `logs/20261019.log` (scored 2026-10-19).
