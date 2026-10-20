# AAPL — System Profile

**Asset:** Apple (AAPL CFD) · **TF:** M15  
**Sleeves:** Harvest + Balanced · **engine only (AOS OFF)**  
**Magics:** **26092501** (Harvest) · **26092502** (Balanced)  
**Presets:** `Profiles/Tester/BMRG/AAPL/`  
**Profile date:** 2026-10-12  
**Evidence:** Tester `logs/20261012.log` · deposit **$500** · leverage 1:500 · every tick · ACCOUNT CURRENCY  
**Framework:** `doc/unified_edge_framework.md` · **binding:** [`edge_framework.md`](./edge_framework.md)  
**Docs home:** [`doc/assets/AAPL/`](./README.md)

**Scope:** Research **asset expansion** (equity CFD book). Not a live replace for AUDUSD / EURUSD.  
**Candidate (2026-10-12):** Harvest baseline · magic **26092501** · AOS OFF — see [`candidate_pool.md`](./candidate_pool.md). AIOS optional later; not required for KEEP.

**Do not mix** with root `system_profile.md` (EURUSD) · `doc/assets/AUDUSD/` · EDX / INF live magics.

---

## 0. Evidence hierarchy

| Authority | Source |
| --- | --- |
| **Primary long** | **2025.01.01 → 2026.08.31** · Harvest + Balanced (latest complete long runs) |
| **Primary tip** | **2026.05.01 → 2026.08.31** · both sleeves |
| **Supporting roll** | **2026.01.01 → 2026.08.31** · regime-split diagnostic |
| **Normative scoring** | [`edge_framework.md`](./edge_framework.md) (binds unified maths · expansion vs production ladders) |
| **Not admissible** | Live FT magics · EUR/AUD L2 pins · treating tip-only PnL as attach-ready |

### Cross-window scoreboard (journal PnL)

| Sleeve | Window | Final | Δ | N | WR | E_N (vs designed BWR) | True-leak pass\* |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| Harvest | May→Aug 2026 tip | 520.91 | **+20.91** | 8 | **75.0%** | **+0.69R** | yes |
| Harvest | Jan→Aug 2026 | 508.89 | +8.89 | 22 | 50.0% | +0.13R | **no** |
| Harvest | **2025.01→2026.08** | **568.26** | **+68.26** | **56** | **58.9%** | **+0.33R** | **yes** |
| Balanced | May→Aug 2026 tip | 516.13 | +16.13 | 8 | 62.5% | +0.56R | yes |
| Balanced | Jan→Aug 2026 | 507.13 | +7.13 | 22 | 45.5% | +0.14R | **no** |
| Balanced | **2025.01→2026.08** | **553.13** | **+53.13** | **53** | **50.9%** | **+0.27R** | **yes** |

\*True leak ≈ med open spread / SL ≈ **8.4–9.7 pp** (preset meta Leak 3.5–3.5/3.0 understates Apple CFD cost). Soft “pass_meta” with 3.5 pp Leak overstates Jan→Aug.

---

## 1. System identity

| Field | Value |
| --- | --- |
| Full name | Bollinger Mean-Reversion Grid on Apple M15 |
| Short code | BMRG · AAPL expansion |
| Primary class | **Mean reversion** (statistical deviation fade) |
| Secondary class | Grid / basket — **OFF** (G0 · MaxLevels=1 · MaxEntries=1) |
| Not | Trend-following, breakout, momentum-continuation, scalping |
| Market / TF | **Apple**, M15 · US cash RTH filter |
| Execution | Closed-bar signal (shift 1) → market · fixed **1.0** lot (broker `VOLUME_MIN≈1`) |
| Realisation | **`FIXED_RR_FADE`** (TP/SL; some gap/`OTHER` exits on overnight inventory) |

### Strategy-class statement

