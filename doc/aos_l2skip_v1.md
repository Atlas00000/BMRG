# AOS-P4 Avoidance Training (offline)

**Phase:** AOS-P4  
**Engine:** Harvest 8210204  
**Labels:** `archive/AOS-P2-T03/harvest_long_labeled.csv` → `archive/AOS-P4-T01/harvest_train_matrix.csv`  
**Model:** `L2skip_v1` · `archive/AOS-P4-T02/L2skip_v1.joblib`  
**Live gate:** **DEFERRED** (AOS-P4-T04) — shadow eligible but signal weak

L2skip only **withholds** engine fires. It does not invent entries. L3 still outranks.

---

## T01 — Labelled dataset

| | |
| --- | ---: |
| n | **530** (= baseline) |
| TP / SL | 289 / 241 |
| lose_rate | **45.47%** |
| Sessions | LON_NY 424 · NY 106 |
| Dow | Wed 147 · Thu 135 · Fri 127 · Mon 121 · Tue **0** |

**Entry features (no lookahead):** hour, dow, session, side, spread, month, week_of_month, hour_bucket, spread_hi, is_mon, is_fri, side_buy  

**Diagnostics only (not for skip):** hold_hours, same_day_exit  

Artifacts: `class_balance.json` · `harvest_train_matrix.csv`

---

## T02 — Walk-forward `L2skip_v1`

| Setting | Value |
| --- | --- |
| Algo | LogisticRegression `class_weight=balanced` C=0.5 + OHE |
| WF | Expanding · min_train 150 · test_block 80 → **5 folds** · n_oos **380** |
| Skip rule | Train quantile **p85** of lose-proba (target ~15%; realised OOS varies) |

### OOS aggregate

| Metric | Value | Comment |
| --- | ---: | --- |
| skip_rate | **26.6%** | above 15% target (fold variance) |
| loser_recall | **31.8%** | modest |
| loser_precision | **56.4%** | slightly above base lose-rate 45% |
| AUC | **0.548** | **weak** — barely above chance |

### Per-fold (watch fold 2)

| Fold | skip% | recall | AUC | EF all → kept |
| ---: | ---: | ---: | ---: | --- |
| 1 | 37.5 | 0.48 | 0.63 | −4.7 → **+3.8** |
| 2 | 63.8 | 0.61 | 0.47 | −9.7 → **−14.3** ⚠ hurts |
| 3 | 21.3 | 0.25 | 0.50 | +7.8 → **+9.7** |
| 4 | 0.0 | 0.00 | 0.38 | +0.3 → +0.3 |
| 5 | 5.0 | 0.05 | 0.48 | +12.8 → +12.7 |

**Accept T02?** **CONDITIONAL ACCEPT** — OOS recall useful in fold 1/3; **fails “no fit-only-on-decay” purity** on fold 2 (Below-frontier stress). Mitigant: L3 already commands f=0 when W250 E_N≤0; do not rely on L2skip alone in that regime.

---

## T03 — Shadow counterfactual

Shadow logs skips; engine still “fires” all (offline CF applies skips).

| Slice | n | WR | EF | Zone |
| --- | ---: | ---: | ---: | --- |
| Baseline all | 530 | 54.53 | **2.33** | Fragile |
| CF apply OOS skips (+ keep first 150) | 429 | 57.11 | **4.91** | Robust |
| OOS region only (fair) | 380 → 279 | 52.89 → 56.27 | **0.69 → 4.07** | Fragile→Fragile |

### Loose bar (§4)

| Check | Result |
| --- | --- |
| remaining n ≥ 100 | **PASS** (429) |
| EF ≥ baseline − 1 pp | **PASS** (4.91 ≥ 0.77) |
| fires ≥ 50% | **PASS** (80.9%) |
| AL improved | **PASS** (0.455 → 0.429) |
| payoff trap | **none** |

**Verdict T03:** **ACCEPT** shadow · `eligible_for_live_gate=true` on loose bar **with AUC caveat**.

---

## T04 — Live avoid-gate

| Status | **DEFERRED** |
| --- | --- |
| Why | Live EA hooks paused; AUC 0.55 too weak to arm hard skip; fold-2 regression |
| Unblock when | Stronger L1 features (BB/ATR/structure) on tape **or** user unpauses live **and** P5 retrain improves OOS AUC |
| Until then | Shadow artifact only; HARD skip remains `DOW_TUE` |

---

## Policy update for `aos_l2_policy_v0`

```text
AI_SKIP L2skip_v1:
  status     = SHADOW_ONLY
  live_gate  = OFF
  reason     = weak_OOS_AUC + fold2_harm
  artifacts  = AOS-P4-T02/L2skip_v1.joblib
```

---

## Task verdicts

| Task | Verdict |
| --- | --- |
| P4-T01 | **ACCEPT** |
| P4-T02 | **CONDITIONAL ACCEPT** (weak AUC; fold-2 hurt) |
| P4-T03 | **ACCEPT** shadow / loose bar |
| P4-T04 | **DEFERRED** |
