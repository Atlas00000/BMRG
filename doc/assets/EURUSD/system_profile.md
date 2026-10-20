# EURUSD — System Profile (M15 chart sleeve)

**Asset:** EURUSD · **TF:** M15  
**Sleeve:** P2 light-selective · Balanced RR · **engine only (AOS OFF)**  
**Magic:** **26101817**  
**Preset:** `Profiles/Tester/BMRG/EURUSD/BMRG-M15-EURUSD-6M-P2_light_selective_chart.set`  
**Also:** `Presets/BMRG-M15-EURUSD-6M-P2_light_selective_chart.set`  
**Profile date:** 2026-10-18  
**Evidence:** Tester `logs/20261018.log` · deposit **$500** · every tick · ACCOUNT CURRENCY  
**Framework:** `doc/unified_edge_framework.md` · **binding:** [`edge_framework.md`](./edge_framework.md) · chart card `doc/BMRG_M15_EURUSD_6M_chart_preset.md`  
**Docs home:** [`doc/assets/EURUSD/`](./README.md)  
**Review:** `blotter/archive/EURUSD-M15-P2/REVIEW.md` · trade stats `TRADE_PROFILE.json`

**Scope:** Research **asset-list expansion** (M15 chart sleeve). **Not** a live replace for M5 Harvest champ (`8210204`) · AUDUSD LIVE · UK100 research OS. Own AIOS planned later; not required for keep.

**Do not mix** with root `system_profile.md` (EURUSD **M5 Harvest** champion book) · `doc/assets/AUDUSD/` · `doc/assets/UK100/` · EDX / INF live magics.

---

## 0. Evidence hierarchy

| Authority | Source |
| --- | --- |
| **Primary tip** | **2026.05.01 → 2026.10.17** · magic **26101817** · n=45 · final **507.14** |
| **Supporting YTD** | **2026.01.01 → 2026.10.17** · same magic · n=72 · final **520.91** |
| **Ladder context** | P0 magic 26101815 (WR &lt; BWR) · P1 magic 26101816 (starved · reject) |
| **Design prior (not blotter)** | Ouroboros M15* probe · n≈52 · WR 50% · EF≈+2.6pp (ATR≤74) |
| **Regime map** | Ouroboros H1 meanrev · May–Sep MATCH · Oct FRAGILE |
| **Normative scoring** | `doc/unified_edge_framework.md` |
| **Not admissible** | Live Harvest `8210204` · aistack · treating P0/P1 as this sleeve · Oct FRAGILE alone as admission |

### Cross-window scoreboard (journal · FIXED_RR design R=1.25 · Leak prior 3.0 pp)

| Window | Final | Δ vs $500 | N | WR | BM | E_N | EF† |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| **Tip 2026.05→10.17** | **507.14** | **+7.14** | **45** | **46.7%** | **+2.2 pp** | **+0.050R** | **−0.7 pp** |
| **YTD 2026.01→10.17** | **520.91** | **+20.91** | **72** | **48.6%** | **+4.2 pp** | **+0.094R** | **+1.2 pp** |
| Design probe (M15*) | — | — | ~52 | 50.0% | +5.6 pp | +0.125R | +2.6 pp |

† Leak prior ≈ 20 pt RT / SL300 → c_R≈0.067 → Leak ≈ 3.0 pp. Replace with deal-exported Leak before Stage-1 production gate.

**Stage 0 (tip):** n≥30 · WR > BWR · E_N > 0 · TP ≥ SL → **PASS**. Stage 1 tip EF thin under cost prior.

---

## 1. System identity

