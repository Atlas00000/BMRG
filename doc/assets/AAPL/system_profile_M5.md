# AAPL M5 — System Profile

**Asset:** Apple (AAPL CFD) · MT5 ticker **Apple** · **TF:** M5  
**Sleeve:** Balanced · TP > SL · **engine only (AOS OFF)**  
**Magic:** **26102011**  
**Preset:** `Profiles/Tester/BMRG/AAPL/BMRG-M5-AAPL-6M-Balanced_TPgtSL.set`  
**Profile date:** 2026-10-20  
**Evidence:** Tester `logs/20261020.log` · deposit **$500** · leverage 1:500 · every tick · ACCOUNT CURRENCY  
**Framework:** `doc/unified_edge_framework.md` · binding [`edge_framework.md`](./edge_framework.md)  
**Sibling (M15):** [`system_profile.md`](./system_profile.md) · Harvest candidate **26092501** — **do not mix sleeves**  
**Docs home:** [`doc/assets/AAPL/`](./README.md)

**Scope:** Research **asset-list expansion** (US equity CFD · M5 cash sleeve). **Not** a live replace for AUDUSD / EURUSD / M15 AAPL Harvest candidate. **Own AIOS:** [`aios_roadmap_M5.md`](./aios_roadmap_M5.md) — **P7 HITL ARMED** · `AAPL_5m_stack` · magic **26162017**.

**Do not mix** with M15 magics · EPG Apple presets · EUR/AUD L2 pins · root `system_profile.md`.

---

## 0. Evidence hierarchy

| Authority | Source |
| --- | --- |
| **Primary tip (preset intent)** | **2026.05.01 → 2026.10.19** · magic **26102011** · AOS OFF |
| **Supporting YTD** | **2026.01.01 → 2026.10.19** · regime-split diagnostic |
| **Supporting Feb→Oct** | **2026.02.01 → 2026.10.19** |
| **Long spanning** | **2025.01.01 → 2026.10.19** |
| **Design prior (not blotter)** | Ouroboros M5* probe in preset header · n≈100 · WR 51% · E_N ≈ +0.26R · EF≈+2.1 pp (prior cost model) |
| **Normative scoring** | [`edge_framework.md`](./edge_framework.md) |
| **Not admissible** | Live FT · treating Jan–Apr wipe as class death · Ouroboros probe as Stage-1 without Tester deal Leak · M15 Harvest as this sleeve |

### Cross-window scoreboard (journal · designed R = 1.47 · BWR = 40.4%)

| Window | Final | Δ | N | WR | BM | E_N | True-leak pass\* | Note |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- | --- |
| **May→Oct tip** | **544.50** | **+44.50** | **77** | **46.8%** | **+6.3 pp** | **+0.16R** | **no** | Primary expansion print |
| Feb→Oct | 509.45 | +9.45 | 124 | 39.5% | −0.9 pp | −0.02R | no | H1 drag |
| Jan→Oct | 498.03 | −1.97 | 145 | 38.6% | −1.8 pp | −0.05R | no | Flat / soft |
| **2025.01→2026.10** | **518.95** | **+18.95** | **289** | **40.1%** | −0.3 pp | ≈0R | no | Long span |
| Design probe (header) | — | — | ~100 | 51.0% | ~+10.6 pp | ~+0.26R | prior only | Stronger than Tester tip WR |

\*True Leak ≈ med open spread / SL ≈ **29 / 190 ≈ 15.3 pp** (long sample med spread ~27 → ~14.2 pp). Preset meta Leak **2.1 pp** is **inadmissible** as production Leak. Formal pass needs WR ≳ **BWR + true Leak ≈ 55%**.

**Stage 0 (tip):** n=77 · WR > BWR · E_N > 0 · TP > SL → **PASS** as expansion research tip. Stage 1 under measured Leak → **OPEN / Fragile** until deal export. Longer windows fail Stage 0 on WR/E_N — label **L3 regime**, not DROP of the tip sleeve.

---

## 1. System identity

