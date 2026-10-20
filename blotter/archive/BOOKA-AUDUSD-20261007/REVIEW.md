# BOOKA-AUDUSD-20261007 — Harvest extract (expansion, not live replace)

**Lens:** Asset-list expansion · engine-only · **AOS OFF** · own AIOS later.  
**Not** a live INF / `8210204` replacement.  
**Source:** Tester `logs/20261007.log` (duplicate run identical)  
**Preset:** `Profiles/Tester/BMRG/BOOKA-Harvest_AUDUSD_M5_G0.set` · magic **8221103**  
**Window scored:** **2026.05.01 → 2026.08.31** · AUDUSD M5 · every tick · deposit $400 · ACCOUNT CURRENCY  
**Reviewed:** 2026-10-07

## Preset / geometry (confirmed in log)

| Field | Locked | Observed |
| --- | --- | --- |
| BB | 20 / **2.2** | init `BB(20,2.2)` |
| SL/TP | **300 / 300** RR=1.0 | fills show ±0.00300 from entry |
| Event | G0 MaxLevels=1 · MaxEntries=1 | single-ticket path |
| Session | 12–20 · skip Tue | regime_filtered by design |
| Risk | 0.5% equity · MaxLot 1.0 | lotMode=1 |
| AOS | OFF · kill-switch on | `aos=0` |

EURUSD-calibrated points transferred as-is — acceptable for Stage-0 expansion; ATR retune only if Leak/RR−R fails later.

## Key metrics (May→Aug)

| Metric | Value |
| --- | ---: |
| Final / PnL | **444.39** / **+44.39** (+11.1%) |
| Opens / closes (n) | 59 / **58** |
| TP / SL | 36 / 22 |
| WR | **62.1%** |
| E_N (R=1 approx) | **+0.241R** |
| Side mix | buy 28-ish / sell 31-ish (near balanced) |
| Hold | med **24h** · mean 38h · ≥12h **74%** (meanrev overnight common) |

No equity halt · no daily-loss close · no FailPause. Loss-streak keyword appears twice (containment light, not a wipeout).

## Rolling windows (30d / step 15d)

| Window | n | WR | E_N | Read |
| --- | ---: | ---: | ---: | --- |
| May04→Jun03 | 18 | 72.2% | +0.444R | Strong |
| May19→Jun18 | 21 | 61.9% | +0.238R | Solid |
| Jun03→Jul03 | 13 | 53.8% | +0.077R | Thin positive (soft regime dip) |
| Jun18→Jul18 | 10 | 80.0% | +0.600R | Best pocket |
| Jul03→Aug02 | 17 | 58.8% | +0.176R | Hold |
| Jul18→Aug17 | 14 | 57.1% | +0.143R | Hold |
| Aug02→Sep01 | 10 | 60.0% | +0.200R | Soft-stress Aug **pass** |
| Aug17→Sep16 | 6 | 50.0% | 0.000R | Stub / small-n flat — not a reject |

**Monthly:** May +0.375R · Jun +0.143R · Jul +0.222R · Aug +0.200R — all months positive.

## Vs prior Book A AUD (2026-10-06)

| Window | PnL | Opens | Expansion read |
| --- | ---: | ---: | --- |
| Jan→Oct (prior) | +32.18 | 168 | Thin but keep |
| May→Oct (prior) | +28.40 | 73 | Small-n support |
| **May→Aug (today)** | **+44.39** | **59** | **Stronger mid-window** |

May→Aug alone beats May→Oct equity → **Sep (and late path) likely ate prior edge**. Frame that as **regime mismatch on the longer tip**, not geometry death. Do not cut AUDUSD from the expansion queue.

## Expansion verdict

**KEEP — promote AUDUSD in the Book A research queue** (engine extract clears this window’s soft WR/E_N bar).

Next (still not live):

1. Export deals → Stage-1 EF / Leak on May→Aug (and optionally full Ouroboros tip).  
2. If Sep→Oct re-run shows WR collapse only in that regime → schedule mild ATR-scaled SL/TP or session tweak **before** inventing AIOS.  
3. Per-symbol AIOS only after engine ACCEPT — own pin/withhold, not EUR L2 copy-paste.  
4. Live FT stays **EURUSD · 8210204 · INF LIVE_WITHHOLD**.

## Live / correlation boundary

USD-fade cluster with EUR/GBP — expansion candidate ≠ diversified Stage-3 capital.
