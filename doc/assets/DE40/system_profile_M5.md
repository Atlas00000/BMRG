# DE40 M5 — System Profile

**Asset:** DE40 (Germany 40 / DAX) · MT5 ticker **DE30** · **TF:** M5  
**Sleeve:** Balanced P0 · **engine only (AOS OFF)**  
**Magic:** **26101903**  
**Preset:** `MQL5/Profiles/Tester/BMRG/DE40/BMRG-M5-DE40-6M-P0_balanced_chart.set`  
**Also:** `Presets/BMRG-M5-DE40-6M-P0_balanced_chart.set` (if mirrored)  
**Chart card:** `Profiles/Tester/BMRG/DE40/BMRG_M5_DE40_6M_chart_preset.md`  
**Profile date:** 2026-10-20  
**Evidence:** Tester `logs/20261020.log` · DE30 M5 · magic **26101903** · deposit **$500** · every tick · scored closes via TP/SL triggers · `blotter/archive/DE40-M5-P0/`  
**Framework:** `doc/unified_edge_framework.md` · binding [`edge_framework.md`](./edge_framework.md) · Ouroboros `research/assets/DE40/`  
**Sibling (M15):** [`system_profile.md`](./system_profile.md) · magic **26101902** — **do not mix sleeves**

**Scope:** Research **asset-list expansion** (EU index CFD · M5 cash sleeve). **Not** a live replace for AUDUSD / EURUSD / UK100 / DE40 M15 research OS. **Own AIOS:** [`aios_roadmap_M5.md`](./aios_roadmap_M5.md) — **P7 HITL ARMED** · `DE40_5m_stack` · magic **26151907**.

**Do not mix** with M15 DE40stack (`26141907`) · root `system_profile.md` · AUD / EUR / UK live magics.

---

## 0. Evidence hierarchy

| Authority | Source |
| --- | --- |
| **Primary blotter (current log)** | **2026.01.01 → 2026.08.31** · magic **26101903** · n_closes=**168** · final **850.64** · PnL **+$350.64** |
| **Design tip core (inside primary)** | **2026.05 → 08** · n=**93** · WR **57.0%** · E_N **+0.282R** · EF_prior **+5.5 pp** |
| **Home MATCH pocket** | **2026.06 → 08** · n=**75** · WR **60.0%** · E_N **+0.350R** · EF_prior **+8.6 pp** |
| **Design prior (not blotter)** | Ouroboros M5* probe · n≈**141** · WR **54.6%** · E_N **+0.229R** · EF≈**+3.2 pp** (ATR≤2380 · cost prior 1100 pts) |
| **Regime map** | Ouroboros H1 meanrev · Jun–Aug MATCH · **May MISMATCH** · **Sep–Oct FRAGILE** · live 30d FRAGILE |
| **Tip May→Oct (P1)** | **2026.05.01 → 2026.10.19** · n=**123** · WR **53.7%** · E_N **+0.207R** · EF_prior **+2.2 pp** · final **707.76** |
| **OPEN / missing** | Deal-measured Leak · MaxDD path export |
| **Not admissible** | Live FX/UK OS magics · treating Feb soft or May MISMATCH as class death · probe as Stage-1 · claiming multi-year depth (broker from **2025.06.05**) · scoring M5 as M15 replace |

### Cross-window scoreboard (FIXED_RR design R=1.25 · Leak prior **7.0 pp**)

| Window | Final | Δ vs $500 | N (TP+SL) | WR | BM | E_N | EF_prior | Note |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| **Jan→Aug 2026 (log)** | **850.64** | **+350.64** | **168** | **57.1%** | **+12.7 pp** | **+0.286R** | **+5.7 pp** | Primary blotter |
| Pre Jan→Apr | — | — | 75 | 57.3% | +12.9 pp | +0.290R | +5.9 pp | Feb soft inside |
| **May→Aug tip core** | — | — | **93** | **57.0%** | **+12.5 pp** | **+0.282R** | **+5.5 pp** | Design tip months present |
| **Jun→Aug MATCH** | — | — | **75** | **60.0%** | **+15.6 pp** | **+0.350R** | **+8.6 pp** | Home sleeve |
| Design probe M5* | — | — | ~141 | 54.6% | +10.2 pp | +0.229R | +3.2 pp | Prior only |
| **Tip May→Oct** | **707.76** | **+207.76** | **123** | **53.7%** | **+9.2 pp** | **+0.207R** | **+2.2 pp** | P1 authority |
| Sep–Oct alone | — | — | 29 | 44.8% | +0.4 pp | ≈0R | −7.0 pp | FRAGILE dilutes tip |

