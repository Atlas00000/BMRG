# UK100-M5-AOS-P4 — REVIEW

**Task:** UK100-M5-AOS-P4 (T01–T04)  
**Scored:** 2026-10-20  
**Verdict:** **ACCEPT** — ledger + det stack signed · EA wire v1.24 · Tester research `.set` ready · L2AI DISARM  

---

## Stack (tip · offline)

| Stack | n_fire | E_N | EF_proxy | L3 halt | Notes |
| --- | ---: | ---: | ---: | ---: | --- |
| **det_v1b** | **83** | **+0.383R** | **+11.08 pp** | **0** | Preferred |
| v1b+Aug | 54 | +0.500R | +16.3 pp | 0 | Aug HOLD calendar |
| v1b+AI shadow | 83 | +0.383R | +11.08 pp | 0 | 2 AI shadow · DISARM |

L8: **23/23** advises on losers (0 winners) — advise-only.

---

## Wire

| Item | Value |
| --- | --- |
| Include | `AOS_L2det_uk_m5.mqh` |
| Route | UK100 ∧ `PERIOD_M5` → M5 map; else M15 `AOS_L2det_uk` |
| EA | BMRG **v1.24** |
| Preset | `BMRG-M5-UK100-6M-P4_research_OS_W50.set` |
| Magic | **26121904** |
| Mode | LIVE_WITHHOLD L2det · L3/L4/ledger ON · L2AI OFF |

---

## Next

Compile → Tester tip May→Aug with P4 `.set` (optional validation) · then **P5** retrain/rollback.
