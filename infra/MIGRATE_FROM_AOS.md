# Migrate-from-AOS inventory

**Task:** `INF-P0-T04`  
**Recipe:** `INF-P0-T04_data_inventoryAos_migratePlan`  
**Locked:** 2026-09-27  
**Rule:** Consume archives only. **Do not reopen Edge Discovery** as a campaign.  
**Target SoR:** Postgres via INF-W02/W03 (`raw` → `core`).

Paths relative to `Experts/BMRG/`.

---

## 1. Must-migrate (INF-W02–W04 inputs)

| Priority | Artefact | Path | Migrates into | Notes |
| --- | --- | --- | --- | --- |
| P0 | Engine baseline pointer | `doc/ai_OS_baseline.md` · `blotter/archive/AOS-P0-T01/BASELINE.json` | Already mirrored → `infra/baselines/ENGINE_BASELINE_v1.json` | INF evals load infra JSON |
| P0 | Harvest long tester log (currency) | `blotter/archive/EDX-POOL_WINDOWS/T04_Long_8210204.log` | `raw.landing_file` → core blotter | Primary engine dump |
| P0 | Harvest champ review / scorecard context | `blotter/archive/EDX-P2-T04/` | `raw` + score provenance | Champion geometry evidence |
| P0 | Pool scorecard matrix | `blotter/archive/EDX-POOL_WINDOWS/SCORECARD_MATRIX.md` | reference only | Sleeve registry numbers |
| P1 | L1 offline tape (fires) | `blotter/archive/AOS-P1-T02/harvest_long_fires.csv` · `.jsonl` | `features.tape_tick` / parquet | 531/531 tagged; Tue=0 |
| P1 | Tape manifest | `blotter/archive/AOS-P1-T02/TAPE_MANIFEST.md` | feature schema provenance | Session algorithm |
| P1 | Labelled train matrix | `blotter/archive/AOS-P4-T01/harvest_train_matrix.csv` | `train.label_row` | n=530; TP/SL 289/241 |
| P1 | Class balance | `blotter/archive/AOS-P4-T01/class_balance.json` | train diagnostics | |
| P1 | L2skip_v1 model | `models/L2skip/versions/L2skip_v1/` (`*.joblib`, `coeffs.json`, `metrics.json`, `META.json`) | `infra/artefacts/models/L2skip/<semver>/` · `ops.model_version` | Shadow challenger; do not overwrite |
| P1 | L2skip shadow CF (model store) | `models/L2skip/versions/L2skip_v1/shadow_cf.json` | `score` / reports | CF EF 2.33→4.91 (labeled Leak) |
| P1 | Shadow decisions | `blotter/archive/AOS-P4-T03/shadow_decisions.csv` · `shadow_counterfactual.json` | `score.skip_ledger` | Actual fires = baseline |
| P1 | WF folds | `blotter/archive/AOS-P4-T02/wf_folds.csv` | `train` fold table | Reuse as harness fixture |
| P2 | Stack AI shadow ledger | `blotter/archive/AOS-P6-T02/stack_ai_shadow_ledger.csv` · `stack_ai_shadow_score.json` | score fixtures | Offline stack CF |
| P2 | Det stack ledger | `blotter/archive/AOS-P6-T01/` (if present) | score fixtures | L2det stack |
| P2 | LIVE pin state | `models/L2skip/LIVE.json` · `rollback.py` · `rollback_log.jsonl` | ops pin/rollback design | Currently pinned `L2skip_v0_engine` |
| P2 | Bad-cell registry | `doc/aos_bad_cells.md` | L2 policy seeds (low skip bar) | Consume; don’t rediscover |
| P2 | L1 feature schema / tape contract | `doc/aos_l1_feature_schema.md` · `doc/aos_l1_tape_contract.md` | P-FEAT contracts | Industrialise in W04 |

---

## 2. Paper / reference only (do not treat as INF wire)

| Artefact | Path | Use |
| --- | --- | --- |
| aistack tester extract | `blotter/archive/AOS-aistack-run/` (ledger, logs, summaries) | Evidence OS *can* lift EF; **STAY_PAPER** — not INF live wiring |
| AOS promote packet | `blotter/archive/AOS-P7-T04/` | Unsigned; not `AOS_LIVE` |
| AOS phase verify | `tools/aos_phase_verify.py` · `blotter/archive/AOS-VERIFY/` | Keep until INF `make test` replaces |
| AOS policy / retrain docs | `doc/aos_l2_policy_v0.md` · `aos_l2skip_v1.md` · `aos_l5_retrain_loop.md` · `aos_p6_stack.md` · `aos_p7_promotion.md` | Design inputs for W05–W11 |

---

## 3. EDX archives (consume geometry / cells only)

| Artefact | Path | Use |
| --- | --- | --- |
| Bad cells / champ filters evidence | `blotter/archive/EDX-P0-T01/` · `doc/aos_bad_cells.md` | Skip seeds for low bar |
| Harvest champion run | `blotter/archive/EDX-P2-T04/` | Engine dump provenance |
| Growth secondary | `blotter/archive/EDX-P4-T01/` | Optional Δ only |

**Forbidden:** new EDX campaign tasks, re-ranking cells from profit alone, treating incomplete month as admission.

---

## 4. Migration order (suggested)

1. **W02** — schemas; land `T04_Long_8210204.log` + AOS-P1 tape as first fixtures  
2. **W03** — normalise → core; prove EF ≈ 1.77 under ENGINE_BASELINE Leak policy  
3. **W04** — load AOS-P1 tape + AOS-P4 labels into features/train (PIT rebuild preferred over blind CSV trust)  
4. **W05** — import L2skip_v1 as *prior* challenger artefact; retrain produces new semver (never overwrite)  
5. **W06** — compare new CF to both ENGINE_BASELINE_v1 and archived AOS-P4-T03 CF  

---

## 5. Coverage checklist (accept)

- [x] Baseline blotter / Harvest long dump named  
- [x] L1 tape (`AOS-P1-T02`) named  
- [x] L2skip_v1 model + metrics named  
- [x] Shadow CF JSON / decisions named  
- [x] No EDX reopen as campaign  

**Verdict:** ACCEPT · `INF-P0-T04`
