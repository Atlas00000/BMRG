# AUDUSD-AOS-P3 — L3 / L4

**task_id:** AUDUSD-AOS-P3  
**archived_at:** 2026-10-19T15:40:00+01:00  
**engine:** CHAMP Harvest · magic **8230901** · L2det v1 (BUY∧May) shadow  
**verdict:** P3 SIGNED for shadow — v1 tip trip-free · P0 tip had 1 BELOW latch

## Sims

| Path | n | MaxDD | Trips | last W20 E_N |
| --- | ---: | ---: | ---: | ---: |
| P0 tip | 41 | 4.4% | **1 BELOW** | +0.50 |
| **v1 BUY∧May kept** | 39 | **3.7%** | **0** | **+0.50** |
| alt BUY∧Thu | 36 | 2.9% | **0** | +0.50 |
| P0 long (diag) | 95 | 6.5% | 1 BELOW · maxL 7 | +0.50 |

## Deliverables

| Task | Status |
| --- | --- |
| P3-T01 L3 halt/derisk (overnight-aware) | **SIGNED** |
| P3-T02 monitors (cost / stall / streak) | **SIGNED** |
| P3-T03 L4 W15/W20 | **SIGNED** · `health_path_*.csv` |
| P3-T04 bus | **SIGNED** · BELOW→HALT |

## Evidence

- `P3_L3L4.json` · `run_p3_l3l4.py` · `health_path_*.csv`  
- Policy: `doc/assets/AUDUSD/aos_l3l4_policy.md`

## Next

P4 — L6 ledger + det stack shadow + L8 overnight MAE advisor. Measured+swap still OPEN. Live **8230931** untouched.
