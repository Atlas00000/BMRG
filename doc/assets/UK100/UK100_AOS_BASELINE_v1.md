# UK100_AOS_BASELINE_v1

**Task:** UK100-AOS-P0-T01  
**Frozen:** 2026-10-12  
**Engine:** Balanced P0 · magic **26101201** · AOS **OFF**  
**Preset:** `BMRG-M15-UK100-6M-P0_balanced_chart.set`  
**Evidence:** Tester `logs/20261012.log` · `system_profile.md` · `blotter/archive/UK100-P0-CHART/`  
**Deposit:** $500 · every tick · ACCOUNT CURRENCY  

This packet is the **OS compare baseline**. OS trials report Δ vs these rows. Do not mutate geometry to “beat” this file — change overlay only.

---

## Geometry lock

| Parameter | Value |
| --- | --- |
| SL / TP | 2500 / 3125 (RR 1.25 · BWR 44.4%) |
| BB | 20 / 2.2 |
| Session | 08:00–17:00 · skip Tue |
| ATR | max 1470 ON |
| Lot | 0.1 |
| AOS | OFF |

---

## Window scoreboard (journal-gross · Leak prior 2.9 pp)

| Window | n | WR | E_N | BM | EF_prior | Final Δ | Role |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| **May→Aug 2026 tip** | **51** | **49.0%** | **+0.103R** | +4.6 pp | **+1.7 pp** | **+$17.14** | **OS default compare** |
| Jan→Apr 2026 prior | 75 | 45.3% | +0.020R | +0.9 pp | −2.0 pp | +$4.48 | L3 diagnostic |
| Hist 2025.12.17→2026.08 | 131 | 45.8% | +0.031R | +1.4 pp | −1.5 pp | +$10.97 | Truncated context |

`hist_from` = **2025.12.17**.

**Leak on this freeze:**

| Source | Leak | Tip EF | Authority |
| --- | ---: | ---: | --- |
| `prior` (design) | 2.9 pp | +1.68 pp | Footnote / preset meta |
| `journal_2x_entry_spread_median` | **4.27 pp** | **+0.31 pp** | **Interim OS** (`UK100-AOS-P0-T03`) |
| `measured` | — | — | OPEN (deal export) |

OS trials: report ΔE_N vs tip row; footnote EF under journal proxy until deals land.

---

## Tip fingerprint (OS must not destroy)

| Slice | Tip value |
| --- | --- |
| BUY / SELL WR | 38.5% / **60.0%** |
| Best DOW | Wed WR 81.8% |
| Soft DOW | Thu WR 30.8% |
| Soft hour | H08 WR 30.8% |
| Max W / L streak | 6 / 6 |
| Hold≥12h | ~6% |

---

## Expansion posture

| Ladder | Verdict |
| --- | --- |
| Expansion (`edge_framework.md`) | **EXPANSION_KEEP** (provisional) |
| Production G0–G5 | **NOT PRODUCTION-WORTHY** |

Bump to `UK100_AOS_BASELINE_v2` only when: measured Leak replaces prior on the same tip window, or geometry intentionally changes under a new magic.
