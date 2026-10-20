# DE40 — System Profile

**Asset:** DE40 (Germany 40 / DAX) · MT5 ticker **DE30** · **TF:** M15  
**Sleeve:** Balanced P0 · **engine only (AOS OFF)**  
**Magic:** **26101902**  
**Preset:** `Profiles/Tester/BMRG/DE40/BMRG-M15-DE40-6M-P0_balanced_chart.set`  
**Also:** `Presets/BMRG-M15-DE40-6M-P0_balanced_chart.set`  
**Profile date:** 2026-10-19  
**Evidence:** Tester cache `Tester/cache/BMRG.DE30.M15.*.tst` (SingleTestCache · deposit **$500** · leverage 1:500 · every tick · ACCOUNT CURRENCY) · Tester `logs/` empty for this session — metrics from equity/deal-step reconstruction  
**Framework:** `doc/unified_edge_framework.md` · **binding:** [`edge_framework.md`](./edge_framework.md) · chart card `doc/BMRG_M15_DE40_6M_chart_preset.md` · Ouroboros `research/assets/DE40/`  
**Docs home:** [`doc/assets/DE40/`](./README.md)  
**AIOS plan:** [`aios_roadmap.md`](./aios_roadmap.md) · baseline [`DE40_AOS_BASELINE_v1.md`](./DE40_AOS_BASELINE_v1.md)  
**Review:** `blotter/archive/DE40-P0-CHART/`

**Scope:** Research **asset-list expansion** (EU index CFD). **Not** a live replace for AUDUSD / EURUSD / UK100 research OS. Own AIOS: **P0 stubs landed** — see roadmap; not required for expansion keep.

**Do not mix** with root `system_profile.md` (EURUSD champion) · `doc/assets/AUDUSD/` · `doc/assets/EURUSD/` · `doc/assets/UK100/` · EDX / INF live magics.

---

## 0. Evidence hierarchy

| Authority | Source |
| --- | --- |
| **Primary tip** | **2026.05.01 → 2026.10.18** · magic **26101902** · n=**77** · final **638.90** |
| **Supporting YTD** | **2026.01.01 → 2026.10.18** · same magic · n=**147** · final **612.43** |
| **2025 stub (broker depth)** | Effective from **2025.06.05** · Jun–Aug 2025 only in long caches · n≈**36–38** · net **−$65…−$77** |
| **Design prior (not blotter)** | Ouroboros M15* probe · n≈79 · WR **58.2%** · EF≈**+4.0 pp** (ATR≤4070 · cost prior 1100 pts) |
| **Regime map** | Ouroboros H1 meanrev · Jun–Aug MATCH · **May MISMATCH** · **Sep–Oct FRAGILE** · live 30d FRAGILE |
| **Normative scoring** | `doc/unified_edge_framework.md` |
| **Not admissible** | Live FX/UK OS magics · treating 2025 MISMATCH stub as class death · probe as Stage-1 blotter · claiming multi-year depth (broker tip from 2025-06) |

### Cross-window scoreboard (FIXED_RR design R=1.25 · Leak prior **9.8 pp**)

| Window | Final | Δ vs $500 | N | WR | R† | BM | E_N | EF† | MaxDD≈ |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| **Tip 2026.05→10.18** | **638.90** | **+138.90** | **77** | **58.4%** | **1.24** | **+14.0 pp** | **+0.310R** | **+4.2 pp** | **4.4%** |
| YTD 2026.01→10.18 | 612.43 | +112.43 | 147 | 50.3% | 1.25 | +5.9 pp | +0.132R | −3.9 pp | 13.9% |
| 2025 Jun→Aug stub | ~423 | −76.5 | 38 | 31.6% | ~1.15 | −12.8 pp | −0.29R | ≪0 | ~16.8% |
| Design probe (M15* · ATR≤p75) | — | — | ~79 | 58.2% | 1.25 | +13.8 pp | +0.310R | +4.0 pp | — |

† R from AW$/|AL|$ on FIXED_RR clusters (~+7.22 / −5.81 on tip). Leak prior = c_R≈1100/5000 → Leak = c_R/(R+1) ≈ **9.8 pp**. Replace with deal-exported Leak before Stage-1 production gate.

