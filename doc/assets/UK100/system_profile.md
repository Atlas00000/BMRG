# UK100 M15 — System Profile

**Asset:** UK100 (FTSE 100 CFD) · **TF:** M15  
**Sleeve:** Balanced P0 · **engine only (AOS OFF)**  
**Magic:** **26101201**  
**Preset:** `Profiles/Tester/BMRG/UK100/BMRG-M15-UK100-6M-P0_balanced_chart.set`  
**Profile date:** 2026-10-12  
**Evidence:** Tester `logs/20261012.log` · deposit **$500** · leverage 1:500 · every tick · ACCOUNT CURRENCY  
**Framework:** `doc/unified_edge_framework.md` · **binding:** [`edge_framework.md`](./edge_framework.md) · chart card `doc/BMRG_M15_UK100_6M_chart_preset.md`  
**Docs home:** [`doc/assets/UK100/`](./README.md)  
**Review:** `blotter/archive/UK100-P0-CHART/REVIEW.md`  
**Sibling M5:** [`system_profile_M5.md`](./system_profile_M5.md) (magic **26101905**)

**Scope:** Research **asset expansion** (index CFD book). Not a live replace for AUDUSD / EURUSD.  
**Candidate posture (2026-10-12):** Balanced baseline · magic **26101201** · AOS OFF — EXPANSION_KEEP. Own AIOS planned in [`aios_roadmap.md`](./aios_roadmap.md); not required for keep.

**Do not mix** with root `system_profile.md` (EURUSD) · `doc/assets/AUDUSD/` · `doc/assets/AAPL/` · EDX / INF live magics.

---

## 0. Evidence hierarchy

| Authority | Source |
| --- | --- |
| **Primary tip** | **2026.05.01 → 2026.08.31** · dedicated run · final **517.14** · n=51 |
| **Supporting prior** | **2026.01.01 → 2026.04.30** · dedicated · final **504.48** · n=75 |
| **Composite hist tip** | Requested 2024.01→2026.08 · **effective hist from 2025.12.17** · final **510.97** · n=131 |
| **Design prior (not blotter)** | Ouroboros M15* probe · n≈74 · WR 54.1% · EF≈+6.7pp |
| **Normative scoring** | `doc/unified_edge_framework.md` |
| **Not admissible** | Live FT magics · EUR/AUD L2 pins · treating truncated “2024” as multi-year · Oct FRAGILE tip as admission |

### Cross-window scoreboard (journal · FIXED_RR design R=1.25)

| Window | Final | Δ vs $500 | N | WR | BM | E_N† | EF† (Leak prior 2.9pp) |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| **May→Aug 2026 tip** | **517.14** | **+17.14** | **51** | **49.0%** | **+4.6 pp** | **+0.103R** | **+1.7 pp** |
| Jan→Apr 2026 prior | 504.48 | +4.48 | 75 | 45.3% | +0.9 pp | +0.020R | −2.0 pp |
| Dec2025→Aug2026 hist | 510.97 | +10.97 | 131 | 45.8% | +1.4 pp | +0.031R | −1.5 pp |
| Design probe (M15*) | — | — | ~74 | 54.1% | +9.6 pp | +0.215R | +6.7 pp |

† Gross of designed R; Leak is **prior** (c_R≈160/2500 → Leak≈2.9 pp), not deal-exported. Replace before Stage-1 production gate.

---

## 1. System identity

| Field | Value |
| --- | --- |
| Full name | Bollinger Mean-Reversion Grid on UK100 M15 |
| Short code | BMRG · UK100 expansion |
| Primary class | **Mean reversion** (statistical deviation fade) |
| Secondary class | Grid / basket — **OFF** (G0 · MaxLevels=1 · MaxEntries=1) |
| Not | Trend-following, breakout, momentum-continuation, scalping theatre |
| Market / TF | **UK100**, M15 · London cash sleeve |
| Execution | Closed-bar signal (shift 1) → market · lot **0.1** (broker `VOLUME_MIN`) |
| Realisation | **`FIXED_RR_FADE`** (TP/SL; rare EOT on window end) |
| Regime posture | **`regime_filtered=true`** (session + skip Tue + ATR max ≈ p75) |

