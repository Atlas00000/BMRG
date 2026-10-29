# GRP-P1-T01 — Dependence + twin stress

**generated_utc:** 2026-10-22T13:17:11.185325+00:00
**P0 accepted:** 66 → **P1 kept:** 66 (dropped hard 0)
**Resilient (tip Sep/Oct hit ≥ 0.5):** 66 · **clean resilient:** 32

## Caveat

Tip-panel dependence + twin stress. Soft EU-index pairs may escalate to hard if co_loss>=0.40. Adverse = Sep/Oct tip months + curated stress calendar. Still provisional until GRP-P2 bootstrap.

## Ban matrix

- Hard: `[['AUDUSD', 'EURUSD']]`
- Soft: `[['AAPL', 'JP225'], ['DE40', 'UK100']]`
- Thresholds: {'co_loss_hard': 0.4, 'co_loss_soft': 0.3, 'min_n_both': 6}

### Top co-loss pairs

| a | b | n_both | co_loss | corr_active |
| --- | --- | ---: | ---: | ---: |
| JP225 | AAPL | 12 | 0.3333 | -0.4581 |
| EURUSD | AUDUSD | 38 | 0.2632 | 0.4348 |
| AUDUSD | AAPL | 19 | 0.2632 | 0.0278 |
| EURUSD | JP225 | 34 | 0.2059 | 0.0692 |
| DE40 | AUDUSD | 32 | 0.1875 | 0.0689 |
| JP225 | AUDUSD | 27 | 0.1852 | 0.181 |
| DE40 | AAPL | 27 | 0.1852 | 0.0114 |
| EURUSD | AAPL | 23 | 0.1739 | -0.1018 |
| JP225 | UK100 | 30 | 0.1667 | 0.1499 |
| EURUSD | USDJPY | 18 | 0.1667 | 0.0774 |
| DE40 | USDJPY | 27 | 0.1481 | 0.1934 |
| JP225 | DE40 | 34 | 0.1176 | -0.0398 |

## Clean resilient (preferred ops shortlist)

| Rank | Group | pen | tip_adv_hit | tip_adv_ΣR | m_hit | sum_R |
| ---: | --- | ---: | ---: | ---: | ---: | ---: |
| 1 | JP225+DE40 | 0.0 | 1.0 | 3.0 | 1.0 | 31.0 |
| 2 | EURUSD+JP225+UK100 | 0.0 | 1.0 | 2.1667 | 1.0 | 23.5833 |
| 3 | EURUSD+JP225+DE40 | 0.0 | 1.0 | 3.6667 | 1.0 | 27.3333 |
| 4 | JP225+USDJPY | 0.0 | 1.0 | 2.2 | 1.0 | 22.4 |
| 5 | JP225+DE40+USDJPY | 0.0 | 1.0 | 2.8 | 1.0 | 25.6 |
| 6 | EURUSD+JP225 | 0.0 | 1.0 | 3.5 | 1.0 | 25.0 |
| 7 | EURUSD+JP225+DE40+USDJPY | 0.0 | 1.0 | 3.35 | 1.0 | 24.2 |
| 8 | DE40+USDJPY | 0.0 | 1.0 | 3.2 | 1.0 | 23.4 |
| 9 | EURUSD+DE40+USDJPY | 0.0 | 1.0 | 3.8 | 1.0 | 22.2667 |
| 10 | EURUSD+JP225+USDJPY | 0.0 | 1.0 | 3.1333 | 1.0 | 21.6 |
| 11 | EURUSD+JP225+USDJPY+UK100 | 0.0 | 1.0 | 2.225 | 1.0 | 21.3875 |
| 12 | DE40+USDJPY+AAPL | 0.0 | 1.0 | 2.0807 | 1.0 | 20.8807 |
| 13 | EURUSD+DE40+USDJPY+AAPL | 0.0 | 1.0 | 2.8105 | 1.0 | 20.6605 |
| 14 | EURUSD+USDJPY+UK100 | 0.0 | 1.0 | 2.3 | 1.0 | 18.5167 |
| 15 | EURUSD+USDJPY+UK100+AAPL | 0.0 | 1.0 | 1.6855 | 1.0 | 17.848 |
| 16 | EURUSD+USDJPY | 0.0 | 1.0 | 3.7 | 1.0 | 17.4 |
| 17 | EURUSD+USDJPY+AAPL | 0.0 | 1.0 | 2.414 | 1.0 | 16.8807 |
| 18 | JP225+DE40+AUDUSD | 0.0 | 0.5 | 0.0 | 0.8333 | 25.0 |
| 19 | JP225+DE40+AUDUSD+USDJPY | 0.0 | 0.5 | 0.6 | 0.8333 | 22.45 |
| 20 | JP225+USDJPY+UK100 | 0.0 | 0.5 | 1.3 | 0.8333 | 21.85 |

## Top kept (all, by penalty)

| Rank | Group | pen | tip_adv_hit | tags | sum_R |
| ---: | --- | ---: | ---: | --- | ---: |
| 1 | JP225+DE40 | 0.0 | 1.0 | — | 31.0 |
| 2 | EURUSD+JP225+UK100 | 0.0 | 1.0 | — | 23.5833 |
| 3 | EURUSD+JP225+DE40 | 0.0 | 1.0 | — | 27.3333 |
| 4 | JP225+USDJPY | 0.0 | 1.0 | — | 22.4 |
| 5 | JP225+DE40+USDJPY | 0.0 | 1.0 | — | 25.6 |
| 6 | EURUSD+JP225 | 0.0 | 1.0 | — | 25.0 |
| 7 | EURUSD+JP225+DE40+USDJPY | 0.0 | 1.0 | — | 24.2 |
| 8 | DE40+USDJPY | 0.0 | 1.0 | — | 23.4 |
| 9 | EURUSD+DE40+USDJPY | 0.0 | 1.0 | — | 22.2667 |
| 10 | EURUSD+JP225+USDJPY | 0.0 | 1.0 | — | 21.6 |
| 11 | EURUSD+JP225+USDJPY+UK100 | 0.0 | 1.0 | — | 21.3875 |
| 12 | DE40+USDJPY+AAPL | 0.0 | 1.0 | — | 20.8807 |
| 13 | EURUSD+DE40+USDJPY+AAPL | 0.0 | 1.0 | — | 20.6605 |
| 14 | EURUSD+USDJPY+UK100 | 0.0 | 1.0 | — | 18.5167 |
| 15 | EURUSD+USDJPY+UK100+AAPL | 0.0 | 1.0 | — | 17.848 |
| 16 | EURUSD+USDJPY | 0.0 | 1.0 | — | 17.4 |
| 17 | EURUSD+USDJPY+AAPL | 0.0 | 1.0 | — | 16.8807 |
| 18 | JP225+DE40+AUDUSD | 0.0 | 0.5 | — | 25.0 |
| 19 | JP225+DE40+AUDUSD+USDJPY | 0.0 | 0.5 | — | 22.45 |
| 20 | JP225+USDJPY+UK100 | 0.0 | 0.5 | — | 21.85 |

## Next

1. GRP-P2 — bootstrap + May–Aug / Sep–Oct holdout (clears provisional).
2. Prefer **clean resilient** shortlist for weight trials (GRP-P3).

Artefacts: `infra/artefacts/grouping/P1_LATEST/` · `blotter/archive/GRP-P1-T01/`
