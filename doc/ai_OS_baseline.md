# AOS_BASELINE — frozen engine health vector

**Task:** AOS-P0-T01  
**Frozen at:** 2026-09-25  
**Engine:** Harvest champion (unchanged)  
**Preset:** `Profiles/Tester/BMRG/EDX-P2-T04_SL300_TP300_RR1_champFilters_G0_long.set`  
**Verify preset (optional re-run):** `Profiles/Tester/BMRG/AOS-P0-T01_L0_baselineLock_Harvest_long.set` (magic **8310001**)  
**Sources:** `blotter/archive/EDX-POOL_WINDOWS/SCORECARD_MATRIX.md` · `blotter/archive/EDX-P2-T04/`  
**Archive:** `blotter/archive/AOS-P0-T01/`

This file is the number every AOS layer experiment must **beat or hold** (loose bar in `doc/ai_OS.md` §4).  
Do not edit silently — bump `baseline_id` and open a new AOS-P0 task if the engine champion changes.

---

## Identity

| Field | Value |
| --- | --- |
| `baseline_id` | **AOS_BASELINE_v1** |
| `engine_role` | Harvest · operational champion |
| `magic_champion` | **8210204** |
| `geometry` | SL300 / TP300 · RR=1.0 · BWR=50% |
| `filters` | session **12–20** · **TradeTue=false** · BBDev **2.2** · G0 · Cooldown 3 · both sides |
| `lot_mode` | Risk% 0.5 (champion; not EXP lot0.02) |
| `symbol` / TF | EURUSD / M5 |
| `deposit_ref` | 400 USD · account **currency** |
| `Leak_proxy` | **2.2 pp** (pool L1) |
| `long_window` | 2025.01.01 → 2026.09.24 |
| `stress_3M` | 2026.07.01 → 2026.09.24 |

---

## Primary vector — Long (decision baseline)

| Symbol | AOS_BASELINE (long) |
| --- | ---: |
| n | **530** |
| WR % | **54.5** |
| BWR % | **50.0** |
| R / RR | **1.0 / 1.0** |
| BM pp | **+4.5** |
| Leak pp | **2.2** |
| EF pp | **1.77** |
| M pp (approx) | **±4.24** |
| Zone | **Fragile** (EF &lt; M) |
| E_N | **+0.091R** |
| Final $ | **~533** |
| fires_90d (provisional) | use ~35–80 band / recalibrate from tape in P1 |

**OS must hold (loose):** W250 EF ≥ **1.77 − 1.0 = 0.77 pp**; W250 MaxDD ≤ baseline MaxDD + 2 pp (MaxDD TBD from blotter if missing — report when first measured under AOS).

---

## Stress vector — 3M (regime weight)

| Symbol | AOS_BASELINE (3M) |
| --- | ---: |
| n | **49** (thin — warn, not kill) |
| WR % | **59.2** |
| BWR % | **50.0** |
| E_N | **+0.184R** |
| EF pp | **+6.43** |
| Final $ | **425.48** |
| Zone | Strong EF / thin n |

---

## Secondary ref (not OS default)

Growth `EDX-P4-T01` magic 8210401 — long EF **5.18** n=420 · G0–G4 PASS · G5 FAIL.  
Use only for optional Δ commentary; experiments default to Harvest.

---

## Iteration reminder

```
ACCEPT layer experiment if:
  n_remaining ≥ 100
  W250 EF ≥ baseline_EF − 1pp
  W250 MaxDD ≤ baseline_MaxDD + 2pp
  90d fires ≥ 50% baseline (warn if stall)
  not (WR↑ and EF↓/E_N↓)
```

Full G0–G5 only at **AOS-P7** promote.