### Strategy-class statement

On UK100 the EA **fades excursions** past ±kσ Bollinger bands back toward the short-horizon mid-band. Same **mean-reversion** class as FX Harvest/Balanced and AAPL — **not** a trend system.

It should win when FTSE **mean-reverts inside the London session** often enough that:

```
WR > BWR = 1 / (1 + R)
E_N = WR × (R + 1) − 1 > 0
BM = WR − BWR > 0
EF = BM − Leak > 0   (after measured costs)
```

With designed **RR = 1.25** → **R ≈ 1.25** → **BWR = 44.4%**. Soft research targets after Leak prior (~2.9 pp): WR ≳ 48–52%, BM ≥ +3–5 pp, E_N ≥ +0.05R on the home tip; prefer EF > 0.

It loses when price **band-rides** (GBP/global risk impulse, trend days, high-vol FRAGILE cells) into the hard SL — classic meanrev failure. Soft or negative calendar months are read first as **regime mismatch**, not class failure.

---

## 2. Edge profile

### 2.1 Theoretical edge (meanrev · Balanced RR=1.25)

| Concept | Designed | Implication |
| --- | ---: | --- |
| Class | Meanrev fade | Edge = **hit-rate above BWR**, with modest R thickness |
| Geometry | SL **2500** / TP **3125** pts | TP > SL always |
| Designed RR / R | **1.25** | Not Harvest RR=1.0 · not lottery RR≥3 |
| BWR | **44.4%** | Lower than Harvest 50% — more WR room |
| Side of edge | **Mixed WR + R** | WR-side primary; R=1.25 lifts E_N when WR clears BWR |
| Leak prior | ~**2.9 pp** (c_R≈160 / (R+1)) | Spread≈140 · RT cost prior≈160 pts |
| Soft research WR | ≳ **48–52%** after Leak prior | Ideal clears probe-like 54% |
| AOS | **OFF** | Pure engine extract; UK100 AIOS later |

**Why RR=1.25 on UK100 (not Harvest 1.0):** User / chart intent = mix functional WR **and** returns. Harvest would raise BWR to 50% and thin E_N for the same WR. Growth RR=1.50 remains an alt (probe EF similar) but is not the locked P0 sleeve.

**Why SL=2500 (~2.1× M15 ATR p50≈1189):** Structural 1R that clears spread Leak. Thin SL≈1200 raises Leak (~6 pp) and taxes EF — rejected in design card.

**Why ATR max 1470 (≈p75) ON:** Declared regime filter (Gate G3). Probe: filtered EF +6.7 pp vs unfiltered +1.3 pp at similar geometry. Cuts high-vol **FRAGILE** (esp. Oct tip) without BB-width starvation.

### 2.2 Structural win path

| Layer | Role on UK100 |
| --- | --- |
| Signal | Long ≤ lower BB; short ≥ upper BB on closed M15 · **BBDev 2.2** |
| Regime gates | ATR **max 1470** ON · BB-width **OFF** |
| Session | London cash **08:00–17:00** server · **skip Tue** |
| Entry hygiene | MaxSpread **200** · cooldown **2** bars |
| Exit | Fixed TP **+1.25R** or SL **−1R** (distance in points) |
| Risk G0 | One event · lot 0.1 · exposure / daily-loss containment |
| Containment | Loss-streak pause (3) · fail pause · daily loss % · equity halt |

### 2.3 Class metric targets (research soft bars)

