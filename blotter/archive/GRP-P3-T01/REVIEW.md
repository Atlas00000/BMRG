# GRP-P3-T01 — Weights inside OOS-stable groups

**generated_utc:** 2026-10-22T13:30:17.487174+00:00
**groups:** 24
**scheme wins (raw):** {'hrp': 1, 'equal': 23}
**scheme wins (f_budget):** {'equal': 24}

## Caveat

Weights from tip daily R cov. f_budget caps are research hints (EURUSD floor/cap · research/caution caps) — not VPS attach policy. Still HITL for GRP-P5.

## Recommended (f_budget) shortlist

| Rank | Group | scheme | sum_R | m_hit | maxDD | vs_eq | prod_w | weights |
| ---: | --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| 1 | JP225+DE40 | equal | 31.0 | 1.0 | -2.5 | 0.0 | 0.0 | DE40:0.50, JP225:0.50 |
| 2 | EURUSD+JP225+DE40 | equal | 27.3333 | 1.0 | -2.6667 | 0.0 | 0.333333 | DE40:0.33, EURUSD:0.33, JP225:0.33 |
| 3 | JP225+DE40+USDJPY | equal | 25.6 | 1.0 | -1.6 | 0.0 | 0.0 | DE40:0.33, JP225:0.33, USDJPY:0.33 |
| 4 | EURUSD+JP225 | equal | 24.4444 | 1.0 | -4.0 | -0.5556 | 0.555556 | EURUSD:0.56, JP225:0.44 |
| 5 | EURUSD+JP225+DE40+USDJPY | equal | 24.2 | 1.0 | -1.7 | 0.0 | 0.25 | DE40:0.25, EURUSD:0.25, JP225:0.25, USDJPY:0.25 |
| 6 | EURUSD+JP225+UK100 | equal | 23.8409 | 1.0 | -2.9091 | 0.2576 | 0.363636 | EURUSD:0.36, JP225:0.36, UK100:0.27 |
| 7 | DE40+USDJPY | equal | 23.4 | 1.0 | -4.275 | 0.0 | 0.0 | DE40:0.50, USDJPY:0.50 |
| 8 | JP225+USDJPY | equal | 22.4 | 1.0 | -1.5 | 0.0 | 0.0 | JP225:0.50, USDJPY:0.50 |
| 9 | EURUSD+DE40+USDJPY | equal | 22.2666 | 1.0 | -1.6667 | 0.0 | 0.333333 | DE40:0.33, EURUSD:0.33, USDJPY:0.33 |
| 10 | EURUSD+JP225+USDJPY | equal | 21.6 | 1.0 | -2.0 | 0.0 | 0.333333 | EURUSD:0.33, JP225:0.33, USDJPY:0.33 |
| 11 | EURUSD+JP225+USDJPY+UK100 | equal | 21.3875 | 1.0 | -1.75 | 0.0 | 0.25 | EURUSD:0.25, JP225:0.25, UK100:0.25, USDJPY:0.25 |
| 12 | DE40+USDJPY+AAPL | equal | 21.3387 | 1.0 | -2.7072 | 0.458 | 0.0 | AAPL:0.27, DE40:0.36, USDJPY:0.36 |
| 13 | EURUSD+DE40+USDJPY+AAPL | equal | 20.6605 | 1.0 | -1.1316 | 0.0 | 0.25 | AAPL:0.25, DE40:0.25, EURUSD:0.25, USDJPY:0.25 |
| 14 | EURUSD+USDJPY+UK100 | equal | 18.3136 | 1.0 | -1.9545 | -0.203 | 0.363636 | EURUSD:0.36, UK100:0.27, USDJPY:0.36 |
| 15 | EURUSD+USDJPY+UK100+AAPL | equal | 17.848 | 1.0 | -1.5625 | 0.0 | 0.25 | AAPL:0.25, EURUSD:0.25, UK100:0.25, USDJPY:0.25 |
| 16 | EURUSD+USDJPY | equal | 17.6889 | 1.0 | -2.0444 | 0.2889 | 0.555556 | EURUSD:0.56, USDJPY:0.44 |
| 17 | EURUSD+USDJPY+AAPL | equal | 16.9751 | 1.0 | -1.3254 | 0.0944 | 0.363636 | AAPL:0.27, EURUSD:0.36, USDJPY:0.36 |
| 18 | JP225+DE40+AUDUSD | equal | 25.0 | 0.8333 | -2.0 | 0.0 | 0.0 | AUDUSD:0.33, DE40:0.33, JP225:0.33 |
| 19 | JP225+DE40+AUDUSD+USDJPY | equal | 22.45 | 0.8333 | -1.5 | 0.0 | 0.0 | AUDUSD:0.25, DE40:0.25, JP225:0.25, USDJPY:0.25 |
| 20 | JP225+USDJPY+UK100 | equal | 21.95 | 0.8333 | -2.0909 | 0.1 | 0.0 | JP225:0.36, UK100:0.27, USDJPY:0.36 |

## Core packs (EUR / JP / DE focus)

- **JP225+DE40** · equal · sum_R=31.0 · w={'JP225': 0.5, 'DE40': 0.5}
- **EURUSD+JP225+DE40** · equal · sum_R=27.3333 · w={'EURUSD': 0.333333, 'JP225': 0.333333, 'DE40': 0.333333}
- **JP225+DE40+USDJPY** · equal · sum_R=25.6 · w={'JP225': 0.333333, 'DE40': 0.333333, 'USDJPY': 0.333333}
- **EURUSD+JP225** · equal · sum_R=24.4444 · w={'EURUSD': 0.555556, 'JP225': 0.444444}
- **EURUSD+JP225+DE40+USDJPY** · equal · sum_R=24.2 · w={'EURUSD': 0.25, 'JP225': 0.25, 'DE40': 0.25, 'USDJPY': 0.25}
- **EURUSD+JP225+UK100** · equal · sum_R=23.8409 · w={'EURUSD': 0.363636, 'JP225': 0.363636, 'UK100': 0.272727}
- **DE40+USDJPY** · equal · sum_R=23.4 · w={'DE40': 0.5, 'USDJPY': 0.5}
- **JP225+USDJPY** · equal · sum_R=22.4 · w={'JP225': 0.5, 'USDJPY': 0.5}
- **EURUSD+DE40+USDJPY** · equal · sum_R=22.2666 · w={'EURUSD': 0.333333, 'DE40': 0.333333, 'USDJPY': 0.333333}
- **EURUSD+JP225+USDJPY** · equal · sum_R=21.6 · w={'EURUSD': 0.333333, 'JP225': 0.333333, 'USDJPY': 0.333333}

## Next

1. GRP-P5 HITL — pick 1–N groups + weights for live profile.
2. GRP-P4 remains paused.

Artefacts: `infra/artefacts/grouping/P3_LATEST/` · `blotter/archive/GRP-P3-T01/`
