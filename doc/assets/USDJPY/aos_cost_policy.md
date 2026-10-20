# USDJPY — AOS cost / Leak policy

**Task:** USDJPY-AOS-P0-T03  
**Frozen:** 2026-10-19  
**Status:** Leak **prior** stub · deal-measured **OPEN**  
**Binding:** [`edge_framework.md`](./edge_framework.md) §4 · [`USDJPY_AOS_BASELINE_v1.md`](./USDJPY_AOS_BASELINE_v1.md)

---

## Defaults (until deal blotter)

| Component | Policy |
| --- | --- |
| Round-turn proxy | Design card **25 pts** RT · `c_R = 25/100 = 0.25R` |
| Leak prior | `Leak = c_R / (R+1) = 0.25/2.2 ≈` **11.4 pp** at R=1.20 |
| MaxSpread gate | **25** = entry filter only — **not** Leak |
| Preset `InpAOS_Leak=11.4` | Metadata only — **not** measured L1 |
| Commission | Broker card (flag 0 if unknown) |
| Swap | Include when `nights_held ≥ 1` (secondary on tip; still mandatory if present) |
| Slippage | Inside 2× spread proxy until fill fields exist |

```
Leak = c_R / (R + 1)
EF   = BM − Leak
```

Every scorecard must set `Leak_source=prior|proxy|measured`.

---

## Why USDJPY is costs_fragile

| | Value |
| --- | ---: |
| Tip BM | +2.8 pp |
| Leak prior | 11.4 pp |
| Tip EF_prior | **−8.6 pp** |
| Soft WR to clear prior | ≈ BWR + Leak ≈ **57%** |
| Tip WR | 48.2% |

Stage-1 bottleneck is **Leak vs thin BM**, not geometry death. OS must not claim Robust on prior. Prefer deal export before hard-arming L2det (shadow CF OK on gross E_N while Leak pending).

---

## Measured path (P0→P1 gate)

1. Export Strategy Tester deals for tip May→Aug (magic 26101828).  
2. Per event: entry/exit spread pts · commission · swap · slippage → `c_R`.  
3. Recompute Leak / EF / M on tip; update baseline footnote `Leak_source=measured`.  
4. If measured EF ≤ 0 on tip → keep **costs_fragile**; OS may still shadow-skip if E_N holds, but no P7 promote.  
5. If measured Leak ≪ 11.4 pp and EF > 0 → upgrade zone; continue P1–P2 with measured as authority.

---

## Double-counting rule

Only **L1 cost** inside EF. Do not add MaxSpread, ATR blocks, or L2 skips into Leak. L2 = `M` / skip policy. L3 = regime. Preset meta Leak is never production L1.
