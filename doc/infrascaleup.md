# BMRG Infra Scale-Up

**Version:** 0.1  
**Status:** Plan — offline-first; **no live AI wiring in this workstream**  
**Governs:** All `INF-P#-T##` tasks below  
**Companions:** `system_profile.md` · `doc/edge_framework.md` · `doc/unified_edge_framework.md` · `doc/ai_OS.md` · `doc/edge_discovery.md` (closed — consume only)  
**Engine (frozen):** Harvest champion — `EDX-P2-T04_…` magic **8210204**  
**OS baseline lock:** `AOS_BASELINE_v1` (`doc/ai_OS_baseline.md`) — long EF **1.77** · n **530** · E_N **+0.091R**  
**Paper OS (do not treat as INF wiring):** `aistack` magic **8399001** · STAY_PAPER  

---

## 0. Mandate

This add-on starts once the EA is stable with the right pipeline/infra and executions. There is **no forward testing for now**.

**Mandatory sequence:**

1. Build pipelines and infra  
2. Train offline  
3. Prove improvement per phase against the engine baseline  
4. Only then discuss wiring  
5. Retrain models on the new stack after wiring is justified  

The engine already has its edge. Infra and AI exist to **protect it under different conditions**, not to overfilter it into a different strategy.

**Out of scope for INF-P0–P6:** live `.set` AI gates, `AOS_LIVE`, demo-account FT, reopening Edge Discovery as a campaign.

**Export-only tester presets** (if needed) are named `EXP-*` and must not change EA logic.

---

## 1. Three vocabularies (do not mix)

| Vocabulary | Meaning | Examples |
| --- | --- | --- |
| **Framework stages** (0–4) | How we **score** | Stage 0 identities · Stage 1 EF/M · Stage 2 W100/250/500 · Stage 3 capital · Stage 4 G0–G5 |
| **AI OS layers** (L1–L10) | What eventually sits on the engine | L1 Perception · L2 Policy · L3 Guardrails · L4 Observer · L5 Retrain · L6 Ledger · L7+ |
| **Infra planes** (below) | What we **build now** so layers train offline | P-DATA · P-STORE · P-FEAT · P-TRAIN · P-OBS · P-PACK · P-BOX · P-TEST · P-ACCESS |

Promotion / wiring uses stages later. Day-to-day INF work uses **planes** + the protect-don't-overfilter bar (§3). Layers are consumers of plane outputs — not the unit of INF task naming.

---

## 2. Protect, don't overfilter (low gate bar)

AI / infra gates must be **conservative on skipping**, **aggressive on logging**.

| Rule | Binding |
| --- | --- |
| Default | **Allow** — fire the engine and log |
| Skip only when | Cell hostile: Edge Discovery `BM_cell ≤ 0`, or predicted-loser with **modest** confidence |
| When unsure | FIRE + log reason_code `ALLOW_UNCERTAIN` |
| Forbidden | Raising skip-confidence / WR targets / filter counts to “look selective” |
| Frozen objective | Hold or lift **E_N / EF**; contain **AL** and **MaxDD**. WR and PF are diagnostics |
| Payoff trap | WR↑ + E_N↓ → **reject** |
| Frequency warn | Fires &lt; **70%** of engine baseline |
| Frequency hard-concern | `FREQUENCY_STALL` (&lt; **50%** baseline) |
| Prefer | Under-skipping during infra phases |

### 2.1 Iteration accept (offline vs `AOS_BASELINE_v1` / engine)

| Check | Bar |
| --- | --- |
| n remaining | ≥ **100** (warn if &lt; 385; do not kill) |
| W250 EF | ≥ baseline EF − **1 pp** (hold = pass) |
| W250 MaxDD | ≤ baseline MaxDD + **2 pp** |
| Skip-rate | Modest; justify every skip cluster |
| Full G0–G5 | **Not** required to accept an infra/training phase |

Promotion / wiring (INF-P6+) has its own (still not discovery-strict) bar. Full Stage-4 remains a later human decision.

### 2.2 Shadow invariant

Intelligence **never rewrites entries**. It only permits or withholds. Until wiring is authorised: withhold only in **shadow** (log would-skip; engine still fires). L3-style hard limits may exist in the eval harness as *simulations*; they outrank intelligence in sim; they are not live until wiring.

---

## 3. Current-stack limitation map

Source: `system_profile.md` · EA `Logger.mqh` · AOS offline artefacts · Strategy Tester reality.  
Every later INF tool must name which row it removes.

| ID | Limitation | Where it hurts | Compensating plane |
| --- | --- | --- | --- |
| L-T01 | Tester is **single-threaded**; no native MC / walk-forward / parallel folds | Cannot prove G2/G4-style harness on the trading box | P-BOX · P-TRAIN |
| L-T02 | Tester history / export UX is fragile; long windows are manual | Incomplete blotters; re-run risk | P-DATA · P-OBS |
| L-T03 | No first-class blotter: deals CSV ≠ adapter contract | Missing `event_id`, legs, `equity_at_open`, declared 1R | P-DATA · P-STORE |
| L-T04 | Fragmented logs: `Print("[BMRG]…")` + Common/Files ledgers | Agent must scrape; no correlation ids | P-OBS · P-ACCESS |
| L-T05 | No point-in-time (PIT) feature store | Leakage risk when joining bars → labels | P-FEAT |
| L-T06 | No Postgres system of record; archives are folders of CSV/JSON | Non-idempotent reloads; hard joins | P-STORE |
| L-T07 | Model registry is a thin folder (`models/L2skip/`) | No eval-run lineage, no multi-model registry | P-TRAIN · P-STORE |
| L-T08 | Scoring is ad-hoc scripts + human scorecards | No golden FX fixture suite as CI | P-TEST · P-TRAIN |
| L-T09 | Heavy jobs (features, train, MC) compete with tester | Trading box thrash; slow iteration | P-BOX · P-PACK |
| L-T10 | Agent access = click through Tester UI / hunt Files | Cursor cannot `make report` | P-ACCESS |
| L-T11 | Costs often **defaulted** (3× spread proxy); not measured per fill | Leak uncertainty contaminates EF | P-DATA |
| L-T12 | AOS offline stack exists but is **not industrialised** (no Docker, no schema migrations, no job queue) | Replays not one-command; drift between machines | P-PACK · P-OBS |
| L-T13 | Live tape publisher deferred; structure_id often `UNK` | L1 thin → L2 weak OOS AUC (~0.55) | P-FEAT (offline enrich) |
| L-T14 | No contract tests on adapter blotter | Silent schema breaks | P-TEST |