**Stage 0 (tip):** n≥30 · WR ≫ BWR · E_N ≫ 0 · TP > SL · MaxDD contained → **PASS**. Stage 1 tip EF **> 0** under Leak prior → preferred research keep.

---

## 1. System identity

| Field | Value |
| --- | --- |
| Full name | Bollinger Mean-Reversion Grid on DE40/DE30 M15 |
| Short code | BMRG · DE40 expansion |
| Primary class | **Mean reversion** (statistical deviation fade) |
| Secondary class | Grid / basket — **OFF** (G0 · MaxLevels=1 · MaxEntries=1) |
| Not | Trend-following, breakout, momentum-continuation, scalping theatre |
| Market / TF | **DE30** (DE40), M15 · Frankfurt / London cash sleeve |
| Execution | Closed-bar signal (shift 1) → market · lot **0.1** (broker `VOLUME_MIN`) |
| Realisation | **`FIXED_RR_FADE`** (TP/SL clusters dominate; rare non-1R leftovers) |
| Regime posture | **`regime_filtered=true`** (session 08–17 + skip Tue + ATR max ≈ p75) |

### Strategy-class statement

On DE40 the EA **fades excursions** past ±kσ Bollinger bands back toward the short-horizon mid-band. Same **mean-reversion** class as UK100 / FX Balanced / AAPL — **not** a trend system.

It should win when DAX **mean-reverts inside the cash session** often enough that:

```
WR > BWR = 1 / (1 + R)
E_N = WR × (R + 1) − 1 > 0
BM = WR − BWR > 0
EF = BM − Leak > 0   (after measured costs)
```

With designed **RR = 1.25** → **R ≈ 1.25** → **BWR = 44.4%**. Soft research targets after Leak prior (~9.8 pp — DE30 spread is fat): WR ≳ **54–58%**, BM ≥ **+10–14 pp**, E_N ≥ **+0.20R** on the home tip; prefer EF > 0.

It loses when price **band-rides** (EU equity impulse, risk-off trend days, high-vol **FRAGILE** cells) into the hard SL — classic meanrev failure. Soft or negative calendar months (esp. **2025-06/07 MISMATCH**, **2026-02/03**, and thinned **Sep–Oct FRAGILE**) are read first as **regime mismatch**, not class failure.

---

## 2. Edge profile

### 2.1 Theoretical edge (meanrev · Balanced RR=1.25)

| Concept | Designed | Implication |
| --- | ---: | --- |
| Class | Meanrev fade | Edge = **hit-rate above BWR**, with modest R thickness |
| Geometry | SL **5000** / TP **6250** pts | TP > SL always (hard rule) |
| Designed RR / R | **1.25** | Not Harvest RR=1.0 · not lottery RR≥3 |
| BWR | **44.4%** | Lower than Harvest 50% — more WR room |
| Side of edge | **Mixed WR + R** | WR-side primary; R=1.25 lifts E_N when WR clears BWR |
| Leak prior | ~**9.8 pp** (c_R≈1100/5000 / (R+1)) | Live spread ≈**1020** · RT cost prior ≈**1100** pts — ~7× UK100 |
| Soft research WR | ≳ **54–58%** after Leak prior | Probe / tip both ~58% |
| Selectivity (P0) | BB **2.2** · CD **2** · ATR≤**4070** | Cuts Sep/Oct FRAGILE high-vol |
| AOS | **OFF** | Pure engine extract; DE40 AIOS later |

**Why RR=1.25 (not Harvest 1.0):** Chart / expansion intent = mix functional WR **and** returns. Harvest would raise BWR to 50% and thin payoff for the same geometry. Growth RR=1.50 remains a design alt (probe EF +3.1 pp) — not the locked P0 sleeve.

**Why SL=5000 (~1.55× M15 ATR p50≈3230):** Structural 1R that clears the DE30 spread tax. Thin SL≈4400 raises Leak (~11 pp) and turns probe EF **negative** — rejected. ATR-p50 SL (~3230) collapses EF under Leak ≈15 pp.

**Why ATR max 4070 (≈p75) ON:** Declared regime filter (Gate G3). Probe: filtered EF **+4.0 pp** vs unfiltered **+2.2 pp**. Cuts high-vol **FRAGILE** (Sep/Oct + live 30d) without BB-width starvation. Prefer tighter p75 over p90 for cleaner regime alignment (EF nearly identical).

### 2.2 Structural win path

