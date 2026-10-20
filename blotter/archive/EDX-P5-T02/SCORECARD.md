# EDX-P5-T02 — Stack tip May→Oct

**Scored:** 2026-10-07  
**Preset:** `EDX-P5-T02_stack_start13_skipMon_G0_AUDUSD-M5_MayOct.set`  
**Identity (run 25):** magic **8230502** · StartHour **13** · TradeMon **false** · SL/TP **300/300** · **2026.05.01 → 2026.10.06**

## Health vector vs tip baseline

| Metric | P0-T04 tip | **P5 stack tip** | Δ |
| --- | ---: | ---: | ---: |
| n | 73 | **61** | −12 |
| WR | 56.2% | **60.7%** | +4.5 pp |
| E_N | +0.123R | **+0.213R** | +0.090R |
| EF* | −1.34 | **+3.16** | +4.50 |
| M (Wilson) | — | ±11.91 | — |
| Zone* | Negative | **Fragile** | EF&gt;0 but EF&lt;M |
| PnL | +27.80 | **+39.10** | +11.30 |
| hour12 / Mon | — | **0 / 0** | — |

\*Leak proxy `costs_defaulted`. vs May→Aug stack (T01): E_N diluted −0.191R (expected tip tax).

## Tip cells (L3)

| Month | n | WR | E_N | Read |
| --- | ---: | ---: | ---: | --- |
| 2026-05…08 | 48 | ≥66.7% | all &gt;0 | primary holds |
| **2026-09** | 11 | **18.2%** | **−0.636R** | **L3 wipeout** (worse than P0 Sep) |
| 2026-10 | 2 | 50% | 0.0 | thin |

## Verdict

**ACCEPT_TIP** — full-window E_N&gt;0 · beats P0-T04 on E_N/EF/pnl · not wipeout.  
Sep remains **L3**; stack does not fix tip regime (hygiene only). May→Aug champion sleeve unchanged.

## Next

**EDX-P6-T01** — freeze stack on long window `2026.03.23 → 2026.09.21`.