| Field | Value |
| --- | --- |
| Full name | Bollinger Mean-Reversion Grid on EURUSD M15 |
| Short code | BMRG · EURUSD M15 expansion |
| Primary class | **Mean reversion** (statistical deviation fade) |
| Secondary class | Grid / basket — **OFF** (G0 · MaxLevels=1 · MaxEntries=1) |
| Not | Trend-following, breakout, momentum-continuation, scalping theatre |
| Market / TF | **EURUSD**, M15 · London/NY overlap sleeve |
| Execution | Closed-bar signal (shift 1) → market · lot **0.01** (min-lot path on $500) |
| Realisation | **`FIXED_RR_FADE`** (TP/SL; rare EOT on window end, excluded from WR) |
| Regime posture | **`regime_filtered=true`** (session 12–20 + skip Tue + ATR max ≈ p90) |

### Strategy-class statement

On EURUSD M15 the EA **fades excursions** past ±kσ Bollinger bands back toward the short-horizon mid-band. Same **mean-reversion** class as M5 Harvest/Balanced, AUDUSD Book A, UK100, AAPL — **not** a trend system.

It should win when EURUSD **mean-reverts inside the London/NY overlap** often enough that:

```
WR > BWR = 1 / (1 + R)
E_N = WR × (R + 1) − 1 > 0
BM = WR − BWR > 0
EF = BM − Leak > 0   (after measured costs)
```

With designed **RR = 1.25** → **R ≈ 1.25** → **BWR = 44.4%**. Soft research targets after Leak prior (~3.0 pp): WR ≳ 48–52%, BM ≥ +3–5 pp, E_N ≥ +0.05R on the home tip; prefer EF > 0.

It loses when price **band-rides** (USD impulse, trend days, high-vol FRAGILE cells) into the hard SL — classic meanrev failure. Soft or negative calendar months are read first as **regime mismatch**, not class failure.

---

## 2. Edge profile

### 2.1 Theoretical edge (meanrev · Balanced RR=1.25)

| Concept | Designed | Implication |
| --- | ---: | --- |
| Class | Meanrev fade | Edge = **hit-rate above BWR**, with modest R thickness |
| Geometry | SL **300** / TP **375** pts | TP > SL always (hard rule) |
| Designed RR / R | **1.25** | Not Harvest RR=1.0 · not lottery RR≥3 |
| BWR | **44.4%** | Lower than Harvest 50% — more WR room |
| Side of edge | **Mixed WR + R** | WR-side primary; R=1.25 lifts E_N when WR clears BWR |
| Leak prior | ~**3.0 pp** (c_R≈20/300 / (R+1)) | MaxSpread 30 · RT cost prior ≈20 pts |
| Soft research WR | ≳ **48–52%** after Leak prior | Ideal clears probe-like 50% |
| Selectivity (P2) | BB **2.3** · CD **3** | Light nudge vs P0; avoid P1 starvation |
| AOS | **OFF** | Pure engine extract; EURUSD M15 AIOS later |

**Why RR=1.25 (not Harvest 1.0):** Chart / expansion intent = mix functional WR **and** returns. Harvest raises BWR to 50% and thins E_N for the same WR. Growth RR≥1.5 often fails BWR on this tip.

**Why SL=300 (~6.5× M15 ATR p50≈46):** Structural 1R on a major — not token-SL WR theatre. Thin SL would inflate Leak and restrict geometry.

**Why ATR max 74 (≈p90) ON:** Declared regime filter (Gate G3). Cuts Oct tip **FRAGILE** (HV) without p75 starvation (ATR≤58 → n≈20 on design probe). BB-width deliberately OFF after P1 starved tip (n≈6).

**Why P2 (not P0 / P1):**

| Sleeve | Delta | Result |
| --- | --- | --- |
| P0 | BB 2.2 · CD 2 · ATR≤74 | Tip WR≈33% &lt; BWR — hit-rate fail |
| P1 | BB 2.4 · CD 3 · ATR≤68 · BBw ON | n≈6 starved — reject |
| **P2** | BB **2.3** · CD **3** · ATR≤**74** · BBw **off** | Tip n=45 · WR 46.7% > BWR · Stage 0 pass |

### 2.2 Structural win path

