# UK100 AIOS sign-off (research OS)

**HITL signed:** 2026-10-13 (operator confirmation in chat)  
**Packet:** `UK100_AOS_RESEARCH_v1` · `blotter/archive/UK100-AOS-P7/promotion_packet.json`  
**Verdict:** **ARM_RESEARCH_OS** — expansion sleeve only · **not** FX live replace · **not** PRODUCTION-WORTHY

---

## Armed research attach

| | |
| --- | --- |
| **Preset** | `Profiles/Tester/BMRG/BMRG-M15-UK100-6M-P7_research_OS_ARMED.set` (also under `UK100/`) |
| **Magic** | **26111307** |
| **Risk / lot** | 0.5% · fixed **0.1** (broker min) |
| Engine | Balanced P0 · SL/TP 2500/3125 · RR 1.25 · session 08–17 · skip Tue · ATR max **1470** |
| AOS | ON · **LIVE_WITHHOLD** · L3/L4 · ledger · W50 |
| **L2** | **`L2det_uk_v1b`** (Thu ∨ BUY∧nearATR) · L2 AI **DISARM** |
| Leak / BWR / R | **4.27** (journal proxy) / 44.4 / 1.25 |
| EA | `Experts\BMRG\BMRG.ex5` ≥ **1.23** |

**Chart / Tester:** UK100 M15 · load P7 `.set` · dates covering tip (e.g. 2026.05.01 → tip). Ledger → `COMMON\Files\BMRG_AOS_ledger_26111307.csv`.

Engine-only baseline remains magic **26101201** / P0 balanced (AOS OFF).

---

## HITL acknowledgements (signed)

1. Not a replace for EURUSD / AUDUSD live books.  
2. Expansion research arm only — full G0–G5 production admit **deferred**.  
3. Leak still **journal proxy** (measured deal Leak OPEN).  
4. L2 AI remains **DISARM** (tip AUC ~0.39).  
5. Broker history truncated (`hist_from` ≥ 2025.12.17).  
6. L9 BUY∧H08 approved as **shadow candidate** — **not** LIVE in this arm.

---

## Evidence snapshot

| Source | Result |
| --- | --- |
| Engine tip May–Aug | n51 · E_N +0.10R · EF_journal +0.31 pp |
| Offline L2det v1b tip | n33 · E_N **+0.36R** · ΔE_N +0.26R |
| Tester OS 2026 Jan–Oct (mag 26111304) | 97 FIRE / 81 SKIP · tip E_N **+0.32R** · bal 561.82 · 0 Thu fires · 0 L3 |
| P6 harden | nearATR keep 0.9/1470 · ATR G3 PASS |

---

## P7-T03 — Paper / tiny-f checklist

Before any paper or tiny-f chart attach:

- [ ] Compile `BMRG.mq5` ≥ 1.23 · confirm Inputs show `InpAOS_UK_L2detEnable=true`  
- [ ] Load **P7** `.set` · magic **26111307** · symbol **UK100** M15  
- [ ] Confirm `InpAiOsMode=LIVE_WITHHOLD` · kill-switch **false** · L2AI **false**  
- [ ] ATR max **1470** · session 08–17 · skip Tue  
- [ ] Lot **0.1** · deposit sized so 1R ≈ 0.5% (or accept fixed lot)  
- [ ] Ledger path writable (`COMMON\Files`)  
- [ ] Rollback known: AOS off → P0 set · or `InpAOS_UK_L2detEnable=false`  
- [ ] Do **not** raise risk% toward live FX books without a new packet  

Optional paper: same stack · demo account · monitor 2 tip weeks before any capital.

---

## Rollback

| Intent | Action |
| --- | --- |
| Det off | `InpAOS_UK_L2detEnable=false` |
| AOS off | `InpAOS_Enable=false` · P0 balanced `.set` |
| Kill L2 mode | `InpAiKillSwitch=true` |
| AI pin | `rollback_l2skip_uk.py rollback --to DISARM` (AI unused in this arm) |

---

## Related docs

`aos_l2_policy.md` · `aos_l3l4_policy.md` · `aos_l6_ledger.md` · `aos_l5_retrain.md` · `aos_p6_harden.md` · `aios_roadmap.md` · `edge_framework.md`
