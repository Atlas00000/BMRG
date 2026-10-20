# JP225 — AOS bad-cell registry (L2det seeds)

**Task:** JP225-AOS-P0-T02 · **updated P1-T03** 2026-10-19  
**Source:** `blotter/archive/JP225-AOS-P1/TAPE_QA.json` · tip tape n=79 · magic **26101904**  
**Engine:** Growth P1 · AOS OFF  

Seed cells for L2det SOFT maps. Not armed until P2 CF under `edge_framework.md`. Do not mutate mid-book without a new task.

---

## Soft / skip candidates (tip primary)

| Cell | Tip evidence | Seed stance |
| --- | --- | --- |
| **May FRAGILE** | n=23 · WR **30.4%** · E_N **−0.24R** | **PRIMARY** SOFT skip / size-down |
| **Jul MISMATCH** | n=13 · WR **30.8%** · E_N **−0.23R** | **PRIMARY** stress-month SOFT |
| **Wed** | n=20 · WR **30.0%** · E_N **−0.25R** | **PRIMARY** DOW SOFT (new from tape) |
| **H08** | n=8 · WR **25.0%** · E_N **−0.38R** | SOFT hour (London open) · small-n |
| **H09** | n=7 · WR **28.6%** · E_N **−0.29R** | SOFT hour · small-n |
| **H14** | n=22 · WR **36.4%** · E_N **−0.09R** | SOFT hour (largest mid-session soft) |
| **SELL** (volume) | n=48 · WR **39.6%** · E_N **−0.01R** ≈ flat | SOFT sell-caution — **never blanket SELL** |
| **Oct MISMATCH** | long n=6 · WR 33% | Thin — HOLD until n≥15 |
| **near_atr ∧ May/Jul/Wed** | conjunction only | Prefer over near_atr alone |

---

## Protect cells (false-skip must be reported)

| Cell | Tip / long evidence | Why protect |
| --- | --- | --- |
| **Aug MATCH** | n=23 · WR **52.2%** · E_N **+0.30R** | Tip home star |
| **Sep MATCH** | long n=20 · WR **50%** · E_N **+0.25R** | Home continuation |
| **Jun FRAGILE (paying)** | n=20 · WR **55%** · E_N **+0.38R** | Never blanket FRAGILE |
| **BUY** | n=31 · WR **48.4%** · E_N **+0.21R** | Tip expectancy carrier |
| **Thu** | n=18 · WR **50%** · E_N **+0.25R** | Tip star DOW |
| **Mon** | n=21 · WR **47.6%** · E_N **+0.19R** | Tip OK DOW |
| **H15** | n=7 · WR **57.1%** · E_N **+0.43R** | Mid-session star (small-n) |
| **H13** | n=16 · WR **50%** · E_N **+0.25R** | Mid-session OK |
| **near_atr_cap alone** | n=10 · WR **60%** · E_N **+0.50R** | **Pays on tip** — do **not** arm as skip alone |
| Geometry / Fade path | tp_lt_sl=0 · R=1.50 | Do not skip via SL/TP/Fade mutate |

---

## Explicit non-seeds

| Idea | Why not |
| --- | --- |
| Blanket FRAGILE skip | Kills **Jun** (+0.38R) |
| Blanket MATCH / BUY skip | Kills home / carrier |
| Blanket near_atr skip | Tip near_atr **WR 60%** — opposite of DE40 story |
| Thin SL / lift MaxSpread | Fat Nikkei spread · Leak collapses |
| Import DE40 BUY∧near_atr / UK H08 / EUR maps | Wrong fingerprint (H08 soft here ≠ UK map) |
| Permanent AllowSell=false | Sells fire-heavy but not class death; caution only |
| Re-open Tokyo 02–09 | Failed design probe |

---

## P2 arming result (2026-10-19) — see `aos_l2_policy.md`

| Order | Map | Result |
| --- | --- | --- |
| 1 | May-FRAGILE alone | **ARM_SOFT** · tip EF cleared · Jun/Aug FP 0 |
| 2 | Jul MISMATCH | **ARM_SOFT** |
| 3 | **May ∨ Jul** | **ARM_SOFT primary** · EF −1.3→**+9.2 pp** · ret 54% |
| 4 | Wed | **HOLD_SOFT** (Aug FP) |
| 5 | H14 / H08 / H09 | HOLD / weak ARM |
| 6 | SELL∧May | **ARM_SOFT** narrow (prec 86%) |
| 7 | May∨Jul∨Wed / FRAGILE all | **REJECT_FREQUENCY_STALL** |
| — | near_atr alone · L2AI | **DISARM** |

Reject any map that false-skips Aug/Sep MATCH, paying Jun, BUY, Thu/Mon, or H13/H15 above the iteration bar.
