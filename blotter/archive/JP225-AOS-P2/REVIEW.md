# JP225-AOS-P2 — L2 policy CF

**Archived:** 2026-10-19  
**Engine:** Growth P1 · magic **26101904** · AOS OFF  
**Evidence:** `P2_CF.json` · tapes tip n=79  
**Policy:** `doc/assets/JP225/aos_l2_policy.md`

## Verdict

**P2 COMPLETE** — **ARM** `May∨Jul` (clears tip EF −1.3 → **+9.2 pp**) · HOLD Wed/H14 · **DISARM** L2AI (AUC≈0.49) · **DISARM** near_atr alone · next **P3**.

## Tasks

| Task | Status |
| --- | --- |
| P2-T01 parity Tue/ATR | **PASS** |
| P2-T02 May / Wed CF | **DONE** — ARM May · HOLD Wed |
| P2-T03 Jul / hours | **DONE** — ARM Jul · ARM May∨Jul · HOLD H14 |
| P2-T04 SELL / near_atr | **DONE** — ARM SELL∧May · DISARM near_atr / blanket SELL |
| P2-T05 size table | **SPEC** |
| P2-T06 L2AI | **DISARM** AUC 0.49 |
| P2-T07 stacks | **DONE** — primary `L2det_May_OR_Jul` |

## Primary arm (tip)

| Metric | P1 baseline | May∨Jul kept |
| --- | ---: | ---: |
| n | 79 | **43** (ret 54.4%) |
| WR | 43.0% | **53.5%** |
| E_N | +0.076R | **+0.337R** |
| EF_prior | **−1.26 pp** | **+9.19 pp** |
| tip_EF_cleared | no | **yes** |
| Jun / Aug / MATCH FP | — | **0 / 0 / 0** |
| Prec. vs losers | — | 69% |

## Explicit non-arms

- Blanket FRAGILE / May∨Jul∨Wed → FREQUENCY_STALL  
- near_atr alone · H13 · BUY-all · Jun skip · L2AI  

## Next

JP225-AOS-P3 L3/L4 · measured Leak still OPEN · no MQH / live arm.
