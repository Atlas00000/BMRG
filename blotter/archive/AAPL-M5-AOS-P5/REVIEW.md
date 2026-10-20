# AAPL-M5-AOS-P5 — REVIEW

**Task:** AAPL-M5-AOS-P5 (T01–T03)  
**Scored:** 2026-10-20  
**Verdict:** **ACCEPT / PASS** — store + train + rollback drill · AI challenger EMPTY · overlay champ L2det v1b  

---

## Train (T01)

| Field | Value |
| --- | --- |
| Semver | `L2skip_aapl_m5_p_prior_20261020_140136` |
| Tip OOS AUC | **0.501** |
| Best tip CF | **DISARM** (AUC&lt;0.55 · thr 0.75 · ΔE_N +0.039 · May FP=1 · Mon FP=0 · BUY FP=3) |
| Mode | SHADOW_ONLY |
| Challenger / AI champ | EMPTY / NONE |
| Overlay champ | `L2det_aapl_m5_v1b` (unchanged) |

---

## Promote rules (T02)

Documented in `doc/assets/AAPL/aos_l5_retrain_M5.md`. No AI challenger — AUC gate fails (&lt;0.55).

---

## Rollback drill (T03)

`snapshot → DISARM → restore` · **PASS** · `_drill/` archived (store + blotter).

---

## Next

`AAPL-M5-AOS-P6` — L9 session soft veto · ±10% L2 stress · ATR/BBw G3 confirm.  
Measured Leak still OPEN · not M15 Harvest / FX replace.
