# UK100 M5 — L2 policy pack (P2 complete)

**Version:** 1.0.0  
**Tasks:** UK100-M5-AOS-P2-T01 … T07  
**Date:** 2026-10-20  
**Compare window:** tip May→Aug 2026 (n=116)  
**Evidence:** `blotter/archive/UK100-M5-AOS-P2/P2_CF.json` · `P2_SUMMARY.json`  
**Costs:** `Leak_source=journal_2x_entry_spread_median` (**5.93 pp**)  
**Mode:** L2det v1b **HITL RESEARCH ARMED** (`UK100_5m_stack` · magic **26121907**) · L2 AI **DISARM** · no geometry change · no M15/FX L2 pin  
**Baseline:** [`UK100_M5_AOS_BASELINE_v1.md`](./UK100_M5_AOS_BASELINE_v1.md)  
**Roadmap:** [`aios_roadmap_M5.md`](./aios_roadmap_M5.md)  
**Sign-off:** [`AIOS_SIGNOFF_M5.md`](./AIOS_SIGNOFF_M5.md)  
**Wire:** `Include/AOS_L2det_uk_m5.mqh` · [`aos_l6_ledger_M5.md`](./aos_l6_ledger_M5.md)

P4 Tester twin remains magic **26121904**.

---

## 0. Armed map summary

| ID | Rule | Status |
| --- | --- | --- |
| `L2det_uk_m5_v1_H12_13` | Skip if hour ∈ {12,13} | **HOLD** aggressive (ΔE_N +0.19 · 8 Wed FP) |
| `L2det_uk_m5_v1_Mon_AND_H12` | Skip if Mon ∧ H12–13 | **ARM_SOFT** (nested in v1b) |
| `L2det_uk_m5_v1_SELL_AND_H12` | Skip if SELL ∧ H12–13 | **ARM_SOFT** (nested in v1b) |
| `L2det_uk_m5_v1_SELL_near_atr` | Skip if SELL ∧ atr≥0.9×869 | **HOLD** optional additive |
| **`L2det_uk_m5_v1b_stack`** | **(Mon∧H12–13) ∨ (SELL∧H12–13)** | **ARM_SOFT** (preferred) |
| `L2det_uk_m5_v1_Mon` | Skip if Mon | **HOLD** (10 H08–11 winner FP) |
| `L2det_uk_m5_v1_Aug` | Skip if month=Aug | **HOLD** calendar seed · tip only |
| Mon ∨ H12–13 / H12 ∨ Aug | — | **REJECT_FREQUENCY_STALL** |
| Permanent skip BUY / SELL | — | **DISARM** |
| Blanket near_atr | — | **DISARM** |
| `L2skip_uk_m5` AI | prior-fit LR | **DISARM** (AUC_tip≈0.40) |

---

## 1. P2-T01 — parity

| Check | Tip | Prior |
| --- | ---: | ---: |
| Tue fires | 0 | 0 |
| ATR &gt; 869 | 0 | 0 |
| Verdict | **PASS** | **PASS** |

Do not re-gate Tue / ATR max in L2det.

---

## 2. P2-T02 — Mon ± H12–13

| Policy | ΔE_N | Ret. | Prec. | Wed FP | H08–11 FP | BUY FP | Verdict |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| skip_Mon | +0.076 | 72.4% | 56% | 0 | **10** | 10 | **HOLD** (morning collateral) |
| skip_H12_13 | **+0.186** | 59.5% | 60% | **8** | 0 | 10 | **HOLD** aggressive |
| Mon ∨ H12–13 | +0.235 | **39.7%** | 54% | 8 | 10 | 19 | **REJECT_FREQUENCY_STALL** |
| **Mon ∧ H12–13** | +0.079 | **92.2%** | **89%** | 0 | 0 | 1 | **ARM_SOFT** |

---

## 3. P2-T03 — side-caution (tip buy-led → SELL first)

| Policy | ΔE_N | Ret. | Prec. | Collateral | Verdict |
| --- | ---: | ---: | ---: | --- | --- |
| skip_SELL | +0.051 | 53.5% | 50% | 7 Wed · 16 H08–11 | HOLD / weak |
| **skip_SELL ∧ H12–13** | **+0.131** | **76.7%** | **67%** | 4 Wed · 0 BUY | **ARM_SOFT** |
| skip_SELL ∧ Mon | +0.038 | 90.5% | 64% | 4 H08–11 | ARM_SOFT weak |
| skip_SELL ∧ near_atr | +0.064 | 87.1% | 67% | 2 Wed · 1 H08–11 | **HOLD** additive |
| skip_BUY | −0.058 | 46.5% | 45% | 34 BUY winners | **REJECT** |
| skip_BUY ∧ near_atr | +0.012 | 82.8% | 50% | 10 BUY | DISARM / no tip lift |

