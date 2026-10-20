# UK100_M5_AOS_BASELINE_v1

**Task:** UK100-M5-AOS-P0-T01  
**Frozen:** 2026-10-20  
**Engine:** Balanced P0 M5 · magic **26101905** · AOS **OFF**  
**Preset:** `BMRG-M5-UK100-6M-P0_balanced_chart.set`  
**Evidence:** Tester `logs/20261020.log` · `system_profile_M5.md` · `blotter/archive/UK100-M5-P0-CHART/`  
**Deposit:** $500 · every tick · ACCOUNT CURRENCY  

This packet is the **OS compare baseline** for UK100 **M5**. OS trials report Δ vs these rows. Do not mutate geometry to “beat” this file — change overlay only. Do **not** compare against M15 `UK100_AOS_BASELINE_v1`.

---

## Geometry lock

| Parameter | Value |
| --- | --- |
| TF | **M5** |
| SL / TP | **1800 / 2250** (RR 1.25 · BWR 44.4%) |
| BB | 20 / 2.2 |
| Session | 08:00–17:00 · skip Tue |
| ATR | max **869** ON (≈p75) · BB-width OFF |
| MaxSpread / cooldown | 200 / **3** bars |
| Lot | 0.1 · G0 MaxLevels=1 · MaxEntries=1 |
| AOS | OFF |

---

## Window scoreboard (journal-gross · Leak prior 4.0 pp)

| Window | n | WR | E_N | BM | EF_prior | Final Δ | Role |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| **May→Aug 2026 tip** | **116** | **52.6%** | **+0.183R** | +8.1 pp | **+4.1 pp** | **+$51.16** | **OS default compare** |
| Jan→Aug 2026 long | 235 | 48.9% | +0.101R | +4.5 pp | +0.5 pp | +$57.25 | Path / MaxDD context |
| Jan→Apr prior (inside long) | ~119 | soft | ≤0 months | — | — | — | L3 diagnostic (regime tax) |

**Leak on this freeze (updated P1 journal proxy):**

| Source | Leak | Tip EF | Authority |
| --- | ---: | ---: | --- |
| `prior` (design · c_R≈160/1800) | **4.0 pp** | **+4.1 pp** | P0 footnote |
| `journal_2x_entry_spread_median` | **5.93 pp** | **+2.22 pp** | **Interim OS** (`UK100-M5-AOS-P1`) |
| `measured` | — | — | OPEN (deal export) |

OS trials: report ΔE_N vs tip row; footnote EF under journal proxy until deals land.

**MaxDD tip path proxy:** ~**2.5%** (R-calibrated from tip Δ$).

---

## Tip fingerprint (OS must not destroy)

| Slice | Tip value | OS note |
| --- | --- | --- |
| BUY / SELL WR | **54.8%** / 50.0% | Tip **buy-led** — protect BUY |
| Best DOW | Wed **65.4%** | Protect — high FP skip = REJECT |
| Soft DOW | Mon **43.8%** | L2det seed |
| Soft hour | H12–13 **40.4%** | L2det seed |
| Strong hours | H08–11 **~66.7%** | Protect — do **not** import M15 H08 skip |
| Soft month | Aug **42.1%** E_N −0.053R | Stress-month seed |
| Strong months | May–Jul WR ≥53.8% | Protect |
| Max W / L streak | 5 / 5 | L3 align with engine pause@3 |
| Hold med win / lose | 1.26h / 0.66h | Losers faster — L8 candidate |
| Hold ≥12h | ~2% | Intraday book |

---

## Expansion posture

| Ladder | Verdict |
| --- | --- |
| Expansion (`edge_framework.md`) | **EXPANSION_KEEP** |
| Production G0–G5 | **NOT PRODUCTION-WORTHY** |
| Live replace FX / M15 UK OS | **No** |

Bump to `UK100_M5_AOS_BASELINE_v2` only when: measured Leak replaces prior on the same tip window, or geometry intentionally changes under a new magic.
