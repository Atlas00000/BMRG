# EURUSD M15 — L2 policy pack (P2 complete)

**Version:** 1.0.0  
**Tasks:** EURUSD-AOS-P2-T01 … T07  
**Date:** 2026-10-18  
**Compare window:** tip May→Oct 2026 (n=45)  
**Evidence:** `blotter/archive/EURUSD-AOS-P2/P2_CF.json`  
**Costs:** `Leak_source=journal_2x_entry_spread_median` (1.19 pp)  
**Mode:** L2det v1b **RESEARCH ARMED** (P7 HITL · magic **26121807**) · L2 AI still **DISARM** · no geometry change · no foreign L2 pin  
**Sign-off:** [`AIOS_SIGNOFF.md`](./AIOS_SIGNOFF.md)  

---

## 0. Armed map summary

| ID | Rule | Status |
| --- | --- | --- |
| `L2det_eur_m15_v1_Thu` | Skip if DOW=Thu | **ARM_SOFT** (primary atom) |
| `L2det_eur_m15_v1_BUY_near_atr` | Skip if BUY ∧ atr≥0.9×74 | **ARM_SOFT** (additive) |
| `L2det_eur_m15_v1_BUY_H13` | Skip if BUY ∧ hour=13 | **ARM_SOFT** (alt atom · tip-clean) |
| `L2det_eur_m15_v1b_stack` | Thu **OR** (BUY∧near_atr) | **ARM_SOFT** (**preferred** shadow stack) |
| `L2det_eur_m15_v1_H19` | Skip if hour=19 | **ARM_SOFT** thin · optional |
| H13 alone / Thu∨H13 | — | **HOLD_SOFT** (SELL/MonFri collateral) |
| Permanent skip BUY | — | **DISARM** (FREQUENCY_STALL · ret 49%) |
| Blanket near_atr | — | **DISARM** on tip |
| skip_Aug alone | — | **HOLD_SOFT** (MonFri/SELL FP) |
| `L2skip_eur_m15` AI | pre-tip LR | **DISARM** (chrono holdout DISARM · tip thr optimistic) |

---

## 1. P2-T01 — parity

Tue fires = **0** · ATR>74 fires = **0** → **PASS**. Do not re-gate Tue/ATR in L2det.

---

## 2. P2-T02 — Thu / H13 / H19

| Policy | Verdict | ΔE_N | Ret. | Prec. | Collateral |
| --- | --- | ---: | ---: | ---: | --- |
| **skip_Thu** | **ARM_SOFT** | +0.045 | 82% | 63% | 1 SELL · 0 MonFri |
| skip_H13 | HOLD_SOFT | +0.045 | 82% | 63% | 2 SELL · 1 MonFri |
| **skip_H19** | **ARM_SOFT** | +0.021 | 93% | 67% | 0 SELL · 1 MonFri (n=3) |
| skip_Thu∨H13 | HOLD_SOFT | +0.150 | 67% | 67% | 3 SELL |
| skip_Thu∨H19 | ARM_SOFT | +0.043 | 78% | 60% | 1 SELL · 1 MonFri |

**Armed primary atom:** `L2det_eur_m15_v1_Thu`.

---

## 3. P2-T03 — buy-caution

| Policy | Verdict | ΔE_N | Ret. | Prec. | Collateral |
| --- | --- | ---: | ---: | ---: | --- |
| skip_BUY | **REJECT_FREQUENCY_STALL** | +0.18 | 49% | 61% | 4 MonFri FP |
| skip_BUY_if_Thu | ARM_SOFT | +0.019 | 89% | 60% | Nested in Thu |
| **skip_BUY_if_H13** | **ARM_SOFT** | **+0.048** | 91% | **75%** | 0 SELL · 0 MonFri |
| **skip_BUY_if_near_atr** | **ARM_SOFT** | **+0.045** | 82% | 63% | 0 SELL · 0 MonFri |
| skip_BUY_if_H19 | ARM_SOFT | +0.021 | 93% | 67% | 1 MonFri |

**Armed additive (preferred with Thu):** `L2det_eur_m15_v1_BUY_near_atr`.  
**Alt additive:** `BUY∧H13` (cleaner prec; keep for stack experiments).  
**Preferred stack:** `L2det_eur_m15_v1b` = Thu **OR** (BUY∧near_atr) → tip kept E_N **+0.234R** · ΔE_N **+0.184R** · ret **68.9%** · prec **71%** · **1 SELL / 0 MonFri FP**.

---

## 4. P2-T04 — stress cells

| Policy | Verdict | ΔE_N | Ret. | Prec. | Note |
| --- | --- | ---: | ---: | ---: | --- |
| skip_Aug | HOLD_SOFT | +0.016 | 84% | 57% | 3 SELL + 3 MonFri FP |
| skip_near_atr_cap (all) | **DISARM** | −0.005 | 62% | 53% | Use BUY∧near_atr instead |
| Feb on tip | N/A | — | — | — | Empty |
| Feb on YTD | HOLD_SOFT | +0.068 | 86% | — | Diagnostic L3 — not tip arm |

**Armed tip stress calendar:** none (Aug too collateral-heavy). Prefer path features over month hardcode.

---

## 5. P2-T05 — size table (spec only)

Wire after L4. Skip outranks size. See [`aos_l2_size_table.md`](./aos_l2_size_table.md).

---

## 6. P2-T06 — `L2skip_eur_m15` (DISARM)

| Item | Value |
| --- | --- |
| Train | pre-tip Jan–Apr (YTD) · LogisticRegression balanced C=0.5 |
| Tip OOS AUC | **≈0.58** |
| Best thr on tip | 0.65 → ARM_SOFT on tip-swept CF (ΔE_N +0.14 · prec 78% · 0 SELL FP) |
| Chrono holdout (last 40% tip) | **DISARM** (ΔE_N −0.10 · prec 33%) |
| Artifact | `infra/artefacts/models/L2skip_eur_m15/LATEST/` · **SHADOW_ONLY** |
| MQH export | **Not generated** |

**Read:** Tip-swept thr overfits. Keep det maps; revisit AI after measured Leak + more hist / features.

---

## 7. P2-T07 — stack scorecard (tip)

| Stack | Kept E_N | ΔE_N | Ret. | Verdict |
| --- | ---: | ---: | ---: | --- |
| P0 engine | +0.050R | — | 100% | BASELINE |
| **L2det v1b** (Thu∨BUY∧near_atr) | **+0.234R** | **+0.184** | 68.9% | **ARM_SOFT** (preferred) |
| L2AI only (thr 0.65) | +0.188R | +0.138 | 80% | tip ARM / holdout **DISARM** |
| L2det OR L2AI | +0.385R | +0.335 | 57.8% | ARM_SOFT but thin ret · defer |
| L2det AND L2AI | +0.098R | +0.048 | 91% | weaker than v1b alone |

**Research shadow arm:** L2det **v1b** only. Do not LIVE_WITHHOLD L2AI until holdout+measured Leak clear.

---

## 8. Explicit non-actions

- Do not permanently disable BUY.  
- Do not blanket near_atr or re-stack P1 BBw.  
- Do not pin M5 / AUD / UK100 L2 models.  
- Do not change SL/TP/BB/CD/ATR max as “OS”.  
- Do not promote on Leak prior; journal proxy OK for shadow CF only.
