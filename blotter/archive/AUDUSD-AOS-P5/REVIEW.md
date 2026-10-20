# AUDUSD-AOS-P5 — REVIEW

**Date:** 2026-10-19  
**Verdict:** **P5 COMPLETE / SIGNED** — retrain store + promote rules + rollback drill  
**Policy:** `doc/assets/AUDUSD/aos_l5_retrain.md`  
**Store:** `infra/artefacts/models/L2skip_aud_m15/`

---

## Tasks

| Task | Deliverable | Verdict |
| --- | --- | --- |
| P5-T01 | Retrain policy + store layout + `train_l2_audusd_m15.py` | **PASS** |
| P5-T02 | Champ/challenger promote rules | **PASS** (AI challenger EMPTY · eligible pending HITL) |
| P5-T03 | Rollback drill | **PASS** `_drill/*/DRILL_REPORT.json` |

---

## Train loop smoke

| Semver | AUC tip | Best tip CF | Chrono holdout |
| --- | ---: | --- | --- |
| `L2skip_aud_m15_p_pretip_20261019_143100` (P2) | 0.597 | ARM_SOFT | HOLD_SOFT |
| `L2skip_aud_m15_p_pretip_20261019_145303` (P5 retrain) | 0.597 | **SHADOW_CANDIDATE** | **HOLD_SHADOW** |

LATEST = SHADOW_ONLY · CHAMP AI = DISARM · CHALLENGER = EMPTY.  
Rules 1–4 clear (tip SHADOW_CANDIDATE · chrono HOLD_SHADOW · stack OR ≥ det).  
Rules 5–6 (HITL + CHALLENGER pin) **deferred** — do not auto-promote.  
**Overlay champ remains `L2det_aud_m15_v1`** (research OS).

---

## Rollback drill

`rollback_l2skip_aud_m15.py drill` → DISARM → restore shadow pin · **pass=true**.

EA checklist: kill-switch / AUD L2det off / AOS off → CHAMP engine **8230901**.  
Never touch live **8230931**.

---

## Next

**P6** hardening (session soft veto · ±10% L2 stress · geometry freeze note).  
No L2 AI LIVE_WITHHOLD. Measured Leak+swap still **OPEN**.
