# DE40 — AOS bad-cell registry (L2det seeds)

**Task:** DE40-AOS-P0-T02 · **updated** DE40-AOS-P1 (tape QA 2026-10-19)  
**Source:** `system_profile.md` · `tapes/de40_*_fire_tape_v0.csv` · `blotter/archive/DE40-AOS-P1/TAPE_QA.json`  
**Engine:** magic **26101902** · AOS OFF  

Seed cells for L2det SOFT maps. P2 CF complete — see arming result below. Do not mutate mid-book without a new task.

---

## Soft / skip candidates

| Cell | Evidence | Seed stance |
| --- | --- | --- |
| **Feb** | YTD n=29 · WR **34%** · E_N≪0 | **PRIMARY** stress-month SOFT |
| **Mar FRAGILE** | YTD n=4 · WR **0%** | **PRIMARY** FRAGILE SOFT (conjunction with tag) |
| **MISMATCH month** | 2025-06/07 stub WR ~32%; tip May MISMATCH still won | SOFT on tag — **CF before blanket** (May tip WR 67%) |
| **near_ATR ∧ FRAGILE residual** | Sep–Oct under ATR≤4070 | SOFT caution — never blanket Sep/Oct |
| **H13** | Tip n=12 · WR **41.7%** · E_N **−0.06R** | SOFT hour candidate |
| **H09** | Tip n=5 · WR **40%** · E_N **−0.10R** | Thin — HOLD until more n; do not arm alone |
| **BUY ∧ near_atr** | Tip BUY WR 54% / E_N +0.22 (weaker than SELL) | SOFT buy-caution conjunction only — **never blanket BUY** |
| **Wed** | Tip n=16 · WR **50%** · E_N +0.13R | Softest DOW but > BWR — HOLD / weak SOFT only after CF |

---

## Protect cells (false-skip must be reported)

| Cell | Evidence | Why protect |
| --- | --- | --- |
| **Aug** | Tip n=33 · WR **64%** · E_N +0.43R | Tip star month |
| **SELL** | Tip n=40 · WR **62.5%** · E_N **+0.41R** | Tip expectancy carrier |
| **Mon** | Tip n=25 · WR **64%** · E_N **+0.44R** | Tip star DOW |
| **Fri** | Tip n=15 · WR **60%** · E_N +0.35R | Tip star DOW |
| **H08** | Tip n=26 · WR **61.5%** · E_N +0.38R | Frankfurt open is a **star** (≠ UK H08 soft) |
| **H12 / H14** | Tip WR 78% / 73% | Mid-session stars |
| **May tip** | n=9 · WR 67% despite MISMATCH tag | Do not blanket-MISMATCH-skip |
| **Jun / Jul MATCH** | Tip WR 50% · net + | Home sleeve |
| **Tue** | n=0 | Already filtered |

---

## Explicit non-seeds

| Idea | Why not |
| --- | --- |
| Reject asset on 2025 stub | MISMATCH regime tax |
| Thin SL below ~5000 | Leak destroys EF under live spread ≈1020 |
| Blanket H08 skip | Tip H08 is strong — UK map does **not** transfer |
| Blanket AllowBuy=false | Buys still E_N>0 on tip |
| Import UK Thu/H08 or EUR maps | Wrong fingerprint |
| Journal Leak_proxy (1.5 pp) as Stage-1 | Tester spreads understate live — prior 9.8 pp until deals |

---

## P2 arming result (2026-10-19)

See [`aos_l2_policy.md`](./aos_l2_policy.md) · `blotter/archive/DE40-AOS-P2/P2_CF.json`.

| Seed | Outcome |
| --- | --- |
| BUY∧near_atr | **ARM_SOFT** (primary) |
| H13 | **HOLD_SOFT** (Aug FP) |
| H13∨BUY∧near_atr | **HOLD_SOFT** (best ΔE_N · more Aug FP) |
| Feb | **ARM_SOFT on YTD only** — not tip calendar |
| Blanket MISMATCH / BUY | **DISARM** |
| L2AI | **DISARM** (AUC≈0.51) |

Reject any map that false-skips **Aug / SELL / Mon / H08 / H12 / H14** above the iteration bar.
