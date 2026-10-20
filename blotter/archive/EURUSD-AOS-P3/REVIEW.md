# EURUSD-AOS-P3 — L3 / L4

**task_id:** EURUSD-AOS-P3  
**archived_at:** 2026-10-18T16:05:00+01:00  
**engine:** P2 light · magic **26101817** · L2det v1b shadow  
**verdict:** P3 SIGNED for shadow — v1b trip-free · P0 tip had 1 BELOW latch  

## Sims (tip)

| Path | n | MaxDD | Trips | last W20 E_N |
| --- | ---: | ---: | ---: | ---: |
| P0 tip | 45 | 3.0% | **1 BELOW** | +0.01 |
| **v1b kept** | 31 | **1.8%** | **0** | **+0.35** |
| Thu∨BUY∧H13 | 34 | 1.7% | **0** | +0.13 |

## Deliverables

| Task | Status |
| --- | --- |
| P3-T01 L3 halt/derisk | **SIGNED** |
| P3-T02 monitors | **SIGNED** (2 freq-stall warns on v1b — expected) |
| P3-T03 L4 W15/W20 | **SIGNED** · `health_path_*.csv` |
| P3-T04 bus | **SIGNED** · BELOW→HALT |

## Evidence

- `P3_L3L4.json` · `run_p3_l3l4.py` · `health_path_*.csv`  
- Policy: `doc/assets/EURUSD/aos_l3l4_policy.md`

## Next

P4 — L6 ledger + det stack shadow + L8 overnight MAE advisor. Measured+swap still OPEN.