| Layer | Role on EURUSD M15 |
| --- | --- |
| Signal | Long ≤ lower BB; short ≥ upper BB on closed M15 · **BBDev 2.3** |
| Regime gates | ATR **max 74** ON · BB-width **OFF** |
| Session | London/NY overlap **12:00–20:00** server · **skip Tue** |
| Entry hygiene | MaxSpread **30** · cooldown **3** bars |
| Exit | Fixed TP **+1.25R** or SL **−1R** (distance in points) |
| Risk G0 | One event · lot 0.01 · exposure / daily-loss containment |
| Containment | Loss-streak pause (3) · fail pause · daily loss % · equity halt |

### 2.3 Class metric targets (research soft bars)

| Metric | Soft target (expansion) | Hard worry |
| --- | --- | --- |
| WR | > 44.4% (BWR); prefer ≥ **48–52%** after Leak prior | Persistently ≤ BWR on tip + W20 |
| R (realised) | ≈ 1.25 (RR−R small) | R ≪ RR without WR compensation |
| BM | > 0; prefer ≥ **+3–5 pp** on home tip | BM ≤ 0 on primary tip |
| E_N | > 0; prefer ≥ **+0.05R** on tip | ≤ 0 on tip and W20 |
| EF | > 0 after measured Leak | Persistently ≤ 0 with honest costs |
| Soft stress months | WR can dip ≈BWR / below (Feb / Aug-like) | Cluster of months ≪ BWR → regime / AIOS, not auto-kill |
| MaxDD (0.01 lot / $500) | soft under ~8–10% research | Equity-halt territory |
| Fire count tip | n ≥ **30** (Stage 0) | Starvation (P1 path) |

### 2.4 Realised edge — primary tip (2026.05 → 2026.10.17)

| Metric | Value | vs target |
| --- | ---: | --- |
| n | **45** | Usable Stage-0 (≥30) |
| WR | **46.7%** | Clears BWR 44.4%; below soft 48–52% and probe 50% |
| Designed R / BWR | 1.25 / 44.4% | On-thesis geometry (realised R holds) |
| BM | **+2.2 pp** | Soft bar thin but > 0 |
| E_N | **+0.050R** | Clears +0.05R soft bar (exact) |
| EF (Leak prior 3.0 pp) | **−0.7 pp** | Stage-1 thin — measure Leak before promote |
| avgR / trade | +0.05R | Positive expectancy |
| PnL (tester final) | **+$7.14** (+1.4%) | Equity confirms E_N direction |
| PF (approx · FIXED_RR) | ~1.09 | Modest |
| Max win / loss streak | 3 / 4 | Within containment pause-3 neighbourhood |

**Probe vs Tester gap:** Design M15* probe overstated WR (~50% → 46.7%) and EF (+2.6 → −0.7 under prior). Same class and geometry; treat probe as **prior**, blotter as **authority**.

### 2.5 Realised edge — supporting YTD (2026.01 → 2026.10.17)

| Metric | Value | vs tip |
| --- | ---: | --- |
| n / WR / E_N | 72 / **48.6%** / **+0.094R** | Stronger than tip |
| BM / EF prior | +4.2 pp / **+1.2 pp** | Clears Stage-1 soft bar under prior |
| PnL | **+$20.91** (+4.2%) | Confirms YTD edge |
| PF approx | ~1.18 | Healthier than tip |

YTD includes Jan (+0.50R) and Apr (+0.29R) home months that dilute Feb (−0.33R). Tip alone is the harder, more conservative admission window.

### 2.6 Regime / transfer caveat

Ouroboros H1 meanrev map (tip months): **May–Sep MATCH** · **Oct FRAGILE** (MATCH% 0 · FRAGILE% ≈95%). Tester soft pockets **Feb** (YTD) and **Aug** (inside MATCH tag) are **local regime / impulse taxes**, not proof the fade class is wrong. Do not reject EURUSD M15 from the expansion list on Feb or Aug alone. Do not claim cross-regime robustness while ATR max stays ON.

