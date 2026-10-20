# JP225 / JPN225 M5 — System Profile

**Asset:** JP225 (Nikkei) · MT5 ticker **JPN225** · **TF:** M5  
**Sleeve:** Growth P0 · **engine only (AOS OFF)**  
**Magic:** **26101906**  
**Preset:** `MQL5/Profiles/Tester/BMRG/JP225/BMRG-M5-JP225-6M-P0_growth_chart.set`  
**Also:** `Presets/` mirror if present  
**Profile date:** 2026-10-20  
**Evidence:** Tester `logs/20261020.log` · JPN225 M5 · magic **26101906** · deposit **$500** · every tick · TP/SL closes · `blotter/archive/JP225-M5-P0-REVIEW/`  
**Framework:** `doc/unified_edge_framework.md` · binding [`edge_framework.md`](./edge_framework.md) · Ouroboros meanrev H1  
**Sibling (M15):** [`system_profile.md`](./system_profile.md) · magic **26101904** / research OS **26151907** — **do not mix sleeves**

**Scope:** Research **asset-list expansion** (JP Nikkei CFD · M5 cash sleeve). **Not** a live replace for AUDUSD / EURUSD / UK100 / DE40 / JP225 **M15** research OS. **Own AIOS:** [`aios_roadmap_M5.md`](./aios_roadmap_M5.md) · P0 stubs frozen 2026-10-20.

**Do not mix** with M15 `JPN225stack` (`26151907`) · M15 May∨Jul L2det · root `system_profile.md` · foreign L2 pins.

---

## 0. Evidence hierarchy

| Authority | Source |
| --- | --- |
| **Primary tip blotter** | **2026.05.01 → 2026.10.19** · magic **26101906** · n=**94** · WR **41.5%** · E_N **+0.245R** · EF_prior **+4.9 pp** · final **535.34** · Δ **+$35.34** |
| **YTD / long-in-year** | **2026.01.01 → 2026.10.19** · n=**130** · WR **38.5%** · E_N **+0.154R** · EF_prior **+1.8 pp** · final **530.06** · Δ **+$30.06** |
| **Design probe (preset card)** | n≈**107** · WR≈**38.3%** · E_N≈**+0.15R** · EF≈**+1.7 pp** (cost prior 2500 · ATR band p40–p75) |
| **Home OFFHOME pocket (counterintuitive vs M15)** | May+Jun FRAGILE + Jul/Oct MISMATCH · n=**60** · WR **50%** · E_N **+0.50R** · EF **+13.4 pp** |
| **Stress MATCH pocket** | Aug–Sep MATCH · n=**34** · WR **26.5%** · E_N **−0.21R** · EF **−10.2 pp** |
| **Regime map** | Ouroboros H1 meanrev · May–Jun **FRAGILE** · Jul/Oct **MISMATCH** · Aug–Sep **MATCH** |
| **OPEN / missing** | Deal-measured Leak · hold-time / hour cells · MaxDD equity path export · formal W15/W20 path |
| **Not admissible** | Live FX/EU OS · treating MATCH-month fail as class death · M15 pins on M5 · probe as sole Stage-1 · live capital admit |

### Cross-window scoreboard (FIXED_RR design R=2.00 · Leak prior **3.3 pp**)

| Window | Final | Δ vs $500 | N (TP+SL) | WR | BM | E_N | EF_prior | Note |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| **May→Oct tip ★** | **535.34** | **+35.34** | **94** | **41.5%** | **+8.2 pp** | **+0.245R** | **+4.9 pp** | Primary tip |
| Jan→Oct 19 | 530.06 | +30.06 | 130 | 38.5% | +5.1 pp | +0.154R | +1.8 pp | YTD |
| OFFHOME (F/M tip months) | — | — | 60 | **50.0%** | **+16.7 pp** | **+0.50R** | **+13.4 pp** | Carries book |
| MATCH Aug–Sep | — | — | 34 | 26.5% | −6.9 pp | −0.21R | −10.2 pp | Regime tax |
| Design probe | — | — | ~107 | ~38.3% | ~+5.0 pp | ~+0.15R | ~+1.7 pp | Prior only |

Leak prior = c_R≈2500/25000 → Leak = c_R/(R+1) ≈ **3.3 pp**. Journal open spread med ≈ **1400** pts ≪ live ≈**2300** — **do not** use journal alone as Stage-1 Leak forever. Prefer deal-exported Leak before capital gates.

