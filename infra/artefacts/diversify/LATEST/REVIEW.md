# DIV-P0-T01 — Diversification MVP scorecard

**generated_utc:** 2026-10-21T16:39:43.753394+00:00
**panel:** 2025-01-02 -> 2026-10-16 · 653 days · ['EURUSD', 'AUDUSD', 'AAPL', 'UK100', 'JP225', 'DE40', 'USDJPY']

## Caveat

P0 uses engine/research fire-tape proxies — not locked live-OS Tester exports. Do not raise live f from this scorecard.

## Sleeve proxies

| Asset | n | E_N | WR | window |
| --- | ---: | ---: | ---: | --- |
| EURUSD | 530 | 0.0906 | 0.5453 | 2025-01-02 -> 2026-09-22 |
| AUDUSD | 95 | 0.1368 | 0.5684 | 2026-01-05 -> 2026-08-28 |
| AAPL | 289 | -0.0071 | 0.4014 | 2025-01-02 -> 2026-10-16 |
| UK100 | 235 | 0.1011 | 0.4894 | 2026-01-02 -> 2026-08-28 |
| JP225 | 130 | 0.1538 | 0.3846 | 2026-01-05 -> 2026-10-16 |
| DE40 | 208 | 0.1899 | 0.5288 | 2026-01-02 -> 2026-10-16 |
| USDJPY | 63 | 0.1524 | 0.5238 | 2025-04-18 -> 2026-10-12 |

## Baseline EURUSD-only

```json
{
  "members": [
    "EURUSD"
  ],
  "k": 1,
  "n_days": 653,
  "sum_R": 48.0,
  "mean_daily_R": 0.073507,
  "month_hit": 0.6667,
  "n_months": 18,
  "quarter_hit": 0.7143,
  "n_quarters": 7,
  "CVaR_m20": -3.25,
  "worst_month": -6.0,
  "best_month": 10.0,
  "maxDD": -21.0,
  "fuse_days": 0,
  "active_days": 307
}
```

## Top clusters (k=2,3 by month_hit, banned twins demoted)

| rank | members | month_hit | n_m | quarter_hit | sum_R | CVaR_m20 | fuse_days | maxDD |
| ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | JP225+DE40 | 0.8 | 10 | 1.0 | 29.75 | -2.6875 | 3 | -6.375 |
| 2 | AUDUSD+JP225+DE40 | 0.75 | 8 | 1.0 | 24.1667 | -1.9583 | 2 | -5.1667 |
| 3 | EURUSD+UK100+USDJPY | 0.7143 | 21 | 0.75 | 27.1167 | -1.1333 | 5 | -7.6 |
| 4 | DE40+USDJPY | 0.6875 | 16 | 0.7143 | 24.55 | -1.1875 | 2 | -4.525 |
| 5 | EURUSD+JP225+DE40 | 0.6667 | 21 | 0.75 | 35.8333 | -1.1667 | 0 | -7.0 |
| 6 | EURUSD+DE40+USDJPY | 0.6667 | 21 | 0.75 | 32.3667 | -1.1333 | 1 | -7.6833 |
| 7 | EURUSD+USDJPY | 0.65 | 20 | 0.75 | 28.8 | -1.875 | 1 | -10.9 |
| 8 | EURUSD+AAPL+UK100 | 0.6364 | 22 | 0.75 | 23.2324 | -1.9132 | 7 | -9.8728 |
| 9 | EURUSD+AAPL+USDJPY | 0.6364 | 22 | 0.75 | 18.5158 | -2.1151 | 2 | -10.0982 |
| 10 | AAPL+DE40+USDJPY | 0.6364 | 22 | 0.75 | 15.6824 | -2.0765 | 1 | -6.3263 |
| 11 | EURUSD+AAPL+DE40 | 0.6364 | 22 | 0.625 | 28.4824 | -1.8684 | 5 | -9.7149 |
| 12 | EURUSD+UK100 | 0.6316 | 19 | 0.7143 | 35.875 | -1.625 | 8 | -10.5 |

## Do not combine (heuristic + known twins)

- **EURUSD+AUDUSD** · co_loss=0.3 · n_both=50 · known_twin_hypothesis
- **UK100+DE40** · co_loss=0.1023 · n_both=88 · known_twin_hypothesis

## Verdict

**ACCEPT P0 research** — best vs EUR month_hit: `JP225+DE40` (month_hit=0.8, sum_R=29.75). Proceed DIV-P1 regime-conditioned corr; do not raise live f.
