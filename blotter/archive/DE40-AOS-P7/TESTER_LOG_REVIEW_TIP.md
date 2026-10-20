# DE40stack — tip re-run (post-compile)

**Date:** 2026-10-19 ~17:08  
**Window:** 2026.05.01 → 2026.10.18 · DE30 M15  
**Preset / magic:** `DE40stack` / **26141907**  
**Log:** `Tester/logs/20261019.log`  
**Ledger:** `COMMON/Files/BMRG_AOS_ledger_26141907.csv`

---

## Verdict: **L2DET ARMED — CONFIRMED**

| Check | Result |
| --- | --- |
| Init | `model=L2det_de40_v1_BUY_near_atr` · LIVE_WITHHOLD · DE30 |
| Withhold | **PASS** — log `Entry blocked: AOS L2DET_SKIP_BUY_NEAR_ATR` |
| Ledger | **PASS** — `layer=L2DET` · FIRE 56 · SKIP 9 |
| Prior false alarm | Fixed by recompile after 16:58 |

---

## Tip score (deposit 500)

| Metric | DE40stack | P0 tip (AOS OFF, same day) |
| --- | ---: | ---: |
| Final balance | **550.61** | **638.90** |
| PnL | **+50.61** (+10.1%) | +138.90 |
| Entries (market) | 56 | — |
| L2det skips | **9** | 0 |

Offline CF reference: ARM n_fire 62 · skips 15 · E_N +0.42R (prior Leak). Tester skips 9 / fires 56 — same direction, slightly fewer skips (ATR live vs tape feature).

Absolute $ below P0 tip is expected if L4 `f_rec` &lt; 1 and/or skipped BUYs were not all losers — OS claim remains **research arm / expansion**, not P0 replace.

---

## Sign-off note

HITL research OS **wire verified** on tip. Keep monitoring; measured Leak still OPEN. Do not promote to live capital admit on this alone.
