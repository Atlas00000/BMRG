# GRP-P2-T01 — Bootstrap + holdout + fuse (OOS-stable range)

**generated_utc:** 2026-10-22T13:21:02.428947+00:00
**candidates:** 32 → **OOS-stable:** 24 · **fail:** 8

## Caveat

Block bootstrap of tip months/weeks + May-Aug/Sep-Oct holdout + fuse stub (next-day suppress after multi-sleeve R_p < -1R). OOS-stable clears provisional for tip panel only — still not a live f / attach promotion.

## Thresholds

```
{
  "boot_hit_p10_floor": 0.5,
  "val_sum_floor": 0.0,
  "val_hit_floor": 0.5,
  "fuse_hit_drop_max": 0.34,
  "month_hit_floor_ref": 0.67,
  "n_boot": 1000,
  "seed": 42,
  "candidate_source": "clean_resilient"
}
```

## OOS-stable groups

| Rank | Group | boot_p10 | val_sum | val_hit | m_hit | sum_R | fuseΔ |
| ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | EURUSD+DE40+USDJPY | 1.0 | 3.8 | 1.0 | 1.0 | 22.2667 | 0.3333 |
| 2 | EURUSD+USDJPY | 1.0 | 3.7 | 1.0 | 1.0 | 17.4 | 0.5 |
| 3 | EURUSD+JP225+DE40 | 1.0 | 3.6667 | 1.0 | 1.0 | 27.3333 | 0.0 |
| 4 | EURUSD+JP225 | 1.0 | 3.5 | 1.0 | 1.0 | 25.0 | -0.5 |
| 5 | EURUSD+JP225+DE40+USDJPY | 1.0 | 3.35 | 1.0 | 1.0 | 24.2 | 0.0 |
| 6 | DE40+USDJPY | 1.0 | 3.2 | 1.0 | 1.0 | 23.4 | 0.0 |
| 7 | EURUSD+JP225+USDJPY | 1.0 | 3.1333 | 1.0 | 1.0 | 21.6 | 0.0 |
| 8 | JP225+DE40 | 1.0 | 3.0 | 1.0 | 1.0 | 31.0 | 0.0 |
| 9 | EURUSD+DE40+USDJPY+AAPL | 1.0 | 2.8105 | 1.0 | 1.0 | 20.6605 | 0.0 |
| 10 | JP225+DE40+USDJPY | 1.0 | 2.8 | 1.0 | 1.0 | 25.6 | 0.0 |
| 11 | EURUSD+USDJPY+AAPL | 1.0 | 2.414 | 1.0 | 1.0 | 16.8807 | 0.0 |
| 12 | EURUSD+USDJPY+UK100 | 1.0 | 2.3 | 1.0 | 1.0 | 18.5167 | 0.0 |
| 13 | EURUSD+JP225+USDJPY+UK100 | 1.0 | 2.225 | 1.0 | 1.0 | 21.3875 | 0.0 |
| 14 | JP225+USDJPY | 1.0 | 2.2 | 1.0 | 1.0 | 22.4 | 0.0 |
| 15 | EURUSD+JP225+UK100 | 1.0 | 2.1667 | 1.0 | 1.0 | 23.5833 | 0.0 |
| 16 | DE40+USDJPY+AAPL | 1.0 | 2.0807 | 1.0 | 1.0 | 20.8807 | 0.0 |
| 17 | EURUSD+USDJPY+UK100+AAPL | 1.0 | 1.6855 | 1.0 | 1.0 | 17.848 | 0.0 |
| 18 | JP225+USDJPY+UK100 | 0.6667 | 1.3 | 0.5 | 0.8333 | 21.85 | 0.0 |
| 19 | USDJPY+UK100 | 0.6667 | 0.95 | 0.5 | 0.8333 | 17.775 | 0.0 |
| 20 | JP225+DE40+AUDUSD+USDJPY | 0.6667 | 0.6 | 0.5 | 0.8333 | 22.45 | 0.0 |
| 21 | USDJPY+UK100+AAPL | 0.6667 | 0.5807 | 0.5 | 0.8333 | 17.1307 | 0.0 |
| 22 | DE40+AUDUSD+USDJPY | 0.6667 | 0.1333 | 0.5 | 0.8333 | 19.9333 | 0.0 |
| 23 | DE40+AUDUSD+USDJPY+AAPL | 0.6667 | 0.0605 | 0.5 | 0.8333 | 18.9105 | 0.0 |
| 24 | JP225+DE40+AUDUSD | 0.6667 | 0.0 | 0.5 | 0.8333 | 25.0 | 0.0 |

## Reject tallies

| Reason | n |
| --- | ---: |
| holdout_val_sum | 8 |

## Sample failures

| Group | reasons | sum_R |
| --- | --- | ---: |
| JP225+AUDUSD | holdout_val_sum=-2.0<0.0 | 21.5 |
| JP225+AUDUSD+UK100 | holdout_val_sum=-1.5<0.0 | 21.25 |
| JP225+AUDUSD+USDJPY+UK100 | holdout_val_sum=-0.525<0.0 | 19.6375 |
| JP225+AUDUSD+USDJPY | holdout_val_sum=-0.5333<0.0 | 19.2667 |
| AUDUSD+USDJPY+UK100 | holdout_val_sum=-1.3667<0.0 | 16.1833 |
| AUDUSD+USDJPY+UK100+AAPL | holdout_val_sum=-1.0645<0.0 | 16.098 |
| AUDUSD+USDJPY+AAPL | holdout_val_sum=-1.2526<0.0 | 14.5474 |
| AUDUSD+USDJPY | holdout_val_sum=-1.8<0.0 | 13.9 |

## Next

1. GRP-P3 — weights inside OOS-stable groups.
2. HITL pick from this range (GRP-P5) — still no auto VPS attach.

Artefacts: `infra/artefacts/grouping/P2_LATEST/` · `blotter/archive/GRP-P2-T01/`
