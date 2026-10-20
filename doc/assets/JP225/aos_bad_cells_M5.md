# JP225 / JPN225 M5 — AOS bad-cell registry (L2det seeds)

**Task:** JP225-M5-AOS-P0-T02 · **updated** JP225-M5-AOS-P1 (tape QA 2026-10-20)  
**Source:** [`system_profile_M5.md`](./system_profile_M5.md) · `tapes/jp225_m5_*_fire_tape_v0.csv` · `blotter/archive/JP225-M5-AOS-P1/TAPE_QA.json`  
**Engine:** magic **26101906** · AOS OFF  
**Sibling:** [`aos_bad_cells.md`](./aos_bad_cells.md) (M15 May∨Jul / MATCH-protect) — **do not import** without M5 CF

Seed cells for L2det SOFT maps. Arm only after P2 CF.

---

## Soft / skip candidates

| Cell | Evidence (tip unless noted) | Seed stance |
| --- | --- | --- |
| **Aug MATCH** | n=17 · WR **29.4%** · E_N **−0.12R** | **PRIMARY** MATCH-month SOFT |
| **Sep MATCH** | n=17 · WR **23.5%** · E_N **−0.29R** | **PRIMARY** MATCH-month SOFT |
| **Aug∨Sep MATCH pocket** | n=34 · WR 26.5% · E_N **−0.21R** | Stack SOFT after CF |
| **Wed** | tip n=22 · WR **31.8%** · E_N **−0.05R** | DOW SOFT — CF before blanket |
| **Mon** | tip n=24 · WR **33.3%** · E_N **0** | Soft / size-down — CF |
| **H09** | tip n=6 · WR **16.7%** · E_N **−0.50R** | Thin hour SOFT |
| **H13** | tip n=20 · WR **30%** · E_N **−0.10R** | Midday SOFT candidate |
| **H16** | tip n=6 · WR **16.7%** · E_N **−0.50R** | Late-session SOFT (thin) |
| **BUY (tip)** | tip BUY n=46 · WR **34.8%** · E_N **+0.04R** vs SELL **+0.44R** | Side-caution **conjunction** only — **never blanket BUY** |
| **Feb** (YTD/prior) | n=10 · WR **20%** · E_N **−0.40R** | Soft pre-tip SOFT |
| **Apr** (YTD/prior) | n=10 · WR **10%** · E_N **−0.70R** | Soft pre-tip SOFT |

---

## Protect cells (false-skip must be reported)

| Cell | Evidence | Why protect |
| --- | --- | --- |
| **Jul MISMATCH** | tip n=20 · WR **60%** · E_N **+0.80R** | **Star month** |
| **Jun FRAGILE** | tip n=17 · WR 47.1% · E_N **+0.41R** | FRAGILE that pays |
| **Oct MISMATCH** | tip n=10 · WR 50% · E_N **+0.50R** | Pays |
| **OFFHOME pocket** | n=60 · WR 50% · E_N **+0.50R** | Tip expectancy carrier |
| **Thu** | tip n=22 · WR **54.5%** · E_N **+0.64R** | Tip star DOW |
| **Fri** | tip n=26 · WR 46.2% · E_N **+0.38R** | Tip strong DOW |
| **H08** | tip n=19 · WR **52.6%** · E_N **+0.58R** | Session open star |
| **H10** | tip n=9 · WR **88.9%** · E_N **+1.67R** | Session star (thin n — still protect) |
| **SELL** | tip n=48 · WR **47.9%** · E_N **+0.44R** | Tip expectancy carrier |
| **near_atr_cap (tip)** | tip n=23 · WR 43.5% · E_N **+0.30R** | Do **not** blanket-skip near band max |
| **Tue** | n=0 | Already filtered |
| **Tip aggregate** | n=94 · EF prior **+4.9 pp** | Home tip |

---

## Explicit non-seeds

| Idea | Why not |
| --- | --- |
| Import M15 **May∨Jul** LIVE_WITHHOLD | Wrong TF — May/Jul **pay** on M5 |
| Protect **Aug/Sep MATCH** as “home” | MATCH is the **tax** on M5 |
| Blanket all FRAGILE / all MISMATCH | Jun FRAGILE + Jul/Oct MISMATCH are stars |
| Blanket AllowBuy=false | Buys still E_N>0 on tip (thin) |
| Reject asset on Aug–Sep | Regime/TF mismatch — not class death |
| Thin SL below ~25000 | Leak destroys EF under live ≈2300 |
| Arm `AOS_L2det_jp.mqh` / `JPN225stack` on M5 | M15 pin — use future `AOS_L2det_jp_m5.mqh` only |
| Journal Leak_proxy as Stage-1 | Tester med ~1400 ≪ live 2300 — prior **3.3 pp** until deals |

---

## P2 arming result (2026-10-20)

See [`aos_l2_policy_M5.md`](./aos_l2_policy_M5.md) · `blotter/archive/JP225-M5-AOS-P2/P2_CF.json`.

| Seed | Outcome |
| --- | --- |
| BUY ∧ MATCH (Aug/Sep) | **ARM_SOFT** (v1c leg) |
| BUY ∧ H09\|13\|16 | **ARM_SOFT** (v1c leg) |
| **v1c stack** | **ARM_SOFT preferred** · ΔE_N +0.234 · SELL/H08/H10 FP 0 · Jul FP 1 |
| MATCH all sides | **HOLD** (6 SELL FP) |
| Aug / Sep all sides | **HOLD** / prefer BUY∧ |
| Wed / Mon / hour all sides | **HOLD / REJECT** protect FP |
| Blanket BUY / FRAGILE / MISMATCH / near_atr | **REJECT** |
| Feb / Apr | **ARM_SOFT on YTD only** |
| L2AI | **DISARM** (AUC≈0.49) |

Reject any map that false-skips **Jul / Jun / Oct / OFFHOME / Thu / H08 / H10 / SELL** above the iteration bar.