| Metric | Soft target (expansion) | Hard worry |
| --- | --- | --- |
| WR | > 44.4% (BWR); prefer ≥ **48–52%** after Leak prior | Persistently ≤ BWR on tip + W20 |
| R (realised) | ≈ 1.25 (RR−R small) | R ≪ RR without WR compensation |
| BM | > 0; prefer ≥ **+4 pp** on home tip | BM ≤ 0 on primary tip |
| E_N | > 0; prefer ≥ **+0.05R** on tip | ≤ 0 on tip and W20 |
| EF | > 0 after measured Leak | Persistently ≤ 0 with honest costs |
| Soft stress months | WR can dip below BWR (Jul-like) | Cluster of months ≪ BWR → regime / AIOS, not auto-kill |
| MaxDD (0.1 lot / $500) | soft under ~8–10% research | Equity-halt territory |

### 2.4 Realised edge — primary tip (2026.05 → 2026.08)

| Metric | Value | vs target |
| --- | ---: | --- |
| n | **51** | Usable Stage-0 |
| WR | **49.0%** | Clears BWR 44.4%; below design probe 54.1% |
| Designed R / BWR | 1.25 / 44.4% | On-thesis geometry |
| BM | **+4.6 pp** | Soft bar cleared |
| E_N | **+0.103R** | Clears +0.05R soft bar |
| EF (Leak prior 2.9 pp) | **+1.7 pp** | Thin but > 0 |
| avgR / trade | +0.10R | Positive expectancy |
| PnL (tester final) | **+$17.14** (+3.4%) | Equity confirms E_N direction |
| PF (approx · FIXED_RR) | ~1.20 | Modest |
| Approx MaxDD (path proxy) | ~5% on longer hist | Contained |

**Probe vs Tester gap:** Design M15* probe overstated WR (~54% → 49%). Still same class and geometry; treat probe as **prior**, blotter as **authority**.

### 2.5 Regime / transfer caveat

Ouroboros H1 meanrev map (last tip): **May–Sep MATCH** (Aug strongest MATCH%≈79%) · **Oct FRAGILE**. Tester soft pockets **Feb** (prior) and **Jul** (inside MATCH tag) are **local regime / impulse taxes**, not proof the fade class is wrong. Do not reject UK100 from the expansion list on prior or Jul alone. Do not claim cross-regime robustness while ATR max stays ON.

Broker history begins **2025.12.17** — any “from 2024” tester request is truncated; do not score as multi-year robustness.

---

## 3. Trade profile

Primary evidence: **dedicated tip** May→Aug (n=51). Prior and hist composite cited where side/regime stories differ.

### 3.1 Winners (tip · n=25 · 49.0%)

| | Tip May→Aug |
| --- | --- |
| Share | 25/51 (**49.0%**) |
| Typical exit | TP at **+1.25R** |
| Med hold (wins) | ~**1.6h** |
| Character | Intraday fade completes inside London sleeve |

- Meanrev still needs **some** time vs losers, but UK100 holds are **short** vs FX/AAPL overnight books.  
- Overnight inventory rare on tip (**~6%** hold ≥12h) — index cash fingerprint, not equity gap book.  
- Best DOW (tip): **Wed** (WR **81.8%**, E_N **+0.84R**, n=11).  
- Best hours (tip, n≥3): **H14** (WR 66.7%, E_N +0.50R) · mid-morning H10–11 strong but thin.

### 3.2 Losers (tip · n=26 · 51.0%)

| | Tip May→Aug |
| --- | --- |
| Share | 26/51 (51.0%) |
| Typical exit | SL at **−1R** |
| Med hold (losses) | ~**1.4h** |
| Character | Continuation / impulse hits stop slightly sooner |

- Soft DOW (tip): **Thu** (WR 30.8%, E_N −0.31R) · **Mon** soft (40%).  
- Soft hours: session open **H08** (WR 30.8%, n=13) — largest subsample below BWR.  
- Max loss streak tip **6** (above containment pause-3 → pauses fire; expected under stress).  
- **Jul** is the hostile calendar pocket (WR 28.6%, n=7) inside a MATCH-tagged month.

### 3.3 Exit mix (tip)

| Exit | Count | Share |
| --- | ---: | ---: |
| Take profit | 25 | 49.0% |
| Stop loss | 26 | 51.0% |
| EOT / other | 1 (window end, excluded from WR) | — |

