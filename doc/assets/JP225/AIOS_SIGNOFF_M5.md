# JP225 M5 AIOS sign-off (research OS)

**HITL signed:** 2026-10-20 (operator confirmation in chat — proceed P7 + **JPN225_5m_stack**)  
**Packet:** `JP225_M5_AOS_RESEARCH_v1` · `blotter/archive/JP225-M5-AOS-P7/promotion_packet.json`  
**Verdict:** **ARM_RESEARCH_OS** — expansion sleeve only · **not** FX/UK/DE live replace · **not** M15 JPN225stack twin · **not** PRODUCTION-WORTHY

---

## Armed research attach

| | |
| --- | --- |
| **Preset (final)** | **`JPN225_5m_stack.set`** |
| Alias | `BMRG-M5-JP225-6M-P7_research_OS_ARMED.set` |
| Paths | `Presets/` · `Profiles/Tester/BMRG/JP225/` |
| **Magic** | **26161907** |
| **Risk / lot** | 0.5% · fixed **0.1** (JPN225 min) |
| Engine | Growth P0 M5 · SL/TP **25000/50000** · RR 2.00 · session 08–17 · skip Tue · ATR **7610–11285** |
| AOS | ON · **LIVE_WITHHOLD** · L3/L4 · ledger · W50 |
| **L2** | **`L2det_jp225_m5_v1c`** ((BUY∧MATCH Aug/Sep)∨(BUY∧H09\|13\|16)) · L2 AI **DISARM** |
| Leak / BWR / R | **3.3** (prior) / 33.3 / 2.00 |
| EA | `Experts\BMRG\BMRG.ex5` ≥ **1.24** · `Include/AOS_L2det_jp_m5.mqh` |

**Chart / Tester:** JPN225 **M5** · load `JPN225_5m_stack.set` · dates covering tip (e.g. 2026.05.01 → 2026.10.19). Ledger → `COMMON\Files\BMRG_AOS_ledger_26161907.csv`.

Engine-only baseline remains magic **26101906** / P0 growth (AOS OFF).  
M15 research OS remains magic **26151907** / **`JPN225stack`** — separate stream.

---

## HITL acknowledgements (signed)

1. Not a replace for EURUSD / AUDUSD / UK100 / DE40 live or research books.  
2. Not a twin of JP225 **M15** research OS / `JPN225stack` / May∨Jul.  
3. Expansion research arm only — full G0–G5 production admit **deferred**.  
4. Leak still **prior 3.3 pp** (measured deal Leak OPEN).  
5. L2 AI remains **DISARM** (tip AUC ≈0.49).  
6. L9 H08 / London / H10 / spread approved as **shadow only** — **not** LIVE in this arm.  
7. Never thin SL under fat Nikkei spread (~2300) · never borrow M15 May∨Jul on M5.

---

## Evidence snapshot

| Source | Result |
| --- | --- |
| Engine tip May→Oct | n94 · WR 41.5% · E_N **+0.245R** · EF_prior **+4.9 pp** · +$35.34 |
| Offline L2det v1c tip (P2) | n69 · E_N **+0.478R** · ΔE_N +0.234R · ret 73.4% · Jul FP 1 · SELL FP 0 |
| P4 det stack | n_fire **69** · E_N **+0.478R** · EF **+12.6 pp** · L3 halt **0** · life EXPANDING |
| P3 health | P0 tip 1× BELOW · **v1c tip 0× BELOW** · MaxDD 3.4%→**1.3%** |
| P5 AI | AUC ≈0.49 · DISARM · challenger EMPTY · drill PASS |
| P6 harden | keep v1c · ATR 7610–11285 G3 PASS · L9 no LIVE |

---

## P7-T03 — Paper / tiny-f checklist

Before any paper or tiny-f chart attach:

- [ ] Compile `BMRG.mq5` ≥ **1.24** · confirm Inputs show `InpAOS_JP_M5_L2detEnable=true`  
- [ ] Load **`JPN225_5m_stack.set`** · magic **26161907** · symbol **JPN225** **M5**  
- [ ] Confirm `InpAiOsMode=LIVE_WITHHOLD` · kill-switch **false** · L2AI **false**  
- [ ] Confirm `InpAOS_JP_L2detEnable=false` (M15 May∨Jul map off)  
- [ ] ATR band **7610–11285** · session 08–17 · skip Tue · MaxSpread 3000 · SL **25000** (do not thin)  
- [ ] Lot **0.1** · deposit sized so 1R ≈ 0.5% (or accept fixed lot)  
- [ ] Ledger path writable (`COMMON\Files`)  
- [ ] Rollback known: AOS off → P0 M5 growth set · or `InpAOS_JP_M5_L2detEnable=false`  
- [ ] Do **not** attach this `.set` to live FX / UK / DE / M15 JP charts  
- [ ] Do **not** raise risk% toward live FX books without a new packet  

Optional paper: same stack · demo account · monitor 2 tip weeks before any capital.

---

## Rollback

| Intent | Action |
| --- | --- |
| Det off | `InpAOS_JP_M5_L2detEnable=false` |
| AOS off | `InpAOS_Enable=false` · P0 M5 growth `.set` |
| Kill L2 mode | `InpAiKillSwitch=true` |
| AI pin | `rollback_l2skip_jp225_m5.py rollback --to DISARM` (AI unused in this arm) |

---

## Related docs

`aos_l2_policy_M5.md` · `aos_l3l4_policy_M5.md` · `aos_l6_ledger_M5.md` · `aos_l5_retrain_M5.md` · `aos_p6_harden_M5.md` · `aios_roadmap_M5.md` · `edge_framework.md` · `system_profile_M5.md`
