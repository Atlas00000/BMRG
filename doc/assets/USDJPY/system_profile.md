# USDJPY — System Profile

**Asset:** USDJPY · **TF:** M15  
**Sleeve:** Balanced P0 · **engine only (AOS OFF)**  
**Magic:** **26101828**  
**Preset:** `Profiles/Tester/BMRG/USDJPY/BMRG-M15-USDJPY-6M-P0_balanced_chart.set`  
**Also:** `Presets/BMRG-M15-USDJPY-6M-P0_balanced_chart.set`  
**Profile date:** 2026-10-19  
**Evidence:** Tester `logs/20261019.log` · deposit **$500** · leverage 1:500 · every tick · ACCOUNT CURRENCY  
**Framework:** `doc/unified_edge_framework.md` · **binding:** [`edge_framework.md`](./edge_framework.md) · chart card `doc/BMRG_M15_USDJPY_6M_chart_preset.md`  
**Docs home:** [`doc/assets/USDJPY/`](./README.md)  
**AIOS plan:** [`aios_roadmap.md`](./aios_roadmap.md)  
**Review:** `blotter/archive/USDJPY-P0-CHART/REVIEW.md` · trade stats `TRADE_PROFILE.json`

**Scope:** Research **asset-list expansion** (yen major · M15 chart sleeve). **Not** a live replace for EURUSD M5 Harvest (`8210204`) · EURUSD M15 OS · AUDUSD LIVE · UK100 research OS. Own AIOS: **P0 stubs landed** — see roadmap; not required for keep.

**Do not mix** with root `system_profile.md` (EURUSD M5 champion) · `doc/assets/EURUSD/` · `doc/assets/AUDUSD/` · `doc/assets/UK100/` · EDX / INF live magics.

---

## 0. Evidence hierarchy

| Authority | Source |
| --- | --- |
| **Primary tip** | **2026.05.01 → 2026.08.31** · magic **26101828** · n=56 · final **505.99** |
| **Supporting YTD** | **2026.01.01 → 2026.10.19** · same magic · n=68 · final **517.99** |
| **Supporting prior** | **2026.01.01 → 2026.04.30** · n=8 · final **501.20** (thin / ATR-starved) |
| **Long hist** | **2025.01.01 → 2026.10.19** · n=83 · final **514.29** (sparse 2025 fires) |
| **Design prior (not blotter)** | Ouroboros M15* probe · n≈66 · WR 57.6% · EF≈+0.8pp (ATR≤70 · 25pt cost prior) |
| **Regime map** | Ouroboros H1 meanrev · Apr–Aug MATCH · **Sep FRAGILE** (FRAGILE%≈57%) · Jul MATCH% soft (41%) / FRAGILE%↑ (36%) |
| **Normative scoring** | `doc/unified_edge_framework.md` |
| **Not admissible** | Live Harvest / EUR M15 OS magics · treating probe as blotter · Sep FRAGILE alone as admission · Jul WR hole as geometry death |

### Cross-window scoreboard (journal · FIXED_RR design R=1.20 · Leak prior 11.4 pp)

| Window | Final | Δ vs $500 | N | WR | BM | E_N | EF† |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| **Tip 2026.05→08.31** | **505.99** | **+5.99** | **56** | **48.2%** | **+2.8 pp** | **+0.061R** | **−8.6 pp** |
| Prior 2026.01→04.30 | 501.20 | +1.20 | 8 | 50.0% | +4.5 pp | +0.100R | −6.9 pp |
| Jan→Aug 2026 | 505.90 | +5.90 | 64 | 48.4% | +3.0 pp | +0.066R | −8.4 pp |
| **YTD 2026.01→10.19** | **517.99** | **+17.99** | **68** | **51.5%** | **+6.0 pp** | **+0.132R** | **−5.4 pp** |
| Long 2025.01→2026.10 | 514.29 | +14.29 | 83 | 49.4% | +3.9 pp | +0.087R | −7.5 pp |
| Design probe (M15*) | — | — | ~66 | 57.6% | +12.1 pp | +0.267R | +0.8 pp |

† Leak prior ≈ 25 pt RT / SL100 → c_R≈0.25 → Leak = c_R/(R+1) ≈ **11.4 pp**. Replace with deal-exported Leak before Stage-1 production gate.

