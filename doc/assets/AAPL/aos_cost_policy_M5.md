# AAPL M5 — AIOS Cost / Leak Policy

**Task:** AAPL-M5-AOS-P0-T03  
**Frozen:** 2026-10-20 (stub)  
**Engine:** magic **26102011** · SL **190** · TP **280** · RR ≈ **1.47**  
**Roadmap:** [`aios_roadmap_M5.md`](./aios_roadmap_M5.md) · binding [`edge_framework.md`](./edge_framework.md)

---

## Identities

```
BWR  = 1 / (1 + R)           # designed R = 1.47 → BWR ≈ 40.4%
BM   = WR − BWR
c_R  = round-turn cost in R   # prefer deal-measured
Leak = c_R / (R + 1)          # report in pp of WR
EF   = BM − Leak
```

`InpAOS_Leak` / preset meta Leak is **metadata only** — never Stage-1 L1.

---

## Current proxies (until deal export)

| Source | Estimate | Use |
| --- | ---: | --- |
| Preset meta Leak | **2.1 pp** | Display / input default only — **inadmissible** for Robust |
| Tip journal med spread (P1) | **29** pts | From `COST_PROXY.json` tip n=77 |
| Framework Leak 1× = (med/SL)/(R+1) | **6.17 pp** | Unified identity |
| Framework Leak 2× | **12.34 pp** | Round-turn stress |
| Profile shorthand med/SL | **~15.3 pp** | Stage-1 authority until measured (BM−c_R style) |
| `spread_high_thr` | **≥30** | L1 cell (tip p80 floor) |

**Tip EF (P1):** BM **+6.33 pp** → EF @ profile 15.3 ≈ **−9.0 pp** · EF @ 2× ≈ **−6.0 pp** · EF @ 1× framework ≈ **+0.16 pp** (not Robust). Stage-1 **fail / Fragile** under profile/2× bars.

**Soft WR after profile Leak:** ≳ BWR + 15.3 ≈ **55%**. Tip WR 46.8% clears BWR only.

P1 artifact: `blotter/archive/AAPL-M5-AOS-P1/COST_PROXY.json`.

---

## Deal-export checklist (measured Leak)

1. Export deals / blotter for magic **26102011** tip window May→Oct.  
2. Per event: entry spread pts · exit spread · overnight swap · gap overrun beyond SL when exit ≠ TP/SL.  
3. Aggregate `c_R` → Leak → EF; set `Leak_source=measured`.  
4. Update this file + baseline scorecard; do **not** change SL/TP to “fix” Leak.  
5. Archive under `blotter/archive/AAPL-M5-AOS-P0-T03/`.

---

## OS implications

| Finding | OS response |
| --- | --- |
| Leak dominates EF | Prefer L2det **high-spread** SOFT + L9 spread tercile before geometry change |
| Overnight / OTHER share high | Elevate **L8** after L2det |
| Tip E_N > 0 but EF ≤ 0 | Keep tip WATCH; iterate OS for EF lift; no live attach |

---

## Status

```text
Leak_source: journal_1x_entry_spread_median (P1) + profile_authority_15.3
med_spread_tip: 29
Leak_1x_pp: 6.17
Leak_2x_pp: 12.34
Leak_profile_pp: 15.3
EF_profile_pp: ~-9.0
spread_high_thr: 30
measured: OPEN
```
