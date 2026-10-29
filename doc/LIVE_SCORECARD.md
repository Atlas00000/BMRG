# Live scorecard

**Generated:** 2026-10-29T16:23Z by `infra/src/diversify/live_scorecard.py` — do not hand-edit tables; re-run the script.
**Basis:** offline MT5 Tester backtest of the **deployed presets** · 2026-01-01 → 2026-09-30 · every tick · $500 · 1:500 · EA **1.28** · designed R (SL/TP geometry).
**Deployed posture:** SHADOW (skips logged only) — EURUSD, AUDUSD, UK100, DE40 · CURRENT (skips enforced) — AAPL, JP225, USDJPY. Set per sleeve by `deploy` in `live_runs.py`.
**Comparisons:** same window with every sleeve SHADOW, and every sleeve CURRENT.
**Canvas:** `live-scorecard.canvas.tsx`

## Summary

- Deployed book (7 sleeves, equal R): **+131.5R** · maxDD **-21.5R** · month hit **78%** · DD diversification **2.81×** · avg pairwise daily corr **-0.01**.
- All-SHADOW book +87.7R · all-CURRENT book +134.7R. Kept skips (AAPL, JP225, USDJPY L2det) were fitted on overlapping data → their contribution is **in-sample, optimistic**.
- EURUSD / UK100: no skip fired in this window (EUR L2 INF max p 0.576 < 0.606 at Tester spread 6). The Q4 calendar withhold seen live is **outside** this window.
- AUDUSD at live risk 3% (6× the 0.5% sleeves) dominates live-risk-weighted drawdown.

## 1. Sleeves — backtest (deployed presets)

| Sleeve | Mode | n | /30d | WR % | ΣR | E_N | PF | EF pp | Zone | maxDD R | Month hit | Worst month R | ΣR shadow | ΣR current |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- | ---: | ---: | ---: | ---: | ---: |
| DE40 | SHADOW | 183 | 20.6 | 54.1 | +39.8 | +0.217 | 1.47 | +2.7 | Fragile | -6.8 | 78% | -4.0 | +39.8 | +37.0 |
| UK100 | SHADOW | 236 | 26.2 | 50.0 | +29.5 | +0.125 | 1.25 | -0.3 | Below | -7.8 | 56% | -2.2 | +29.5 | +29.5 |
| EURUSD | SHADOW | 173 | 19.3 | 58.4 | +29.0 | +0.168 | 1.40 | +6.2 | Strong | -8.0 | 67% | -2.0 | +29.0 | +29.0 |
| AAPL | CURRENT | 71 | 7.9 | 46.5 | +10.6 | +0.150 | 1.28 | -9.2 | Below | -7.1 | 62% | -5.5 | -10.0 | +10.6 |
| USDJPY | CURRENT | 51 | 6.5 | 54.9 | +10.6 | +0.208 | 1.46 | -2.0 | Below | -6.4 | 71% | -3.2 | +4.4 | +10.6 |
| JP225 | CURRENT | 85 | 9.6 | 36.5 | +8.0 | +0.094 | 1.15 | -0.1 | Below | -15.0 | 44% | -9.0 | -9.0 | +8.0 |
| AUDUSD | SHADOW | 100 | 11.2 | 52.0 | +4.0 | +0.040 | 1.08 | -0.4 | Below | -13.0 | 56% | -7.0 | +4.0 | +10.0 |

EF pp = WR − breakeven WR − Leak (per-sleeve RR / Leak from run cards). Zone: Strong / Fragile / Below.

## 2. Rolling metrics — backtest (deployed presets)

W20 / W50 = rolling trade windows used by AOS L3/L4 (EF pp, E_N); 30d R = rolling calendar-30-day designed R.

| Sleeve | W20 EF min | W50 EF min | W50 EF last | W50 EN last | % bars W50 EF ≤ 0 | 30d R min | 30d R last |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| AAPL | -25.7 | -11.7 | -5.7 | +0.237 | 100.0% | -5.0 | +1.4 |
| AUDUSD | -22.4 | -8.4 | +7.6 | +0.200 | 45.1% | -8.0 | -5.0 |
| DE40 | -21.4 | -7.4 | +6.6 | +0.305 | 35.1% | -5.2 | +4.2 |
| EURUSD | -22.2 | -6.2 | +7.8 | +0.200 | 16.1% | -6.0 | +7.0 |
| JP225 | -16.6 | -8.6 | +7.4 | +0.320 | 36.1% | -9.0 | -2.0 |
| UK100 | -15.3 | -10.3 | -6.3 | -0.010 | 40.6% | -5.2 | +0.2 |
| USDJPY | -21.9 | -2.9 | -2.9 | +0.188 | 100.0% | -4.2 | +3.6 |

## 3. Portfolio combination — live book as a group

Daily designed-R panel (calendar days, by close date). **equal_R** = each sleeve 1R per trade; **live_risk_weighted** = R × (live risk % / 0.5%) (AUDUSD ×6); GRP primary = frozen JP225+DE40 cluster for reference. DD diversification × = Σ sleeve maxDD ÷ book maxDD (higher = more offset).