Leak prior = c_R≈1100/7000 → Leak = c_R/(R+1) ≈ **7.0 pp**. Journal open spread p50 ≈ **84** pts ≪ live ≈**1020** — **do not** use journal as Stage-1 Leak. Replace with deal-exported Leak before production gates.

**Stage 0 (Jan–Aug / May–Aug):** n≫30 · WR ≫ BWR · E_N ≫ 0 · TP > SL → **PASS** as expansion research. Stage 1 tip EF under **measured** Leak still **OPEN** until May→Oct + deals.

---

## 1. System identity

| Field | Value |
| --- | --- |
| Full name | Bollinger Mean-Reversion Grid on DE40/DE30 **M5** |
| Short code | BMRG · DE40 M5 expansion |
| Primary class | **Mean reversion** (statistical deviation fade) |
| Secondary class | Grid / basket — **OFF** (G0 · MaxLevels=1 · MaxEntries=1) |
| Not | Trend-following, breakout, momentum-continuation, scalping theatre |
| Market / TF | **DE30** (DE40), **M5** · Frankfurt / London cash sleeve |
| Execution | Closed-bar signal (shift 1) → market · lot **0.1** (broker `VOLUME_MIN`) |
| Realisation | **`FIXED_RR_FADE`** (TP/SL dominate) |
| Regime posture | **`regime_filtered=true`** (session 08–17 + skip Tue + ATR max ≈ M5 p75) |

### Strategy-class statement

On DE40 M5 the EA **fades excursions** past ±kσ Bollinger bands back toward the short-horizon mid-band — same **mean-reversion** class as DE40 M15 / UK100 / FX Balanced. **Not** a trend system.

It should win when DAX **mean-reverts inside the cash session** often enough that:

```
WR > BWR = 1 / (1 + R)
E_N = WR × (R + 1) − 1 > 0
BM = WR − BWR > 0
EF = BM − Leak > 0   (after measured costs)
```

With designed **RR = 1.25** → **R ≈ 1.25** → **BWR = 44.4%**. Soft research targets after Leak prior (~7.0 pp — still fat DE30 spread, milder than M15’s 9.8 pp because SL is wider): WR ≳ **54–58%**, BM ≥ **+10–13 pp**, E_N ≥ **+0.20R** on the home tip; prefer EF > 0.

It loses when price **band-rides** (EU equity impulse, risk-off trend days, high-vol **FRAGILE** cells) into the hard SL — classic meanrev failure. Soft months (**Feb**, **May MISMATCH**, soft **Jun**) are read first as **regime mismatch**, not class failure.

---

## 2. Edge profile

### 2.1 Theoretical edge (meanrev · Balanced RR=1.25)

| Concept | Designed | Implication |
| --- | ---: | --- |
| Class | Meanrev fade | Edge = **hit-rate above BWR**, with modest R thickness |
| Geometry | SL **7000** / TP **8750** pts | TP > SL always (hard rule) |
| Designed RR / R | **1.25** | Not Harvest RR=1.0 · not lottery RR≥3 |
| BWR | **44.4%** | Lower than Harvest 50% — more WR room |
| Side of edge | **Mixed WR + R** | WR-side primary; R=1.25 lifts E_N when WR clears BWR |
| Leak prior | ~**7.0 pp** (c_R≈1100/7000 / (R+1)) | Live spread ≈**1020** · RT cost prior ≈**1100** pts |
| Soft research WR | ≳ **54–58%** after Leak prior | Probe 54.6% · blotter May–Aug 57.0% |
| Selectivity (P0) | BB **2.2** · CD **6** · ATR≤**2380** | Cuts Sep/Oct FRAGILE high-vol; CD longer than M15 |
| AOS | **OFF** | Pure engine extract; M5 AIOS later |

**Why RR=1.25 (not Harvest 1.0):** Expansion intent = mix functional WR **and** returns. Harvest (7000/7000) raises BWR to 50% and thins payoff — kept as design alt (probe EF≈+4.0 pp), not locked P0.

