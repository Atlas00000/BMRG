# AAPL M5 — L2 policy pack (P2 complete)

**Version:** 1.0.0  
**Tasks:** AAPL-M5-AOS-P2-T01 … T07  
**Date:** 2026-10-20  
**Compare window:** tip May→Oct 2026 (n=77)  
**Evidence:** `blotter/archive/AAPL-M5-AOS-P2/P2_CF.json` · `P2_SUMMARY.json`  
**Costs:** Leak profile authority **15.3 pp** · P1 2× journal **12.34 pp** (measured OPEN)  
**Mode:** L2det v1b **HITL RESEARCH ARMED** (`AAPL_5m_stack` · magic **26162017**) · L2 AI **DISARM** · no geometry change · no M15 Thu/18 pin  
**Baseline:** [`AAPL_M5_AOS_BASELINE_v1.md`](./AAPL_M5_AOS_BASELINE_v1.md)  
**Roadmap:** [`aios_roadmap_M5.md`](./aios_roadmap_M5.md)  
**Wire:** `Include/AOS_L2det_aapl_m5.mqh` · presets magic **26162011** / **26162012**

---

## 0. Armed map summary

| ID | Rule | Status |
| --- | --- | --- |
| `L2det_aapl_m5_v1_Jul` | Skip if month==Jul | **ARM_SOFT** (nested in v1b) |
| `L2det_aapl_m5_v1_Wed` | Skip if DOW==Wed | **ARM_SOFT** (nested in v1b) |
| **`L2det_aapl_m5_v1b_stack`** | **Jul ∨ Wed** | **ARM_SOFT** (preferred) |
| `L2det_aapl_m5_v1_H18` | Skip if hour==18 | **HOLD** (ΔE_N +0.06 alone · 2 May FP in Jul∨H18) |
| `L2det_aapl_m5_v1_spread30` | Skip if spread≥30 | **HOLD** optional · tip saturated |
| `L2det_aapl_m5_v1_H1` | Skip Jan–Apr | **HOLD** YTD only (tip NO_OP) |
| Jul ∨ Wed ∨ H18 / +spread | — | **REJECT_FREQUENCY_STALL** |
| Permanent skip BUY / May / Mon | — | **REJECT / DISARM** |
| `L2skip_aapl_m5` AI | prior-fit LR | **DISARM** (AUC_tip≈0.50) |

---

## 1. P2-T01 — parity

| Check | Tip | YTD |
| --- | ---: | ---: |
| Tue fires | 0 | 0 |
| ATR &gt; 98 | 0 | 0 |
| BBw out of 0.30–2.00 | 0 | 0 |
| Verdict | **PASS** | **PASS** |

Do not re-gate Tue / ATR / BBw in L2det.

---

## 2. P2-T02 — Wed ± spread / H18

| Policy | ΔE_N | Ret. | Prec. | May FP | Mon FP | Verdict |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| skip_Wed | +0.080 | 67.5% | 60% | 1 | 0 | **ARM_SOFT** |
| skip_spread≥30 | +0.080 | 70.1% | 61% | 1 | 0 | **ARM_SOFT** weak |
| Wed ∧ spread | +0.027 | 89.6% | 62% | 0 | 0 | ARM_SOFT thin |
| skip_H18 | +0.060 | 79.2% | 62% | 2 | 1 | **HOLD** |
| Wed ∨ H18 | +0.142 | 52.0% | 59% | 3 | 1 | HOLD / thin ret |

---

## 3. P2-T03 — Jul / H1 / side

| Policy | ΔE_N | Ret. | Prec. | May/Mon FP | Verdict |
| --- | ---: | ---: | ---: | --- | --- |
| **skip_Jul** | **+0.160** | **80.5%** | **80%** | 0 / 0 | **ARM_SOFT** |
| **Jul ∨ Wed** | **+0.193** | **57.1%** | **64%** | 1 / 0 | **ARM_SOFT preferred** |
| Jul ∨ H18 | +0.257 | 63.6% | 71% | **2** / 1 | **HOLD** (May FP) |
| Jul ∨ Wed ∨ H18 | +0.299 | **44.2%** | 63% | 3 / 1 | **REJECT_FREQUENCY_STALL** |
| YTD skip_H1 | +0.201 | 53.1% | 71% | 0 / 7 Mon | **HOLD** seasonal |
| skip_BUY / May / Mon | neg | — | — | protect hit | **REJECT** |

---

## 4. Preferred stack — v1b

```text
SKIP if (month == Jul)  OR  (DOW == Wed)
```

| | Baseline tip | After v1b |
| --- | ---: | ---: |
| n | 77 | **44** |
| WR | 46.8% | **~54.5%** |
| E_N | +0.157R | **+0.349R** |
| ΔE_N / ΔEF_profile | — | **+0.193R / +7.8 pp** |
| Retention | 100% | **57.1%** |
| Prec. losers | — | **63.6%** |
| May / Mon winner FP | — | **1 / 0** |

Optional toggles (OFF in presets): H18 · spread≥30 · H1.

---

## 5. P2-T04 — size table

See [`aos_l2_size_table_M5.md`](./aos_l2_size_table_M5.md) — spec only; wire after L4.

---

## 6. P2-T05/T06 — L2 AI

| Item | Result |
| --- | --- |
| Train | prior Jan–Apr n=68 · avoid-loser LR |
| AUC tip OOS | **≈0.50** |
| Best thr tip ΔE_N | &lt; +0.02 bar |
| Verdict | **DISARM** — artifact under `infra/artefacts/models/L2skip_aapl_m5/LATEST/` shadow-only |

---

## 7. P2-T07 — wire

| Piece | Path |
| --- | --- |
| Include | `Include/AOS_L2det_aapl_m5.mqh` |
| Router | `Include/AOS.mqh` — Apple **M5** before M15 path |
| Inputs | `InpAOS_AAPL_M5_*` in `Config.mqh` |
| Shadow `.set` | `AAPL-M5-AOS-P2-T02_L2det_JulWed_shadow_Balanced.set` · **26162011** |
| Live `.set` | `AAPL-M5-AOS-P2-T02_L2det_JulWed_live_Balanced.set` · **26162012** |

M15 `InpAOS_AAPL_L2detEnable` stays **false** on M5 runs.
