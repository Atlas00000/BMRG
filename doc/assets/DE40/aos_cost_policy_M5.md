# DE40 M5 — AOS cost / Leak policy

**Task:** DE40-M5-AOS-P0-T03  
**Frozen:** 2026-10-20  
**Status:** Leak **prior** = Stage-1 authority · journal **proxy** optimistic · deal-measured **OPEN**  
**Binding:** [`edge_framework.md`](./edge_framework.md) · [`DE40_M5_AOS_BASELINE_v1.md`](./DE40_M5_AOS_BASELINE_v1.md)  
**Sibling:** [`aos_cost_policy.md`](./aos_cost_policy.md) (M15 · Leak prior **9.8 pp** on SL 5000) — different geometry; do not mix

---

## Defaults (until deal blotter)

| Component | Policy |
| --- | --- |
| Round-turn proxy | Design card **1100 pts** RT (live spread≈1020 + buffer) · `c_R = 1100/7000 ≈ 0.157R` |
| Leak prior | `Leak = c_R / (R+1) = 0.157/2.25 ≈` **7.0 pp** at R=1.25 |
| MaxSpread gate | **1500** = entry filter only — **not** Leak |
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

Jan–Aug open-spread median in Tester journal ≈ **84 pts** (max 410) → grossly understates live DE30 ≈**1020** pts.

**Do not promote on journal proxy.** Keep **Leak prior 7.0 pp** as Stage-1 bind until deal export.

Why milder than M15 9.8 pp: same RT cost prior on a **wider SL (7000 vs 5000)** → lower `c_R` → lower Leak. Do not conclude “M5 is cheaper to trade” without measured deals.

---

## Why tip is not costs_fragile (prior)

| | Tip May→Oct | Tip-core May→Aug | Jan→Aug (P0) |
| --- | ---: | ---: | ---: |
| BM | **+9.2 pp** | ~+12 pp | +12.7 pp |
| Leak prior | 7.0 pp | 7.0 pp | 7.0 pp |
| EF_prior | **+2.2 pp** | ~+5.0 pp | **+5.7 pp** |
| Soft WR to clear prior | ≈ BWR + Leak ≈ **51.4%** | same | same |
| Observed WR | **53.7%** | **56.4%** | **57.1%** |
| Journal Leak_proxy | ≈**1.1 pp** (p50 spread 84) | — | — |

Tip clears Stage-1 **under prior** (thinner than tip-core because Sep–Oct). Soft Feb / Oct do not. Journal proxy is **not** authority. OS still **must measure** Leak before P7. Do not thin SL to “improve” WR theatre.

---

## Measured path (P0→P1 gate)

1. Export Strategy Tester deals for tip May→Oct when available (magic **26101903** · DE30 M5); until then use May→Aug + Jan→Aug.  
2. Per event: entry/exit spread pts · commission · swap · slippage → `c_R`.  
3. Recompute Leak / EF / M; update baseline footnote `Leak_source=measured`.  
4. If measured tip EF ≤ 0 → re-label **costs_fragile**; OS may still shadow-skip if E_N holds, but no P7 promote.  
5. If measured Leak ≤ prior and EF > 0 → keep tip healthy zone; continue P1–P2 with measured as authority.

---

## Explicit non-claims

- Prior ≠ measured.  
- Journal p50 ≠ live spread.  
- M15 Leak 9.8 pp is not transferable to M5 (different SL).
