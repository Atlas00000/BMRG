# USDJPY-AOS-P7 — Tester + chart log review

**Date:** 2026-10-19 ~17:13–17:15  
**Source:** Agent `20261019.log` (Tester) · Terminal `MQL5/Logs/20261019.log` (chart)  
**Preset / magic:** `USDJPYstack` · **26131807**  
**Verdict:** **CONFIRMED** — research OS armed, L2det live, test passed

## Tester (Agent)

| Field | Value |
| --- | --- |
| Window | 2026.05.01 → 2026.10.18 |
| Result | **Test passed** · 10.3M ticks · 11604 bars · ~2.0s |
| Init | AOS ON · L2mode=`LIVE_WITHHOLD` · model=`L2det_usdjpy_v1c_near_atr_OR_H16_20261019` |
| Semver | WARN expected: input `L2skip_usdjpy_DISARM` vs baked `L2det_usdjpy_v1c` — **using baked** |
| Deposit → final | 500.00 → **527.01** (**+27.01**, +5.4%) |
| Trades | **n=40** (buy 15 / sell 25 by market open) |
| Exits | TP **25** · SL **15** → WR **62.5%** |
| L2det skips | NEAR_ATR **9** · H16 **2** · total **11** |
| Other blocks (sample) | ATR · session · weekday as designed |

### vs offline P4 tip v1c CF

| | Offline tip v1c | This Tester run |
| --- | --- | --- |
| Window | tip (narrower) | May–Oct full |
| n_fire / n_skip | 37 / 9 | 40 / 11 |
| WR | 62.16% | **62.5%** |
| Note | E_N +0.37 offline | PnL +27.01 on 500; Leak still prior OPEN |

WR aligns with offline v1c. Count/window differ (full May–Oct vs tip slice) — expected.

## Chart attach (Terminal 17:15:38)

- Same WARN + **AOS ON** · model v1c · magic **26131807** · ledger `BMRG_AOS_ledger_26131807.csv` (0 bytes — no fires yet)
- Init OK · side=NONE · no signal on bar 16:00
- Chart `fade=0` (Tester run had fade=1 from preset) — confirm chart inputs match `USDJPYstack` if fade intended

## Open

- Measured Leak still **OPEN** (prior 11.4 pp until deal-cost ledger)
- Not production / not live FX replace