| Field | Value |
| --- | --- |
| Full name | Bollinger Mean-Reversion Grid on Apple **M5** (Balanced TP>SL) |
| Short code | BMRG · AAPL M5 expansion |
| Primary class | **Mean reversion** (statistical deviation fade) |
| Secondary class | Grid / basket — **OFF** (G0 · MaxLevels=1 · MaxEntries=1) |
| Not | Trend-following, breakout, momentum-continuation, EPG pullback |
| Market / TF | **Apple**, **M5** · US cash RTH filter |
| Execution | Closed-bar signal (shift 1) → market · fixed **1.0** lot (`VOLUME_MIN≈1`) |
| Realisation | **`FIXED_RR_FADE`** (TP/SL; material overnight `OTHER`) |
| Regime posture | **`regime_filtered=true`** (RTH 14–20 · skip Tue · ATR 24–98 · BBw 0.30–2.00%) |

### Strategy-class statement

On Apple M5 the EA **fades excursions** past ±kσ Bollinger bands back toward the short-horizon mid-band — same **mean-reversion** class as AAPL M15 / FX Balanced. **Not** a trend system.

It should win when Apple **mean-reverts inside US RTH** often enough that:

```
WR > BWR = 1 / (1 + R)
E_N = (R + 1)(WR − BWR) > 0
BM = WR − BWR > 0
EF = BM − Leak > 0   (after measured costs)
```

With designed **RR ≈ 1.47** (TP 280 / SL 190) → **BWR ≈ 40.4%**. Soft research targets after **true** Leak (~15 pp): WR ≳ **55%**, BM ≥ **+5–10 pp** gross, E_N ≥ **+0.10R** on the tip; prefer EF > 0 after deals.

It loses when price **band-rides** (earnings / trend days / HV stretch) into the hard SL — classic meanrev failure. Soft **Jan–Apr 2026** and fragile **Jul** are read first as **regime mismatch**, not class failure.

**Why M5 geometry ≠ M15:** M5 ATR p50 ≈ **63 pts** → SL **190** ≈ 3×ATR. Do **not** import M15 SL 300/320 onto M5.

---

## 2. Edge profile

### 2.1 Theoretical edge (meanrev · Balanced RR≈1.47)

| Concept | Designed | Implication |
| --- | ---: | --- |
| Class | Mean reversion fade | Edge = **WR above BWR**, with thicker R than Harvest RR1.25 |
| RR / BWR | **1.47 / 40.4%** | Lower BWR than Harvest M15 (44.4%) — more room if WR soft |
| Side of edge | **Mixed WR + R** | Tip shows R_real ~**1.75** > RR when winners extend (`OTHER`) |
| Soft WR after true Leak | ≳ **55%** | Tip WR 46.8% clears BWR but **not** true Leak |
| AOS | **OFF** | Pure engine extract; Apple M5 AIOS later |

**Why Balanced on M5:** Hit-rate alone is hard under fat equity CFD spreads; RR>1 lowers BWR while keeping TP>SL. Sleeve is still meanrev — do not “fix” by converting to trend RR.

### 2.2 Structural win path

| Layer | Role on Apple M5 |
| --- | --- |
| Signal | Long ≤ lower BB; short ≥ upper BB · **BBDev 2.5** |
| Regime gates | ATR **24–98** pts · BBw **0.30–2.00%** (wider than M15 max 1.50 — M5 width units) |
| Session | US RTH ≈ **14:00–20:00** · **skip Tue** |
| Hygiene | MaxSpread **40** · cooldown **6** bars (M5 clock) |
| Exit | Fixed TP +RR or SL −1 designed SL |
| Risk G0 | One event · fixed lot 1.0 · daily/equity containment |

### 2.3 Class metric targets (research soft bars)

| Metric | Soft target (expansion) | Hard worry |
| --- | --- | --- |
| WR | > 40.4%; after true Leak prefer ≳ **55%** | Persistently ≤ BWR on tip **and** W20 |
| R | ≈ 1.47 (±20% with gap noise) | R ≪ RR without WR lift |
| BM | > 0; prefer ≥ +5 pp on tip | BM ≤ 0 on tip |
| E_N | > 0; prefer ≥ +0.10R on tip | ≤ 0 on tip W20 and calendar tip months |
| MaxDD ($500 / 1 lot) | soft under ~8–10% on tip | Path DD ≫ tip earnings |
| Soft stress month | WR may &lt; BWR (Jul-like) | Multi-month H1 cluster → L3, not auto DROP tip |