→ Realisation stays **`FIXED_RR_FADE`**. No MID-exit logic.

### 3.4 Side balance

| Side | Tip n/WR/E_N | Prior n/WR/E_N | Hist composite |
| --- | --- | --- | --- |
| BUY | 26 / **38.5%** / **−0.14R** | 35 / **54.3%** / **+0.22R** | 64 / 46.9% / +0.06R |
| SELL | 25 / **60.0%** / **+0.35R** | 40 / **37.5%** / **−0.16R** | 67 / 44.8% / +0.01R |

**Read:** Tip edge is **sell-led**; prior edge is **buy-led**. Sides flip with regime — not a permanent one-sided engine. Optional later AIOS: side-caution by regime cell, not a preset flip yet.

### 3.5 Weekday (entry) — Tue filtered

| DOW | Tip n/WR/E_N | Prior n/WR/E_N |
| --- | --- | --- |
| Mon | 10 / 40% / −0.10R | 19 / **68%** / **+0.54R** |
| Tue | 0 / filtered | 0 / filtered |
| Wed | 11 / **82%** / **+0.84R** | 22 / 32% / −0.28R |
| Thu | 13 / **31%** / **−0.31R** | 16 / 44% / −0.02R |
| Fri | 17 / 47% / +0.06R | 18 / 39% / −0.13R |

Tue skip is live (n=0). **Thu** is the structural soft pocket on the tip; **Wed** is the tip star. Prior inverts Wed weakness — regime, not fixed DOW law.

### 3.6 Streaks

| | Tip | Prior | Hist |
| --- | ---: | ---: | ---: |
| Max win streak | 6 | 4 | 6 |
| Max loss streak | 6 | 7 | 7 |

Containment (`InpMaxLossStreak=3`) will pause after clusters — observed pause/fail blocks in log are consistent with this fingerprint.

---

## 4. Rolling windows

### 4.1 Calendar months (hist tip · closed TP/SL)

| Month | n | WR | E_N | Regime note |
| --- | ---: | ---: | ---: | --- |
| 2025-12 | 4 | 25% | −0.44R | Tip start · thin |
| 2026-01 | 31 | 48.4% | +0.09R | Prior · near flat |
| 2026-02 | 23 | **34.8%** | **−0.22R** | Prior drag |
| 2026-03 | 6 | 50% | +0.13R | Thin |
| 2026-04 | 15 | 53.3% | +0.20R | Prior recovery |
| 2026-05 | 9 | **55.6%** | **+0.25R** | MATCH home (dedicated tip) |
| 2026-06 | 11 | **54.5%** | **+0.23R** | MATCH home |
| 2026-07 | 7 | **28.6%** | **−0.36R** | MATCH tag · local fail |
| 2026-08 | 24 | 50.0% | +0.13R | MATCH strongest · high fire count |

**Tip months only (May–Aug dedicated):** 3/4 months E_N>0; Jul is the stress month. Aug carries volume (n=24) at BWR+ margin.

### 4.2 Dedicated window averages

| Window | n | WR | BM | E_N | EF† | Final Δ |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| May→Aug tip | 51 | 49.0% | +4.6 pp | **+0.103R** | +1.7 pp | **+$17.14** |
| Jan→Apr prior | 75 | 45.3% | +0.9 pp | +0.020R | −2.0 pp | +$4.48 |
| Hist Dec→Aug | 131 | 45.8% | +1.4 pp | +0.031R | −1.5 pp | +$10.97 |

### 4.3 Rolling trade windows (expectancy path)

#### Tip May→Aug (n=51)

| Window | Path avg WR | Path avg E_N | Min E_N | Max E_N | Read |
| --- | ---: | ---: | ---: | ---: | --- |
| W10 | ~49.8% | **+0.12R** | −0.33R | +0.58R | Soft Jul pocket visible |
| W15 | ~48.1% | **+0.08R** | −0.40R | +0.50R | Avg still > 0 |
| W20 | ~46.2% | **+0.03R** | −0.21R | +0.24R | Thin but non-collapsed |