### Deployed book

| Metric | equal_R | live_risk_weighted | GRP primary JP225+DE40 |
| --- | ---: | ---: | ---: |
| ΣR | 131.48 | 151.48 | 47.75 |
| maxDD R | -21.53 | -85.23 | -16.50 |
| Σ sleeve maxDD R | -60.51 | -125.51 | -21.25 |
| DD diversification × | 2.81 | 1.47 | 1.29 |
| Month hit | 78% | 67% | 78% |
| Worst month R | -17.28 | -52.28 | -8.00 |
| Best month R | 33.55 | 58.02 | 22.25 |
| Day hit (active) | 60% | 61% | 52% |
| Worst day R | -6.00 | -12.80 | -3.00 |
| CVaR day 20% R | -2.25 | -6.95 | -1.31 |
| Worst ~30d R | -17.28 | -54.88 | -10.25 |
| Max sleeves losing same day | 4 | 4 | 2 |
| Days with ≥3 sleeves losing | 27 | 27 | 0 |
| Avg pairwise daily corr | -0.01 | -0.01 | 0.08 |

### Book comparison (equal R)

| Metric | deployed | all SHADOW | all CURRENT |
| --- | ---: | ---: | ---: |
| ΣR | 131.48 | 87.65 | 134.73 |
| maxDD R | -21.53 | -21.95 | -24.53 |
| Σ sleeve maxDD R | -60.51 | -72.64 | -60.26 |
| DD diversification × | 2.81 | 3.31 | 2.46 |
| Month hit | 78% | 78% | 78% |
| Worst month R | -17.28 | -15.75 | -21.28 |
| Best month R | 33.55 | 28.02 | 33.57 |
| Day hit (active) | 60% | 56% | 59% |
| Worst day R | -6.00 | -5.00 | -7.00 |
| CVaR day 20% R | -2.25 | -3.02 | -2.09 |
| Worst ~30d R | -17.28 | -15.75 | -21.28 |
| Max sleeves losing same day | 4 | 4 | 5 |
| Days with ≥3 sleeves losing | 27 | 31 | 25 |
| Avg pairwise daily corr | -0.01 | 0.02 | -0.02 |

### Monthly R (deployed presets)

| Month | AAPL | AUDUSD | DE40 | EURUSD | JP225 | UK100 | USDJPY | **Book (equal R)** |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 2026-01 | +2.3 | +5.0 | +11.8 | -1.0 | +2.0 | +11.8 | +1.2 | **+33.0** |
| 2026-02 | -5.5 | -7.0 | -4.0 | +4.0 | -4.0 | -0.8 | +0.0 | **-17.3** |
| 2026-03 | +0.4 | -2.0 | -1.0 | +10.0 | +3.0 | -1.5 | +1.2 | **+10.1** |
| 2026-04 | +0.9 | -2.0 | +4.2 | -2.0 | -9.0 | -1.2 | -1.8 | **-10.8** |
| 2026-05 | +6.4 | +3.0 | +1.0 | +0.0 | +3.0 | +11.0 | +4.2 | **+28.6** |
| 2026-06 | -0.1 | +4.0 | +1.2 | +4.0 | -1.0 | +6.8 | +5.4 | **+20.3** |
| 2026-07 | +0.0 | +4.0 | +6.2 | +5.0 | +16.0 | +5.5 | -3.2 | **+33.5** |
| 2026-08 | +6.3 | +4.0 | +15.5 | +3.0 | +0.0 | -2.2 | +3.6 | **+30.2** |
| 2026-09 | -0.1 | -5.0 | +4.8 | +6.0 | -2.0 | +0.2 | +0.0 | **+3.9** |

## 4. Live forward test

**Status: running since 2026-10-29 17:19 (VPS, server+1)** — no scored closes yet; run the update procedure below.

Update procedure (from `infra/`):

```bat
python -m src.diversify.run_p2_scorer --log ..\..\..\..\logs\hosting.6917926.experts --from <go-live YYYY-MM-DD> --out artefacts\live_scorecard\LIVE --archive ..\blotter\archive\LIVE-SCORECARD-LIVE
python -m src.diversify.live_scorecard
```

## 5. Adding symbols

1. Add a `LiveRunCard` (magic, RR, BWR, Leak, `risk_pct`) to `infra/src/diversify/live_runs.py`.
2. Generate its LIVE-SHADOW preset (`blotter/archive/LIVE-SHADOW-PRESETS/_make_presets.py` from a VPS input dump).
3. Back-test it on the scorecard window into the same log, re-run `run_p2_scorer --out artefacts\live_scorecard\BT_SHADOW`, then `live_scorecard`.

## Sources

- Backtest logs: `blotter/archive/LIVE-SHADOW-PRESETS/tester_{SHADOW,CURRENT}_v128.log`
- Scored artefacts: `infra/artefacts/live_scorecard/BT_SHADOW`, `BT_CURRENT`, `LIVE_SCORECARD.json`
- Presets: `Presets/LIVE-SHADOW_*.set` (full 120 inputs from VPS dump 2026-10-28 23:00)
