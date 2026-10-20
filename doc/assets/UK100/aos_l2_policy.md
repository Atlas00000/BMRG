# UK100 — L2 policy pack (P2 complete)

**Version:** 1.1.0  
**Tasks:** UK100-AOS-P2-T01 … T07  
**Date:** 2026-10-12  
**Compare window:** tip May→Aug 2026 (n=51)  
**Evidence:**  
- `blotter/archive/UK100-AOS-P2-T02/SHADOW_CF.json` (T01–T02)  
- `blotter/archive/UK100-AOS-P2-REMAINING/P2_REMAINING_CF.json` (T03–T07)  
**Costs:** `Leak_source=journal_2x_entry_spread_median` (4.27 pp)  
**Mode:** L2det v1b **RESEARCH ARMED** (P7 HITL · magic **26111307**) · L2 AI still **DISARM** · no geometry change · no foreign L2 pin  
**Sign-off:** [`AIOS_SIGNOFF.md`](./AIOS_SIGNOFF.md)

---

## 0. Armed map summary

| ID | Rule | Status |
| --- | --- | --- |
| `L2det_uk_v1_Thu` | Skip if DOW=Thu | **ARM_SOFT** (primary) |
| `L2det_uk_v1_BUY_near_atr` | Skip if BUY ∧ atr≥0.9×1470 | **ARM_SOFT** (additive) |
| `L2det_uk_v1_Jul` | Skip if month=Jul | **ARM_SOFT** (calendar seed · tip only) |
| `L2det_uk_v1b_stack` | Thu **OR** (BUY∧near_atr) | **ARM_SOFT** (preferred shadow stack) |
| `L2det_uk_v1_BUY_H08` | Skip if BUY ∧ hour=08 | **HOLD** (strong tip · 1 Wed FP) |
| H08 alone / Thu∨H08 | — | **DISARM / deferred** |
| Permanent skip BUY | — | **DISARM** (prior BUY was the edge) |
| Blanket near_atr | — | **DISARM** on tip |
| `L2skip_uk` AI | prior-fit LR | **DISARM** (AUC_tip≈0.39 · no thr ARM) |

---

## 1. P2-T01 — parity (unchanged)

Tue fires = 0 · ATR>1470 fires = 0 → **PASS**. Do not re-gate Tue/ATR in L2det.

---

## 2. P2-T02 — Thu (primary)

| | Baseline tip | After skip_Thu |
| --- | ---: | ---: |
| n | 51 | 38 |
| WR | 49.0% | 55.3% |
| E_N | +0.103R | **+0.243R** |
| EF_proxy | +0.31 pp | **+6.55 pp** |
| Prec. losers | — | 69.2% |
| Wed/SELL winners skipped | — | **0 / 0** |

---

## 3. P2-T03 — buy-caution

| Policy | Verdict | ΔE_N | Ret. | Prec. | Collateral |
| --- | --- | ---: | ---: | ---: | --- |
| skip_BUY | **REJECT_FREQUENCY_STALL** | +0.25 | 49% | 62% | prior **DISARM** (ΔE_N −0.18) |
| skip_BUY_if_Thu | ARM_SOFT | +0.02 | 82% | 56% | Nested in Thu — no separate arm |
| **skip_BUY_if_near_atr** | **ARM_SOFT** | **+0.08** | 82% | 67% | 0 Wed · 0 SELL FP |
| skip_BUY_if_H08 | ARM_SOFT | +0.19 | 78% | 82% | 1 Wed FP → **HOLD** |

**Armed additive:** `L2det_uk_v1_BUY_near_atr`.  
**Preferred stack with Thu:** `L2det_uk_v1b_stack` = Thu OR (BUY∧near_atr) → tip kept E_N **+0.364R** · ΔE_N **+0.261R** · ret 64.7% · prec 72% · **0 Wed/SELL FP**.

---

## 4. P2-T04 — stress cells

