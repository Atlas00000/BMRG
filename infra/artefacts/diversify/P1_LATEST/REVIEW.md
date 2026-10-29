# DIV-P1-T01 — Regime-conditioned diversification

**generated_utc:** 2026-10-21T16:43:02.240137+00:00
**panel:** 2025-01-02 -> 2026-10-16 · 653 days

## Caveat

Regime tags from fire-tape ouroboros/regime_tag (normalized). EURUSD Harvest labeled has no tag → UNTAGGED except stress months. Stress calendar is doc-curated months — not live L2.

## Book regime day counts

| Regime | days |
| --- | ---: |
| UNTAGGED | 322 |
| FRAGILE | 186 |
| MISMATCH | 98 |
| MATCH | 47 |

**Stress-calendar active days:** 127 (doc months × active sleeve)

## Co-loss deltas (conditioned - full) — top adverse spikes

| pair | co_loss full | co_loss adverse | delta | n_both adverse |
| --- | ---: | ---: | ---: | ---: |
| AUDUSD+UK100 | 0.2143 | 0.2903 | 0.076 | 31 |
| AUDUSD+JP225 | 0.2105 | 0.2581 | 0.0476 | 31 |
| AUDUSD+DE40 | 0.0976 | 0.1333 | 0.0357 | 30 |
| EURUSD+AUDUSD | 0.3 | 0.3333 | 0.0333 | 36 |
| EURUSD+DE40 | 0.1304 | 0.1552 | 0.0248 | 58 |
| DE40+USDJPY | 0.1786 | 0.2 | 0.0214 | 25 |
| EURUSD+USDJPY | 0.2083 | 0.2222 | 0.0139 | 18 |
| JP225+DE40 | 0.2063 | 0.2143 | 0.008 | 56 |
| AAPL+USDJPY | 0.1724 | 0.1786 | 0.0062 | 28 |
| AAPL+UK100 | 0.2742 | 0.2787 | 0.0045 | 61 |

## Clusters resilient on ADVERSE days (sum_R>=0, n>=10)

| members | adverse sum_R | adverse days | full month_hit | full sum_R |
| --- | ---: | ---: | ---: | ---: |
| EURUSD+JP225+DE40 | 26.1667 | 284 | 0.6667 | 35.8333 |
| JP225+DE40 | 24.25 | 284 | 0.8 | 29.75 |
| EURUSD+DE40+USDJPY | 21.7667 | 284 | 0.6667 | 32.3667 |
| EURUSD+USDJPY | 20.9 | 284 | 0.65 | 28.8 |
| EURUSD+UK100+USDJPY | 20.0167 | 284 | 0.7143 | 27.1167 |
| DE40+USDJPY | 17.65 | 284 | 0.6875 | 24.55 |
| AUDUSD+JP225+DE40 | 16.8333 | 284 | 0.75 | 24.1667 |
| EURUSD+AAPL+UK100 | 13.4342 | 284 | 0.6364 | 23.2324 |

## Stress month registry (P1-T03)

- **AUDUSD** m=02 · Feb soft · _AUDUSD aos_bad_cells / profile_
- **AUDUSD** m=03 · Mar soft · _AUDUSD aos_bad_cells / profile_
- **AUDUSD** m=05 · May soft · _AUDUSD aos_bad_cells_
- **AAPL** m=05 · May cell · _AAPL aos_bad_cells_M5_
- **AAPL** m=07 · Jul cell · _AAPL aos_bad_cells_M5_
- **UK100** m=09 · Sep tip soft · _UK100 M5 profile / P1_
- **DE40** m=02 · Feb stress-month · _DE40 aos_bad_cells_
- **DE40** m=03 · Mar FRAGILE · _DE40 aos_bad_cells_
- **JP225** m=02 · Feb soft · _JP225 aos_bad_cells_M5_
- **JP225** m=04 · Apr soft · _JP225 aos_bad_cells_M5_
- **JP225** m=08 · Aug MATCH tax · _JP225 aos_bad_cells_M5_
- **JP225** m=09 · Sep MATCH tax · _JP225 aos_bad_cells_M5_
- **USDJPY** m=07 · Jul sleeve caution · _USDJPY aos_bad_cells / P6_
- **EURUSD** m=09 · Sep soft proxy · _EURUSD edge / historical tip_

## Verdict

**ACCEPT P1 research** — most resilient clean cluster on ADVERSE: `EURUSD+JP225+DE40` (adverse sum_R=26.1667, full month_hit=0.6667). Use for DIV-P2 live-tape refresh; do not raise live f.
