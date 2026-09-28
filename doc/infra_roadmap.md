# BMRG Infra Scale-Up — Weekly Implementation Roadmap

**Version:** 0.2  
**Status:** Active plan — offline-first; no live AI wiring until INF-W09 GO + explicit auth  
**Implementation table:** §2 (master) + per-week Implement tables in §5  
**Detail / contracts:** `doc/infrascaleup.md` (normative for planes, schema, accept bar)  
**Context:** `system_profile.md` · `doc/edge_framework.md` · `doc/ai_OS.md` · `doc/edge_discovery.md` (closed)  
**Engine baseline:** Harvest magic **8210204** · `AOS_BASELINE_v1` · EF **1.77** · n **530** · E_N **+0.091R**

---

## 0. How to use this roadmap

| ID family | Meaning |
| --- | --- |
| **INF-W##** | Calendar implementation week (execute one week at a time) |
| **INF-P#-T##** | Task inside a phase (detail in `infrascaleup.md`) |
| **EXP-*** | Tester export-only preset (never changes EA logic) |

**Rules**

1. Finish the current week’s tasks → week exit checklist → then start the next week.  
2. One **INF-P#-T##** at a time inside the week (first `PENDING` in order).  
3. Offline → shadow → wire. No forward testing in INF-W01–W08.  
4. Default allow; low skip bar; speak WR/R/BM/Leak/EF/E_N/MaxDD/skip-rate — not “AI confidence.”  
5. Do not reopen Edge Discovery; do not treat `aistack` as INF wiring.

**Mandatory sequence**

```
pipelines (W01–W04) → train/shadow (W05–W06) → docker/box (W07–W08)
  → prove gate (W09) → wiring design (W10) → retrain loop (W11)
```

---

## 1. Week board (current)

| Week ID | Phase | Focus | Status |
| --- | --- | --- | --- |
| INF-W01 | INF-P0 | Limitation map + baseline lock | **DONE** (2026-09-27) |
| INF-W02 | INF-P1 | Contract + Postgres schema | **DONE** (2026-09-27) |
| INF-W03 | INF-P2 | Ingest pipeline | **DONE** (2026-09-27) |
| INF-W04 | INF-P3 | Offline L1 / PIT tape | **DONE** (2026-09-27) |
| INF-W05 | INF-P4a | WF harness + L2 train + shadow ledger | **DONE** (2026-09-27) |
| INF-W06 | INF-P4b | CF eval + L3/L4 sim | **DONE** (2026-09-27) |
| INF-W07 | INF-P5a | Observability + Docker compose | **DONE** (2026-09-27) |
| INF-W08 | INF-P5b | Dedicated box + infra tests + agent access | **DONE** (2026-09-27) |
| INF-W09 | INF-P6 | Phase-prove gate (GO/NO-GO) | **DONE** (2026-09-28) · auto NO-GO → **USER GO** |
| INF-W10 | INF-P7 | Wiring plan (design only) | **DONE** (2026-09-28) |
| INF-W11 | INF-P8 | Retrain loop on new stack | **DONE** (2026-09-28) |

**Status:** Infra W01–W11 complete. **EA LIVE_WITHHOLD hook shipped (BMRG v1.21)** — pin model baked in EA; FT programme still needs separate auth.

---

## 2. Implementation table (master)

Execute top → bottom. One `INF-P#-T##` at a time. Status: `PENDING` / `RUNNING` / `DONE` / `REJECTED`.