**Stage 0 (tip):** n≥30 · WR > BWR · E_N > 0 · TP ≥ SL → **PASS**. Stage 1 tip EF deeply negative under 25pt cost prior (thin BM vs major Leak).

---

## 1. System identity

| Field | Value |
| --- | --- |
| Full name | Bollinger Mean-Reversion Grid on USDJPY M15 |
| Short code | BMRG · USDJPY M15 expansion |
| Primary class | **Mean reversion** (statistical deviation fade) |
| Secondary class | Grid / basket — **OFF** (G0 · MaxLevels=1 · MaxEntries=1) |
| Not | Trend-following, breakout, momentum-continuation, scalping theatre |
| Market / TF | **USDJPY**, M15 · London/NY overlap sleeve (Tokyo 02–12 failed design probe) |
| Execution | Closed-bar signal (shift 1) → market · risk% lot path on $500 |
| Realisation | **`FIXED_RR_FADE`** (TP/SL; no EOT orphans on scored windows) |
| Regime posture | **`regime_filtered=true`** (session 12–20 + skip Tue + ATR max ≈ tight p50 band) |

### Strategy-class statement

On USDJPY M15 the EA **fades excursions** past ±kσ Bollinger bands back toward the short-horizon mid-band. Same **mean-reversion** class as EURUSD M5 Harvest/Balanced, EURUSD M15 P2, AUDUSD Book A, UK100, AAPL — **not** a trend system.

It should win when USDJPY **mean-reverts inside the London/NY overlap** often enough that:

```
WR > BWR = 1 / (1 + R)
E_N = WR × (R + 1) − 1 > 0
BM = WR − BWR > 0
EF = BM − Leak > 0   (after measured costs)
```

With designed **RR = 1.20** → **R ≈ 1.20** → **BWR ≈ 45.5%**. Soft research targets after Leak prior (~11.4 pp on 25pt RT): WR ≳ **57%+** to clear Stage-1 EF under that prior; softer Stage-0 bar remains WR > BWR and E_N > 0. Prefer EF > 0 after **measured** Leak (may be lower than 25pt prior).

It loses when price **band-rides** (USD/JPY impulse, BoJ/risk-off trend days, high-vol FRAGILE cells) into the hard SL — classic meanrev failure. Soft or negative calendar months (esp. **Jul**) are read first as **regime mismatch**, not class failure.

---

## 2. Edge profile

### 2.1 Theoretical edge (meanrev · Balanced RR=1.20)

| Concept | Designed | Implication |
| --- | ---: | --- |
| Class | Meanrev fade | Edge = **hit-rate above BWR**, with modest R thickness |
| Geometry | SL **100** / TP **120** pts | TP > SL always (hard rule) |
| Designed RR / R | **1.20** | Not Harvest RR=1.0 · not lottery RR≥3 · slightly below EUR/UK 1.25 |
| BWR | **45.5%** | Higher bar than RR1.25 (44.4%) — needs more WR for same BM |
| Side of edge | **Mixed WR + R** | WR-side primary; R=1.20 lifts E_N when WR clears BWR |
| Leak prior | ~**11.4 pp** (c_R≈25/100 / (R+1)) | MaxSpread 25 · RT cost prior ≈25 pts — **expensive vs SL** |
| Soft research WR | ≳ **57%** to clear EF under 25pt prior; Stage-0 ≥ **45.5%** | Probe claimed 57.6%; Tester tip ~48% |
| Selectivity (P0) | BB **2.2** · CD **2** · ATR≤**70** | Tight ATR vs EUR p90 — cuts Sep FRAGILE |
| AOS | **OFF** | Pure engine extract; USDJPY AIOS later |

**Why RR=1.20 (not Harvest 1.0 / not EUR 1.25):** Chart / expansion intent = mix functional WR **and** returns inside preferred [1.20, 1.35] band. Exact RR=1.25 (100/125) thinned Stage-1 under the same 25pt prior in design probes — kept as alt with MaxSpread 20.

**Why SL=100 (~1.5× M15 ATR p50≈65):** Structural 1R on yen major — not token-SL WR theatre. Do **not** import EURUSD 300pt or GBPJPY 160pt floors (wrong ATR scale; would starve under ATR≤70).

