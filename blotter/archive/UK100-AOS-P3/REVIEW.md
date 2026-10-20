# UK100-AOS-P3 — L3 / L4 offline sign-off

**Date:** 2026-10-12  
**Artifacts:** `P3_L3L4.json` · `run_p3_l3l4.py` · `health_path_*.csv`  
**Policy:** `doc/assets/UK100/aos_l3l4_policy.md`

## Headline

| Path | MaxDD | L3 trips | Max loss streak |
| --- | ---: | ---: | ---: |
| P0 tip | 3.5% | 1× BELOW frontier | 6 |
| **v1b kept** | **1.4%** | **0** | **3** |
| v1b+Jul | 1.4% | 0 | 3 |

v1b L2det removes the tip below-frontier halt. DD never near 25% at research size.

## Tasks

| Task | Verdict |
| --- | --- |
| P3-T01 | **SIGNED** — DD25 / derisk20 / BELOW→halt · recommend W50 when wiring |
| P3-T02 | **SIGNED** — stall warn · streak watch · no cost drift on tip |
| P3-T03 | **SIGNED** — W15/W20 paths archived |
| P3-T04 | **SIGNED** — bus table in policy |

## Next

P4 ledger + Tester shadow stack, or research `.set` with L3/L4 ON · L2 AI OFF · W50.
