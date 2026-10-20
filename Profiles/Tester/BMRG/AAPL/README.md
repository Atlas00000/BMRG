# BMRG Tester — AAPL / Apple

## M5

| Item | Value |
| --- | --- |
| Symbol (MT5) | **Apple** (canonical AAPL) |
| Chart TF | **M5** |
| Engine preset | `BMRG-M5-AAPL-6M-Balanced_TPgtSL.set` · magic **26102011** · AOS OFF |
| **Research OS** | **`AAPL_5m_stack.set`** · magic **26162017** · HITL P7 |
| Alias | `BMRG-M5-AAPL-6M-P7_research_OS_ARMED.set` (same contents) |
| Pre-HITL | `BMRG-M5-AAPL-6M-P4_research_OS_W50.set` · magic **26162014** |
| Dates (tip) | 2026.05.01 → 2026.10.19 |
| Geometry | SL 190 / TP 280 (RR≈1.47) · ATR **24–98** · BBw **0.30–2.00** · session 14–20 · skip Tue |

**AAPL_5m_stack:** L2det_aapl_m5_v1b (Jul ∨ Wed) · L3/L4 · ledger W50 · L2AI DISARM.  
Compile `BMRG.mq5` (needs `AOS_L2det_aapl_m5.mqh`) before Tester. Not M15 Harvest / Thu·18.

Sign-off: `Experts/BMRG/doc/assets/AAPL/AIOS_SIGNOFF_M5.md`

## M15 (sibling — do not mix)

Pool **KEEP** candidate: Harvest magic **26092501**. See `doc/assets/AAPL/candidate_pool.md`.
