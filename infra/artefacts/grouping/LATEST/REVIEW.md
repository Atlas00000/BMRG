# GRP-P0-T01 — Asset group enum (tip 6m)

**generated_utc:** 2026-10-22T13:07:50.545059+00:00
**panel:** 2026-05-01 → 2026-10-19 (172 days)
**enumerated:** 112 · **accepted provisional:** 66 · **rejected:** 46

## Caveat

Equal-weight tip 6m designed R. Admission rules 1–4 only — bootstrap/holdout (rule 5) is GRP-P2. Provisional range; do not raise live f or auto-attach.

## EUR-only baseline

| month_hit | quarter_hit | sum_R | CVaR_m20 | maxDD |
| ---: | ---: | ---: | ---: | ---: |
| 0.8333 | 0.6667 | 20.0 | 0.0 | -5.0 |

## Acceptable range (provisional)

Rank: soft-clean first, then month_hit · quarter_hit · E_month · −|CVaR| · sum_R.

### Soft-clean (no twin / freq / caution-only flags)

| Rank | Group | k | m_hit | q_hit | E_month | sum_R | CVaR | fuse |
| ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | JP225+DE40 | 2 | 1.0 | 1.0 | 5.1667 | 31.0 | 1.5 | 0 |
| 2 | EURUSD+JP225+UK100 | 3 | 1.0 | 1.0 | 4.7167 | 23.5833 | 0.3333 | 1 |
| 3 | EURUSD+JP225+DE40 | 3 | 1.0 | 1.0 | 4.5556 | 27.3333 | 1.2083 | 0 |
| 4 | JP225+USDJPY | 2 | 1.0 | 1.0 | 4.48 | 22.4 | 1.8 | 0 |
| 5 | JP225+DE40+AAPL | 3 | 1.0 | 1.0 | 4.3246 | 25.9474 | 0.9737 | 0 |
| 6 | JP225+DE40+USDJPY | 3 | 1.0 | 1.0 | 4.2667 | 25.6 | 1.4 | 0 |
| 7 | EURUSD+JP225 | 2 | 1.0 | 1.0 | 4.1667 | 25.0 | 0.75 | 2 |
| 8 | EURUSD+JP225+DE40+AAPL | 4 | 1.0 | 1.0 | 4.0768 | 24.4605 | 1.3553 | 0 |
| 9 | EURUSD+JP225+DE40+USDJPY | 4 | 1.0 | 1.0 | 4.0333 | 24.2 | 1.675 | 0 |
| 10 | DE40+USDJPY | 2 | 1.0 | 1.0 | 3.9 | 23.4 | 1.6 | 1 |
| 11 | JP225+DE40+USDJPY+AAPL | 4 | 1.0 | 1.0 | 3.8601 | 23.1605 | 1.0303 | 0 |
| 12 | EURUSD+JP225+DE40+USDJPY+AAPL | 5 | 1.0 | 1.0 | 3.7547 | 22.5284 | 1.3242 | 0 |
| 13 | EURUSD+DE40+USDJPY | 3 | 1.0 | 1.0 | 3.7111 | 22.2667 | 1.475 | 1 |
| 14 | EURUSD+JP225+AAPL | 3 | 1.0 | 1.0 | 3.6579 | 21.9474 | 1.1404 | 0 |
| 15 | EURUSD+JP225+UK100+AAPL | 4 | 1.0 | 1.0 | 3.608 | 21.648 | 0.7928 | 1 |
| 16 | EURUSD+JP225+USDJPY | 3 | 1.0 | 1.0 | 3.6 | 21.6 | 1.5 | 0 |
| 17 | EURUSD+JP225+USDJPY+UK100 | 4 | 1.0 | 1.0 | 3.5646 | 21.3875 | 0.875 | 1 |
| 18 | DE40+USDJPY+AAPL | 3 | 1.0 | 1.0 | 3.4801 | 20.8807 | 1.0404 | 0 |
| 19 | EURUSD+DE40+USDJPY+AAPL | 4 | 1.0 | 1.0 | 3.4434 | 20.6605 | 1.4053 | 0 |
| 20 | EURUSD+JP225+USDJPY+UK100+AAPL | 5 | 1.0 | 1.0 | 3.3797 | 20.2784 | 0.8742 | 0 |
| … | (30 more soft-clean in ACCEPTABLE_RANGE.json) | | | | | | | |

### Soft-flagged still admitted (16) — need GRP-P1 stress

| Rank | Group | k | m_hit | soft | sum_R |
| ---: | --- | ---: | ---: | --- | ---: |
| 1 | JP225+DE40+UK100 | 3 | 1.0 | eu_index_twin | 27.5833 |
| 2 | EURUSD+JP225+DE40+UK100 | 4 | 1.0 | eu_index_twin | 25.6875 |
| 3 | JP225+DE40+UK100+AAPL | 4 | 1.0 | eu_index_twin | 24.648 |
| 4 | JP225+DE40+USDJPY+UK100 | 4 | 1.0 | eu_index_twin | 24.3875 |
| 5 | EURUSD+JP225+DE40+UK100+AAPL | 5 | 1.0 | eu_index_twin | 23.7184 |
| 6 | EURUSD+JP225+DE40+USDJPY+UK100 | 5 | 1.0 | eu_index_twin | 23.51 |
| 7 | JP225+DE40+USDJPY+UK100+AAPL | 5 | 1.0 | eu_index_twin | 22.6784 |
| 8 | DE40+USDJPY+UK100 | 3 | 1.0 | eu_index_twin | 22.5167 |
| 9 | EURUSD+DE40+USDJPY+UK100 | 4 | 1.0 | eu_index_twin | 21.8875 |
| 10 | DE40+USDJPY+UK100+AAPL | 4 | 1.0 | eu_index_twin | 20.848 |
| 11 | EURUSD+DE40+USDJPY+UK100+AAPL | 5 | 1.0 | eu_index_twin | 20.6784 |
| 12 | JP225+DE40+AUDUSD+UK100 | 4 | 0.8333 | eu_index_twin | 23.9375 |
| 13 | JP225+DE40+AUDUSD+UK100+AAPL | 5 | 0.8333 | eu_index_twin | 22.3184 |
| 14 | JP225+DE40+AUDUSD+USDJPY+UK100 | 5 | 0.8333 | eu_index_twin | 22.11 |
| 15 | DE40+AUDUSD+USDJPY+UK100 | 4 | 0.8333 | eu_index_twin | 20.1375 |
| … | (1 more flagged) | | | | |

## Reject reason tallies

| Reason | n |
| --- | ---: |
| quarter_hit | 34 |
| hard_ban_pair | 26 |
| month_hit | 10 |

## Next

1. GRP-P1 — co-loss / twin stress re-rank.
2. GRP-P2 — bootstrap + May–Aug / Sep–Oct holdout (clears provisional).
3. Do not promote to VPS from this range alone.

Artefacts: `infra/artefacts/grouping/LATEST/` · archive `blotter/archive/GRP-P0-T01/`