**Stage 0 tip:** n≫30 · WR > BWR · E_N > 0 · TP > SL → **PASS**.  
**Stage 1 tip (prior Leak):** EF **+4.9 pp** → **PASS** under prior. Measured Leak still **OPEN** on M5.

---

## 1. System identity

| Field | Value |
| --- | --- |
| Full name | Bollinger Mean-Reversion Grid on JP225/JPN225 **M5** |
| Short code | BMRG · JP225 M5 expansion |
| Primary class | **Mean reversion** (statistical deviation fade) |
| Secondary class | Grid / basket — **OFF** (G0 · MaxLevels=1 · MaxEntries=1) |
| Not | Trend-following, breakout, momentum-continuation, M15 OS clone |
| Market / TF | **JPN225**, **M5** · London cash sleeve (Tokyo 02–09 rejected on probe) |
| Execution | Closed-bar signal (shift 1) → market · lot **0.1** (broker `VOLUME_MIN`) |
| Realisation | **`FIXED_RR_FADE`** (TP/SL dominate) |
| Regime posture | **`regime_filtered=true`** (session 08–17 + skip Tue + ATR **band** p40–p75) |

### Strategy-class statement

On JPN225 M5 the EA **fades excursions** past ±kσ Bollinger bands back toward the short-horizon mid-band — same **mean-reversion** class as JP225 M15 / DE40 / UK100 / FX Growth sleeves. **Not** a trend system.

It should win when Nikkei **mean-reverts inside the London cash session** often enough that:

```
WR > BWR = 1 / (1 + R)
E_N = WR × (R + 1) − 1 > 0
BM = WR − BWR > 0
EF = BM − Leak > 0   (after honest costs)
```

With designed **RR = 2.00** → **R = 2.00** → **BWR = 33.3%**. Soft research targets after Leak prior (~3.3 pp): WR ≳ **38–42%**, BM ≥ **+5–8 pp**, E_N ≥ **+0.15R** on tip; prefer EF > 0.

It loses when price **band-rides** (Nikkei impulse, risk-off trend days, hostile cells) into the hard SL — classic meanrev failure. Soft calendar months are read first as **regime / TF mismatch**, not class death.

**Critical TF caveat:** On **M15**, MATCH months carry the book and OFFHOME (May FRAGILE / Jul MISMATCH) tax EF. On **M5**, the blotter **flips**: OFFHOME pays and MATCH Aug–Sep fail. Any future M5 AIOS must use **M5-native** bad cells — never import M15 `May∨Jul` / MATCH-protect pins blindly.

---

## 2. Edge profile

### 2.1 Theoretical edge (meanrev · Growth RR=2.00)

| Concept | Designed | Implication |
| --- | ---: | --- |
| Class | Meanrev fade | Edge = **hit-rate above BWR**, with **thick R** to clear fat spread |
| Geometry | SL **25000** / TP **50000** pts | TP > SL always (hard rule) |
| Designed RR / R | **2.00** | Not Balanced 1.0–1.5 · not Harvest |
| BWR | **33.3%** | Much lower than Harvest 50% — WR room after Leak |
| Side of edge | **Mixed WR + fat R** | R=2.0 is required so modest WR still clears Leak |
| Leak prior | ~**3.3 pp** (c_R≈2500/25000 / (R+1)) | Live spread ≈**2300** · RT cost prior ≈**2500** pts |
| Soft research WR | ≳ **38–42%** after Leak prior | Probe ~38% · tip blotter **41.5%** |
| Selectivity (P0) | BB **2.5** · CD **3** · ATR **7610–11285** | Band cuts chop + FRAGILE HV; CD denser than M15 |
| Fade | **OFF** on M5 P0 | Unlike M15 P1 wrLift |
| AOS | **OFF** | Pure engine extract; M5 AIOS later |

**Why RR=2.00 (not ≤1.5):** Under fat Nikkei spread, M5 design card reports **viable_count=0** for RR≤1.5 (all EF&lt;0). Growth RR=2.0 is the only geometry that clears Leak at design. Thinning SL raises `c_R` and destroys EF — never “fix” Leak by shrinking SL.

**Why ATR band (min 7610 ≈p40 · max 11285 ≈p75) ON:** Declared regime filter (Gate G3). Max-only alone left EF&lt;0 on probe; band cuts low-vol chop **and** May/Jun FRAGILE high-vol tails.