### 2.4 Realised edge — primary tip (2026.05 → 2026.10.19)

| Metric | Value | vs target |
| --- | ---: | --- |
| n | **77** | Usable Stage-0 tip |
| WR | **46.8%** | > BWR 40.4%; **&lt; true-leak bar ~55%** |
| BM (des BWR) | **+6.3 pp** | Gross OK |
| E_N | **+0.16R** | Clears +0.10R soft |
| R_real | ~**1.75** | Above designed RR (fat wins / OTHER) |
| PnL | **+$44.50** (+8.9%) | Confirms direction of E_N |
| True Leak | ~**15.3 pp** | Dominates Stage-1 |
| EF_proxy (BM − true Leak) | ~**−9 pp** | Negative — Fragile / fail until costs cut or WR lifts |
| MaxDD (path) | ~**5.0%** | Contained on tip |
| PF | ~**1.54** | |

**Leak / EF:** journal gross only. Preset Leak 2.1 pp must not be used for Robust claims.

### 2.5 Regime / transfer caveat

Tip H1 meanrev was **MATCH** in Ouroboros notes; Tester shows **May–Jun strong**, **Jul fragile**, **Aug–Oct soft-positive**. **Jan–Apr 2026** is hostile (WR ~25–33%). Longer windows dilute tip — expected **L3 regime leak**, not proof the fade class is wrong. Do not reject M5 Balanced from the expansion list on Jan→Oct alone.

---

## 3. Trade profile

Evidence: tip n=77 · supporting Jan→Oct n=145 · long n=289.

### 3.1 Winners (tip · n=36 · 46.8%)

- Fade completes to TP (**29** clean TP on tip) or extends via `OTHER`.  
- Med hold of winners longer than losers (overnight inventory common — **43/77** holds ≥12h on tip).  
- **BUY** carries tip WR (**54%**, +20.8); **SELL** lower WR (**39%**) but still net positive (+26.2) via larger wins.  
- Best DOW on tip: **Mon** (WR 62%) · **Thu** strong $ (+30).

### 3.2 Losers (tip · n=41 · 53.2%)

- Continuation into SL (**36** clean SL) or adverse `OTHER`.  
- Faster stops than winners on average.  
- Soft DOW on longer spans: **Wed** (Jan–Oct WR 29%, −27.5).  
- **Jul** is the tip stress month: WR **20%** but net still **+$6.6** (asymmetric payoff) — expectancy fragile, not wiped.

### 3.3 Exit mix (tip)

| Exit | Count | Share |
| --- | ---: | ---: |
| Take profit | 29 | 37.7% |
| Stop loss | 36 | 46.8% |
| OTHER (gap/slip path) | 12 | 15.6% |

→ Realisation stays **`FIXED_RR_FADE`** with equity overnight noise.

### 3.4 Side balance

| Side | Tip n / WR / net | Jan–Oct n / WR / net |
| --- | --- | --- |
| BUY | 39 / **54%** / **+20.8** | 76 / 42% / −0.6 |
| SELL | 38 / 39% / **+26.2** | 69 / 35% / +2.9 |

Tip: both sides contribute $. Full YTD: BUY flattens — H1 buy wound (regime), not a permanent sell-only engine.

### 3.5 Weekday (entry) — Tue filtered · tip

| DOW | n | WR | Net |
| --- | ---: | ---: | ---: |
| Mon | 16 | **62%** | +12.5 |
| Tue | 0 | — | filtered |
| Wed | 25 | 40% | −0.6 |
| Thu | 19 | 47% | **+30.0** |
| Fri | 17 | 41% | +5.0 |

### 3.6 Streaks / path (tip)

W20 path: early tip WR ~65% → mid-summer dip (W20 E_N min ~**−0.51R**) → finish WR ~50% / E_N ~**+0.24R**. MaxDD tip ~5%; Jan–Oct path MaxDD ~9%; long ~10.8%.

