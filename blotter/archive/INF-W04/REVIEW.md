# INF-W04 — Offline L1 tape (INF-P3) REVIEW

**Week:** INF-W04  
**Completed:** 2026-09-27  
**Verdict:** ACCEPT  

| Task | Artefact | Prove | Verdict |
| --- | --- | --- | --- |
| INF-P3-T01 | `infra/src/features/pit_builder.py` | PIT join rejects future; leakage probe; pytest | ACCEPT |
| INF-P3-T02 | `artefacts/tape/harvest_l1.parquet` | n=531; Tue=0; LON_NY∪NY=100%; AOS enrich 531/531 | ACCEPT |
| INF-P3-T03 | `harvest_labels.parquet` · `harvest_event_features.parquet` | labels joined; `skip_applied=false` for all | ACCEPT |
| INF-P3-T04 | `LATEST_REGIME_TAPE.parquet` + manifest JSON | Agent-readable path; schema aos_l1_v0 | ACCEPT |

## Accept bars

- coverage: **1.0** (≥0.95)
- tue_count: **0**
- session LON_NY|NY share: **1.0**
- skips_applied: **0** (fire count unchanged)

## Tests

`pytest src/features/test_p3_features.py` → **5 passed**

## Next

**INF-W05** → `INF-P4-T01` (walk-forward harness).