**Why BBDev=2.5 (vs M15 2.3):** M5 noise denser; wider bands reduce false extremes.

**Why London 08–17 · skip Tue:** Same cash sleeve as M15 expansion; Tokyo open rejected on probe.

### 2.2 Structural win path

| Layer | Role on JP225 / JPN225 M5 |
| --- | --- |
| Signal | Long ≤ lower BB; short ≥ upper BB on closed M5 · **BBDev 2.5** |
| Regime gates | ATR **band 7610–11285** ON · BB-width **OFF** |
| Session | London cash **08:00–17:00** server · **skip Tue** |
| Entry hygiene | MaxSpread **3000** (must clear live ≈2300) · cooldown **3** bars |
| Exit | Fixed TP **+2.0R** or SL **−1R** (distance in points) |
| Risk G0 | One event · lot **0.1** · exposure / daily-loss containment |
| Containment | Loss-streak pause (3) · fail pause · daily loss % · equity halt |

### 2.3 Class metric targets (research soft bars)

| Metric | Soft target (expansion) | Hard worry |
| --- | --- | --- |
| WR | > 33.3% (BWR); prefer ≥ **38–42%** after Leak prior | Persistently ≤ BWR on tip + W20 |
| R (realised) | ≈ 2.00 (RR−R small) | R ≪ RR without WR compensation |
| BM | > 0; prefer ≥ **+5 pp** on tip | BM ≤ 0 on primary tip |
| E_N | > 0; prefer ≥ **+0.15R** on tip | ≤ 0 on tip and W20 |
| EF | > 0 after measured Leak | Persistently ≤ 0 with honest costs |
| Soft stress months | WR can dip ≪ BWR (MATCH on M5; hostile cells) | Cluster of **paying** OFFHOME months also ≪ BWR → revisit geometry |
| MaxDD (0.1 lot / $500) | soft under ~15% research | Equity-halt territory |
| Fire count tip | n ≥ **30** (Stage 0) | Starvation (ATR band + session too tight) |

### 2.4 Realised edge — tip blotter (2026.05.01 → 2026.10.19)

| Metric | Value | vs target |
| --- | ---: | --- |
| n (TP+SL closes) | **94** | Usable Stage-0 |
| Side (buy/sell) | **~45 / 49** (balanced-ish) | Not one-side theatre |
| WR | **41.5%** | Clears BWR 33.3%; ≥ soft bar |
| Designed R / BWR | **2.00** / 33.3% | On-thesis · realised R med **2.00** |
| BM | **+8.2 pp** | Soft bar cleared |
| E_N | **+0.245R** | Clears +0.15R soft bar |
| EF (Leak prior 3.3 pp) | **+4.9 pp** | Preferred under prior |
| PnL (tester final) | **+$35.34** (+7.1%) | Equity confirms E_N |
| Final balance | **535.34** | Deposit 500 |
| MaxDD proxy | **~3.4%** | Soft |
| tp_lt_sl | **0** | Geometry hard rule OK |

**Probe vs Tester tip:** Design ~107 / 38% / +0.15R → tip blotter 94 / 41.5% / +0.245R — same direction, tip stronger.

### 2.5 Realised edge — YTD & regime slices

| Slice | n | WR | BM | E_N | EF_prior |
| --- | ---: | ---: | ---: | ---: | ---: |
| Jan→Oct 19 | 130 | 38.5% | +5.1 pp | +0.154R | +1.8 pp |
| May→Oct tip | 94 | 41.5% | +8.2 pp | **+0.245R** | **+4.9 pp** |
| OFFHOME (May–Jul+Oct) | 60 | **50.0%** | **+16.7 pp** | **+0.50R** | **+13.4 pp** |
| MATCH Aug–Sep | 34 | 26.5% | −6.9 pp | −0.21R | −10.2 pp |

YTD hides weak Feb/Apr and still clears Stage-0; tip is the expansion authority.

### 2.6 Regime / transfer caveat

Ouroboros H1 meanrev map vs Tester monthly closes (tip months + YTD):