M15 ATR (Point=0.00001): p50 ≈ 46 · p75 ≈ 58 · p90 ≈ 74 · mean ≈ 49.

---

## 3. Trade profile

Primary evidence: **tip** May→Oct (n=45). YTD cited where side/regime stories differ. All lots **0.01**.

### 3.1 Winners (tip · n=21 · 46.7%)

| | Tip May→Oct | YTD |
| --- | --- | --- |
| Share | 21/45 (**46.7%**) | 35/72 (48.6%) |
| Typical exit | TP at **+1.25R** | same |
| Med hold (wins) | ~**23.9h** | ~**22.6h** |
| Mean hold (wins) | ~41.3h | ~31.2h |
| Hold ≥12h (wins) | **85.7%** | 65.7% |

- Meanrev on M15 needs **multi-bar / overnight** completion more often than UK100 cash (~1.6h med).  
- Inventory fingerprint: **overnight-capable** FX book, not index cash scalp.  
- Best DOW (tip): **Mon / Fri** (WR 50%, E_N +0.125R).  
- Best hours (tip, n≥3): **H12** (WR 50%, E_N +0.125R) · **H14** (WR 50%, E_N +0.125R).

### 3.2 Losers (tip · n=24 · 53.3%)

| | Tip May→Oct | YTD |
| --- | --- | --- |
| Share | 24/45 (53.3%) | 37/72 (51.4%) |
| Typical exit | SL at **−1R** | same |
| Med hold (losses) | ~**24.6h** | ~**19.4h** |
| Hold ≥12h (losses) | 66.7% | 59.5% |

- Soft DOW (tip): **Thu** (WR 37.5%, E_N −0.156R).  
- Soft hours: **H13** (WR 37.5%, n=8) · **H19** (WR 33.3%, n=3) · late-session thin.  
- Max loss streak tip **4** (above containment pause-3 → pauses fire; expected under stress).  
- **Aug** is the hostile tip calendar pocket (WR 42.9%, E_N −0.036R); **Feb** is the YTD hole (WR 30%, E_N −0.325R).

### 3.3 Exit mix (tip)

| Exit | Count | Share |
| --- | ---: | ---: |
| Take profit | 21 | 46.7% |
| Stop loss | 24 | 53.3% |
| EOT / other | excluded from WR | — |

→ Realisation stays **`FIXED_RR_FADE`**. No MID-exit logic. Realised win R = +1.25 · loss R = −1.0 on every scored deal.

### 3.4 Side balance

| Side | Tip n / WR / E_N | YTD n / WR / E_N |
| --- | --- | --- |
| BUY | 23 / **39.1%** / **−0.12R** | 34 / **35.3%** / **−0.21R** |
| SELL | 22 / **54.5%** / **+0.23R** | 38 / **60.5%** / **+0.36R** |

**Read:** Edge is **sell-led** on both tip and YTD. Buys sit below BWR — candidate AIOS hygiene later (side-caution by regime cell), **not** a preset flip yet. Do not hard-disable buys from one tip alone.

### 3.5 Weekday (entry) — Tue filtered

| DOW | Tip n / WR / E_N | YTD n / WR / E_N |
| --- | --- | --- |
| Mon | 16 / **50%** / **+0.13R** | 21 / **52%** / **+0.18R** |
| Tue | 0 / filtered | 0 / filtered |
| Wed | 13 / 46% / +0.04R | 21 / 43% / −0.04R |
| Thu | 8 / **38%** / **−0.16R** | 12 / 42% / −0.06R |
| Fri | 8 / **50%** / **+0.13R** | 18 / **56%** / **+0.25R** |

Tue skip is live (n=0). **Thu** is the structural soft pocket on the tip; **Mon/Fri** carry. Wed is near flat on tip, soft on YTD.