**Why SL=7000 (~3.9× M5 ATR p50≈1782):** Structural 1R that clears the DE30 spread tax. Thin SL (~ATR×1.5 ≈2700) pushes Leak toward ~18 pp and kills EF. SL 6000 raises Leak (~8.1 pp) and thins probe EF — rejected for P0.

**Why ATR max 2380 (≈p75) ON:** Declared regime filter (Gate G3). Probe: filtered sleeve keeps n≈141 with EF **+3.2 pp**. Cuts high-vol **FRAGILE** without BB-width starvation. Tester log: **469** ATR>max blocks Jan–Aug — gate is live.

**Why CD=6 (vs M15 CD=2):** M5 fires denser; longer cooldown reduces double-taps on the same excursion.

### 2.2 Structural win path

| Layer | Role on DE40 / DE30 M5 |
| --- | --- |
| Signal | Long ≤ lower BB; short ≥ upper BB on closed M5 · **BBDev 2.2** |
| Regime gates | ATR **max 2380** ON · BB-width **OFF** |
| Session | Frankfurt / London cash **08:00–17:00** server · **skip Tue** |
| Entry hygiene | MaxSpread **1500** (must clear live ≈1020) · cooldown **6** bars |
| Exit | Fixed TP **+1.25R** or SL **−1R** (distance in points) |
| Risk G0 | One event · lot **0.1** · exposure / daily-loss containment |
| Containment | Loss-streak pause (3) · fail pause · daily loss % · equity halt |

### 2.3 Class metric targets (research soft bars)

| Metric | Soft target (expansion) | Hard worry |
| --- | --- | --- |
| WR | > 44.4% (BWR); prefer ≥ **54–58%** after Leak prior | Persistently ≤ BWR on tip + W20 |
| R (realised) | ≈ 1.25 (RR−R small) | R ≪ RR without WR compensation |
| BM | > 0; prefer ≥ **+10 pp** on home tip | BM ≤ 0 on primary tip |
| E_N | > 0; prefer ≥ **+0.20R** on tip | ≤ 0 on tip and W20 |
| EF | > 0 after measured Leak | Persistently ≤ 0 with honest costs |
| Soft stress months | WR can dip ≪ BWR (MISMATCH / FRAGILE) | Cluster of home MATCH months ≪ BWR → revisit geometry |
| MaxDD (0.1 lot / $500) | soft under ~15% research | Equity-halt territory |
| Fire count tip | n ≥ **30** (Stage 0) | Starvation (ATR + session too tight) |

### 2.4 Realised edge — primary blotter (2026.01 → 2026.08.31)

| Metric | Value | vs target |
| --- | ---: | --- |
| n (TP+SL closes) | **168** | Usable Stage-0 |
| Entries (buy/sell) | **176** (91 / 85) | Near side-balanced |
| WR | **57.1%** | Clears BWR 44.4%; ≥ soft bar |
| Designed R / BWR | **1.25** / 44.4% | On-thesis |
| BM | **+12.7 pp** | Soft bar cleared |
| E_N | **+0.286R** | Clears +0.20R soft bar |
| EF (Leak prior 7.0 pp) | **+5.7 pp** | Preferred under prior |
| PnL (tester final) | **+$350.64** (+70.1%) | Equity confirms E_N |
| Final balance | **850.64** | Deposit 500 |

**Probe vs Tester:** Design M5* WR 54.6% / E_N +0.229R → blotter May–Aug WR 57.0% / E_N +0.282R — same direction, blotter slightly stronger on the tip-core months present in the log.

### 2.5 Realised edge — tip-core & MATCH pockets

| Slice | n | WR | BM | E_N | EF_prior |
| --- | ---: | ---: | ---: | ---: | ---: |
| May→Aug (design tip months in log) | 93 | 57.0% | +12.5 pp | **+0.282R** | **+5.5 pp** |
| Jun→Aug MATCH only | 75 | **60.0%** | **+15.6 pp** | **+0.350R** | **+8.6 pp** |
| Pre Jan→Apr | 75 | 57.3% | +12.9 pp | +0.290R | +5.9 pp |

Pre-tip looks healthy in aggregate but **hides Feb** (−0.10R) and **Mar** (ATR-starved). Do not read Jan–Apr average as “always on.”