On Apple the EA **fades excursions** past ±kσ Bollinger bands back toward the short-horizon mid-band. Same **mean-reversion** class as FX Harvest/Balanced — not a trend system.

It should win when Apple **mean-reverts inside RTH** often enough that:

```
WR > BWR = 1 / (1 + R)
E_N = (R + 1)(WR − BWR) > 0
BM = WR − BWR > 0
```

It loses when price **band-rides** (earnings impulse, trend days, gap-through) into the hard SL — classic meanrev failure mode. Soft or negative calendar months on this asset are read first as **regime mismatch**, not class failure.

---

## 2. Edge profile

### 2.1 Theoretical edge (meanrev · two RR sleeves)

| Concept | Harvest | Balanced | Implication |
| --- | ---: | ---: | --- |
| Class | Meanrev fade | Meanrev fade | Edge = **hit-rate above BWR**, optionally thicker R |
| Geometry | SL **300** / TP **375** | SL **320** / TP **480** | TP > SL always |
| Designed RR / R | **1.25** | **1.50** | |
| BWR | **44.4%** | **40.0%** | Lower BWR = more room for WR shortfall |
| Side of edge | **WR-side** (hit-rate sleeve) | **Mixed WR + R** | Balanced tolerates lower WR if R holds |
| Soft research WR | ≳ 48–50% after true leak (~9 pp) | ≳ 49–50% after true leak (~8–9 pp) | Preset Leak 3.5 pp is too optimistic on Apple |
| AOS | OFF | OFF | Pure engine extract; asset AIOS later |

**Why these RRs on Apple:** Equity CFD ATR (M15 p50 ≈ 100–110 pts) supports SL ≈ 2.8–3.0×ATR. Harvest keeps a modest RR for hit-rate; Balanced lowers BWR further when tip WR is strong but sample is thin. Neither sleeve is trend RR (no asymmetric trail / BE logic).

### 2.2 Structural win path

| Layer | Role on Apple |
| --- | --- |
| Signal | Long ≤ lower BB; short ≥ upper BB on closed M15 · **BBDev 2.5** (deeper extremes than FX 2.2) |
| Regime gates | ATR **50–180** pts · BB-width **0.40–1.50%** (skips dead tape + HV blowouts) |
| Session | US RTH ≈ **14:30–20:00** (verify broker TZ) · **skip Tue** |
| Entry hygiene | MaxSpread **40** · cooldown **3** bars |
| Exit | Fixed TP at designed R or SL at −1 designed SL distance |
| Risk G0 | One event · fixed lot 1.0 · exposure/daily-loss containment |
| Containment | Loss-streak pause (3) · daily loss % · equity halt |

**Structural selectivity note:** On long windows only ~**30–36%** of bars sit inside BB-width max 1.50% (p50 BBw ≈ 2.0%). The width gate is the main throttle — intentional WR protection, not a bug.

### 2.3 Class metric targets (research soft bars)

| Metric | Harvest soft | Balanced soft | Hard worry |
| --- | --- | --- | --- |
| WR | > 44.4% + true Leak (~9 pp) → ≳ **53%** ideal; ≥50% research soft | > 40% + ~9 pp → ≳ **49%** | Persistently ≤ BWR on W20 and full year |
| R (realised) | ≈ 1.25 (RR−R small) | ≈ 1.50 | R ≪ RR without WR compensation |
| BM | > 0; prefer ≥ +5 pp on clean windows | > 0; prefer ≥ +5 pp | BM ≤ 0 |
| E_N | > 0; prefer ≥ +0.10R on primary long | > 0; prefer ≥ +0.10R | ≤ 0 on W20 and calendar year |
| MaxDD (fixed 1 lot / $500) | soft under ~8–10% research | same | Equity-halt territory |
| Soft stress months | WR can dip below BWR | same | Cluster of months << BWR → regime / AIOS later, not auto-kill asset |

### 2.4 Realised edge — primary long (2025.01 → 2026.08)