---

## 4. Rolling windows

### 4.1 Calendar months (shared tip months · from Jan–Oct run)

| Month | n | WR | E_N | Net | Flag |
| --- | ---: | ---: | ---: | ---: | --- |
| 2026-01 | 21 | 33% | −0.18R | −10.9 | << regime |
| 2026-02 | 17 | 24% | −0.42R | −14.2 | << |
| 2026-03 | 18 | 33% | −0.18R | −9.2 | << |
| 2026-04 | 12 | 25% | −0.38R | −10.3 | << |
| **2026-05** | 12 | **67%** | **+0.65R** | **+14.8** | ok |
| 2026-06 | 12 | 50% | +0.24R | +6.0 | ~ |
| 2026-07 | 15 | 20% | −0.51R | +6.6 | << WR / OK $ |
| 2026-08 | 15 | 53% | +0.32R | +12.9 | ~ |
| 2026-09 | 17 | 47% | +0.16R | +3.9 | ~ |
| 2026-10 | 6 | 50% | +0.24R | +2.8 | ~ thin |

### 4.2 Quarters

| Slice | Tip (May–Oct) | Jan–Oct |
| --- | --- | --- |
| Jan–Mar | — | n=56 WR 30% · −34 · E_N −0.25R |
| Apr–Jun | n=24 WR **58%** · +21 · E_N **+0.44R** | n=36 WR 47% · +10 |
| Jul–Sep | n=47 WR 40% · +23 · E_N ≈0 | same months |
| Oct | n=6 WR 50% · +2.8 | thin |

### 4.3 Rolling trade W20 (expectancy)

| Window | Tip path | Jan–Oct path |
| --- | --- | --- |
| Avg WR / E_N | ~44% / **+0.08R** | ~40% / **−0.02R** |
| Min E_N | ~**−0.51R** (summer) | ~**−0.51R** |
| End state | WR ~50% · E_N ~**+0.24R** | recovers to ~+0.24R |

### 4.4 Year split (long window)

| Year | n | WR | Net | E_N |
| --- | ---: | ---: | ---: | ---: |
| 2025 | 144 | 41.7% | +26.2 | +0.03R |
| 2026 | 145 | 38.6% | +2.4 | −0.05R |

### 4.5 Frequency

| Metric | Tip | Jan–Oct | Long |
| --- | ---: | ---: | ---: |
| Span | ~5.5 months | ~9.5 months | ~22 months |
| Closed trades | 77 | 145 | 289 |
| Trades / 30d | ~14 | ~15 | ~13 |

Much higher frequency than AAPL M15 Harvest (~3/month) — M5 + wider BBw max.

---

## 5. Performance

### 5.1 Primary tip (2026.05.01 → 2026.10.19)

| Setting | Value |
| --- | --- |
| Symbol / TF | Apple M5 |
| Magic | **26102011** |
| Geometry | SL190 / TP280 · RR≈1.47 |
| AOS | Off |
| Deposit | 500 |
| Final balance | **544.50** |
| Net PnL | **+44.50** (+8.9%) |
| MaxDD (path) | ~5.0% |
| Containment | No equity-halt observed in scored path |

### 5.2 Cross-window context (expansion lens)

| Window | PnL | Read |
| --- | ---: | --- |
| May→Oct tip | **+44.50** | Primary KEEP-shaped Stage-0 |
| Feb→Oct | +9.45 | Diluted |
| Jan→Oct | −1.97 | H1 tax ≈ tips earnings |
| 2025→2026.10 | +18.95 | Long keep thin; 2025 carries |

**Interpretation:** Mid/late-2026 tip engine is healthy on gross E_N; early-2026 and true Leak prevent production claims. Expansion keep tip sleeve; do not attach.

### 5.3 vs M15 Harvest candidate

| | M5 Balanced (this) | M15 Harvest (pool candidate) |
| --- | --- | --- |
| Magic | 26102011 | **26092501** |
| Tip $ / WR | +45 / 47% | +21 / 75% (shorter tip sample) |
| Frequency | High (~14/30d) | Low (~3/30d) |
| True Leak | ~15 pp | ~9 pp |
| Pool role | **WATCH / tip research** | **KEEP candidate** |

