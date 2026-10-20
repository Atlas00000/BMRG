# USDJPY — L2 policy pack (P2 complete)

**Version:** 1.0.0  
**Tasks:** USDJPY-AOS-P2-T01 … T07  
**Date:** 2026-10-19  
**Compare window:** tip filter May→Aug 2026 from long 2025.01→2026.10.18 (**n=46**, path-dep vs dedicated n=56)  
**Evidence:** `blotter/archive/USDJPY-AOS-P2/P2_CF.json`  
**Costs:** `Leak_source=prior_11.4pp` (authority) · journal proxy **3.6 pp** reported only  
**Mode:** L2det **SHADOW / RESEARCH** · L2 AI **SHADOW_ONLY** · no geometry change · no foreign L2 pin · no research OS arm yet  

---

## 0. Armed map summary

| ID | Rule | Status |
| --- | --- | --- |
| `L2det_usdjpy_v1_near_atr` | Skip if `near_atr_cap` | **ARM_SOFT** (primary slim) |
| `L2det_usdjpy_v1c_near_atr_OR_H16` | Skip if near_atr **OR** hour=16 | **ARM_SOFT** (preferred research stack) |
| `L2det_usdjpy_v1_SELL_near_atr` | Skip if SELL ∧ near_atr | **ARM_SOFT** (sell-caution; nested in near_atr) |
| `L2det_usdjpy_v1_H16` | Skip if hour=16 | **ARM_SOFT** (thin n=3 · zero protect FP) |
| `L2det_usdjpy_v1_Jul` | Skip if month=Jul | **HOLD_SOFT** (ΔE_N+ · BUY/Fri/H12·H15 FP) |
| `L2det_usdjpy_v1a_Jul_OR_near_atr` | Jul **OR** near_atr | **HOLD_SOFT** (best ΔE_N · ret 61% · protect FP) |
| `L2det_usdjpy_v1b_Jul_OR_SELL_near_atr` | Jul **OR** (SELL∧near_atr) | **HOLD_SOFT** |
| Thu / Thu∨H14 | — | **DISARM** (ΔE_N− · path-flip vs dedicated tip) |
| H14 alone | — | **HOLD_SOFT** (flat ΔE_N · BUY FP) |
| Blanket SELL | — | **REJECT_FREQUENCY_STALL** (ret 39%) |
| `L2skip_usdjpy` AI | tip-internal LR | **SHADOW_ONLY** — tip CF ARM_SOFT but train overlaps tip; **do not LIVE_WITHHOLD** |

---

## 1. P2-T01 — parity

| Check | Result |
| --- | --- |
| Tue fires | **0** → **PASS** |
| atr > 70 on tape | **0** → **PASS** |
| near_atr_cap tip / YTD | present (stress feature OK) |

Do **not** re-gate Tue / ATR max inside L2det.

---

## 2. P2-T02 — Thu / H14 / H16

### Tip (primary)

| Policy | Verdict | ΔE_N | Ret. | Prec. | Protect FP (BUY/Fri/H12/H15/May/Jun) |
| --- | --- | ---: | ---: | ---: | --- |
| skip_Thu | **DISARM** | −0.030 | 80.4% | 44% | BUY 2 · Fri 0 · H12 3 · H15 1 · May 0 · **Jun 4** |
| skip_H14 | HOLD_SOFT | 0.0 | 82.6% | 50% | BUY **3** · Fri 1 · May 2 · Jun 2 |
| **skip_H16** | **ARM_SOFT** | **+0.077** | **93.5%** | **100%** | **all 0** |
| skip_Thu∨H14 | DISARM | −0.107 | 67.4% | — | — |

### YTD (support)

| Policy | Verdict | ΔE_N | Ret. | Note |
| --- | --- | ---: | ---: | --- |
| skip_Jul | HOLD_SOFT | +0.208 | 74.1% | Same as tip — calendar stress holds |
| skip_Thu | (see tip) | — | — | Do not ARM Thu from this path |

**Armed tip:** **H16** only from T02. Thu stays DISARM (confirms P1 path-flip).

---

## 3. P2-T03 — sell-caution

| Policy | Verdict | ΔE_N | Ret. | Prec. | Collateral |
| --- | --- | ---: | ---: | ---: | --- |
| skip_SELL | **REJECT_FREQUENCY_STALL** | +0.122 | **39.1%** | — | Kills fire rate |
| **skip_SELL∧near_atr** | **ARM_SOFT** | **+0.105** | **91.3%** | **100%** | Protect FP **0** |
| skip_SELL∧Thu | HOLD_SOFT | 0.0 | 87.0% | — | Nested flat |
| skip_SELL∧H14 | ARM_SOFT | +0.052 | 91.3% | — | Weaker than near_atr |
| skip_SELL∧Jul | ARM_SOFT | +0.085 | 84.8% | — | Calendar nested |

