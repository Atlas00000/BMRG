# JP225-AOS-P4 — REVIEW

**Date:** 2026-10-19  
**Verdict:** **P4 COMPLETE / SIGNED** — L6 ledger + det stack shadow · L2AI DISARM · L8 secondary advise · **no MQH / no research OS arm**  
**Docs:** `doc/assets/JP225/aos_l6_ledger.md`  
**Artefacts:** `P4_STACK.json` · `ledger_*.csv` · `tapes/jp225_tip_ledger_may_or_jul_shadow.csv`  
**Leak:** measured **2.45 pp** (`JP225-AOS-LEAK`)

---

## Tasks

| Task | Deliverable | Verdict |
| --- | --- | --- |
| P4-T01 | L6 schema + offline writer | **PASS** |
| P4-T02 | Det stack L1+L2det May∨Jul+L3+L4+L6 | **PASS** |
| P4-T03 | + L2AI shadow on det fires | **PASS** (DISARM; n_shadow=0 · no model) |
| P4-T04 | L8 MAE/overnight abort advisor | **PASS** advise-only · secondary |

---

## Tip stack CF (n_signals=79 · Leak_measured=2.45 pp)

| Stack | n_fire | n_l2det | n_L3 | WR% | E_N | EF_pp | L8 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| **det_may_or_jul** (canonical) | 30 | 36 | 13 | 43.33 | **0.083** | **+0.89** | 15 |
| det_may_only | 32 | 23 | 24 | 46.88 | 0.172 | +4.43 | 15 |
| det_may_or_jul + AI shadow | 30 | 36 | 13 | 43.33 | 0.083 | +0.89 | 15 |
| baseline_no_l2 (diag) | 20 | 0 | 59 | 25.0 | −0.375 | −17.4 | 15 |

Skip precision (May∨Jul losers among skips): **69.4%**.  
L8: **15/15** on losers · **0** on winners · **3** overnight · not armed.  
L2AI: **0** `WOULD_SKIP_SHADOW` (DISARM · no tip scorer).

**Note:** Engine tip (all 79 · no L2/L3) already clears Stage-1 under measured Leak (EF **+0.59 pp**). Stack `n_fire` is lower because L3 **BELOW** latch (P3) withholds post-trip fires — same behaviour as offline UK/EUR P4 writers (no unlatch). May∨Jul still improves EF vs latched baseline_no_l2 and cuts halt density 59→13.

---

## Explicit non-goals (honoured)

- No `AOS_L2det_jp225.mqh`
- No research OS `.set` / magic **26151907**
- No live attach

---

## Next

**P5** — retrain loop / `L2skip_jp225/` store · champ-challenger · rollback drill.  
Keep L2AI DISARM until AUC evidence. Wire MQH only after P6/P7 path.
