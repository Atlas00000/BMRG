# DE40 AIOS sign-off (research OS — DE40stack)

**HITL signed:** 2026-10-19 (operator confirmation in chat — “proceed with P7” + name **DE40stack**)  
**Packet:** `DE40_M15_AOS_RESEARCH_v1` · `blotter/archive/DE40-AOS-P7/promotion_packet.json`  
**Verdict:** **ARM_RESEARCH_OS** — DE40/DE30 M15 expansion sleeve only · **not** live FX/UK replace · **not** PRODUCTION-WORTHY

---

## Armed research attach

| | |
| --- | --- |
| **Preset (canonical)** | **`DE40stack.set`** |
| **Also** | `BMRG-M15-DE40-6M-P7_research_OS_ARMED.set` |
| **Tester (MT5)** | `MQL5/Profiles/Tester/BMRG/DE40/DE40stack.set` |
| **Presets** | `Experts/BMRG/Presets/DE40stack.set` |
| **Magic** | **26141907** |
| **Risk / lot** | 0.5% · fixed **0.1** (DE30 min) |
| Engine | Balanced P0 · SL/TP 5000/6250 · RR 1.25 · BB 2.2 · session 08–17 · skip Tue · ATR max **4070** |
| AOS | ON · **LIVE_WITHHOLD** · L3/L4 · ledger · W50 |
| **L2** | **`L2det_de40_v1_BUY_near_atr`** (BUY∧nearATR @ 0.9×4070) · L2 AI **DISARM** · H13 **off** |
| Leak / BWR / R | **9.8** (prior) / 44.4 / 1.25 |
| EA | Compile `BMRG.mq5` with `Include/AOS_L2det_de.mqh` |

**Chart / Tester:** DE30 M15 · load **DE40stack** · dates e.g. **2026.05.01 → tip**.  
Ledger → `COMMON\Files\BMRG_AOS_ledger_26141907.csv`.

Engine-only baseline remains magic **26101902** / P0 balanced (AOS OFF).  
P4 pre-HITL twin: magic **26141904** / `…P4_research_OS_W50.set`.

---

## HITL acknowledgements (signed)

1. Not a replace for AUDUSD / EURUSD / UK100 live or research books.  
2. Expansion research arm only — full G0–G5 production admit **deferred**.  
3. Leak still **prior 9.8 pp** (deal-measured OPEN).  
4. L2 AI remains **DISARM** (AUC≈0.52 · chrono stall).  
5. L9 Frankfurt / H08 / H13 approved as **shadow only** — **not** LIVE in this arm.  
6. No foreign L2 pins (EUR / UK / AUD / AAPL / INF).

---

## Evidence snapshot

| Source | Result |
| --- | --- |
| Engine tip May→Oct | n77 · WR 58.4% · E_N **+0.31R** · EF_prior **+4.2 pp** |
| Offline L2det ARM tip | n62 · WR 62.9% · E_N **+0.42R** · ΔE_N **+0.10R** · ret 80.5% |
| P3 L3/L4 | tip trip-free on ARM path |
| P6 harden | nearATR keep **0.9/4070** · ATR G3 PASS · L9 no LIVE |

---

## P7-T03 — Paper / tiny-f checklist

Before any paper or tiny-f chart attach:

- [ ] Compile `BMRG.mq5` · confirm Inputs show `InpAOS_DE_L2detEnable=true`  
- [ ] Load **DE40stack.set** · magic **26141907** · symbol **DE30** M15  
- [ ] Confirm `InpAiOsMode=LIVE_WITHHOLD` · kill-switch **false** · L2AI **false**  
- [ ] ATR max **4070** · session 08–17 · skip Tue · BBDev 2.2  
- [ ] Lot **0.1** · risk 0.5%  
- [ ] Ledger path writable (`COMMON\Files`)  
- [ ] Rollback known: AOS off → P0 balanced · or `InpAOS_DE_L2detEnable=false`  
- [ ] Do **not** attach this `.set` to live FX / UK charts  

Optional paper: same stack · demo · monitor 2 tip weeks before any capital.

---

## Rollback

| Intent | Action |
| --- | --- |
| Det off | `InpAOS_DE_L2detEnable=false` |
| AOS off | `InpAOS_Enable=false` · P0 balanced `.set` |
| Kill L2 mode | `InpAiKillSwitch=true` |
| AI pin | `rollback_l2skip_de40.py rollback --to DISARM` (AI unused in this arm) |

---

## Related docs

`aos_l2_policy.md` · `aos_l3l4_policy.md` · `aos_l6_ledger.md` · `aos_l5_retrain.md` · `aos_p6_harden.md` · `aios_roadmap.md` · `edge_framework.md`