#### Prior Jan→Apr (n=75)

| Window | Path avg E_N | Min E_N | Read |
| --- | ---: | ---: | --- |
| W10 | +0.06R | −0.78R | Deep Feb draw in path |
| W15 | +0.08R | −0.40R | Recovers into Apr |
| W20 | +0.08R | −0.33R | Avg > 0 despite soft WR |

#### Hist composite (n=131)

| Window | Path avg E_N | Min E_N | Read |
| --- | ---: | ---: | --- |
| W10 | +0.05R | −0.78R | Regime dips |
| W20 | +0.07R | −0.33R | No sustained collapse |
| W30 | +0.06R | −0.10R | Smoothed; still ≥ ~0 |

**Interpretation:** Expectancy averages stay near / above zero; path minima mark **regime mismatch clusters**, not permanent expectancy death.

### 4.4 Frequency

| Metric | Tip May→Aug | Prior Jan→Apr | Hist ~9m tip |
| --- | ---: | ---: | ---: |
| Closed trades | 51 | 75 | 131 |
| Trades / 30d | ~12.8 | ~18.8 | ~14.6 |
| Selectivity | Session + Tue + ATR max | Same | Same |
| Gate blocks (tip-scale) | Session / weekday / ATR dominate | Same | Same |

Higher fire rate than AAPL RTH+BBw sleeve; lower than FX M5 Harvest. ATR max binds material volume (healthy throttle).

---

## 5. Performance

### 5.1 Primary tip (2026.05.01 → 2026.08.31)

| Setting | Value |
| --- | --- |
| Symbol / TF | UK100 M15 |
| Magic | **26101201** |
| Geometry | SL2500 / TP3125 · RR **1.25** |
| Filters | 08–17 · skip Tue · ATR max **1470** · AOS **off** |
| Deposit | 500 |
| Final balance | **517.14** |
| Net PnL | **+$17.14** (+3.4%) |
| n / WR / E_N | 51 / 49.0% / **+0.103R** |
| Containment | Pause/fail blocks present; no equity-halt wipe observed |

### 5.2 Diagnostic windows

| Window | Final Δ | WR | E_N | Read |
| --- | ---: | ---: | ---: | --- |
| May→Aug tip | **+$17.14** | 49.0% | +0.103R | Home tip viable · thin EF |
| Jan→Apr prior | +$4.48 | 45.3% | +0.020R | Soft; Leak prior → EF≤0 |
| Dec2025→Aug hist | +$10.97 | 45.8% | +0.031R | Diluted by prior + Jul; still net + |

**Interpretation:** Engine has a **modest meanrev edge on UK100 when the tip cooperates** (May–Jun–Aug). Prior (esp. Feb) and Jul are regime taxes. Expansion keep; not attach-ready; AIOS candidate later for skip / side-caution / Jul-like cells.

### 5.3 Vs design probe

| | Probe (M15*) | Tester tip |
| --- | ---: | ---: |
| n | ~74 | 51 |
| WR | 54.1% | 49.0% |
| E_N | +0.215R | +0.103R |
| EF | +6.7 pp | +1.7 pp (prior Leak) |

Same geometry; Tester softer — expect this on live friction / path dependency. Do not overfit back to probe WR.

### 5.4 Expansion lens

| Question | Answer |
| --- | --- |
| Keep on asset list? | **Yes** — tip E_N>0, geometry clean, gates healthy |
| Live replace AUD/EUR? | **No** |
| AIOS now? | **No** — engine-only fingerprint first; native UK100 L2 later |
| Main hygiene watches | Thu · H08 · BUY on tip · Jul-like stress · Feb-like prior |
| Next evidence | Deal export → measured Leak/EF/MaxDD; Sep tip if MATCH continues |

---

## 6. Key metrics (scorecard snapshot)

### Balanced P0 · May→Aug 2026 tip · magic 26101201