| Policy | Verdict | ΔE_N | Ret. | Prec. | Note |
| --- | --- | ---: | ---: | ---: | --- |
| **skip_Jul** | **ARM_SOFT** | +0.07 | 86% | 71% | Calendar seed; 1 Wed + 2 SELL FP |
| skip_near_atr_cap (all sides) | **DISARM** | −0.01 | 65% | 50% | Use BUY∧near_atr instead |
| skip_Thu_PLUS_Jul | ARM_SOFT | +0.19 | 65% | 67% | Optional; more SELL FP than v1b |
| Feb (prior only) | ARM_SOFT on prior | +0.11 | 69% | 65% | Diagnostic — not tip arm |

**Armed:** `L2det_uk_v1_Jul` for **tip shadow** only. Replace with non-calendar features when hist grows (do not hardcode Jul in multi-year live).

---

## 5. P2-T05 — size table (spec only)

Wire after L4. Skip outranks size.

| State | f_mult |
| --- | ---: |
| Expanding / Stable | 1.0 |
| Compressing | 0.5 |
| Near frontier | 0.25 |
| Below frontier | 0.0 |
| L2det WOULD_SKIP | 0.0 |

Full table: `P2_REMAINING_CF.json` → `P2_T05_size_table`.

---

## 6. P2-T06 — `L2skip_uk` (DISARM)

| Item | Value |
| --- | --- |
| Train | prior n=75 · LogisticRegression balanced C=0.5 |
| Tip OOS AUC | **≈0.39** (worse than chance) |
| Best thr on tip | 0.80 → 1 skip · prec 0 · ΔE_N **−0.023** → **DISARM** |
| Artifact | `infra/artefacts/models/L2skip_uk/LATEST/` · **SHADOW_ONLY · not armed** |
| MQH export | **Not generated** |

**Read:** Prior→tip transfer fails for UK100 at this n/feature set. Keep det maps; revisit AI after hist tape + measured Leak + more features (session_age, structure).

---

## 7. P2-T07 — stack scorecard (tip)

| Stack | Kept E_N | ΔE_N | Ret. | Verdict |
| --- | ---: | ---: | ---: | --- |
| P0 engine | +0.103R | — | 100% | BASELINE |
| **L2det_Thu** | **+0.243R** | +0.141 | 74.5% | **ARM_SOFT** |
| L2AI only | +0.080R | −0.023 | 98% | **DISARM** |
| L2det OR L2AI | +0.216R | +0.113 | 72.5% | ARM_SOFT (worse than Thu alone) |
| L2det AND L2AI | +0.103R | 0 | 100% | DISARM (no overlap) |
| **Thu OR BUY∧near_atr (v1b)** | **+0.364R** | **+0.261** | 64.7% | **ARM_SOFT** (best det stack) |

---

## 8. MQL wire (EA ≥ 1.23)

| Item | Value |
| --- | --- |
| Header | `Include/AOS_L2det_uk.mqh` · semver `L2det_uk_v1b_20261012` |
| Route | UK100 never uses INF/AUD L2 AI coeffs |
| Inputs | `InpAOS_UK_L2detEnable` · SkipThu · SkipBuyNearAtr · SkipJul (off) · AtrCap 1470 · NearFrac 0.9 |
| Tester preset | `Profiles/Tester/BMRG/BMRG-M15-UK100-6M-P4_research_OS_W50.set` · `InpAiOsMode=LIVE_WITHHOLD` |
| L2 AI | still **DISARM** |

Offline shadow CF remains in `blotter/archive/UK100-AOS-P2-*` / P4 ledgers.

---

## 9. Scorecard stamp

```text
aos_task: UK100-AOS-P2-T07
aos_overlay: L2det_shadow
policy_primary: L2det_uk_v1_Thu
policy_stack: L2det_uk_v1b_stack
policy_jul: L2det_uk_v1_Jul
l2ai: DISARM
verdict: P2_COMPLETE_SHADOW
canvas: display_only
```
