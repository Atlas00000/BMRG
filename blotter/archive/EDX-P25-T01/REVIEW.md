# EDX-P25-T01 — BBDev sensitivity REVIEW

**Scored:** 2026-09-25  
**Source:** `Tester/logs/20260925.log` → magic-keyed CLEAN extracts (TRADE / TP / SL / init / final only)  
**Base:** Growth P4-T01 · SL300/TP450 · session 12–20 · skip Tue · BBDev **2.2**  
**Leak proxy:** 2.2 pp (pool L1) · BWR 40% · R = RR = 1.5

## Windows actually run

| Run | Magic | BBDev | Tester from→to |
| --- | ---: | ---: | --- |
| T01a 3M | 8212501 | 2.0 | 2026.07.01 → 2026.08.31 |
| T01a Long | 8212501 | 2.0 | 2025.01.01 → **2026.08.31** |
| T01a 3M (re-run) | 8212501 | 2.0 | 2026.07.01 → **2026.09.24** |
| T01b Long | 8212502 | 2.4 | 2025.01.01 → **2026.08.31** |
| T01b 3M | 8212502 | 2.4 | 2026.07.01 → 2026.08.31 |
| T01b 3M (re-run) | 8212502 | 2.4 | 2026.07.01 → **2026.09.24** |

Growth ref = Long/3M → **2026.09.24**. Long legs here end **Aug31** — Δ vs Growth is approximate until Long→Sep24.

## Scorecard

| Leg | Window | n | WR% | BM | E_N | EF | Zone | Final $ | Pool |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- | ---: | --- |
| **T01a BBDev 2.0** | Long→Aug31 | 447 | 44.3 | +4.3 | 0.107 | **2.10** | Fragile | 534 | KEEP (dominated) |
| **T01a BBDev 2.0** | 3M Jul–Aug | 26 | 34.6 | −5.4 | −0.135 | **−7.58** | Negative | 389 | **DROP** |
| **T01a BBDev 2.0** | 3M→Sep24 | 34 | 41.2 | +1.2 | 0.029 | **−1.02** | Negative | 406 | **DROP** (EF≤0) |
| **T01b BBDev 2.4** | Long→Aug31 | 360 | **47.8** | +7.8 | **0.194** | **5.58** | Robust* | 607 | KEEP (n&lt;385) |
| **T01b BBDev 2.4** | 3M Jul–Aug | 24 | 54.2 | +14.2 | 0.354 | 11.97 | Fragile/thin | 425 | KEEP thin |
| **T01b BBDev 2.4** | 3M→Sep24 | 33 | 48.5 | +8.5 | 0.212 | **6.28** | Fragile/thin | 420 | KEEP thin |
| Growth BBDev 2.2 | Long→Sep24 | 420 | 47.4 | +7.4 | 0.185 | 5.18 | Robust* | 621 | ref |
| Growth BBDev 2.2 | 3M→Sep24 | 33 | 42.4 | +2.4 | 0.061 | 0.22 | Fragile/thin | 404 | ref |

## Verdict

| Task | Decision |
| --- | --- |
| **T01a (BBDev 2.0)** | **Not an upgrade.** Long clears pool bar but WR/E_N/EF/$ worse than Growth / T01b. Both 3M windows **DROP** (EF≤0; Jul–Aug also WR&lt;BWR). Narrower bands → more events, worse quality. |
| **T01b (BBDev 2.4)** | **Promising hygiene candidate.** Long→Aug31: higher WR/E_N/EF than Growth snapshot; fewer trades. 3M→Sep24 EF **6.28** ≫ Growth 3M 0.22. Do **not** replace Growth base until Long→**2026.09.24** and n≥385. Optional later pool role: *Growth-tight* entry. |
| **P25 base** | Hold **BBDev 2.2** for T02/T03. |

**Side read:** Wider k (2.4) filters WR-side noise; narrower (2.0) hurts — consistent with WR-side diagnosis.

## Artifacts

```
blotter/archive/EDX-P25-T01/
  01_3M_Aug31_8212501_BBDev2.0.log
  02_Long_Aug31_8212501_BBDev2.0.log
  03_3M_Sep24_8212501_BBDev2.0.log
  04_Long_Aug31_8212502_BBDev2.4.log
  05_3M_Aug31_8212502_BBDev2.4.log
  06_3M_Sep24_8212502_BBDev2.4.log
  SCORECARD.csv / SCORECARD.json
  REVIEW.md
```

## Next

**EDX-P25-T02** — `EDX-P25-T02_cooldown6_GrowthBase_G0_long.set` (magic **8212503**), BBDev **2.2**. Prefer tester end **2026.09.24**.
