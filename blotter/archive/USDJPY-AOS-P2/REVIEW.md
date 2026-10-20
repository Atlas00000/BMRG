# USDJPY-AOS-P2 — L2 policy

**task_id:** USDJPY-AOS-P2  
**archived_at:** 2026-10-19T16:15:00+01:00  
**engine:** Balanced P0 · magic **26101828** · AOS OFF (det shadow only)  
**verdict:** P2 COMPLETE — L2det **v1c ARM_SOFT** (near_atr∨H16) · slim **near_atr ARM_SOFT** · L2AI **SHADOW_ONLY** (train overlap) · Thu **DISARM**

## Deliverables

| Task | Result |
| --- | --- |
| P2-T01 | Parity **PASS** (Tue=0 · ATR>70=0) |
| P2-T02 | Thu **DISARM** · H14 HOLD · **H16 ARM_SOFT** |
| P2-T03 | SELL blanket REJECT · **SELL∧near_atr ARM_SOFT** |
| P2-T04 | **near_atr ARM_SOFT** · Jul HOLD · **v1c ARM_SOFT** |
| P2-T05 | Size table SPEC (`aos_l2_size_table.md`) |
| P2-T06 | `L2skip_usdjpy` SHADOW_ONLY · tip AUC 0.75 (contaminated) · holdout AUC 0.55 |
| P2-T07 | Preferred stack = **v1c** kept E_N **+0.368R** (Δ+0.268) · ret 80.4% · protect FP 0 |

## Preferred map

```text
L2det_usdjpy_v1c = near_atr_cap OR hour==16
# slim fallback:
L2det_usdjpy_v1_near_atr = near_atr_cap
# sell-caution nested:
L2det_usdjpy_v1_SELL_near_atr = SELL AND near_atr_cap
```

| Metric | Baseline | After v1c |
| --- | ---: | ---: |
| n | 46 | 37 (ret 80.4%) |
| E_N | +0.100R | **+0.368R** |
| EF_prior | −6.9 pp | **+5.3 pp** |
| Prec losers | — | 100% |
| Protect FP | — | **0** |

## Evidence

- `P2_CF.json` · `tip_l2ai_scored.csv` · `run_p2_cf.py`  
- Policy: `doc/assets/USDJPY/aos_l2_policy.md`  
- Size: `doc/assets/USDJPY/aos_l2_size_table.md`  
- Model: `infra/artefacts/models/L2skip_usdjpy/LATEST/` (SHADOW_ONLY)

## Next

P3 — L3 halt + L4 W15/W20 health bus with **v1c** shadow overlay.  
Do not LIVE_WITHHOLD L2AI. Do not hard-arm Jul/Thu. Do not change geometry.
