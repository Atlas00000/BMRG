# JP225-AOS-P7 — Tester confirm (magic 26151907)

**Date:** 2026-10-19  
**Preset:** `JPN225stack` · Leak inp **2.45** · AOS ON · JP L2det ON  
**Log:** `Tester/logs/20261019.log`  
**Artefact:** `TESTER_REVIEW.json`

## Runs found (3)

| Window | n | WR% | E_N | EF_pp | Δ$ | MaxDD% | L2det | L3 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- | ---: |
| Jan→Apr (pre-tip) | 50 | 40.0 | 0.00 | **−2.45** | −0.27 | 2.4 | none (no May/Jul) | 16 |
| **May→Aug tip ★** | **43** | **53.5** | **+0.34** | **+11.0** | **+22.15** | **1.5** | May24+Jul15 | 0 |
| Sep→Oct 18 | 26 | 46.2 | +0.15 | **+3.7** | +5.78 | 1.2 | none | 0 |

## Tip vs engine (26101904 AOS OFF)

| | Engine P1 | **JPN225stack** |
| --- | ---: | ---: |
| n | 79 | **43** |
| WR | 43.0% | **53.5%** |
| EF (meas 2.45) | +0.59 | **+11.0** |
| Δ$ | +9.28 | **+22.15** |
| MaxDD proxy | 3.7% | **1.5%** |

Matches offline May∨Jul keep (n=43 · WR 53.5%). MQH wire **live** (`L2DET_SKIP_MAY` / `L2DET_SKIP_JUL`).

**Verdict:** tip path **PASS** · stack confirmed.
