# EDX-P2-T02 — SL200 / TP300 (RR=1.5 held)

**Scored:** 2026-09-25 12:00  
**Preset:** `EDX-P2-T02_SL200_TP300_RR1.5_champFilters_G0_long.set`  
**Magic:** 8210202 · champ filters · **currency**  
**Window:** **2026.07.01 → 2026.09.24** (3M recent stress; Sep truncated by design)

## Inputs verified

SL=200, TP=300 → R=1.5, StartHour=12, TradeTue=false ✓

## Health vector (3M)

| Metric | T02 | T01 same 3M | Balanced long (ref) |
| --- | ---: | ---: | ---: |
| n | 61 | 43 | 420 |
| WR | **44.3%** | 32.6% | 47.4% |
| BWR | 40.0% | 30.8% | 40.0% |
| BM | +4.3 pp | +1.8 | +7.4 |
| Leak L1 | 3.31 | ~2.5 | 2.21 |
| EF | **+0.96** | −0.75 | +5.18 |
| E_N | **+0.107R** | +0.058 | +0.185 |
| M | ±12.5 | ±14 | ±4.8 |
| Zone | Fragile | Negative | Robust* |
| Final | **$414.65** | $406.52 | $620.63 |

## Pool verdict

**POOL_KEEP** (provisional / `thin` — n=61 &lt; 100)  
- E_N > 0 · WR > BWR · EF > 0  
- Same 3M window: **beats Survival T01** on WR, EF, E_N, final  
- Role: **Balanced-scale** (RR=1.5 kept, tighter stops) — recent sleeve healthier than stretched RR=2.25

Long-window admission still recommended when convenient (n≥385 for gates).

## Interpretation

Holding RR=1.5 while cutting stop scale **preserves the breakeven frontier at 40%** and recovered WR into the mid-40s on this late-2026 stress window — unlike T01’s high-R / low-WR path that went EF-negative here.