**Why ATR max 70 ON:** Declared regime filter (Gate G3). Cuts **Sep FRAGILE** high-vol tip. Probe: ATR≤70 lifted WR to 57.6% / EF≈+0.8pp vs unfiltered EF negative under 25pt prior. Wider ATR≤92 diluted EF. BB-width deliberately OFF (fire starvation risk).

**Why session 12–20 (not Tokyo 02–12):** Design probe Tokyo sleeve failed (WR≈45% · EF≪0). London/NY overlap is the home session for this yen fade.

### 2.2 Structural win path

| Layer | Role on USDJPY M15 |
| --- | --- |
| Signal | Long ≤ lower BB; short ≥ upper BB on closed M15 · **BBDev 2.2** |
| Regime gates | ATR **max 70** ON · BB-width **OFF** |
| Session | London/NY overlap **12:00–20:00** server · **skip Tue** |
| Entry hygiene | MaxSpread **25** · cooldown **2** bars |
| Exit | Fixed TP **+1.20R** or SL **−1R** (distance in points) |
| Risk G0 | One event · risk% sizing · exposure / daily-loss containment |
| Containment | Loss-streak pause (3) · fail pause · daily loss % · equity halt |

### 2.3 Class metric targets (research soft bars)

| Metric | Soft target (expansion) | Hard worry |
| --- | --- | --- |
| WR | > 45.5% (BWR); prefer ≥ **57%** after 25pt Leak prior | Persistently ≤ BWR on tip + W20 |
| R (realised) | ≈ 1.20 (RR−R small) | R ≪ RR without WR compensation |
| BM | > 0; prefer ≥ **+11–12 pp** to clear prior Leak | BM ≤ 0 on primary tip |
| E_N | > 0; prefer ≥ **+0.05R** on tip | ≤ 0 on tip and W20 |
| EF | > 0 after measured Leak | Persistently ≤ 0 with honest costs |
| Soft stress months | WR can dip ≪ BWR (Jul-like) | Cluster of months ≪ BWR → regime / AIOS, not auto-kill |
| MaxDD (risk% / $500) | soft under ~8–10% research | Equity-halt territory |
| Fire count tip | n ≥ **30** (Stage 0) | Starvation (ATR + session too tight) |

### 2.4 Realised edge — primary tip (2026.05 → 2026.08.31)

| Metric | Value | vs target |
| --- | ---: | --- |
| n | **56** | Usable Stage-0 (≥30) |
| WR | **48.2%** | Clears BWR 45.5%; **well below** soft 57% and probe 57.6% |
| Designed R / BWR | 1.20 / 45.5% | On-thesis geometry (FIXED_RR) |
| BM | **+2.8 pp** | Soft bar thin but > 0 |
| E_N | **+0.061R** | Clears +0.05R soft bar |
| EF (Leak prior 11.4 pp) | **−8.6 pp** | Stage-1 fail under prior — measure Leak before promote |
| avgR / trade | +0.06R | Positive expectancy |
| PnL (tester final) | **+$5.99** (+1.2%) | Equity confirms E_N direction |
| PF (approx · FIXED_RR) | ~1.12 | Modest |
| Max win / loss streak | 3 / **7** | Loss streak above pause-3 → containment fires |

**Probe vs Tester gap:** Design M15* probe overstated WR (~57.6% → 48.2%) and EF (+0.8 → −8.6 under prior). Same class and geometry; treat probe as **prior**, blotter as **authority**. Major Leak prior vs thin BM is the Stage-1 bottleneck — not geometry death.

### 2.5 Realised edge — supporting YTD (2026.01 → 2026.10.19)

| Metric | Value | vs tip |
| --- | ---: | --- |
| n / WR / E_N | 68 / **51.5%** / **+0.132R** | Stronger than tip |
| BM / EF prior | +6.0 pp / **−5.4 pp** | Still EF≤0 under 25pt prior |
| PnL | **+$17.99** (+3.6%) | Confirms YTD edge |
| PF approx | ~1.27 | Healthier than tip |

YTD lifts on Aug recover + Oct stub + slightly better path after Jul hole. Tip alone remains the harder admission window. Prior Jan→Apr is **n=8 starved** under ATR≤70 — do not over-read.

### 2.6 Regime / transfer caveat

Ouroboros H1 meanrev map (design tip months):

