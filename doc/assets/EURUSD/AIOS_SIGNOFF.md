# EURUSD M15 AIOS sign-off (research OS)

**HITL signed:** 2026-10-18 (operator confirmation in chat — “proceed with P7”)  
**Packet:** `EURUSD_M15_AOS_RESEARCH_v1` · `blotter/archive/EURUSD-AOS-P7/promotion_packet.json`  
**Verdict:** **ARM_RESEARCH_OS** — M15 expansion sleeve only · **not** M5 Harvest live replace · **not** PRODUCTION-WORTHY

---

## Armed research attach

| | |
| --- | --- |
| **Preset (Tester)** | `Profiles/Tester/BMRG/EURUSD/BMRG-M15-EURUSD-6M-P7_research_OS_ARMED.set` |
| **Also** | `Experts/BMRG/Presets/BMRG-M15-EURUSD-6M-P7_research_OS_ARMED.set` |
| **Magic** | **26121807** |
| **Risk / lot** | 0.5% · fixed **0.01** |
| Engine | P2 light · SL/TP 300/375 · RR 1.25 · BB 2.3 · CD 3 · session 12–20 · skip Tue · ATR max **74** |
| AOS | ON · **LIVE_WITHHOLD** · L3/L4 · ledger · W50 |
| **L2** | **`L2det_eur_m15_v1b`** (Thu ∨ BUY∧nearATR) · L2 AI **DISARM** |
| Leak / BWR / R | **1.19** (journal proxy) / 44.4 / 1.25 |
| EA | Compile `BMRG.mq5` with `Include/AOS_L2det_eur.mqh` |

**Chart / Tester:** EURUSD M15 · load **P7** `.set` · dates e.g. **2026.05.01 → tip**.  
Ledger → `COMMON\Files\BMRG_AOS_ledger_26121807.csv`.

Engine-only baseline remains magic **26101817** / P2 light (AOS OFF).  
P4 pre-HITL twin: magic **26121804** / `…P4_research_OS_W50.set`.

---

## HITL acknowledgements (signed)

1. Not a replace for EURUSD **M5 Harvest** live books (`8210xxx` / `8399xxx`).  
2. Expansion research arm only — full G0–G5 production admit **deferred**.  
3. Leak still **journal proxy** 1.19 pp (measured deal Leak + **swap** OPEN).  
4. L2 AI remains **DISARM** (chrono holdout).  
5. L9 H19 approved as **shadow candidate** — **not** LIVE in this arm.  
6. No foreign L2 pins (AUD / UK100 / AAPL / M5).

---

## Evidence snapshot

| Source | Result |
| --- | --- |
| Engine tip May→Oct | n45 · WR 46.7% · E_N **+0.05R** · EF_journal **+1.04 pp** |
| Offline L2det v1b tip | n31 · WR 54.8% · E_N **+0.234R** · ΔE_N **+0.184R** · ret 69% |
| P3 L3/L4 | v1b tip trip-free (P0 had 1× BELOW) |
| P6 harden | nearATR keep **0.9/74** · ATR G3 PASS · H19 SHADOW |

---

## P7-T03 — Paper / tiny-f checklist

Before any paper or tiny-f chart attach:

- [ ] Compile `BMRG.mq5` · confirm Inputs show `InpAOS_EUR_L2detEnable=true`  
- [ ] Load **P7** `.set` · magic **26121807** · symbol **EURUSD** M15  
- [ ] Confirm `InpAiOsMode=LIVE_WITHHOLD` · kill-switch **false** · L2AI **false**  
- [ ] ATR max **74** · session 12–20 · skip Tue · BBDev 2.3 · CD 3  
- [ ] Lot **0.01** · risk 0.5%  
- [ ] Ledger path writable (`COMMON\Files`)  
- [ ] Rollback known: AOS off → P2 light set · or `InpAOS_EUR_L2detEnable=false`  
- [ ] Do **not** attach this `.set` to M5 Harvest live charts  

Optional paper: same stack · demo · monitor 2 tip weeks before any capital.

---

## Rollback

| Intent | Action |
| --- | --- |
| Det off | `InpAOS_EUR_L2detEnable=false` |
| AOS off | `InpAOS_Enable=false` · P2 light `.set` |
| Kill L2 mode | `InpAiKillSwitch=true` |
| AI pin | `rollback_l2skip_eur_m15.py rollback --to DISARM` (AI unused in this arm) |

---

## Related docs

`aos_l2_policy.md` · `aos_l3l4_policy.md` · `aos_l6_ledger.md` · `aos_l5_retrain.md` · `aos_p6_harden.md` · `aios_roadmap.md` · `edge_framework.md`