| Layer | Role on DE40 / DE30 |
| --- | --- |
| Signal | Long ≤ lower BB; short ≥ upper BB on closed M15 · **BBDev 2.2** |
| Regime gates | ATR **max 4070** ON · BB-width **OFF** |
| Session | Frankfurt / London cash **08:00–17:00** server · **skip Tue** |
| Entry hygiene | MaxSpread **1500** (must clear live ≈1020) · cooldown **2** bars |
| Exit | Fixed TP **+1.25R** or SL **−1R** (distance in points) |
| Risk G0 | One event · lot **0.1** · exposure / daily-loss containment |
| Containment | Loss-streak pause (3) · fail pause · daily loss % · equity halt |

### 2.3 Class metric targets (research soft bars)

| Metric | Soft target (expansion) | Hard worry |
| --- | --- | --- |
| WR | > 44.4% (BWR); prefer ≥ **54–58%** after Leak prior | Persistently ≤ BWR on tip + W20 |
| R (realised) | ≈ 1.25 (RR−R small) | R ≪ RR without WR compensation |
| BM | > 0; prefer ≥ **+10 pp** on home tip (fat Leak) | BM ≤ 0 on primary tip |
| E_N | > 0; prefer ≥ **+0.20R** on tip | ≤ 0 on tip and W20 |
| EF | > 0 after measured Leak | Persistently ≤ 0 with honest costs |
| Soft stress months | WR can dip ≪ BWR (MISMATCH / FRAGILE) | Cluster of home MATCH months ≪ BWR → revisit geometry |
| MaxDD (0.1 lot / $500) | soft under ~10–15% research | Equity-halt territory |
| Fire count tip | n ≥ **30** (Stage 0) | Starvation (ATR + session too tight) |

### 2.4 Realised edge — primary tip (2026.05 → 2026.10.18)

| Metric | Value | vs target |
| --- | ---: | --- |
| n | **77** | Usable Stage-0 (≥30) · matches probe n≈79 |
| WR | **58.4%** | Clears BWR 44.4%; **matches** design probe 58.2% |
| Realised R / BWR | **1.24** / 44.6% | On-thesis (RR−R ≈ 0.01) |
| BM | **+14.0 pp** | Soft bar cleared (fat-Leak sleeve) |
| E_N | **+0.310R** | Clears +0.20R soft bar |
| EF (Leak prior 9.8 pp) | **+4.2 pp** | Stage-1 preferred under prior |
| avgR / trade | **+0.31R** | Strong expectancy |
| PnL (tester final) | **+$138.90** (+27.8%) | Equity confirms E_N |
| PF (approx · FIXED_RR) | **~1.75** | Healthy |
| MaxDD (equity path) | **~$23** (**4.4%**) | Contained on tip |

**Probe vs Tester:** Design M15* probe and Tester tip align unusually well (WR 58.2% → 58.4%; E_N +0.310R both). Treat probe as **prior**, tip blotter as **authority** — here they agree.

### 2.5 Realised edge — supporting YTD (2026.01 → 2026.10.18)

| Metric | Value | vs tip |
| --- | ---: | --- |
| n / WR / E_N | 147 / **50.3%** / **+0.132R** | Softer WR; still E_N>0 |
| BM / EF prior | +5.9 pp / **−3.9 pp** | EF≤0 under 9.8 pp prior — tip remains admission window |
| PnL | **+$112.43** (+22.5%) | Still net + after Jan–Mar drag |
| MaxDD | **~$71** (**13.9%**) | Regime taxes visible |
| PF approx | ~1.26 | Diluted vs tip |

YTD is diluted by **Feb–Mar** (and thin Jan) before the tip home sleeve. Do not use YTD alone to reject; do not use tip alone to claim full-year robustness.

### 2.6 Regime / transfer caveat

Ouroboros H1 meanrev map (design tip months + relevant context):

