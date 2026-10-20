# USDJPY — AOS bad-cell registry (L2det seeds)

**Task:** USDJPY-AOS-P0-T02 · **updated P2** 2026-10-19  
**Source:** `system_profile.md` · dedicated tip (P0) · P1 long-filter tip · P2 CF (`P2_CF.json`)  
**Engine:** magic **26101828** · AOS OFF  

Seed cells for L2det SOFT maps. Armed status from P2 under `edge_framework.md` / [`aos_l2_policy.md`](./aos_l2_policy.md).

---

## Soft / skip candidates

| Cell | Dedicated tip (n=56) | P1 long-filter tip (n=46) | P2 tip CF | Stance |
| --- | --- | --- | --- | --- |
| **near_atr / SELL∧near_atr** | (not sliced) | near_atr n=7 · **WR 0%** | **ARM_SOFT** · ΔE_N +0.20 / +0.10 · protect FP 0 | **ARMED** primary |
| **H16** | thin | n=3 · WR 0% | **ARM_SOFT** · ΔE_N +0.08 · protect FP 0 | **ARMED** (thin) |
| **near_atr∨H16 (v1c)** | — | — | **ARM_SOFT** · ΔE_N **+0.27** · ret 80% | **ARMED** preferred stack |
| **Jul** | WR 33% · E_N −0.27R | WR **29%** · E_N **−0.37R** | HOLD_SOFT · ΔE_N +0.21 · BUY/Fri FP | HOLD challenger |
| **H14** | WR 43% soft | WR 50% flat | HOLD_SOFT · ΔE_N 0 · BUY FP | HOLD |
| **Thu** | WR **31%** soft | WR **56%** star | **DISARM** · ΔE_N −0.03 | **DISARM** (path-sensitive) |
| **SELL** (blanket) | fire-heavy ≈BWR | still thinner than BUY | REJECT_FREQUENCY_STALL (ret 39%) | Never blanket SELL |

---

## Protect cells (false-skip must be reported)

| Cell | P1 tip evidence | Why protect |
| --- | --- | --- |
| **BUY** | WR 56% · E_N +0.22R | Expectancy carrier (both tapes) |
| **Fri** | WR 56% · E_N +0.22R | Tip star |
| **H12 / H15** | H12 58% · H15 71% | Session stars |
| **May / Jun** | E_N +0.22 / +0.27R | MATCH home months |
| **Aug** | thin but +0.65R | Recover month |

Armed maps (near_atr · H16 · v1c · SELL∧near_atr) scored **0** protect FP on tip. Jul stacks still tax BUY/Fri/H12·H15.

Mon flipped soft on P1 tape (−0.04R) vs star on dedicated — report false-skip; do not permanently protect or skip Mon from one path.

---

## Explicit non-seeds

| Idea | Why not |
| --- | --- |
| Blanket AllowSell=false | Sell volume ≠ permanent side death · ret collapse |
| Blanket AllowBuy=false | Buys carry tip |
| Hard-arm Thu | DISARM on P2 tip · flipped vs dedicated |
| Hard-arm Jul alone | HOLD — protect FP · calendar-only |
| Lift ATR max / open Tokyo | Geometry / failed probe — new preset only |
| Sep skip layer | Already starved by ATR≤70 |
| Import EUR BUY-caution / UK H08 / DE40 maps | Wrong fingerprint |
| LIVE_WITHHOLD L2AI | Train overlaps tip · holdout AUC ~0.55 |
| Replace Leak prior with journal 3.6pp proxy | Optimistic · Stage-1 still prior 11.4 pp |

---

## P2 arming result

1. ~~Jul alone~~ → **HOLD_SOFT**  
2. **near_atr** / **SELL∧near_atr** → **ARM_SOFT**  
3. **H16** → **ARM_SOFT** (thin)  
4. Thu → **DISARM**  
5. Preferred stack → **`v1c = near_atr OR H16`** (**ARM_SOFT**)