### 2.6 Regime / transfer caveat

Ouroboros H1 meanrev map vs Tester monthly closes (Jan–Aug 2026):

| Month | Tag | n | WR | E_N | EF_prior | Read |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| 2026-01 | pre / MATCH-ish | 36 | **63.9%** | **+0.438R** | +12.4 pp | Strong open |
| 2026-02 | soft | 25 | **40.0%** | **−0.100R** | −11.4 pp | **Regime tax** — not class death |
| 2026-03 | gated | 1 | 0% | −1.0R | — | ATR starvation (127 blocks) |
| 2026-04 | recovery | 13 | **76.9%** | **+0.731R** | +25.5 pp | Into tip |
| 2026-05 | **MISMATCH** | 18 | **44.4%** | **0.0R** | −7.0 pp | Tag matches soft print |
| 2026-06 | MATCH | 19 | 47.4% | +0.066R | −4.1 pp | Soft MATCH start |
| 2026-07 | MATCH | 24 | **58.3%** | **+0.312R** | +6.9 pp | On-home |
| 2026-08 | MATCH | **32** | **68.8%** | **+0.547R** | +17.3 pp | **Star month** |
| 2026-09 | **FRAGILE** | — | — | — | — | **Not in log** |
| 2026-10 | **FRAGILE** | — | — | — | — | **Not in log** |

**Read:** Edge concentrates in **Jul–Aug MATCH** (and Jan/Apr). **Feb** and **May MISMATCH** explain soft expectancy — frame as regime, not “M5 fade is broken.” **Sep–Oct FRAGILE** must be scored before any keep claim that includes the full design tip.

**Broker depth:** YWO DE30 history from **2025.06.05**. M5 ATR (Point=0.01): p50 ≈ 1782 · p75 ≈ 2384 · p90 ≈ 2912 · mean ≈ 1860.

---

## 3. Trade profile

Primary evidence: Jan→Aug 2026 closes (n=168 TP/SL). Side counts from entries. Hold-time / hour cells OPEN until deal export.

### 3.1 Winners (n=96 · 57.1%)

| | Jan→Aug | May→Aug | Jun→Aug MATCH |
| --- | ---: | ---: | ---: |
| Share | 96/168 (**57.1%**) | 53/93 (57.0%) | 45/75 (**60.0%**) |
| Typical exit | TP at **~+1.25R** | same | same |
| Character | Fade completes to fixed TP | same | densest in Aug |

- Realisation stays **FIXED_RR** — winners are TP hits.  
- Best calendar pocket: **Aug** (WR **68.8%**, n=32) — strongest MATCH month.  
- **Jan** and **Apr** also win-heavy; do not overweight pre-tip alone.

### 3.2 Losers (n=72 · 42.9%)

| | Jan→Aug | May→Aug | Stress months |
| --- | ---: | ---: | --- |
| Share | 72/168 (42.9%) | 40/93 (43.0%) | Feb 15 SL · May 10 SL |
| Typical exit | SL at **~−1R** | same | same |
| Character | Continuation / impulse into stop | MISMATCH / soft MATCH | Regime tax |

- Classic meanrev failure: band-ride into SL.  
- Soft pockets: **Feb** (WR 40%) · **May MISMATCH** (WR 44.4% · E_N 0) · soft **Jun** (WR 47.4%).  
- **Mar** almost no fires (ATR gate) — starvation, not a long loser streak book.

### 3.3 Exit mix (Jan→Aug)

| Exit | Count | Share | Read |
| --- | ---: | ---: | --- |
| Take profit (~+1.25R) | 96 | 57.1% | On-thesis |
| Stop loss (~−1R) | 72 | 42.9% | On-thesis |
| Other / open / non-1R | ~8 entry−close gap | small | Negligible for class read |

→ Realisation stays **`FIXED_RR_FADE`**. No MID-exit logic.

### 3.4 Side mix (entries)

| Side | Entries | Share | Read |
| --- | ---: | ---: | --- |
| BUY | 91 | 51.7% | Balanced |
| SELL | 85 | 48.3% | Balanced |

Unlike M15 tip (SELL-led expectancy), M5 Jan–Aug entries are near 50/50. Side-conditioned WR OPEN until deal tape.