| Week | Task ID | Plane | Implement (artefact / path) | Responsibility | Status |
| --- | --- | --- | --- | --- | --- |
| INF-W01 | `INF-P0-T01` | P-ACCESS | `doc/infrascaleup.md` §3 · `infra/LIMITATIONS.md` | Lock L-T01…L-T14 + plane ownership | DONE |
| INF-W01 | `INF-P0-T02` | P-OBS | `infra/baselines/ENGINE_BASELINE_v1.json` | Freeze Harvest health vector (EF 1.77 / n 530) | DONE |
| INF-W01 | `INF-P0-T03` | P-ACCESS | `infra/PHASE_EXITS.md` | Measurable exits for W02–W09 | DONE |
| INF-W01 | `INF-P0-T04` | P-DATA | `infra/MIGRATE_FROM_AOS.md` | Inventory AOS archives to migrate (no EDX reopen) | DONE |
| INF-W02 | `INF-P1-T01` | P-DATA | `infra/schemas/adapter_*.schema.json` | Adapter blotter / manifest / metadata contracts | DONE |
| INF-W02 | `INF-P1-T02` | P-STORE | `infra/migrations/versions/0001_core.py` | Postgres schemas raw/core/features/train/score/ops | DONE |
| INF-W02 | `INF-P1-T03` | P-DATA | `infra/landing/**` · `infra/src/ingest/landing.py` | Landing zone + checksum / quarantine | DONE |
| INF-W02 | `INF-P1-T04` | P-STORE | `core.event_manifest` rebuild job | Deterministic `event_id` + declared 1R | DONE |
| INF-W03 | `INF-P2-T01` | P-DATA | `infra/src/ingest/mt5_normalise.py` | Deals/Print → adapter rows | DONE |
| INF-W03 | `INF-P2-T02` | P-DATA | `infra/src/ingest/load_core.py` | Idempotent raw→core load | DONE |
| INF-W03 | `INF-P2-T03` | P-DATA | cost flag columns on core | Defaulted vs measured Leak components | DONE |
| INF-W03 | `INF-P2-T04` | P-TEST | `infra/fixtures/blotter/harvest_long_v1/` · scorecard | E2E replay → baseline EF ≈ 1.77 | DONE |
| INF-W04 | `INF-P3-T01` | P-FEAT | `infra/src/features/pit_builder.py` | PIT features; leakage tests | DONE |
| INF-W04 | `INF-P3-T02` | P-FEAT | `features.tape_tick` · `artefacts/tape/*.parquet` | Materialise L1 tape (aos_l1_v0+) | DONE |
| INF-W04 | `INF-P3-T03` | P-FEAT | `train.label_row` / labelled parquet | Event–feature join; labels; **no skip** | DONE |
| INF-W04 | `INF-P3-T04` | P-ACCESS | `artefacts/tape/LATEST_REGIME_TAPE.parquet` | Trainer-facing tape + manifest | DONE |
| INF-W05 | `INF-P4-T01` | P-TRAIN | `infra/src/train/walkforward.py` | G2-style WF harness (not promote gate) | DONE |
| INF-W05 | `INF-P4-T02` | P-TRAIN | `artefacts/models/L2skip/<semver>/` | Train low-threshold L2 shadow; never overwrite | DONE |
| INF-W05 | `INF-P4-T03` | P-OBS | `score.skip_ledger` · decision JSONL | WOULD_SKIP / FIRE / ALLOW_UNCERTAIN | DONE |
| INF-W06 | `INF-P4-T04` | P-TRAIN | `reports/LATEST_EVAL.json` | CF blotter vs `ENGINE_BASELINE_v1` | DONE |
| INF-W06 | `INF-P4-T05` | P-TRAIN | L3/L4 sim hooks in eval harness | MaxDD/stall/frontier sim (not live) | DONE |
| INF-W07 | `INF-P5-T01` | P-OBS | `infra/artefacts/logs/**` | JSONL + correlation ids | DONE |
| INF-W07 | `INF-P5-T02` | P-OBS | metrics block in `LATEST_EVAL.json` | fire/skip, nulls, stall, cost drift | DONE |
| INF-W07 | `INF-P5-T03` | P-PACK | `infra/docker-compose.yml` · image Dockerfiles | Pin ingest/features/trainer/scorer/eval/postgres | DONE |
| INF-W08 | `INF-P5-T04` | P-BOX | `infra/BOX.md` · queue worker | Dedicated box profile + job queue | DONE |
| INF-W08 | `INF-P5-T05` | P-TEST | `infra/src/**/test_*.py` · FX fixtures | Contract + FX-01…16 + replay + smoke | DONE |
| INF-W08 | `INF-P5-T06` | P-ACCESS | `infra/Makefile` · `README.md` · `.env.example` | `make ingest\|features\|train\|score\|report` | DONE |
| INF-W09 | `INF-P6-T01` | P-OBS | `reports/INF-P6-T01_phaseProve.json` | W250/W500 baseline vs shadow | DONE |
| INF-W09 | `INF-P6-T02` | P-OBS | `INF-P6-T02_skip_audit.md` | Skip-cluster audit (hostile cells only) | DONE |
| INF-W09 | `INF-P6-T03` | P-ACCESS | `doc/infra_wiring_eligibility.md` | GO / NO-GO for wiring design | DONE · **NO-GO** |
| INF-W10 | `INF-P7-T01` | P-ACCESS | `doc/infra_wiring_plan.md` | L2/L3 attach design (permit/withhold) | DONE |
| INF-W10 | `INF-P7-T02` | P-TRAIN | wiring plan § champ/challenger | Promote/rollback runbook + dry-run | DONE |
| INF-W10 | `INF-P7-T03` | P-DATA | `EXP-P7-T03_export_Harvest_long.set` | Export-only preset (optional; no AI gate) | DONE |
| INF-W11 | `INF-P8-T01` | P-TRAIN | `infra/src/train/retrain_loop.py` | Scheduled + trigger retrain (shadow) | DONE |
| INF-W11 | `INF-P8-T02` | P-TRAIN | `ops.eval_run` gate before pin | Shadow ACCEPT required to pin | DONE |
| INF-W11 | `INF-P8-T03` | P-TRAIN | new model semver | Post-wire retrain **only if authorised** | DONE |

