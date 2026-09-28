# EDX-P2-T03..T05 — 3M Jul–Sep 2026 batch

**Scored:** 2026-09-25 12:05–12:06  
**Window:** 2026.07.01 → 2026.09.24 · currency · champ filters  
**Segments:** `tester_segment_3M_CLEAN.log` per task (stamp-bounded)

| Task | Geometry | n | WR | BWR | E_N | EF | Final | Pool |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| T02 (ref) | SL200/TP300 RR1.5 | 61 | 44.3% | 40.0% | +0.107 | +0.96 | $414.65 | KEEP |
| **T03** | SL300/**TP600** RR2 | 25 | 32.0% | 33.3% | **−0.04** | **−3.17** | $395.19 | **DROP** |
| **T04** | SL300/**TP300** RR1 | 49 | **59.2%** | 50.0% | **+0.184** | **+6.43** | **$425.48** | **KEEP** |
| **T05** | SL300/**TP=0** MID | 133 | 58.7% | 58.1%* | +0.010 | **−2.64** | $401.14 | **costs_fragile** |

\*Realised R≈0.72 from MID PnL → high BWR; BM only +0.56 pp.

## Verdicts

### T03 — Wider TP — **POOL_DROP**
WR fell below BWR on this window. Wider target did not pay; opposite of needed G5 headroom *here*. Do not deploy.

### T04 — Closer TP RR=1 — **POOL_KEEP** (thin)
Best **3M** sleeve in this batch: WR≅59% clears 50% BWR, EF +6.4, E_N≈champ long-run. Role: **Harvest / high-WR** (lower R). Note n=49 provisional; confirm on long window before sizing up.

### T05 — MID exit — **POOL_KEEP_costs_fragile**
Alive on E_N>0 and WR≳BWR but **EF≤0** after Leak (small R). Watch / small-f only until long blotter or cost model refined.

## P2 geometry phase (T01–T05) summary

| Preset | Pool | Role |
| --- | --- | --- |
| T01 SL200/TP450 | KEEP (long); 3M fragile | Survival (low BWR) |
| T02 SL200/TP300 | KEEP (3M) | Balanced-scale |
| T03 SL300/TP600 | **DROP** (3M) | — |
| T04 SL300/TP300 | KEEP (3M) | Harvest / high-WR |
| T05 TP off MID | costs_fragile (3M) | Mid-exit experimental |

**Next:** optional long-window confirm for T02/T04; or P2-T10 lock payoff mix from pool; re-try G5 on a KEEP member with TP≥450.
