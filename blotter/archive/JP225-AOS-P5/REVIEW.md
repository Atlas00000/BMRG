# JP225-AOS-P5 — REVIEW

**Date:** 2026-10-19  
**Verdict:** **P5 COMPLETE / SIGNED** — retrain store + promote rules + rollback drill  
**Policy:** `doc/assets/JP225/aos_l5_retrain.md`  
**Store:** `infra/artefacts/models/L2skip_jp225/`  
**Mode:** offline · **no MQH** · L2 AI **DISARM**

---

## Tasks

| Task | Deliverable | Verdict |
| --- | --- | --- |
| P5-T01 | Retrain policy + store layout + `train_l2_jp225.py` | **PASS** |
| P5-T02 | Champ/challenger promote rules | **PASS** (AI challenger EMPTY) |
| P5-T03 | Rollback drill | **PASS** `_drill/*/DRILL_REPORT.json` |

---

## Train loop smoke

| Semver | AUC tip | Best tip CF | Chrono holdout |
| --- | ---: | ---: | ---: |
| `L2skip_jp225_p_pretip_20261019_152317` (P5) | **0.493** | SHADOW_CANDIDATE (thr 0.75 · n_skip=4 · prec 1.0) | **SHADOW_CANDIDATE** |

LATEST = SHADOW_ONLY · CHAMP AI = DISARM · CHALLENGER = EMPTY.  
Rule **#1** (AUC≥0.55) **blocks** challenger promotion despite tip CF + chrono looking clean (thr optimistic / small-n skips).  
**Overlay champ remains `L2det_jp225_v1_May_OR_Jul`** (offline CF · no MQH).

Trigger: `Leak_source` → measured (2.45 pp) — retrain allowed under P5-T01.

---

## Rollback drill

`rollback_l2skip_jp225.py drill` → DISARM → restore shadow pin · **pass=true**.

EA checklist: kill-switch / AiOsMode OFF / AOS off → Growth P1 engine.

---

## Next

**P6** hardening (session soft veto · ±10% L2 stress · ATR G3 note).  
No L2 AI LIVE_WITHHOLD. No research OS arm.
