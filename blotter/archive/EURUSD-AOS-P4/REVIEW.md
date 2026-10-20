# EURUSD-AOS-P4 — REVIEW

**Date:** 2026-10-18  
**Verdict:** **P4 COMPLETE / SIGNED** — ledger schema + offline writer · det stack shadow · L2AI DISARM overlay · L8 overnight-primary advise · research `.set` W50  
**Docs:** `doc/assets/EURUSD/aos_l6_ledger.md`  
**Artefacts:** `P4_STACK.json` · `ledger_*.csv` · `tapes/eurusd_m15_tip_ledger_v1b_shadow.csv`  
**Preset:** `Presets/BMRG-M15-EURUSD-6M-P4_research_OS_W50.set` · `Profiles/Tester/BMRG/EURUSD/` (magic **26121804**)  
**MQL:** `Include/AOS_L2det_eur.mqh` · `InpAOS_EUR_*` (default Enable=false)

---

## Tasks

| Task | Deliverable | Verdict |
| --- | --- | --- |
| P4-T01 | L6 schema + offline writer | **PASS** |
| P4-T02 | Det stack L1+L2det+L3+L4+L6 | **PASS** |
| P4-T03 | + L2AI shadow on det fires | **PASS** (DISARM; n_shadow=5) |
| P4-T04 | L8 MAE/overnight abort advisor | **PASS** advise-only |

---

## Tip stack CF (n_signals=45, Leak_proxy=1.19 pp)

| Stack | n_fire | n_l2det_skip | WR% | E_N | EF_pp | L3 halt | L8 advise |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| **det_v1b** (canonical) | 31 | 14 | 54.84 | **0.2339** | **9.209** | 0 | 21 |
| det_v1b + AI shadow | 31 | 14 | 54.84 | 0.2339 | 9.209 | 0 | 21 |

L2AI shadow: **5** `WOULD_SKIP_SHADOW` · `final_permit` unchanged (DISARM).  
L8: **21/21** advises on losers · **0** on winners · **16** overnight · not armed.

Skip precision (v1b losers among skips): **71.4%**.  
Fire retention: **31/45 = 68.9%** (matches P2 v1b).

---

## Research `.set` / MQL wire

`AOS_L2det_eur.mqh` (Thu ∨ BUY∧nearATR) gated so M5 Harvest stays INF when `InpAOS_EUR_L2detEnable=false`.

Preset:

- `Presets/BMRG-M15-EURUSD-6M-P4_research_OS_W50.set`
- `Profiles/Tester/BMRG/EURUSD/BMRG-M15-EURUSD-6M-P4_research_OS_W50.set`

`InpAiOsMode=LIVE_WITHHOLD` · kill-switch OFF · Leak 1.19 · W50. Compile before Tester.

---

## Next

**P5** — retrain loop / `L2skip_eur_m15/` store · champ-challenger · rollback drill.  
Measured Leak+swap still **OPEN**. Do **not** arm on live M5 Harvest.
