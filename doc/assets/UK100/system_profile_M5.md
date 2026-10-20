# UK100 M5 — System Profile

**Asset:** UK100 (FTSE 100 CFD) · **TF:** M5  
**Sleeve:** Balanced P0 · **engine only (AOS OFF)**  
**Magic:** **26101905**  
**Preset:** `Profiles/Tester/BMRG/UK100/BMRG-M5-UK100-6M-P0_balanced_chart.set`  
**Profile date:** 2026-10-20  
**Evidence:** Tester `logs/20261020.log` · deposit **$500** · every tick · ACCOUNT CURRENCY  
**Framework:** `doc/unified_edge_framework.md` · UK100 binding [`edge_framework.md`](./edge_framework.md) (M15-first; M5 uses same maths)  
**Chart card:** `Profiles/Tester/BMRG/UK100/BMRG_M5_UK100_6M_chart_preset.md`  
**Review:** `blotter/archive/UK100-M5-P0-CHART/REVIEW.md`  
**Sibling:** M15 engine profile [`system_profile.md`](./system_profile.md) · M15 research OS [`AIOS_SIGNOFF.md`](./AIOS_SIGNOFF.md)

**Scope:** Research **asset-list expansion** (index CFD · denser TF). **Not** a live replace for EURUSD / AUDUSD / M15 UK100 live research OS.  
**Candidate posture (2026-10-20):** **EXPANSION_KEEP** · AOS OFF · M5 AIOS **P0 locked** — [`aios_roadmap_M5.md`](./aios_roadmap_M5.md) (do not borrow M15 L2det / FX pins).

**Do not mix** with root `system_profile.md` (EURUSD) · `doc/assets/AUDUSD/` · `doc/assets/AAPL/` · M15 magics **26101201** / **26111307**.

---

## 0. Evidence hierarchy

| Authority | Source |
| --- | --- |
| **Primary tip** | **2026.05.01 → 2026.08.31** · n=116 closed · final **551.16** |
| **Supporting long** | **2026.01.01 → 2026.08.31** · n=235 closed · final **557.25** |
| **Design prior (not blotter)** | Ouroboros M5* probe · n≈154 · WR 50.7% · E_N +0.14R · EF≈+2.3 pp |
| **Regime context** | Ouroboros H1 meanrev map: May–Sep **MATCH** · Oct **FRAGILE** |
| **Not admissible** | Live FT magics · M15 L2 pins on this magic · treating Aug softness as class death · Oct incomplete tip as admission |

### Cross-window scoreboard (journal · FIXED_RR design R=1.25 · Leak **prior 4.0 pp**)

| Window | Final | Δ vs $500 | N | WR | BM | E_N | EF† |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| **May→Aug tip** | **551.16** | **+51.16** | **116** | **52.6%** | **+8.1 pp** | **+0.183R** | **+4.1 pp** |
| Jan→Aug long | 557.25 | +57.25 | 235 | 48.9% | +4.5 pp | +0.101R | +0.5 pp |
| Design probe (M5*) | — | — | ~154 | 50.7% | +6.2 pp | +0.140R | +2.3 pp |

† Gross of designed R; Leak = preset prior **4.0 pp** (`c_R≈160/1800`). Not deal-exported. Tip Tester **holds / slightly beats** design probe.

**Prior months inside long (regime diagnostic):**

| Month | N | WR | E_N | Read |
| --- | ---: | ---: | ---: | --- |
| 2026-01 | 49 | 55.1% | +0.240R | On-home |
| 2026-02 | 40 | 40.0% | −0.100R | Soft — regime tax |
| 2026-03 | 6 | 33.3% | −0.250R | Starved / hostile — ATR + session |
| 2026-04 | 24 | 37.5% | −0.156R | Soft — regime tax |

---

## 1. System identity

| Field | Value |
| --- | --- |
| Full name | Bollinger Mean-Reversion Grid on UK100 M5 |
| Short code | BMRG · UK100 M5 expansion |
| Primary class | **Mean reversion** (statistical deviation fade) |
| Secondary class | Grid / basket — **OFF** (G0 · MaxLevels=1 · MaxEntries=1) |
| Not | Trend-following, breakout, momentum-continuation, scalping theatre |
| Market / TF | **UK100**, **M5** · London cash sleeve |
| Execution | Closed-bar signal (shift 1) → market · lot **0.1** (broker `VOLUME_MIN`) |
| Realisation | **`FIXED_RR_FADE`** (TP/SL; rare multi-bar / overnight path) |
| Regime posture | **`regime_filtered=true`** (session + skip Tue + ATR max ≈ M5 p75) |