| Metric | Harvest | Balanced | vs target |
| --- | ---: | ---: | --- |
| n | **56** | **53** | Usable Stage-0 |
| WR | **58.9%** | **50.9%** | Both > BWR; Harvest clearer WR-side |
| Designed BWR | 44.4% | 40.0% | |
| BM | **+14.5 pp** | **+10.9 pp** | Strong gross |
| E_N (designed R) | **+0.33R** | **+0.27R** | Clear of +0.10R soft bar |
| avgR / trade | +0.43 | +0.34 | Positive expectancy |
| exp $ / trade | +1.28 | +1.08 | Fixed 1-lot scale |
| R_real (avgWin/|avgLoss|) | ~1.37 | ~1.57 | Near designed RR (gap/`OTHER` noise) |
| PnL (tester final) | **+$68.26** (+13.7%) | **+$53.13** (+10.6%) | Harvest ahead on long |
| True leak | ~9.0 pp | ~8.4 pp | Must use in pass/fail |
| MaxDD (path approx) | ~3.9% | ~5.3% | Contained |
| PF (approx) | ~1.96 | ~1.63 | |

**Leak / EF:** journal has no full deal-cost vector. Treat BM/E_N as **gross of spread already in fills**; formal EF = BM − Leak pending deal export. True spread/SL already shows Jan→Aug 2026 fails a honest leak bar on both sleeves.

### 2.5 Regime / transfer caveat

Apple is **not** FX microstructure. USD impulse, earnings, and overnight gaps produce meanrev failure clusters (notably **2026-01…04** and several soft 2025 months). Tip **May→Aug 2026** recovers hard on both sleeves — same pattern as other expansion assets: **hostile regime ≠ dead class**. Do not reject AAPL from the expansion list on Jan→Aug alone.

---

## 3. Trade profile

Primary evidence: **long window** trades (Harvest n=56 · Balanced n=53). Tip and Jan→Aug cited where side/regime stories differ.

### 3.1 Winners

| | Harvest long | Balanced long |
| --- | --- | --- |
| Share | 33/56 (**58.9%**) | 27/53 (**50.9%**) |
| Typical exit | TP at +RR (27 TP of 56) | TP at +RR (19 TP of 53) |
| Med hold (wins) | ~**42.5h** | ~**48.7h** |
| Character | Fade completes; often overnight | Same; slightly longer holds |

- Meanrev needs **time** — winners hold longer than losers on both sleeves.  
- **Overnight inventory common** (~73–77% of trades hold ≥12h) — equity open-risk is part of the fingerprint, not a scalp book.  
- Best DOW (long): **Fri** and **Wed** carry most expectancy; **Thu** is the weak pocket on both sleeves.

### 3.2 Losers

| | Harvest long | Balanced long |
| --- | --- | --- |
| Share | 23/56 (41.1%) | 26/53 (49.1%) |
| Typical exit | SL / adverse `OTHER` (gap past SL) | Same |
| Med hold (losses) | ~**20.5h** | ~**21.8h** |
| Character | Continuation / impulse hits stop sooner | Same |

- Faster resolution than winners — trend/impulse days stop out.  
- Max loss streak Harvest **5** · Balanced **8** (Balanced long can cluster — containment pause matters).  
- Soft hours: entry **18** UTC weak on both; **14** (session open) is high-n mixed; **17** strong when it fires.

### 3.3 Exit mix (long window)

| Exit | Harvest | Balanced |
| --- | ---: | ---: |
| Take profit | 27 (48%) | 19 (36%) |
| Stop loss | 17 (30%) | 19 (36%) |
| OTHER (gap/slip/partial path) | 12 (21%) | 15 (28%) |

→ Realisation remains **`FIXED_RR_FADE`**, with material overnight gap noise (`OTHER`). Not MID-exit logic.

### 3.4 Side balance