---

## 4. P2-T04 — stress cells

| Policy | ΔE_N | Ret. | Prec. | Note | Verdict |
| --- | ---: | ---: | ---: | --- | --- |
| skip_Aug | +0.115 | 67.2% | 58% | 5 Wed · 10 H08–11 FP | **HOLD** calendar |
| H12 ∨ Aug | +0.249 | 37.9% | 54% | Frequency stall | **REJECT** |
| Mon ∨ Aug | +0.208 | 47.4% | 56% | Frequency stall | **REJECT** |
| blanket near_atr | +0.095 | 69.8% | 57% | Use SELL∧near_atr instead | **DISARM** |
| prior Feb / Apr | — | — | — | Diagnostic only | Not tip arm |

---

## 5. Preferred stack — v1b

```text
SKIP if (Mon ∧ hour∈{12,13})  OR  (SELL ∧ hour∈{12,13})
```

| | Baseline tip | After v1b |
| --- | ---: | ---: |
| n | 116 | **83** |
| WR | 52.6% | **61.4%** |
| E_N | +0.183R | **+0.383R** |
| EF_proxy | +2.22 pp | **+11.08 pp** |
| ΔE_N / ΔEF | — | **+0.199R / +8.86 pp** |
| Retention | 100% | **71.6%** |
| Prec. losers | — | **69.7%** |
| Wed / H08–11 / BUY winner FP | — | **4 / 0 / 1** |

**HITL override:** auto bar flagged HOLD_SOFT on Wed FP=4; **ARM_SOFT** accepted — midday Wed losers dominate, morning protect intact, tip BUY almost untouched.

**Not armed:** full H12–13 alone (more BUY+Wed FP); Mon∨H12 / H12∨Aug (FREQUENCY_STALL).

---

## 6. P2-T05 — size table (spec only)

Wire after L4. Skip outranks size. See [`aos_l2_size_table_M5.md`](./aos_l2_size_table_M5.md).

| State | f_mult |
| --- | ---: |
| Expanding / Stable | 1.0 |
| Compressing | 0.5 |
| Near frontier | 0.25 |
| Below frontier | 0.0 |
| L2det WOULD_SKIP | 0.0 |

---

## 7. P2-T06 — `L2skip_uk_m5` (DISARM)

| Item | Value |
| --- | --- |
| Train | prior n=119 · LogisticRegression balanced C=0.5 |
| Features | hour, spread, atr, near_atr, Mon, H12–13, Aug/Feb/Apr, buy/sell |
| Prior AUC | ≈0.61 |
| Tip OOS AUC | **≈0.40** (worse than chance) |
| Best thr tip | 0.55 → 2 skips · prec **0** · ΔE_N **−0.019** → **DISARM** |
| Artifact | `infra/artefacts/models/L2skip_uk_m5/LATEST/` · **SHADOW_ONLY** |
| MQH export | **Not generated** |

**Read:** Prior→tip transfer fails (same class of failure as M15 UK L2AI). Keep det maps; revisit after hist tape + measured Leak + structure flags.

---

## 8. P2-T07 — stack scorecard (tip)

| Stack | Kept E_N | ΔE_N | Ret. | Verdict |
| --- | ---: | ---: | ---: | --- |
| P0 engine | +0.183R | — | 100% | BASELINE |
| H12–13 alone | +0.370R | +0.186 | 59.5% | HOLD aggressive |
| Mon ∧ H12–13 | +0.262R | +0.079 | 92.2% | ARM_SOFT nested |
| SELL ∧ H12–13 | +0.315R | +0.131 | 76.7% | ARM_SOFT nested |
| **v1b (Mon∧H12)∨(SELL∧H12)** | **+0.383R** | **+0.199** | **71.6%** | **ARM_SOFT preferred** |
| v1b2 (Mon∧H12)∨(SELL∧near_atr) | +0.316R | +0.133 | 81.0% | HOLD softer |
| L2AI only | +0.164R | −0.019 | 98% | **DISARM** |
| H12 ∨ L2AI | +0.343R | +0.160 | 58% | worse than H12 alone / DISARM AI |

---

## 9. Explicit non-claims

- Do not import M15 `Thu` / `H08` / `Jul` / `BUY∧near_atr` maps.  
- Do not attach `L2det_uk` / `L2skip_uk` pins to magic **26101905**.  
- Shadow only — no chart arm until P4 ledger + P7 HITL (magic **26121907**).  
- Aug calendar HOLD — replace with non-calendar features when hist grows.

---

## 10. Next

P3 — L3 halt / L4 W20–W50 health on v1b kept path · then P4 ledger + Tester research `.set` when wiring `AOS_L2det_uk_m5`.