### 3.5 Open / hour / hold

| Item | Status |
| --- | --- |
| Hold-time win vs lose | OPEN (need deal export) |
| Hour / DOW cells | OPEN (Tue filtered by preset) |
| Overnight inventory | Expected low (session 08–17) — confirm on tape |
| Loss-streak containment | `InpMaxLossStreak=3` armed |

---

## 4. Rolling windows

### 4.1 Calendar months (closes)

| Month | n | WR | E_N | EF_prior | Regime note |
| --- | ---: | ---: | ---: | ---: | --- |
| 2026-01 | 36 | 63.9% | +0.438R | +12.4 pp | Strong pre-tip |
| 2026-02 | 25 | 40.0% | −0.100R | −11.4 pp | Soft — regime tax |
| 2026-03 | 1 | 0% | −1.0R | — | ATR starved (127 blocks) |
| 2026-04 | 13 | 76.9% | +0.731R | +25.5 pp | Recovery |
| 2026-05 | 18 | 44.4% | 0.0R | −7.0 pp | **MISMATCH** |
| 2026-06 | 19 | 47.4% | +0.066R | −4.1 pp | Soft MATCH |
| 2026-07 | 24 | 58.3% | +0.312R | +6.9 pp | MATCH |
| 2026-08 | 32 | 68.8% | +0.547R | +17.3 pp | MATCH star |
| 2026-09 | — | — | — | — | FRAGILE · **missing** |
| 2026-10 | — | — | — | — | FRAGILE · **missing** |

### 4.2 Dedicated window averages

| Window | n | WR | BM | E_N | EF_prior | Final Δ |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| **Jan→Aug (log primary)** | **168** | **57.1%** | **+12.7 pp** | **+0.286R** | **+5.7 pp** | **+$350.64** |
| Pre Jan→Apr | 75 | 57.3% | +12.9 pp | +0.290R | +5.9 pp | — |
| May→Aug tip core | 93 | 57.0% | +12.5 pp | +0.282R | +5.5 pp | — |
| Jun→Aug MATCH | 75 | 60.0% | +15.6 pp | +0.350R | +8.6 pp | — |

### 4.3 Rolling expectancy (path proxy from monthly sequence)

Formal W15/W20 trade-path not yet rebuilt from deal order. Monthly sequence already shows:

| Path view | Read |
| --- | --- |
| Expectancy through MATCH core | Jul–Aug carry · E_N +0.31…+0.55R |
| Soft dips | Feb (−0.10R) · May (0R) · Jun (+0.07R) |
| Collapse risk | Not seen on MATCH cluster; FRAGILE months unscored |

**Interpretation:** Soft months = **regime mismatch taxes**. Home MATCH expectancy stays clearly positive. Re-score W15/W20 after tip May→Oct deal export.

### 4.4 Frequency & gates

| Metric | Jan→Aug |
| --- | ---: |
| TP+SL closes | 168 |
| Entries | 176 |
| ATR>max blocks | **469** |
| Trades / month (closes) | ~21 |
| vs design probe | Probe n≈141 on tip ~6m; blotter denser on Jan–Aug (includes pre-tip) |

ATR blocks peak Mar–May (regime / vol) and collapse in Aug (5) — gate tracks FRAGILE/high-vol, not random starvation.

### 4.5 Cost / spread note

| Source | Spread |
| --- | --- |
| Journal open p50 | ≈ **84** pts (optimistic Tester) |
| Live broker prior | ≈ **1020** pts |
| Leak authority | **prior 7.0 pp** until deals |

---

## 5. Performance

### 5.1 Primary window (2026.01.01 → 2026.08.31)

| Setting | Value |
| --- | --- |
| Symbol / TF | **DE30** M5 (DE40) |
| Magic | **26101903** |
| Geometry | SL**7000** / TP**8750** · RR **1.25** |
| Filters | 08–17 · skip Tue · ATR max **2380** · CD **6** · AOS **off** |
| Deposit | 500 |
| Final balance | **850.64** |
| Net PnL | **+$350.64** (+70.1%) |
| n / WR / E_N | 168 / **57.1%** / **+0.286R** |
| BM / EF_prior | +12.7 pp / **+5.7 pp** |
| Side entries | BUY 91 · SELL 85 |

### 5.2 vs design probe