| Side | Harvest long | Balanced long | Jan→Aug 2026 note |
| --- | --- | --- | --- |
| BUY | n=26 WR **61.5%** net **+28.9** | n=25 WR **56.0%** net **+28.5** | Harvest BUY WR **40%** · Balanced BUY **30%** — H1 wound |
| SELL | n=30 WR **56.7%** net **+42.7** | n=28 WR **46.4%** net **+28.8** | Both SELLs hold up better in 2026 H1 |

**Read:** Over the full 20m both sides contribute. **2026 YTD drag is buy-side regime**, not “sell-only engine.” Optional later hygiene: buy-caution in hostile regimes (AIOS), not a preset flip yet.

### 3.5 Weekday (entry) — Tue filtered · long window

| DOW | Harvest n/WR/E_N | Balanced n/WR/E_N |
| --- | --- | --- |
| Mon | 8 / 50% / +0.13R | 8 / 38% / −0.06R |
| Tue | 0 / — / filtered | 0 / — / filtered |
| Wed | 19 / **68%** / **+0.54R** | 19 / **63%** / **+0.58R** |
| Thu | 19 / 42% / −0.05R | 17 / **29%** / **−0.26R** |
| Fri | 10 / **80%** / **+0.80R** | 9 / **78%** / **+0.94R** |

Tue skip is live (n=0). Thu is the structural soft pocket on Apple — watchlist for AIOS, not an immediate preset change.

### 3.6 Streaks (long)

| | Harvest | Balanced |
| --- | ---: | ---: |
| Max win streak | 6 | 4 |
| Max loss streak | 5 | 8 |

---

## 4. Rolling windows

### 4.1 Calendar months — Harvest long (2025.01→2026.08)

| Month | n | WR | E_N | Month | n | WR | E_N |
| --- | ---: | ---: | ---: | --- | ---: | ---: | ---: |
| 2025-01 | 2 | 50% | +0.13R | 2026-01 | 4 | 25% | −0.44R |
| 2025-02 | 3 | 33% | −0.25R | 2026-02 | 3 | 33% | −0.25R |
| 2025-03 | 2 | 100% | +1.25R | 2026-03 | 4 | 50% | +0.13R |
| 2025-04 | 1 | 100% | +1.25R | 2026-04 | 3 | 33% | −0.25R |
| 2025-05 | 3 | 67% | +0.50R | 2026-05 | 2 | 50% | +0.13R |
| 2025-06 | 3 | 100% | +1.25R | 2026-06 | 1 | 100% | +1.25R |
| 2025-07 | 4 | 75% | +0.69R | 2026-07 | 1 | 100% | +1.25R |
| 2025-08 | 2 | 50% | +0.13R | 2026-08 | 4 | 75% | +0.69R |
| 2025-09 | 2 | 50% | +0.13R | | | | |
| 2025-10 | 1 | 0% | −1.00R | | | | |
| 2025-11 | 6 | 83% | +0.88R | | | | |
| 2025-12 | 5 | 40% | −0.10R | | | | |

**Year split Harvest:** 2025 n=34 WR **64.7%** net **+$61.7** · 2026 n=22 WR **50.0%** net **+$9.9**.

### 4.2 Calendar months — Balanced long (same span)

Hostile clusters align with Harvest (2025-05/08/10/12, 2026-01/02/04/06). Strong pockets: 2025-03/04/06/07/11, 2026-07/08.

**Year split Balanced:** 2025 n=32 WR **56.2%** net **+$53.7** · 2026 n=21 WR **42.9%** net **+$3.5**.

### 4.3 Rolling trade windows (expectancy)

#### Harvest long

| Window | Path WR (avg) | Path E_N (avg) | Min E_N | Read |
| --- | ---: | ---: | ---: | --- |
| W10 | ~58% | **+0.30R** | −0.55R | Soft pocket into 2026 H1 |
| W15 | ~57% | **+0.28R** | −0.25R | Recovers into tip |
| W20 | ~56% | **+0.26R** | −0.21R | No sustained collapse |

