# EDX-P5-T01 — Stack StartHour13 + skip Mon

**Scored:** 2026-10-07  
**Preset:** `EDX-P5-T01_stack_start13_skipMon_G0_AUDUSD-M5_MayAug.set`  
**Identity (run 21):** magic **8230501** · StartHour **13** · TradeMon **false** · SL/TP **300/300** · May→Aug  
**Note:** A later 8230501 run used Start=12/Mon=true (P0 clone) — **ignored**.

## Health vector

| Metric | P0 | P3-T02 (Start13) | **P5 stack** |
| --- | ---: | ---: | ---: |
| n | 58 | 57 | **47** |
| WR | 62.1% | 68.4% | **70.2%** |
| E_N | +0.241R | +0.368R | **+0.404R** |
| EF* | +4.57 | +11.42 | **+13.21** |
| M (Wilson) | ±12.1 | — | ±12.66 |
| Zone* | Fragile | — | **Robust*** |
| PnL | +44.39 | +62.90 | **+57.10** |
| hour12 / Mon | 24 / 13 | 0 / 11 | **0 / 0** |

\*Leak proxy `costs_defaulted`. Robust = EF>M on this sample; n still **Insufficient** (&lt;100) for production G1.

## Verdict

**ACCEPT_STACK** — beats P0 **and** P3-T02 on E_N/EF.  
Slight $ below T02 alone (−$5.80) but higher expectancy / WR; freq 81% of P0 (no stall).

**Champion expansion sleeve (May→Aug):** StartHour=13 + skip Mon + SL300/TP300 · mag 8230501.

## Next

1. **EDX-P5-T02** — same stack on tip window May→Oct (regime survival).  
2. Then **EDX-P6-T01** freeze candidate on long window for gate path.
