# JP225 / JPN225 M5 — L2 policy pack (P2 complete)

**Version:** 1.0.0  
**Tasks:** JP225-M5-AOS-P2-T01 … T08  
**Date:** 2026-10-20  
**Compare window:** tip May→Oct 2026 (n=94 · →10.19) · YTD support for Feb/Apr  
**Evidence:** `blotter/archive/JP225-M5-AOS-P2/P2_CF.json` · `P2_SUMMARY.json`  
**Costs:** `Leak_source=prior_3.3pp` (authority) · journal proxy ≈3.7 pp reported only  
**Mode:** L2det v1c **ARM_SOFT** (research enable default **false**) · L2 AI **DISARM** · no geometry change · no M15 `AOS_L2det_jp` pin on M5  
**Baseline:** [`JP225_M5_AOS_BASELINE_v1.md`](./JP225_M5_AOS_BASELINE_v1.md)  
**Roadmap:** [`aios_roadmap_M5.md`](./aios_roadmap_M5.md)  
**Wire:** `Include/AOS_L2det_jp_m5.mqh` · Config `InpAOS_JP_M5_*`

---

## 0. Armed map summary

| ID | Rule | Status |
| --- | --- | --- |
| `L2det_jp225_m5_v1_BuyMatch` | Skip if BUY ∧ ouroboros MATCH (Aug/Sep) | **ARM_SOFT** (nested in v1c) |
| `L2det_jp225_m5_v1_BuyH09_13_16` | Skip if BUY ∧ hour∈{9,13,16} | **ARM_SOFT** (nested in v1c) |
| **`L2det_jp225_m5_v1c_stack`** | **(BUY∧MATCH) ∨ (BUY∧H09\|13\|16)** | **ARM_SOFT** (**preferred**) |
| `L2det_jp225_m5_v1_MATCH` | Skip if MATCH (all sides) | **HOLD** (6 SELL FP) |
| `L2det_jp225_m5_v1_Sep` / `Aug` | Calendar all sides | **HOLD** / nested prefer BUY∧ |
| Blanket BUY / Mon / H09\|13\|16 all | — | **REJECT** (Jul / OFFHOME FP) |
| Blanket FRAGILE / MISMATCH / near_atr | — | **REJECT** (kills home) |
| Feb / Apr (YTD only) | Soft months | **ARM_SOFT on YTD** — not tip calendar |
| `L2skip_jp225_m5` AI | prior→tip LR | **DISARM** (AUC_tip≈0.49) |

---

## 1. P2-T01 — parity

| Check | Tip | YTD |
| --- | ---: | ---: |
| Tue fires | 0 | 0 |
| ATR outside band 7610–11285 | 0 | 0 |
| Verdict | **PASS** | **PASS** |

Do not re-gate Tue / ATR band in L2det.

---

## 2. P2-T02 — MATCH months (primary tax)

| Policy | ΔE_N | Ret. | Prec. | Jul FP | SELL FP | Verdict |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| skip_Aug | +0.080 | 81.9% | 71% | 0 | 3 | **ARM_SOFT** / prefer BUY∧ |
| skip_Sep | +0.119 | 81.9% | 76% | 0 | 3 | **ARM_SOFT** / prefer BUY∧ |
| skip_MATCH | +0.255 | 63.8% | 74% | 0 | **6** | **HOLD** (SELL FP) |
| **skip_BUY ∧ MATCH** | **+0.140** | **83.0%** | **81%** | **0** | **0** | **ARM_SOFT** |

---

## 3. P2-T03 — DOW / hour soft

| Policy | ΔE_N | Ret. | Prec. | Jul FP | OFF FP | Verdict |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| skip_Wed | +0.089 | 76.6% | 68% | 1 | 3 | **HOLD** |
| skip_Mon | +0.084 | 74.5% | 67% | **4** | 7 | **REJECT_PROTECT_FP** |
| skip_H09\|13\|16 all | +0.255 | 66.0% | 75% | **2** | 5 | **REJECT_PROTECT_FP** |
| **skip_BUY ∧ H09\|13\|16** | **+0.119** | **81.9%** | **76%** | 1 | 2 | **ARM_SOFT** |

---

## 4. P2-T04 — side / regime

| Policy | ΔE_N | Ret. | Note | Verdict |
| --- | ---: | ---: | --- | --- |
| skip_BUY | +0.193 | **51%** | Jul FP 5 · H10 FP 5 | **REJECT** |
| skip_SELL | — | — | Carrier | **DISARM** |
| skip_FRAGILE_all | −0.026 | 68% | Kills Jun | **REJECT** |
| skip_MISMATCH_all | −0.213 | 68% | Kills Jul | **REJECT** |
| skip_near_atr_all | −0.019 | 76% | H10 FP | **REJECT** |
| ytd_skip_Feb / Apr | +0.05…+0.07 | 92% | Support | **ARM_SOFT YTD** |

---

## 5. Preferred stack — v1c

```text
SKIP if (BUY ∧ MATCH)  OR  (BUY ∧ hour ∈ {9,13,16})
```

MATCH = Ouroboros tag Aug/Sep (month∈{8,9} on tip map).

| | Baseline tip | After v1c |
| --- | ---: | ---: |
| n | 94 | **69** |
| WR | 41.5% | **49.3%** |
| E_N | +0.245R | **+0.478R** |
| EF_prior | +4.86 pp | **+12.64 pp** |
| ΔE_N / ΔEF | — | **+0.234R / +7.79 pp** |
| Retention | 100% | **73.4%** |
| Prec. losers | — | **80.0%** |
| Jul / SELL / H08 / H10 FP | — | **1 / 0 / 0 / 0** |

**Why not blanket MATCH (max ΔE_N among HOLD):** 6 SELL winner FP — tip is sell-led; protect overrides.  
**Why not MATCH∨Wed / all-hour:** Jul / OFFHOME / SELL collateral.  
**Safer nested leg alone:** BUY∧MATCH (ΔE_N +0.140 · zero protect FP) — keep as fallback if v1c Jul FP worries in P6.

**Not armed:** blanket BUY · Mon · all-side hours · FRAGILE · MISMATCH · near_atr · M15 May∨Jul.

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

## 7. P2-T07/T08 — L2 AI

| Item | Result |
| --- | --- |
| Pin | `L2skip_jp225_m5` |
| Train | prior Jan–Apr n=36 → tip OOS |
| AUC tip | **≈0.49** |
| Best thr ΔE_N | thin (+0.04 · n_skip=3) |
| Verdict | **DISARM** — do not LIVE_WITHHOLD |

Stack + AI does not beat clean v1c on protect FP; leave AI shadow-only.

---

## 8. Wire / enable

| Input | Default | Role |
| --- | --- | --- |
| `InpAOS_JP_M5_L2detEnable` | **false** | Master M5 gate |
| `InpAOS_JP_M5_SkipBuyMatch` | true | v1c leg |
| `InpAOS_JP_M5_SkipBuyH09_13_16` | true | v1c leg |
| `InpAOS_JP_M5_SkipMatchAll` | false | Optional aggressive (SELL FP) |

M15 `InpAOS_JP_L2detEnable` is now gated `Period() != PERIOD_M5` so May∨Jul never runs on M5.