| Month | Tag | n | WR | E_N | EF_prior | Read |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| 2026-01 | ? | 5 | 60% | +0.80R | +23.4 pp | Thin · strong |
| 2026-02 | ? | 10 | 20% | −0.40R | −16.6 pp | Soft pre-tip |
| 2026-03 | ? | 11 | 45% | +0.36R | +8.8 pp | OK |
| 2026-04 | ? | 10 | 10% | −0.70R | −26.6 pp | Soft pre-tip |
| 2026-05 | **FRAGILE** | 13 | 38% | +0.15R | +1.8 pp | Pays lightly |
| 2026-06 | **FRAGILE** | 17 | **47%** | **+0.41R** | **+10.4 pp** | **Pays** |
| 2026-07 | **MISMATCH** | 20 | **60%** | **+0.80R** | **+23.4 pp** | **Star month on M5** |
| 2026-08 | **MATCH** | 17 | 29% | −0.12R | −7.2 pp | **Regime tax** |
| 2026-09 | **MATCH** | 17 | 24% | −0.29R | −13.1 pp | **Regime tax** |
| 2026-10 | **MISMATCH** | 10 | 50% | +0.50R | +13.4 pp | Pays · incomplete tip |

**Read:** Edge concentrates in **Jun–Jul + Oct** (FRAGILE/MISMATCH). **Aug–Sep MATCH** explain soft expectancy — frame as **regime/TF mismatch**, not “M5 fade is broken.” Opposite of M15 MATCH-home story.

**Broker / ATR context (preset):** Point=0.01 · Digits=2 · live spread≈2300 · volume_min=0.1. M5 ATR pts: p40≈7614 · p50≈8472 · p75≈11285 · p90≈14830.

---

## 3. Trade profile

Primary evidence: tip May→Oct 2026 closes (n=94) · YTD n=130 for side/context. Hold-time / hour cells OPEN until deal export.

### 3.1 Winners

| | Tip May→Oct | YTD Jan→Oct | OFFHOME tip months |
| --- | ---: | ---: | ---: |
| Share | 39/94 (**41.5%**) | 50/130 (38.5%) | 30/60 (**50%**) |
| Typical exit | TP at **~+2.0R** | same | same |
| Character | Fade completes to fixed TP | same | densest Jul |

- Realisation stays **FIXED_RR** — winners are TP hits.  
- Best calendar pocket: **Jul MISMATCH** (WR **60%**, n=20) — strongest M5 month.  
- **Jun FRAGILE** and **Oct MISMATCH** also win-heavy relative to BWR.

### 3.2 Losers

| | Tip May→Oct | Stress MATCH | Soft pre-tip |
| --- | ---: | ---: | --- |
| Share | 55/94 (58.5%) | Aug 12 SL · Sep 13 SL | Feb 8 SL · Apr 9 SL |
| Typical exit | SL at **~−1R** | same | same |
| Character | Continuation / impulse into stop | MATCH months | Thin n · regime tax |

- Classic meanrev failure: band-ride into SL.  
- Soft pockets: **Aug–Sep MATCH** · **Feb/Apr** pre-tip.  
- Do **not** equate MATCH tag with “must protect” on M5 — here MATCH is the tax.

### 3.3 Exit mix (tip May→Oct)

| Exit | Count | Share | Read |
| --- | ---: | ---: | --- |
| Take profit (~+2.0R) | 39 | 41.5% | On-thesis |
| Stop loss (~−1R) | 55 | 58.5% | On-thesis (fat R compensates) |
| Other / non-1R | 0 parsed | — | FIXED_RR clean |

→ Realisation stays **`FIXED_RR_FADE`**. No MID-exit logic.

### 3.4 Side mix

| Window | BUY | SELL | Read |
| --- | ---: | ---: | --- |
| Tip (from monthly sums) | ~46 | ~48 | Near balanced |
| YTD | 59 | 71 | Mild SELL lean |

Unlike a one-side harvest story, M5 is two-sided fade. Side-conditioned WR OPEN until deal tape.

### 3.5 Open / hour / hold

| Item | Status |
| --- | --- |
| Hold-time win vs lose | OPEN (need deal export) |
| Hour / DOW cells | OPEN (Tue filtered by preset) |
| Overnight inventory | Expected low (session 08–17) — confirm on tape |
| Loss-streak containment | `InpMaxLossStreak=3` · fail pause 24 bars armed |

---

## 4. Rolling windows

### 4.1 Calendar months (closes)

