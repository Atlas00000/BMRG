# AOS-P6 Full Stack Presets (offline)

**Phase:** AOS-P6  
**Engine:** Harvest 8210204 · baseline EF **1.77** (labeled path EF **2.33**)  
**Live AI pin:** `L2skip_v0_engine` · shadow `L2skip_v1`  
**Live EA hooks:** still deferred

Stack order: L1 perceive → L2 permit → **L3 veto** → L4 observe → L5 versions → L6 ledger → L7–L9 advise.

---

## T01 — Deterministic stack `L1+L2det+L3+L4+L6`

| Layer | Role in stack |
| --- | --- |
| L1 | Feature schema / tape contract (offline labels) |
| L2det | HARD `DOW_TUE` only (already 0 on champ tape) |
| L3 | Halt new entries when lifecycle **Below frontier** / HALT_* |
| L4 | Lifecycle + f_rec advisory (halt path uses Below) |
| L6 | Full decision ledger |

| Path | n | WR | EF | Zone |
| --- | ---: | ---: | ---: | --- |
| Baseline (engine fires) | 530 | 54.53 | **2.33** | Fragile |
| Det after L3 halts | **355** | 55.21 | **3.01** | Fragile |

Skipped: **175** all via L3 halt (Tue already absent). Fires kept **67%**. Loose bar **PASS**.

**Verdict:** **ACCEPT** · `archive/AOS-P6-T01/`

Preset: `AOS-P6-T01_stack_L1L2detL3L4L6_Harvest_long.set`

---

## T02 — + L2 AI skip (shadow)

| Mode | n | EF | Notes |
| --- | ---: | ---: | --- |
| Live path (AI OFF) | 355 | **3.01** | = T01 det |
| CF if AI armed on det fires | 317 | **4.90** | +38 shadow skips |

Ledger includes `L2ai_shadow` + dual model versions. Loose bar on CF **PASS**. Live AI **OFF**.

**Verdict:** **ACCEPT** shadow stack · live AI **DEFERRED** · `archive/AOS-P6-T02/`

Preset: `AOS-P6-T02_stack_L2ai_Harvest_long.set`

---

## T03 — L7 sleeve throttle (Harvest primary)

| Sleeve | Weight | Status |
| --- | ---: | --- |
| Harvest | 1.00 | **PRIMARY** |
| Growth | 0.25 | OPTIONAL_THROTTLED |
| Survival | 0.00 | BLOCKED (costs_fragile) |
| Mid | 0.00 | **BLOCKED** |

Dry-run: Mid fires **0** · Survival **0** · Harvest allowed.

**Verdict:** **ACCEPT** · `archive/AOS-P6-T03/l7_sleeve_throttle.json`

---

## T04 — L8 MAE early-abort advisor

No MAE path on current tape. Offline proxy census: SL with hold ≤ 2h → **78** events (32% of SL, 15% of all).

| Mode | Status |
| --- | --- |
| Shadow advisor | **ACCEPT** (spec + census) |
| Live abort rule | **DEFERRED** |
| Rewrites entries? | **No** |

---

## T05 — L9 multi-horizon soft veto

Spec only until H1/H4 tape exists.

```text
If H1/H4 regime vote conflicts with M5 fade side
  → soft veto into L2 (raise skip thresh)
  → never bypass L3
```

Armed: **false** (noop offline).

**Verdict:** **ACCEPT** spec · live **DEFERRED**

---

## Stack readiness summary

| Stack | Live? | Offline |
| --- | --- | --- |
| Det L1–L4+L6 | Spec ready; EA hook deferred | **ACCEPT** |
| + L2 AI | Shadow only | **ACCEPT** shadow |
| + L7 throttle | Policy ready | **ACCEPT** |
| + L8 MAE | Shadow census | Spec **ACCEPT** |
| + L9 multi-TF | Unarmed | Spec **ACCEPT** |

**Next:** AOS-P7 promotion gates (only phase that requires full G0–G5) — still paper until live hooks + L10.

---

## Task verdicts

| Task | Verdict |
| --- | --- |
| P6-T01 | **ACCEPT** |
| P6-T02 | **ACCEPT** shadow / live AI deferred |
| P6-T03 | **ACCEPT** |
| P6-T04 | **ACCEPT** shadow spec / live deferred |
| P6-T05 | **ACCEPT** spec / live deferred |
