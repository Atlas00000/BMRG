# AUDUSD M15 — L2 policy pack (P2 complete)

**Version:** 1.0.0  
**Tasks:** AUDUSD-AOS-P2-T01 … T07  
**Date:** 2026-10-19  
**Compare window:** tip May→Aug 2026 (n=41) · long Jan→Aug diagnostic  
**Evidence:** `blotter/archive/AUDUSD-AOS-P2/P2_CF.json`  
**Costs:** `Leak_source=journal_2x_entry_spread_median` (5.0 pp proxy)  
**Mode:** L2det **v1 SHADOW ARM_SOFT** · L2 AI **SHADOW_ONLY** (chrono HOLD) · no geometry change · no foreign / live-M5 L2 pin  
**Sign-off:** live Track B remains [`AIOS_SIGNOFF.md`](./AIOS_SIGNOFF.md) (**8230931**) — untouched  

---

## 0. Armed map summary

| ID | Rule | Status |
| --- | --- | --- |
| `L2det_aud_m15_v1_BUY_May` | Skip if BUY ∧ month=May | **ARM_SOFT** (**preferred** primary atom) |
| `L2det_aud_m15_v1_BUY_Thu` | Skip if BUY ∧ DOW=Thu | **ARM_SOFT** (alt atom · same ΔE_N, more Jun/Aug FP) |
| Blanket `skip_Thu` / `skip_May` | All sides | **HOLD_SOFT** (SELL / WedFri collateral) |
| Permanent skip BUY | — | **HOLD** / reject path (ret 56%) |
| `BUY∧near_atr` | — | **DISARM** (ΔE_N −0.005) |
| `fast_lose` / `band_ride` labels | Post-outcome structure | **SHADOW_LABEL_ONLY** — never arm |
| Feb / Mar (long) | YTD diagnostic | **HOLD_SOFT** — not tip arm |
| `L2skip_aud_m15` AI | pre-tip LR thr 0.575 | Tip **ARM_SOFT** · chrono **HOLD_SOFT** → **SHADOW_ONLY** |

---

## 1. P2-T01 — parity

Mon fires = **0** · Tue fires = **0** · outside session = **0** → **PASS**.  
Do **not** re-gate Mon/Tue/session in L2det — engine already filters.

---

## 2. P2-T02 — Thu / May DOW-month

| Policy | Verdict | ΔE_N | Ret. | Prec. | Collateral |
| --- | --- | ---: | ---: | ---: | --- |
| skip_Thu | HOLD_SOFT | +0.151 | 75.6% | 60% | 2 SELL · 4 JunAug FP |
| skip_May | HOLD_SOFT | +0.107 | 78.0% | 56% | 4 SELL · 4 WedFri FP |
| skip_Thu∨May | HOLD_SOFT | +0.116 | 63.4% | 47% | heavy collateral |
| skip_Thu∨May ¬WedFri | HOLD_SOFT | +0.151 | 75.6% | 60% | collapses to Thu |

**Read:** Tip lift from blanket Thu/May is real but **SELL / WedFri / Jun–Aug** false-skips block arm. Prefer **side-conditioned** atoms (T03).

---

## 3. P2-T03 — buy-caution (preferred)

| Policy | Verdict | ΔE_N | Ret. | Prec. | Collateral |
| --- | --- | ---: | ---: | ---: | --- |
| skip_BUY | HOLD_SOFT | +0.036 | 56.1% | 39% | 9 WedFri · 11 JunAug FP |
| **skip_BUY_if_Thu** | **ARM_SOFT** | **+0.065** | 87.8% | 60% | 0 SELL · 0 WedFri · 2 JunAug |
| **skip_BUY_if_May** | **ARM_SOFT** | **+0.065** | **95.1%** | **100%** | **0 / 0 / 0** |
| skip_BUY_if_near_atr | **DISARM** | −0.005 | 92.7% | 33% | WedFri FP |

**Preferred primary atom:** `L2det_aud_m15_v1_BUY_May`  
- kept E_N **+0.333R** · ΔE_N **+0.065R** · ΔEF_proxy **+3.25 pp** · ret **95.1%** · skips **n=2** (thin — confirm on P4 ledger)  
**Alt atom:** `BUY∧Thu` (same ΔE_N, more core-month FP).

---

## 4. P2-T04 — structure / long stress

| Policy | Verdict | Note |
| --- | --- | --- |
| skip_fast_lose / skip_band_ride | SHADOW_LABEL_ONLY | Outcome-leaked labels — CF looks perfect by construction |
| skip_near_atr_high (all) | HOLD_SOFT | Collateral on SELL/WedFri |
| May∨fast_lose / Thu∨fast_lose stacks | HOLD_SOFT | Retention ≤63% + label leak |
| Feb / Mar / Feb∨Mar (long) | HOLD_SOFT | Diagnostic for L3/L5 — not tip arm |

Do **not** arm structure labels until pre-trade proxies exist (L1 path features → L2 AI).

---

## 5. P2-T05 — size table (spec only)

Wire after L4. Skip outranks size. See [`aos_l2_size_table.md`](./aos_l2_size_table.md).

---

## 6. P2-T06 — `L2skip_aud_m15` (SHADOW_ONLY)

| Item | Value |
| --- | --- |
| Train | pre-tip long rows · LogisticRegression balanced C=0.5 |
| Tip OOS AUC | **≈0.597** |
| Best thr on tip | 0.575 → ARM_SOFT (ΔE_N +0.100 · prec 100% · ret 92.7% · 0 SELL/WedFri FP) |
| Chrono holdout (last ~40% tip) | **HOLD_SOFT** (ΔE_N +0.055 · prec 50% · 1 JunAug FP) |
| Artifact | `infra/artefacts/models/L2skip_aud_m15/LATEST/` · semver `L2skip_aud_m15_p_pretip_20261019_143100` |
| MQH export | **Not generated** |

**Read:** Tip thr optimistic vs chrono. Keep det map as research primary; AI stays shadow until holdout prec clears + measured Leak.

---

## 7. P2-T07 — stack scorecard (tip)

| Stack | Kept E_N | ΔE_N | Ret. | Verdict |
| --- | ---: | ---: | ---: | --- |
| P0 engine | +0.268R | — | 100% | BASELINE |
| **L2det v1** (BUY∧May) | **+0.333R** | **+0.065** | 95.1% | **ARM_SOFT** (preferred) |
| L2AI only (thr 0.575) | +0.368R | +0.100 | 92.7% | tip ARM / chrono **HOLD** |
| L2det OR L2AI | +0.444R | +0.176 | 87.8% | tip ARM_SOFT · defer (AI holdout) |
| L2det AND L2AI | +0.268R | 0 | 100% | DISARM (no overlap) |

**Research shadow arm:** L2det **v1** (`BUY∧May`) only.  
Do not LIVE_WITHHOLD L2AI. Do not OR-stack until chrono + measured Leak clear.  
Do not touch live M5 pin `L2skip_aud_*` / magic **8230931**.

---

## 8. Explicit non-actions

- Do not permanently disable BUY or blanket Thu/May.  
- Do not arm `fast_lose` / `band_ride` outcome labels.  
- Do not pin EUR / UK100 / DE40 / live M5 L2 models onto M15 OS.  
- Do not change SL/TP/BB/CD/session as “OS”.  
- Do not promote on Leak prior; journal proxy OK for shadow CF only.
