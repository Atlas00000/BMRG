# JP225 / JPN225 M5 — AOS cost / Leak policy

**Task:** JP225-M5-AOS-P0-T03  
**Frozen:** 2026-10-20  
**Status:** Leak **prior** = Stage-1 authority · journal **proxy** optimistic · deal-measured **OPEN**  
**Binding:** [`edge_framework.md`](./edge_framework.md) · [`JP225_M5_AOS_BASELINE_v1.md`](./JP225_M5_AOS_BASELINE_v1.md)  
**Sibling:** [`aos_cost_policy.md`](./aos_cost_policy.md) (M15 · Leak **measured 2.45 pp**) — different geometry/TF; do not mix

---

## Defaults (until deal blotter)

| Component | Policy |
| --- | --- |
| Round-turn proxy | Design card **~2500 pts** RT (live spread≈2300 + buffer) · `c_R = 2500/25000 = 0.10R` |
| Leak prior | `Leak = c_R / (R+1) = 0.10/3.00 ≈` **3.3 pp** at R=2.00 |
| MaxSpread gate | **3000** = entry filter only — **not** Leak |
| Preset Leak metadata | If present — metadata only — **not** measured L1 |
| Commission | Broker card (flag 0 if unknown) |
| Swap | Include when `nights_held ≥ 1` (expect rare on cash sleeve; still mandatory if present) |
| Slippage | Inside 2× spread proxy until fill fields exist |

```
Leak = c_R / (R + 1)
EF   = BM − Leak
```

Every scorecard must set `Leak_source=prior|proxy|measured`.

---

## Journal proxy (not Stage-1 authority)

Tip / YTD open-spread median in Tester journal ≈ **1400** pts → understates live JPN225 ≈**2300** pts.

**Do not promote on journal proxy.** Keep **Leak prior 3.3 pp** as Stage-1 bind until M5 deal export.

Why milder Leak than M15 prior (~4.3 pp on RR 1.50 / SL 23260): Growth **RR=2.00** + wider SL **25000** → lower `c_R/(R+1)`. Do not conclude “M5 is cheaper” without measured deals. M15 measured **2.45 pp** is **not** transferable to M5.

---

## Why tip is not costs_fragile (prior)

| | Tip May→Oct | YTD Jan→Oct | OFFHOME tip | MATCH Aug–Sep |
| --- | ---: | ---: | ---: | ---: |
| BM | **+8.2 pp** | +5.1 pp | +16.7 pp | −6.9 pp |
| Leak prior | 3.3 pp | 3.3 pp | 3.3 pp | 3.3 pp |
| EF_prior | **+4.9 pp** | +1.8 pp | **+13.4 pp** | **−10.2 pp** |
| Soft WR to clear prior | ≈ BWR + Leak ≈ **36.6%** | same | same | same |
| Observed WR | **41.5%** | 38.5% | **50%** | 26.5% |

Tip clears Stage-1 **under prior**. MATCH pocket does not — that is the OS target cell, not a reason to thin SL. Journal proxy is **not** authority. OS still **must measure** Leak before P7.

---

## Measured path (P0→P1 / P7 gate)

1. Export Strategy Tester deals for tip May→Oct (magic **26101906** · JPN225 M5).  
2. Per event: entry/exit spread pts · commission · swap · slippage → `c_R`.  
3. Recompute Leak / EF / M; update baseline footnote `Leak_source=measured`.  
4. If measured tip EF ≤ 0 → re-label **costs_fragile**; OS may still shadow-skip if E_N holds, but no P7 promote.  
5. If measured Leak ≤ prior and EF > 0 → keep tip healthy zone; continue P1–P2 with measured as authority.

---

## Explicit non-claims

- Prior ≠ measured.  
- Journal p50 ≠ live spread.  
- M15 Leak measured 2.45 pp is not transferable to M5 (different SL / TF / fills).  
- Never thin SL to “fix” Leak under ~2300 live spread.
