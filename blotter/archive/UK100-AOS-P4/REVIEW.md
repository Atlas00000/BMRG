# UK100-AOS-P4 — REVIEW

**Date:** 2026-10-12  
**Verdict:** **P4 COMPLETE / SIGNED** — ledger schema + offline writer · det stack shadow · L2AI DISARM overlay · L8 advise-only · research `.set` W50  
**Docs:** `doc/assets/UK100/aos_l6_ledger.md`  
**Artefacts:** `P4_STACK.json` · `ledger_*.csv` · `tapes/uk100_tip_ledger_v1b_shadow.csv`  
**Preset:** `Profiles/Tester/BMRG/UK100/BMRG-M15-UK100-6M-P4_research_OS_W50.set` (magic **26111304**)

---

## Tasks

| Task | Deliverable | Verdict |
| --- | --- | --- |
| P4-T01 | L6 schema + offline writer | **PASS** |
| P4-T02 | Det stack L1+L2det+L3+L4+L6 | **PASS** |
| P4-T03 | + L2AI shadow on det fires | **PASS** (DISARM; n_shadow=1) |
| P4-T04 | L8 MAE abort advisor | **PASS** advise-only |

---

## Tip stack CF (n_signals=51, Leak_proxy=4.27 pp)

| Stack | n_fire | n_skip | WR% | E_N | EF_pp | L3 halt | L8 advise |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| **det_v1b** (canonical) | 33 | 18 | 60.61 | **0.3636** | **11.90** | 0 | 5 |
| det_v1b_jul | 29 | 22 | 62.07 | 0.3966 | 13.36 | 0 | 5 |
| det_v1b + AI shadow | 33 | 18 | 60.61 | 0.3636 | 11.90 | 0 | 5 |
| det_v1b_jul + AI shadow | 29 | 22 | 62.07 | 0.3966 | 13.36 | 0 | 5 |

L2AI shadow: **1** `WOULD_SKIP_SHADOW` · `final_permit` unchanged (DISARM).  
L8: **5/5** advises landed on losers · **0** on winners · not armed.

Skip precision (v1b losers among skips): **72.2%**.

---

## Research `.set` / MQL wire

EA **v1.23** wires `AOS_L2det_uk.mqh` (Thu ∨ BUY∧nearATR). Preset at:

- `Profiles/Tester/BMRG/BMRG-M15-UK100-6M-P4_research_OS_W50.set`
- `Profiles/Tester/BMRG/UK100/…` (same)

`InpAiOsMode=LIVE_WITHHOLD` · kill-switch OFF · compile OK (0 errors). Run Tester UK100 M15 tip window to confirm skips + ledger.

---

## Next

**P5** — retrain loop / `L2skip_uk/` store · champ-challenger · rollback drill.  
Deal-measured Leak still **OPEN**. LIVE_WITHHOLD **not** armed.
