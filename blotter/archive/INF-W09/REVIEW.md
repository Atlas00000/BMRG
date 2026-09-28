# INF-W09 — Phase-prove gate (INF-P6) REVIEW

**Week:** INF-W09  
**Completed:** 2026-09-28  
**Week verdict:** ACCEPT (gate completed)  
**Wiring eligibility:** **NO-GO**

| Task | Artefact | Prove | Verdict |
| --- | --- | --- | --- |
| INF-P6-T01 | `INF-P6-T01_phaseProve.json` | W250/W500/long engine vs CF | metrics ACCEPT · prove REJECT |
| INF-P6-T02 | `INF-P6-T02_skip_audit.md` | Cluster justify hostile/modest-conf | FAIL — 3 edge FPs |
| INF-P6-T03 | `doc/infra_wiring_eligibility.md` | GO/NO-GO | **NO-GO** |

## Metrics (hold)

| | Engine | Shadow CF | Δ |
| --- | ---: | ---: | ---: |
| EF_pp | 2.33 | 2.99 | +0.67 |
| fires_kept | — | 92.6% | — |
| MaxDD_pp | 21.0 | 16.8 | −4.1 |

## Skip audit fail (blocks GO)

- `LON_NY|Thu|SELL` n=4 prec=0.25 BM=+6.4
- `LON_NY|Mon|BUY` n=1 prec=0.0 BM=+6.5
- `NY|Mon|BUY` n=1 prec=0.0 BM=+25.0

## Next

**Retrain INF-W05** (raise thr / protect-cell allow) → **INF-W06** CF → re-run **INF-W09**.  
Do **not** start INF-W10 until GO. Live preset still FORBIDDEN.
