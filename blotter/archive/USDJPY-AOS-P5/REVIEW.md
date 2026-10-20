# USDJPY-AOS-P5 — REVIEW

**Date:** 2026-10-19  
**Verdict:** **P5 COMPLETE / SIGNED** — retrain store + promote rules + rollback drill  
**Policy:** `doc/assets/USDJPY/aos_l5_retrain.md`  
**Store:** `infra/artefacts/models/L2skip_usdjpy/`

---

## Tasks

| Task | Deliverable | Verdict |
| --- | --- | --- |
| P5-T01 | Retrain policy + store layout + `train_l2_usdjpy.py` | **PASS** |
| P5-T02 | Champ/challenger promote rules | **PASS** (AI challenger EMPTY) |
| P5-T03 | Rollback drill | **PASS** `_drill/*/DRILL_REPORT.json` |

---

## Train loop smoke

| Semver | Pre-n | AUC tip | Best tip CF | Chrono holdout |
| --- | ---: | ---: | --- | --- |
| `L2skip_usdjpy_p_pretip_20261019_155324` | 14 | **0.471** | HOLD_SHADOW (BUY FP 6) | SHADOW_CANDIDATE |

LATEST = SHADOW_ONLY · CHAMP AI = DISARM · CHALLENGER = EMPTY.  
Rules #1–#2 (AUC≥0.55 · SHADOW_CANDIDATE) **block** challenger promotion.  
Pre-tip thin (long tape n=14; YTD pre alone n=5) — expected.  
**Overlay champ remains `L2det_usdjpy_v1c_near_atr_OR_H16`** (offline CF · no MQH).

---

## Rollback drill

`rollback_l2skip_usdjpy.py drill` → DISARM → restore shadow pin · **pass=true**.

EA checklist: kill-switch / AiOsMode OFF / AOS off → Balanced P0 engine · or keep P4 magic 26131804 health-only.

---

## Next

**P6** hardening (H14/spread soft veto · ±10% L2 stress · ATR G3 note).  
No L2 AI LIVE_WITHHOLD. Measured Leak still **OPEN**.