#### Balanced long

| Window | Path WR (avg) | Path E_N (avg) | Min E_N | Read |
| --- | ---: | ---: | ---: | --- |
| W10 | ~49% | **+0.23R** | −0.75R | Deeper 2026 H1 dip |
| W15 | ~48% | **+0.21R** | −0.33R | Tip repairs |
| W20 | ~47% | **+0.18R** | −0.25R | Avg still > 0 |

**Tip-only (May→Aug):** both sleeves too thin for W20 (n=8); treat as confirmation, not primary.

**Jan→Aug 2026:** W10 starts ~30% WR / negative E_N and climbs to ~50–70% by August — textbook regime recovery path.

### 4.4 Frequency

| Metric | Harvest long | Balanced long | Tip (either) |
| --- | ---: | ---: | ---: |
| Span | ~20 months | ~20 months | ~4 months |
| Closed trades | 56 | 53 | 8 |
| Trades / 30d | ~2.8 | ~2.7 | ~2 |
| Selectivity | High (BB-width + RTH + skip Tue) | Same | Same |

Low frequency is expected: equity RTH + tight BB-width gate. Not an FX M5 Harvest rate.

---

## 5. Performance

### 5.1 Primary long (2025.01.01 → 2026.08.31)

| Setting | Harvest | Balanced |
| --- | --- | --- |
| Symbol / TF | Apple M15 | Apple M15 |
| Magic | 26092501 | 26092502 |
| Geometry | SL300 / TP375 · RR1.25 | SL320 / TP480 · RR1.50 |
| AOS | Off | Off |
| Deposit | 500 | 500 |
| Final balance | **568.26** | **553.13** |
| Net PnL | **+68.26** (+13.7%) | **+53.13** (+10.6%) |
| MaxDD (path) | ~3.9% | ~5.3% |
| Containment | No equity halt observed | No equity halt; longer loss streak |

### 5.2 Tip & diagnostic windows

| Window | Harvest | Balanced | Read |
| --- | ---: | ---: | --- |
| May→Aug 2026 | **+20.91** · WR 75% · n=8 | +16.13 · WR 62.5% · n=8 | Tip edge live; Harvest ahead |
| Jan→Aug 2026 | +8.89 · WR 50% · n=22 | +7.13 · WR 45.5% · n=22 | Soft; fails true-leak bar |

**Interpretation:** Engine has a multi-month meanrev edge on Apple when regime cooperates (2025 + tip 2026). 2026 H1 is a **regime tax**, especially on buys. Expansion keep; not attach-ready; AIOS candidate later for skip/buy-caution.

### 5.3 Sleeve comparison (expansion lens)

| Question | Answer |
| --- | --- |
| Which sleeve for hit-rate research? | **Harvest** — higher WR, higher long PnL, cleaner tip |
| Which for RR / BWR stress? | **Balanced** — still E_N>0 on long; thicker R when fades complete |
| Prefer for next AIOS tape? | Start with **Harvest** (more winners, clearer WR-side label) |
| Replace live FX? | **No** |

---

## 6. Key metrics (scorecard snapshot)

### Harvest · 2025.01→2026.08 · magic 26092501

| Metric | Value |
| --- | ---: |
| RR / R_real / RR−R | 1.25 / ~1.37 / small (noise) |
| BWR / WR / BM | 44.4% / **58.9%** / **+14.5 pp** |
| E_N | **+0.33R** |
| n | 56 |
| PF (approx) | ~1.96 |
| expR / trade | +0.43 |
| True Leak | ~9.0 pp |
| MaxDD | ~3.9% |
| Side diagnosis | WR-side meanrev · both sides on long |
| regime_filtered | **true** (RTH + skip Tue + ATR/BBw) |
| Live boundary | **Research only** · expansion queue |