---

## 6. Key metrics (scorecard snapshot)

### Tip · 2026.05→2026.10 · magic 26102011

| Metric | Value |
| --- | ---: |
| RR / R_real / RR−R | 1.47 / ~1.75 / R ≥ RR (noise OK) |
| BWR / WR / BM | 40.4% / **46.8%** / **+6.3 pp** |
| E_N | **+0.16R** |
| n | 77 |
| PF (approx) | ~1.54 |
| expR / trade | +0.32 |
| True Leak | ~15.3 pp |
| EF_proxy | **&lt; 0** |
| MaxDD | ~5.0% |
| Side diagnosis | Mixed WR+R meanrev · tip BUY WR ahead |
| regime_filtered | **true** |
| Live boundary | **Research only** · expansion · not M15 replace |

### Jan→Oct · same magic

| Metric | Value |
| --- | ---: |
| WR / E_N | 38.6% / −0.05R |
| Net | −$1.97 (path ~+$2) |
| MaxDD | ~9.0% |
| Verdict | Regime-diluted · L3 label |

---

## 7. Behavioural fingerprint (AAPL M5 Balanced)

1. Class: **mean-rev entry · FIXED_RR exit** (Balanced RR≈1.47).  
2. Tip earns; H1 2026 and true Leak (~15 pp) are the main drag.  
3. Overnight-heavy inventory — gap/`OTHER` is part of the equity CFD fingerprint.  
4. Frequency ≫ M15 Harvest; selectivity still ATR/BBw/RTH gated.  
5. Soft pockets: **Jan–Apr**, **Jul WR**, **Wed** on long spans.  
6. Strong pockets: **May**, **Mon**, tip path repair into Oct.  
7. AOS OFF — do not score EUR/AUD L2 on this magic.  
8. Preset meta Leak 2.1 pp must be replaced by deal Leak before Robust.

---

## 8. Locked geometry (reference)

| Parameter | Value |
| --- | --- |
| InpBBPeriod / InpBBDev | 20 / **2.5** |
| InpSL_Points / InpTP_Points | **190 / 280** |
| Designed RR / BWR / meta Leak | ≈1.47 / 40.4% / 2.1 pp (meta only) |
| InpMaxLevels / InpMaxEntries | 1 / 1 |
| InpLotMode / InpLot | Fixed / **1.0** |
| InpMaxSpread / CooldownBars | **40** / **6** |
| Session | **14:00–20:00** · skip Tue |
| ATR regime | **24–98** pts ON |
| BB-width regime | **0.30–2.00%** ON |
| InpMagic | **26102011** |
| InpAOS_Enable | **false** |

Preset: `Profiles/Tester/BMRG/AAPL/BMRG-M5-AAPL-6M-Balanced_TPgtSL.set`.

---

## 9. Recommended use

| Do | Don’t |
| --- | --- |
| Keep M5 Balanced on **expansion research** list (tip Stage-0) | Treat as live replace or M15 Harvest swap |
| Score with **true Leak ~15 pp** | Use preset Leak 2.1 as production bar |
| Read Jan–Apr / Jul as **regime mismatch (L3)** | Hard-DROP the tip sleeve on Jan→Oct alone |
| Deal export → EF / MaxDD Stage-1 before AIOS | Pin EUR/AUD L2 or change SL/TP as first fix |
| Optional later: Wed / H1 skip AIOS vs this baseline | Mix magics with **26092501** candidate |

---

## 10. One-line thesis

**Apple M5 BMRG Balanced (SL190/TP280 · RR≈1.47 · magic 26102011) is a RTH-filtered G0 Bollinger mean-reversion fade; on May→Oct 2026 it realises gross E_N +0.16R / +$45 with H1 2026 regime tax on longer rolls and true Leak ~15 pp blocking Stage-1 — suitable for expansion research beside the M15 Harvest candidate, not live attach, AIOS only after deal-scored EF.**