### Strategy-class statement

Same **mean-reversion** class as UK100 M15 / FX Balanced / AAPL: the EA **fades excursions** past ±kσ Bollinger bands back toward the short-horizon mid-band on the **M5** clock. It is **not** a trend system and must not be scored as one (trend systems target lower WR with larger R; this sleeve targets **WR above BWR** at modest R).

It should win when FTSE **mean-reverts inside the London session** on M5 often enough that:

```
WR > BWR = 1 / (1 + R)
E_N = WR × (R + 1) − 1 > 0
BM  = WR − BWR > 0
EF  = BM − Leak > 0   (after honest costs)
```

With designed **RR = 1.25** → **R ≈ 1.25** → **BWR = 44.4%**. Soft research targets after Leak prior (~4.0 pp): WR ≳ **50–54%**, BM ≥ +5–8 pp, E_N ≥ **+0.10R** on the home tip; prefer EF > 0.

It loses when price **band-rides** (index impulse, GBP/global risk, high-vol **FRAGILE** cells) into the hard SL — classic meanrev failure. Soft calendar months (Feb / Apr / Aug tip) are read first as **regime mismatch**, not class failure. **ATR max is required on M5** — unfiltered same geometry has EF &lt; 0 in design.

---

## 2. Edge profile

### 2.1 Theoretical edge (meanrev · Balanced RR=1.25)

| Concept | Designed | Implication |
| --- | ---: | --- |
| Class | Meanrev fade | Edge = **hit-rate above BWR**, with modest R thickness |
| Geometry | SL **1800** / TP **2250** pts | TP > SL always |
| Designed RR / R | **1.25** | Same Balanced intent as M15; denser TF, thinner SL in points |
| BWR | **44.4%** | Lower than Harvest 50% — more WR room |
| Side of edge | **Mixed WR + R** | Tip observed **buy-led**; not a permanent side lock |
| Leak prior | **~4.0 pp** (c_R≈160/1800) | Spread≈140 · RT prior≈160 pts — higher Leak than M15 SL2500 |
| Soft research WR | ≳ **50–54%** after Leak prior | Tip landed **52.6%** |
| AOS | **OFF** | Pure engine extract; M5 AIOS later if kept |

**Why RR=1.25 (not Harvest 1.0):** Mix functional WR and returns. Harvest raises BWR to 50% and thins E_N for the same WR.

**Why SL=1800 (~2.8× M5 ATR p50≈643):** Structural 1R that clears spread Leak on M5. Thin SL≈1000 → Leak ~7 pp → EF negative even with ATR gate (design card **restricted**).

**Why ATR max 869 (≈p75) ON — required:** Unfiltered same SL/TP: WR≈46.8% · EF≈**−1.6 pp**. Filtered: EF≈**+2.3 pp** (probe). Cuts high-vol / FRAGILE without BB-width starvation.

**M5 vs M15 structural note:** Same class and RR. M5 fires denser (tip n=116 vs M15 tip n=51), uses tighter points SL, pays a **higher Leak prior** (4.0 vs ~2.9–4.3 pp depending on M15 cost model). Do not merge scorecards or magics.

### 2.2 Structural win path

| Layer | Role on UK100 M5 |
| --- | --- |
| Signal | Long ≤ lower BB; short ≥ upper BB on closed M5 · **BBDev 2.2** |
| Regime gates | ATR **max 869** ON · BB-width **OFF** |
| Session | London cash **08:00–17:00** server · **skip Tue** |
| Entry hygiene | MaxSpread **200** · cooldown **3** bars (denser TF) |
| Exit | Fixed TP **+1.25R** or SL **−1R** (points) |
| Risk G0 | One event · lot 0.1 · MaxDailyEntries 20 · containment |
| Containment | Loss-streak pause (3) · fail pause 24 bars · daily loss % · equity halt |

### 2.3 Class metric targets (research soft bars)