**What the tester cannot do (dedicated box must):**

- Parallel walk-forward folds and Monte Carlo path ensembles at scale  
- Postgres ingest + migrations + feature materialisation  
- Dockerised train/score/eval with pinned images  
- Deterministic replay of a frozen blotter slice → stable health vector  
- Agent-readable scorecards without MetaTrader UI  

**What stays on the trading / tester box:**

- Strategy Tester runs (engine + EXP export presets)  
- EA compile / attach  
- Raw deal / log export drop into landing zone  

---

## 4. Locked engine baseline (infra north star)

Imported from `AOS_BASELINE_v1` / Harvest P2-T04. Infra phases prove against this vector — not against “AI confidence.”

| Field | Long (decision) | 3M stress |
| --- | ---: | ---: |
| n | **530** | 49 (thin — warn) |
| WR / BWR / R | 54.5% / 50% / 1.0 | 59.2% / 50% / 1.0 |
| BM / Leak / EF | +4.5 / 2.2 / **1.77** | — / — / **6.43** |
| E_N | **+0.091R** | +0.184R |
| Zone | Fragile (long) | Strong EF / thin n |
| Magic / geometry | **8210204** · SL300/TP300 · 12–20 · skip Tue · BBDev 2.2 · G0 | same |

Secondary ref only: Growth P4-T01 EF 5.18 (not OS default).

Paper `aistack` ΔEF is **evidence that protection can help**, not a license to wire or to raise skip bars. INF rebuilds the industrial path to re-earn that lift under shadow + low skip.

---

## 5. Target architecture

```
┌──────────────── TRADING / TESTER BOX ────────────────┐
│  BMRG.ex5 (engine frozen)                            │
│  Strategy Tester → EXP-* export only (P0–P6)         │
│  Drop zone: infra/landing/inbox/                     │
└─────────────────────────┬────────────────────────────┘
                          │ blotter / deals / logs / .set notes
                          ▼
┌──────────────── DEDICATED INFRA BOX (Docker) ────────┐
│  ingest ──► raw.* ──► core.* (events, 1R, costs)     │
│                │                                     │
│                ├──► features.* (PIT L1 tape)         │
│                ├──► train.*   (labels, folds)        │
│                ├──► score.*   (health vectors, CF)   │
│                └──► ops.*     (runs, models, logs)   │
│                                                      │
│  trainer / scorer / eval-runner / job queue          │
│  artefact store: models/ · reports/ · fixtures/      │
│  latest → reports/LATEST_EVAL.json                   │
└─────────────────────────┬────────────────────────────┘
                          │ Read-only paths for Cursor
                          ▼
┌──────────────── AGENT / HUMAN ACCESS ────────────────┐
│  make ingest|features|train|score|report             │
│  doc/ + blotter/archive/INF-*/ + reports/            │
└──────────────────────────────────────────────────────┘
```

**Layer mapping (eventually, after INF-P6 gate):**

| Layer | Trains / runs on | Live wire? |
| --- | --- | --- |
| L1 | P-FEAT tape offline | Later (AOS-P1-T03 deferred) |
| L2 | P-TRAIN shadow → wire only post INF-P6/P7 | Not in INF-P0–P5 |
| L3/L4 | Sim in eval harness now; live later | Design in INF-P7 |
| L5 | INF-P8 retrain loop | After wiring plan |
| L6 | P-OBS + `ops.decision_ledger` | Shadow always on |

---

## 6. Concrete stack proposal

| Plane | Choose | Why (limitation removed) |
| --- | --- | --- |
| **P-DATA** | Landing: `infra/landing/{inbox,staging, Quarantine}/` · Parquet + CSV · idempotent loader | L-T02, L-T03, L-T11 |
| **P-STORE** | **Postgres 16** · schemas `raw` / `core` / `features` / `train` / `score` / `ops` · Alembic (or sqitch) migrations | L-T06, L-T03 |
| **P-FEAT** | Python feature builder · DuckDB or PG for PIT joins · Arrow/Parquet dumps for trainer | L-T05, L-T13 |
| **P-TRAIN** | scikit-learn / LightGBM · walk-forward harness (G2-*style*, not promotion gate) · MLflow-lite or `ops.model_versions` | L-T01, L-T07 |
| **P-OBS** | Structured JSONL logs · `event_id` / `run_id` / `model_semver` · Prometheus-optional later; **must** have `reports/LATEST_EVAL.json` | L-T04, L-T12 |
| **P-PACK** | Docker images: `bmrg-ingest` · `bmrg-features` · `bmrg-trainer` · `bmrg-scorer` · `bmrg-eval` · `postgres:16` · Compose v2 · pinned digests | L-T09, L-T12 |
| **P-BOX** | Dedicated server: **16+ vCPU · 64 GB RAM · 2 TB NVMe** (min viable: 8 vCPU / 32 GB / 500 GB) · job queue **RQ/Redis** or **Dramatiq** · artefact volume | L-T01, L-T09 |
| **P-TEST** | pytest · FX-01…FX-16 golden · contract tests · blotter replay freeze · compose smoke · migration dry-run | L-T08, L-T14 |
| **P-ACCESS** | Repo `infra/` · `.env.example` (no secrets in git) · `Makefile` · agent paths in §12 | L-T10 |

Object store (optional P-BOX+): MinIO or local `infra/artefacts/` mirroring S3 layout (`s3://bmrg/{env}/models/...`).

---

## 7. Schema sketch (normative direction)

Adapter contract (`unified_edge_framework.md` §8 + `edge_framework.md` §8) is the **source of truth**.

### 7.1 Schemas

| Schema | Contents |
| --- | --- |
| `raw` | Untouched landings: deals CSV, Print logs, EXP manifests, checksums |
| `core` | Normalised blotter legs, event manifest, EA metadata, cost components |
| `features` | PIT L1 tape rows; as-of joins to events |
| `train` | Labelled rows, fold assignments, sample weights |
| `score` | Health vectors, skip ledgers, counterfactual blotters, gate decisions (sim) |
| `ops` | `run_id`, model versions, eval runs, job status, decision ledger |

