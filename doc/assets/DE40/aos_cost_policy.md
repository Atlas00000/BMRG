# DE40 — AOS cost / Leak policy

**Task:** DE40-AOS-P0-T03  
**Frozen:** 2026-10-19  
**Status:** Leak **prior** = Stage-1 authority · journal **proxy** from P1 · deal-measured **OPEN**  
**Binding:** [`edge_framework.md`](./edge_framework.md) · [`DE40_AOS_BASELINE_v1.md`](./DE40_AOS_BASELINE_v1.md) · P1 `blotter/archive/DE40-AOS-P1/COST_PROXY.json`

---

## Defaults (until deal blotter)

| Component | Policy |
| --- | --- |
| Round-turn proxy | Design card **1100 pts** RT (live spread≈1020 + buffer) · `c_R = 1100/5000 = 0.22R` |
| Leak prior | `Leak = c_R / (R+1) = 0.22/2.25 ≈` **9.8 pp** at R=1.25 |
| MaxSpread gate | **1500** = entry filter only — **not** Leak |
| Preset `InpAOS_Leak=9.8` | Metadata only — **not** measured L1 |
| Commission | Broker card (flag 0 if unknown) |
| Swap | Include when `nights_held ≥ 1` (expect rare on cash sleeve; still mandatory if present) |
| Slippage | Inside 2× spread proxy until fill fields exist |

```
Leak = c_R / (R + 1)
EF   = BM − Leak
```

Every scorecard must set `Leak_source=prior|proxy|measured`.

---

## Journal proxy (P1 — not Stage-1 authority)

Tip entry-spread median in Tester journal = **84 pts** (mean 108 · max 410) → `c_R_proxy=2×84/5000` → Leak_proxy ≈ **1.5 pp** · EF_proxy ≈ **+12.5 pp**.

**Do not promote on journal proxy.** Tester spreads understate live DE30 ≈1020 pts. Keep **Leak prior 9.8 pp** / EF prior **+4.2 pp** as the Stage-1 bind until deal export.

---

## Why tip is not costs_fragile (prior)

| | Tip May→Oct | YTD Jan→Oct |
| --- | ---: | ---: |
| BM | **+14.0 pp** | +5.9 pp |
| Leak prior | 9.8 pp | 9.8 pp |
| EF_prior | **+4.2 pp** | **−3.9 pp** |
| Soft WR to clear prior | ≈ BWR + Leak ≈ **54%** | same |
| Observed WR | **58.4%** | 50.3% |

Tip clears Stage-1 **under prior**. YTD does not (Feb–Mar dilution). OS still **must measure** Leak before P7 — prior is not production L1. Do not thin SL to “improve” WR theatre.

---

## Measured path (P0→P1 gate)

1. Export Strategy Tester deals for tip May→Oct (magic **26101902** · DE30).  
2. Per event: entry/exit spread pts · commission · swap · slippage → `c_R`.  
3. Recompute Leak / EF / M on tip; update baseline footnote `Leak_source=measured`.  
4. If measured tip EF ≤ 0 → re-label **costs_fragile**; OS may still shadow-skip if E_N holds, but no P7 promote.  
5. If measured Leak ≤ prior and EF > 0 → keep tip healthy zone; continue P1–P2 with measured as authority.

---

## Double-counting rule

Only **L1 cost** inside EF. Do not add MaxSpread, ATR blocks, or L2 skips into Leak. L2 = `M` / skip policy. L3 = regime. Preset meta Leak is never production L1.

---

## Spread hygiene note

DE30 live spread ≈ **1020** pts (~7× UK100). MaxSpread **1500** must stay above live. Re-measure before any promote. Geometry SL **5000** exists to clear this tax — OS does not “fix” cost by shrinking SL.
