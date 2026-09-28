# EDX-P25-T03 — One-side isolation REVIEW

**Scored:** 2026-09-25  
**Source:** `Tester/logs/20260925.log` → magics **8212504** / **8212505** CLEAN  
**Held:** SL300/TP450 · BBDev 2.2 · Cooldown 3 · session 12–20 · skip Tue  
**Changed:** AllowBuy xor AllowSell  
**Leak:** 2.2 pp · BWR 40% · R = RR = 1.5

## Inputs verified

| Leg | Magic | AllowBuy | AllowSell | BBDev | CD | Window end |
| --- | ---: | --- | --- | ---: | ---: | --- |
| T03a | 8212504 | true | false | 2.2 | 3 | 2026.09.24 |
| T03b | 8212505 | false | true | 2.2 | 3 | 2026.09.24 |

## Scorecard

| Leg | Window | n | opens B/S | WR% | E_N | EF | Zone | Final $ | Pool |
| --- | --- | ---: | --- | ---: | ---: | ---: | --- | ---: | --- |
| **Buy-only** | Long | 318 | 319/0 | 41.8 | 0.046 | **−0.38** | Negative | 427 | **DROP** |
| **Sell-only** | Long | 296 | 0/297 | 43.9 | 0.098 | **1.72** | Fragile | 488 | KEEP (dominated) |
| **Buy-only** | 3M | 27 | 28/0 | 44.4 | 0.111 | 2.24 | Fragile/thin | 408 | KEEP thin |
| **Sell-only** | 3M | 28 | 0/28 | 46.4 | 0.161 | 4.23 | Fragile/thin | 411 | KEEP thin |
| Growth both | Long | 420 | ~balanced | 47.4 | 0.185 | **5.18** | Robust* | 621 | ref |
| Growth both | 3M | 33 | — | 42.4 | 0.061 | 0.22 | Fragile/thin | 404 | ref |

## Verdict

| Finding | Decision |
| --- | --- |
| **Buy-only** | Long **fails Leak** (EF≤0). Not a deploy sleeve. |
| **Sell-only** | Clears pool bar on long but **far below** Growth dual (EF 1.72 vs 5.18). Dominated. |
| **Asymmetry** | Sell > buy on WR/E_N/EF (long and 3M). Useful for WR-side diagnosis; **do not** switch Growth to sell-only. |
| **P25 base** | Keep **AllowBuy + AllowSell**. Dual-side is the edge; one-side destroys / compresses it. |

**P25 phase close:** BBDev 2.0 DROP · BBDev 2.4 promising (optional later) · Cooldown 6 neutral · side isolation shows sell healthier but both sides required.

## Artifacts

```
blotter/archive/EDX-P25-T03/
  01_Long_…_8212504_buyOnly.log
  02_Long_…_8212505_sellOnly.log
  03_3M_…_8212504_buyOnly.log
  04_3M_…_8212505_sellOnly.log
  SCORECARD.csv / SCORECARD.json
  REVIEW.md
```

## Next

P25 complete. Options: (1) optional Long→Sep24 confirm on BBDev 2.4; (2) G5 re-open with TP≥450; (3) code-blocked P2-T06–T09.