### 3.6 Streaks

| | Tip | YTD |
| --- | ---: | ---: |
| Max win streak | 3 | 4 |
| Max loss streak | 4 | 5 |

Containment (`InpMaxLossStreak=3`) will pause after clusters — observed fail-pause blocks in log are consistent with this fingerprint.

---

## 4. Rolling windows

### 4.1 Calendar months (YTD path · closed TP/SL)

| Month | n | WR | E_N | Regime note |
| --- | ---: | ---: | ---: | --- |
| 2026-01 | 9 | **66.7%** | **+0.50R** | Strong · pre-tip |
| 2026-02 | 10 | **30.0%** | **−0.33R** | **YTD hole · regime mismatch** |
| 2026-03 | 1 | 100% | +1.25R | Thin |
| 2026-04 | 7 | **57.1%** | **+0.29R** | Recovery |
| 2026-05 | 9 | 44.4% | 0.00R | MATCH · ≈BWR |
| 2026-06 | 9 | 44.4% | 0.00R | MATCH · ≈BWR |
| 2026-07 | 7 | **57.1%** | **+0.29R** | MATCH · tip carry |
| 2026-08 | 7 | 42.9% | −0.04R | MATCH tag · local soft |
| 2026-09 | 11 | 45.5% | +0.02R | MATCH · thin + |
| 2026-10 | 2 | 50.0% | +0.13R | **FRAGILE tip** · thin n |

**Tip months only (May–Oct):** 4/6 months E_N≥0; Jul carries; May/Jun flat at BWR; Aug soft; Oct underpowered.

### 4.2 Dedicated window averages

| Window | n | WR | BM | E_N | EF† | Final Δ |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Tip May→Oct | 45 | 46.7% | +2.2 pp | **+0.050R** | −0.7 pp | **+$7.14** |
| YTD Jan→Oct | 72 | 48.6% | +4.2 pp | **+0.094R** | +1.2 pp | **+$20.91** |

### 4.3 Rolling trade windows (expectancy path)

#### Tip May→Oct (n=45)

| Window | Path avg WR | Path avg E_N | Min E_N | Max E_N | Read |
| --- | ---: | ---: | ---: | ---: | --- |
| W10 | ~45.8% | **+0.03R** | −0.33R | +0.35R | Soft Aug pocket visible |
| W15 | ~45.8% | **+0.03R** | −0.25R | +0.20R | Avg still > 0 |
| W20 | ~46.3% | **+0.04R** | −0.21R | +0.13R | Thin but non-collapsed |
| W30 | ~45.8% | **+0.03R** | −0.03R | +0.13R | Smoothed ≥ ~0 |

#### YTD Jan→Oct (n=72)

| Window | Path avg WR | Path avg E_N | Min E_N | Max E_N | Read |
| --- | ---: | ---: | ---: | ---: | --- |
| W10 | ~46.5% | **+0.05R** | −0.55R | +0.58R | Deep Feb draw in path |
| W15 | ~46.7% | **+0.05R** | −0.25R | +0.35R | Recovers |
| W20 | ~47.4% | **+0.07R** | −0.21R | +0.24R | Avg > 0 despite Feb |
| W30 | ~46.7% | **+0.05R** | −0.03R | +0.20R | No sustained collapse |

**Interpretation:** Expectancy averages stay near / above zero; path minima mark **regime mismatch clusters** (Feb · Aug), not permanent expectancy death.

### 4.4 Frequency

| Metric | Tip May→Oct | YTD ~9.5m |
| --- | ---: | ---: |
| Closed trades | 45 | 72 |
| Trades / 30d | ~8.1 | ~7.6 |
| Selectivity | Session + Tue + ATR max + BB 2.3 + CD 3 | Same |
| Gate blocks | Session / weekday dominate; ATR>74 sparse | Same |

