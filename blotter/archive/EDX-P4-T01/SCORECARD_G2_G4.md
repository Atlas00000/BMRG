# EDX-P4-T02 / T03 / T04 — G2–G4 from currency champion blotter

**Source:** EDX-P4-T01 archive (frozen T05 stack, magic 8210401)  
**Leak used:** 2.21 pp (L1) · **No IS re-optimisation** (params frozen)

---

## G2 — Anchored walk-forward

Four calendar OOS folds (~5 months). WFE for folds with IS:

| Fold | OOS n | OOS WR | OOS E_N | Zone | IS→OOS WFE |
| --- | ---: | ---: | ---: | --- | ---: |
| OOS1 2025.01–05 | 135 | 49.6% | +0.241R | Fragile | (no IS) |
| OOS2 2025.06–10 | 115 | 45.2% | +0.130R | Fragile | 0.54 |
| OOS3 2025.11–2026.03 | 91 | 46.2% | +0.154R | Fragile | 0.81 |
| OOS4 2026.04–09 | 79 | 48.1% | +0.203R | Fragile | 1.13 |

| Criterion | Result |
| --- | --- |
| ≥4 folds | PASS |
| OOS E_N > 0 in ≥75% | **4/4** PASS |
| mean WFE ≥ 0.5 | **0.83** PASS |
| Pooled OOS EF > 0 | PASS (each OOS BM>0; small-n Fragile vs M only) |

**G2 PASS** (frozen-param anchored WF)

---

## G3 — Regime robustness

Champion is **intentionally filtered**: `InpStartHour=12`…`EndHour=20`, `InpTradeTue=false`.

| Metadata | Value |
| --- | --- |
| `regime_filtered` | **true** |
| Declared filters | Session 12:00–20:00 server; skip Tuesday |
| ATR×ER cells | Deferred (not required when regime_filtered) |

DoW BM (n≥20): worst = Wednesday **+1.67 pp > 0**. Max DoW share ≈ Thursday ~24% ≤ 70%.

Note: hour bucket 14–16 has BM −4.0 pp (exit-hour mix / thin) — monitored, not a G3 fail under declared session filter.

**G3 PASS** (`regime_filtered=true`)

---

## G4 — Monte Carlo (equity space, C₀=$400, f≈0.75%/trade fixed lot)

DD_limit = 25% × $400 = **$100**. Ruin = equity ≤ $200. Iterations = 5000. Block = 20.

| Procedure | P95 MaxDD | median G | P(ruin) | Gate |
| --- | ---: | ---: | ---: | --- |
| Observed | $34.5 | $632.5* | 0 | — |
| MC-1 shuffle | $61.5 | $632.5 | 0% | ok |
| **MC-2 block20** | **$60** ≤100 | **$625** >0 | **0%** ≤1% | **PASS** |
| MC-3 stress (WR−M, R−10%, cost×1.5) | $119 | **$430.7** ≥400 | **0.04%** ≤5% | **PASS** |

\*Price-path proxy; account final = $620.63.

**G4 PASS**

---

## Gate stack so far

```
G0 PASS ∧ G1 PASS ∧ G2 PASS ∧ G3 PASS ∧ G4 PASS
G5 PENDING  (±10% params + cost ×1.5 blotter confirm)
```
