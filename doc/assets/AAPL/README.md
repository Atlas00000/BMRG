# AAPL asset docs

Equity-CFD expansion research for **Apple** (MT5 ticker often `Apple`). Separate from AUDUSD / EURUSD live books and from root `system_profile.md`.

| Doc | Role |
| --- | --- |
| [`candidate_pool.md`](./candidate_pool.md) | **Current candidate lock** (M15 Harvest baseline) |
| [`system_profile.md`](./system_profile.md) | M15 · Harvest + Balanced (descriptive) |
| [`system_profile_M5.md`](./system_profile_M5.md) | **M5 Balanced TPgtSL** · class · trade · rolling · metrics |
| [`edge_framework.md`](./edge_framework.md) | **Normative** AAPL binding of `unified_edge_framework.md` |
| [`aios_roadmap.md`](./aios_roadmap.md) | **M15** Harvest AIOS (optional vs KEEP candidate) |
| [`BUILD_PLAN.md`](./BUILD_PLAN.md) | M15 compile/test L2det Thu·18 |
| [`aios_roadmap_M5.md`](./aios_roadmap_M5.md) | **M5** Balanced AIOS · P0–P7 **HITL ARMED** · tip WATCH |
| [`AIOS_SIGNOFF_M5.md`](./AIOS_SIGNOFF_M5.md) | HITL · **`AAPL_5m_stack`** · magic **26162017** |
| [`BUILD_PLAN_M5.md`](./BUILD_PLAN_M5.md) | M5 compile/test plan (L2det_m5 · no Thu/18 transplant) |
| [`AAPL_M5_AOS_BASELINE_v1.md`](./AAPL_M5_AOS_BASELINE_v1.md) | Frozen M5 P0 scorecard |
| [`aos_bad_cells_M5.md`](./aos_bad_cells_M5.md) | M5 L2det seed registry |
| [`aos_cost_policy_M5.md`](./aos_cost_policy_M5.md) | M5 Leak ~15.3 pp stub · measured OPEN |
| [`aos_l1_tape_contract_M5.md`](./aos_l1_tape_contract_M5.md) | M5 L1 schema v0 · P1 **DONE** |
| [`tapes/`](./tapes/) | `aapl_m5_*_fire_tape_v0.csv` |
| [`aos_l2_policy_M5.md`](./aos_l2_policy_M5.md) | M5 L2det v1b Jul∨Wed **ARM** · L2AI DISARM |
| [`aos_l3l4_policy_M5.md`](./aos_l3l4_policy_M5.md) | M5 L3/L4 **SIGNED** · DD25 · W15/W20/W50 |
| [`aos_l6_ledger_M5.md`](./aos_l6_ledger_M5.md) | M5 P4 ledger · det_v1b · magic **26162014** |
| [`aos_l5_retrain_M5.md`](./aos_l5_retrain_M5.md) | M5 P5 L2skip store · AUC≈0.501 DISARM · rollback PASS |
| [`aos_p6_harden_M5.md`](./aos_p6_harden_M5.md) | M5 P6 L9 no LIVE · v1b keep · ATR/BBw G3 |

**Presets:** `MQL5/Profiles/Tester/BMRG/AAPL/` · **`AAPL_5m_stack.set`** (research OS)  
**Parent maths:** `doc/unified_edge_framework.md`  
**Scope:** asset-list **expansion** · **candidate = M15 Harvest AOS OFF** · M5 = tip research WATCH **HITL ARMED** · **not** a live replace.  
**Benchmark:** [`edge_framework.md`](./edge_framework.md) — Canvas display only.

| Sleeve | Preset | Magic | RR | BWR | Pool |
| --- | --- | ---: | ---: | ---: | --- |
| **Harvest M15 (candidate)** | `BMRG-M15-AAPL-6M-Harvest_RR1.25.set` | **26092501** | 1.25 | 44.4% | **KEEP** |
| Balanced M15 | `BMRG-M15-AAPL-6M-Balanced_RR1.5.set` | 26092502 | 1.50 | 40.0% | WATCH |
| **Balanced M5 (engine)** | `BMRG-M5-AAPL-6M-Balanced_TPgtSL.set` | **26102011** | ≈1.47 | 40.4% | WATCH |
| **M5 research OS** | **`AAPL_5m_stack.set`** | **26162017** | ≈1.47 | 40.4% | **WATCH HITL** |

Evidence: M15 `logs/20261012.log` · M5 `logs/20261020.log` (scored 2026-10-20).
