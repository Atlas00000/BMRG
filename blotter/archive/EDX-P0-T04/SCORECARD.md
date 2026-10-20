# EDX-P0-T04 — SCORECARD (tip stress May→Oct)

**Scored:** 2026-10-07T16:28+01:00  
**Preset:** `EDX-P0-T04_baseline_G0_AUDUSD-M5_MayOct.set` · magic **8230104**  
**Window:** **2026.05.01 → 2026.10.06** · AUDUSD M5 · ACCOUNT CURRENCY  
**Compare to:** EDX-P0-T01 May→Aug baseline

## Identity — PASS

| Field | Expected | Observed |
| --- | --- | --- |
| Magic | 8230104 | **8230104** |
| SL/TP | 300/300 | **300/300** |
| Window tip | ≥ 2026.10 | **→ 2026.10.06** |

---

## Health vector vs P0-T01

| Metric | P0-T01 (May→Aug) | **P0-T04 (May→Oct)** | Δ |
| --- | ---: | ---: | ---: |
| n | 58 | **73** | +15 |
| WR | 62.07% | **56.16%** | −5.91 pp |
| R / RR−R | 1.0 / 0 | **1.0 / 0** | — |
| BM | +12.07 pp | **+6.16 pp** | −5.91 |
| Leak* | 7.50 pp | **7.50 pp** | — |
| EF* | +4.57 pp | **−1.34 pp** | −5.91 |
| E_N | +0.241R | **+0.123R** | −0.118R |
| PnL | +44.39 | **+27.80** | −16.59 |
| Zone | Fragile | **Negative** (EF≤0) | tip leak |
| Side | WR-side | **WR-side** | R-side still rejected |

\*Leak proxy `costs_defaulted` (3×spread/SL).

---

## Tip cells (L3 regime)

| Month | n | WR | E_N | Read |
| --- | ---: | ---: | ---: | --- |
| 2026-05…08 | (as P0) | ≥53.8% | all &gt;0 | primary holds |
| **2026-09** | 11 | **27.3%** | **−0.455R** | **wipeout cell** |
| **2026-10** | 3 | 33.3% | −0.333R | thin / provisional |

**Label:** regime leak **L3** on tip — not class death. Primary May→Aug EXPANSION_KEEP stands.

---

## Accept / reject

| Criterion | Result |
| --- | --- |
| Identity / tip window | **PASS** |
| Tip vs primary documented | **PASS** — Sep eats edge |
| Drop asset? | **NO** — L3 tip mismatch |
| Task | **ACCEPT** (diagnostic) |

**Does not beat P0 on E_N/EF** — expected for tip stress; not a regression of the baseline sleeve.
