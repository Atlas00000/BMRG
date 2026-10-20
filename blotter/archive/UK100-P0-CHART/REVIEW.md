# UK100-P0-CHART — expand-book review (not live)

**Preset:** `Profiles/Tester/BMRG/UK100/BMRG-M15-UK100-6M-P0_balanced_chart.set`  
**Log:** `Tester/logs/20261012.log`  
**Frame:** asset-list expansion research · AOS OFF · not a live replacement  
**Deposit:** 500 USD · magic 26101201 · G0

## Geometry (confirmed in log)

| Input | Value |
| --- | --- |
| SL / TP | 2500 / 3125 (RR 1.25, TP>SL) |
| BB | 20 / 2.2 |
| Session | 08–17 · Tue off |
| ATR regime | ON · max 1470 |
| Lot | 0.1 (broker min) |
| AOS | OFF |

First OPEN lines match designed SL/TP distances exactly.

## Rolling windows (closed TP/SL excl. EOT)

| Window (requested) | Effective hist | n | WR | Final | Net vs 500 | E_N† | EF† |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 2026.05.01 → 08.31 | full tip | 51 | **49.0%** | 517.14 | **+3.4%** | +0.103R | +1.7pp |
| 2026.01.01 → 04.30 | from ~Dec17 tip | 75 | 45.3% | 504.48 | +0.9% | +0.020R | −2.0pp |
| 2024.01.01 → 08.31 | **hist from 2025.12.17** | 131 | 45.8% | 510.97 | +2.2% | +0.031R | −1.5pp |

† Design R=1.25, BWR=44.4%, Leak prior 2.9pp (not blotter-measured c_R).

## Monthly WR (design tip + prior)

| Month | n | WR | Note |
| --- | ---: | ---: | --- |
| 2025.12 | 4 | 25% | tip start / thin |
| 2026.01 | 31 | 48% | |
| 2026.02 | 23 | **35%** | main prior drag |
| 2026.03 | 6 | 50% | thin |
| 2026.04 | 15 | 53% | |
| 2026.05 | 9–10 | 50–56% | MATCH home |
| 2026.06 | 11 | 55% | MATCH home |
| 2026.07 | 7 | **29%** | MATCH tag but local fail |
| 2026.08 | 24 | 50% | MATCH strongest · high fire count |

## Gate behaviour

Session / weekday / ATR blocks dominate (healthy). Pause/fail rare. Spread rarely blocking (maxSpread 200 vs ~120–140).

## Verdict

**KEEP_RESEARCH / EXPAND_CANDIDATE** — not live, not AIOS yet.  
Design May–Aug window clears BWR with thin positive EF; Jan–Apr and long composite diluted by regime-mismatch months (esp. Feb, Jul). Long “2024” run is truncated by broker history → do not treat as multi-year evidence.
