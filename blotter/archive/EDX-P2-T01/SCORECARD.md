# EDX-P2-T01 — Tighter SL (200) keep TP 450

**Scored:** 2026-09-25 11:34  
**Preset:** `EDX-P2-T01_SL200_TP450_champFilters_G0_long.set`  
**Magic:** 8210201 · currency · champion filters (12–20, skip Tue)  
**Geometry:** SL=200, TP=450 → designed **RR=2.25**

## vs champion (P4-T01)

| Metric | Champion | T01 | Δ |
| --- | ---: | ---: | ---: |
| n | 420 | 509 | +89 |
| WR | 47.38% | **34.18%** | **−13.2 pp** |
| R / RR | 1.50 | 2.25 | +0.75 |
| BWR | 40% | 30.77% | −9.2 |
| BM | +7.38 | +3.42 | −3.96 |
| Leak (L1) | 2.21 | 2.54 | +0.33 |
| EF | **5.18** | **0.87** | **−4.31** |
| E_N | **0.185R** | **0.111R** | **−0.074R** |
| M | ±4.78 | ±4.12 | — |
| Zone | Robust | **Fragile** | — |
| Final | $620.63 | **$513.97** | −$106.66 |
| Freq | 100% | 121% of champ opens | OK (≥50%) |

## Verdict

**POOL_KEEP (Survival)** · **DOMINATED** vs Balanced ref on E_N/EF.

Admission clear: WR 34.2% > BWR 30.8%, E_N 0.111 > 0, EF 0.87 > 0 (Fragile vs M). Lower BWR = sleeve that can stay alive when hit rate compresses. Not a growth champion — keep in `doc/candidate_pool.md` for regime blend / retune.

**Next:** EDX-P2-T02 (SL200/TP300 hold RR=1.5).
