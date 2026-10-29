# DIV-P2-T01 — Live-preset long-run scorer

**generated_utc:** 2026-10-22T14:22:27.236054+00:00
**sources:** 20261022.log
**trades:** 573
**sleeves:** AAPL, AUDUSD, DE40, EURUSD, JP225, UK100, USDJPY
**panel:** 2026-05-01 → 2026-10-20 (match_tester_window=True)

## How segmentation works

One Tester window per live preset is enough (tip 6m or longer).
Each closed trade keeps `close_time`; the scorer buckets into calendar
months / quarters / years and trailing 30/90/365d — no per-month re-run.
Use `--match-tester-window` with `--from/--to` when the journal also
contains older longer passes.

## Sleeve rollup

| Asset | n | month_hit | q_hit | full E_N | full EF | maxDD_R | worst_month |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| AAPL | 46 | 0.4 | 0.6667 | 0.3444 | -1.352 | -4.0 | 2026-06 |
| AUDUSD | 63 | 0.6667 | 0.6667 | 0.2063 | 7.917 | -10.0 | 2026-09 |
| DE40 | 112 | 0.8333 | 0.6667 | 0.2857 | 5.743 | -7.0 | 2026-10 |
| EURUSD | 110 | 0.8333 | 0.6667 | 0.1818 | 6.891 | -5.0 | 2026-10 |
| JP225 | 72 | 0.6667 | 1.0 | 0.4167 | 10.622 | -4.0 | 2026-08 |
| UK100 | 121 | 0.6 | 1.0 | 0.1715 | 1.736 | -5.75 | 2026-08 |
| USDJPY | 49 | 0.8 | 1.0 | 0.302 | 2.284 | -5.4 | 2026-07 |

## Artefact tables

- `ROLLING.json` — full metrics pack per sleeve × M/Q/Y + trailing 30/60/90/180/365d
- `PERIOD_TABLE_{M,Q,Y}.csv` — flat rows for notebooks / cluster features
- `HIT_MATRIX_{M,Q,Y}.json` — rich cell: sum_R · E_N · WR · EF · maxDD · streak

## Next

1. Tip panel complete (7/7).
2. P2-T02: point `manifest.py` tapes at `P2_LATEST/sleeves/*_live_fire_tape.csv`.
3. `python -m src.diversify.run_mvp` then `run_p1` for cluster / adverse dependence.

Artefacts: `infra\artefacts\diversify\P2_LATEST/` · archive `blotter\archive\DIV-P2-T01/`