| Month | Tag | MATCH% | FRAGILE% |
| --- | --- | ---: | ---: |
| 2026-04 | MATCH | 59.7 | 20.5 |
| 2026-05 | MATCH | 52.4 | 17.3 |
| 2026-06 | MATCH | 55.7 | 19.9 |
| 2026-07 | MATCH | **41.3** | **35.7** |
| 2026-08 | MATCH | 49.9 | 21.7 |
| 2026-09 | **FRAGILE** | 20.6 | **57.4** |

Tester **Jul WR 33.3%** sits inside a soft MATCH / elevated-FRAGILE month — **local regime tax**, not proof the fade class is wrong. **Sep = 0 fires** under ATR≤70 — gate doing its job on FRAGILE tip. Do not reject USDJPY from the expansion list on Jul alone. Do not claim cross-regime robustness while ATR max stays ON.

M15 ATR (Point=0.001): p50 ≈ 65 · p75 ≈ 92 · p90 ≈ 133 · mean ≈ 80. Quieter than GBPJPY (p50≈100).

---

## 3. Trade profile

Primary evidence: **tip** May→Aug (n=56). YTD cited where side/regime stories differ. Source: `TRADE_PROFILE.json` from Tester journal (CTrade duplicates excluded).

### 3.1 Winners (tip · n=27 · 48.2%)

| | Tip May→Aug | YTD Jan→Oct |
| --- | --- | --- |
| Share | 27/56 (**48.2%**) | 35/68 (51.5%) |
| Typical exit | TP at **+1.20R** | same |
| Med hold (wins) | ~**1.2h** | ~**1.5h** |
| Mean hold (wins) | ~6.6h | ~5.7h |
| Hold ≥12h (wins) | **11.1%** | 8.6% |

- Meanrev on USDJPY M15 is mostly **intraday fade** inside the 12–20 sleeve — closer to UK100 cash holds than EURUSD M15 overnight inventory.  
- Inventory fingerprint: **session-bound yen book**, not multi-day carry.  
- Best DOW (tip): **Fri** (WR 60%, E_N +0.32R) · **Mon** (WR 56%, E_N +0.24R).  
- Best hours (tip, n≥4): **H18 / H19** (WR 75%, E_N +0.65R) · **H15** (WR 56%, E_N +0.22R).

### 3.2 Losers (tip · n=29 · 51.8%)

| | Tip May→Aug | YTD Jan→Oct |
| --- | --- | --- |
| Share | 29/56 (51.8%) | 33/68 (48.5%) |
| Typical exit | SL at **−1R** | same |
| Med hold (losses) | ~**0.9h** | ~**0.8h** |
| Hold ≥12h (losses) | 6.9% | 6.1% |

- Soft DOW (tip): **Thu** (WR **30.8%**, E_N **−0.32R**, n=13) — same structural soft pocket as EUR/UK tips.  
- Soft hours: **H14** (WR 42.9%, E_N −0.06R, n=14) · **H16–17** thin and weak.  
- Max loss streak tip **7** (above containment pause-3 → pauses fire; expected under Jul stress).  
- **Jul** is the hostile tip calendar pocket (WR 33.3%, E_N −0.27R, n=18).

### 3.3 Exit mix (tip)

| Exit | Count | Share |
| --- | ---: | ---: |
| Take profit | 27 | 48.2% |
| Stop loss | 29 | 51.8% |
| EOT / other | 0 on scored tip | — |

→ Realisation stays **`FIXED_RR_FADE`**. No MID-exit logic. Realised win R = +1.20 · loss R = −1.0 on every scored deal.

### 3.4 Side balance

| Side | Tip n / WR / E_N | YTD n / WR / E_N |
| --- | --- | --- |
| BUY | 21 / **52.4%** / **+0.15R** | 24 / **54.2%** / **+0.19R** |
| SELL | 35 / 45.7% / +0.01R | 44 / 50.0% / +0.10R |

**Read:** Fire count is **sell-heavy** (~63% of tip opens), but **expectancy is buy-led** on tip and YTD. Sells sit near BWR on tip — volume without edge thickness. Candidate later AIOS: sell-caution / regime-cell hygiene, **not** a preset flip yet. Do not hard-disable sells from one tip alone.

### 3.5 Weekday (entry) — Tue filtered

