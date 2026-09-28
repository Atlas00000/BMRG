# BMRG M5 EURUSD ~6M — P0 Balanced Geometry Preset

**Status:** RESEARCH PRESET / UNTESTED  
**Not:** live edge proof · production sign-off · optimised on this window  
**Sources for design intent only:** `doc/edge_framework.md` · `doc/system_profile.md`  
**Preset file:** `Presets/BMRG-M5-EURUSD-6M-P0_balanced_geom.set`

| Field | Value |
| --- | --- |
| EA | BMRG (Bollinger Mean-Reversion Grid) |
| Symbol | EURUSD |
| Chart TF | **M5** |
| Tester window (intent) | **2026.03.23 → 2026.09.23** (~6 months ending “today” in workspace) |
| Model | Every tick based on real ticks if available; else 1-minute OHLC — note which you use |
| Aggregation | **Basket events** (`MaxLevels=1`, `MaxEntries=1`) |

Confirm exact from→to in the Strategy Tester date picker if history starts later; record the actual dates in the scorecard below after the run.

---

## 1. How BMRG should behave on M5 EURUSD (intent — not proof)

From **system profile** + **edge_framework** bindings:

- **Class:** Mean-reversion fade of closes beyond ±kσ (BB); optional grid (here **off** / depth 1).
- **Entry:** Closed bar ≤ lower BB → long; ≥ upper BB → short; one direction at a time.
- **Alpha exit:** Closed bar touches/crosses **middle band (SMA)** → flatten basket (not a fixed RR TP).
- **Abort:** Hard SL in points and/or basket loss % / daily / equity halts.
- **Edge shape (hypothesis):** Elevated WR, modest `R`; edge dies on trend/band-ride and M5 cost leak.
- **Benchmark unit:** Basket `event_id`, not raw tickets.
- **Sessions:** Profile does not hard-require a narrow EURUSD session. P0 keeps **time filter OFF** (wide ALLOW). Next lever if needed: London→NY window (e.g. 08:00–20:00 server), not a scalp box.
- **Risk intent:** Prefer Risk% so `f ≈ InpRiskPercent/100` with `risk_definition` using hard SL (Gap B priority 1 / risk% path).

---

## 2. Geometry (balanced mid-band — design intent)

| Piece | Choice | Rationale |
| --- | --- | --- |
| BB | Period 20, Dev **2.0σ** | Profile / engine default signal |
| Alpha TP | `InpTP_Points = 0` | Mid-band exit owns reward (profile §2.3) |
| 1R | `InpSL_Points = **250**` (~25 pips on 5-digit) | Real abort distance beyond typical band touch — **not** a token stop inventing fake RR |
| Designed RR (ex-ante proxy) | `RR_design ≈ \|entry − mid\| / \|entry − SL\|` (`edge_framework` Gap A) | Target **mid band ~0.8–1.2**, not scalp-RR or lottery-RR |
| Grid | `MaxLevels=1`, `MaxEntries=1` | Clean single-leg events; avoid undeclared multi-leg 1R / left-tail depth on first run |
| Fixed TP theatre | Forbidden | No TP &lt; SL; no tiny SL + huge TP |

**Rough M5 EURUSD prior (planning only):** band→mid often ~150–250 points. With SL=250, `RR_design` lands near **~0.8–1.0** when the fade is a clean outer-band touch — balanced for an MR sleeve that needs functional WR **and** non-crushed R.

`designed_rr` for metadata stays **unfrozen** until a validation sample exists (`edge_framework` Gap A).

---

## 3. Expectancy sanity check (`edge_framework` / profile formulas)

Formulas (from BMRG `edge_framework` §4–5 and `system_profile` §2.4):

```text
BWR = 1 / (1 + R)
BM  = WR − BWR
Leak = c_R / (R + 1)
EF  = BM − Leak
E_N = WR × (R + 1) − 1
```

**Assume for design sanity (not a backtest):** realised `R ≈ 1.0` if geometry delivers mid-band RR and exits are mostly mid vs SL.

| Check | Value |
| --- | ---: |
| Breakeven WR **before** costs (`BWR` at R=1) | **50.0%** |
| Assumed M5 EURUSD friction prior | ~20–40 points round-trip (spread + ~0.5×spread slip×2 legs per Gap F spirit) on 250-pt SL → **`c_R ≈ 0.08–0.16`** |
| Leak at R=1 | **~4–8 pp** |
| Min WR for `EF > 0` after that cost prior | **~54–58%** |
| Balanced planning band (profile hypothesis) | WR **~55–68%**, R **~0.6–1.3** |

**Design-not-doomed?** At mid-band RR with modest M5 costs, positive `EF` is **possible in principle** if WR sits in the MR band — not forced negative by tiny-TP/huge-SL theatre, and not WR-maxed by a token SL.  
**If first run shows R ≪ 0.5 with WR theatre, or WR ≪ BWR+Leak with OK R → revise geometry/costs before optimising filters.**

---

## 4. Parameter table (changed vs engine defaults)

