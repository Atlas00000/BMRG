# INF-W02 — Contract + schema (INF-P1) REVIEW

**Week:** INF-W02  
**Completed:** 2026-09-27  
**Verdict:** ACCEPT — all P1 tasks DONE  

| Task | Artefact | Prove | Verdict |
| --- | --- | --- | --- |
| INF-P1-T01 | `infra/schemas/adapter_*.schema.json` | Golden + reject missing equity/risk; pytest | ACCEPT |
| INF-P1-T02 | `migrations/versions/0001_core.py` | upgrade/downgrade/upgrade; schemas raw/core/features/train/score/ops | ACCEPT |
| INF-P1-T03 | `infra/src/ingest/landing.py` | staged then idempotent_skip on same sha256 | ACCEPT |
| INF-P1-T04 | `artefacts/rebuild/harvest_p1/` | n=531 (Δ+1 vs 530); SL300 100%; risk_ccy=3.0; deterministic event_id | ACCEPT |

## Rebuild summary

- n_opens / manifest / blotter: **531**
- baseline_n: 530 · n_delta: **+1** (within ±5)
- sl_points_match_pct: **100%**
- risk_ccy: **3.0** (= 300 × 0.01 × 1.0)
- event_id sample: `8210204-EURUSD-BUY-20250102153000-2`
- joined_exits from train matrix: 530

## Tests

`pytest infra/src/ingest/test_p1_contract.py` → **5 passed**

## Ops notes

- Postgres: `docker-compose up -d postgres` (Compose v5; not `docker compose` on this host)
- URL: `postgresql+psycopg2://bmrg:bmrg@localhost:54329/bmrg`

## Next

**INF-W03** → `INF-P2-T01` (MT5 normaliser → adapter).
