# BMRG Tester — DE40 / DE30

## M15

| Item | Value |
| --- | --- |
| Symbol (MT5) | **DE30** (canonical Ouroboros DE40) |
| Chart TF | M15 |
| Engine preset | `BMRG-M15-DE40-6M-P0_balanced_chart.set` · magic **26101902** · AOS OFF |
| **Research OS** | **`DE40stack.set`** · magic **26141907** · HITL P7 |
| Alias | `BMRG-M15-DE40-6M-P7_research_OS_ARMED.set` (same contents) |
| Pre-HITL | `BMRG-M15-DE40-6M-P4_research_OS_W50.set` · magic **26141904** |
| Dates (tip) | 2026.05.01 → tip |
| Geometry | SL 5000 / TP 6250 (RR 1.25) · ATR max 4070 · session 08–17 · skip Tue |

**DE40stack:** L2det BUY∧nearATR LIVE_WITHHOLD · L3/L4 · ledger W50 · L2AI DISARM.  
Compile `BMRG.mq5` (needs `AOS_L2det_de.mqh`) before Tester.

Sign-off: `Experts/BMRG/doc/assets/DE40/AIOS_SIGNOFF.md`

## M5

| Item | Value |
| --- | --- |
| Chart TF | **M5** |
| Engine preset | `BMRG-M5-DE40-6M-P0_balanced_chart.set` · magic **26101903** · AOS OFF |
| **Research OS** | **`DE40_5m_stack.set`** · magic **26151907** · HITL P7 |
| Alias | `BMRG-M5-DE40-6M-P7_research_OS_ARMED.set` (same contents) |
| Pre-HITL | `BMRG-M5-DE40-6M-P4_research_OS_W50.set` · magic **26151904** |
| Dates (tip) | 2026.05.01 → 2026.10.19 |
| Geometry | SL 7000 / TP 8750 (RR 1.25) · ATR max **2380** · session 08–17 · skip Tue |

**DE40_5m_stack:** L2det_de40_m5_v1b ((BUY∧H14\|16)∨(BUY∧Oct)) · L3/L4 · ledger W50 · L2AI DISARM.  
Compile `BMRG.mq5` (needs `AOS_L2det_de_m5.mqh`) before Tester. Not a twin of M15 `DE40stack`.

Sign-off: `Experts/BMRG/doc/assets/DE40/AIOS_SIGNOFF_M5.md`
