# INF-W05 — Train + shadow ledger (INF-P4a) REVIEW

**Week:** INF-W05  
**Completed:** 2026-09-27  
**Verdict:** ACCEPT  

| Task | Artefact | Prove | Verdict |
| --- | --- | --- | --- |
| INF-P4-T01 | `infra/src/train/walkforward.py` | Expanding WF; train_start=0; no fit-only-on-decay | ACCEPT |
| INF-P4-T02 | `artefacts/models/L2skip/L2skip_inf_p92_20260927_223519/` | p92 low-skip; never overwrite; versioned | ACCEPT |
| INF-P4-T03 | `shadow_ledger_oos.csv` · `reports/skip_ledger/LATEST_*` | WOULD_SKIP / FIRE / ALLOW_UNCERTAIN; shadow_fire=True | ACCEPT |

## OOS shadow metrics (p92 under-skip)

| Metric | Value |
| --- | ---: |
| n_oos | 380 |
| skip_rate | **10.3%** |
| fires_kept | **89.7%** |
| AUC | 0.508 (weak — shadow only) |
| n_remaining if skip | 341 |
| FREQUENCY_STALL | no (&gt;50%) |
| fires &lt;70% warn | no |

## Policy

- Default allow; skip only if `p_lose >= thr` (train p92)
- Near-threshold band → `ALLOW_UNCERTAIN` (still fire)
- Engine unrestricted in shadow (`shadow_fire=true` on all rows)

## Tests

`pytest src/train/test_p4a_train.py` → **2 passed**

## Next

**INF-W06** → `INF-P4-T04` (counterfactual scorecard vs baseline).
