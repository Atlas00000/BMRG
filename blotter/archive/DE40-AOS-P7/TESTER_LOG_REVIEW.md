# DE40stack — Tester log review

**Date:** 2026-10-19  
**Log:** `Tester/logs/20261019.log` (UTF-16)  
**Ledger:** `COMMON/Files/BMRG_AOS_ledger_26141907.csv` (last window overwrites)  
**Deposit assumed:** 500 USD

---

## Verdict

| Check | Result |
| --- | --- |
| Preset / magic | **PASS** — `26141907` · `InpAOS_DE_L2detEnable=true` · LIVE_WITHHOLD |
| Init banner | **PASS** — `model=L2det_de40_v1_BUY_near_atr_20261019` · `sym=DE30` · aos=1 |
| L2det withhold | **FAIL** — **0** `BUY_NEAR_ATR` skips in all DE40stack windows |
| Ledger path | **SUSPECT** — rows are `layer=L2` / `FIRE` / non-zero `ai_proba` (FX AI path), **not** `L2DET` |
| Tip May→Oct OS | **NOT RUN** — longest tip-like OS window is May→Aug |
| Recompile | Tester runs **16:53–16:56**; `BMRG.ex5` rebuilt **16:58** — re-run required |

**Bottom line:** DE40stack **loaded** and made money on May→Aug, but **L2det BUY∧nearATR did not block entries** in these logs. Treat balances as L3/L4/engine only until a re-run shows `L2DET` / `Entry blocked: AOS L2DET_SKIP_BUY_NEAR_ATR`.

---

## DE40stack windows (magic 26141907)

| Window | Final bal | PnL | Market entries | L2det BUY_NEAR skips |
| --- | ---: | ---: | ---: | ---: |
| **2026.05.01 → 08.31** | **558.07** | **+58.07** | 48 | **0** |
| 2026.01.01 → 08.31 | 479.59 | −20.41 | 52 | 0 |
| 2026.01.01 → 04.30 | 479.59 | −20.41 | 52 | 0 |
| 2025.09.01 → 12.31 | 434.27 | −65.73 | 51 | 0 |
| 2025.05.01 → 08.31 | 476.11 | −23.89 | 51 | 0 |
| 2026.05.01 → 06.30 | 509.93 | +9.93 | 14 | 0 |
| 2026.02.01 → 03.31 | 460.21 | −39.79 | 18 | 0 |

Entry blocks observed = engine **ATR max** (`ATR … > max 4070`), not L2det.

History gap: Tester warned **no data 2025.01–04**.

---

## P0 baseline (earlier same day, magic 26101902, AOS OFF)

| Window | Final bal |
| --- | ---: |
| 2026.01.01 → 10.18 | 612.43 |
| **2026.05.01 → 10.18 (tip)** | **638.90** |
| 2025.06 → 2026.10 (broker depth) | 423.49 |

---

## Ledger sample (last run = Feb→Mar, n=18)

All rows: `decision=FIRE` · `layer=L2` · `reason=FIRE_OK` · `mode=LIVE_WITHHOLD` · `model=L2det_de40_…` · `ai_proba≈0.02–0.04`.

Expected when DE path is live: `layer=L2DET` and occasional `SKIP` / `L2DET_SKIP_BUY_NEAR_ATR`.

---

## Action

1. Confirm MetaEditor compile **after** `AOS_L2det_de.mqh` wire (ex5 ≥ 16:58 done).  
2. Re-run **DE40stack** tip **2026.05.01 → 2026.10.18** (or → today).  
3. Confirm log contains `Entry blocked: AOS L2DET_SKIP_BUY_NEAR_ATR` and ledger `layer=L2DET`.  
4. Only then score OS Δ vs P0 tip (638.90 / offline ARM n=62).
