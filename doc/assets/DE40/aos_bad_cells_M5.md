# DE40 M5 — AOS bad-cell registry (L2det seeds)

**Task:** DE40-M5-AOS-P0-T02 · **updated** DE40-M5-AOS-P1 (tape QA 2026-10-20)  
**Source:** [`system_profile_M5.md`](./system_profile_M5.md) · `tapes/de40_m5_*_fire_tape_v0.csv` · `blotter/archive/DE40-M5-AOS-P1/TAPE_QA.json`  
**Engine:** magic **26101903** · AOS OFF  
**Sibling:** [`aos_bad_cells.md`](./aos_bad_cells.md) (M15) — do not import M15 arm map without M5 CF

Seed cells for L2det SOFT maps. Arm only after P2 CF.

---

## Soft / skip candidates

| Cell | Evidence | Seed stance |
| --- | --- | --- |
| **Feb** | YTD n=28 · WR **35.7%** · E_N **−0.20R** | **PRIMARY** stress-month SOFT |
| **May MISMATCH** | Tip n=17 · WR **47.1%** · E_N **+0.06R** | SOFT on tag — **CF before blanket** (thin edge; not tip star) |
| **Oct FRAGILE** | Tip n=8 · WR **25%** · E_N **−0.44R** | **PRIMARY** residual FRAGILE SOFT (thin n — CF with Sep) |
| **Sep–Oct pocket** | n=29 · WR **44.8%** · E_N ≈0 | SOFT caution — never blanket Sep alone (Sep WR 52% / +0.18R) |
| **H14** | Tip n=4 · WR **25%** · E_N **−0.44R** | Thin hour SOFT — HOLD until more n / CF |
| **H16** | Tip n=9 · WR **33%** · E_N **−0.25R** | Soft late-session SOFT candidate |
| **BUY (tip)** | Tip BUY n=71 · WR **46.5%** · E_N **+0.05R** vs SELL **+0.43R** | Side-caution conjunction only — **never blanket BUY** |
| **Mon (YTD)** | YTD Mon WR 46.6% · tip Mon OK (+0.13R) | Soft on YTD only — not tip calendar |
| **Jun soft MATCH** | Tip n=19 · WR 47.4% · E_N +0.07R | Weak SOFT / size-down after CF |
| **Mar ATR-starved** | n=1 | Already engine-gated — OS mirror / no double-count |

---

## Protect cells (false-skip must be reported)

| Cell | Evidence | Why protect |
| --- | --- | --- |
| **Aug** | Tip n=34 · WR **64.7%** · E_N **+0.46R** | Star MATCH month |
| **Jul** | Tip n=24 · WR 58.3% · E_N +0.31R | MATCH home |
| **SELL** | Tip n=52 · WR **63.5%** · E_N **+0.43R** | Tip expectancy carrier |
| **Wed** | Tip n=30 · WR **63.3%** · E_N **+0.43R** | Tip star DOW |
| **H08 / H10 / H15** | Tip strong E_N | Session stars |
| **near_atr_cap (tip)** | Tip n=36 · WR **61.1%** · E_N **+0.38R** | Do **not** blanket-skip near ATR (unlike residual FRAGILE intuition) |
| **May→Aug tip-core** | n=94 · WR 56.4% · E_N +0.27R | Home tip-core |
| **Tue** | n=0 | Already filtered |

---

## Explicit non-seeds

| Idea | Why not |
| --- | --- |
| Reject asset on Feb / Oct | Regime tax / thin FRAGILE — not class death |
| Thin SL below ~7000 | Leak destroys EF under live spread ≈1020 |
| Import M15 BUY∧near_atr / H13 map | Wrong TF · tip near_atr is a **star** on M5 |
| Blanket AllowBuy=false | Buys still E_N>0 on tip |
| Journal Leak_proxy as Stage-1 | Tester spreads understate live — prior **7.0 pp** until deals |
| Arm `AOS_L2det_de.mqh` on M5 | M15 pin — use `AOS_L2det_de_m5.mqh` v1b instead |

---

## P2 arming result (2026-10-20)

See [`aos_l2_policy_M5.md`](./aos_l2_policy_M5.md) · `blotter/archive/DE40-M5-AOS-P2/P2_CF.json`.

| Seed | Outcome |
| --- | --- |
| BUY ∧ H14\|16 | **ARM_SOFT** (v1b leg) |
| BUY ∧ Oct | **ARM_SOFT** (v1b leg) |
| **v1b stack** | **ARM_SOFT preferred** · ΔE_N +0.081 · SELL FP 0 |
| H14\|16 all sides | **HOLD** (SELL FP) |
| Oct all sides | **HOLD** (1 SELL FP) |
| Oct ∨ H14\|16 | **HOLD** max ΔE_N · more SELL FP |
| Feb | **ARM_SOFT on YTD only** |
| Blanket BUY / near_atr / BUY∧near_atr | **REJECT / DISARM** |
| Blanket MISMATCH / Sep–Oct | **HOLD / DISARM** |
| L2AI | **DISARM** (AUC≈0.51) |

Reject any map that false-skips **Aug / SELL / Wed / tip near_atr** above the iteration bar.
