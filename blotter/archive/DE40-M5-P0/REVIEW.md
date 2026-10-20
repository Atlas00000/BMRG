# DE40 M5 P0 — Tester log review (expansion)

**Date:** 2026-10-20  
**Scope:** Asset-list **expansion** · **not** live replace · AOS OFF · AIOS later  
**Preset:** `MQL5/Profiles/Tester/BMRG/DE40/BMRG-M5-DE40-6M-P0_balanced_chart.set`  
**Log:** `Tester/logs/20261020.log` · magic **26101903**  
**Artefact:** `SCORE.json`

---

## Window in log

| Window | Final bal | PnL vs $500 | Status |
| --- | ---: | ---: | --- |
| **2026.01.01 → 08.31** | **850.64** | **+350.64** | scored |
| Design tip May→Oct / Sep–Oct FRAGILE | — | — | **not in this log yet** |

---

## Geometry (confirmed from inputs)

SL **7000** / TP **8750** (RR 1.25) · BB 2.2 · CD **6** · session 08–17 · skip Tue · ATR max **2380** · lot 0.1 · AOS **OFF** · Leak prior **7.0 pp**.

---

## Closes (TP/SL) — prior Leak 7.0 pp

| Slice | n | WR | E_N | EF_prior |
| --- | ---: | ---: | ---: | ---: |
| Full Jan–Aug | 168 | 57.1% | +0.286R | +5.7 pp |
| Pre Jan–Apr | 75 | 57.3% | +0.290R | +5.9 pp (Feb soft inside) |
| **May–Aug (design tip core)** | **93** | **57.0%** | **+0.282R** | **+5.5 pp** |
| **Jun–Aug MATCH** | **75** | **60.0%** | **+0.350R** | **+8.6 pp** |

Regime framing holds: **May MISMATCH** weak · **Aug MATCH** star · **Feb** soft pre-tip — not class death.

---

## Notes

- Journal open spread p50 ≈ **84** pts ≪ live ~**1020** — keep Leak **prior 7.0 pp** for Stage-1.
- ATR max active (469 blocks) — G3 FRAGILE cut working.
- Side mix roughly balanced BUY/SELL.
- Next: run tip **2026.05.01→10.18** and Sep–Oct alone before any AIOS / keep decision.
