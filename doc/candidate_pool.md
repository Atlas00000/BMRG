# BMRG candidate pool

**Role:** Living set of deployable / compoundable presets — not a single “best” winner.  
**Admission:** E_N > 0 · WR > BWR · EF > 0 preferred (else `costs_fragile`).  
**Windows:** Long = 2025.01.01→2026.09.24 · 3M = 2026.07.01→2026.09.24  

**Current champion (operational):** `EDX-P2-T04_SL300_TP300_RR1_champFilters_G0_long.set` — magic **8210204** · Harvest · RR=1.0 · BWR 50%.

## Current members (both windows filled 2026-09-25)

| Preset | Magic | Role | Long | 3M | Notes |
| --- | ---: | --- | --- | --- | --- |
| `EDX-P2-T04_…` SL300/TP300 | **8210204** | **Harvest · champion** | KEEP EF 1.77 n=530 | KEEP EF **6.43** n=49 | Current primary; best recent; long confirmed |
| `EDX-P4-T01_…` SL300/TP450 | 8210401 | Balanced / Growth | KEEP EF **5.18** n=420 | KEEP EF 0.22 n=33 thin | Best long EF; G0–G4 pass; G5 fail TP−10; secondary |
| `EDX-P2-T01_…` SL200/TP450 | 8210201 | Survival | KEEP EF 0.87 n=509 | costs_fragile EF−0.75 | Low BWR sleeve; cut f in late-2026 stress |
| `EDX-P2-T02_…` SL200/TP300 | 8210202 | Balanced-scale | KEEP EF 0.09 n=636 | KEEP EF 0.96 n=61 | Scale variant |
| `EDX-P2-T05_…` TP off | 8210205 | Mid-exit | costs_fragile EF−3.1 n=1042 | costs_fragile EF−2.6 | Watch only — not deploy |

## Experimental (not champion · not pool admission)

| Preset | Magic | Diff vs Harvest champion | Notes |
| --- | ---: | --- | --- |
| `EDX-EXP-Harvest_lot0.02_DD50_G0_long.set` | **8210290** | Fixed lot **0.02** · EquityHalt **50%** | Capital / sizing stress only; score separately; do not overwrite 8210204 |

Full matrix: `blotter/archive/EDX-POOL_WINDOWS/SCORECARD_MATRIX.md`

## Dropped

| Preset | Why |
| --- | --- |
| P2-T03 TP600 | 3M WR&lt;BWR, E_N&lt;0 |
| G5 TP−10 on Growth (405) | EF≤0 |
| P3-T01 session-only | Lost to P0 |

## Blend

Primary weight on **Harvest**; compound small-f with **Growth + Survival** for regime retune. Prefer long for size; use 3M to decide sleeve weight *now*.
