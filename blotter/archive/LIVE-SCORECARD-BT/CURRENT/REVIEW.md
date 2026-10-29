# CURRENT — Live-preset long-run scorer

**generated_utc:** 2026-10-29T15:36:08.890334+00:00
**sources:** tester_CURRENT_v128.log
**trades:** 886
**sleeves:** AAPL, AUDUSD, DE40, EURUSD, JP225, UK100, USDJPY
**panel:** 2026-01-01 → 2026-09-30 (match_tester_window=False)

## How segmentation works

One Tester window per live preset is enough (tip 6m or longer).
Each closed trade keeps `close_time`; the scorer buckets into calendar
months / quarters / years and trailing 30/90/365d — no per-month re-run.
Use `--match-tester-window` with `--from/--to` when the journal also
contains older longer passes.

## Sleeve rollup

| Asset | n | month_hit | q_hit | full E_N | full EF | maxDD_R | worst_month |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| AAPL | 71 | 0.625 | 0.6667 | 0.1497 | -9.221 | -7.1053 | 2026-02 |
| AUDUSD | 100 | 0.5556 | 0.6667 | 0.1 | 2.6 | -9.0 | 2026-02 |
| DE40 | 170 | 0.7778 | 1.0 | 0.2176 | 2.718 | -10.0 | 2026-02 |
| EURUSD | 173 | 0.6667 | 1.0 | 0.1676 | 6.182 | -8.0 | 2026-04 |
| JP225 | 85 | 0.4444 | 0.6667 | 0.0941 | -0.129 | -15.0 | 2026-04 |
| UK100 | 236 | 0.5556 | 1.0 | 0.125 | -0.33 | -7.75 | 2026-08 |
| USDJPY | 51 | 0.7143 | 1.0 | 0.2078 | -1.998 | -6.4 | 2026-07 |

## Artefact tables

- `ROLLING.json` — full metrics pack per sleeve × M/Q/Y + trailing 30/60/90/180/365d
- `PERIOD_TABLE_{M,Q,Y}.csv` — flat rows for notebooks / cluster features
- `HIT_MATRIX_{M,Q,Y}.json` — rich cell: sum_R · E_N · WR · EF · maxDD · streak

## Next

1. Tip panel complete (7/7).
2. P2-T02: point `manifest.py` tapes at `P2_LATEST/sleeves/*_live_fire_tape.csv`.
3. `python -m src.diversify.run_mvp` then `run_p1` for cluster / adverse dependence.

Artefacts: `infra\artefacts\live_scorecard\BT_CURRENT/` · archive `blotter\archive\LIVE-SCORECARD-BT\CURRENT/`
