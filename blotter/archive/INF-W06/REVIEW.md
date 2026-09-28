# INF-W06 — Counterfactual prove (INF-P4b) REVIEW

**Week:** INF-W06  
**Completed:** 2026-09-27  
**Verdict:** ACCEPT  

| Task | Artefact | Prove | Verdict |
| --- | --- | --- | --- |
| INF-P4-T04 | `reports/LATEST_EVAL.json` · `cf_eval.py` | Drop OOS WOULD_SKIP; CF EF ≥ engine−1pp; no payoff trap | ACCEPT |
| INF-P4-T05 | `l3_l4_sim.py` · `INF-P4-T05_l3l4_sim.json` | Halt → HALT_NO_ENTRY over L2 WOULD_SKIP/FIRE | ACCEPT |

## CF vs engine (identity EF)

| Metric | Engine | CF | Δ |
| --- | ---: | ---: | ---: |
| n | 530 | 491 | −39 |
| ef_pp | 2.3283 | 2.9935 | +0.6652 |
| fires_kept_pct | — | **92.64%** | — |
| maxdd_pp | — | — | −4.14 |

Protect bar: long EF hold, maxDD ok, fires ≥70%, no payoff trap — all pass. warn=[].

## L3/L4 sim

- Halt demo (Below-frontier + MaxDD): `l3_outranks_l2=true`
- Effective action under halt: `HALT_NO_ENTRY` (L2 decision not authority)

## Tests

`pytest src/eval/test_p4b_eval.py` → **3 passed**

## Next

**INF-W07** → `INF-P5-T01` (observability + Docker compose).