| DOW | Tip n / WR / E_N | YTD n / WR / E_N |
| --- | --- | --- |
| Mon | 16 / **56%** / **+0.24R** | 19 / **63%** / **+0.39R** |
| Tue | 0 / filtered | 0 / filtered |
| Wed | 17 / 47% / +0.04R | 19 / 42% / −0.07R |
| Thu | 13 / **31%** / **−0.32R** | 18 / **39%** / **−0.14R** |
| Fri | 10 / **60%** / **+0.32R** | 12 / **67%** / **+0.47R** |

Tue skip is live (n=0). **Thu** is the structural soft pocket; **Mon/Fri** carry. Wed is near flat on tip, soft on YTD.

### 3.6 Streaks

| | Tip | YTD |
| --- | ---: | ---: |
| Max win streak | 3 | 5 |
| Max loss streak | **7** | **7** |

Containment (`InpMaxLossStreak=3`) will pause after clusters — observed fail-pause blocks in log are consistent with this fingerprint (esp. around Jul).

---

## 4. Rolling windows

### 4.1 Calendar months (YTD path · closed TP/SL)

| Month | n | WR | E_N | Regime note |
| --- | ---: | ---: | ---: | --- |
| 2026-01 | 2 | 50.0% | +0.10R | Thin / ATR-starved |
| 2026-03 | 1 | 100% | +1.20R | Thin |
| 2026-04 | 5 | 40.0% | −0.12R | Soft prior |
| 2026-05 | 13 | **53.8%** | **+0.19R** | MATCH home |
| 2026-06 | 22 | **54.5%** | **+0.20R** | MATCH · best fire month |
| 2026-07 | 18 | **33.3%** | **−0.27R** | **MATCH tag · regime mismatch hole** |
| 2026-08 | 4 | 75.0% | +0.65R | Thin recover |
| 2026-09 | **0** | — | — | **FRAGILE · ATR≤70 starve (correct)** |
| 2026-10 | 3 | 100% | +1.20R | Stub tip |

**Tip months only (May–Aug):** 3/4 months E_N>0; Jun carries volume; **Jul is the stress month**. Aug thin but positive.

### 4.2 Dedicated window averages

| Window | n | WR | BM | E_N | EF† | Final Δ |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Tip May→Aug | 56 | 48.2% | +2.8 pp | **+0.061R** | −8.6 pp | **+$5.99** |
| Prior Jan→Apr | 8 | 50.0% | +4.5 pp | +0.100R | −6.9 pp | +$1.20 |
| YTD Jan→Oct | 68 | 51.5% | +6.0 pp | **+0.132R** | −5.4 pp | **+$17.99** |
| Long 2025→Oct | 83 | 49.4% | +3.9 pp | +0.087R | −7.5 pp | +$14.29 |

### 4.3 Rolling trade windows (expectancy path)

#### Tip May→Aug (n=56)

| Window | Path avg WR | Path avg E_N | Min E_N | Max E_N | Read |
| --- | ---: | ---: | ---: | ---: | --- |
| W10 | ~45.7% | **+0.01R** | −0.78R | +0.54R | Soft Jul pocket visible |
| W15 | ~46.0% | **+0.01R** | −0.71R | +0.47R | Avg still ≥ 0 |
| W20 | ~46.5% | **+0.02R** | −0.45R | +0.43R | Thin but non-collapsed |
| W30 | ~47.2% | **+0.04R** | −0.19R | +0.32R | Smoothed ≥ ~0 |

#### YTD Jan→Oct (n=68)

| Window | Path avg WR | Path avg E_N | Min E_N | Max E_N | Read |
| --- | ---: | ---: | ---: | ---: | --- |
| W10 | ~47.8% | **+0.05R** | −0.78R | +0.76R | Deep Jul draw in path |
| W15 | ~46.9% | **+0.03R** | −0.71R | +0.47R | Recovers |
| W20 | ~47.1% | **+0.04R** | −0.45R | +0.43R | Avg > 0 despite Jul |
| W30 | ~48.3% | **+0.06R** | −0.19R | +0.32R | No sustained collapse |

**Interpretation:** Expectancy averages stay near / above zero; path minima mark **regime mismatch clusters** (Jul), not permanent expectancy death.

### 4.4 Frequency

