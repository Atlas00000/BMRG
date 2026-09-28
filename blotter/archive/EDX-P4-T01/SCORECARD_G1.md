# EDX-P4-T01 — G1 production gate (currency champion)

**Scored:** 2026-09-25 10:33  
**Preset:** `EDX-P4-T01_champion_T05_currency_G0_long.set`  
**Magic:** 8210401  
**Deposit:** 400.00 USD · **Final:** 620.63 USD · every tick · 2025.01.01→2026.09.24  

## Contract (G0)

| Check | Result |
| --- | --- |
| Account currency PnL | **PASS** (not pips) |
| G0 geometry MaxLevels/Entries=1 | PASS |
| Hard SL 300 / TP 450 | PASS (1R = $3.00 @ 0.01 lot) |
| n ≥ 385 Standard | **420** PASS |
| preset_id / magic match | PASS |

## Health vector

| Metric | Value |
| --- | ---: |
| n | 420 (199 TP / 221 SL) |
| WR | **47.38%** |
| AW / AL | $4.50 / $3.00 |
| R / RR / RR−R | **1.500 / 1.500 / 0** |
| BWR | 40% |
| BM | **+7.38 pp** |
| mean entry spread | 5.51 pts |
| c_R (3×spread/300) | 0.0551 |
| Leak (L1 proxy) | **2.21 pp** |
| EF | **+5.18 pp** |
| M | ±4.78 pp |
| E_N | **+0.185R** |
| Zone | **Robust** |
| Price-path ΣPnL | $232.50 |
| Account net | +$220.63 (residual friction ~$11.87 → alt Leak ≈0.38 pp) |

## G1 checks

| Rule | Result |
| --- | --- |
| EF > M (full) | 5.18 > 4.78 **PASS** |
| EF > M (latest W500 ≡ full, n=420) | **PASS** |
| WR > BWR+Leak (42.21%) | 47.38% · z≈2.15 **PASS** |
| Bootstrap R p05 | 1.50 **PASS** |

## Verdict

**G1 PASS**

Artifacts: `tester_segment_currency.log`, `events_currency.csv`
