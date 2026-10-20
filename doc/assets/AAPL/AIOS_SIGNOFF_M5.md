# AAPL M5 AIOS sign-off (research OS)

**HITL signed:** 2026-10-20 (operator confirmation in chat — proceed P7 + **AAPL_5m_stack**)  
**Packet:** `AAPL_M5_AOS_RESEARCH_v1` · `blotter/archive/AAPL-M5-AOS-P7/promotion_packet.json`  
**Verdict:** **ARM_RESEARCH_OS** — tip WATCH expansion sleeve only · **not** M15 Harvest replace · **not** FX live replace · **not** PRODUCTION-WORTHY

---

## Armed research attach

| | |
| --- | --- |
| **Preset (final)** | **`AAPL_5m_stack.set`** |
| Alias | `BMRG-M5-AAPL-6M-P7_research_OS_ARMED.set` |
| Paths | `Experts/BMRG/Presets/` · **`MQL5/Profiles/Tester/BMRG/AAPL/`** (Tester load path) |
| **Magic** | **26162017** |
| **Risk / lot** | 0.5% · fixed **1.0** (Apple min) |
| Engine | Balanced P0 M5 · SL/TP **190/280** · RR≈1.47 · session 14–20 · skip Tue · ATR **24–98** · BBw **0.30–2.00** |
| AOS | ON · **LIVE_WITHHOLD** · L3/L4 · ledger · W50 |
| **L2** | **`L2det_aapl_m5_v1b`** (Jul ∨ Wed) · L2 AI **DISARM** |
| Leak / BWR / R | **15.3** (profile) / 40.4 / 1.47 |
| EA | `Experts\BMRG\BMRG.ex5` ≥ **1.24** · `Include/AOS_L2det_aapl_m5.mqh` |

**Chart / Tester:** Apple **M5** · load `AAPL_5m_stack.set` · dates covering tip (e.g. 2026.05.01 → 2026.10.19). Ledger → `COMMON\Files\BMRG_AOS_ledger_26162017.csv`.

Engine-only baseline remains magic **26102011** / Balanced TPgtSL (AOS OFF).  
M15 Harvest candidate remains magic **26092501** — separate stream · **pool KEEP**.

---

## HITL acknowledgements (signed)

1. Not a replace for M15 Harvest candidate or EUR / AUD / DE40 / UK live books.  
2. Not a twin of M15 `L2det_aapl` Thu/18 — M5 map is **Jul ∨ Wed** only.  
3. Expansion research arm only — full G0–G5 production admit **deferred**.  
4. Leak still **profile 15.3 pp** (measured deal Leak OPEN) · Stage-1 **Fragile**.  
5. EF_profile under Leak still **&lt; 0** on det stack (−2.1 pp) — no Robust claim.  
6. L2 AI remains **DISARM** (tip AUC ~0.50).  
7. L9 RTH / spread approved as **shadow only** — **not** LIVE in this arm.  
8. Never thin SL under fat spread · never borrow M15 Thu/18 on M5.

---

## Evidence snapshot

| Source | Result |
| --- | --- |
| Engine tip May→Oct | n77 · WR 46.8% · E_N **+0.16R** · BM **+6.3 pp** · +$44.50 |
| Offline L2det v1b tip (P2) | n44 · E_N **+0.349R** · ΔE_N +0.193R · ret 57.1% |
| P4 det stack | n_fire **41** · E_N **+0.327R** · EF_profile **−2.1 pp** · life NEAR · L8 21/21 |
| P3 health | P0 tip MaxDD ~8% · v1b MaxDD **2.6%** · 1× BELOW retained |
| P5 AI | AUC 0.501 · DISARM · challenger EMPTY · drill PASS |
| P6 harden | keep v1b · ATR/BBw G3 PASS · L9 no LIVE |

---

## P7-T03 — Paper / tiny-f checklist

Before any paper or tiny-f chart attach:

- [ ] Compile `BMRG.mq5` ≥ **1.24** · confirm Inputs show `InpAOS_AAPL_M5_L2detEnable=true`  
- [ ] Load **`AAPL_5m_stack.set`** · magic **26162017** · symbol **Apple** **M5**  
- [ ] Confirm `InpAiOsMode=LIVE_WITHHOLD` · kill-switch **false** · L2AI **false**  
- [ ] Confirm `InpAOS_AAPL_L2detEnable=false` (M15 Thu/18 map off)  
- [ ] ATR **24–98** · BBw **0.30–2.00** · session 14–20 · skip Tue · MaxSpread 40  
- [ ] Lot **1.0** · deposit sized for equity CFD (or accept fixed lot)  
- [ ] Ledger path writable (`COMMON\Files`)  
- [ ] Rollback known: AOS off → P0 Balanced set · or `InpAOS_AAPL_M5_L2detEnable=false`  
- [ ] Do **not** attach this `.set` to live FX / M15 Harvest charts  
- [ ] Do **not** raise risk% toward live books without a new packet  

Optional paper: same stack · demo account · monitor 2 tip weeks before any capital.

---

## Rollback

| Intent | Action |
| --- | --- |
| Det off | `InpAOS_AAPL_M5_L2detEnable=false` |
| AOS off | `InpAOS_Enable=false` · P0 M5 Balanced `.set` |
| Kill L2 mode | `InpAiKillSwitch=true` |
| AI pin | `rollback_l2skip_aapl_m5.py rollback --to DISARM` (AI unused in this arm) |

---

## Related docs

`aos_l2_policy_M5.md` · `aos_l3l4_policy_M5.md` · `aos_l6_ledger_M5.md` · `aos_l5_retrain_M5.md` · `aos_p6_harden_M5.md` · `aios_roadmap_M5.md` · `edge_framework.md` · `system_profile_M5.md` · `candidate_pool.md`