---

## 3. Weekly cadence

| Step | Action |
| --- | --- |
| Start of week | Read §2 implementation table rows for that week; touch only listed task IDs |
| During week | Execute tasks in ID order; one at a time; mark Status in §2 |
| End of week | Run week exit checklist; archive under `blotter/archive/INF-W##/` or per-task `INF-P#-T##/` |
| Pass | Mark week `DONE` in §1 and task rows `DONE` in §2; open next week |
| Fail | Stay on same week; fix gaps only — no scope adds / no live wire |

---

## 4. Accept bar (every training / eval week)

| Check | Bar |
| --- | --- |
| n remaining | ≥ 100 (warn if &lt; 385) |
| W250 EF | ≥ baseline EF − 1 pp |
| W250 MaxDD | ≤ baseline MaxDD + 2 pp |
| Fires | warn &lt; 70% baseline; hard-concern &lt; 50% (`FREQUENCY_STALL`) |
| Payoff trap | WR↑ + E_N↓ → reject |
| G0–G5 | Not required for week accept |

---

## 5. Weekly implementation phases

Detail contracts: `doc/infrascaleup.md`. Rows below are the **write / implement** tables for each week (same role as File | Responsibility in `roadmap.md`).

### INF-W01 — Lock (INF-P0)

**Week ID:** `INF-W01` · **Phase:** `INF-P0`  
**Goal:** Catalogue limits; freeze engine baseline; no Docker, no training.

**Implement (batch, then check)**

| Task ID | File / path | Responsibility |
| --- | --- | --- |
| `INF-P0-T01` | `infra/LIMITATIONS.md` (+ confirm `infrascaleup.md` §3) | Lock L-T01…L-T14; map each to plane + later task |
| `INF-P0-T02` | `infra/baselines/ENGINE_BASELINE_v1.json` | Copy AOS_BASELINE_v1; EF 1.77 / n 530 / magic 8210204 |
| `INF-P0-T03` | `infra/PHASE_EXITS.md` | Exit criteria for W02–W09 in framework symbols |
| `INF-P0-T04` | `infra/MIGRATE_FROM_AOS.md` | List AOS blotter/tape/L2skip/shadow CF sources |

**Week exit (`INF-W01`)**

- [x] Every L-Txx referenced by ≥1 later task  
- [x] Baseline JSON matches `doc/ai_OS_baseline.md`  
- [x] No EDX reopen; migrate inventory complete  
- [x] §2 Status → DONE for P0-T01…T04  

---

### INF-W02 — Contract + schema (INF-P1)

**Week ID:** `INF-W02` · **Phase:** `INF-P1`  
**Goal:** Adapter contract → Postgres + landing zone; rebuild events / 1R.

**Implement (batch, then check)**

| Task ID | File / path | Responsibility |
| --- | --- | --- |
| `INF-P1-T01` | `infra/schemas/adapter_blotter.schema.json` · `event_manifest.schema.json` · `ea_metadata.schema.json` | Formal adapter contract (+ BMRG extras) |
| `INF-P1-T02` | `infra/migrations/versions/0001_core.py` | Create raw/core/features/train/score/ops + core tables |
| `INF-P1-T03` | `infra/landing/{inbox,staging,quarantine}/` · `infra/src/ingest/landing.py` | Checksum landing; quarantine corrupt drops |
| `INF-P1-T04` | event rebuild loader → `core.event_manifest` | Deterministic `event_id`; declared 1R from SL×vol×tick |

