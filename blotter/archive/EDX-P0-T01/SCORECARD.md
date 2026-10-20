# EDX-P0-T01 — SCORECARD (AUDUSD baseline LOCKED)

**Scored:** 2026-10-07T16:25+01:00  
**Source:** Tester `logs/20261007.log` run mag **8230101**  
**Preset:** `Profiles/Tester/BMRG/AUDUSD/EDX-P0-T01_baseline_G0_AUDUSD-M5_MayAug.set`  
**Window:** 2026.05.01 → 2026.08.31 · AUDUSD M5 · every tick · ACCOUNT CURRENCY · deposit 400  
**Inbox:** empty (journal-scored; deal export still preferred for measured Leak)

## Identity — PASS

| Field | Expected | Observed |
| --- | --- | --- |
| Magic | 8230101 | **8230101** |
| SL / TP | 300 / 300 | **300 / 300** |
| BBDev | 2.2 | 2.2 |
| Session | 12–20 · skip Tue | (preset) |
| AOS | off | aos=0 |
| G0 | MaxLevels/Entries=1 | yes |

---

## Full health vector (reference for all later EDX tasks)

| Metric | Value | Notes |
| --- | ---: | --- |
| n | **58** | Insufficient (&lt;100) for firm conclusions; expansion OK |
| WR | **62.07%** | |
| AW | **1.000R** | FIXED_RR TP |
| AL | **1.000R** | FIXED_RR SL |
| R | **1.000** | |
| RR | **1.000** | designed |
| RR−R | **0.000** | no payoff compression on exits |
| BWR | **50.00%** | |
| BM | **+12.07 pp** | |
| FMI | **0.241** | |
| med spread | 15 pts | from log quotes |
| c_R | **0.150** | proxy `3×spread/SL` — `costs_defaulted` |
| Leak | **7.50 pp** | proxy; replace with deal costs in P05 |
| EF | **+4.57 pp** | BM − Leak |
| M (Wilson) | **±12.12 pp** | |
| M (normal) | ±12.49 pp | |
| E_N | **+0.241R** | |
| PF | **1.636** | |
| Final / PnL | **444.39 / +44.39** | |
| MaxDD | *pending deal/equity path export* | |
| f_declared | 0.5% | |
| f_realised | ~min-lot floor on $400 | |

### Production-gate zone (Stage 1)

| | |
| --- | --- |
| Zone | **Fragile** (`0 < EF ≤ M`: 4.57 ≤ 12.12) |
| Tier | **Insufficient** (n&lt;100) — cannot claim Robust / PRODUCTION-WORTHY |
| Expansion ladder | **EXPANSION_KEEP** (E_N>0 · WR>BWR · identity OK) |

### Side diagnosis (hypothesis lock for AUDUSD G0)

| Claim | Result |
| --- | --- |
| Working hypothesis: AL too large / **R-side** | **REJECTED** |
| Evidence | R = RR = 1.0 · AW = AL = 1.0R · RR−R = 0 |
| Locked side | **WR-side** — edge is hit-rate margin above 50% BWR |

Do **not** default to tightening SL to “fix AL.” Prefer filters / session hygiene / regime (P1/P3) and only run payoff neighborhood for pool diversity.

---

## Rolling / lifecycle (P0-T02 preview from same run)

### Monthly

| Month | n | WR | E_N |
| --- | ---: | ---: | ---: |
| 2026-05 | 17 | 70.6% | +0.412R |
| 2026-06 | 13 | 53.8% | +0.077R |
| 2026-07 | 19 | 63.2% | +0.263R |
| 2026-08 | 9 | 55.6% | +0.111R |

All months E_N > 0.

### W20 (step 10)

| Trades | WR | E_N |
| --- | ---: | ---: |
| [0:20] | 65% | +0.30R |
| [10:30] | 65% | +0.30R |
| [20:40] | 65% | +0.30R |
| [30:50] | 60% | +0.20R |

Lifecycle (expansion W20): **Stable / Expanding** bias — no Below-frontier.  
ΔD (EF): not computed across non-overlapping W250 (n too small); treat ΔD as N/A until longer sample.

### Streaks

| | Value |
| --- | ---: |
| Max loss streak | 3 |
| Expected worst ≈ | 4.2 |
| DEPENDENCE (1.5×) | ~6.3 — **no flag** |

---

## Accept / reject

| Criterion | Result |
| --- | --- |
| Identity / preset | **PASS** |
| Full vector filled | **PASS** (MaxDD pending export) |
| Zone named | **Fragile** + Insufficient n |
| Side named | **WR-side** · R-side claim **REJECTED** |
| Task | **ACCEPT — baseline LOCKED** |

**Baseline values later tasks must beat (primary):**

| Metric | P0-T01 |
| --- | ---: |
| E_N | +0.241R |
| EF (proxy) | +4.57 pp |
| WR | 62.07% |
| BM | +12.07 pp |
| n | 58 |
| PnL | +44.39 |

Regression rule: WR↑ with E_N↓ or EF↓ = reject.