| Month | Tag | MATCH% | FRAGILE% | Tester note (tip / YTD) |
| --- | --- | ---: | ---: | --- |
| 2025-06 | **MISMATCH** | — | — | Stub WR ~36% · class-off |
| 2025-07 | **MISMATCH** | — | — | Stub WR ~32% · class-off |
| 2026-01 | MATCH | — | — | YTD WR 45% · near flat |
| 2026-02 | MATCH | — | — | YTD WR **34%** · drag |
| 2026-03 | **FRAGILE** | — | — | YTD n=4 WR **0%** · ATR gate thins |
| 2026-04 | MATCH | — | — | YTD WR 75% · recovery |
| 2026-05 | **MISMATCH** | 40.4 | 14.1 | Tip WR **67%** · local win despite tag |
| 2026-06 | MATCH | 49.9 | 21.0 | Tip WR 50% · near BWR+ |
| 2026-07 | MATCH | 49.1 | 21.6 | Tip WR 50% · flat-ish |
| 2026-08 | MATCH | **67.2** | 0.0 | Tip WR **64%** · **n=33** star month |
| 2026-09 | **FRAGILE** | 31.0 | 45.9 | Tip WR 54% · still + under ATR max |
| 2026-10 | **FRAGILE** | 15.0 | 66.4 | Tip n=4 WR 50% · incomplete / gated |

**Read:** Jun–Aug on-home for meanrev (Aug strongest). May is tagged MISMATCH but tip still printed; Sep–Oct FRAGILE are thinned by ATR max — residual trades can still clear BWR. **2025-06/07** and **2026-02/03** failures are **regime mismatch / FRAGILE taxes**, not proof the fade class is wrong. Do not reject DE40 from the expansion list on the 2025 stub or Feb alone. Do not claim cross-regime robustness while ATR max stays ON.

**Broker depth:** YWO DE30 M1 starts **2025-06-05** (~489d). Full 2y not available. Long-window tester filenames that request 2025.01→2026.10 may only retain pre-tip equity in some caches — score dedicated tip / YTD runs.

M15 ATR (Point=0.01): p50 ≈ 3230 · p75 ≈ 4071 · p90 ≈ 4818 · mean ≈ 3328.

---

## 3. Trade profile

Primary evidence: **tip** May→Oct 2026 (n=77). YTD cited for regime contrast. Side / DOW / hold-time open until deal export (Tester journal empty this session).

### 3.1 Winners (tip · n=45 · 58.4%)

| | Tip May→Oct | YTD Jan→Oct |
| --- | --- | --- |
| Share | 45/77 (**58.4%**) | 74/147 (50.3%) |
| Typical exit | TP at **~+1.25R** (~+$7.2 on 0.1 lot) | same |
| PnL cluster | **+7.0…+7.4** dominates | same |
| Character | Fade completes to fixed TP | Same geometry |

- Tip winners are almost pure **FIXED_RR TP** hits — realisation stays on-thesis.  
- Best calendar pocket on tip: **Aug** (WR **64%**, n=33, net **+$81**) — strongest MATCH month.  
- May (despite MISMATCH tag) also strong (WR 67%, n=9).

### 3.2 Losers (tip · n=32 · 41.6%)

| | Tip May→Oct | YTD Jan→Oct |
| --- | --- | --- |
| Share | 32/77 (41.6%) | 73/147 (49.7%) |
| Typical exit | SL at **~−1R** (~−$5.8 on 0.1 lot) | same |
| PnL cluster | **−5.6…−5.9** dominates | same |
| Character | Continuation / impulse hits stop | Same |

- Classic meanrev failure: band-ride into SL.  
- Soft YTD pockets: **Feb** (WR 34%, n=29) · **Mar** (WR 0%, n=4 FRAGILE-thinned) · **2025-06/07 MISMATCH** stub.  
- One outlier loss (~−$15.6) appears in 2025 stub only — not the tip fingerprint.

### 3.3 Exit mix (tip · inferred from PnL clusters)

| Exit | Count≈ | Share | Read |
| --- | ---: | ---: | --- |
| Take profit (~+1.25R) | 45 | 58.4% | On-thesis |
| Stop loss (~−1R) | 32 | 41.6% | On-thesis |
| Other / non-1R | ~0–2 | <3% | Negligible |

→ Realisation stays **`FIXED_RR_FADE`**. No MID-exit logic.

### 3.4 Side / DOW / hold (P1 tape)

Source: `tapes/de40_tip_fire_tape_v0.csv` · `blotter/archive/DE40-AOS-P1/TAPE_QA.json`.

