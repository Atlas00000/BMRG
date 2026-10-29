# GRP-P5-T01 — HITL group promotion

**generated_utc:** 2026-10-22T13:48:34.312492+00:00
**status:** FROZEN
**panel:** 2026.05.01 → 2026.10.20 tip

## Caveat

HITL capital-map freeze from tip 6m grouping (P0–P4). Designed R. Does not raise live f. Canvas/display secondary to this scorecard + live_asset_profile.md.

## Primary

**JP225+DE40** · policy `max_sum_R` · weights `{'JP225': 0.5, 'DE40': 0.5}`

Highest tip designed sum_R among OOS-stable/Pareto; clean tiers; equal 50/50; shallow fuse; keep EURUSD as separate production sleeve.

| metric | value |
| --- | ---: |
| month_hit | 1.0 |
| quarter_hit | 1.0 |
| sum_R | 31.0 |
| E_month | 5.1667 |
| CVaR_m20 | 1.5 |
| maxDD | -2.5 |
| fuse_days | 0 |
| max_tail_dep | 0.3333 |
| val_sum_R | 3.0 |
| boot_month_hit_p10 | 1.0 |

## Secondaries (policy menu)

- **DE40+USDJPY** (`max_holdout_val`) — Best Sep–Oct holdout among Pareto front; use when prioritizing recent tip resilience.
  sum_R=23.4 · m_hit=1.0 · val=3.2 · maxDD=-4.275 · tail=0.375 · w={'DE40': 0.5, 'USDJPY': 0.5}
- **JP225+USDJPY** (`best_CVaR`) — Best CVaR / shallow maxDD on front; Asia+JPY diversifier without DE.
  sum_R=22.4 · m_hit=1.0 · val=2.2 · maxDD=-1.5 · tail=0.45 · w={'JP225': 0.5, 'USDJPY': 0.5}
- **EURUSD+DE40+USDJPY+AAPL** (`min_maxDD`) — Only Pareto champion that includes production EURUSD; shallowest maxDD. AAPL at equal 25% — keep light / caution in attach policy.
  sum_R=20.6605 · m_hit=1.0 · val=2.8105 · maxDD=-1.1316 · tail=0.4875 · w={'EURUSD': 0.25, 'DE40': 0.25, 'USDJPY': 0.25, 'AAPL': 0.25}
- **USDJPY+UK100** (`min_tail`) — Lowest max pairwise tail_dep on front but weaker tip hit / holdout; UK100 halt history — watch only, not default capital.
  sum_R=17.775 · m_hit=0.8333 · val=0.95 · maxDD=-2.625 · tail=0.254 · w={'USDJPY': 0.615385, 'UK100': 0.384615}

## VPS attach policy (primary map)

| Sleeve | Posture | Bucket |
| --- | --- | --- |
| EURUSD | full | production |
| JP225 | full | research_cluster_primary |
| DE40 | full | research_cluster_primary |
| USDJPY | light | research_optional |
| AAPL | light | caution |
| UK100 | off_pending_halt_review | caution |
| AUDUSD | ft_twin_only | fx_twin_excluded_from_groups |

## Next

1. Operator confirms primary vs alternate on VPS.
2. Update `doc/live_asset_profile.md` capital map (done with this task).
3. No live f raise from tip grouping alone.

Artefacts: `infra/artefacts/grouping/P5_LATEST/` · `blotter/archive/GRP-P5-T01/`
