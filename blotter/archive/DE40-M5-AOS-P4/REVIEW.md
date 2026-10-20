# DE40-M5-AOS-P4 — REVIEW

**Task:** DE40-M5-AOS-P4 (T01–T04)  
**Scored:** 2026-10-20  
**Verdict:** **ACCEPT** — ledger + det stack signed · research `.set` ready · L2AI DISARM · next **P5**  

---

## Stack (tip · offline · Leak prior 7.0 pp)

| Stack | n_fire | E_N | EF_prior | L3 halt | Notes |
| --- | ---: | ---: | ---: | ---: | --- |
| **det_v1b** | **104** | **+0.298R** | **+6.25 pp** | **6** | Preferred · unlatch ON |
| v1b+Oct all | 102 | +0.302R | +6.40 pp | 6 | HOLD (SELL FP) |
| v1b+AI shadow | 104 | +0.298R | +6.25 pp | 6 | 27 AI shadow · DISARM |
| forever latch | 36 | +0.06R | −4.2 pp | 85 | **REJECT** for OS compare |

L8: **14/14** advises on losers (0 winners) — advise-only.  
ΔE_N vs tip baseline: **+0.091R**.

---

## Wire

| Item | Value |
| --- | --- |
| Include | `AOS_L2det_de_m5.mqh` |
| Route | DE40 ∧ `PERIOD_M5` → M5 map; M15 `AOS_L2det_de` gated off |
| Preset | `BMRG-M5-DE40-6M-P4_research_OS_W50.set` |
| Magic | **26151904** |
| Mode | LIVE_WITHHOLD L2det · L3/L4/ledger ON · L2AI OFF · W250=50 |

---

## Next

Compile → optional Tester tip with P4 `.set` · then **P5** retrain/rollback.
