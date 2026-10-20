# AUDUSD-AOS-P4 — REVIEW

**Date:** 2026-10-19  
**Verdict:** **P4 COMPLETE / SIGNED** — ledger schema + offline writer · det stack shadow · L2AI SHADOW overlay · L8 overnight-primary advise · research `.set` W50 · MQL L2det_aud  
**Docs:** `doc/assets/AUDUSD/aos_l6_ledger.md`  
**Artefacts:** `P4_STACK.json` · `ledger_*.csv` · `tapes/audusd_m15_tip_ledger_v1_shadow.csv`  
**Preset:** `Presets/BMRG-M15-AUDUSD-6M-P4_research_OS_W50.set` · `Profiles/Tester/BMRG/AUDUSD/` (magic **8231941**)  
**MQL:** `Include/AOS_L2det_aud.mqh` · `InpAOS_AUD_*` (default Enable=false)

---

## Tasks

| Task | Deliverable | Verdict |
| --- | --- | --- |
| P4-T01 | L6 schema + offline writer | **PASS** |
| P4-T02 | Det stack L1+L2det+L3+L4+L6 | **PASS** |
| P4-T03 | + L2AI shadow on det fires | **PASS** (SHADOW; n_shadow=3) |
| P4-T04 | L8 MAE/overnight abort advisor | **PASS** advise-only |

---

## Tip stack CF (n_signals=41, Leak_proxy=5.0 pp)

| Stack | n_fire | n_l2det_skip | WR% | E_N | EF_pp | L3 halt | L8 advise |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| **det_v1** (canonical) | 39 | 2 | 66.67 | **0.3333** | **11.667** | 0 | 6 |
| det_v1 + AI shadow | 39 | 2 | 66.67 | 0.3333 | 11.667 | 0 | 6 |

L2AI shadow: **3** `WOULD_SKIP_SHADOW` · `final_permit` unchanged (SHADOW_ONLY).  
L8: **6/6** advises on losers · **0** on winners · **4** overnight · not armed.

Skip precision (v1 losers among skips): **100%**.  
Fire retention: **39/41 = 95.1%** (matches P2 v1).

---

## Research `.set` / MQL wire

`AOS_L2det_aud.mqh` (BUY∧May) gated so live M5 SCALE stays on AI pin when `InpAOS_AUD_L2detEnable=false`.

Preset:

- `Presets/BMRG-M15-AUDUSD-6M-P4_research_OS_W50.set`
- `Profiles/Tester/BMRG/AUDUSD/BMRG-M15-AUDUSD-6M-P4_research_OS_W50.set`

`InpAiOsMode=LIVE_WITHHOLD` · kill-switch OFF · Leak 5.0 · W50. Compile before Tester.

---

## Next

**P5** — retrain loop / `L2skip_aud_m15/` store · champ-challenger · rollback drill.  
Measured Leak+swap still **OPEN**. Do **not** arm on live M5 SCALE **8230931**.
