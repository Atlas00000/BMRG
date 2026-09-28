# BMRG `infra/` — offline scale-up root

**Roadmap:** `doc/infra_roadmap.md`  
**Contracts:** `doc/infrascaleup.md`  
**Locks:** `LIMITATIONS.md` · `baselines/ENGINE_BASELINE_v1.json` · `PHASE_EXITS.md` · `BOX.md` · `IMAGE_LOCK.json`  
**Agent Read table:** `AGENT_PATHS.md` (no Tester UI)

## Agent paths (summary)

| Path | Role |
| --- | --- |
| `artefacts/reports/LATEST_EVAL.json` | Newest scorecard — primary agent Read |
| `BOX.md` | Dedicated box CPU/RAM/disk + Redis queue |
| `AGENT_PATHS.md` | Full make targets + Read paths |
| `baselines/ENGINE_BASELINE_v1.json` | Engine health vector for all INF evals |
| `fixtures/fx/FX_GOLDEN.json` | FX-01…16 golden vectors |
| `landing/inbox/` | Drop tester exports (tester idle during box jobs) |

## Commands (W08)

```bat
cd infra
docker-compose up -d postgres redis
set BMRG_DATABASE_URL=postgresql+psycopg2://bmrg:bmrg@localhost:54329/bmrg
set BMRG_REDIS_URL=redis://localhost:6379/0
make.bat ingest
make.bat features
make.bat train
make.bat score
make.bat eval
make.bat report
make.bat queue-demo
make.bat test
```

GNU make equivalents: `make ingest|features|train|score|eval|report|test|queue-demo`

**Live FT forbidden.** Heavy jobs: Redis queue (`src/jobqueue/`) or `worker.py --local p4_eval`.

Latest scorecard: `infra/artefacts/reports/LATEST_EVAL.json`  
Queue result: `infra/artefacts/queue/LATEST_JOB.json`  
Correlation logs: `infra/artefacts/logs/LATEST_CORRELATION.jsonl`
