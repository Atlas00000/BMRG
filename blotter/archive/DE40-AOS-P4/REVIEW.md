# DE40-AOS-P4 — REVIEW

**Date:** 2026-10-19  
**Verdict:** **P4 COMPLETE / SIGNED** — ledger schema + offline writer · det stack shadow · L2AI DISARM overlay · L8 cash-sleeve advise · research `.set` W50  
**Docs:** `doc/assets/DE40/aos_l6_ledger.md`  
**Artefacts:** `P4_STACK.json` · `ledger_*.csv` · `tapes/de40_tip_ledger_arm_shadow.csv`  
**Preset:** `Presets/BMRG-M15-DE40-6M-P4_research_OS_W50.set` · `Profiles/Tester/BMRG/DE40/` (magic **26141904**)

---

## Tasks

| Task | Deliverable | Verdict |
| --- | --- | --- |
| P4-T01 | L6 schema + offline writer | **PASS** |
| P4-T02 | Det stack L1+L2det+L3+L4+L6 | **PASS** (ARM BUY∧near_atr) |
| P4-T03 | + L2AI shadow on det fires | **PASS** (DISARM; n_shadow=18) |
| P4-T04 | L8 MAE abort advisor | **PASS** advise-only |

---

## Tip stack CF (Leak prior 9.8 pp)

| Stack | n_fire | n_l2det_skip | WR% | E_N | EF_pp | L3 halt | L8 advise |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| P0 engine | 77 | 0 | 58.4 | +0.31 | +4.2 | 0 | 16 |
| **det ARM** | **62** | **15** | **62.9** | **+0.42** | **+8.7** | 0 | 16 |
| det HOLD v1b | 53 | 24 | 66.0 | +0.49 | +11.8 | 0 | 16 |
| ARM + AI shadow | 62 | 15 | 62.9 | +0.42 | +8.7 | 0 | 16 |

L8: **16/16** advises on losers · **0** on winners · not armed.  
L2AI: DISARM — shadow skips do not change `final_permit`.

---

## Gaps / next

- No `AOS_L2det_de.mqh` — BUY∧near_atr is **offline** only; research `.set` uses `InpAiOsMode=0` with L3/L4/ledger ON.
- Measured Leak still OPEN (deal export).
- Next: **P5** retrain/rollback store for `L2skip_de40/`.

---

## Preset copies

- `Presets/BMRG-M15-DE40-6M-P4_research_OS_W50.set`
- `Profiles/Tester/BMRG/DE40/BMRG-M15-DE40-6M-P4_research_OS_W50.set`
- This archive folder
