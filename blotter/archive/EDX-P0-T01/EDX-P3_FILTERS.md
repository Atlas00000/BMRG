# EDX-P3 filter results vs P0

**Scored:** 2026-09-25 ~10:19–10:21  
**Window:** 2025.01.01–2026.09.24 (match P0)  
**Mode:** still pips / deposit 400 (`costs_defaulted`; Leak proxy **2.24 pp**)  
**P0 beat bar:** E_N ≥ 0.1184R, EF ↑ vs 2.50 pp, freq ≥ 50%

| Preset | Magic | Opens | n | WR | BM | E_N | EF (Leak 2.24) | M | Zone | Final pips | vs P0 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- | ---: | --- |
| **P0 baseline** | 8210001 | 572 | 570 | 44.74% | +4.74 | +0.118R | +2.50 | ±4.08 | Fragile | 591.23 | — |
| P3-T01 session 12–20 | 8210301 | 470 | 469 | 43.71% | +3.71 | +0.093R | +1.47 | ±4.49 | Fragile | 515.25 | **REJECT** |
| P3-T02 skip Tue | 8210302 | 493 | 490 | 45.31% | +5.31 | +0.133R | +3.07 | ±4.41 | Fragile | 584.55 | **ACCEPT** |
| **P3-T05 stacked** | 8210305 | 421 | 420 | **47.38%** | **+7.38** | **+0.185R** | **+5.14** | ±4.78 | **Robust*** | **620.63** | **ACCEPT (champion)** |

\*Robust only under default Leak=2.24 pp and R=1.5 proxy. Currency blotter required before G1 claim.

## Deltas vs P0

| Preset | ΔWR | ΔE_N | ΔEF | Freq | Decision |
| --- | ---: | ---: | ---: | ---: | --- |
| T01 | −1.03 pp | −0.026R | −1.03 pp | 82% | Reject — filter hurts expectancy |
| T02 | +0.57 pp | +0.014R | +0.57 pp | 86% | Accept — small lift |
| T05 | +2.64 pp | +0.066R | +2.64 pp | 74% | **Accept — champion** |

## Interpretation

- **Session-only (cut 08–12)** failed: removing London morning also removed useful setups (likely entries that become overnight winners). Isolation cell “LON thin” ≠ “LON removable in isolation.”
- **Skip Tuesday** helps modestly (matches BM≤0 cell).
- **Stack** works: afternoon session + no Tuesday → best WR/E_N/EF; freq 74% ≥ 50% (no FREQUENCY_STALL).

## Side diagnosis

Unchanged: **WR-side** improvement via filters (not R/AL geometry).

## Champion lock

```
EDX-P3-T05_session12-20_skipTue_G0_long.set
InpStartHour=12, InpTradeTue=false, else = P0/EF-G1
```

**Next:** treat T05 as filter champion → optional currency re-run → P4 gates (or finish deferred P1 ATR/ER). P2 payoff still deferred unless champion stalls.
