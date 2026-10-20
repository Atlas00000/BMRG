# UK100-M5-AOS-P3 — REVIEW

**Task:** UK100-M5-AOS-P3 (T01–T04)  
**Scored:** 2026-10-20  
**Verdict:** **ACCEPT / SIGNED** — L3+L4 shadow · v1b tip **trip-free** · proceed P4  

---

## Sim scoreboard (tip · journal Leak 5.93 pp)

| Path | n | MaxDD | L3 trips | last W20 E_N | last life |
| --- | ---: | ---: | ---: | ---: | --- |
| P0 tip | 116 | 1.9% | **1 BELOW** (Aug cluster) | −0.21 | BELOW |
| **v1b kept** | 83 | 1.6% | **0** | **+0.46** | **EXPANDING** |
| H12 aggressive | 69 | 1.3% | 0 | +0.35 | EXPANDING |

v1b removes the P0 below-frontier latch. MaxDD ≪ 25%. Freq-stall warns expected under skips — do not lift ATR max.

---

## Deliverables

| Artifact | Role |
| --- | --- |
| `aos_l3l4_policy_M5.md` | Normative L3/L4 + bus |
| `P3_L3L4.json` / `P3_SUMMARY.json` | Full + compact |
| `health_path_P0_tip.csv` | P0 path |
| `health_path_v1b_kept.csv` | Preferred path |
| `health_path_H12_aggressive_kept.csv` | Diagnostic |
| `run_p3_l3l4.py` | Repro |

---

## Next

`UK100-M5-AOS-P4` — L6 ledger + det stack shadow · optional `AOS_L2det_uk_m5` wire.
