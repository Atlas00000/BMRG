# GRP-ALT-MINMAXDD-CF — EURUSD+DE40+USDJPY+AAPL (25% each)

**Verdict:** **PASS_EXTENDED_AAPL_TIP**  
**Splice:** EUR / DE40 / USDJPY = Jan–Oct · **AAPL = May–Oct tip** (halt avoided)  
**Source:** `Tester/logs/20261022.log`  
**Generated:** 2026-10-22

## Why splice

Jan–Oct AAPL M5 halted after Apr (sum_R −5.5, dark May–Oct). Operator re-ran **Apple M5 · 26162017 · 2026.05.01→2026.10.20** (final balance 531.18). Prior halt tape kept as `sleeves/AAPL_live_fire_tape_jan_apr_halt.csv`.

## Sleeve designed R

| Sleeve | Window | n | sum_R |
| --- | --- | ---: | ---: |
| EURUSD | Jan–Oct | 214 | +36.0 |
| DE40 | Jan–Oct | 190 | +41.8 |
| USDJPY | Jan–Oct | 55 | +15.4 |
| AAPL | **May–Oct tip** | 46 | **+15.8** |

## Equal-weight cluster

| Metric | AAPL tip splice | Prior (AAPL halt) | Tip freeze May–Oct |
| --- | ---: | ---: | ---: |
| sum_R | **+27.2** | +21.9 | +20.7 |
| month_hit | **90%** (9/10) | 90% | 100% |
| E_month | **2.72** | 2.19 | 3.44 |
| CVaR_m20 | **−0.02** | −0.71 | 1.41 |
| maxDD | **−1.44** | −2.58 | −1.13 |
| worst_month | **−0.19** (Feb) | −1.58 (Feb) | — |
| best_month | **+6.79** (Aug) | +5.21 (Aug) | — |
| Sep–Oct | **+2.81** | +2.85 | +2.81 |
| boot hit p10 | **80%** | 80% | — |
| fuse | **0** | 0 | 0 |

Δ vs halt version: **+5.3R** from AAPL tip contribution.

## Monthly (group equal 25%)

| Month | Group | EUR | DE40 | USDJPY | AAPL | Hit |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| Jan | +2.36 | −1.00 | +9.25 | +1.20 | 0 | Y |
| Feb | **−0.19** | +5.00 | −5.75 | 0 | 0 | N |
| Mar | +2.55 | +10.00 | −1.00 | +1.20 | 0 | Y |
| Apr | +2.36 | +3.00 | +8.25 | −1.80 | 0 | Y |
| May | +4.25 | 0 | +3.00 | +4.20 | **+9.79** | Y |
| Jun | +3.39 | +7.00 | +1.25 | +5.40 | −0.11 | Y |
| Jul | +2.93 | +5.00 | +7.50 | −0.80 | 0 | Y |
| Aug | **+6.79** | +2.00 | +15.25 | +3.60 | **+6.32** | Y |
| Sep | +2.66 | +6.00 | +4.75 | 0 | −0.11 | Y |
| Oct | +0.15 | −1.00 | −0.75 | +2.40 | −0.05 | Y |

## Read

- Halt-avoid AAPL tip **cleans** Feb drag and lifts Aug; path closer to tip freeze maxDD.
- Still **9/10** months · bootstrap floor **~8/10**.
- AAPL remains light attach (EF Below history); Jan–Apr is intentionally empty in this splice.
- No live `f` raise.
