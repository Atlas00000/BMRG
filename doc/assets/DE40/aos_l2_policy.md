# DE40 — L2 policy pack (P2 complete)

**Version:** 1.0.0  
**Tasks:** DE40-AOS-P2-T01 … T07  
**Date:** 2026-10-19  
**Compare window:** tip May→Oct 2026 (n=77) · YTD support for Feb  
**Evidence:** `blotter/archive/DE40-AOS-P2/P2_CF.json`  
**Costs:** `Leak_source=prior_9.8pp` (authority) · journal proxy 1.5 pp reported only  
**Mode:** L2det **RESEARCH ARMED** (P7 HITL · **DE40stack** · magic **26141907**) · L2 AI still **DISARM** · no geometry change · no foreign L2 pin  

---

## 0. Armed map summary

| ID | Rule | Status |
| --- | --- | --- |
| `L2det_de40_v1_BUY_near_atr` | Skip if BUY ∧ atr≥0.9×4070 | **ARMED** research OS (`DE40stack` · `AOS_L2det_de.mqh`) |
| `L2det_de40_v1_H13` | Skip if hour=13 | **HOLD_SOFT** (ΔE_N+ · Aug FP) |
| `L2det_de40_v1b_stack` | H13 **OR** (BUY∧near_atr) | **HOLD_SOFT** (best ΔE_N · more Aug FP) |
| `L2det_de40_v1_Feb` | Skip if month=Feb | **ARM_SOFT on YTD only** — not tip calendar arm |
| `L2det_de40_v1_Mar` | Skip if month=Mar | **ARM_SOFT on YTD** (thin n) |
| Blanket MISMATCH / Sep–Oct | — | **DISARM** (May collateral / tip FRAGILE still +) |
| Permanent skip BUY | — | **DISARM** (ret≈52% · SELL carries tip) |
| Blanket near_atr | — | **HOLD/DISARM** — use BUY∧near_atr |
| `L2skip_de40` AI | YTD→tip LR | **DISARM** (AUC_tip≈0.51) |

---

## 1. P2-T01 — parity

| Check | Result |
| --- | --- |
| Tue fires | **0** → **PASS** |
| atr > 4070 on tape | **0** → **PASS** |
| near_atr_cap tip / YTD | present (stress feature OK) |

Do **not** re-gate Tue / ATR max inside L2det.

---

## 2. P2-T02 — H13 / Feb

### Tip (primary)

| Policy | Verdict | ΔE_N | Ret. | Prec. | Protect FP (Aug/SELL/Mon/H08) |
| --- | --- | ---: | ---: | ---: | --- |
| **skip_H13** | **HOLD_SOFT** | **+0.070** | 84.4% | 58% | Aug **3** · SELL 2 · Mon 1 · H08 0 |
| skip_Feb | N/A_EMPTY | — | — | — | no Feb on tip |
| skip_Wed | HOLD_SOFT | +0.050 | 79.2% | — | weaker than H13 |

### YTD (support)

| Policy | Verdict | ΔE_N | Ret. | Prec. |
| --- | --- | ---: | ---: | ---: |
| **skip_Feb** | **ARM_SOFT** | **+0.088** | 80.3% | 66% |
| skip_Feb_OR_H13 | HOLD_SOFT | +0.110 | 71.4% | — |
| skip_Mar | ARM_SOFT | +0.032 | 97.3% | thin |

**Armed tip:** none from T02 alone (H13 stays HOLD until Aug FP falls or conjunction).  
**Armed YTD-path research:** Feb SOFT for support-window CF / L3 path — **do not** hardcode Feb into multi-year live without non-calendar features.

---

## 3. P2-T03 — buy-caution

| Policy | Verdict | ΔE_N | Ret. | Prec. | Collateral |
| --- | --- | ---: | ---: | ---: | --- |
| skip_BUY | HOLD_SOFT | +0.091 | **51.9%** | — | Near FREQUENCY_STALL · **DISARM** for arm |
| skip_BUY_if_H13 | HOLD_SOFT | +0.055 | 89.6% | — | Nested |
| **skip_BUY_if_near_atr** | **ARM_SOFT** | **+0.100** | **80.5%** | **60%** | Aug 1 · **SELL 0** · Mon 3 · H08 2 |
| skip_BUY_if_fragile | HOLD_SOFT | +0.022 | 89.6% | — | Weak |

**Armed additive:** `L2det_de40_v1_BUY_near_atr`.

---

## 4. P2-T04 — regime / FRAGILE

| Policy | Verdict | ΔE_N | Ret. | Note |
| --- | --- | ---: | ---: | --- |
| skip_MISMATCH_all | **DISARM** | −0.025 | 88% | Kills May tip wins |
| skip_MISMATCH_not_May | N/A_EMPTY | — | — | Tip MISMATCH = May only |
| skip_FRAGILE_all | HOLD_SOFT | +0.035 | 78% | Sep still + under ATR |
| skip_near_atr_cap (all) | HOLD_SOFT | +0.053 | 66% | Prefer BUY∧near_atr |
| skip_FRAGILE_and_near_atr | HOLD_SOFT | +0.022 | 90% | Weak additive |
| skip_Sep_Oct | HOLD_SOFT | +0.035 | 78% | Same as FRAGILE_all |

**Armed:** none as standalone tip calendar. Prefer BUY∧near_atr over blanket FRAGILE.

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

## 6. P2-T06 — `L2skip_de40` (DISARM)

| Item | Value |
| --- | --- |
| Train | Jan–Apr 2026 YTD slice · LogisticRegression balanced C=0.5 |
| Tip OOS AUC | **≈0.51** (coin-flip) |
| Best thr on tip | HOLD_SOFT at best · no ARM with AUC≥0.55 |
| Artifact | `infra/artefacts/models/L2skip_de40/LATEST/` · **SHADOW_ONLY · not armed** |
| MQH export | **Not generated** |

**Read:** Pre-tip→tip transfer fails at this n/feature set. Keep det maps; revisit AI after measured Leak + structure flags + more hist.

---

## 7. P2-T07 — stack scorecard (tip)

| Stack | Kept E_N | ΔE_N | Ret. | Verdict |
| --- | ---: | ---: | ---: | --- |
| P0 engine | +0.315R | — | 100% | BASELINE |
| L2det_H13 | +0.385R | +0.070 | 84.4% | HOLD_SOFT |
| **L2det_BUY_near_atr** | **+0.415R** | **+0.100** | **80.5%** | **ARM_SOFT** |
| H13 ∨ BUY∧near_atr (v1b) | +0.486R | +0.171 | 68.8% | HOLD_SOFT (Aug FP) |
| H13 ∨ FRAGILE∧near_atr | +0.397R | +0.082 | 75.3% | HOLD_SOFT |
| L2AI only | — | — | — | **DISARM** |
| v1b ∨ L2AI | +0.519R | +0.204 | 51.9% | HOLD (stall edge) |

**Preferred research stack:** arm **BUY∧near_atr** alone for shadow CF / future OS wiring. Keep **H13** and **v1b** as HOLD challengers (higher ΔE_N, more Aug collateral).

---

## 8. Protect-cell discipline

False-skip on **Aug / SELL / Mon / H08** must be reported every CF.  
UK **H08-soft** map does **not** transfer — DE40 H08 is a tip star.

---

## 9. Next

- Optional: deal-measured Leak before hard OS arm  
- P3 L3/L4 with BUY∧near_atr overlay in shadow  
- Do not pin EUR/UK/USDJPY L2 models  
- Do not thin SL / lift ATR max as “OS”
