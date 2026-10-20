# DE40 M5 — L2 policy pack (P2 complete)

**Version:** 1.0.0  
**Tasks:** DE40-M5-AOS-P2-T01 … T07  
**Date:** 2026-10-20  
**Compare window:** tip May→Oct 2026 (n=123 · →10.19) · YTD support for Feb  
**Evidence:** `blotter/archive/DE40-M5-AOS-P2/P2_CF.json` · `P2_SUMMARY.json`  
**Costs:** `Leak_source=prior_7.0pp` (authority) · journal proxy ≈1.1 pp reported only  
**Mode:** L2det v1b **HITL RESEARCH ARMED** (`DE40_5m_stack` · magic **26151907**) · L2 AI **DISARM** · no geometry change · no M15 `AOS_L2det_de` pin  
**Baseline:** [`DE40_M5_AOS_BASELINE_v1.md`](./DE40_M5_AOS_BASELINE_v1.md)  
**Roadmap:** [`aios_roadmap_M5.md`](./aios_roadmap_M5.md)  
**Wire:** `Include/AOS_L2det_de_m5.mqh` · Config `InpAOS_DE_M5_*`

---

## 0. Armed map summary

| ID | Rule | Status |
| --- | --- | --- |
| `L2det_de40_m5_v1_BuyH14_16` | Skip if BUY ∧ hour∈{14,16} | **ARM_SOFT** (nested in v1b) |
| `L2det_de40_m5_v1_BuyOct` | Skip if BUY ∧ month==Oct | **ARM_SOFT** (nested in v1b) |
| **`L2det_de40_m5_v1b_stack`** | **(BUY∧H14\|16) ∨ (BUY∧Oct)** | **ARM_SOFT** (**preferred**) |
| `L2det_de40_m5_v1_H14_16` | Skip if hour∈{14,16} (all sides) | **HOLD** aggressive (SELL FP) |
| `L2det_de40_m5_v1_Oct` | Skip if month==Oct (all sides) | **HOLD** additive (1 SELL FP) |
| `L2det_de40_m5_v1_Oct_OR_H14_16` | Oct ∨ H14\|16 | **HOLD** max ΔE_N · more SELL FP |
| Blanket BUY / Sep–Oct / MISMATCH | — | **DISARM** / HOLD weak |
| Blanket near_atr / BUY∧near_atr | — | **DISARM / REJECT** (tip near_atr is a **star**) |
| Feb (YTD only) | Skip if month==Feb | **ARM_SOFT on YTD** — not tip calendar |
| `L2skip_de40_m5` AI | prior→tip LR | **DISARM** (AUC_tip≈0.51) |

---

## 1. P2-T01 — parity

| Check | Tip | YTD |
| --- | ---: | ---: |
| Tue fires | 0 | 0 |
| ATR &gt; 2380 | 0 | 0 |
| Verdict | **PASS** | **PASS** |

Do not re-gate Tue / ATR max in L2det.

---

## 2. P2-T02 — late session (H14 / H16)

| Policy | ΔE_N | Ret. | Prec. | Aug FP | SELL FP | Verdict |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| skip_H14 | (in H14_16) | — | — | — | — | nested |
| skip_H16 | (in H14_16) | — | — | — | — | nested |
| **skip_H14_16** | **+0.061** | **89.4%** | **69%** | 1 | 2 | **ARM_SOFT** / prefer BUY∧ |
| skip_H11 | — | — | — | — | — | not primary |

---

## 3. P2-T03 — buy-caution (tip sell-led)

| Policy | ΔE_N | Ret. | Prec. | Aug FP | SELL FP | Verdict |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| skip_BUY | +0.221 | **42.3%** | 54% | **12** | 0 | **REJECT_FREQUENCY_STALL** |
| skip_SELL | — | — | — | — | — | **DISARM** (carrier) |
| **skip_BUY ∧ H14\|16** | **+0.056** | **92.7%** | **78%** | 1 | **0** | **ARM_SOFT** |
| skip_BUY ∧ Oct | (in v1b) | — | — | — | 0 | **ARM_SOFT** |
| skip_BUY ∧ fragile | +0.060 | 83.7% | 60% | 0 | 0 | **HOLD** (Sep collateral) |
| skip_BUY ∧ near_atr | **−0.013** | 79.7% | 44% | 4 | 0 | **DISARM** |
| skip_BUY ∧ MISMATCH | — | — | — | — | — | weak / HOLD |

**Armed additive:** BUY∧H14\|16 · BUY∧Oct (stack as v1b).

---

## 4. P2-T04 — regime / FRAGILE

| Policy | ΔE_N | Ret. | Prec. | Note | Verdict |
| --- | ---: | ---: | ---: | --- | --- |
| skip_Oct | +0.045 | 93.5% | 75% | 1 SELL FP | **HOLD** (prefer BUY∧Oct) |
| skip_Sep_Oct | +0.061 | 76.4% | 55% | Sep still + | **HOLD** — never blanket Sep |
| skip_FRAGILE_all | ≈ Sep–Oct | — | — | — | **HOLD** |
| skip_MISMATCH_all | +0.024 | 86% | 53% | May / SELL FP | **HOLD / DISARM** arm |
| skip_near_atr_all | **−0.069** | 71% | 39% | Kills tip star | **REJECT** |
| ytd_skip_Feb | +0.060 | 86.5% | 64% | Support only | **ARM_SOFT YTD** |

---

## 5. Preferred stack — v1b

```text
SKIP if (BUY ∧ hour ∈ {14,16})  OR  (BUY ∧ month == October)
```

| | Baseline tip | After v1b |
| --- | ---: | ---: |
| n | 123 | **110** |
| WR | 53.7% | **57.3%** |
| E_N | +0.207R | **+0.289R** |
| EF_prior | +2.21 pp | **+5.83 pp** |
| ΔE_N / ΔEF | — | **+0.081R / +3.62 pp** |
| Retention | 100% | **89.4%** |
| Prec. losers | — | **76.9%** |
| Aug / SELL winner FP | — | **1 / 0** |

**Why not Oct∨H14_16 (max ΔE_N +0.091):** 3 SELL winner FP — tip is sell-led; protect overrides max ΔE_N.

**Not armed:** blanket BUY · near_atr · BUY∧near_atr · Sep–Oct calendar · M15 BUY∧near_atr pin.

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

## 7. P2-T06 / T07 — L2 AI + stack

| Item | Result |
| --- | --- |
| Train | prior Jan–Apr → tip OOS |
| AUC tip | **≈0.51** |
| Best thr ΔE_N | &lt; arm bar |
| Verdict | **DISARM** |
| Stack + AI | No lift over v1b alone |

Pin: `infra/artefacts/models/L2skip_de40_m5/LATEST/` (shadow only).

---

## 8. Wire / preset notes

| Input | Default | Role |
| --- | --- | --- |
| `InpAOS_DE_M5_L2detEnable` | false | Master (true on research OS preset) |
| `InpAOS_DE_M5_SkipBuyH14_16` | true | v1b leg |
| `InpAOS_DE_M5_SkipBuyOct` | true | v1b leg |
| `InpAOS_DE_M5_SkipH14_16All` | false | Aggressive optional |
| `InpAOS_DE_M5_SkipOctAll` | false | Aggressive optional |

Engine magic stays **26101903**. Research OS arm magic **26151907** at P7 (`DE40M5stack`).
