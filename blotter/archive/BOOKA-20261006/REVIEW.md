# BOOKA-20261006 — Harvest extract (asset expansion, not live replace)

**Lens:** Expand the **research asset list** under Book A · engine-only · **AOS OFF**.  
**Not** a replacement for live INF / `8210204` on EURUSD. Per-symbol AIOS comes later.  
**Source:** Tester `logs/20261006.log`  
**Reviewed:** 2026-10-06 (reframed same day)  
**Expert:** BMRG.ex5 · magics **8221101–03** · deposit $400 · every tick · ACCOUNT CURRENCY  
**Geometry:** BB(20,2.2) · SL/TP **300 pts** (EURUSD-calibrated transfer) · session 12–20 · skip Tue

## Results (primary Jan→Oct 2026 unless noted)

| Symbol | Magic | Window | Final | PnL | Opens | Expansion read |
| --- | ---: | --- | ---: | ---: | ---: | --- |
| EURUSD | 8221101 | Jan→Oct | 516.75 | **+116.75** | 204 | Strong **geometry confirm** on home symbol (research magic, not live pin) |
| EURUSD | 8221101 | May→Oct | 462.92 | +62.92 | 100 | Holds on shorter window |
| AUDUSD | 8221103 | Jan→Oct | 432.18 | +32.18 | 168 | **Keep in expansion queue** — thin but positive; regime/points may still be off |
| AUDUSD | 8221103 | May→Oct | 428.40 | +28.40 | 73 | Small-n support |
| GBPUSD | 8221102 | Jan→Oct | 394.62 | **-5.38** | 256 | **Not cut** — treat as **regime / ATR-points mismatch** until retune; May→Oct was +14 |
| GBPUSD | 8221102 | May→Oct | 414.18 | +14.18 | 131 | Path exists off full-window noise |

With AOS off: OPEN lines only — WR/E_N need deal export. Approx R=1 from PnL: EUR ~+0.18R · AUD ~+0.05R · GBP ≲0 on full window.

## Framing (do / don’t)

| Do | Don’t |
| --- | --- |
| Score each symbol as an **expansion candidate** | Treat Book A as live champion swap |
| Expect **point/ATR regime mismatch** on non-EUR transfers | Hard-reject GBP solely on raw Jan→Oct equity |
| Plan **per-symbol AIOS** after engine extract clears Stage gates | Mix magics with `8210204` / INF LIVE_WITHHOLD blotters |
| Keep EUR live path unchanged | Stack EUR/GBP/AUD as “diversified” Stage-3 capital (USD cluster) |

## Expansion queue (next)

1. **EURUSD 8221101** — export deals → Stage-1 EF/Leak (calibration baseline for the book).  
2. **AUDUSD 8221103** — same scorecard; optional mild SL/TP ATR scale if Leak fails.  
3. **GBPUSD 8221102** — **retune first** (ATR-scaled points or BBDev), then re-test; do not discard the asset.  
4. After engine ACCEPTs: design **per-symbol AIOS** (own pin / withhold), not a copy-paste of EUR L2.

## Live boundary

Live FT remains **EURUSD · magic 8210204 · INF LIVE_WITHHOLD**. Book A does not change that attach.
