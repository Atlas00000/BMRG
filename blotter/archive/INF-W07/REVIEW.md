# INF-W07 — Observability + Docker (INF-P5a) REVIEW

**Week:** INF-W07  
**Completed:** 2026-09-27  
**Verdict:** ACCEPT  

| Task | Artefact | Prove | Verdict |
| --- | --- | --- | --- |
| INF-P5-T01 | `artefacts/logs/*.jsonl` · `jsonl_log.py` | event_id traced ingest→eval | ACCEPT |
| INF-P5-T02 | `metrics` in `LATEST_EVAL.json` | fire/skip, nulls, stall, cost drift keys | ACCEPT |
| INF-P5-T03 | `docker-compose.yml` · `images/*` · `IMAGE_LOCK.json` | 5 service tags built; scorer smoke ACCEPT | ACCEPT |

## Correlation

- event_id: `8210204-EURUSD-BUY-20250102153000-2`
- stages: ingest.normalise → ingest.load → features.tape → scorer.health → eval.cf

## Metrics (surface)

| Key | Value |
| --- | ---: |
| fires_kept_pct | 89.74 |
| feature_null_pct | 12.25 |
| FREQUENCY_STALL | false |
| cost_drift_ratio | 1.0 |

## Compose

Images: `bmrg-{ingest,features,trainer,scorer,eval}:inf-w07`  
Scorer container: `{"verdict":"ACCEPT","ef":2.3283}`

## Tests

`pytest src/obs/test_p5a_obs.py` → **3 passed**

## Next

**INF-W08** → `INF-P5-T04` (dedicated box + infra tests + agent access).
