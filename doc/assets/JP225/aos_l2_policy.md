# JP225 — L2 policy pack (P2 complete)

**Version:** 1.0.0  
**Tasks:** JP225-AOS-P2-T01 … T07  
**Date:** 2026-10-19  
**Compare window:** tip May→Aug 2026 (n=79) · Jan→Aug support  
**Evidence:** `blotter/archive/JP225-AOS-P2/P2_CF.json`  
**Costs:** `Leak_source=measured_2.45pp` (authority from **JP225-AOS-LEAK**) · prior 4.3 / proxy 4.8 retained as stress only  
**Mode:** L2det **ARMED research OS** (`JPN225stack` · `AOS_L2det_jp.mqh`) · L2 AI **DISARM** · no geometry change · no foreign L2 pin  

**Mission result:** Primary map **clears tip Stage-1** under Leak prior (kept EF **+9.2 pp** · WR **53.5%** · E_N **+0.34R**). Under **measured**, engine tip alone EF **+0.59 pp**; May∨Jul kept EF **+11.0 pp**.

---

## 0. Armed map summary

| ID | Rule | Status |
| --- | --- | --- |
| `L2det_jp225_v1_May_OR_Jul` | Skip if May **OR** Jul | **ARMED** research OS (`JPN225stack`) |
| `L2det_jp225_v1_May_fragile` | Skip if May ∧ FRAGILE | **ARM_SOFT** (subset / lighter ret) |
| `L2det_jp225_v1_Jul` | Skip if month=Jul | **ARM_SOFT** (subset) |
| `L2det_jp225_v1_SELL_AND_May` | Skip if SELL ∧ May-FRAGILE | **ARM_SOFT** (narrow · high prec) |
| `L2det_jp225_v1_Wed` | Skip if Wed | **HOLD_SOFT** (Aug FP) |
| `L2det_jp225_v1_H14` | Skip if hour=14 | **HOLD_SOFT** (Jun/Aug FP) |
| `L2det_jp225_v1_H08` / `H09` | Skip H08 or H09 | **ARM_SOFT** weak / **HOLD** as OR |
| Blanket FRAGILE / May∨Jul∨Wed | — | **REJECT_FREQUENCY_STALL** (ret&lt;50%) |
| Blanket near_atr / H13 / BUY | — | **DISARM** |
| `L2skip_jp225` AI | Jan–Apr→tip LR | **DISARM** (AUC≈0.49) |

---

## 1. P2-T01 — parity

| Check | Result |
| --- | --- |
| Tue fires | **0** → **PASS** |
| atr > 19670 on tape | **0** → **PASS** |
| near_atr_cap tip | present (feature OK · **not** a skip alone) |

Do **not** re-gate Tue / ATR max / Fade inside L2det.

---

## 2. P2-T02 — May / Wed

### Tip (primary)

| Policy | Verdict | ΔE_N | ΔEF_pp | Ret. | Prec. | Protect FP |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| **skip_May_fragile** | **ARM_SOFT** | **+0.130** | **+5.2** | 70.9% | 70% | Jun **0** · Aug **0** · tip EF **cleared** |
| skip_Wed | HOLD_SOFT | +0.111 | +4.4 | 74.7% | 70% | Jun 1 · Aug **4** |
| skip_May_OR_Wed | HOLD_SOFT | +0.203 | +8.1 | 54.4% | — | borderline ret |
| skip_FRAGILE_all | REJECT_FREQ | +0.035 | +1.4 | **45.6%** | — | kills Jun path |
| skip_Jun | **DISARM** | −0.101 | −4.1 | 74.7% | — | protect cell |

**Armed tip:** May-FRAGILE. Wed stays HOLD (Aug collateral).

---

## 3. P2-T03 — Jul / hours

| Policy | Verdict | ΔE_N | ΔEF_pp | Ret. | Note |
| --- | --- | ---: | ---: | ---: | --- |
| **skip_Jul** / MISMATCH | **ARM_SOFT** | **+0.061** | **+2.4** | 83.5% | tip EF cleared · Jun/Aug FP 0 |
| **skip_May_OR_Jul** | **ARM_SOFT** | **+0.261** | **+10.5** | **54.4%** | **primary stack** · EF +9.2 pp |
| skip_H14 | HOLD_SOFT | +0.065 | +2.6 | 72.2% | Jun 3 · Aug 4 FP |
| skip_H08 | ARM_SOFT | +0.051 | +2.0 | 89.9% | weak · small-n |
| skip_H09 | ARM_SOFT | +0.035 | +1.4 | 91.1% | weak · small-n |
| skip_H08∨H09 | HOLD_SOFT | +0.096 | +3.8 | 81.0% | — |
| skip_H14∨H08∨H09 | HOLD_SOFT | +0.234 | +9.3 | 53.2% | Aug/Jun FP risk |
| skip_H13 | **DISARM** | −0.044 | −1.8 | 79.7% | protect hour |

