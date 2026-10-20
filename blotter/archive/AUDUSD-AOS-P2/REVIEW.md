# AUDUSD-AOS-P2 — L2 policy

**task_id:** AUDUSD-AOS-P2  
**archived_at:** 2026-10-19T15:35:00+01:00  
**engine:** CHAMP Harvest · magic **8230901** · AOS OFF (det shadow only)  
**verdict:** P2 COMPLETE — L2det **v1 ARM_SOFT** (BUY∧May) · L2AI **SHADOW_ONLY** (chrono HOLD)

## Deliverables

| Task | Result |
| --- | --- |
| P2-T01 | Parity PASS (Mon=0 · Tue=0 · session=0) |
| P2-T02 | Blanket Thu/May **HOLD_SOFT** (SELL/WedFri/JunAug FP) |
| P2-T03 | **BUY∧May ARM_SOFT** preferred · BUY∧Thu alt · BUY∧near_atr DISARM |
| P2-T04 | fast_lose/band_ride **LABEL_ONLY** · Feb/Mar long HOLD diagnostic |
| P2-T05 | Size table SPEC (`aos_l2_size_table.md`) |
| P2-T06 | `L2skip_aud_m15` SHADOW_ONLY · tip AUC 0.60 · chrono HOLD_SOFT |
| P2-T07 | Preferred stack = **L2det v1** kept E_N **+0.333R** (Δ+0.065) |

## Preferred map

```text
L2det_aud_m15_v1 = BUY AND month==May
```

| Metric | Baseline | After v1 |
| --- | ---: | ---: |
| n | 41 | 39 (ret 95.1%) |
| E_N | +0.268R | **+0.333R** |
| Prec losers | — | 100% |
| SELL / WedFri / JunAug FP | — | 0 / 0 / 0 |
| skips_n | — | **2** (thin — reconfirm P4) |

## Evidence

- `P2_CF.json` · `tip_l2ai_scored.csv` · `run_p2_cf.py`  
- Policy: `doc/assets/AUDUSD/aos_l2_policy.md`  
- Model: `infra/artefacts/models/L2skip_aud_m15/LATEST/` (SHADOW_ONLY)

## Next

P3 — L3 halt + L4 W15/W20 health bus. Do not LIVE_WITHHOLD L2AI. Do not change geometry. Live **8230931** untouched.