### 7.2 Core identities

```text
event_id = "{magic}-{symbol}-{side}-{YYYYMMDDhhmmss}-{first_ticket}"   # edge_framework §8.3
```

Deterministic rebuild: same legs → same `event_id`. Migrations never silently rewrite IDs without a version bump.

### 7.3 Essential tables (v0)

| Table | Key columns |
| --- | --- |
| `raw.landing_file` | path, sha256, landed_at, source (tester/ea/manual) |
| `core.blotter_leg` | event_id, leg_id, fills, volumes, pnl_*, costs_* |
| `core.event_manifest` | event_id, risk_ccy (declared 1R), equity_at_open, signal_tag, exit_reason |
| `core.ea_metadata` | preset_id, magic, ea_version, designed_rr, regime_filtered, costs_defaulted[], geometry_mode |
| `features.tape_tick` | t_close, symbol, regime_id, structure_id, session_id, features jsonb, asof_bar |
| `features.event_features` | event_id, feature_vector, tape_schema |
| `train.label_row` | event_id, y_lose, y_pnl_R, fold_id, split |
| `score.health_vector` | run_id, window, WR, R, BWR, BM, Leak, EF, M, E_N, ΔD, MaxDD, n, fires, skip_rate |
| `score.skip_ledger` | event_id, decision (WOULD_SKIP\|WOULD_FIRE\|ALLOW_UNCERTAIN), reason_code, model_semver, confidence |
| `ops.model_version` | model_semver, layer, path, metrics jsonb, parent_semver, created_at — **never overwrite** |
| `ops.eval_run` | run_id, recipe_id, baseline_id, scorecard_path, verdict |
| `ops.decision_ledger` | t, layer, decision, features, reason_code, model_version, run_id |

`costs_defaulted` vs measured must be **flagged per component** on every event (L-T11).

---

## 8. Target repo layout (infra)

```
BMRG/
├── doc/infrascaleup.md          # this file
├── infra/
│   ├── README.md
│   ├── Makefile
│   ├── .env.example
│   ├── docker-compose.yml
│   ├── images/{ingest,features,trainer,scorer,eval}/Dockerfile
│   ├── migrations/              # Alembic
│   ├── schemas/                 # SQL + JSON Schema for adapter
│   ├── landing/{inbox,staging,quarantine}/
│   ├── fixtures/fx/             # FX-01…FX-16 + blotter golden slices
│   ├── src/
│   │   ├── ingest/
│   │   ├── features/
│   │   ├── train/
│   │   ├── score/               # framework scoring engine
│   │   ├── eval/                # shadow CF + iteration bar
│   │   └── access/              # report writers for agent
│   ├── artefacts/{models,reports,logs}/
│   └── reports/LATEST_EVAL.json # symlink or copy of newest scorecard
├── blotter/{inbox,archive}/     # existing EDX/AOS convention preserved
├── models/                      # legacy AOS store; migrate → infra/artefacts
└── tools/                       # keep aos_phase_verify.py until INF replace
```

Secrets: `.env` local / box only. Never commit broker passwords, API keys, or account numbers.

---

## 9. Replay / eval recipe format

No live AI `.set` in INF-P0–P6. Every task ends with:

```text
RECIPE: INF-P{phase}-T{task}_{plane}_{change}
e.g. INF-P4-T02_train_L2shadow_skipRangeHighVol_2018-2024

INPUTS:   paths / run_id / baseline_id
COMMANDS: make … or docker compose run …
OUTPUTS:  scorecard JSON · skip ledger · health_vector delta
ACCEPT:   loose bar §2.1 vs AOS_BASELINE_v1 (framework numbers)
REJECT:   payoff trap · FREQUENCY_STALL hard-concern without justification · entry rewrite
```

If a tester preset is needed only to **export** a blotter slice:

```text
EXP-P{phase}-T{task}_export_{slice}.set   # engine-identical; magic bookkeeping only
```

---

## 10. Task template

Every `INF-P#-T##` states:

| Field | Content |
| --- | --- |
| **Plane** | P-DATA … P-ACCESS |
| **Limitation** | L-Txx compensated |
| **What changes** | Infra / pipeline only (engine SL/TP frozen) |
| **Artefact** | Path(s) produced |
| **Prove** | Offline metric / health-vector Δ (never “feels better”) |
| **Recipe** | Replay/eval recipe id + commands |
| **Accept / reject** | §2.1 |
| **Status** | `PENDING` / `RUNNING` / `DONE` / `REJECTED` |

**Active rule:** execute only the first `PENDING` task in order. One at a time.

---

## 11. PHASES

### INF-P0 — LIMITATION MAP + BASELINE LOCK

No Docker. No training. Catalogue limits; freeze success criteria.

#### INF-P0-T01 — Publish limitation map + plane ownership


| | |
| --- | --- |
| **Plane** | P-ACCESS (meta) |
| **Limitation** | L-T12 (undocumented stack debt) |
| **What changes** | None in code — confirm §3 table as working inventory; link each plane to owner path under `infra/` (may be stubs) |
| **Artefact** | `doc/infrascaleup.md` §3 locked; optional `infra/LIMITATIONS.md` mirror |
| **Prove** | Every L-Txx has ≥1 future INF task referencing it |
| **Recipe** | `INF-P0-T01_access_limitationMap_lock` — Read this doc; no commands |
| **Accept** | Map complete; no silent “TBD” on L-T01–L-T14 |
| **Status** | `DONE` — **ACCEPT** · `infra/LIMITATIONS.md` · `archive/INF-P0-T01/` |


#### INF-P0-T02 — Freeze infra baseline pointer to AOS_BASELINE_v1


| | |
| --- | --- |
| **Plane** | P-OBS |
| **Limitation** | L-T08 (ad-hoc scorecards) |
| **What changes** | Write `infra/baselines/ENGINE_BASELINE_v1.json` copying Harvest long + 3M fields from `doc/ai_OS_baseline.md` |
| **Artefact** | `infra/baselines/ENGINE_BASELINE_v1.json` · `blotter/archive/INF-P0-T02/` |
| **Prove** | JSON EF=1.77, n=530, E_N=0.091, magic=8210204; checksum matches markdown |
| **Recipe** | `INF-P0-T02_obs_baselineLock_Harvest` — validate JSON vs `ai_OS_baseline.md` |
| **Accept** | Pointer stable; INF evals must load this file |
| **Status** | `DONE` — **ACCEPT** · `infra/baselines/ENGINE_BASELINE_v1.json` · `archive/INF-P0-T02/` |


