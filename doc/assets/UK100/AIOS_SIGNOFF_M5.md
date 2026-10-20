# UK100 M5 AIOS sign-off (research OS)

**HITL signed:** 2026-10-20 (operator confirmation in chat)  
**Packet:** `UK100_M5_AOS_RESEARCH_v1` · `blotter/archive/UK100-M5-AOS-P7/promotion_packet.json`  
**Verdict:** **ARM_RESEARCH_OS** — expansion sleeve only · **not** FX live replace · **not** M15 UK twin · **not** PRODUCTION-WORTHY

---

## Armed research attach

| | |
| --- | --- |
| **Preset (final)** | **`UK100_5m_stack.set`** |
| Alias | `BMRG-M5-UK100-6M-P7_research_OS_ARMED.set` |
| Paths | `Presets/` · `Profiles/Tester/BMRG/` · `Profiles/Tester/BMRG/UK100/` |
| **Magic** | **26121907** |
| **Risk / lot** | 0.5% · fixed **0.1** (broker min) |
| Engine | Balanced P0 M5 · SL/TP **1800/2250** · RR 1.25 · session 08–17 · skip Tue · ATR max **869** |
| AOS | ON · **LIVE_WITHHOLD** · L3/L4 · ledger · W50 |
| **L2** | **`L2det_uk_m5_v1b`** ((Mon∧H12–13)∨(SELL∧H12–13)) · L2 AI **DISARM** |
| Leak / BWR / R | **5.93** (journal proxy) / 44.4 / 1.25 |
| EA | `Experts\BMRG\BMRG.ex5` ≥ **1.24** |

**Chart / Tester:** UK100 **M5** · load `UK100_5m_stack.set` · dates covering tip (e.g. 2026.05.01 → tip). Ledger → `COMMON\Files\BMRG_AOS_ledger_26121907.csv`.

Engine-only baseline remains magic **26101905** / P0 balanced (AOS OFF).  
M15 research OS remains magic **26111307** — separate stream.

---

## HITL acknowledgements (signed)

1. Not a replace for EURUSD / AUDUSD live books.  
2. Not a twin of UK100 **M15** research OS / `L2det_uk`.  
3. Expansion research arm only — full G0–G5 production admit **deferred**.  
4. Leak still **journal proxy** 5.93 pp (measured deal Leak OPEN).  
5. L2 AI remains **DISARM** (tip AUC ~0.41).  
6. L9 H14+ / spread_p66 approved as **shadow candidates** — **not** LIVE in this arm.

---

## Evidence snapshot

| Source | Result |
| --- | --- |
| Engine tip May–Aug | n116 · E_N +0.183R · EF_journal +2.22 pp · +$51 |
| Offline L2det v1b tip | n83 · E_N **+0.383R** · ΔE_N +0.199R · L3 trips **0** |
| P3 health | P0 had 1 BELOW · v1b trip-free · last W20 +0.46 |
| P5 AI | AUC 0.41 · DISARM · challenger EMPTY |
| P6 harden | keep H12–13 · ATR 869 G3 PASS · L9 morning DISARM |

---

## P7-T03 — Paper / tiny-f checklist

Before any paper or tiny-f chart attach:

- [ ] Compile `BMRG.mq5` ≥ **1.24** · confirm Inputs show `InpAOS_UK_M5_L2detEnable=true`  
- [ ] Load **`UK100_5m_stack.set`** · magic **26121907** · symbol **UK100** **M5**  
- [ ] Confirm `InpAiOsMode=LIVE_WITHHOLD` · kill-switch **false** · L2AI **false**  
- [ ] Confirm `InpAOS_UK_L2detEnable=false` (M15 map off)  
- [ ] ATR max **869** · session 08–17 · skip Tue  
- [ ] Lot **0.1** · deposit sized so 1R ≈ 0.5% (or accept fixed lot)  
- [ ] Ledger path writable (`COMMON\Files`)  
- [ ] Rollback known: AOS off → P0 M5 set · or `InpAOS_UK_M5_L2detEnable=false`  
- [ ] Do **not** raise risk% toward live FX books without a new packet  

Optional paper: same stack · demo account · monitor 2 tip weeks before any capital.

---

## Rollback

| Intent | Action |
| --- | --- |
| Det off | `InpAOS_UK_M5_L2detEnable=false` |
| AOS off | `InpAOS_Enable=false` · P0 M5 balanced `.set` |
| Kill L2 mode | `InpAiKillSwitch=true` |
| AI pin | `rollback_l2skip_uk_m5.py rollback --to DISARM` (AI unused in this arm) |

---

## Related docs

`aos_l2_policy_M5.md` · `aos_l3l4_policy_M5.md` · `aos_l6_ledger_M5.md` · `aos_l5_retrain_M5.md` · `aos_p6_harden_M5.md` · `aios_roadmap_M5.md` · `edge_framework.md` · `system_profile_M5.md`
