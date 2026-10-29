# GRP-P4-T01 — Tail · Pareto · Surrogate

**generated_utc:** 2026-10-22T13:42:28.556373+00:00
**OOS-stable:** 24 · **Pareto front:** 5

## Caveat

P4 enhances OOS-stable tip groups: lower-tail dep (q=0.2), Pareto on hit/E/CVaR/DD/fuse/tail, ridge surrogate LOO. Does not invent membership. Not a live attach.

## T03 — Tail dependence (q=0.2)

Escalate→hard: 0 · New soft: 8

| a | b | co_loss | tail_dep | corr | action |
| --- | --- | ---: | ---: | ---: | --- |
| EURUSD | AUDUSD | 0.2632 | 0.6111 | 0.4348 | — |
| DE40 | AUDUSD | 0.1875 | 0.5308 | 0.0689 | new_soft |
| AUDUSD | AAPL | 0.2632 | 0.5278 | 0.0278 | new_soft |
| JP225 | AAPL | 0.3333 | 0.5 | -0.4581 | — |
| JP225 | AUDUSD | 0.1852 | 0.4911 | 0.181 | new_soft |
| EURUSD | USDJPY | 0.1667 | 0.4875 | 0.0774 | new_soft |
| JP225 | UK100 | 0.1667 | 0.4762 | 0.1499 | new_soft |
| EURUSD | JP225 | 0.2059 | 0.4521 | 0.0692 | new_soft |
| JP225 | USDJPY | 0.05 | 0.45 | -0.1567 | new_soft |
| USDJPY | AAPL | 0.0 | 0.45 | -0.1446 | new_soft |

## T01 — Pareto front (policy champions)

Champions: `{'max_sum_R': 'JP225+DE40', 'max_holdout_val': 'DE40+USDJPY', 'best_CVaR': 'JP225+USDJPY', 'min_maxDD': 'EURUSD+DE40+USDJPY+AAPL', 'min_tail': 'USDJPY+UK100'}`

| Group | policy | m_hit | sum_R | CVaR | maxDD | tail | val_sum |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| JP225+DE40 | max_sum_R | 1.0 | 31.0 | 1.5 | -2.5 | 0.3333 | 3.0 |
| DE40+USDJPY | max_holdout_val | 1.0 | 23.4 | 1.6 | -4.275 | 0.375 | 3.2 |
| JP225+USDJPY | best_CVaR | 1.0 | 22.4 | 1.8 | -1.5 | 0.45 | 2.2 |
| EURUSD+DE40+USDJPY+AAPL | min_maxDD | 1.0 | 20.6605 | 1.4053 | -1.1316 | 0.4875 | 2.8105 |
| USDJPY+UK100 | min_tail | 0.8333 | 17.775 | 0.275 | -2.625 | 0.254 | 0.95 |

## T02 — Surrogate

LOO R²=0.6234 · RMSE=0.0316 · n=32

Top |coef| features:
- `has_aud`: -0.0477
- `has_eur`: 0.0259
- `mean_corr`: 0.0184
- `mean_freq`: -0.0119
- `max_tail`: -0.0109
- `n_core`: 0.009
- `k`: 0.0068
- `has_uk`: -0.0047

## Next

1. GRP-P5 HITL — pick from Pareto champions + equal weights (P3).
2. Apply any tail escalate_hard into ban matrix before live attach.

Artefacts: `infra/artefacts/grouping/P4_LATEST/` · `blotter/archive/GRP-P4-T01/`