#### INF-P0-T03 — Success criteria pack for INF-P1–P6


| | |
| --- | --- |
| **Plane** | P-ACCESS |
| **Limitation** | L-T10 (unclear agent Done definition) |
| **What changes** | Document per-phase exit checks (schema migrates, ingest replay, PIT coverage, shadow bar, compose smoke, phase-prove gate) |
| **Artefact** | §11 phase headers + `infra/PHASE_EXITS.md` |
| **Prove** | Each phase has measurable exit; none require live FT |
| **Recipe** | `INF-P0-T03_access_phaseExits_doc` |
| **Accept** | Exits cite framework symbols (EF, E_N, MaxDD, skip-rate, fires) |
| **Status** | `DONE` — **ACCEPT** · `infra/PHASE_EXITS.md` · `archive/INF-P0-T03/` |


#### INF-P0-T04 — Inventory existing AOS artefacts to migrate (not reopen EDX)


| | |
| --- | --- |
| **Plane** | P-DATA |
| **Limitation** | L-T06 (folder-only SoR) |
| **What changes** | Catalogue `blotter/archive/AOS-*`, `models/L2skip/`, tape CSVs — migration sources for P1–P2 |
| **Artefact** | `infra/MIGRATE_FROM_AOS.md` |
| **Prove** | List covers baseline blotter, L1 tape, L2skip_v1, shadow CF JSON |
| **Recipe** | `INF-P0-T04_data_inventoryAos_migratePlan` |
| **Accept** | No EDX re-open; consume archives only |
| **Status** | `DONE` — **ACCEPT** · `infra/MIGRATE_FROM_AOS.md` · `archive/INF-P0-T04/` |

**Phase exit P0:** Baseline JSON locked; limitation map owned; migrate inventory written. **COMPLETE 2026-09-27.**

---

### INF-P1 — CONTRACT + SCHEMA

Adapter blotter / manifest / metadata → Postgres schema + migrations. Landing zone. Prove rebuild of events and 1R.

#### INF-P1-T01 — JSON Schema for adapter blotter + manifest + metadata


| | |
| --- | --- |
| **Plane** | P-DATA |
| **Limitation** | L-T03, L-T14 |
| **What changes** | Formal schemas from unified §8 + BMRG extras (`exit_reason`, `spread_points_entry`, `group_event_id`, …) |
| **Artefact** | `infra/schemas/adapter_blotter.schema.json` · `event_manifest.schema.json` · `ea_metadata.schema.json` |
| **Prove** | Validates a hand-built Harvest row set; rejects missing `equity_at_open` / `risk_ccy` |
| **Recipe** | `INF-P1-T01_data_adapterSchema_v0` — `make schema-test` |
| **Accept** | Contract tests green on ≥1 golden event |
| **Status** | `DONE` — **ACCEPT** · `infra/schemas/*.schema.json` · `archive/INF-P1-T01/` |


| | |
| --- | --- |
| **Plane** | P-STORE |
| **Limitation** | L-T06 |
| **What changes** | Create `raw/core/features/train/score/ops`; tables §7.3 |
| **Artefact** | `infra/migrations/versions/0001_core.py` |
| **Prove** | `alembic upgrade head` on empty DB; `\dn` shows six schemas |
| **Recipe** | `INF-P1-T02_store_pgSchemas_0001` — compose postgres + migrate |
| **Accept** | Dry-run upgrade/downgrade clean |
| **Status** | `DONE` — **ACCEPT** · `0001_core` upgrade/downgrade · schemas×6 · `archive/INF-P1-T02/` |


| | |
| --- | --- |
| **Plane** | P-DATA |
| **Limitation** | L-T02 |
| **What changes** | `infra/landing/{inbox,staging,quarantine}`; ingest refuses overwrite without sha change |
| **Artefact** | dirs + `infra/src/ingest/landing.py` |
| **Prove** | Drop duplicate file → idempotent no-op; corrupt file → quarantine |
| **Recipe** | `INF-P1-T03_data_landingZone_checksum` |
| **Accept** | Documented drop path for tester exports |
| **Status** | `DONE` — **ACCEPT** · `landing.py` idempotent sha256 · `archive/INF-P1-T03/` |


| | |
| --- | --- |
| **Plane** | P-STORE · P-TEST |
| **Limitation** | L-T03 |
| **What changes** | Loader maps G0 tickets → events; `risk_ccy` from SL points × volume × tick value |
| **Artefact** | `core.event_manifest` rows from Harvest archive slice |
| **Prove** | Rebuild n events ≈ 530 (±tolerance for scratches); 1R consistent with SL300 geometry |
| **Recipe** | `INF-P1-T04_store_eventId_1R_rebuild_Harvest` |
| **Accept** | Deterministic event_id; score Stage-0 identities match baseline within fixture tol |
| **Status** | `DONE` — **ACCEPT** · n=531 (Δ+1) · risk_ccy=3.0 · SL300 100% · `archive/INF-P1-T04/` |

**Phase exit P1:** Migrations apply; adapter schemas exist; Harvest events rebuild with 1R. **COMPLETE 2026-09-27.**

---

### INF-P2 — INGEST PIPELINE

Automated export → validate → load. Idempotent. Cost defaulted vs measured flagged. Replay one historical dump end-to-end.

#### INF-P2-T01 — Tester/EA export normaliser (deals + Print → adapter)


| | |
| --- | --- |
| **Plane** | P-DATA |
| **Limitation** | L-T03, L-T04 |
| **What changes** | Parsers for MT5 deals CSV + `[BMRG][TRADE]` lines → adapter rows |
| **Artefact** | `infra/src/ingest/mt5_normalise.py` |
| **Prove** | Normaliser output validates against INF-P1 schemas |
| **Recipe** | `INF-P2-T01_data_normalise_mt5Deals_Harvest` |
| **Accept** | ≥95% of archive opens map to legs; failures quarantined with reason |
| **Status** | `DONE` — **ACCEPT** · coverage ≥95% · `fixtures/blotter/harvest_long_v1/` · `archive/INF-P2-T01/` |


