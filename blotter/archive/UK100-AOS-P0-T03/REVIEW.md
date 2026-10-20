# UK100-AOS-P0-T03 — journal Leak proxy + tip fire tape

**Date:** 2026-10-12  
**Window:** 2026.05.01 → 2026.08.31 · magic 26101201 · AOS OFF  
**Log:** `Tester/logs/20261012.log` (UK100 tip run only)  
**Artifacts:** `COST_PROXY.json` · `uk100_tip_fire_tape.csv` · builder script  

## Leak / EF (journal proxy)

| Metric | Value |
| --- | ---: |
| n | 51 |
| WR / BM | 49.0% / +4.58 pp |
| E_N | +0.103R |
| Entry spread | **120 pts** (all fires; med=mean) |
| `c_R` (2×spread/SL) | 0.096R |
| **Leak_proxy** | **4.27 pp** |
| **EF_proxy** | **+0.31 pp** |
| Leak_prior (design) | 2.9 pp |
| EF_prior | +1.68 pp |
| Zone | **Fragile** (EF ≪ M) |

**Read:** Journal 2×entry-spread is **stricter** than design prior (160 RT pts). Tip still EF>0 but thinner. Still **not** full deal-measured Leak (no exit spread / commission / swap).

## Tape

51 labeled fires written for P1 (side, DOW, hour, ATR, spread, bad-cell flags, ouroboros month tag).

## Verdict

`Leak_source=journal_2x_entry_spread_median` accepted as interim for OS shadow CF.  
`Leak_source=measured` remains **OPEN** until deals.csv export.