| Input | Default | **P0 balanced** | Why |
| --- | ---: | ---: | --- |
| `InpLotMode` | Fixed | **Risk %** | First-class `f`; Stage 3–comparable when blotter exists |
| `InpRiskPercent` | 0.5 | **0.75** | Research-safe; `f = 0.0075` |
| `InpRiskBase` | Equity | Equity | Unchanged |
| `InpSL_Points` | 200 | **250** | Structural 1R; mid-band RR intent |
| `InpTP_Points` | 0 | **0** | Mid exit |
| `InpMaxSpread` | 30 | **25** | Light M5 sanity (not overfilter) |
| `InpMaxLevels` | 1 | 1 | Unchanged / required for clean P0 |
| `InpMaxEntries` | 1 | 1 | Unchanged |
| `InpMaxBasketLossPct` | 3.0 | **2.5** | Light containment |
| `InpMaxDailyLossPct` | 3.0 | **2.5** | Light containment |
| `InpMaxDailyEntries` | 20 | **30** | Avoid choking ~6M M5 sample |
| `InpMaxExposurePct` | 20 | **15** | Milder concurrent pressure |
| `InpMaxLot` | 1.0 | **0.50** | Cap runaway Risk% on small SL mistakes |
| `InpMaxLossStreak` | 3 | **4** | Slightly less choke vs default |
| `InpUseTimeFilter` | false | **false** | Wide ALLOW (P0) |
| `InpUseATRRegime` | false | **false** | No regime skip until earned |
| `InpUseBBWidthRegime` | false | **false** | Same |
| `InpMagic` | 26092101 | **26092350** | Tag this research sleeve |
| BB / ATR / grid step / cooldown / permissions | defaults | defaults | Signal unchanged |

**1R definition (this preset):**  
`risk_definition = hard_sl` (Risk% sizes from `InpSL_Points`).  
`risk_ccy ≈ equity_at_open × 0.75/100` (target); lot from SL distance × tick value.  
`f = risk_ccy / equity_at_open ≈ 0.0075` when sizing works as designed.

---

## 5. Light filters & containment

| Layer | P0 setting |
| --- | --- |
| Time / DoW | OFF (weekdays default true; Sat/Sun false) |
| ATR / BB-width regime | OFF |
| Spread | max **25** points |
| Failure pause | order fails 3; loss streak 4; pause 12 bars |
| Daily flatten on loss | OFF |
| Equity halt | 10% from start (engine default) |

`regime_filtered = false` for metadata until a filter is turned on.

---

## 6. Design-not-restricted checklist (signed)

| # | Rule | P0 |
| ---: | --- | --- |
| 1 | 1R is structural SL distance (250 pts), not token stop | ☐ signed |
| 2 | Alpha exit remains mid-band (`TP=0`); no fake fixed RR theatre | ☐ signed |
| 3 | Designed RR mid-band (~0.8–1.2 intent); not scalp or lottery | ☐ signed |
| 4 | Expectancy can be positive under BMRG formulas after cost prior | ☐ signed |
| 5 | No WR-only or R-only optimisation on this 6M window | ☐ signed |
| 6 | Filters default ALLOW; skip not piled on | ☐ signed |
| 7 | Grid depth 1 — no exposure explosion inventing ticket WR | ☐ signed |
| 8 | Profile/edge_framework text **not** treated as validated baseline | ☐ signed |
| 9 | Artefact labelled RESEARCH / UNTESTED | ☐ signed |

*(Check boxes when you accept the preset before the first run.)*

---

## 7. Post-run scorecard template (fill after test)

**Actual tester dates:** ________ → ________  
**Model / ticks:** ________  
**Deposit / leverage:** ________  
**n basket events:** ________  

### Core (`edge_framework` / profile)

| Metric | Value | Notes |
| --- | --- | --- |
| `n` | | &lt;100 = plumbing only |
| `WR` | | Basket events |
| `AW` / `AL` | | In R |
| `R = AW/AL` | | |
| `BWR = 1/(1+R)` | | |
| `BM = WR − BWR` | | pp |
| mean `c_R` | | estimate if no blotter |
| `Leak = c_R/(R+1)` | | pp |
| `EF = BM − Leak` | | |
| `M` (approx) | | optional |
| `E_N = WR×(R+1)−1` | | |
| `PF` | | diagnostic only |
| MaxDD | | |
| mid% / SL% exits | | `exit_reason_mix` |
| mean hold bars | | |
| gate block rate | | |
| fires / 90d proxy | | vs ~80/90d hypothesis |

### First-run verdict (exploratory — not G0–G5)

| Outcome | Criteria (research bar) |
| --- | --- |
| **Healthy enough to iterate** | `n` usable; `R` not crushed (&gt;~0.5); WR not absurd theatre; EF not obviously doomed by costs alone; fires not starved |
| **Design restricted / dead geometry** | Token-SL WR theatre (`WR` high, `R` tiny); or `R` OK but WR ≪ BWR+Leak with no cost excuse; or near-zero fires from overfilter |
| **Do not claim edge** | Any positive PnL without basket metrics above |

**Single next tweak lever (pick one side only):**

- If **WR high / R crushed** → widen SL slightly or audit mid-exit quality (`RR−R`); do **not** add filters.  
- If **R OK / WR weak** → optional **session widen→London–NY** or cost/spread audit first; only then mild BBDev — **one change**.  
- If **fires starved** → loosen spread or keep time OFF; investigate `FREQUENCY_STALL`, don’t add gates.

---

## 8. Load path

```text
Experts/BMRG/Presets/BMRG-M5-EURUSD-6M-P0_balanced_geom.set
```

Strategy Tester → Expert **BMRG** → Inputs → Load set → Symbol **EURUSD** · Period **M5** · Dates **2026.03.23–2026.09.23** (adjust to available history).

Chart: M5 EURUSD with Bollinger(20, 2) for visual sanity (EA computes its own handles).