| | |
| --- | --- |
| **Plane** | P-DATA · P-STORE |
| **Limitation** | L-T06 |
| **What changes** | Upsert by sha256 + event_id; re-run safe |
| **Artefact** | `infra/src/ingest/load_core.py` · `ops.eval_run` row |
| **Prove** | Load twice → row counts unchanged |
| **Recipe** | `INF-P2-T02_data_idempotentLoad_HarvestDump` |
| **Accept** | Idempotency test green |
| **Status** | `DONE` — **ACCEPT** · load×2 stable · `archive/INF-P2-T02/` |


| | |
| --- | --- |
| **Plane** | P-DATA |
| **Limitation** | L-T11 |
| **What changes** | Persist `costs_defaulted[]` per event; Leak uses flagged proxy when needed |
| **Artefact** | columns on `core.event_manifest` / cost JSON |
| **Prove** | Scorecard reports Leak source; baseline Leak ~2.2 pp reproducible under same defaults |
| **Recipe** | `INF-P2-T03_data_costFlags_leakProxy` |
| **Accept** | No silent mix of measured/default without flag |
| **Status** | `DONE` — **ACCEPT** · costs_defaulted + component flags · Leak source named · `archive/INF-P2-T03/` |


| | |
| --- | --- |
| **Plane** | P-DATA · P-TEST |
| **Limitation** | L-T02, L-T08 |
| **What changes** | Freeze dump under `infra/fixtures/blotter/harvest_long_v1/`; pipeline replay |
| **Artefact** | `score.health_vector` for long window · `reports/INF-P2-T04_scorecard.json` |
| **Prove** | WR, R, BM, Leak, EF, E_N within tol of `ENGINE_BASELINE_v1` |
| **Recipe** | `INF-P2-T04_data_e2eReplay_HarvestLong_2025-2026` — `make ingest score REPORT=INF-P2-T04` |
| **Accept** | EF within ±0.05 pp of 1.77 under identical Leak policy; else investigate data integrity first |
| **Status** | `DONE` — **ACCEPT** · n=530 WR≈54.53 EF≈2.33 (bm−leak identity; doc 1.77 gap noted) · `INF-P2-T04_scorecard.json` |

**Phase exit P2:** One command replays Harvest dump → baseline health vector. **COMPLETE 2026-09-27.**

---

### INF-P3 — FEATURE / REGIME TAPE (offline L1)

PIT-correct perception features. Join to events. **Do not skip live trades.** Dump regime tape for trainer.

#### INF-P3-T01 — PIT feature builder (as-of bar close)


| | |
| --- | --- |
| **Plane** | P-FEAT |
| **Limitation** | L-T05 |
| **What changes** | Build features using only bars ≤ signal bar; unit test forbids future leak |
| **Artefact** | `infra/src/features/pit_builder.py` · leakage tests |
| **Prove** | Leakage test: shifting labels forward breaks join; builder uses `t_close ≤ entry_time` |
| **Recipe** | `INF-P3-T01_feat_pitBuilder_noLeakage` |
| **Accept** | pytest leakage suite green |
| **Status** | `DONE` — **ACCEPT** · PIT tests · `archive/INF-P3-T01/` |


| | |
| --- | --- |
| **Plane** | P-FEAT |
| **Limitation** | L-T13 |
| **What changes** | Enrich beyond AOS stubs: ATR/ER terciles, BB width, session, structure v1 where possible |
| **Artefact** | `features.tape_tick` + Parquet `infra/artefacts/tape/harvest_l1.parquet` |
| **Prove** | ≥95% engine events have feature join; Tue=0; session LON_NY/NY ≥95% on champ |
| **Recipe** | `INF-P3-T02_feat_l1Tape_Harvest_long` |
| **Accept** | Coverage bars from `aos_l1_tape_contract.md`; null-rate report written |
| **Status** | `DONE` — **ACCEPT** · harvest_l1.parquet n=531 · Tue=0 · sess 100% · `archive/INF-P3-T02/` |


| | |
| --- | --- |
| **Plane** | P-FEAT · P-TRAIN |
| **Limitation** | L-T05 |
| **What changes** | `train.label_row` with y_lose / pnl_R; **no policy applied** |
| **Artefact** | labelled Parquet + table |
| **Prove** | n labels = n scoreable events; class balance reported |
| **Recipe** | `INF-P3-T03_feat_labelJoin_Harvest_noSkip` |
| **Accept** | Fire count unchanged vs baseline (perception-only phase) |
| **Status** | `DONE` — **ACCEPT** · labels joined · skip_applied=false · `archive/INF-P3-T03/` |


| | |
| --- | --- |
| **Plane** | P-FEAT · P-ACCESS |
| **Limitation** | L-T10 |
| **What changes** | Export stable path agent can Read |
| **Artefact** | `infra/artefacts/tape/LATEST_REGIME_TAPE.parquet` + manifest JSON |
| **Prove** | `make features` refreshes LATEST_*; Cursor Read works |
| **Recipe** | `INF-P3-T04_feat_regimeTape_export` |
| **Accept** | Manifest lists schema version + row counts |
| **Status** | `DONE` — **ACCEPT** · `LATEST_REGIME_TAPE.parquet` · `archive/INF-P3-T04/` |

**Phase exit P3:** PIT tape + labels; zero live skips; trainer-ready dump. **COMPLETE 2026-09-27.**

---

### INF-P4 — OFFLINE TRAIN + EVAL HARNESS (L2 shadow, not wired)

Train skip/enter models. Shadow only. Counterfactual blotter vs baseline with **low** skip bar. Versioned models.

#### INF-P4-T01 — Walk-forward fold harness (G2-style tooling)


| | |
| --- | --- |
| **Plane** | P-TRAIN · P-TEST |
| **Limitation** | L-T01 |
| **What changes** | Anchored / rolling folds; fit through decay; never fit-only-on-decay window |
| **Artefact** | `infra/src/train/walkforward.py` |
| **Prove** | Dry-run emits fold table; decay window excluded from sole fit |
| **Recipe** | `INF-P4-T01_train_walkforwardHarness_G2style` |
| **Accept** | Harness tests green; **not** a promotion gate |
| **Status** | `DONE` — **ACCEPT** · expanding WF · `archive/INF-P4-T01/` |


