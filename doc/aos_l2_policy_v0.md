# AOS L2 Policy v0 (offline)

**Phase:** AOS-P2  
**Engine:** Harvest 8210204 · `AOS_BASELINE_v1`  
**Tape:** `blotter/archive/AOS-P1-T02/` + labeled `AOS-P2-T03/harvest_long_labeled.csv`  
**Live publisher:** deferred — all gates evaluated offline

L2 only **permits / withholds / sizes**. It does not invent entries.

---

## 0. Offline score snapshot (Harvest long labeled)

| Metric | Value |
| --- | ---: |
| n closed | 530 |
| WR / BWR | 54.53% / 50% |
| BM / Leak / EF | +4.53 / 2.2 / **~2.33**\* |
| E_N | ~0.091 |
| Tue opens | **0** |
| LON_AM opens | **0** |

\*EF from closed TP/SL labeling; matrix baseline EF 1.77 used Leak on currency scorecard — treat **parity checks** as primary for P2-T01/T02; health hold vs `AOS_BASELINE` EF 1.77 for later AI gates.

---

## 1. Deterministic HARD skip map v1

| Cell | Rule at signal | Champ tape effect | Status |
| --- | --- | --- | --- |
| `DOW_TUE` | skip if Tuesday | 0 fires already | **ACTIVE** (engine parity) |
| — | other BM≤0 hour cells | none on champ 12–20 | none |

```text
HARD_SKIP(signal):
  if dow == Tue: return SKIP("DOW_TUE")
  return FIRE
```

**Ledger reason_codes:** `DOW_TUE` | `FIRE_OK`

---

## 2. Soft / advisory gates

| Gate | Rule | Harvest offline result | Policy v0 |
| --- | --- | --- | --- |
| `SOFT_LON_AM` | skip hour 08–12 | 0 opens (no-op on champ) | **ARMED** only if session window widened |
| `BUY_CAUTION` | raise skip thresh on buys | Buy EF **2.63** ≥ Sell **2.04** — opposite of Growth P25 | **DISARMED** on Harvest |
| `EXIT_INTRADAY` | BM −0.3 on same-day exits | Lookahead — cannot skip at entry | **L8 feature only** |
| `AI_v0_skip_Mon` | trial skip Monday | skip 22.8% fires; EF flat | **REJECT** as hard gate (no EF lift) |

---

## 3. Size modulator v0 (spec — needs L4 lifecycle)

| Lifecycle (from L4) | f multiplier |
| --- | ---: |
| Expanding | 1.00 |
| Stable | 0.75 |
| Compressing | 0.50 |
| Near frontier | 0.25 |
| Below frontier | **0.00** (L3 also forces 0) |

Fire count unchanged; size only. Offline: document only until L4 observer exists (AOS-P3).

---

## 4. AI skip classifier v0 → `L2skip_v1`

**Status:** Trained offline (AOS-P4). **SHADOW_ONLY** — live gate **OFF**.

| | |
| --- | --- |
| Artifact | `archive/AOS-P4-T02/L2skip_v1.joblib` |
| Doc | `doc/aos_l2skip_v1.md` |
| OOS AUC | **0.55** (weak) |
| Shadow CF | EF 2.33 → 4.91 · loose bar PASS |
| Live | **DEFERRED** (P4-T04) until stronger L1 features / P5 |

Entry features: hour, dow, session, side, spread, month, week_of_month, hour_bucket, …  
Do **not** arm live AI skip on current AUC; L3 Below-frontier halt remains the hard safety net.

---

## 5. Counterfactual summary vs leave-all-on

| Gate | skip% | fires left | ΔEF | Verdict |
| --- | ---: | ---: | ---: | --- |
| HARD_TUE | 0% | 100% | 0 | **ACCEPT** parity |
| SOFT_LON_AM | 0% | 100% | 0 | **ACCEPT** no-op on champ |
| MAP_v1 hard | 0% | 100% | 0 | **ACCEPT** |
| Skip all buys | 48.9% | 51.1% | ~0 + FREQUENCY_STALL warn | **REJECT** for Harvest |
| Skip Monday | 22.8% | 77.2% | ~0 | **REJECT** hard gate |

---

## 6. OS offline next

P2 deterministic layer **complete** for champ geometry.  
Proceed **AOS-P3** offline observer specs / **AOS-P4** train on `harvest_long_labeled.csv` — still no live tape.
