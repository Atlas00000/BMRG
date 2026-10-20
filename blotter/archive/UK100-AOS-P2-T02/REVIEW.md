# UK100-AOS-P2-T01 / P2-T02 — L2det shadow CF

**Date:** 2026-10-12  
**Tape:** tip n=51 · prior n=75  
**Artifacts:** `SHADOW_CF.json` · `shadow_cf_l2det.py`  
**Normative policy:** `doc/assets/UK100/aos_l2_policy.md`

## P2-T01 parity

Tue fires = 0 · ATR>1470 fires = 0 → **PASS**.

## P2-T02 tip CF (headline)

| Policy | ΔE_N | Retention | Prec. losers | Verdict |
| --- | ---: | ---: | ---: | --- |
| skip_Thu | **+0.141R** | 74.5% | 69% | **ARM_SOFT** (primary) |
| skip_H08 | +0.141R | 74.5% | 69% | ARM_SOFT (hold — Wed/SELL collateral) |
| Thu OR H08 | +0.263R | 54.9% | 65% | ARM_SOFT tip / prior-hostile |
| Thu AND H08 | +0.069R | 94.1% | 100% | ARM_SOFT (conservative alt) |

**Armed for shadow:** `L2det_uk_v1_Thu` — tip kept WR 55.3% · E_N **+0.243R** · EF_proxy **+6.55 pp**.

## Verdict

**ACCEPT** Thu SOFT map for shadow. No LIVE_WITHHOLD · no geometry change · no foreign pin.