Lower fire rate than UK100 M15 tip (~13/mo) and FX M5 Harvest; intentional light selectivity after P0 hit-rate fail. ATR max binds HV without P1 starvation.

---

## 5. Performance

### 5.1 Primary tip (2026.05.01 → 2026.10.17)

| Setting | Value |
| --- | --- |
| Symbol / TF | EURUSD M15 |
| Magic | **26101817** |
| Geometry | SL300 / TP375 · RR **1.25** · BB **2.3** · CD **3** |
| Filters | 12–20 · skip Tue · ATR max **74** · AOS **off** |
| Deposit | 500 |
| Final balance | **507.14** |
| Net PnL | **+$7.14** (+1.4%) |
| n / WR / E_N | 45 / 46.7% / **+0.050R** |
| Containment | Fail-pause present; no equity-halt wipe observed |

### 5.2 Diagnostic windows

| Window | Final Δ | WR | E_N | Read |
| --- | ---: | ---: | ---: | ---: |
| Tip May→Oct | **+$7.14** | 46.7% | +0.050R | Home tip viable · Stage 0 · EF thin |
| YTD Jan→Oct | **+$20.91** | 48.6% | +0.094R | Stronger · EF prior > 0 |
| P0 tip (prior ladder) | negative / WR≪BWR | ~33% | &lt;0 | Hit-rate fail — superseded |
| P1 tip | starved | ~33% / n≈6 | — | Reject — filters too tight |

**Interpretation:** Engine has a **modest meanrev edge on EURUSD M15 when light selectivity is applied** (P2). P0 under-filters (WR fails); P1 over-filters (starves). Feb and Aug are regime taxes. Expansion keep; not attach-ready; AIOS candidate later for buy-caution / Thu / Feb-like cells.

### 5.3 Vs design probe

| | Probe (M15*) | Tester tip |
| --- | ---: | ---: |
| n | ~52 | 45 |
| WR | 50.0% | 46.7% |
| E_N | +0.125R | +0.050R |
| EF | +2.6 pp | −0.7 pp (prior Leak) |

Same geometry family; Tester softer — expect this on live friction / path dependency. Do not overfit back to probe WR.

### 5.4 Expansion lens

| Question | Answer |
| --- | --- |
| Keep on asset list? | **Yes** — tip Stage 0 pass, geometry clean, gates healthy |
| Live replace M5 Harvest / AUD? | **No** |
| AIOS now? | **No** — engine-only fingerprint first; native EURUSD M15 L2 later |
| Main hygiene watches | **BUY** · **Thu** · **H13/H19** · **Feb** · **Aug** · Oct FRAGILE |
| Next evidence | Deal export → measured Leak/EF/MaxDD; extend tip if MATCH continues |

---

## 6. Key metrics (scorecard snapshot)

### P2 light · tip 2026.05→10.17 · magic 26101817

| Metric | Value |
| --- | ---: |
| RR / R_design / RR−R | 1.25 / 1.25 / ~0 (FIXED_RR) |
| BWR / WR / BM | 44.4% / **46.7%** / **+2.2 pp** |
| E_N | **+0.050R** |
| Leak prior / EF prior | 3.0 pp / **−0.7 pp** |
| n | 45 |
| PF (approx) | ~1.09 |
| expR / trade | +0.05R |
| Net PnL | **+$7.14** (+1.4%) |
| Side diagnosis | Tip **sell-led**; BUY below BWR |
| regime_filtered | **true** (12–20 + skip Tue + ATR≤p90) |
| Live boundary | **Research only** · expansion keep · Stage 0 pass |

### Supporting YTD (same geometry)

| Metric | YTD Jan→Oct |
| --- | ---: |
| WR / E_N / EF prior | 48.6% / +0.094R / **+1.2 pp** |
| Net PnL | **+$20.91** |
| Max loss streak | 5 |
| Soft month | Feb WR 30% |

### Sleeve ladder