| | Probe M5* | Tester May–Aug | Tester Jan–Aug |
| --- | ---: | ---: | ---: |
| n | ~141 | 93 | 168 |
| WR | 54.6% | 57.0% | 57.1% |
| E_N | +0.229R | +0.282R | +0.286R |
| EF | +3.2 pp | +5.5 pp | +5.7 pp |

Directionally consistent; blotter does not falsify the probe. Tip May→Oct still required for Stage-1 tip admission.

### 5.3 vs DE40 M15 Balanced P0 (context only)

| | M5 (this) | M15 ([system_profile.md](./system_profile.md)) |
| --- | --- | --- |
| Magic | 26101903 | 26101902 |
| SL / TP | 7000 / 8750 | 5000 / 6250 |
| ATR max | 2380 | 4070 |
| Leak prior | 7.0 pp | 9.8 pp |
| Tip authority | May–Aug proxy (full tip OPEN) | May→Oct n=77 · E_N +0.31R |
| Role | Expansion TF sleeve | Expansion TF sleeve + AIOS DE40stack |

Different TF/geometry — **not** a replace; score separately.

### 5.4 Drawdown / stress

| Item | Status |
| --- | --- |
| MaxDD path | OPEN (not exported this session) |
| Soft months | Feb · May · soft Jun — expected under regime map |
| Equity halt | Not observed as book-killer on Jan–Aug final |

---

## 6. Key metrics (one-pager)

| Metric | Value | Authority |
| --- | ---: | --- |
| Class | Meanrev FIXED_RR_FADE | Identity |
| RR / BWR | **1.25** / **44.4%** | Design |
| Leak prior | **7.0 pp** | Cost policy until deals |
| Primary window | 2026.01→08 | Tester log |
| Final / PnL | **850.64** / **+$350.64** | Tester |
| n / WR / E_N / EF | **168** / **57.1%** / **+0.286R** / **+5.7 pp** | Closes |
| Tip-core May→Aug E_N | **+0.282R** | Closes |
| MATCH Jun→Aug E_N | **+0.350R** | Closes |
| Star month | **2026-08** WR 68.8% | Calendar |
| Soft months | Feb · May MISMATCH | Regime |
| ATR blocks | 469 | Filters live |
| Open spread journal p50 | ~84 pts | Optimistic |
| Live spread prior | ~1020 pts | Broker |
| AOS | OFF | Preset |
| Tip May→Oct / Sep–Oct | **MISSING** | Next run |
| Pool (pending tip) | **EXPANSION_KEEP candidate** | Not live admit |

---

## 7. Explicit non-claims

- Not a live capital admit · not a replace for DE40 M15 / FX / UK books.  
- Probe is a **design prior**, not Stage-1 blotter.  
- Jan–Aug ≠ full design tip (May→Oct); FRAGILE Sep–Oct **untested** here.  
- Journal spreads understate live Leak — prior 7.0 pp remains authority.  
- Soft Feb / May are **regime mismatch**, not automatic geometry rejection.  
- Do not borrow M15 `DE40stack` L2det on M5 — M5 arm is `L2det_de40_m5_v1b` only.

---

## 8. Status / next evidence

| Item | Status |
| --- | --- |
| Tip May→Oct | **DONE** (n123 · →10.19) |
| M5 AIOS P0–P7 | **HITL ARMED** · [`AIOS_SIGNOFF_M5.md`](./AIOS_SIGNOFF_M5.md) · **`DE40_5m_stack`** · magic **26151907** |
| Measured Leak | **OPEN** (prior 7.0 pp authority) |
| Next | Tester confirm ledger · paper/tiny-f checklist · deal-scored Leak |

---

## 9. Related paths

| Path | Role |
| --- | --- |
| `Profiles/Tester/BMRG/DE40/DE40_5m_stack.set` | **HITL research OS** |
| `Profiles/Tester/BMRG/DE40/BMRG-M5-DE40-6M-P0_balanced_chart.set` | Engine P0 |
| `blotter/archive/DE40-M5-P0/` · `DE40-M5-AOS-P7/` | Engine · promotion |
| [`system_profile.md`](./system_profile.md) | M15 sibling |
| [`edge_framework.md`](./edge_framework.md) | Normative maths binding |
| [`README.md`](./README.md) | Asset index |