---

## 4. P2-T04 — SELL / near_atr

| Policy | Verdict | ΔE_N | ΔEF_pp | Ret. | Prec. | Note |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| skip_SELL_all | REJECT_FREQ | +0.134 | +5.3 | **39%** | — | BUY carries · stall |
| skip_BUY_all | **DISARM** | −0.086 | −3.5 | 61% | — | kills carrier |
| **skip_SELL_AND_May** | **ARM_SOFT** | **+0.155** | **+6.2** | **82.3%** | **86%** | narrow · no BUY FP |
| skip_SELL_AND_MayJulWed | HOLD_SOFT | +0.200 | +8.0 | 62% | — | broader |
| skip_near_atr_alone | **DISARM** | −0.061 | −2.5 | 87% | 40% | **pays on tip** |
| skip_near_atr∧MayJulWed | ARM_SOFT | +0.005 | +0.2 | 94% | — | weak additive |

**Armed additive:** SELL∧May (if lighter retention preferred over full May).  
**Never** blanket near_atr or blanket SELL.

---

## 5. P2-T05 — size table (spec only)

Wire after L4. Skip outranks size. See [`aos_l2_size_table.md`](./aos_l2_size_table.md).

| State | f_mult |
| --- | ---: |
| Expanding / Stable | 1.0 |
| Compressing | 0.5 |
| Near frontier | 0.25 |
| Below frontier | 0.0 |
| L2det WOULD_SKIP | 0.0 |

---

## 6. P2-T06 — `L2skip_jp225` (DISARM)

| Item | Value |
| --- | --- |
| Train | Jan–Apr 2026 · LogisticRegression balanced C=0.5 |
| Tip OOS AUC | **≈0.49** (coin-flip) |
| Arm | **DISARM** |
| Artifact | `infra/artefacts/models/L2skip_jp225/LATEST/` · **SHADOW_ONLY** |
| MQH export | **Not generated** |

**Read:** Pre-tip→tip transfer fails at this n/feature set. Keep det maps; revisit AI after measured Leak + structure flags + more hist.

---

## 7. P2-T07 — stack scorecard (tip)

| Stack | Verdict | ΔE_N | Ret. | Kept EF_pp | tip_EF_cleared |
| --- | --- | ---: | ---: | ---: | --- |
| P1 engine | BASELINE | 0 | 100% | **−1.26** | no |
| May-FRAGILE | ARM_SOFT | +0.130 | 70.9% | +3.91 | **yes** |
| Jul | ARM_SOFT | +0.061 | 83.5% | +1.16 | **yes** |
| **May ∨ Jul** | **ARM_SOFT** | **+0.261** | **54.4%** | **+9.19** | **yes** |
| Wed | HOLD_SOFT | +0.111 | 74.7% | +3.16 | yes |
| H14 | HOLD_SOFT | +0.065 | 72.2% | +1.31 | yes |
| May∨Jul∨Wed | REJECT_FREQ | +0.288 | **41.8%** | +10.2 | yes |
| near_atr alone | DISARM | −0.061 | 87% | −3.72 | no |
| L2AI | REJECT_FREQ / DISARM | — | — | — | AUC fail |

**Preferred research arm:** `L2det_jp225_v1_May_OR_Jul`.

---

## 8. Implementation notes (shadow)

```text
WOULD_SKIP = (month==May && ouroboros==FRAGILE) || (month==Jul)
# optional narrow: side==SELL && month==May && FRAGILE
# HOLD research only: dow==Wed · hour in {8,9,14}
# NEVER: near_atr alone · FRAGILE all · Tue/ATR/Fade re-gate · foreign pins
```

Protect false-skip on every CF: **Jun · Aug/MATCH · BUY · H13 · H15**.

---

## 9. Next

- **P3** L3/L4 guardrails + rolling health (tip path post-skip).  
- Deal-measured Leak before P7.  
- Do not MQH-arm until shadow ledger + HITL.  
- Optional: re-run CF if P1.5 engine becomes new baseline.
