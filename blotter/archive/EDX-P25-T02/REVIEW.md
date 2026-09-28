# EDX-P25-T02 — CooldownBars=6 REVIEW

**Scored:** 2026-09-25  
**Source:** `Tester/logs/20260925.log` → magic **8212503** CLEAN extracts  
**Preset:** `EDX-P25-T02_cooldown6_GrowthBase_G0_long.set`  
**Held:** SL300/TP450 · BBDev **2.2** · session 12–20 · skip Tue · G0  
**Changed:** CooldownBars **6** (base 3)  
**Leak:** 2.2 pp · BWR 40% · R = RR = 1.5

## Scorecard

| Window | n | WR% | BM | E_N | EF | Zone | Final $ | vs Growth | Pool |
| --- | ---: | ---: | ---: | ---: | ---: | --- | ---: | --- | --- |
| **Long→Sep24** | 408 | 47.6 | +7.6 | **0.189** | **5.35** | Robust* | 619 | Growth n420 WR47.4 E_N0.185 EF5.18 $621 | **KEEP** |
| **3M→Sep24** | 33 | 42.4 | +2.4 | 0.061 | 0.22 | Fragile/thin | 404 | ≈ Growth 3M | **KEEP** thin |
| Growth Long | 420 | 47.4 | +7.4 | 0.185 | 5.18 | Robust* | 621 | ref | — |
| Growth 3M | 33 | 42.4 | +2.4 | 0.061 | 0.22 | Fragile/thin | 404 | ref | — |

Frequency: Long 408/420 ≈ **97%** — **no FREQUENCY_STALL**.

## Verdict

**POOL_KEEP** but **not an upgrade.** Cooldown 6 ≈ Growth on WR/E_N/EF/$; trims ~12 events with negligible health lift. Hold **CooldownBars=3** on Growth base for T03.

## Artifacts

```
blotter/archive/EDX-P25-T02/
  01_3M_to20260924_8212503_cooldown6.log
  02_Long_to20260924_8212503_cooldown6.log
  SCORECARD.csv / SCORECARD.json
  REVIEW.md
```

## Next

**EDX-P25-T03** — buy-only / sell-only (`8212504` / `8212505`), BBDev 2.2 + Cooldown 3 held.
