# BMRG INF dedicated box profile (INF-P5-T04)

**Recipe:** `INF-P5-T04_box_dedicated_queue_profile`  
**Rule:** Heavy train / WF / CF / MC jobs run on the INF box. MT5 Strategy Tester stays idle during those jobs.

## Target (production box)

| Resource | Min viable | Preferred |
| --- | ---: | ---: |
| vCPU | 8 | **16+** |
| RAM | 32 GB | **64 GB** |
| Disk | 500 GB SSD | **2 TB NVMe** |
| OS | Linux or Win Server | Linux preferred for workers |
| Docker | compose + postgres + redis + job images | required |
| Artefacts | shared volume / sync to agent-readable path | `infra/artefacts/` |

## This host (dev / interim)

| Resource | Value | Notes |
| --- | --- | --- |
| Hostname role | INF interim box (not tester-dedicated) | Cursor agent host |
| Logical CPUs | 12 | Below preferred 16; OK for shadow train |
| RAM | ~24 GB | Below min-viable 32 GB — keep one heavy job at a time |
| Disk C: | ~188 GB free / ~953 GB | artefacts + docker layers |
| Disk D: | ~39 GB free / ~930 GB | overflow / archives |
| Postgres | `localhost:54329` via compose | pin in `IMAGE_LOCK.json` |
| Redis | `localhost:6379` via compose | job queue |
| Tester | **Must stay idle** while `make train` / queue jobs run | no live FT |

Gap vs preferred: RAM and vCPU. Do not schedule concurrent train+eval+features on this host.

## Job queue

| Item | Value |
| --- | --- |
| Broker | Redis 7 (compose service `redis`) |
| Worker | `bmrg-worker:inf-w08` · `src/jobqueue/worker.py` |
| Queue key | `bmrg:jobs` (Redis list) |
| Results | `artefacts/queue/<job_id>.json` + `artefacts/queue/LATEST_JOB.json` |
| Allowed jobs | `p4_eval` (INF-P4 CF replay), `p2_ingest`, `p5a_obs`, `features_tape` |
| Concurrency | **1** heavy job (protect 24 GB host) |

### Commands

```bat
cd infra
docker-compose up -d postgres redis
python src/jobqueue/enqueue.py --job p4_eval
python src/jobqueue/worker.py --once
```

Or: `make queue-demo` (enqueue + one-shot worker).

**Accept prove:** worker completes `p4_eval` while Strategy Tester is not required; scorecard lands under `artefacts/`.

## Separation from tester

| Machine role | Runs |
| --- | --- |
| Tester box | MT5 Strategy Tester exports only → drop to `landing/inbox/` |
| INF box | ingest · features · train · score · eval · queue worker |
| Agent (Cursor) | `make report` / Read `LATEST_EVAL.json` — no Tester UI |

Live forward-test wiring remains **forbidden** until INF-P6 GO + INF-P7 design.
