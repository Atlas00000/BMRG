# EDX-P3 — Entry filters vs P0-T01

**Scored:** 2026-10-07 · Tester log  
**Baseline P0:** n=58 · WR 62.07% · E_N **+0.241R** · EF **+4.57 pp** · pnl **+44.39** · Start=12 · Mon=on · BB=2.2 · CD=3

## Results

| Task | Magic | Change | n | WR | E_N | EF pp | PnL | vs P0 | Verdict |
| --- | ---: | --- | ---: | ---: | ---: | ---: | ---: | --- | --- |
| P3-T01 | 8230301 | skip Mon | 47 | 63.8% | **+0.277** | **+6.33** | +41.41 | E_N/EF↑ · $↓ · freq 81% | **ACCEPT** |
| P3-T02 | 8230302 | StartHour **13** | 57 | **68.4%** | **+0.368** | **+11.42** | **+62.90** | all↑ · h12=0 · freq 98% | **ACCEPT** ★ |
| P3-T03 | 8230303 | BBDev **2.5** | 48 | 50.0% | ~0 | −7.50 | +2.30 | collapses margin | **REJECT** |
| P3-T04 | 8230304 | Cooldown **6** | 58 | 62.1% | +0.241 | +4.57 | +44.39 | identical to P0 | **NO_DELTA** |

### Filter sanity

| Task | n hour=12 | n Mon |
| --- | ---: | ---: |
| T01 skip Mon | 22 | **0** |
| T02 StartHour 13 | **0** | 11 |
| T03 BBDev 2.5 | 16 | 11 |
| T04 CD6 | 24 | 13 |

## Δ vs P0

| Task | ΔE_N | ΔEF | ΔWR | ΔPnL | Δn |
| --- | ---: | ---: | ---: | ---: | ---: |
| T01 | +0.036 | +1.76 | +1.8 | −2.98 | −11 |
| **T02** | **+0.127** | **+6.85** | **+6.4** | **+18.51** | −1 |
| T03 | −0.241 | −12.07 | −12.1 | −42.09 | −10 |
| T04 | 0 | 0 | 0 | 0 | 0 |

## Stack backlog (P5)

1. **Primary:** StartHour=13 (T02) — best lone filter; justified by P1 cell n≥30 BM≤0.  
2. **Optional add:** skip Mon (T01) — ACCEPT but smaller lift and lower $. Test stack = T02+T01.  
3. **Drop:** BBDev 2.5 · Cooldown 6 (no help).

Payoff stays **SL300/TP300** (P2).

## Next

**EDX-P5-T01** stack: StartHour13 (+ optional skip Mon) · or run T01+T02 combo preset before P4 ATR gates.
