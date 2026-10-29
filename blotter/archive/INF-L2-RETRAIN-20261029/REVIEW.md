# INF-L2-RETRAIN-20261029 — EURUSD L2 INF retrain attempt

**task_id:** INF-L2-RETRAIN-20261029  
**model under review:** `L2skip_inf_p92_20260927_223519` (LIVE_WITHHOLD on EURUSD 8210204)  
**trigger:** LIVE-20261029 — late-Oct withhold of all in-session EUR signals (calendar features)  
**verdict:** **NO_SHIP — no candidate shows out-of-sample skill; recommend SHADOW, not a new pin**

## Data

`infra/artefacts/tape/LATEST_REGIME_TAPE.parquet` · EURUSD n=531 · 2025-01-02 → 2026-09-23 · lose rate 0.45.  
Thin late-year coverage: Oct 27 · Nov 13 · Dec 19 trades (2025 only). No newer unbiased tape: Oct 2026 Tester/live EUR trades were generated with this withhold active (skipped trades missing).

## Walk-forward (same expanding folds as INF-P4-T02 · min_train 150 · test 80 · p92 skip · ±0.03 band)

| Variant | OOS AUC | Skip % | ΔR vs no filter | Per-fold ΔR |
| --- | ---: | ---: | ---: | --- |
| Baseline (live model recipe) | 0.508 | 10.3 | +3 | +2, +4, −3, 0, 0 |
| Drop month + week_of_month | 0.442 | 6.8 | **−8** | — |
| Drop calendar + spread | 0.454 | 1.1 | 0 | — |
| Drop month/wom + spread_hi | 0.445 | 1.8 | −1 | — |
| Month categorical | 0.476 | 10.8 | −1 | +6, 0, −5, −2, 0 |
| Late-month flag (wom ≥ 4) | 0.445 | 10.8 | −1 | +6, +3, −10, 0, 0 |
| Session/side/dow only | 0.452 | 0.0 | 0 | — |
| Baseline, stronger reg C=0.05 | 0.510 | 6.8 | +8 | +5, +3, 0, 0, 0 |

OOS n = 380. Every variant AUC 0.44–0.51 (coin flip). Any ΔR gain comes only from the earliest small-train folds; the three most recent folds give 0 or negative. The live model's only "signal" is the linear month / week-of-month trend, which extrapolates into Oct–Dec (skip 41% → 67% of session).

## Decision

- Do **not** pin a retrained model: a calendar-free model is worse than no filter (−8R), and calendar variants are not stable across folds.
- Recommended: EURUSD `InpAiOsMode=1` (SHADOW) — engine fires, model still logs WOULD_SKIP to the AOS ledger → builds an unbiased tape for a future retrain.
- `InpLogGateBlocks=true` on EUR/AUD presets.
- Retrain again once ≥ ~150 new shadow-logged EUR outcomes exist (incl. a Q4 with no withhold).

No model artefacts written; `LATEST_LIVE` pin and `Include/AOS_L2skip_inf.mqh` unchanged.

## Operator decision (2026-10-29)

EURUSD → **SHADOW**: new preset `INF-SHADOW_Harvest_long_ddl30.set` (= live ddl30 preset with `InpAiOsMode=1`, `InpLogGateBlocks=true`; magic 8210204, risk 0.5%, Harvest geometry unchanged). Copies: `doc/presets/`, `Presets/`, `Profiles/Tester/BMRG/`. Requires load on EURUSD chart + VPS migrate.
