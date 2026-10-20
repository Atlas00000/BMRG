# EDX-P6-T01 — Freeze candidate long window

**Scored:** 2026-10-07  
**Preset:** `EDX-P6-T01_candidate_G0_AUDUSD-M5_long.set`  
**Identity (run 27):** magic **8230601** · StartHour **13** · TradeMon **false** · SL/TP **300/300** · **2026.03.23 → 2026.09.21**

## Health vector

| Metric | P0 May→Aug | P5 stack May→Aug | **P6 freeze long** |
| --- | ---: | ---: | ---: |
| n | 58 | 47 | **73** |
| n_tier | Insufficient | Insufficient | **Insufficient** (&lt;100) |
| WR | 62.1% | 70.2% | **57.5%** |
| E_N | +0.241R | +0.404R | **+0.151R** |
| EF* | +4.57 | +13.21 | **+0.53** |
| M | ±12.1 | ±12.7 | **±11.06** |
| Zone* | Fragile | Robust* | **Fragile** |
| PnL | +44.39 | +57.10 | **+35.77** |
| hour12 / Mon | — | 0 / 0 | **0 / 0** |

\*Leak proxy. G1 proxy: EF &lt; M → **FAIL**.

## Months

| Month | n | WR | E_N |
| --- | ---: | ---: | ---: |
| 2026-03 | 3 | 0% | −1.000 |
| 2026-04 | 15 | 40% | −0.200 |
| 2026-05…08 | 48 | ≥66.7% | all &gt;0 |
| 2026-09 | 7 | 28.6% | −0.429 |

## Verdict

**ACCEPT_FREEZE** — E_N&gt;0 on protocol long window; freeze recorded.  
Not production-eligible: n_tier Insufficient · Fragile · early months + Sep dilute May→Aug edge.
