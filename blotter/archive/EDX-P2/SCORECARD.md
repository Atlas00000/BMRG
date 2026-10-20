# EDX-P2 — Payoff / exit experiments vs P0-T01

**Scored:** 2026-10-07 · Tester `20261007.log`  
**Baseline (P0-T01):** n=58 · WR 62.07% · E_N **+0.241R** · EF **+4.57 pp** · pnl +44.39 · RR=1

Leak policy: spread proxy `3×med_spread/SL` (`costs_defaulted`).

## Results

| Task | Magic | SL/TP | n | WR | R | E_N | EF pp | PnL | Verdict |
| --- | ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| **P0-T01** | 8230101 | 300/300 | 58 | 62.1% | 1.0 | **+0.241** | **+4.57** | +44.39 | baseline |
| P2-T01 | 8230201 | 240/240 | 84 | 47.6% | 1.0 | **−0.048** | −11.76 | −10.56 | **REJECT** |
| P2-T02 | 8230202 | 360/360 | 39 | 48.7% | 1.0 | **−0.026** | −7.53 | −1.30 | **REJECT** |
| P2-T03 | 8230203 | 300/450 | 36 | 22.2% | 1.5 | **−0.444** | −23.78 | −48.40 | **REJECT** |
| P2-T04 | 8230204 | 300/240 | — | — | — | — | — | — | **INVALID** |

### P2-T04 note

Init refused: `TP_Points must be >= SL_Points when TP is on`. Trap preset cannot run on this EA build — treat as **N/A**, not a scored regression.

## Δ vs P0 (completed runs)

| Task | ΔE_N | ΔEF | ΔWR | ΔPnL |
| --- | ---: | ---: | ---: | ---: |
| T01 240/240 | −0.289 | −16.3 | −14.5 pp | −54.95 |
| T02 360/360 | −0.267 | −12.1 | −13.4 pp | −45.69 |
| T03 300/450 | −0.685 | −28.4 | −39.9 pp | −92.79 |

## Side diagnosis (confirmed)

All completed P2 geometries keep **R ≈ RR** (FIXED_RR). None fix a phantom AL problem — they **destroy WR**.

| Claim | Result |
| --- | --- |
| AL too large / R-side primary | **REJECTED again** |
| Path forward | **WR-side hygiene (P3)** — session StartHour 13, optional skip Mon — not SL surgery |

## P2-T05 — Exit summary

| Pick | Geometry |
| --- | --- |
| **Keep champion payoff** | **SL300 / TP300 RR=1** (P0) |
| Reject | ATR downscale 240, upscale 360, Growth RR1.5 |
| Deferred | TP&lt;SL trap (EA hard block) |

**Phase 2 complete for scored tasks.** Next: **EDX-P3-T02** StartHour=13 (session cell justified) or P3-T01 skip Mon (provisional).
