# EURUSD-AOS-P2 — L2 policy

**task_id:** EURUSD-AOS-P2  
**archived_at:** 2026-10-18T16:00:00+01:00  
**engine:** P2 light · magic **26101817** · AOS OFF (det shadow only)  
**verdict:** P2 COMPLETE — L2det **v1b ARM_SOFT** (Thu∨BUY∧near_atr) · L2AI **DISARM** (holdout)  

## Deliverables

| Task | Result |
| --- | --- |
| P2-T01 | Parity PASS (Tue=0 · ATR>74=0) |
| P2-T02 | Thu ARM_SOFT · H19 thin ARM · H13 HOLD |
| P2-T03 | BUY blanket REJECT · BUY∧near_atr / BUY∧H13 ARM_SOFT |
| P2-T04 | near_atr blanket DISARM · Aug HOLD · Feb YTD diagnostic |
| P2-T05 | Size table SPEC (`aos_l2_size_table.md`) |
| P2-T06 | `L2skip_eur_m15` SHADOW_ONLY · tip AUC 0.58 · chrono holdout DISARM |
| P2-T07 | Preferred stack = **v1b** kept E_N **+0.234R** (Δ+0.184) |

## Preferred map

```text
L2det_eur_m15_v1b = Thu OR (BUY AND near_atr_cap)
```

| Metric | Baseline | After v1b |
| --- | ---: | ---: |
| n | 45 | 31 (ret 68.9%) |
| E_N | +0.050R | **+0.234R** |
| Prec losers | — | 71% |
| SELL FP / MonFri FP | — | 1 / 0 |

## Evidence

- `P2_CF.json` · `tip_l2ai_scored.csv` · `run_p2_cf.py`  
- Policy: `doc/assets/EURUSD/aos_l2_policy.md`  
- Model: `infra/artefacts/models/L2skip_eur_m15/LATEST/` (SHADOW_ONLY)

## Next

P3 — L3 halt + L4 W15/W20 health bus. Do not LIVE_WITHHOLD L2AI. Do not change geometry.