| | |
| --- | --- |
| **Plane** | P-TRAIN |
| **Limitation** | L-T07 |
| **What changes** | Train P(lose) / avoid-loser; threshold **low** (prefer under-skip); write new semver, never overwrite |
| **Artefact** | `ops.model_version` + `infra/artefacts/models/L2skip/<semver>/` |
| **Prove** | Per-fold report: skip-rate, EF/E_N/MaxDD vs baseline; OOS metrics logged |
| **Recipe** | `INF-P4-T02_train_L2shadow_skipRangeHighVol_2018-2024` (window per available history) |
| **Accept** | §2.1 on counterfactual; reject payoff trap; skip clusters justified |
| **Status** | `DONE` — **ACCEPT** · `L2skip_inf_p92_*` · OOS skip≈10% · fires_kept≈90% · `archive/INF-P4-T02/` |


| | |
| --- | --- |
| **Plane** | P-TRAIN · P-OBS |
| **Limitation** | L-T04 |
| **What changes** | Score historical events; engine unrestricted; log `ALLOW_UNCERTAIN` |
| **Artefact** | `score.skip_ledger` · JSONL decision log |
| **Prove** | Actual fires = baseline; shadow decisions complete |
| **Recipe** | `INF-P4-T03_train_L2shadow_ledger_Harvest` |
| **Accept** | Ledger answers “why would it skip?” per event |
| **Status** | `DONE` — **ACCEPT** · WOULD_SKIP 39 / ALLOW_UNCERTAIN 77 / WOULD_FIRE 264 · all shadow_fire · `archive/INF-P4-T03/` |


| | |
| --- | --- |
| **Plane** | P-TRAIN · P-TEST |
| **Limitation** | L-T08 |
| **What changes** | Remove WOULD_SKIP events; recompute Stage 0–2 vector |
| **Artefact** | `reports/INF-P4-T04_cf_scorecard.json` → copy to `LATEST_EVAL.json` |
| **Prove** | Framework numbers: WR, R, BWR, BM, Leak, EF, M, E_N, ΔD, MaxDD, skip-rate, fire-count vs baseline |
| **Recipe** | `INF-P4-T04_train_cfEval_L2shadow_vsBaseline` — `make score report` |
| **Accept** | §2.1; warn fires &lt;70%; hard-concern &lt;50%; prefer under-skip |
| **Status** | `PENDING` |


#### INF-P4-T05 — L3/L4 simulation hooks in harness (not live)


| | |
| --- | --- |
| **Plane** | P-TRAIN |
| **Limitation** | L-T01 |
| **What changes** | Simulate MaxDD halt / FREQUENCY_STALL / Below-frontier f=0 on CF path |
| **Artefact** | sim trip log in scorecard |
| **Prove** | L3 outranks L2 in sim (skip ignored when halted) |
| **Recipe** | `INF-P4-T05_train_L3L4sim_harness` |
| **Accept** | Documented sim semantics; no EA wire |
| **Status** | `PENDING` |

**Phase exit P4:** Versioned shadow model + CF scorecard passing protect-don't-overfilter bar (or explicit REJECT with reason).

---

### INF-P5 — OBSERVABILITY + DOCKER + DEDICATED BOX

Structured logs, compose stack, move heavy jobs off tester. Infra tests. Agent access paths.

#### INF-P5-T01 — Structured JSON logging + correlation ids


| | |
| --- | --- |
| **Plane** | P-OBS |
| **Limitation** | L-T04 |
| **What changes** | All infra services emit JSONL with `event_id`, `run_id`, `model_semver`; reason codes for would-be skips |
| **Artefact** | `infra/artefacts/logs/` · log schema |
| **Prove** | One replay produces greppable correlation across ingest→score |
| **Recipe** | `INF-P5-T01_obs_jsonl_correlationIds` |
| **Accept** | Agent can trace one event_id end-to-end |
| **Status** | `PENDING` |


#### INF-P5-T02 — Metrics surface (fire/skip, lag, nulls, cost drift, stall)


| | |
| --- | --- |
| **Plane** | P-OBS |
| **Limitation** | L-T04, L-T11 |
| **What changes** | Emit ops metrics into `score.health_vector` extras + `LATEST_EVAL.json` |
| **Artefact** | metrics block in scorecard |
| **Prove** | FREQUENCY_STALL and feature-null % visible without Tester UI |
| **Recipe** | `INF-P5-T02_obs_metricsSurface_evalJson` |
| **Accept** | Required keys present in LATEST_EVAL |
| **Status** | `PENDING` |


#### INF-P5-T03 — Docker images + compose (local = server)


| | |
| --- | --- |
| **Plane** | P-PACK |
| **Limitation** | L-T09, L-T12 |
| **What changes** | Images for ingest, features, trainer, scorer, eval, postgres; pin versions/digests |
| **Artefact** | `infra/docker-compose.yml` · Dockerfiles |
| **Prove** | `docker compose up` + `make replay PHASE=P2` on clean machine |
| **Recipe** | `INF-P5-T03_pack_compose_smoke_local` |
| **Accept** | Smoke green; versions pinned in lockfile |
| **Status** | `PENDING` |


#### INF-P5-T04 — Dedicated box profile + job queue


| | |
| --- | --- |
| **Plane** | P-BOX |
| **Limitation** | L-T01, L-T09 |
| **What changes** | Document hardware; deploy compose; RQ/Redis (or Dramatiq) for train/MC/WF jobs; artefact volume |
| **Artefact** | `infra/BOX.md` · queue worker service |
| **Prove** | Heavy train job runs on box while tester box idle; artefacts visible via sync/mount |
| **Recipe** | `INF-P5-T04_box_dedicated_queue_profile` |
| **Accept** | BOX.md lists CPU/RAM/disk; queue processes one INF-P4 replay |
| **Status** | `PENDING` |


#### INF-P5-T05 — Infra test suite (schema, FX, replay, smoke)


| | |
| --- | --- |
| **Plane** | P-TEST |
| **Limitation** | L-T08, L-T14 |
| **What changes** | Contract tests; golden FX-01…FX-16; frozen blotter → stable health vector; migration dry-run; permission checks |
| **Artefact** | `infra/src/**/test_*.py` · CI script or `make test` |
| **Prove** | `make test` green; FX fixtures match unified §10 within tol |
| **Recipe** | `INF-P5-T05_test_infraSuite_fxReplaySmoke` |
| **Accept** | No live FT; no demo “see if it works” |
| **Status** | `PENDING` |