| Metric | Tip May→Aug | YTD ~9.5m |
| --- | ---: | ---: |
| Closed trades | 56 | 68 |
| Trades / 30d | ~14.0 | ~7.2 |
| Selectivity | Session + Tue + ATR max + BB 2.2 + CD 2 | Same |
| Gate blocks | Session / weekday dominate; ATR>70 regular | Same |

Tip fire rate ~14/mo — similar to UK100 M15 tip denser than EURUSD M15 P2 (~8/mo). Prior Jan→Apr collapses to n=8 under ATR≤70 (HV winter/yen). Sep starve is intentional.

---

## 5. Performance

### 5.1 Primary tip (2026.05.01 → 2026.08.31)

| Setting | Value |
| --- | --- |
| Symbol / TF | USDJPY M15 |
| Magic | **26101828** |
| Geometry | SL100 / TP120 · RR **1.20** · BB **2.2** · CD **2** |
| Filters | 12–20 · skip Tue · ATR max **70** · AOS **off** |
| Deposit | 500 |
| Final balance | **505.99** |
| Net PnL | **+$5.99** (+1.2%) |
| n / WR / E_N | 56 / 48.2% / **+0.061R** |
| Containment | Fail-pause present; no equity-halt wipe observed |

### 5.2 Diagnostic windows

| Window | Final Δ | WR | E_N | Read |
| --- | ---: | ---: | ---: | --- |
| Tip May→Aug | **+$5.99** | 48.2% | +0.061R | Home tip viable · Stage 0 · EF prior ≪ 0 |
| YTD Jan→Oct | **+$17.99** | 51.5% | +0.132R | Stronger · still EF≤0 under prior |
| Prior Jan→Apr | +$1.20 | 50.0% | +0.10R | Starved n=8 — weak evidence |
| Long 2025→Oct | +$14.29 | 49.4% | +0.087R | Diluted by sparse 2025 + Jul |

**Interpretation:** Engine has a **modest meanrev edge on USDJPY when May–Jun cooperate**. Jul is the regime tax; Sep silence is the ATR gate. Expansion keep; not attach-ready; AIOS candidate later for Thu / Jul-like / sell-volume hygiene. Stage-1 blocked by **Leak prior vs thin BM** until measured costs.

### 5.3 Vs design probe

| | Probe (M15*) | Tester tip |
| --- | ---: | ---: |
| n | ~66 | 56 |
| WR | 57.6% | 48.2% |
| E_N | +0.267R | +0.061R |
| EF | +0.8 pp | −8.6 pp (prior Leak) |

Same geometry family; Tester much softer — expect this on tick friction / path dependency / Jul cluster. Do not overfit back to probe WR.

### 5.4 Expansion lens

| Question | Answer |
| --- | --- |
| Keep on asset list? | **Yes** — tip Stage 0 pass, geometry clean, gates healthy |
| Live replace EUR/AUD/UK? | **No** |
| AIOS now? | **No** — engine-only fingerprint first; native USDJPY L2 later |
| Main hygiene watches | **Thu** · **Jul** · **H14** · sell-volume without edge · Leak prior |
| Next evidence | Deal export → measured Leak/EF/MaxDD; optional BB2.0 fire-count alt; Jul skip cell |

---

## 6. Key metrics (scorecard snapshot)

### Balanced P0 · tip 2026.05→08.31 · magic 26101828

| Metric | Value |
| --- | ---: |
| RR / R_design / RR−R | 1.20 / 1.20 / ~0 (FIXED_RR) |
| BWR / WR / BM | 45.5% / **48.2%** / **+2.8 pp** |
| E_N | **+0.061R** |
| Leak prior / EF prior | 11.4 pp / **−8.6 pp** |
| n | 56 |
| PF (approx) | ~1.12 |
| expR / trade | +0.06R |
| Net PnL | **+$5.99** (+1.2%) |
| Side diagnosis | Tip **buy-led expectancy**; sell-heavy fire count |
| Hold fingerprint | Med win ~1.2h · session-bound (not overnight FX) |
| regime_filtered | **true** (12–20 + skip Tue + ATR≤70) |
| Live boundary | **Research only** · expansion keep · Stage 0 pass · Stage 1 OPEN |

### Supporting YTD (same geometry)