| Month | n | WR | E_N | EF_prior | Regime note |
| --- | ---: | ---: | ---: | ---: | --- |
| 2026-01 | 5 | 60.0% | +0.80R | +23.4 pp | Thin strong |
| 2026-02 | 10 | 20.0% | −0.40R | −16.6 pp | Soft — regime tax |
| 2026-03 | 11 | 45.5% | +0.36R | +8.8 pp | OK |
| 2026-04 | 10 | 10.0% | −0.70R | −26.6 pp | Soft — regime tax |
| 2026-05 | 13 | 38.5% | +0.15R | +1.8 pp | FRAGILE · pays light |
| 2026-06 | 17 | 47.1% | +0.41R | +10.4 pp | FRAGILE · **pays** |
| 2026-07 | 20 | 60.0% | +0.80R | +23.4 pp | MISMATCH · **star** |
| 2026-08 | 17 | 29.4% | −0.12R | −7.2 pp | MATCH · tax |
| 2026-09 | 17 | 23.5% | −0.29R | −13.1 pp | MATCH · tax |
| 2026-10 | 10 | 50.0% | +0.50R | +13.4 pp | MISMATCH · pays |

### 4.2 Dedicated window averages

| Window | n | WR | BM | E_N | EF_prior | Final Δ |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| **May→Oct tip ★** | **94** | **41.5%** | **+8.2 pp** | **+0.245R** | **+4.9 pp** | **+$35.34** |
| Jan→Oct YTD | 130 | 38.5% | +5.1 pp | +0.154R | +1.8 pp | +$30.06 |
| OFFHOME tip months | 60 | 50.0% | +16.7 pp | +0.50R | +13.4 pp | — |
| MATCH Aug–Sep | 34 | 26.5% | −6.9 pp | −0.21R | −10.2 pp | — |

### 4.3 Rolling expectancy (path proxy from monthly sequence)

Formal W15/W20 trade-path not yet rebuilt from deal order. Monthly sequence already shows:

| Path view | Read |
| --- | --- |
| Expectancy through OFFHOME core | Jun–Jul–Oct carry · E_N +0.41…+0.80R |
| Soft dips | Aug–Sep MATCH (−0.12…−0.29R) · Feb/Apr pre-tip |
| Collapse risk | Not seen on tip aggregate; MATCH cluster is the known tax |

**Interpretation:** Soft MATCH months = **regime/TF mismatch taxes**. Paying OFFHOME expectancy stays clearly positive. Re-score W15/W20 after deal export if M5 AIOS starts.

### 4.4 Frequency & gates

| Metric | Tip May→Oct | YTD |
| --- | ---: | ---: |
| TP+SL closes | 94 | 130 |
| Trades / month (tip avg) | ~16 | ~13 |
| vs design probe | Probe n≈107 on ~6m tip-ish; tip blotter 94 — same order | — |
| Spread med (opens) | ~1050–1400 | 1400 |

ATR band is declared ON in preset (G3). Block counts OPEN until gate-log tally export.

### 4.5 Cost / spread note

| Source | Spread / cost |
| --- | --- |
| Journal open med | ≈ **1400** pts (Tester optimistic vs live) |
| Live broker prior | ≈ **2300** pts |
| Leak authority (now) | **prior 3.3 pp** until M5 deals |
| Never | Thin SL under fat Nikkei spread |

---

## 5. Performance

### 5.1 Primary tip window (2026.05.01 → 2026.10.19)

| Setting | Value |
| --- | --- |
| Symbol / TF | **JPN225** M5 |
| Magic | **26101906** |
| Geometry | SL**25000** / TP**50000** · RR **2.00** |
| Filters | 08–17 · skip Tue · ATR band **7610–11285** · BB **2.5** · CD **3** · Fade **OFF** · AOS **off** |
| Deposit | 500 |
| Final balance | **535.34** |
| Net PnL | **+$35.34** (+7.1%) |
| n / WR / E_N | 94 / **41.5%** / **+0.245R** |
| BM / EF_prior | +8.2 pp / **+4.9 pp** |
| MaxDD proxy | **~3.4%** |
| Geometry check | realised R med **2.00** · tp_lt_sl **0** |

### 5.2 vs design probe

| | Probe (card) | Tester tip May→Oct | Tester YTD |
| --- | ---: | ---: | ---: |
| n | ~107 | 94 | 130 |
| WR | ~38.3% | 41.5% | 38.5% |
| E_N | ~+0.15R | +0.245R | +0.154R |
| EF | ~+1.7 pp | +4.9 pp | +1.8 pp |

