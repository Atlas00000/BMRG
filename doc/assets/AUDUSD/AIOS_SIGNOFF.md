# AUDUSD AIOS sign-off

Two tracks — do **not** mix magics / pins / presets.

| Track | Magic | Role |
| --- | ---: | --- |
| **A — M15 research OS** | **8231941** | P7 HITL **ARM_RESEARCH_OS** (this section) |
| **B — live M5 SCALE** | **8230931** | Live Risk 3% (section below) |

---

## A. M15 research OS (P7 HITL)

**HITL signed:** 2026-10-19 (operator — “proceed with P7 and also provide the preset”)  
**Packet:** `AUDUSD_M15_AOS_RESEARCH_v1` · `blotter/archive/AUDUSD-AOS-P7/promotion_packet.json`  
**Verdict:** **ARM_RESEARCH_OS** — M15 CHAMP research sleeve only · **not** live M5 SCALE replace · **not** PRODUCTION-WORTHY

### Armed research attach

| | |
| --- | --- |
| **Preset (primary)** | **`AUDUSD_stack.set`** |
| **Alias** | `BMRG-M15-AUDUSD-6M-P7_research_OS_ARMED.set` |
| **Paths** | `Presets/` · `Profiles/Tester/BMRG/AUDUSD/` · `doc/presets/` |
| **Magic** | **8231941** |
| **Risk / lot** | 0.5% · fixed **0.01** |
| Engine | CHAMP · SL/TP **300/300** · BB **2.2** · Start**13** · skip Mon/Tue · ATR **OFF** |
| AOS | ON · **LIVE_WITHHOLD** · L3/L4 · ledger · **W50** |
| **L2** | **`L2det_aud_m15_v1`** (BUY∧May) · L2 AI **OFF** (challenger SHADOW store) |
| Leak / BWR / R | **5.0** (journal proxy) / 50 / 1.0 |
| EA | Compile `BMRG.mq5` with `Include/AOS_L2det_aud.mqh` |

**Chart / Tester:** AUDUSD **M15** · load **AUDUSD_stack** · tip window e.g. **2026.05.01 → tip**.  
Ledger → `COMMON\Files\BMRG_AOS_ledger_8231941.csv`.

Engine-only baseline remains magic **8230901** / CHAMP Harvest (AOS OFF).

### HITL acknowledgements (signed)

1. Not a replace for live M5 SCALE **8230931**.  
2. Expansion research arm only — full G0–G5 production admit **deferred**.  
3. Leak still **journal proxy** 5.0 pp (measured deal Leak + **swap** OPEN).  
4. L2 AI remains **OFF** in EA (challenger `…145303` SHADOW store only).  
5. L9 BUY∧Thu approved as **shadow** — **not** LIVE (`SkipBuyThu=false`).  
6. No foreign L2 pins (EUR / UK100 / DE40 / AAPL / live M5 pin).

### Evidence snapshot

| Source | Result |
| --- | --- |
| Engine tip May→Aug | n41 · WR 63.4% · E_N **+0.268R** · EF_journal **+8.4 pp** |
| Offline L2det v1 tip | n39 · WR 66.7% · E_N **+0.333R** · ΔE_N **+0.065R** · ret **95.1%** · prec 100% |
| P3 L3/L4 | v1 tip **0 trips** (P0 had 1× BELOW) |
| P6 harden | geometry freeze PASS · BUY∧May keep · L9 Thu SHADOW |

### P7-T03 — Paper / tiny-f checklist

Before any paper or tiny-f chart attach:

- [ ] Compile `BMRG.mq5` · confirm Inputs show `InpAOS_AUD_L2detEnable=true`  
- [ ] Load **`AUDUSD_stack.set`** · magic **8231941** · symbol **AUDUSD** M15  
- [ ] Confirm `InpAiOsMode=LIVE_WITHHOLD` · kill-switch **false** · L2AI **false**  
- [ ] Geometry: SL/TP **300/300** · BBDev **2.2** · Start**13** · Mon/Tue **false** · ATR regime **false**  
- [ ] Lot **0.01** · risk 0.5% · W50 · Leak 5.0  
- [ ] Ledger path writable (`COMMON\Files`)  
- [ ] Rollback known: AOS off → CHAMP `.set` · or `InpAOS_AUD_L2detEnable=false`  
- [ ] Do **not** attach this `.set` to live M5 SCALE charts (**8230931**)  

Optional paper: same stack · demo · monitor 2 tip weeks before any capital.

### Rollback (research OS)

| Intent | Action |
| --- | --- |
| Det off | `InpAOS_AUD_L2detEnable=false` |
| AOS off | `InpAOS_Enable=false` · CHAMP Harvest `.set` |
| Kill L2 mode | `InpAiKillSwitch=true` |
| AI pin | `rollback_l2skip_aud_m15.py rollback --to DISARM` (AI unused in EA arm) |

---

## B. Live M5 SCALE (Track B — unchanged)

**Signed:** 2026-10-08 (FT Risk 0.5%) · **Live scale promoted:** 2026-10-08

| | |
| --- | --- |
| **Preset** | `Profiles/Tester/BMRG/AUDUSD/AUDUSD-AIOS_SCALE_Risk3_champ_G0.set` |
| **Magic** | **8230931** |
| **Risk** | **3.0%** |
| Engine | Champ Start13 + skip Mon/Tue · SL/TP 300/300 |
| AOS | ON · LIVE_WITHHOLD · L3/L4 · ledger |
| **W window** | **`InpAOS_W250=250`** |
| **L2 pin** | **`L2skip_aud_p90_20261008_122523`** · bake `Include/AOS_L2skip_aud.mqh` |
| Leak / BWR / R | 2.4 / 50 / 1.0 |
| Evidence | `blotter/archive/AUDUSD-RISK3-Q/` |

**Chart attach:** Expert `Experts\BMRG\BMRG.ex5` · AUDUSD **M5** · SCALE `.set` · magic **8230931**.

### Prior FT baseline (retained)

| | |
| --- | --- |
| Preset | `AUDUSD-AIOS_LIVE_WITHHOLD_champ_G0.set` |
| Magic | **8230921** |
| Risk | **0.5%** |
| Role | FT / research twin — do not use as AUDUSD live size |

---

## Related docs

`aos_l2_policy.md` · `aos_l3l4_policy.md` · `aos_l6_ledger.md` · `aos_l5_retrain.md` · `aos_p6_harden.md` · `aios_roadmap.md` · `edge_framework.md`
