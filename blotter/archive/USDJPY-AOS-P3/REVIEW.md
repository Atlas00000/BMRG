# USDJPY-AOS-P3 — L3 / L4

**task_id:** USDJPY-AOS-P3  
**archived_at:** 2026-10-19T16:25:00+01:00  
**engine:** Balanced P0 · magic **26101828** · AOS OFF (L3/L4 shadow only)  
**verdict:** P3 SIGNED (shadow) — **v1c tip+YTD trip-free** · P0 BELOW latch works · near_atr alone insufficient  

**Policy:** [`doc/assets/USDJPY/aos_l3l4_policy.md`](../../../doc/assets/USDJPY/aos_l3l4_policy.md)  
**Evidence:** `P3_L3L4.json` · `health_path_*.csv` · `run_p3_l3l4.py`

## Deliverables

| Task | Result |
| --- | --- |
| P3-T01 | L3 halt/derisk **SIGNED** · DD 25 / derisk 20 / BELOW latch |
| P3-T02 | Cost-drift · FREQUENCY_STALL · streak monitors **SIGNED** |
| P3-T03 | W15/W20 health paths archived · W50 optional |
| P3-T04 | Recommend bus BELOW→HALT · COMPRESSING→INVESTIGATE **SIGNED** |

## Tip summary

| Path | n | MaxDD | Trips | last EN20 |
| --- | ---: | ---: | ---: | ---: |
| P0 | 46 | 4.9% | **1** BELOW | −0.23 |
| near_atr | 39 | 3.2% | **1** BELOW | −0.01 |
| **v1c** | **37** | **2.2%** | **0** | **+0.21** |
| Jul HOLD | 32 | 1.4% | 0 | +0.43 |

## YTD

| Path | n | MaxDD | Trips |
| --- | ---: | ---: | ---: |
| P0 / near_atr | 54 / 44 | ~4.9% / 3.1% | **1** BELOW each |
| **v1c** | **41** | **2.2%** | **0** |

## Next

P4 ledger + det stack shadow (L1+L2det v1c+L3+L4+L6). Do not LIVE_WITHHOLD L2AI. Do not change geometry.