| Metric | Value |
| --- | ---: |
| RR / R_design / RR−R | 1.25 / 1.25 / ~0 (FIXED_RR) |
| BWR / WR / BM | 44.4% / **49.0%** / **+4.6 pp** |
| E_N | **+0.103R** |
| Leak prior / EF prior | 2.9 pp / **+1.7 pp** |
| n | 51 |
| PF (approx) | ~1.20 |
| expR / trade | +0.10R |
| Net PnL | **+$17.14** (+3.4%) |
| Side diagnosis | Tip **sell-led**; prior buy-led (regime flip) |
| regime_filtered | **true** (London + skip Tue + ATR≤p75) |
| Live boundary | **Research only** · expansion queue |

### Supporting windows (same geometry)

| Metric | Prior Jan→Apr | Hist Dec→Aug |
| --- | ---: | ---: |
| WR / E_N | 45.3% / +0.020R | 45.8% / +0.031R |
| EF prior | −2.0 pp | −1.5 pp |
| Net PnL | +$4.48 | +$10.97 |
| Max loss streak | 7 | 7 |

---

## 7. Behavioural fingerprint (UK100)

1. Class: **mean-rev entry · FIXED_RR exit** (same family as FX/AAPL Balanced).  
2. **Intraday** holds (med win ~1.6h) — not an overnight inventory book.  
3. ATR max gate + London session + Tue skip define selectivity; BB-width deliberately OFF.  
4. Tip fires ~13 trades/month — denser than AAPL, sparser than FX M5.  
5. Structural soft pockets on tip: **Thu**, **H08**, **BUY**, **Jul**.  
6. Tip star pocket: **Wed** + **SELL** + **H14**.  
7. Side leadership **flips** tip vs prior — regime, not permanent bias.  
8. AOS OFF — fingerprint is pure engine; do not evaluate EUR/AUD L2 pins here.  
9. History tip from **2025.12.17** — long-window claims must state truncation.  
10. Tester WR sits below design probe — use blotter for keep/reject, probe for geometry design only.

---

## 8. Locked geometry (reference)

| Parameter | Value |
| --- | --- |
| InpBBPeriod / InpBBDev | 20 / **2.2** |
| InpMaxLevels / InpMaxEntries | **1 / 1** |
| InpLotMode / InpLot / MinLot | Risk% / **0.1** / **0.1** |
| InpSL_Points / InpTP_Points | **2500 / 3125** |
| Designed RR / BWR / Leak prior | **1.25 / 44.4% / 2.9 pp** |
| InpMaxSpread / CooldownBars | **200 / 2** |
| Session | **08:00–17:00** · **skip Tue** |
| ATR regime | ON · max **1470** · min 0 |
| BB-width regime | **OFF** |
| InpAOS_Enable | **false** |
| InpMagic | **26101201** |

Preset: `Profiles/Tester/BMRG/UK100/BMRG-M15-UK100-6M-P0_balanced_chart.set`.

---

## 9. Recommended use

| Do | Don’t |
| --- | --- |
| Keep UK100 on the **expansion asset list** | Treat as live AUDUSD/EURUSD replace |
| Score home tip (May–Aug / MATCH months) as primary | Claim multi-year robustness from truncated hist |
| Read Feb / Jul / Thu / H08 softness as **regime** | Hard-reject the asset on prior or Jul alone |
| Next: deal export → Leak/EF Stage-1; Sep tip; then UK100 AIOS | Pin EUR/AUD L2 models onto UK100 |
| Watch tip buy-caution / Thu hygiene as AIOS features | Flip to trend geometry or Harvest RR without a new sleeve card |
| Keep ATR max declared when claiming G3 | Claim unfiltered cross-regime edge |

---

## 10. One-line thesis

**UK100 M15 BMRG is a London-filtered G0 Bollinger mean-reversion fade (Balanced RR1.25 · ATR≤p75 · AOS OFF); on 2026.05→08 it realises WR 49% / E_N +0.10R / +$17 on $500 with thin positive EF under Leak prior — suitable for expansion research, not live attach, with Feb/Jul and tip buy/Thu softness read as regime mismatch until deal-scored EF and a UK100-specific AIOS.**
