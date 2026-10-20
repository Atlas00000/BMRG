# EURUSD_AOS_BASELINE_v1

**Task:** EURUSD-AOS-P0-T01  
**Frozen:** 2026-10-18  
**Engine:** P2 light-selective · magic **26101817** · AOS **OFF**  
**Preset:** `BMRG-M15-EURUSD-6M-P2_light_selective_chart.set`  
**Evidence:** Tester `logs/20261018.log` · `system_profile.md` · `blotter/archive/EURUSD-M15-P2/`  
**Deposit:** $500 · every tick · ACCOUNT CURRENCY  

This packet is the **OS compare baseline**. OS trials report Δ vs these rows. Do not mutate geometry to “beat” this file — change overlay only.

---

## Geometry lock

| Parameter | Value |
| --- | --- |
| SL / TP | 300 / 375 (RR 1.25 · BWR 44.4%) |
| BB | 20 / **2.3** |
| Cooldown | **3** |
| Session | 12:00–20:00 · skip Tue |
| ATR | max **74** ON · BB-width OFF |
| Lot | 0.01 (research path) |
| AOS | OFF |

---

## Window scoreboard (journal-gross · Leak prior 3.0 pp)

| Window | n | WR | E_N | BM | EF_prior | Final Δ | Role |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| **May→Oct 2026 tip** | **45** | **46.7%** | **+0.050R** | +2.2 pp | **−0.7 pp** | **+$7.14** | **OS default compare** |
| Jan→Oct 2026 YTD | 72 | 48.6% | +0.094R | +4.2 pp | +1.2 pp | +$20.91 | Support / L3 diagnostic |

**Leak on this freeze:**

| Source | Leak | Tip EF | Authority |
| --- | ---: | ---: | --- |
| `prior` (design 20pt RT) | 3.0 pp | −0.7 pp | Footnote / preset meta (pessimistic vs journal) |
| `journal_2x_entry_spread_median` | **1.19 pp** | **+1.04 pp** | **Interim OS** (`EURUSD-AOS-P1` / P0-T03) |
| `measured` | — | — | OPEN (deal export · **swap mandatory** · nights≈76%) |

OS trials: report ΔE_N vs tip row; footnote EF under **journal proxy** until deals+swap land. Do not promote P7 on proxy alone.

---

## Tip fingerprint (OS must not destroy)

| Slice | Tip value |
| --- | --- |
| BUY / SELL WR | **39.1%** / **54.5%** |
| Best DOW | Mon / Fri WR 50% |
| Soft DOW | Thu WR **37.5%** |
| Soft hours | H13 WR 37.5% · H19 WR 33.3% |
| Protect hours | H12 / H14 WR 50% |
| Best month | Jul WR 57.1% E_N +0.29R |
| Soft months | May/Jun ≈BWR · Aug soft · Feb (YTD) WR 30% |
| Max W / L streak | 3 / 4 |
| Hold≥12h (wins) | ~**86%** (overnight-heavy) |

---

## Sleeve ladder (context only — not OS identity)

| Sleeve | Magic | Note |
| --- | ---: | --- |
| P0 | 26101815 | WR &lt; BWR — superseded |
| P1 | 26101816 | starved — reject |
| **P2** | **26101817** | **This baseline** |

---

## Expansion posture

| Ladder | Verdict |
| --- | --- |
| Expansion (`edge_framework.md`) | **EXPANSION_KEEP** (costs_fragile / WATCH footnote until measured Leak) |
| Production G0–G5 | **NOT PRODUCTION-WORTHY** |

Bump to `EURUSD_AOS_BASELINE_v2` only when: measured Leak replaces prior on the same tip window, or geometry intentionally changes under a new magic.