| Metric | Soft target (expansion) | Hard worry |
| --- | --- | --- |
| WR | > 44.4%; prefer ≥ **50–54%** after Leak prior | Persistently ≤ BWR on tip + W20 |
| R (realised) | ≈ 1.25 (RR−R small) | R ≪ RR without WR lift |
| BM | > 0; prefer ≥ **+6 pp** on home tip | BM ≤ 0 on primary tip |
| E_N | > 0; prefer ≥ **+0.10R** on tip | ≤ 0 on tip and W20 |
| EF | > 0 after measured Leak | Persistently ≤ 0 with honest costs |
| Soft stress months | WR can dip below BWR (Feb/Aug-like) | Cluster ≪ BWR → regime / later AIOS, not auto-kill |
| MaxDD (0.1 lot / $500) | Soft under ~8–10% research | Equity-halt territory |
| Frequency | Tip ~25–40 / month when ATR allows | Starvation (Mar-like n=6) = filter working or hostile regime |

---

## 3. Trade profile

### 3.1 Tip May→Aug 2026 (primary · n=116 closed)

| Slice | N | WR | Notes |
| --- | ---: | ---: | --- |
| All | 116 | **52.6%** | TP 61 / SL 55 · 1 open unclosed at window end |
| **BUY** | 62 | **54.8%** | Tip **buy-led** (inverse of soft M15 tip sell-led story) |
| **SELL** | 54 | **50.0%** | Still ≥ BWR |
| Wed | 26 | **65.4%** | Best DOW |
| Fri | 30 | 53.3% | Solid |
| Thu | 28 | 50.0% | Neutral (unlike M15 tip Thu soft) |
| Mon | 32 | **43.8%** | Soft DOW — below BWR |
| Tue | 0 | — | Skip Tue held |

**Hour buckets (tip):**

| Bucket | N | WR |
| --- | ---: | ---: |
| H08–09 | 15 | **66.7%** |
| H10–11 | 36 | **66.7%** |
| H12–13 | 47 | **40.4%** |
| H14–16 | 18 | 44.4% |

Morning London cash carries the tip edge; midday **H12–13** is the soft pocket (candidate for later L2det — not armed here).

**Calendar (tip):**

| Month | Tag (H1) | N | WR | E_N | Read |
| --- | --- | ---: | ---: | ---: | --- |
| May | MATCH | 25 | 64.0% | +0.440R | Strong |
| Jun | MATCH | 27 | 55.6% | +0.250R | Strong |
| Jul | MATCH | 26 | 53.8% | +0.212R | OK (SELL soft 36% inside) |
| Aug | MATCH | 38 | **42.1%** | **−0.053R** | Local tax under MATCH tag |

### 3.2 Winners vs losers (tip)

| | Winners (TP) | Losers (SL) |
| --- | ---: | ---: |
| N | 61 | 55 |
| Hold med (h) | **1.26** | **0.66** |
| Hold mean (h) | 2.49 | 2.27 |
| Hold p90 (h) | ~3.5 | ~2.7 |
| Hold ≥12h | 2 total across tip | — |

**Read:** Losers resolve **faster** than winners (classic fade: adverse impulse hits SL quicker; meanrev winners take longer to reach +1.25R). Overnight path is **rare** (~2% of tip holds ≥12h) — mostly intraday inventory.

**Streaks (tip):** max win **5** · max loss **5** (containment pause at 3 can interrupt live; Tester path still shows raw streaks).

### 3.3 Long Jan→Aug behaviour (diagnostic)

| Slice | Value |
| --- | --- |
| N / WR / E_N | 235 / 48.9% / **+0.101R** |
| Side | Near-balanced BUY 49.1% · SELL 48.8% |
| Soft cluster | Feb–Apr (regime) · Aug tip soft continues |
| Max streaks | W7 / L7 |
| Hold med | ~0.9 h · ≥12h: 4 |

---

## 4. Rolling windows

Expectancy = rolling E_N on designed R=1.25 (journal TP/SL). Tip path is the OS/expansion health reference; long path shows regime stress.

### Tip May→Aug

| Window | Mean E_N | Min | Max | Share ≤ 0 |
| --- | ---: | ---: | ---: | ---: |
| W10 | +0.17 | −0.55 | +1.03 | ~29% |
| W15 | +0.19 | −0.25 | +0.65 | ~14% |
| **W20** | **+0.20** | −0.21 | +0.46 | **~5%** |
| W30 | +0.19 | −0.10 | +0.42 | ~9% |
| **W50** | **+0.19** | **+0.04** | +0.35 | **0%** |

Late tip softness (Aug) pulls W15/W20 last prints negative (~−0.21 to −0.25) while **W50 stays positive** — expansion read: short-horizon regime tax, not expectancy death.

### Long Jan→Aug