**Week exit (`INF-W02`)**

- [x] Migrations upgrade/downgrade clean  
- [x] Schema rejects missing `equity_at_open` / `risk_ccy`  
- [x] Rebuild ≈ 530 events; 1R consistent with SL300  
- [x] §2 Status → DONE for P1-T01…T04  

---

### INF-W03 — Ingest (INF-P2)

**Week ID:** `INF-W03` · **Phase:** `INF-P2`  
**Goal:** Export → validate → load; idempotent; e2e replay = baseline.

**Implement (batch, then check)**

| Task ID | File / path | Responsibility |
| --- | --- | --- |
| `INF-P2-T01` | `infra/src/ingest/mt5_normalise.py` | MT5 deals CSV + `[BMRG][TRADE]` → adapter rows |
| `INF-P2-T02` | `infra/src/ingest/load_core.py` | Idempotent upsert raw→core by sha256 / event_id |
| `INF-P2-T03` | core cost columns / JSON | Flag `costs_defaulted` vs measured per component |
| `INF-P2-T04` | `infra/fixtures/blotter/harvest_long_v1/` · score job | Freeze dump; replay → health vector ≈ baseline |

**Week exit (`INF-W03`)**

- [x] Load twice → row counts unchanged  
- [x] Leak source flagged; proxy ≈ 2.2 pp under same policy  
- [x] Scorecard EF identity under Leak 2.2 (≈2.33; doc 1.77 gap noted)  
- [x] §2 Status → DONE for P2-T01…T04  

---

### INF-W04 — Offline L1 tape (INF-P3)

**Week ID:** `INF-W04` · **Phase:** `INF-P3`  
**Goal:** PIT features + labels; **zero live skips**; trainer-ready tape.

**Implement (batch, then check)**

| Task ID | File / path | Responsibility |
| --- | --- | --- |
| `INF-P3-T01` | `infra/src/features/pit_builder.py` · leakage tests | Features only from bars ≤ signal; forbid future leak |
| `INF-P3-T02` | `features.tape_tick` · `artefacts/tape/harvest_l1.parquet` | Materialise L1 (session/vol/structure as available) |
| `INF-P3-T03` | `train.label_row` / labelled parquet | Join features→events; y_lose / pnl_R; no policy |
| `INF-P3-T04` | `artefacts/tape/LATEST_REGIME_TAPE.parquet` + manifest | Stable path for trainer / agent Read |

**Week exit (`INF-W04`)**

- [x] Leakage pytest green  
- [x] ≥95% events joined; Tue=0; LON_NY/NY ≥95% on champ  
- [x] Fire count unchanged vs baseline  
- [x] §2 Status → DONE for P3-T01…T04  

---

### INF-W05 — Train + shadow ledger (INF-P4a)

**Week ID:** `INF-W05` · **Phase:** `INF-P4` (part A)  
**Goal:** Walk-forward harness; train low-threshold L2; shadow decisions only.

**Implement (batch, then check)**

| Task ID | File / path | Responsibility |
| --- | --- | --- |
| `INF-P4-T01` | `infra/src/train/walkforward.py` | Anchored/rolling folds; fit through decay |
| `INF-P4-T02` | `artefacts/models/L2skip/<semver>/` · `ops.model_version` | Train P(lose); low skip threshold; never overwrite |
| `INF-P4-T03` | `score.skip_ledger` · decision JSONL | Log WOULD_SKIP / WOULD_FIRE / ALLOW_UNCERTAIN |

**Week exit (`INF-W05`)**

- [x] No fit-only-on-decay  
- [x] New `model_semver` written  
- [x] Actual fires = engine baseline (shadow only)  
- [x] §2 Status → DONE for P4-T01…T03  

---

### INF-W06 — Counterfactual prove (INF-P4b)

**Week ID:** `INF-W06` · **Phase:** `INF-P4` (part B)  
**Goal:** CF blotter vs baseline; L3/L4 sim in harness; protect-don’t-overfilter.

**Implement (batch, then check)**

