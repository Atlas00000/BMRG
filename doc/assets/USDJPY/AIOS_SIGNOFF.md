# USDJPY AIOS sign-off (research OS — USDJPYstack)

**HITL signed:** 2026-10-19 (operator confirmation in chat — “proceed with P7” + name **USDJPYstack**)  
**Packet:** `USDJPY_M15_AOS_RESEARCH_v1` · `blotter/archive/USDJPY-AOS-P7/promotion_packet.json`  
**Verdict:** **ARM_RESEARCH_OS** — USDJPY M15 expansion sleeve only · **not** live FX replace · **not** PRODUCTION-WORTHY

---

## Armed research attach

| | |
| --- | --- |
| **Preset (canonical)** | **`USDJPYstack.set`** |
| **Also** | `BMRG-M15-USDJPY-6M-P7_research_OS_ARMED.set` |
| **Tester (MT5)** | `MQL5/Profiles/Tester/BMRG/USDJPY/USDJPYstack.set` |
| **Presets** | `Experts/BMRG/Presets/USDJPYstack.set` |
| **Magic** | **26131807** |
| **Risk / lot** | 0.5% · **0.01** |
| Engine | Balanced P0 · SL/TP 100/120 · RR 1.20 · BB 2.2 · session 12–20 · skip Tue · ATR max **70** |
| AOS | ON · **LIVE_WITHHOLD** · L3/L4 · ledger · W50 |
| **L2** | **`L2det_usdjpy_v1c`** (nearATR @ 0.9×70 **OR** H16) · L2 AI **DISARM** · Jul **off** |
| Leak / BWR / R | **11.4** (prior) / 45.5 / 1.20 |
| EA | Compile `BMRG.mq5` with `Include/AOS_L2det_usdjpy.mqh` |

**Chart / Tester:** USDJPY M15 · load **USDJPYstack** · dates e.g. **2026.05.01 → tip**.  
Ledger → `COMMON\Files\BMRG_AOS_ledger_26131807.csv`.

Engine-only baseline remains magic **26101828** / P0 balanced (AOS OFF).  
P4 pre-HITL twin: magic **26131804** / `…P4_research_OS_W50.set`.

---

## HITL acknowledgements (signed)

1. Not a replace for AUDUSD / EURUSD / UK100 / DE40 live or research books.  
2. Expansion research arm only — full G0–G5 production admit **deferred**.  
3. Leak still **prior 11.4 pp** (deal-measured OPEN).  
4. L2 AI remains **DISARM** (AUC≈0.47 · CHALLENGER EMPTY).  
5. L9 H14 / spread / Jul approved as **shadow only** — **not** LIVE in this arm.  
6. No foreign L2 pins · do **not** reopen Tokyo / lift ATR max.

---

## Evidence snapshot

| Source | Result |
| --- | --- |
| Engine tip (path) | n46 · WR 50% · E_N **+0.10R** · EF_prior **−6.9 pp** |
| Offline L2det v1c tip | n37 · WR 62.2% · E_N **+0.37R** · ΔE_N **+0.27R** · ret 80.4% · L3 halt **0** |
| P3 L3/L4 | tip+YTD trip-free on v1c |
| P6 harden | nearATR keep **0.9/70+H16** · ATR G3 PASS · L9 no LIVE |

---

## P7-T03 — Paper / tiny-f checklist

Before any paper or tiny-f chart attach:

- [ ] Compile `BMRG.mq5` · confirm Inputs show `InpAOS_USDJPY_L2detEnable=true`  
- [ ] Load **USDJPYstack.set** · magic **26131807** · symbol **USDJPY** M15  
- [ ] Confirm `InpAiOsMode=LIVE_WITHHOLD` · kill-switch **false** · L2AI **false**  
- [ ] ATR max **70** · session 12–20 · skip Tue · BBDev 2.2  
- [ ] Lot **0.01** · risk 0.5%  
- [ ] Ledger path writable (`COMMON\Files`)  
- [ ] Rollback known: AOS off → P0 balanced · or `InpAOS_USDJPY_L2detEnable=false`  
- [ ] Do **not** attach this `.set` to live AUD/EUR/UK/DE charts  
- [ ] Do **not** reopen Tokyo or lift ATR max  

Optional paper: same stack · demo · monitor 2 tip weeks before any capital.

---

## Rollback

| Intent | Action |
| --- | --- |
| Det off | `InpAOS_USDJPY_L2detEnable=false` |
| AOS off | `InpAOS_Enable=false` · P0 balanced `.set` |
| Kill L2 mode | `InpAiKillSwitch=true` |
| AI pin | `rollback_l2skip_usdjpy.py rollback --to DISARM` (AI unused in this arm) |

---

## Related docs

`aos_l2_policy.md` · `aos_l3l4_policy.md` · `aos_l6_ledger.md` · `aos_l5_retrain.md` · `aos_p6_harden.md` · `aios_roadmap.md` · `edge_framework.md`