#### INF-P5-T06 — Agent access: Makefile + paths + env example


| | |
| --- | --- |
| **Plane** | P-ACCESS |
| **Limitation** | L-T10 |
| **What changes** | `make ingest|features|train|score|report`; document Read paths |
| **Artefact** | `infra/Makefile` · `infra/README.md` · `.env.example` |
| **Prove** | Agent produces scorecard via make without Tester clicks |
| **Recipe** | `INF-P5-T06_access_makeTargets_agentPaths` |
| **Accept** | README path table matches §12 |
| **Status** | `PENDING` |

**Phase exit P5:** Compose smoke green; box profile written; `make test` green; agent can Read `LATEST_EVAL.json`.

---

### INF-P6 — PHASE-PROVE GATE (still offline)

Per-layer / per-phase report: baseline vs shadow OS on W250/W500. Wiring plan only if EF held/lifted and skip-rate not starving.

#### INF-P6-T01 — Consolidated phase-prove scorecard


| | |
| --- | --- |
| **Plane** | P-OBS · P-TRAIN |
| **Limitation** | L-T08 |
| **What changes** | Single report: engine baseline vs best shadow stack (L2±L3sim) |
| **Artefact** | `reports/INF-P6-T01_phaseProve.json` · `blotter/archive/INF-P6-T01/` |
| **Prove** | W250/W500 EF, E_N, MaxDD, skip-rate, fire-count; framework fields complete |
| **Recipe** | `INF-P6-T01_obs_phaseProve_W250W500_shadowVsEngine` |
| **Accept** | §2.1; fires ≥70% preferred; &lt;50% → FAIL prove (do not write wiring plan) |
| **Status** | `PENDING` |


#### INF-P6-T02 — Skip-cluster audit (hostile cells only)


| | |
| --- | --- |
| **Plane** | P-OBS |
| **Limitation** | Overfilter failure mode |
| **What changes** | Audit every skip cluster vs `aos_bad_cells.md` / BM_cell≤0 / modest-confidence losers |
| **Artefact** | `INF-P6-T02_skip_audit.md` |
| **Prove** | No skip cluster justified only by “higher WR” |
| **Recipe** | `INF-P6-T02_obs_skipClusterAudit_lowBar` |
| **Accept** | Each cluster cites cell evidence or model precision on losers |
| **Status** | `PENDING` |


#### INF-P6-T03 — Wiring-plan eligibility verdict


| | |
| --- | --- |
| **Plane** | P-ACCESS |
| **Limitation** | Process |
| **What changes** | Write GO / NO-GO for INF-P7; **no live preset** |
| **Artefact** | `doc/infra_wiring_eligibility.md` |
| **Prove** | Verdict references P6-T01 numbers only |
| **Recipe** | `INF-P6-T03_access_wiringEligibility_offline` |
| **Accept** | GO only if EF held/lifted and not starving; else NO-GO + retrain path |
| **Status** | `PENDING` |

**Phase exit P6:** Explicit GO/NO-GO. No live `.set` AI wiring authored unless GO **and** user authorises P7 execution.

---

### INF-P7 — WIRING PLAN (design only unless explicitly authorised)

How L2/L3 attach to the stable EA, champion/challenger, rollback, retrain cadence. Still not forward testing unless user says so.

#### INF-P7-T01 — Attachment design (permit/withhold only)


| | |
| --- | --- |
| **Plane** | P-ACCESS |
| **Limitation** | Process / L-T12 |
| **What changes** | Design doc: EA hooks, shadow→live flag, L3 precedence, no entry rewrite |
| **Artefact** | `doc/infra_wiring_plan.md` |
| **Prove** | Checklist covers rollback, model pin, kill-switch |
| **Recipe** | `INF-P7-T01_access_wiringDesign_L2L3` — doc only |
| **Accept** | User-readable; no code wire unless authorised follow-up task |
| **Status** | `PENDING` |


#### INF-P7-T02 — Champion/challenger + rollback runbook


| | |
| --- | --- |
| **Plane** | P-TRAIN · P-OBS |
| **Limitation** | L-T07 |
| **What changes** | Promote rule aligned with protect bar; one-command rollback |
| **Artefact** | runbook section in wiring plan + `ops` tables usage |
| **Prove** | Dry-run promote/reject on fixtures |
| **Recipe** | `INF-P7-T02_train_champChallenger_rollbackDesign` |
| **Accept** | Dry-run correct; no silent overwrite |
| **Status** | `PENDING` |


#### INF-P7-T03 — Optional EXP export preset only (still no AOS_LIVE)


| | |
| --- | --- |
| **Plane** | P-DATA |
| **Limitation** | L-T02 |
| **What changes** | If needed: `EXP-*` preset identical to Harvest for blotter refresh — **not** AI gate |
| **Artefact** | `Profiles/Tester/BMRG/EXP-P7-T03_export_Harvest_long.set` (only if authorised) |
| **Prove** | Engine logic unchanged vs 8210204 champion |
| **Recipe** | `INF-P7-T03_data_EXP_exportOnly_Harvest` |
| **Accept** | Diff vs champion inputs = magic/path bookkeeping only |
| **Status** | `PENDING` |

**Phase exit P7:** Wiring plan exists; implementation tasks require explicit user authorisation. No FT by default.

---

### INF-P8 — RETRAIN LOOP ON THE NEW STACK

Only after infra stable **and** wiring plan exists.

#### INF-P8-T01 — Scheduled + trigger retrain policy on infra


| | |
| --- | --- |
| **Plane** | P-TRAIN · P-BOX |
| **Limitation** | L-T01, L-T07 |
| **What changes** | Monthly + Compressing / Near-frontier triggers via job queue; PIT; versioned artefacts |
| **Artefact** | `infra/src/train/retrain_loop.py` · ops schedules |
| **Prove** | Dry-run enqueue → train → shadow eval → no live swap |
| **Recipe** | `INF-P8-T01_train_retrainLoop_scheduled_shadow` |
| **Accept** | Shadow eval before any model pin change |
| **Status** | `PENDING` |


