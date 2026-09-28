# Agent access paths (INF-P5-T06)

Cursor / agent reads these files — **no Strategy Tester UI**.

## Primary scorecard

| Path | Role |
| --- | --- |
| `infra/artefacts/reports/LATEST_EVAL.json` | Newest eval / obs scorecard |
| `infra/artefacts/reports/INF-P5a_scorecard.json` | P5a obs + metrics |
| `infra/artefacts/reports/INF-P4-T04_cf_scorecard.json` | CF prove (P4b) |
| `infra/artefacts/queue/LATEST_JOB.json` | Last box queue job result |

## Correlation / ops

| Path | Role |
| --- | --- |
| `infra/artefacts/logs/LATEST_CORRELATION.jsonl` | event_id ingest→eval trace |
| `infra/artefacts/reports/skip_ledger/LATEST_SKIP_LEDGER.csv` | Shadow WOULD_SKIP ledger |
| `infra/artefacts/tape/LATEST_REGIME_TAPE.parquet` | Trainer-facing L1 tape |

## Contracts / locks

| Path | Role |
| --- | --- |
| `infra/baselines/ENGINE_BASELINE_v1.json` | Frozen Harvest health vector |
| `infra/BOX.md` | Dedicated box + queue profile |
| `infra/IMAGE_LOCK.json` | Docker image pins |
| `infra/PHASE_EXITS.md` | Week exit criteria |
| `infra/fixtures/fx/FX_GOLDEN.json` | FX-01…16 expected values |

## Make targets (from `infra/`)

```text
make up              # postgres + redis
make ingest          # P2 e2e normalise/load/score
make features        # L1 tape
make train           # L2 shadow (versioned; never overwrite)
make score           # harvest fixture health vector
make eval            # P4b CF + L3/L4 sim
make report          # print LATEST_EVAL.json head
make test            # full INF pytest suite (no live FT)
make queue-demo      # enqueue p4_eval + worker --once
```

Windows without GNU make: `make.bat <target>` or the Python lines in `README.md`.
