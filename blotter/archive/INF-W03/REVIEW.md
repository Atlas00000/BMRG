# INF-W03 — Ingest (INF-P2) REVIEW

**Week:** INF-W03  
**Completed:** 2026-09-27  
**Verdict:** ACCEPT  

| Task | Artefact | Prove | Verdict |
| --- | --- | --- | --- |
| INF-P2-T01 | `infra/src/ingest/mt5_normalise.py` · `fixtures/blotter/harvest_long_v1/` | open_coverage ≥95% (530/531 joined); schema validate | ACCEPT |
| INF-P2-T02 | `infra/src/ingest/load_core.py` | load×2 → n_events stable; 2nd `landed_new=false` | ACCEPT |
| INF-P2-T03 | cost flags on manifest/legs | `costs_defaulted` + `cost_component_flags`; Leak source named | ACCEPT |
| INF-P2-T04 | `artefacts/reports/INF-P2-T04_scorecard.json` | n=530 WR≈54.53 R=1.0 BM≈4.53 Leak=2.2 EF≈**2.33** (identity) | ACCEPT |

## Health vector (baseline_proxy Leak)

| Metric | Replay | ENGINE_BASELINE_v1 |
| --- | ---: | ---: |
| n | 530 | 530 |
| WR % | 54.5283 | 54.5 |
| R | 1.0 | 1.0 |
| BM pp | 4.5283 | 4.5 |
| Leak pp | 2.2 | 2.2 |
| EF pp | **2.3283** | 1.77 |
| E_N | 0.0906 | 0.091 |
| Zone | Fragile | Fragile |

**Note:** Locked baseline `ef_pp=1.77` is arithmetically inconsistent with bm−leak (≈4.5−2.2=**2.3**). Replay holds framework identity under the same Leak proxy; ΔEF vs doc 1.77 ≈ +0.56 pp is a documentation gap, not a data-integrity fail.

## Tests

`pytest src/ingest/test_p2_ingest.py` → **3 passed**

## Next

**INF-W04** → `INF-P3-T01` (PIT feature builder).