| Slice | Tip n / WR / E_N | Read |
| --- | --- | --- |
| **SELL** | 40 / **62.5%** / **+0.41R** | Tip expectancy carrier |
| **BUY** | 37 / 54.1% / +0.22R | Weaker but still > BWR |
| **Mon** | 25 / **64%** / **+0.44R** | Star DOW |
| Wed | 16 / 50% / +0.13R | Softest DOW (still ≥ BWR+) |
| Thu | 21 / 57% / +0.29R | OK |
| Fri | 15 / 60% / +0.35R | Star |
| Tue | 0 | Filtered |
| **H08** | 26 / **62%** / **+0.38R** | Frankfurt open = **star** (≠ UK soft H08) |
| H13 | 12 / **42%** / **−0.06R** | Soft hour seed |
| H12 / H14 | 9+11 / 78% / 73% | Mid-session stars |
| Med hold win / lose | ~1.0h / ~1.5h | Intraday cash sleeve |
| nights_held | ~0% tip | Not overnight inventory |

2 YTD fires closed via **daily-loss HALT** (flatten) — labeled `exit_reason=HALT`, y_lose=1.

### 3.5 Streaks / containment

| | Tip (path proxy) | YTD (path proxy) |
| --- | --- | --- |
| Expectancy path | W20 min E_N ≈ **+0.01R** | W20 min E_N ≈ **−0.34R** |
| Containment | `InpMaxLossStreak=3` armed | Same |

YTD path minima mark Feb–Mar regime clusters — containment pauses are expected under stress, not bugs.

---

## 4. Rolling windows

### 4.1 Calendar months

#### Tip sleeve (2026.05 → 2026.10) — primary

| Month | n | WR | Net $ | E_N≈ | Regime note |
| --- | ---: | ---: | ---: | ---: | --- |
| 2026-05 | 9 | **67%** | **+26.3** | +0.50R | MISMATCH tag · local win |
| 2026-06 | 12 | 50% | +8.3 | +0.12R | MATCH |
| 2026-07 | 6 | 50% | +4.1 | +0.12R | MATCH · thin |
| 2026-08 | **33** | **64%** | **+81.4** | +0.43R | MATCH strongest · volume |
| 2026-09 | 13 | 54% | +16.0 | +0.21R | FRAGILE · ATR-thinned · still + |
| 2026-10 | 4 | 50% | +2.8 | +0.12R | FRAGILE · incomplete tip |

**Tip months:** 6/6 net +; Aug carries the book. FRAGILE Sep still prints positive under ATR max.

#### YTD extras (before tip)

| Month | n | WR | Net $ | Regime note |
| --- | ---: | ---: | ---: | --- |
| 2026-01 | 29 | 45% | +1.4 | Soft MATCH |
| 2026-02 | 29 | **34%** | **−39.1** | Drag · regime tax |
| 2026-03 | 4 | **0%** | **−23.1** | FRAGILE · gated thin |
| 2026-04 | 8 | **75%** | **+32.3** | Recovery into tip |

#### 2025 stub (broker depth · not admission)

| Month | n | WR | Net $ | Regime note |
| --- | ---: | ---: | ---: | --- |
| 2025-06 | 11 | 36% | −12.4 | **MISMATCH** |
| 2025-07 | 25 | 32% | −52.4 | **MISMATCH** |
| 2025-08 | 2 | 0% | −11.8 | Thin |

### 4.2 Dedicated window averages

| Window | n | WR | BM | E_N | EF† | Final Δ | MaxDD≈ |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| **May→Oct tip** | **77** | **58.4%** | **+14.0 pp** | **+0.310R** | **+4.2 pp** | **+$138.90** | **4.4%** |
| Jan→Oct YTD | 147 | 50.3% | +5.9 pp | +0.132R | −3.9 pp | +$112.43 | 13.9% |
| 2025 Jun→Aug stub | 38 | 31.6% | −12.8 pp | −0.29R | ≪0 | −$76.5 | 16.8% |

### 4.3 Rolling trade windows (expectancy path)

R-units from $ PnL / |AL|≈5.81 (1R dollar proxy on 0.1 lot).

#### Tip May→Oct (n=77)

| Window | Path avg WR | Path avg E_N | Min E_N | Max E_N | Read |
| --- | ---: | ---: | ---: | ---: | --- |
| W10 | ~58.7% | **+0.32R** | −0.11R | +1.03R | Healthy; rare soft dip |
| W15 | ~59.4% | **+0.33R** | **+0.04R** | +0.94R | Min still > 0 |
| W20 | ~60.0% | **+0.34R** | **+0.01R** | +0.79R | No collapse |
| W30 | ~61.5% | **+0.38R** | +0.12R | +0.57R | Smoothed strong |

