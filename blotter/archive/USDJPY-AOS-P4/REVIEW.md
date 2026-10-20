# USDJPY-AOS-P4 — REVIEW

**Date:** 2026-10-19  
**Verdict:** **P4 COMPLETE / SIGNED** — ledger schema + offline writer · det stack shadow · L2AI SHADOW overlay · L8 session-sleeve advise · research `.set` W50  
**Docs:** `doc/assets/USDJPY/aos_l6_ledger.md`  
**Artefacts:** `P4_STACK.json` · `ledger_*.csv` · `tapes/usdjpy_tip_ledger_v1c_shadow.csv`  
**Preset:** `Presets/BMRG-M15-USDJPY-6M-P4_research_OS_W50.set` · `Profiles/Tester/BMRG/USDJPY/` (magic **26131804**)

---

## Tasks

| Task | Deliverable | Verdict |
| --- | --- | --- |
| P4-T01 | L6 schema + offline writer | **PASS** |
| P4-T02 | Det stack L1+L2det+L3+L4+L6 | **PASS** (ARM **v1c**) |
| P4-T03 | + L2AI shadow on det fires | **PASS** (SHADOW_ONLY; n_shadow=9) |
| P4-T04 | L8 MAE abort advisor | **PASS** advise-only (secondary) |

---

## Tip stack CF (Leak prior 11.4 pp)

| Stack | n_fire | n_l2det_skip | L3 halt | WR% | E_N | EF_pp | L8 advise |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| P0 engine | 34 | 0 | **12** | 50.0 | +0.10 | −6.9 | 9 |
| near_atr slim | 32 | 6 | **8** | 53.1 | +0.17 | −3.7 | 9 |
| **det ARM v1c** | **37** | **9** | **0** | **62.2** | **+0.37** | **+5.3** | 9 |
| Jul HOLD | 32 | 14 | 0 | 59.4 | +0.31 | +2.5 | 9 |
| v1c + AI shadow | 37 | 9 | 0 | 62.2 | +0.37 | +5.3 | 9 |

L8: **9/9** advises on losers · **0** on winners · not armed.  
L2AI: SHADOW_ONLY — shadow skips do not change `final_permit`.  
v1c skip precision: **100%** · retention **80.4%**.

---

## Gaps / next

- No `AOS_L2det_usdjpy.mqh` — v1c is **offline** only; research `.set` uses `InpAiOsMode=0` with L3/L4/ledger ON.
- Measured Leak still OPEN (deal export).
- Next: **P5** retrain/rollback store for `L2skip_usdjpy/`.

---

## Preset copies

- `Presets/BMRG-M15-USDJPY-6M-P4_research_OS_W50.set`
- `Profiles/Tester/BMRG/USDJPY/BMRG-M15-USDJPY-6M-P4_research_OS_W50.set`
- This archive folder
