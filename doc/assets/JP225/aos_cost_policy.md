# JP225 — AOS cost / Leak policy

**Task:** JP225-AOS-P0-T03 · closed by **JP225-AOS-LEAK**  
**Frozen:** 2026-10-19  
**Status:** Leak **measured** · `Leak_source=measured_median_deal_fill`  
**Binding:** [`edge_framework.md`](./edge_framework.md) · [`JP225_AOS_BASELINE_v1.md`](./JP225_AOS_BASELINE_v1.md) · [`LEAK_MEASURED.json`](./LEAK_MEASURED.json)

---

## Authority (tip May→Aug · magic 26101904 · n=79)

| Component | Policy |
| --- | --- |
| Round-turn cost | `entry_spread_pts + max(0, adverse_exit_slip_pts)` from Tester deal fills |
| Median cost_pts_rt | **1423** (mean 1581 · min 1050 · max 2611) |
| c_R median | **0.0612** (= 1423/23260) |
| **Leak measured** | `c_R / (R+1)` = **2.45 pp** at R=1.50 |
| Preset `InpAOS_Leak` | Prefer **2.45** when wiring research OS; prior 4.3 remains conservative stress |
| Commission / swap | Tester journal = **0**; include when live deal export has fields |
| MaxSpread gate | **3000** = entry filter only — **not** Leak |

```
Leak = c_R / (R + 1)
EF   = BM − Leak
```

Every scorecard must set `Leak_source=prior|proxy|measured`.

---

## Tip Stage-1 under measured

| | Prior (stub) | **Measured** |
| --- | ---: | ---: |
| Tip BM | +3.0 pp | +3.0 pp |
| Leak | 4.3 pp | **2.45 pp** |
| Tip EF | **−1.3 pp** | **+0.59 pp** |
| Soft WR to clear | ≈44.3% | ≈42.4% |
| Tip WR | 43.0% | 43.0% |
| Zone | regime_fragile | **tip_stage1_pass_measured** |

Primary mission (tip EF > 0 after Leak) **clears on measured without L2**. L2det May∨Jul remains the hygiene arm (EF **+11.0 pp** kept · MaxDD path from P3).

**Never thin SL** to “fix” Leak — thinner SL raises `c_R` and destroys EF.

---

## History (stubs retained for audit)

| Stub | Value | Role now |
| --- | ---: | --- |
| Design prior RT 2500 pts | Leak **4.3 pp** | Conservative stress / pre-deal CF |
| Journal 2× spread proxy | Leak **4.82 pp** | Upper-bound check only |

---

## Double-counting rule

Only **L1 cost** inside EF. Do not add MaxSpread, ATR blocks, FadeConfirm, or L2 skips into Leak. L2 = `M` / skip policy. L3 = regime. Preset meta Leak is never production L1.
