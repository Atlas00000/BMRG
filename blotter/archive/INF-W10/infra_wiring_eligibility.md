# INF wiring eligibility (INF-P6-T03) — amended

**Recipe:** `INF-P6-T03_access_wiringEligibility_offline`  
**Automated gate (2026-09-28):** **NO-GO** (skip-audit edge overfilter)  
**User amendment (2026-09-28):** **GO — USER AUTHORISED**

Offline CF metrics accepted by operator for wiring design + retrain loop:
EF +0.67pp · fires kept 92.6% · MaxDD −4.1pp. Residual risk: L2 may still skip some winners in LON_NY/NY; monitor via skip audit on every retrain.

**Live preset / AOS_LIVE EA code gate:** still requires separate explicit ship step; W10 = design + dry-run; W11 = shadow retrain loop (offline blotter + realtime landing). No silent live swap.

## Gate inputs (P6-T01) — unchanged

| Metric | Engine | Shadow CF | Δ |
| --- | ---: | ---: | ---: |
| n | 530 | 491 | −39 |
| EF_pp | 2.3283 | 2.9935 | +0.6652 |
| E_N | 0.090566 | 0.10387 | +0.0133 |
| MaxDD_pp | 20.9774 | 16.8403 | −4.1371 |
| fires_kept_pct | — | 92.6415 | — |

## Decision

| Layer | Verdict |
| --- | --- |
| Auto skip-audit | FAIL (3 protect-cell FPs) |
| Operator override | **GO** for INF-W10 design + INF-W11 retrain |
| Live AI attach in EA | Not shipped in W10; pin only via W11 shadow gate |

**Next:** INF-W10 → INF-W11.