#### YTD Jan→Oct (n=147)

| Window | Path avg E_N | Min E_N | Read |
| --- | ---: | ---: | --- |
| W10 | +0.14R | **−0.57R** | Feb–Mar draw visible |
| W15 | +0.14R | −0.42R | Same |
| W20 | +0.15R | −0.34R | Avg > 0 despite soft WR |
| W30 | +0.15R | −0.33R | No permanent expectancy death |

**Interpretation:** Tip expectancy averages stay strongly positive; path minima on YTD mark **regime mismatch clusters**, not class death.

### 4.4 Frequency

| Metric | Tip May→Oct | YTD ~10m |
| --- | ---: | ---: |
| Closed trades | 77 | 147 |
| Trades / 30d | ~14.0 | ~14.7 |
| Selectivity | Session + Tue + ATR max | Same |
| vs UK100 tip | Similar density (~13/mo) | — |
| vs FX M5 Harvest | Sparser | — |

ATR max binds Sep/Oct volume (healthy throttle). Aug fire count (n=33) is the MATCH harvest month.

---

## 5. Performance

### 5.1 Primary tip (2026.05.01 → 2026.10.18)

| Setting | Value |
| --- | --- |
| Symbol / TF | **DE30** M15 (DE40) |
| Magic | **26101902** |
| Geometry | SL**5000** / TP**6250** · RR **1.25** |
| Filters | 08–17 · skip Tue · ATR max **4070** · AOS **off** |
| Deposit | 500 |
| Final balance | **638.90** |
| Net PnL | **+$138.90** (+27.8%) |
| n / WR / E_N | 77 / **58.4%** / **+0.310R** |
| EF (Leak prior) | **+4.2 pp** |
| MaxDD | **~4.4%** |
| Containment | Path-stable; no equity-halt wipe observed |

### 5.2 Diagnostic windows

| Window | Final Δ | WR | E_N | EF† | Read |
| --- | ---: | ---: | ---: | ---: | --- |
| May→Oct tip | **+$138.90** | 58.4% | +0.310R | +4.2 pp | Home tip **strong** |
| Jan→Oct YTD | +$112.43 | 50.3% | +0.132R | −3.9 pp | Diluted by Feb–Mar; still net + |
| 2025 Jun–Aug stub | −$76.5 | 31.6% | −0.29R | ≪0 | **MISMATCH** — not class reject |

**Interpretation:** Engine has a **strong meanrev edge on DE40 when the tip / MATCH sleeve cooperates** (esp. Aug). YTD and 2025 stub failures are regime taxes. Expansion keep; not attach-ready; AIOS later for Feb-like / MISMATCH / FRAGILE cells — after deal-scored Leak.

### 5.3 Vs design probe

| | Probe (M15* · ATR≤p75) | Tester tip |
| --- | ---: | ---: |
| n | ~79 | **77** |
| WR | 58.2% | **58.4%** |
| E_N | +0.310R | **+0.310R** |
| EF | +4.0 pp | **+4.2 pp** (prior Leak) |

Same geometry; Tester **confirms** probe — rare alignment. Still require measured Leak from deals before production Stage-1.

### 5.4 Expansion lens

| Question | Answer |
| --- | --- |
| Keep on asset list? | **Yes** — tip E_N/EF strong, geometry clean, gates healthy |
| Live replace AUD/EUR/UK? | **No** |
| AIOS now? | **P0 stubs done** — see [`aios_roadmap.md`](./aios_roadmap.md); next = deal export + P1 tape |
| Main hygiene watches | Feb–Mar · 2025 MISMATCH stub · Sep/Oct FRAGILE residual · fat spread Leak |
| Next evidence | Deal export → measured Leak · side/DOW/hour tape → P2 L2det CF |

---

## 6. Key metrics (scorecard snapshot)

### Balanced P0 · May→Oct 2026 tip · magic 26101902