Directionally consistent; tip blotter does not falsify the probe.

### 5.3 vs JP225 M15 Growth (context only)

| | M5 (this) | M15 ([system_profile.md](./system_profile.md)) |
| --- | --- | --- |
| Magic (engine) | 26101906 | 26101904 |
| SL / TP | 25000 / 50000 | 23260 / 34890 |
| RR / BWR | **2.00** / 33.3% | 1.50 / 40.0% |
| ATR gate | band 7610–11285 | max 19670 |
| Fade | OFF | ON (P1) |
| Tip EF (prior/meas) | **+4.9** prior | M15 measured tip **+0.59** (engine); OS May∨Jul stronger |
| Regime home | **OFFHOME pays · MATCH fails** | **MATCH pays · OFFHOME taxes** |
| Research OS | none yet | **JPN225stack** 26151907 |
| Role | Expansion TF sleeve | Expansion TF sleeve + AIOS |

Different TF/geometry/regime fingerprint — **not** a replace; score separately; **never** share L2det pins.

### 5.4 Drawdown / stress

| Item | Status |
| --- | --- |
| MaxDD proxy (tip) | ~3.4% on 0.1 lot / $500 |
| Soft months | Aug–Sep MATCH · Feb/Apr — expected under M5 map |
| Equity halt | Not observed as book-killer on tip/YTD finals |

---

## 6. Key metrics (one-pager)

| Metric | Value | Authority |
| --- | ---: | --- |
| Class | Meanrev FIXED_RR_FADE | Identity |
| RR / BWR | **2.00** / **33.3%** | Design |
| Leak prior | **3.3 pp** | Cost policy until M5 deals |
| Primary tip | 2026.05→10.19 | Tester log |
| Final / PnL (tip) | **535.34** / **+$35.34** | Tester |
| n / WR / E_N / EF (tip) | **94** / **41.5%** / **+0.245R** / **+4.9 pp** | Closes |
| OFFHOME E_N | **+0.50R** | Closes |
| MATCH Aug–Sep E_N | **−0.21R** | Closes |
| Star month | **2026-07** WR 60% | Calendar |
| Soft months | Aug–Sep MATCH · Feb/Apr | Regime |
| Realised R / tp_lt_sl | **2.00** / **0** | Geometry |
| Journal spread med | ~1400 pts | Optimistic |
| Live spread prior | ~2300 pts | Broker |
| AOS | OFF | Preset |
| Pool | **EXPANSION_KEEP candidate** | Not live admit |

---

## 7. Explicit non-claims

- Not a live capital admit · not a replace for JP225 M15 / FX / UK / DE books.  
- Probe is a **design prior**, not the only Stage-1 blotter (tip closes are).  
- MATCH-month failure on M5 is **regime/TF mismatch**, not automatic DROP.  
- Journal spreads understate live Leak — prior 3.3 pp remains M5 authority until deals.  
- Do **not** borrow M15 `JPN225stack` / `May∨Jul` L2det on M5.  
- Do **not** thin SL under ~2300 live spread to “fix” Leak.

---

## 8. Status / next evidence

| Item | Status |
| --- | --- |
| Tip May→Oct engine | **DONE** (n94 · EF +4.9 prior) |
| M5 AIOS | **P0 stubs DONE** — see [`aios_roadmap_M5.md`](./aios_roadmap_M5.md) |
| Measured Leak (M5) | **OPEN** |
| Next | P1 tape · deal Leak · L2det CF on Aug–Sep MATCH (protect Jul) |

---

## 9. Related paths

| Path | Role |
| --- | --- |
| `Profiles/Tester/BMRG/JP225/BMRG-M5-JP225-6M-P0_growth_chart.set` | Engine P0 M5 |
| `blotter/archive/JP225-M5-P0-REVIEW/` | Scorecard · REVIEW |
| [`system_profile.md`](./system_profile.md) | M15 sibling |
| [`edge_framework.md`](./edge_framework.md) | Normative maths binding |
| [`README.md`](./README.md) | Asset index |
| [`aios_roadmap_M5.md`](./aios_roadmap_M5.md) | M5 AIOS plan |
| [`JP225_M5_AOS_BASELINE_v1.md`](./JP225_M5_AOS_BASELINE_v1.md) | OS baseline freeze |
| `Presets/JPN225stack.set` | **M15 only** research OS — do not load on M5 |
