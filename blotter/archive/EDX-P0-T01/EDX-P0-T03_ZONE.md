# EDX-P0-T03 — Production-gate zone (Stage 1 numbers)

**Scored:** 2026-09-25  
**Source:** P0-T01 full sample + P0-T02 windows  
**Cost assumption:** Leak = 0 (costs_defaulted — pips run)

## Formulae

```
BM  = WR − BWR
EF  = BM − Leak
M   = 1.96 × sqrt(WR(1−WR)/n)
```

## Full sample (n=570, WR=44.74%, R=1.5, BWR=40%)

| Symbol | Value |
| --- | ---: |
| BM | +4.74 pp |
| Leak | 0 pp (unmeasured) |
| EF | +4.74 pp |
| M | ±4.08 pp |
| EF > M? | Yes (+0.66 pp headroom) |
| Gross zone | **Robust** (fragile in practice) |

## With illustrative Leak stress (not measured)

| Leak | EF | vs M 4.08 | Zone |
| ---: | ---: | --- | --- |
| 0 pp | 4.74 | > M | Robust |
| 1 pp | 3.74 | ≤ M | Fragile |
| 2 pp | 2.74 | ≤ M | Fragile |
| 5 pp | −0.26 | ≤ 0 | Negative |

EURUSD M5 round-turn friction often lands in the 1–3 pp WR-equivalent range at this R → **expect Fragile** once currency blotter exists.

## Gate-relevant windows

| Sample | EF | M | Zone |
| --- | ---: | ---: | --- |
| Full | 4.74 | 4.08 | Robust* |
| Latest W500 | 4.20 | 4.35 | Fragile |
| Latest W250 | 4.80 | 6.16 | Fragile |

Unified G1 requires EF > M on full **and** latest W500.  
**G1 verdict (gross):** **FAIL** — W500 Fragile even at Leak=0.

## Official P0 Stage 1 label

**Fragile** (production gate not passed).  
Do not treat the full-sample gross Robust as production-worthy.

## Side diagnosis (unchanged)

**WR-side** thin margin; R ≈ RR.
