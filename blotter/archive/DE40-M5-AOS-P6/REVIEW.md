# DE40-M5-AOS-P6 — REVIEW

**Task:** DE40-M5-AOS-P6 (T01–T03)  
**Scored:** 2026-10-20  
**Verdict:** **ACCEPT / P6_COMPLETE** — L9 no LIVE · v1b keep · ATR 2380 G3 PASS  

---

## Results

| Task | Verdict | Note |
| --- | --- | --- |
| **P6-T01** L9 | **PASS** | Frankfurt/H08 DISARM · H13/spread HOLD_SHADOW · no LIVE wire |
| **P6-T02** ±10% L2 | **PASS_WITH_NOTES** | Keep v1b; Sep widen note-only; nearATR REJECT confirmed |
| **P6-T03** ATR G3 | **PASS** | `InpATRMaxPoints=2380` on P0 + P4 |

Tip v1b kept: **E_N +0.289R** · ret **89.4%** · SELL FP **0**.

---

## Artifacts

- `P6_HARDEN.json` · `P6_SUMMARY.json` · `run_p6_harden.py`
- Policy: `doc/assets/DE40/aos_p6_harden_M5.md`

---

## Next

`DE40-M5-AOS-P7` — promotion packet · HITL · target magic **26151907** / `DE40M5stack`.
