# DE40-AOS-P5 — REVIEW

**Date:** 2026-10-19  
**Verdict:** **P5 COMPLETE / SIGNED** — retrain store + promote rules + rollback drill  
**Policy:** `doc/assets/DE40/aos_l5_retrain.md`  
**Store:** `infra/artefacts/models/L2skip_de40/`

---

## Tasks

| Task | Deliverable | Verdict |
| --- | --- | --- |
| P5-T01 | Retrain policy + store layout + `train_l2_de40.py` | **PASS** |
| P5-T02 | Champ/challenger promote rules | **PASS** (AI challenger EMPTY) |
| P5-T03 | Rollback drill | **PASS** `_drill/*/DRILL_REPORT.json` |

---

## Train loop smoke

| Semver | AUC tip | Best tip CF | Chrono holdout |
| --- | ---: | --- | --- |
| `L2skip_de40_p_pretip_20261019_150458` (P5) | 0.519 | HOLD_SHADOW | **REJECT_FREQUENCY_STALL** |

LATEST = SHADOW_ONLY · CHAMP AI = DISARM · CHALLENGER = EMPTY.  
Rules #1–#3 (AUC≥0.55 · SHADOW_CANDIDATE · chrono OK) **block** challenger promotion.  
**Overlay champ remains `L2det_de40_v1_BUY_near_atr`** (offline CF · no MQH).

---

## Rollback drill

`rollback_l2skip_de40.py drill` → DISARM → restore shadow pin · **pass=true**.

EA checklist: kill-switch / AiOsMode OFF / AOS off → Balanced P0 engine.

---

## Next

**P6** hardening (session soft veto · ±10% L2 stress · ATR G3 note).  
No L2 AI LIVE_WITHHOLD. Measured Leak still **OPEN**.