| Task ID | File / path | Responsibility |
| --- | --- | --- |
| `INF-P4-T04` | `infra/src/eval/cf_eval.py` · `reports/LATEST_EVAL.json` | Remove WOULD_SKIP; Stage 0–2 vs baseline |
| `INF-P4-T05` | `infra/src/eval/l3_l4_sim.py` | Simulate MaxDD halt / stall / Below-frontier f=0 |

**Week exit (`INF-W06`)**

- [x] Full framework vector on CF blotter  
- [x] §4 accept bar held (or explicit REJECT)  
- [x] Fires ≥70% preferred; &lt;50% = fail week  
- [x] §2 Status → DONE for P4-T04…T05  

---

### INF-W07 — Observability + Docker (INF-P5a)

**Week ID:** `INF-W07` · **Phase:** `INF-P5` (part A)  
**Goal:** Structured logs + metrics; compose stack local = server images.

**Implement (batch, then check)**

| Task ID | File / path | Responsibility |
| --- | --- | --- |
| `INF-P5-T01` | `infra/src/obs/jsonl_log.py` · `artefacts/logs/` | JSONL with event_id / run_id / model_semver |
| `INF-P5-T02` | `infra/src/obs/metrics.py` · `LATEST_EVAL.json` | fire/skip, lag, nulls, cost drift, FREQUENCY_STALL |
| `INF-P5-T03` | `infra/docker-compose.yml` · `images/*/Dockerfile` · `IMAGE_LOCK.json` | Pin ingest/features/trainer/scorer/eval/postgres |

**Week exit (`INF-W07`)**

- [x] Trace one `event_id` ingest→score  
- [x] Compose smoke + replay works  
- [x] §2 Status → DONE for P5-T01…T03  

---

### INF-W08 — Box + tests + agent access (INF-P5b)

**Week ID:** `INF-W08` · **Phase:** `INF-P5` (part B)  
**Goal:** Heavy jobs off tester; infra tests; `make` for Cursor.

**Implement (batch, then check)**

| Task ID | File / path | Responsibility |
| --- | --- | --- |
| `INF-P5-T04` | `infra/BOX.md` · `src/jobqueue/` · redis+worker | Dedicated box CPU/RAM/disk + Redis list worker |
| `INF-P5-T05` | `fixtures/fx/` · `test_fx.py` · `test_p5b_suite.py` | FX-01…16, contract, replay freeze, migration dry-run |
| `INF-P5-T06` | `Makefile` · `make.bat` · `AGENT_PATHS.md` · `.env.example` | `make ingest\|features\|train\|score\|report\|test` |

**Week exit (`INF-W08`)**

- [x] Heavy job on box while tester idle  
- [x] `make test` green (no live FT)  
- [x] Agent Reads `LATEST_EVAL.json` without Tester UI  
- [x] §2 Status → DONE for P5-T04…T06  

---

### INF-W09 — Phase-prove gate (INF-P6)

**Week ID:** `INF-W09` · **Phase:** `INF-P6`  
**Goal:** Offline baseline vs shadow OS; GO/NO-GO. Still no live preset.

**Implement (batch, then check)**

| Task ID | File / path | Responsibility |
| --- | --- | --- |
| `INF-P6-T01` | `infra/src/eval/phase_prove.py` · `reports/INF-P6-T01_phaseProve.json` | W250/W500 engine vs shadow (full framework fields) |
| `INF-P6-T02` | `INF-P6-T02_skip_audit.md` | Justify every skip cluster (hostile / modest-confidence only) |
| `INF-P6-T03` | `doc/infra_wiring_eligibility.md` | GO / NO-GO for INF-W10 |

**Week exit (`INF-W09`)**

- [x] EF held/lifted; not starving (fires &lt;50% → NO-GO) — EF +0.67pp · fires 92.6%  
- [x] No skip cluster justified only by higher WR — **3 edge overfilter clusters FAIL audit**  
- [x] **GO** → W10; **NO-GO** → return W05/W06 — **NO-GO issued**  
- [x] §2 Status → DONE for P6-T01…T03  

---

### INF-W10 — Wiring plan design (INF-P7)

**Week ID:** `INF-W10` · **Phase:** `INF-P7`  
**Goal:** Design L2/L3 attach + rollback. **Not** FT / `AOS_LIVE` unless authorised.

**Implement (batch, then check)**