**Armed additive:** `L2det_usdjpy_v1_SELL_near_atr`. Never permanent `AllowSell=false`.

---

## 4. P2-T04 — stress / near-ATR

| Policy | Verdict | ΔE_N | Ret. | Prec. | Protect FP |
| --- | --- | ---: | ---: | ---: | --- |
| skip_Jul | HOLD_SOFT | +0.206 | 69.6% | 71% | BUY 2 · Fri 1 · H12 1 · H15 2 |
| **skip_near_atr** | **ARM_SOFT** | **+0.197** | **84.8%** | **100%** | **all 0** |
| Jul∨near_atr (v1a) | HOLD_SOFT | **+0.393** | 60.9% | 78% | same Jul FP |
| Jul∨SELL∧near_atr (v1b) | HOLD_SOFT | +0.293 | 65.2% | — | Jul FP |
| **near_atr∨H16 (v1c)** | **ARM_SOFT** | **+0.268** | **80.4%** | **100%** | **all 0** |

**Armed:** near_atr (slim) · v1c (preferred stack). Jul / v1a / v1b stay HOLD challengers until protect FP drops or non-calendar features join.

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

## 6. P2-T06 — `L2skip_usdjpy` (SHADOW_ONLY)

| Item | Value |
| --- | --- |
| Train | Tip first 60% (May–Jun) — YTD Jan–Apr too thin (n&lt;12) |
| Tip AUC | **0.75** (optimistic — train overlaps tip) |
| Holdout (last 40% tip) | ARM_SOFT · AUC **0.55** · ΔE_N +0.19 |
| Best thr | 0.55 · tip ret 63% · BUY/Fri FP **0** |
| Artifact | `infra/artefacts/models/L2skip_usdjpy/LATEST/` · **SHADOW_ONLY** |
| MQH export | **Not generated** |

**Read:** Tip CF looks ARM_SOFT, but train is path-contaminated and holdout AUC is coin-flip+. Keep det maps as authority. Revisit AI after measured Leak + pre-tip train window + structure flags. **Do not LIVE_WITHHOLD.**

---

## 7. P2-T07 — stack scorecard (tip)

| Stack | Kept E_N | ΔE_N | Ret. | Verdict |
| --- | ---: | ---: | ---: | --- |
| P0 enginedet | +0.100R | — | 100% | BASELINE |
| L2det_Thu | +0.070R | −0.030 | 80.4% | **DISARM** |
| L2det_H14 | +0.100R | 0.0 | 82.6% | HOLD_SOFT |
| L2det_H16 | +0.177R | +0.077 | 93.5% | ARM_SOFT |
| L2det_Jul | +0.306R | +0.206 | 69.6% | HOLD_SOFT |
| **L2det_near_atr** | **+0.297R** | **+0.197** | **84.8%** | **ARM_SOFT** |
| L2det_SELL∧near_atr | +0.205R | +0.105 | 91.3% | ARM_SOFT |
| Jul∨near_atr (v1a) | +0.493R | +0.393 | 60.9% | HOLD_SOFT |
| Jul∨SELL∧near_atr (v1b) | +0.393R | +0.293 | 65.2% | HOLD_SOFT |
| **near_atr∨H16 (v1c)** | **+0.368R** | **+0.268** | **80.4%** | **ARM_SOFT** |
| L2AI only | +0.593R | +0.493 | 63.0% | SHADOW (train overlap) |
| v1b∨L2AI | +0.886R | +0.786 | **45.7%** | REJECT_FREQUENCY_STALL |

**Preferred research stack:** arm **`L2det_usdjpy_v1c = near_atr OR H16`** for shadow CF / future OS wiring. Slim fallback = **near_atr alone**. Keep **Jul / v1a / v1b** as HOLD challengers (higher ΔE_N, protect FP + thinner ret).

---

## 8. Protect-cell discipline

False-skip on **BUY / Fri / H12 / H15 / May / Jun** must be reported every CF.  
Armed maps (near_atr · H16 · v1c · SELL∧near_atr) scored **0** protect FP on tip.  
Jul stacks still tax BUY/Fri/H12·H15 — do not hard-arm Jul from this tape alone.

---

## 9. Next

- Optional: deal-measured Leak before hard OS arm  
- P3 L3/L4 with **v1c** overlay in shadow  
- Do not pin EUR/UK/AUD/DE40 L2 models  
- Do not thin SL / lift ATR max / reopen Tokyo as “OS”  
- Do not LIVE_WITHHOLD L2AI until clean pre-tip train  
