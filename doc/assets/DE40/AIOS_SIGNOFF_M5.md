# DE40 M5 AIOS sign-off (research OS)

**HITL signed:** 2026-10-20 (operator confirmation in chat — proceed P7 + **DE40_5m_stack**)  
**Packet:** `DE40_M5_AOS_RESEARCH_v1` · `blotter/archive/DE40-M5-AOS-P7/promotion_packet.json`  
**Verdict:** **ARM_RESEARCH_OS** — expansion sleeve only · **not** FX/UK live replace · **not** M15 DE40stack twin · **not** PRODUCTION-WORTHY

---

## Armed research attach

| | |
| --- | --- |
| **Preset (final)** | **`DE40_5m_stack.set`** |
| Alias | `BMRG-M5-DE40-6M-P7_research_OS_ARMED.set` |
| Paths | `Presets/` · `Profiles/Tester/BMRG/DE40/` |
| **Magic** | **26151907** |
| **Risk / lot** | 0.5% · fixed **0.1** (DE30 min) |
| Engine | Balanced P0 M5 · SL/TP **7000/8750** · RR 1.25 · session 08–17 · skip Tue · ATR max **2380** |
| AOS | ON · **LIVE_WITHHOLD** · L3/L4 · ledger · W50 |
| **L2** | **`L2det_de40_m5_v1b`** ((BUY∧H14\|16)∨(BUY∧Oct)) · L2 AI **DISARM** |
| Leak / BWR / R | **7.0** (prior) / 44.4 / 1.25 |
| EA | `Experts\BMRG\BMRG.ex5` ≥ **1.24** · `Include/AOS_L2det_de_m5.mqh` |

**Chart / Tester:** DE30 **M5** · load `DE40_5m_stack.set` · dates covering tip (e.g. 2026.05.01 → 2026.10.19). Ledger → `COMMON\Files\BMRG_AOS_ledger_26151907.csv`.

Engine-only baseline remains magic **26101903** / P0 balanced (AOS OFF).  
M15 research OS remains magic **26141907** / **`DE40stack`** — separate stream.

---

## HITL acknowledgements (signed)

1. Not a replace for EURUSD / AUDUSD / UK100 live or research books.  
2. Not a twin of DE40 **M15** research OS / `DE40stack` / `L2det` BUY∧nearATR.  
3. Expansion research arm only — full G0–G5 production admit **deferred**.  
4. Leak still **prior 7.0 pp** (measured deal Leak OPEN).  
5. L2 AI remains **DISARM** (tip AUC ~0.51).  
6. L9 Frankfurt / H13 / spread approved as **shadow only** — **not** LIVE in this arm.  
7. Never thin SL under fat spread · never borrow M15 L2det on M5.

---

## Evidence snapshot

| Source | Result |
| --- | --- |
| Engine tip May→Oct | n123 · WR 53.7% · E_N **+0.207R** · EF_prior **+2.2 pp** · +$208 |
| Offline L2det v1b tip (P2) | n110 · E_N **+0.289R** · ΔE_N +0.081R · ret 89.4% |
| P4 det stack | n_fire **104** · E_N **+0.298R** · EF **+6.25 pp** · life STABLE |
| P3 health | P0 tip 1× BELOW · v1b ends NEAR (improved) |
| P5 AI | AUC 0.51 · DISARM · challenger EMPTY · drill PASS |
| P6 harden | keep v1b · ATR 2380 G3 PASS · L9 no LIVE |

---

## P7-T03 — Paper / tiny-f checklist

Before any paper or tiny-f chart attach:

- [ ] Compile `BMRG.mq5` ≥ **1.24** · confirm Inputs show `InpAOS_DE_M5_L2detEnable=true`  
- [ ] Load **`DE40_5m_stack.set`** · magic **26151907** · symbol **DE30** **M5**  
- [ ] Confirm `InpAiOsMode=LIVE_WITHHOLD` · kill-switch **false** · L2AI **false**  
- [ ] Confirm `InpAOS_DE_L2detEnable=false` (M15 map off)  
- [ ] ATR max **2380** · session 08–17 · skip Tue · MaxSpread 1500  
- [ ] Lot **0.1** · deposit sized so 1R ≈ 0.5% (or accept fixed lot)  
- [ ] Ledger path writable (`COMMON\Files`)  
- [ ] Rollback known: AOS off → P0 M5 set · or `InpAOS_DE_M5_L2detEnable=false`  
- [ ] Do **not** attach this `.set` to live FX / UK / M15 DE charts  
- [ ] Do **not** raise risk% toward live FX books without a new packet  

Optional paper: same stack · demo account · monitor 2 tip weeks before any capital.

---

## Rollback

| Intent | Action |
| --- | --- |
| Det off | `InpAOS_DE_M5_L2detEnable=false` |
| AOS off | `InpAOS_Enable=false` · P0 M5 balanced `.set` |
| Kill L2 mode | `InpAiKillSwitch=true` |
| AI pin | `rollback_l2skip_de40_m5.py rollback --to DISARM` (AI unused in this arm) |

---

## Related docs

`aos_l2_policy_M5.md` · `aos_l3l4_policy_M5.md` · `aos_l6_ledger_M5.md` · `aos_l5_retrain_M5.md` · `aos_p6_harden_M5.md` · `aios_roadmap_M5.md` · `edge_framework.md` · `system_profile_M5.md`
