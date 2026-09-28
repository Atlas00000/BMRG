# BMRG Infra — Limitation Map (locked)

**Task:** `INF-P0-T01`  
**Recipe:** `INF-P0-T01_access_limitationMap_lock`  
**Locked:** 2026-09-27  
**Normative source:** `doc/infrascaleup.md` §3  
**Status:** LOCKED — bump only via new INF-P0 task  

Every INF tool / task must name the `L-Txx` it removes. No silent TBD on L-T01…L-T14.

---

## 1. Limitation inventory

| ID | Limitation | Hurts | Compensating plane(s) | Owner path (stub → implement) | First INF task |
| --- | --- | --- | --- | --- | --- |
| L-T01 | Tester single-threaded; no native MC / walk-forward / parallel folds | Cannot prove G2/G4-style harness on trading box | P-BOX · P-TRAIN | `infra/BOX.md` · `infra/src/train/` | `INF-P4-T01` · `INF-P5-T04` |
| L-T02 | Tester history / export UX fragile; long windows manual | Incomplete blotters; re-run risk | P-DATA · P-OBS | `infra/landing/` · `infra/src/ingest/` | `INF-P1-T03` · `INF-P2-T04` |
| L-T03 | No first-class blotter; deals CSV ≠ adapter contract | Missing `event_id`, legs, `equity_at_open`, declared 1R | P-DATA · P-STORE | `infra/schemas/` · `infra/src/ingest/` | `INF-P1-T01` · `INF-P1-T04` |
| L-T04 | Fragmented logs (`Print` + Common/Files) | Agent scrape; no correlation ids | P-OBS · P-ACCESS | `infra/artefacts/logs/` · `infra/src/access/` | `INF-P5-T01` · `INF-P5-T06` |
| L-T05 | No point-in-time feature store | Leakage when joining bars → labels | P-FEAT | `infra/src/features/` | `INF-P3-T01` |
| L-T06 | No Postgres SoR; archives are folders | Non-idempotent reloads; hard joins | P-STORE | `infra/migrations/` | `INF-P1-T02` · `INF-P0-T04` |
| L-T07 | Thin model registry (`models/L2skip/`) | No eval-run lineage | P-TRAIN · P-STORE | `infra/artefacts/models/` | `INF-P4-T02` · `INF-P5-T02` |
| L-T08 | Ad-hoc scoring / human scorecards | No golden FX CI | P-TEST · P-TRAIN | `infra/fixtures/fx/` · `infra/src/score/` | `INF-P0-T02` · `INF-P5-T05` |
| L-T09 | Heavy jobs compete with tester | Trading-box thrash | P-BOX · P-PACK | `infra/docker-compose.yml` · `infra/BOX.md` | `INF-P5-T03` · `INF-P5-T04` |
| L-T10 | Agent access = Tester UI / hunt Files | No `make report` | P-ACCESS | `infra/Makefile` · `infra/README.md` | `INF-P0-T03` · `INF-P5-T06` |
| L-T11 | Costs often defaulted (3× spread proxy) | Leak uncertainty in EF | P-DATA | `infra/src/ingest/` (cost flags) | `INF-P2-T03` |
| L-T12 | AOS offline not industrialised (no Docker / migrations / queue) | Replay drift across machines | P-PACK · P-OBS | `infra/` root | `INF-P0-T01` · `INF-P5-T03` |
| L-T13 | Live tape deferred; `structure_id` often `UNK` | Thin L1 → weak OOS AUC | P-FEAT | `infra/src/features/` · `artefacts/tape/` | `INF-P3-T02` |
| L-T14 | No contract tests on adapter blotter | Silent schema breaks | P-TEST | `infra/schemas/` · tests | `INF-P1-T01` · `INF-P5-T05` |

---

## 2. Plane ownership

| Plane | Owns | Stub / root path |
| --- | --- | --- |
| P-DATA | Landing, normalise, cost flags, EXP export ingest | `infra/landing/` · `infra/src/ingest/` |
| P-STORE | Postgres schemas, migrations, core tables | `infra/migrations/` · `infra/schemas/` |
| P-FEAT | PIT builder, L1 tape, labels | `infra/src/features/` · `infra/artefacts/tape/` |
| P-TRAIN | WF harness, models, CF eval, retrain | `infra/src/train/` · `infra/src/eval/` · `infra/artefacts/models/` |
| P-OBS | Baseline JSON, JSONL logs, LATEST_EVAL, prove reports | `infra/baselines/` · `infra/artefacts/logs/` · `infra/artefacts/reports/` |
| P-PACK | Docker images + compose | `infra/images/` · `infra/docker-compose.yml` |
| P-BOX | Dedicated server profile + job queue | `infra/BOX.md` (W08) |
| P-TEST | FX fixtures, contract/replay/smoke | `infra/fixtures/` · `infra/src/**/test_*.py` |
| P-ACCESS | Makefile, README, env example, agent paths | `infra/Makefile` · `infra/README.md` · `.env.example` |

---

## 3. Tester vs dedicated box

**Tester / trading box keeps:** Strategy Tester, EA compile/attach, raw deal/log export into `infra/landing/inbox/`.

**Dedicated box must:** parallel WF/MC, Postgres + migrations, feature materialisation, Docker train/score/eval, deterministic blotter replay, agent-readable scorecards.

---

## 4. Accept

- [x] L-T01…L-T14 named with no TBD  
- [x] Each L-Txx has ≥1 future INF task  
- [x] Each plane has owner path under `infra/`  

**Verdict:** ACCEPT · `INF-P0-T01`