| Task ID | File / path | Responsibility |
| --- | --- | --- |
| `INF-P7-T01` | `doc/infra_wiring_plan.md` | Permit/withhold hooks; L3 precedence; kill-switch |
| `INF-P7-T02` | wiring plan § + dry-run fixture | Champion/challenger promote + one-command rollback |
| `INF-P7-T03` | `Profiles/Tester/BMRG/EXP-P7-T03_export_Harvest_long.set` | Optional export-only; engine logic unchanged |

**Week exit (`INF-W10`)**

- [x] Plan covers pin, rollback, L3 outrank  
- [x] Champ/challenger dry-run correct  
- [x] No live AI gate shipped  
- [x] §2 Status → DONE for P7-T01…T03  

---

### INF-W11 — Retrain loop (INF-P8)

**Week ID:** `INF-W11` · **Phase:** `INF-P8`  
**Goal:** Scheduled + trigger retrain on new stack; shadow before pin.

**Implement (batch, then check)**

| Task ID | File / path | Responsibility |
| --- | --- | --- |
| `INF-P8-T01` | `infra/src/train/retrain_loop.py` · ops schedules | Monthly + Compressing/Near-frontier enqueue |
| `INF-P8-T02` | shadow gate before `ops.model_version` pin | Challenger must pass §4 bar vs baseline + champ |
| `INF-P8-T03` | new model semver artefact | Post-wire retrain only if user authorised wire |

**Week exit (`INF-W11`)**

- [x] Dry-run: enqueue → train → shadow → no silent live swap  
- [x] Failed challenger never pins  
- [x] T03 blocked unless authorised  
- [x] §2 Status → DONE for P8-T01…T03  

---

## 6. ID quick reference

### 6.1 Weeks → phases

| Week | Phase IDs | Task IDs |
| --- | --- | --- |
| INF-W01 | INF-P0 | P0-T01…T04 |
| INF-W02 | INF-P1 | P1-T01…T04 |
| INF-W03 | INF-P2 | P2-T01…T04 |
| INF-W04 | INF-P3 | P3-T01…T04 |
| INF-W05 | INF-P4 | P4-T01…T03 |
| INF-W06 | INF-P4 | P4-T04…T05 |
| INF-W07 | INF-P5 | P5-T01…T03 |
| INF-W08 | INF-P5 | P5-T04…T06 |
| INF-W09 | INF-P6 | P6-T01…T03 |
| INF-W10 | INF-P7 | P7-T01…T03 |
| INF-W11 | INF-P8 | P8-T01…T03 |

### 6.2 Planes (what each week builds toward)

| Plane | Primary weeks |
| --- | --- |
| P-ACCESS / P-OBS | W01, W07, W08, W09 |
| P-DATA / P-STORE | W02, W03 |
| P-FEAT | W04 |
| P-TRAIN | W05, W06, W11 |
| P-PACK / P-BOX / P-TEST | W07, W08 |

---

## 7. Definition of infra scale-up “implementation complete”

All must be true:

- [ ] INF-W01–W08 exit checklists passed  
- [ ] INF-W09 GO (or documented NO-GO with return path)  
- [ ] INF-W10 wiring **design** written  
- [ ] INF-W11 retrain loop operable in shadow  
- [ ] Engine Harvest geometry unchanged; intelligence only permit/withhold (shadow until authorised)  
- [ ] Agent path: `make -C infra report` → `LATEST_EVAL.json` without Tester UI  

Live wire / `AOS_LIVE` / forward testing are **out of this roadmap** unless a later authorised task says so.

---

## 8. Document map

| File | Role |
| --- | --- |
| `doc/infra_roadmap.md` | **This file** — week board · **§2 implementation table** · weekly write tables |
| `doc/infrascaleup.md` | Normative planes, schema, task contracts, recipes |
| `doc/ai_OS.md` | L1–L10 layer semantics (consume) |
| `system_profile.md` | Engine behaviour / limits |
| `doc/edge_framework.md` | Stage scoring + adapter |
| `doc/edge_discovery.md` | Bad cells (closed campaign) |
| `doc/ai_OS_baseline.md` | Frozen engine health vector |

---

## 9. Versioning

- **0.2** — Master implementation table (§2) + per-week Implement (File/path | Responsibility) tables.  
- **0.1** — Initial weekly roadmap INF-W01…W11 mapped to INF-P0…P8 tasks.  
- Bump when a week completes or week boundaries change.
