# L2-SHADOW-VS-WITHHOLD-CF — offline replay, AI skip withhold vs shadow

**task_id:** L2-SHADOW-VS-WITHHOLD-CF · **generated:** 2026-10-29  
**script:** `_replay.py` (pinned `model.joblib` + EA threshold `thr + 0.03`) · outputs `SCORECARD.json`, `MONTHLY.csv`  
**tapes (unfiltered engine, RR 1, BWR 50%):** EURUSD 8210204 n=530 (2025-01 → 2026-09) · AUDUSD 8230921 n=126 (2026-01 → 2026-10)  
**verdict:** **SHADOW ≥ WITHHOLD on EURUSD (except W250 floor) · AUDUSD withhold destroys edge OOS → shadow recommended for both**

Two views: **IS** = pinned model on its own training tape (optimistic for withhold); **OOS** = walk-forward ledger decisions (honest), compared on the same rows.

## EURUSD (INF `L2skip_inf_p92`)

| Metric | SHADOW (all) | WITHHOLD IS | SHADOW on OOS rows | WITHHOLD OOS |
| --- | ---: | ---: | ---: | ---: |
| n | 530 | 518 | 380 | 341 |
| skip rate | — | 2.3% | — | 10.3% |
| WR | 54.5% | 54.4% | 52.9% | 53.7% |
| ΣR | **+48** | +46 | +22 | **+25** |
| E_N | 0.091 | 0.089 | 0.058 | 0.073 |
| maxDD R | −21 | −20 | −21 | **−16** |
| month hit | **57%** | 52% | 47% | 47% |
| W50 EF min / % bars ≤ 0 | −12 / 37% | −12 / 39% | −12 / 46% | −12 / 41% |
| W250 EF min / % bars ≤ 0 | −2.8 / 39% | −2.4 / 45% | −0.4 / 15% | **+0.8 / 0%** |

- In-sample the pinned model skipped trades that **won 58%** → withhold −2R.
- OOS withhold +3R and −5R shallower DD, but gains came from the early folds only (per-fold +2, +4, −3, 0, 0).
- **Q4 2025 (n=59):** shadow −1R vs withhold −3R; withhold month-hit 0/3. Q4 tape skip 17% vs **41–67%** modelled live now (live spread 6–7 vs tape spread mix 1–12 → `spread_hi` almost always on live).
- Watch: on OOS rows shadow's W250 EF dips to −0.4 (15% of bars) — W250 L3 BELOW could trip briefly where withhold would not.

## AUDUSD (`L2skip_aud_p90`, OOS AUC 0.464)

| Metric | SHADOW (all) | WITHHOLD IS | SHADOW on OOS rows | WITHHOLD OOS |
| --- | ---: | ---: | ---: | ---: |
| n | 126 | 116 | 76 | 56 |
| skip rate | — | 7.9% | — | **26.3%** |
| WR | 51.6% | 52.6% | **56.6%** | 53.6% |
| ΣR | +4 | +6 | **+10** | +4 |
| E_N | 0.032 | 0.052 | **0.132** | 0.071 |
| maxDD R | −14 | −12 | −7 | −7 |
| month hit | 50% | 50% | **57%** | 43% |
| W50 EF min / % ≤ 0 | −14 / 56% | −10 / 36% | +8 / 0% | +6 / 0% |

- In-sample (fit on these 126 trades) withhold looks +2R; out-of-sample it **removes 26% of fires and costs −6R** (E_N halves).
- Q4: only 2 tape trades — no evidence either way; same calendar-numeric features as EUR (month, week-of-month, spread_hi).

## AUDUSD status

Not previously reviewed: still LIVE_WITHHOLD on VPS (magic 8230931 @ 3%, model `L2skip_aud_p90_20261008_122523`). Same treatment as EUR recommended: `InpAiOsMode=1` + `InpLogGateBlocks=true`.