| Metric | YTD Jan→Oct |
| --- | ---: |
| WR / E_N / EF prior | 51.5% / +0.132R / **−5.4 pp** |
| Net PnL | **+$17.99** |
| Max loss streak | 7 |
| Soft month | Jul WR 33.3% |

### Sleeve ladder

| Sleeve | Magic | Status |
| --- | ---: | --- |
| **P0 balanced** | **26101828** | **chart sleeve · tip Stage 0 pass · EXPAND_CANDIDATE** |
| P0 RR1.25 alt | 26101829 | design prior only · not Tester-scored |
| P0 fire-count BB2.0 | 26101830 | design prior only · not Tester-scored |

---

## 7. Behavioural fingerprint (USDJPY M15 P0)

1. Class: **mean-rev entry · FIXED_RR exit** (same family as EUR M15 / UK100 / AAPL Balanced).  
2. **Session-bound** holds (med win ~1.2h tip) — closer to UK100 cash than EURUSD M15 overnight.  
3. ATR max **70** + session 12–20 + Tue skip define selectivity; BB-width deliberately OFF.  
4. Tip fires ~14 trades/month — denser than EUR M15 P2; prior winter starved under ATR.  
5. Structural soft pockets: **Thu**, **Jul**, **H14**, sell-volume without edge thickness.  
6. Tip / YTD star pockets: **Mon/Fri**, **H15 / H18–19**, **BUY expectancy**, **May–Jun**.  
7. Side leadership is **buy-led on expectancy** despite sell-heavy fire count — opposite of EUR M15 tip’s sell-led story.  
8. AOS OFF — fingerprint is pure engine; do not evaluate EUR/UK L2 pins here.  
9. Sep tip FRAGILE + zero fires — do not use as admission; ATR gate is the declared cut.  
10. Tester WR sits **far below** design probe — use blotter for keep/reject, probe for geometry design only.  
11. Stage-1 bottleneck is **Leak prior (11.4 pp) vs thin BM (+2.8 pp)** — measured c_R is mandatory before AIOS spend.

---

## 8. Locked geometry (reference)

| Parameter | Value |
| --- | --- |
| InpBBPeriod / InpBBDev | 20 / **2.2** |
| InpMaxLevels / InpMaxEntries | **1 / 1** |
| InpLotMode / Risk% | Risk% / **0.5** |
| InpSL_Points / InpTP_Points | **100 / 120** |
| Designed RR / BWR / Leak prior | **1.20 / 45.5% / 11.4 pp** |
| InpMaxSpread / CooldownBars | **25 / 2** |
| Session | **12:00–20:00** · **skip Tue** |
| ATR regime | ON · max **70** · min 0 |
| BB-width regime | **OFF** |
| InpAOS_Enable | **false** |
| InpMagic | **26101828** |

Preset: `Profiles/Tester/BMRG/USDJPY/BMRG-M15-USDJPY-6M-P0_balanced_chart.set`.

---

## 9. Recommended use

| Do | Don’t |
| --- | --- |
| Keep USDJPY on the **expansion asset list** | Treat as live EUR/AUD/UK replace |
| Score tip (May→Aug) as primary; YTD as support | Claim Stage-1 production on Leak **prior** alone |
| Read Jul / Thu / H14 softness as **regime** | Hard-reject the sleeve on Jul alone |
| Next: deal export → Leak/EF Stage-1; then native AIOS plan | Pin EUR/UK L2 models onto this sleeve |
| Watch Thu / Jul / sell-volume hygiene as AIOS features | Flip to trend geometry or Harvest RR without a new sleeve card |
| Keep ATR max declared when claiming G3 | Claim unfiltered cross-regime edge |
| Remember Tokyo session failed design probe | Re-open 02–12 without a new card |
| Note SL is yen-ATR-scaled (100) | Import EUR 300 / GBPJPY 160 floors |

---

## 10. One-line thesis

**USDJPY M15 BMRG is a London/NY-filtered G0 Bollinger mean-reversion fade (Balanced RR1.20 · BB2.2 · ATR≤70 · AOS OFF); on 2026.05→08 it realises WR 48.2% / E_N +0.06R / +$6 on $500 with Stage 0 pass but deeply negative EF under a 25pt Leak prior — suitable for expansion research ahead of measured-cost Stage-1 and a yen-native AIOS, not live attach, with Jul/Thu softness and Sep starve read as regime filtering until deal-scored EF.**