### Balanced · 2025.01→2026.08 · magic 26092502

| Metric | Value |
| --- | ---: |
| RR / R_real / RR−R | 1.50 / ~1.57 / small |
| BWR / WR / BM | 40.0% / **50.9%** / **+10.9 pp** |
| E_N | **+0.27R** |
| n | 53 |
| PF (approx) | ~1.63 |
| expR / trade | +0.34 |
| True Leak | ~8.4 pp |
| MaxDD | ~5.3% |
| Side diagnosis | Mixed WR+R · BUY hurts in 2026 H1 |
| regime_filtered | **true** |
| Live boundary | **Research only** · expansion queue |

---

## 7. Behavioural fingerprint (AAPL)

1. Class: **mean-rev entry · FIXED_RR exit** (same family as FX Harvest/Balanced).  
2. Hit-rate sleeve (**Harvest**) is the stronger Apple print on tip and long.  
3. Inventory is **overnight-heavy** — gap/`OTHER` exits are part of the equity CFD fingerprint.  
4. BB-width gate keeps frequency low (~3 trades/month); ATR gate rarely binds.  
5. Structural soft pockets: **Thu**, hour **18**, **2026 H1 buys**.  
6. Fri/Wed and tip May→Aug are the cleanest expectancy pockets.  
7. AOS OFF — fingerprint is pure engine; do not evaluate EUR/AUD L2 pins on this blotter.  
8. True Leak ~9 pp must replace preset 3.5 pp in any formal pass/fail.

---

## 8. Locked geometry (reference)

### Shared

| Parameter | Value |
| --- | --- |
| InpBBPeriod / InpBBDev | 20 / **2.5** |
| InpMaxLevels / InpMaxEntries | 1 / 1 |
| InpLotMode / InpLot | Fixed / **1.0** |
| InpMaxSpread / CooldownBars | **40** / **3** |
| Session | **14:30–20:00** · skip Tue |
| ATR regime | **50–180** pts ON |
| BB-width regime | **0.40–1.50%** ON |
| InpAOS_Enable | **false** |

### Harvest · magic 26092501

| Parameter | Value |
| --- | --- |
| InpSL_Points / InpTP_Points | **300 / 375** |
| Designed RR / BWR / meta Leak | 1.25 / 44.4% / 3.5 pp |

### Balanced · magic 26092502

| Parameter | Value |
| --- | --- |
| InpSL_Points / InpTP_Points | **320 / 480** |
| Designed RR / BWR / meta Leak | 1.50 / 40.0% / 3.0 pp |

Presets: `Profiles/Tester/BMRG/AAPL/BMRG-M15-AAPL-6M-Harvest_RR1.25.set` · `…Balanced_RR1.5.set`.

---

## 9. Recommended use

| Do | Don’t |
| --- | --- |
| Keep Apple on the **expansion asset list** | Treat as live AUDUSD/EURUSD replace |
| Prefer **Harvest** as primary research sleeve | Claim Robust EF from journal WR alone |
| Score pass/fail with **true Leak ~9 pp** | Use preset Leak 3.5 pp as production bar |
| Read 2026 H1 / Thu / buy softness as **regime** | Hard-reject the asset on Jan→Aug alone |
| Next: deal export → Leak/EF/MaxDD Stage-1; then asset AIOS | Pin EUR/AUD L2 models onto Apple |
| Optional probes: Thu caution · buy-caution in hostile ATR | Flip to trend geometry |

---

## 10. One-line thesis

**Apple M15 BMRG is a RTH-filtered G0 Bollinger mean-reversion fade (Harvest RR1.25 + Balanced RR1.5); on 2025.01→2026.08 both sleeves realise positive E_N (Harvest +0.33R / +$68 · Balanced +0.27R / +$53) with tip confirmation — suitable for expansion research, not live attach, with 2026 H1 softness read as regime mismatch until deal-scored EF and an Apple-specific AIOS.**
