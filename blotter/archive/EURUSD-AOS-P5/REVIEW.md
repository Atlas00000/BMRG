# EURUSD-AOS-P5 — REVIEW

**Date:** 2026-10-18  
**Verdict:** **P5 COMPLETE / SIGNED** — retrain store + promote rules + rollback drill  
**Policy:** `doc/assets/EURUSD/aos_l5_retrain.md`  
**Store:** `infra/artefacts/models/L2skip_eur_m15/`

---

## Tasks

| Task | Deliverable | Verdict |
| --- | --- | --- |
| P5-T01 | Retrain policy + store layout + `train_l2_eurusd_m15.py` | **PASS** |
| P5-T02 | Champ/challenger promote rules | **PASS** (AI challenger EMPTY) |
| P5-T03 | Rollback drill | **PASS** `_drill/*/DRILL_REPORT.json` |

---

## Train loop smoke

| Semver | AUC tip | Best tip CF | Chrono holdout |
| --- | ---: | --- | --- |
| `L2skip_eur_m15_p_pretip_20261018_145108` (P2) | 0.583 | ARM_SOFT | DISARM |
| `L2skip_eur_m15_p_pretip_20261018_150651` (P5 retrain) | 0.583 | SHADOW_CANDIDATE | **DISARM** |

LATEST = SHADOW_ONLY · CHAMP AI = DISARM · CHALLENGER = EMPTY.  
Rule #3 (chrono holdout) **blocks** challenger promotion — tip thr remains optimistic.  
**Overlay champ remains `L2det_eur_m15_v1b`** (research OS).

---

## Rollback drill

`rollback_l2skip_eur_m15.py drill` → DISARM → restore shadow pin · **pass=true**.

EA checklist: kill-switch / EUR L2det off / AOS off → P2 light engine.

---

## Next

**P6** hardening (session soft veto · ±10% L2 stress · ATR G3 note).  
No L2 AI LIVE_WITHHOLD. Measured Leak+swap still **OPEN**.