| Sleeve | Magic | Status |
| --- | ---: | --- |
| P0 balanced | 26101815 | WR &lt; BWR — superseded |
| P1 selective | 26101816 | reject — starved |
| **P2 light** | **26101817** | **chart sleeve · tip Stage 0 pass** |

---

## 7. Behavioural fingerprint (EURUSD M15 P2)

1. Class: **mean-rev entry · FIXED_RR exit** (same family as M5 Harvest/Balanced · UK100 · AAPL).  
2. **Overnight-capable** holds (med win ~24h tip) — FX inventory, not UK100 cash scalp.  
3. ATR max gate + session 12–20 + Tue skip + light BB/CD define selectivity; BB-width deliberately OFF.  
4. Tip fires ~8 trades/month — sparser than UK100 / M5 Harvest; intentional after P0 fail.  
5. Structural soft pockets: **BUY**, **Thu**, **H13/H19**, **Feb**, **Aug**.  
6. Tip / YTD star pockets: **SELL**, **Mon/Fri**, **H12/H14**, **Jul** (and Jan/Apr on YTD).  
7. Side leadership is **sell-led** tip and YTD — stronger than UK100’s tip/prior flip.  
8. AOS OFF — fingerprint is pure engine; do not evaluate M5 L2 pins here.  
9. Oct tip FRAGILE + thin n — do not use as admission; ATR gate is the declared cut.  
10. Tester WR sits below design probe — use blotter for keep/reject, probe for geometry design only.

---

## 8. Locked geometry (reference)

| Parameter | Value |
| --- | --- |
| InpBBPeriod / InpBBDev | 20 / **2.3** |
| InpMaxLevels / InpMaxEntries | **1 / 1** |
| InpLotMode / Risk% | Risk% / **0.5** (realised lot **0.01** on $500) |
| InpSL_Points / InpTP_Points | **300 / 375** |
| Designed RR / BWR / Leak prior | **1.25 / 44.4% / 3.0 pp** |
| InpMaxSpread / CooldownBars | **30 / 3** |
| Session | **12:00–20:00** · **skip Tue** |
| ATR regime | ON · max **74** · min 0 |
| BB-width regime | **OFF** |
| InpAOS_Enable | **false** |
| InpMagic | **26101817** |

Preset: `Profiles/Tester/BMRG/EURUSD/BMRG-M15-EURUSD-6M-P2_light_selective_chart.set`.

---

## 9. Recommended use

| Do | Don’t |
| --- | --- |
| Keep EURUSD M15 P2 on the **expansion asset list** | Treat as live M5 Harvest / AUDUSD replace |
| Score tip (May→Oct) as primary; YTD as support | Claim Stage-1 production on Leak **prior** alone |
| Read Feb / Aug / BUY / Thu softness as **regime** | Hard-reject the sleeve on Feb or Aug alone |
| Next: deal export → Leak/EF Stage-1; follow [`aios_roadmap.md`](./aios_roadmap.md) | Pin M5 aistack / AUD / UK100 L2 models onto this sleeve |
| Watch buy-caution / Thu hygiene as AIOS features (bad-cell registry) | Flip to trend geometry or Harvest RR without a new sleeve card |
| Keep ATR max declared when claiming G3 | Claim unfiltered cross-regime edge |
| Remember P0/P1 ladder lessons | Re-stack P1 (ATR≤68 + BBw) without a new card |

---

## 10. One-line thesis

**EURUSD M15 BMRG is a London/NY-filtered G0 Bollinger mean-reversion fade (Balanced RR1.25 · BB2.3 · CD3 · ATR≤p90 · AOS OFF); on 2026.05→10 it realises WR 46.7% / E_N +0.05R / +$7 on $500 with Stage 0 pass and thin/negative EF under Leak prior — suitable for expansion research ahead of per-asset AIOS, not live attach, with Feb/Aug and tip buy/Thu softness read as regime mismatch until deal-scored EF.**