| Window | Mean E_N | Min | Max | Share ≤ 0 |
| --- | ---: | ---: | ---: | ---: |
| W20 | +0.13 | −0.33 | +0.58 | ~20% |
| W50 | +0.13 | −0.10 | +0.35 | ~19% |

≤0 share on long is almost entirely the **Feb–Apr** mismatch cluster. Do not DROP the sleeve from the expansion list on prior alone.

---

## 5. Performance

| Lens | Result |
| --- | --- |
| Tip $ (from 500) | **+$51.16** (~+10.2%) |
| Long $ | **+$57.25** (~+11.5%) |
| Tip MaxDD (path proxy, R-calibrated) | **~2.5%** |
| Long MaxDD (path proxy) | Soft mid-single-digit research (Feb–Apr dig) |
| vs design probe | Tip **better** WR/E_N/EF on comparable ATR-gated sleeve |
| vs M15 tip engine | Different magic/TF — denser fires, higher Leak prior, tip E_N +0.18 vs M15 ~+0.10 (not a horse-race; separate sleeves) |
| Filters | Tue **0** fires · ATR max binding · session gated |
| AOS | Off — geometry claim is engine-only |

**Expansion verdict:** **KEEP** on tip Stage-0 / research. Soft Aug and prior Feb–Apr = **regime mismatch**, allowed. Not production admit; not live replace; measured Leak still OPEN.

---

## 6. Key metrics (cheat sheet)

### Locked geometry

```text
Symbol UK100 · TF M5 · Magic 26101905 · AOS OFF
SL 1800 · TP 2250 · RR 1.25 · BWR 44.4%
BB 20 / 2.2 · ATR max 869 (p75) ON · BB-width OFF
Session 08:00–17:00 · skip Tue · MaxSpread 200 · cooldown 3
Lot 0.1 · G0 MaxLevels=1 · MaxEntries=1
Leak prior 4.0 pp (c_R≈160/1800)
```

### Tip health (authoritative blotter)

```text
n=116 · WR=52.6% · BM=+8.1pp · E_N=+0.183R · EF_prior=+4.1pp
BUY WR 54.8% · SELL WR 50.0%
Best: Wed / H08–11 · Soft: Mon / H12–13 / Aug
W20 E_N mean +0.20 (~5% ≤0) · W50 mean +0.19 (0% ≤0)
Δ$ +51.16 · MaxDD proxy ~2.5% · hold med ~1h
```

### Soft research targets vs tip

| Metric | Target | Tip |
| --- | --- | --- |
| WR vs BWR | > 44.4% (prefer ≥50%) | **52.6%** ✓ |
| E_N | > 0 (prefer ≥0.10R) | **+0.183R** ✓ |
| EF after Leak prior | > 0 | **+4.1 pp** ✓ |
| Regime filter declared | ATR + session + Tue | ✓ |

---

## 7. Explicit non-claims

- Not a live replace for FX books or for UK100 **M15** research OS (**26111307**).  
- Not PRODUCTION-WORTHY / full G0–G5 admit.  
- Design probe ≠ Tester blotter (blotter wins).  
- Soft months ≠ auto DROP under expansion ladder.  
- Do not lift ATR max to “fix” frequency.  
- Do not attach M15 `L2det_uk` or EUR/AUD L2 pins to magic **26101905** without a dedicated M5 AIOS stream.

---

## 8. AIOS (started)

| Item | Path |
| --- | --- |
| Roadmap | [`aios_roadmap_M5.md`](./aios_roadmap_M5.md) |
| Baseline | [`UK100_M5_AOS_BASELINE_v1.md`](./UK100_M5_AOS_BASELINE_v1.md) |
| Bad cells | [`aos_bad_cells_M5.md`](./aos_bad_cells_M5.md) |
| Cost | [`aos_cost_policy_M5.md`](./aos_cost_policy_M5.md) |
| Status | **P7 HITL ARMED** · `UK100_5m_stack` · magic **26121907** · measured Leak OPEN |
| Sign-off | [`AIOS_SIGNOFF_M5.md`](./AIOS_SIGNOFF_M5.md) |
| L2 pack | [`aos_l2_policy_M5.md`](./aos_l2_policy_M5.md) |
| L3/L4 | [`aos_l3l4_policy_M5.md`](./aos_l3l4_policy_M5.md) |
| L6 | [`aos_l6_ledger_M5.md`](./aos_l6_ledger_M5.md) |

Keep M5 and M15 scorecards / magics disjoint.
