# LIVE-SHADOW-PRESETS — shadow presets, Jan–Sep 2026 backtests, EA 1.28

**task_id:** LIVE-SHADOW-PRESETS · **date:** 2026-10-29  
**verdict:** **PRESETS READY · EA 1.28 REQUIRED (1.27 deadlock) · scorecard published** → `doc/LIVE_SCORECARD.md` + canvas `live-scorecard.canvas.tsx`

## Presets

`_make_presets.py` builds every preset from the VPS input dump (`vps_inputs_20261028_2300.json`, 120 inputs per chart) — the repo `.set` files omitted 23–55 inputs and had no file for live AUDUSD `8230931` @3%.

| Chart | LIVE-SHADOW preset | Changes vs live |
| --- | --- | --- |
| EURUSD M5 8210204 | `LIVE-SHADOW_EURUSD_M5.set` | `InpAiOsMode` 2→1 · `InpLogGateBlocks` false→true |
| AUDUSD M5 8230931 | `LIVE-SHADOW_AUDUSD_M5.set` | same |
| Apple M5 26162017 | `LIVE-SHADOW_Apple_M5.set` | `InpAiOsMode` 2→1 |
| UK100 M5 26121907 | `LIVE-SHADOW_UK100_M5.set` | same |
| JPN225 M5 26161907 | `LIVE-SHADOW_JPN225_M5.set` | same |
| DE30 M5 26151907 | `LIVE-SHADOW_DE30_M5.set` | same |
| USDJPY M15 26131807 | `LIVE-SHADOW_USDJPY_M15.set` | same |

Copies: `Presets/`, `doc/presets/`, `Profiles/Tester/BMRG/`. Baseline twins `LIVE-CURRENT_*.set` (exact live, Tester only). `INF-SHADOW_Harvest_long_ddl30.set` (partial inputs) is superseded by `LIVE-SHADOW_EURUSD_M5.set`.

## EA 1.27 deadlock → 1.28

First batch on 1.27: UK100 dark from 11 Feb, DE30 from 20 Feb, JP225 from mid-Jun, Apple from 12 Aug (`AOS f_rec=0 (Below)` forever).  
Cause: dual-window BELOW sets life=BELOW → f=0; soft-derisk used `MathMin(f, 0.25)` = 0 → no entries → no confirming close → hard halt + 500-bar probe never reached. Introduced when 1.26 moved the BELOW streak to closes-only.  
Fix (`Include/AOS.mqh`): while confirming, `f = 0.25` unless an L3 MaxDD halt is active. Compiled **1.28** (0 errors / 0 warnings). Re-run: `f_rec=0` blocks 0 on all sleeves; all trade to late Sep.  
Evidence: `tester_{SHADOW,CURRENT}_v127_20261029.log`.

## Backtests (1.28)

`_run_tester.ps1` (headless terminal64 `/config`, every tick, $500, 1:500, 2026.01.01→2026.09.30) · `_split_runs.py` → `tester_{SHADOW,CURRENT}_v128.log` · scored with `run_p2_scorer --out artefacts/live_scorecard/BT_*` (new `--out/--archive` flags) · `live_scorecard.py` → JSON + MD.

| Book (equal R) | ΣR | maxDD R | Month hit |
| --- | ---: | ---: | ---: |
| All LIVE-SHADOW | +87.7 | −22.0 | 78% |
| All current inputs | +134.7 | −24.5 | 78% |
| **Deployed mix** (shadow EUR/UK/DE/AUD · skips kept AAPL/JP/USDJPY) | **+131.5** | **−21.5** | 78% |

(First draft reported +72.5 / +119.6 — portfolio panel dropped weekend closes; fixed to calendar days.)

## Operator decision (2026-10-29)

**Load folder:** `MQL5/Profiles/Tester/BMRG/live/` holds exactly the 7 deploy presets; comparison twins stay in `Profiles/Tester/BMRG/` (`_make_presets.py` and `_run_tester.ps1` handle both).

SHADOW: EURUSD, UK100, DE30, AUDUSD → load `LIVE-SHADOW_*.set`. Keep current inputs (skips enforced): Apple, JPN225, USDJPY — no preset reload, EA 1.28 only. Encoded as `deploy` in `infra/src/diversify/live_runs.py`.

Skip layers add +47R, mainly L2det on AAPL (+20.6), JP225 (+17.0), USDJPY (+6.2) and AUD L2 AI (+6.0) — all fitted on overlapping data (in-sample). EURUSD/UK100 identical (no skip fired; EUR max p 0.576).
