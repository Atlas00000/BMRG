# GRP-PRIMARY-CF — JP225 50% · DE40 50%

**Verdict:** **PASS** — tip re-test matches frozen GRP-P5 primary exactly  
**Source:** `Tester/logs/20261022.log` · window `2026.05.01→2026.10.20`  
**Generated:** 2026-10-22

## Tester passes

| Sleeve | Symbol | Magic | n | final balance (acct) | Test clock |
| --- | --- | ---: | ---: | ---: | --- |
| JP225 | JPN225 M5 | 26161907 | 72 | 543.09 USD | ~15:16 |
| DE40 | DE30 M5 | 26151907 | 112 | 756.18 USD | ~15:17 |

Account equity is path-dependent; **designed R** is the cluster authority.

## Sleeve designed R (tip)

| Sleeve | sum_R | E_N | WR | maxDD_R | m_hit | q_hit |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| JP225 | +30.0 | 0.42 | 47% | −4.0 | 67% | 100% |
| DE40 | +32.0 | 0.29 | 57% | −7.0 | 83% | 67% |

## Equal-weight cluster vs frozen

| Metric | This CF | Frozen P5 | Δ |
| --- | ---: | ---: | ---: |
| sum_R | **+31.0** | +31.0 | 0 |
| month_hit | **100%** | 100% | 0 |
| quarter_hit | **100%** | 100% | 0 |
| E_month | **5.17** | 5.17 | 0 |
| CVaR_m20 | **1.50** | 1.50 | 0 |
| maxDD | **−2.50** | −2.50 | 0 |
| worst_month | **+0.63** | +0.63 | 0 |
| co_loss | **0.041** | 0.041 | 0 |
| Sep–Oct val_sum_R | **+3.0** | +3.0 | 0 |
| boot month hit_p10 | **100%** | 100% | 0 |
| fuse triggers | **0** | 0 | 0 |

## Notes

- Semver WARN on both (input DISARM label vs baked L2det) — baked coeffs used; same as prior tip panel.
- AOS ledger FileOpen 5004 in Tester — non-blocking for tape parse.
- No live `f` raise from this CF alone.
