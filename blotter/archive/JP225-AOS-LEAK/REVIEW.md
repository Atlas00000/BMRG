# JP225-AOS-LEAK — REVIEW

**Date:** 2026-10-19  
**Verdict:** **MEASURED CLOSED** — Leak authority = deal-fill median · tip Stage-1 **PASS** under measured · no MQH / no live arm  
**Artefacts:** `LEAK_MEASURED.json` · `tip_deal_costs.csv` · `measure_jp225_tip_leak.py`  
**Docs:** `doc/assets/JP225/aos_cost_policy.md` · `doc/assets/JP225/LEAK_MEASURED.json`

---

## Method

| Field | Value |
| --- | --- |
| Source | Tester `20261019.log` tip chunk magic **26101904** May→Aug |
| n | **79** / 79 paired (OPEN → TP/SL → exit deal) |
| cost_pts_rt | `entry_spread_pts + max(0, adverse_exit_slip_pts)` |
| commission / swap | **0** (absent in Tester journal) |
| Authority | `Leak = median(c_R) / (R+1)` · R=1.50 · SL=23260 |

---

## Result

| Metric | Prior stub | Journal 2× proxy | **Measured median** |
| --- | ---: | ---: | ---: |
| cost_pts_rt | 2500 | — | **1423** |
| c_R | 0.107 | — | **0.0612** |
| Leak_pp | 4.3 | 4.82 | **2.45** |
| Tip EF_pp | **−1.3** | −1.8 | **+0.59** |
| Tip Stage-1 | FAIL | FAIL | **PASS** |
| May∨Jul kept EF_pp | +9.2 | — | **+11.0** |

Entry spread med **1400** pts (mean 1546 · max 2300). Exit adverse slip med **15** pts (share adverse 57%).

**Zone:** `tip_stage1_pass_measured`

**Live footnote:** live snapshot ~2300 pts may exceed tester entry median — re-check before P7. Tester deal-fill is tip authority for OS CF until then.

---

## Next

**P4** ledger + det stack offline · still **no** MQH / research OS arm.