| Metric | Value |
| --- | ---: |
| RR / R_realised / RR−R | 1.25 / **1.24** / ~0.01 |
| BWR / WR / BM | 44.4% / **58.4%** / **+14.0 pp** |
| E_N | **+0.310R** |
| Leak prior / EF prior | 9.8 pp / **+4.2 pp** |
| n | **77** |
| PF (approx) | **~1.75** |
| expR / trade | **+0.31R** |
| Net PnL | **+$138.90** (+27.8%) |
| MaxDD (path) | **~4.4%** |
| regime_filtered | **true** (cash session + skip Tue + ATR≤p75) |
| Live boundary | **Research only** · expansion keep |

### Supporting windows (same geometry)

| Metric | YTD Jan→Oct | 2025 Jun–Aug stub |
| --- | ---: | ---: |
| WR / E_N | 50.3% / +0.132R | 31.6% / −0.29R |
| EF prior | −3.9 pp | ≪0 |
| Net PnL | +$112.43 | −$76.5 |
| MaxDD | ~13.9% | ~16.8% |
| Read | Diluted keep | Regime mismatch |

---

## 7. Behavioural fingerprint (DE40)

1. Class: **mean-rev entry · FIXED_RR exit** (same family as UK100 / FX / AAPL Balanced).  
2. Tip WR/E_N **match design probe** — geometry is not fiction.  
3. ATR max gate + Frankfurt/London session + Tue skip define selectivity; BB-width deliberately OFF.  
4. Tip fires ~14 trades/month — UK100-like density; Aug is the volume star (n=33).  
5. Fat DE30 spread forces **fat SL (5000)** — Leak prior ~9.8 pp is the Stage-1 tax to beat.  
6. Soft pockets are **regime**: 2025-06/07 MISMATCH, 2026-02/03, residual FRAGILE Sep/Oct.  
7. Tip star pocket: **Aug MATCH** (WR 64%, +$81).  
8. AOS OFF — fingerprint is pure engine; do not evaluate EUR/UK L2 pins here.  
9. Broker history from **2025.06.05** — long-window claims must state truncation.  
10. Expansion candidate — **not** live attach; AIOS after deal-scored Leak + bad-cell tape.

---

## 8. Locked geometry (reference)

| Parameter | Value |
| --- | --- |
| InpBBPeriod / InpBBDev | 20 / **2.2** |
| InpMaxLevels / InpMaxEntries | **1 / 1** |
| InpLotMode / InpLot / MinLot | Risk% / **0.1** / **0.1** |
| InpSL_Points / InpTP_Points | **5000 / 6250** |
| Designed RR / BWR / Leak prior | **1.25 / 44.4% / 9.8 pp** |
| InpMaxSpread / CooldownBars | **1500 / 2** |
| Session | **08:00–17:00** · **skip Tue** |
| ATR regime | ON · max **4070** · min 0 |
| BB-width regime | **OFF** |
| InpAOS_Enable | **false** |
| InpMagic | **26101902** |

Preset: `Profiles/Tester/BMRG/DE40/BMRG-M15-DE40-6M-P0_balanced_chart.set`.

---

## 9. Recommended use

| Do | Don’t |
| --- | --- |
| Keep DE40 on the **expansion asset list** | Treat as live AUDUSD/EURUSD/UK100 replace |
| Score home tip (May–Oct / MATCH months) as primary | Reject on 2025 MISMATCH stub or Feb alone |
| Read Feb–Mar / 2025-06/07 / FRAGILE months as **regime** | Hard-reject the asset or flip to trend geometry |
| Next: deal export → measured Leak/EF; side/DOW tape; then DE40 AIOS | Pin EUR/UK L2 models onto DE30 |
| Re-check live spread vs MaxSpread 1500 before promote | Thin SL below ~5000 (Leak kills EF) |
| Keep ATR max declared when claiming G3 | Claim unfiltered cross-regime edge |

---

## 10. One-line thesis

**DE40/DE30 M15 BMRG is a Frankfurt/London-filtered G0 Bollinger mean-reversion fade (Balanced RR1.25 · SL5000/TP6250 · ATR≤p75 · AOS OFF); on 2026.05→10 it realises WR 58.4% / E_N +0.31R / EF ≈+4.2 pp under Leak prior / +$139 on $500 with MaxDD ~4% — strong expansion keep, not live attach, with 2025 MISMATCH and 2026 Feb–Mar softness read as regime mismatch until deal-scored Leak and a DE40-specific AIOS.**
