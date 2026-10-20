# UK100-AOS-P2-T03 … T07 — remaining P2

**Date:** 2026-10-12  
**Artifacts:** `P2_REMAINING_CF.json` · `run_p2_remaining.py` · `tip_l2ai_scored.csv`  
**Policy:** `doc/assets/UK100/aos_l2_policy.md` v1.1  

## Verdicts

| Task | Verdict |
| --- | --- |
| **P2-T03** buy-caution | **ARM** `BUY∧near_atr` · DISARM blanket BUY · HOLD BUY∧H08 |
| **P2-T04** stress | **ARM** Jul (tip seed) · DISARM blanket near_atr |
| **P2-T05** size table | **SPEC_ONLY** (wire after L4) |
| **P2-T06** L2skip_uk | **DISARM** (tip AUC≈0.39) |
| **P2-T07** stacks | Best = **Thu OR BUY∧near_atr** (E_N +0.36R) · AI adds nothing |

## Best tip stack (v1b)

n 51→33 · WR↑ · E_N **+0.364R** · ΔE_N **+0.261R** · retention 64.7% · prec 72% · 0 Wed/SELL winner skips.

## P2 phase

**COMPLETE** for shadow det policy. Next phase = P3 L3/L4 (or wire shadow ledger reasons).
