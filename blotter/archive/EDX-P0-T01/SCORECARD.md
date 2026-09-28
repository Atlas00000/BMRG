# EDX-P0-T01 SCORECARD (provisional)

**Scored:** 2026-09-25
**Preset:** EDX-P0-T01_baseline_G0-EF-G1_EURUSD-M5_long.set (inputs matched)
**Log:** Tester/Agent 20260925.log @ 09:49:23

## Contract checks

| Rule | Required | Actual | Pass |
| --- | --- | --- | --- |
| Geometry G0 | MaxLevels=1 MaxEntries=1 | 1 / 1 | YES |
| BBDev / SL / TP | 2.2 / 300 / 450 | match | YES |
| Magic | 8210001 | 8210001 | YES |
| Window | 2025.01.01–2026.09.24 | **2026.07.01–2026.09.24** | **NO** |
| Profit mode | Account currency | **pips** (deposit 400) | **NO** |
| Evidence tier | n≥100 provisional / ≥385 Standard | **n=41 opens / 40 exits** | **NO** |

## Health vector (ticket = event under G0; R assumed = RR = 1.5 from full TP/SL exits)

| Metric | Value |
| --- | --- |
| n (opens) | 41 |
| n (TP+SL) | 40 |
| WR | 32.5% (13 TP / 27 SL) |
| AW | ~+1.5R (proxy; all TP hits) |
| AL | ~1.0R (proxy; all SL hits) |
| R | ~1.5 (proxy; RR−R ≈ 0) |
| RR | 1.5 |
| RR−R | ~0 (no MID exits) |
| BWR | 40% |
| BM | **−7.5 pp** |
| FMI | n/a (BM negative) |
| Leak (c_R) | **unmeasured** (pips mode; costs_defaulted) |
| EF | ≤ BM − Leak → **≤ −7.5 pp** (Negative zone even before Leak) |
| M | ±14.5 pp (n=40; Wilson-scale huge) |
| E_N | **−0.188R** |
| PF proxy | 0.72 |
| MaxDD | not available in currency (pips path 400→376.31) |
| Final | 376.31 pips (−23.69 from 400) |

## Rolling (calendar months inside window)

| Month | Opens | WR |
| --- | ---: | ---: |
| 2026.07 | 20 | 36.8% |
| 2026.08 | 13 | 30.8% |
| 2026.09 | 8 | 25.0% |

Lifecycle (provisional): **Below frontier** / compressing through the quarter. ΔD not computable on trade-count W250 (n≪250).

## Production-gate zone

**Negative** (EF ≤ 0). Not Fragile/Robust. G1 cannot pass.

## Side diagnosis (this sample)

**WR-side** — not R-side.

- Exit mix is textbook full SL/TP → realised R ≈ designed RR; AL ≈ 1R, AW ≈ 1.5R.
- Failure is win rate far below BWR (32.5% vs 40%).
- Working hypothesis *"AL too large compressing R"* is **rejected on this sample** (pending long-window currency blotter).

## Verdict

| Field | Result |
| --- | --- |
| Task accept (scored?) | YES — vector filled |
| Official P0 baseline for EDX deltas | **NO** — wrong window, pips mode, n insufficient |
| Next action | Re-run T01 with long window + currency profit; or mark this as P0-T04-like quarterly cell |

