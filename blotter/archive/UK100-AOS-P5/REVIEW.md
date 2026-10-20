# UK100-AOS-P5 — REVIEW

**Date:** 2026-10-12  
**Verdict:** **P5 COMPLETE / SIGNED** — retrain store + promote rules + rollback drill  
**Policy:** `doc/assets/UK100/aos_l5_retrain.md`  
**Store:** `infra/artefacts/models/L2skip_uk/`

---

## Tasks

| Task | Deliverable | Verdict |
| --- | --- | --- |
| P5-T01 | Retrain policy + store layout + `train_l2_uk100.py` | **PASS** |
| P5-T02 | Champ/challenger promote rules | **PASS** (AI challenger EMPTY) |
| P5-T03 | Rollback drill | **PASS** `_drill/*/DRILL_REPORT.json` |

---

## Train loop smoke

| Semver | AUC tip | Best CF |
| --- | ---: | --- |
| `L2skip_uk_p_prior_20261012_222755` | 0.389 | DISARM |
| `L2skip_uk_p_prior_20261012_225955` (P5 retrain) | 0.388 | DISARM |

LATEST = SHADOW_ONLY · CHAMP AI = DISARM · CHALLENGER = EMPTY.  
**Overlay champ remains `L2det_uk_v1b`** (Tester-validated).

---

## Rollback drill

`rollback_l2skip_uk.py drill` → DISARM → restore shadow pin · **pass=true**.

EA checklist documented (kill-switch / UK L2det off / AOS off → P0).

---

## Next

**P6** hardening (session soft veto · ±10% L2 stress · ATR G3 note).  
No L2 AI LIVE_WITHHOLD.