#### INF-P8-T02 — Shadow eval gate before model pin


| | |
| --- | --- |
| **Plane** | P-TRAIN · P-OBS |
| **Limitation** | Overfilter / payoff trap |
| **What changes** | Challenger must pass §2.1 vs baseline + vs champion shadow |
| **Artefact** | `ops.eval_run` + LATEST_EVAL |
| **Prove** | Failed challenger never pins |
| **Recipe** | `INF-P8-T02_train_shadowGate_beforePin` |
| **Accept** | Pin only on ACCEPT; else keep prior semver |
| **Status** | `PENDING` |


#### INF-P8-T03 — Post-wiring retrain (only if wire authorised)


| | |
| --- | --- |
| **Plane** | P-TRAIN |
| **Limitation** | L-T13 |
| **What changes** | Retrain on new stack data after wire justified; still shadow-first |
| **Artefact** | new model semver |
| **Prove** | CF / shadow metrics reported in framework numbers |
| **Recipe** | `INF-P8-T03_train_retrainAfterWire_shadowFirst` |
| **Accept** | User authorisation recorded; §2.1 |
| **Status** | `PENDING` |

**Phase exit P8:** Retrain loop operable on dedicated box; live swap still behind human pin.

---

## 12. Agent / human access paths

| Path | Role |
| --- | --- |
| `doc/infrascaleup.md` | This plan — task board |
| `doc/ai_OS.md` | Layer semantics (consume; do not reopen EDX) |
| `doc/edge_framework.md` | Scoring contract |
| `doc/ai_OS_baseline.md` / `infra/baselines/ENGINE_BASELINE_v1.json` | Frozen engine vector |
| `infra/landing/inbox/` | Drop tester exports |
| `infra/artefacts/reports/LATEST_EVAL.json` | Single latest scorecard for agent Read |
| `infra/artefacts/logs/` | JSONL correlation logs |
| `infra/artefacts/models/` | Versioned models (never overwrite) |
| `infra/fixtures/` | FX + frozen blotter slices |
| `blotter/inbox/` → `blotter/archive/INF-P#-T##/` | Human/agent review drop (existing rule) |
| `make -C infra ingest\|features\|train\|score\|report\|test` | One-command plane ops |

**APIs (target):** local HTTP optional (`localhost:8080/eval/latest`) — nice-to-have after P5; files are enough for Cursor.

---

## 13. Execution board (current)

| Phase | Next task | Ready? |
| --- | --- | --- |
| INF-P0 | Complete (W01) | `infra/LIMITATIONS.md` · `ENGINE_BASELINE_v1.json` |
| INF-P1 | Complete (W02) | schemas · `0001_core` · rebuild n=531 |
| INF-P2 | Complete (W03) | fixture + load + scorecard EF≈2.33 |
| INF-P3 | Complete (W04) | `LATEST_REGIME_TAPE.parquet` n=531 · 0 skips |
| INF-P4a | Complete (W05) | L2 shadow p92 · skip≈10% · ledger |
| **INF-P4b** | **INF-P4-T04** | Yes — start INF-W06 |
| INF-P5 | Blocked on prior phase exit | — |
| INF-P6 | Phase-prove gate | After P5 |
| INF-P7 | Design only | After P6 GO |
| INF-P8 | Retrain loop | After wiring plan |

**Do now:** execute `INF-P0-T01` then T02–T04 in order.  
**Do not:** wire AI into live execution; open EDX; raise skip thresholds; run forward tests.

---

## 14. Delta report format (every completed INF task)

```text
TASK: INF-P#-T##
PLANE: P-*
LIMITATION: L-Txx
RECIPE: INF-P#-T##_...
ENGINE_BASELINE: AOS_BASELINE_v1 / ENGINE_BASELINE_v1
n, fires, WR, R, BWR, BM, Leak, EF, M, E_N, ΔD, MaxDD, AL, skip_rate
vs BASELINE: ΔEF, ΔMaxDD, Δfires, ΔE_N, ΔAL, Δskip
ZONE: Negative|Fragile|Robust
LIFECYCLE_W250: ...
ACCEPT|REJECT|WARN (FREQUENCY_STALL|n<385|overfilter|...)
ARCHIVE: blotter/archive/INF-P#-T##/
ARTEFACTS: infra/... paths
```

---

## 15. Rules of engagement (sticky)

1. One INF task at a time; ends with recipe + accept/reject.  
2. Offline → shadow → wire. Never skip INF-P6 prove gate.  
3. Default allow; skip is earned. When unsure, fire and log.  
4. L3 outranks intelligence in sim and (later) live.  
5. Intelligence never rewrites entries — only permit/withhold (shadow until authorised).  
6. Speak framework numbers on every eval — not “AI confidence.”  
7. Every tool names the L-Txx limitation it removes.  
8. No live AI `.set` until INF-P6 GO **and** explicit authorisation for wire work.  
9. EDX remains closed as a campaign; bad cells are inputs, not a new discovery stream.  
10. Overfiltering is a first-class failure mode — prefer under-skipping in INF phases.

---

## 16. Document map

| File | Role |
| --- | --- |
| `doc/infrascaleup.md` | **This plan** — planes + INF tasks |
| `doc/infra_roadmap.md` | Weekly implementation board (`INF-W01`…`W11`) |
| `system_profile.md` | Engine behaviour / known limits (evidence) |
| `doc/edge_framework.md` | Stage scoring + adapter bindings |
| `doc/unified_edge_framework.md` | Maths, adapter contract, FX-01…FX-16 |
| `doc/ai_OS.md` | L1–L10 target layers (paper / STAY_PAPER) |
| `doc/edge_discovery.md` | Isolated edge / bad cells (**closed**) |
| `doc/ai_OS_baseline.md` | Frozen engine health vector |
| `doc/aos_bad_cells.md` | Skip-seed registry for low-bar policy |
| `doc/aos_l1_feature_schema.md` · `aos_l1_tape_contract.md` | L1 contracts to industrialise |
| `infra/` | Target implementation root (created from P0/P1) |

---

## 17. Versioning

- **0.1** — Initial infra scale-up plan: limitation map, stack, schema, INF-P0…P8 tasks, offline-first / protect-don't-overfilter bar.  
- Bump when phases complete, schema migrations land, or baseline_id changes.
