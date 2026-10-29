# DIV-P2 — Live-preset long-run runcard

**Goal:** Re-test each live sleeve once on the **tip 6m** window, then score **monthly / quarterly** rollups — without re-running Tester per month.  
**Consumes into:** [`asset_grouping_roadmap.md`](./asset_grouping_roadmap.md) (GRP-P0 daily panel / enum)

**Scorer:** `python -m src.diversify.run_p2_scorer` (from `infra/`)  
**Cards:** `infra/src/diversify/live_runs.py`  
**Outputs:** `infra/artefacts/diversify/P2_LATEST/` · `blotter/archive/DIV-P2-T01/`

---

## 1. Tester recipe (each sleeve)

| Setting | Value |
| --- | --- |
| Expert | `Experts\BMRG\BMRG.ex5` |
| Model | Every tick (or 1-min OHLC if agreed — footnote) |
| Deposit / mode | ACCOUNT CURRENCY |
| Window | **2026.05.01 → 2026.10.20** (tip 6m · primary panel) |
| One pass | **One chart / one preset / one magic** per run — do not merge tip+long |
| Halt | Leave live fuse ON (as-traded); ddl review is a later ops task |

### Live presets to run

| Asset | Symbol | TF | Magic | Preset |
| --- | --- | --- | ---: | --- |
| EURUSD | EURUSD | M5 | **8210204** | `INF-LIVE_WITHHOLD_Harvest_long_ddl30.set` |
| AUDUSD | AUDUSD | M5 | **8230931** | `AUDUSD-AIOS_SCALE_Risk3_champ_G0.set` |
| AAPL | Apple | M5 | **26162017** | `AAPL_5m_stack.set` |
| UK100 | UK100 | M5 | **26121907** | `UK100_5m_stack.set` |
| JP225 | JPN225 | M5 | **26161907** | `JPN225_5m_stack.set` |
| DE40 | DE30 | M5 | **26151907** | `DE40_5m_stack.set` |
| USDJPY | USDJPY | M15 | **26131807** | `USDJPYstack.set` |

Load the `.set` from `Presets/` or `Profiles/Tester/BMRG/` / `doc/presets/` twin.

---

## 2. Score (segment long run)

After each run (or after all seven), from `infra/`:

```bat
python -m src.diversify.run_p2_scorer --log ..\..\..\Tester\logs\YYYYMMDD.log
rem or drop logs into blotter\inbox\ then:
python -m src.diversify.run_p2_scorer --inbox
```

Multiple `--log` flags are fine — scorer merges by magic / asset.

### What you get without re-testing

| Layer | Source |
| --- | --- |
| Trade tape | OPEN → AOS close TP/SL · designed `pnl_R` from SL/TP |
| Full + each **M / Q / Y** bucket + trailing **30/60/90/180/365d** | Full metrics pack below |
| Flat CSVs | `PERIOD_TABLE_{M,Q,Y}.csv` — one row per asset×period |
| Hit matrices | rich cells: sum_R · E_N · WR · EF · maxDD · streak |

### Metrics pack (every rolling window)

| Group | Fields |
| --- | --- |
| **Counts** | n · wins · losses · scratches · calendar_days · active_days · trades_per_30d |
| **Expectancy** | WR · WR_wilson_low · E_N · sum_R · median_R · std_R · best/worst_trade_R · avg_win_R · avg_loss_R · R_realised · designed_RR · profit_factor_R |
| **Edge** | BWR · BM_pp · Leak_pp · EF_pp · EF_zone · EF_gt_0 · WR_wilson_gt_BWR |
| **Path** | maxDD_R · max_loss/win_streak · max_neg_day_streak · pos/neg days · day_hit_rate · best/worst/mean/std day_R · CVaR_day_20 |
| **Mix** | exit_TP/SL/MID · buy/sell n · buy/sell WR · buy/sell E_N |
| **Friction** | hold_h mean/median/p90 · spread_pts median/p90 |
| **Period rollup** | hit_rate · mean/median E_N · mean EF · CVaR_period_20 · worst/best period id · pct_EF_gt_0 · pct_below_frontier |

`positive_cycle` = `sum_R > 0` for that window (used in cluster month/quarter hit-rate).

---

## 3. Into asset grouping (GRP-P0)

When all seven sleeves are present in `P2_LATEST/sleeves/*_live_fire_tape.csv`:

1. Build daily \(R_{i,t}\) panel from those tapes.  
2. Exhaustive enum k=2…5 under equal weight → acceptable **range** of groups.  
3. See [`asset_grouping_roadmap.md`](./asset_grouping_roadmap.md) phases GRP-P0…P5.

---

## 4. Why not one Tester run for all symbols?

MT5 Strategy Tester is single-symbol. Run **seven tip-6m passes** (same dates). The scorer stitches them. Live VPS hosting logs can smoke-test the parser but are **not** a history substitute.
