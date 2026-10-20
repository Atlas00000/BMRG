# AUDUSD — Edge Discovery

**Version:** 0.1.0  
**Status:** **Active** — Book A asset expansion (not live replace)  
**Symbol:** AUDUSD · M5 · G0 · AOS OFF  
**Governs:** EDX experiments below (one task at a time)  
**Normative parents:** [`edge_framework.md`](./edge_framework.md) · `doc/unified_edge_framework.md`  
**EA under study:** [`system_profile.md`](./system_profile.md)  
**Blotter:** `blotter/inbox/` → archive + clear automatically after review  
(`.cursor/rules/blotter-clear-after-review.mdc` — **do not ask**)  
**Presets (load path):** `MQL5/Profiles/Tester/BMRG/AUDUSD/`  
**Do not mix** with EURUSD EDX (`doc/edge_discovery.md`) or live `8210204` / INF.

---

## 0. Objective and frozen rules

### Goal

Isolate and refine the AUDUSD Harvest-extract edge so we keep a **pool of expectancy-positive, survival-aware** configurations:

```
E_N > 0
WR  > BWR          # BM > 0 (above breakeven frontier)
EF  > 0            # after Leak (preferred)
→ Stage-1 Robust: EF > M   # production bar — not raw profit / PF
```

**Survival matters as much as profit.** Positive expectancy alone is not enough if MaxDD, ruin path, loss clustering, or tip-regime wipeouts make the sleeve un-compoundable.

**Not** sole objectives: raw profit, PF, or WR chasing (90% WR / 0.15 payoff trap = fail).

### Discovery objective (every task)

```
maximise E_N  subject to  EF > M   (when Leak measurable)
else (expansion): keep E_N > 0 and WR > BWR; label EXPANSION_KEEP|WATCH|DROP
report FULL health vector delta vs EDX-P0-T01 — never PF / $ alone
```

Pool admission (expansion): `E_N > 0` ∧ `WR > BWR` (EF>0 preferred).  
Production capital on a member: still requires G0–G5 on that preset (`edge_framework.md` §7.2).

### Investigation order (before any structural tweak)

1. **Data integrity** — blotter, event_id, 1R, preset/magic match, G0  
2. **Execution / costs** — `c_R`, Leak, RR−R gap  
3. **Regime** — where BM lives / dies (tip mismatch allowed as L3)  
4. **Structural change** — SL/TP/filters/code  

No parameter tweaks before 1–3 are excluded for the claim under test.

### Evidence tiers

| n events | Use |
| --- | --- |
| < 100 | No firm conclusions — descriptive / EXPANSION_WATCH only |
| 100–384 | Provisional — cannot pass production gates |
| ≥ 385 | Gate-eligible (Standard) |
| ≥ 1068 | High confidence |

AUDUSD May→Aug profile currently **n≈58** → treat all pre-deal conclusions as **provisional**. Lengthen window and/or export deals before Robust claims.

### Working hypothesis (confirm or reject)

> **Claim to test:** Weakness is **payoff-side (R / AL)**, not frequency-side — good trades exist, but **average loss (AL) is too large**, compressing realised `R`, raising `BWR`, and eating `BM`/`EF`.

**Locked by EDX-P0-T01 (May→Aug, Leak still proxied):**

| Side | Evidence | Status |
| --- | --- | --- |
| **WR-side** | WR **62.07%** ≫ BWR 50%; AW=AL=**1.0R**; RR−R=**0** | **LOCKED** |
| **R-side (AL too large)** | No AL inflation vs AW on FIXED_RR G0 | **REJECTED** as primary |
| **Both** | Tip / Mon / hour-12 still open as **regime/hygiene** (not AL) | Open for P1/P3 |

**Explicit rule:** Do **not** default to tightening SL to “fix AL.” P2 payoff runs are pool-diversity / ATR-scale only. Prefer P1 isolation → P3 filters for WR-side margin.

### Canvas caveat

Canvas / charts = **display only**. Verdicts come from blotters scored under [`edge_framework.md`](./edge_framework.md).

---

## 1. Task template (every EDX task)

| Field | Content |
| --- | --- |
| **ID** | `EDX-P#-T##` |
| **What changes** | Inputs / procedure / code (or “none — score only”) |
| **Metric targeted** | Framework symbol(s) |
| **Expected health-vector effect** | Directional claim on WR, R, BM, Leak, EF, E_N, n, MaxDD, … |
| **Test preset** | File under `Profiles/Tester/BMRG/AUDUSD/` |
| **Beat / pool bar** | Full vector vs **EDX-P0-T01**; pool: E_N>0 · WR>BWR |
| **Accept / reject** | Clear criterion (see task) |
| **Status** | `PENDING` / `RUNNING` / `DONE` / `REJECTED` / `SKIPPED` |

**Active task:** execute **only** the first `PENDING` task in order. Do not skip phases.

After scoring: archive → clear inbox → update `blotter/CURRENT.md` (**no ask**).

---

## 2. Preset naming and tester contract

```
EDX-P{phase}-T{task}_{change-summary}_{context}.set
```

**Always:**

- Geometry baseline: **G0** (`MaxLevels=1`, `MaxEntries=1`) unless task says otherwise  
- Tester: **AUDUSD** M5 · every tick · **ACCOUNT CURRENCY** (never pips)  
- AOS OFF · kill-switch on  
- Unique **magic** per preset (82301xx series)  
- After run: export deals → `blotter/inbox/`  

**Preset directory (new — do not dump into EURUSD BMRG root):**

```
C:\Users\emili\AppData\Roaming\MetaQuotes\Terminal\D0E8209F77C8CF37AD8BF550E51FF075\MQL5\Profiles\Tester\BMRG\AUDUSD\
```

**Primary window (P0 reference):** `2026.05.01 → 2026.08.31`  
**Tip stress window:** `2026.05.01 → 2026.10.03` (or history tip)  
**Long validation window:** `2026.03.23 → 2026.09.21` (Book A protocol)

---

## 3. Provisional baseline (pre-P0 · journal only)

From `system_profile.md` / `blotter/archive/BOOKA-AUDUSD-20261007/` — **not** the official EDX-P0 scorecard until deals are scored.

| Metric | May→Aug (gross) |
| --- | ---: |
| n | 58 |
| WR | 62.1% |
| R (approx) | ≈ 1.0 |
| BWR / BM | 50% / +12.1 pp |
| E_N | +0.241R |
| PnL | +$44.39 |
| Zone | Fragile / Insufficient n (Leak pending) |
| Side (provisional) | **WR-side leading**; R-side unproven |

Official P0 replaces this table.

---

## PHASE 0 — BASELINE SCORECARD (`EDX-P0`)

Reference every later preset is compared against. **No strategy changes.**

### EDX-P0-T01 — Full-sample G0 baseline health vector

| | |
| --- | --- |
| **What changes** | Nothing — score Book A Harvest geometry on May→Aug |
| **Metric targeted** | Full health vector: n, WR, AW, AL, R, RR−R, BWR, BM, FMI, Leak (c_R), EF, M, E_N, PF, MaxDD; W15/W20/W30 now, W100/W250/W500 when n allows |
| **Expected effect** | Establishes reference; zone Negative/Fragile/Robust; side diagnosis WR vs R |
| **Test preset** | `EDX-P0-T01_baseline_G0_AUDUSD-M5_MayAug.set` |
| **Magic** | **8230101** |
| **Tester window** | 2026.05.01 → 2026.08.31 |
| **Changed inputs** | (baseline) BBDev 2.2 · SL300/TP300 · session 12–20 · skip Tue · Risk% 0.5 · AOS off |
| **Hypothesis** | Under clean G0 + currency, edge is WR-side (R≈RR); AL-compression claim is false unless RR−R or AW/AL say otherwise |
| **Beat baseline** | N/A — this **is** the baseline |
| **Accept** | Deal blotter scored; health vector filled; zone named; **WR-side / R-side / both** stated explicitly |
| **Reject** | Pips mode; MaxLevels≠1; wrong symbol; AOS on; **wrong magic/SL/TP** |
| **Status** | `DONE` **ACCEPT** 2026-10-07 — baseline LOCKED. See `blotter/archive/EDX-P0-T01/SCORECARD.md` |

### EDX-P0-T02 — Rolling windows + lifecycle + ΔD

| | |
| --- | --- |
| **What changes** | None — analysis on T01 blotter |
| **Metric targeted** | W15/W20/W30 (+ W100+ if n); lifecycle; ΔD |
| **Expected effect** | Detect Compressing / Near frontier / Below; tip vs mid |
| **Test preset** | Reuse T01 (no new run if archive complete) |
| **Accept** | Lifecycle + ΔD documented per `edge_framework.md` §5 |
| **Status** | `DONE` — W20 Stable/Expanding; all months E_N>0; ΔD N/A (n&lt;W250). See SCORECARD |

### EDX-P0-T03 — Production-gate zone calc (Stage 1 numbers)

| | |
| --- | --- |
| **What changes** | None — apply cost model; flag `costs_defaulted` if needed |
| **Metric targeted** | BM, Leak, EF, M → zone |
| **Expected effect** | Official P0 verdict Negative / Fragile / Robust |
| **Test preset** | T01 |
| **Accept** | EF, M, zone on scorecard; note n tier |
| **Status** | `DONE` — **Fragile** EF +4.57pp ≤ M ±12.12pp · Leak proxy 7.5pp `costs_defaulted` · Insufficient n |

### EDX-P0-T04 — Tip stress (May→Oct) vs May→Aug baseline

| | |
| --- | --- |
| **What changes** | Window only |
| **Metric targeted** | WR, E_N, BM, EF vs T01; regime leak L3 |
| **Expected effect** | Confirm whether longer tip eats edge (profile: May→Oct &lt; May→Aug) without killing class |
| **Test preset** | `EDX-P0-T04_baseline_G0_AUDUSD-M5_MayOct.set` |
| **Magic** | **8230104** |
| **Hypothesis** | Tip softness = regime mismatch, not AL death |
| **Accept** | Vector vs T01; label L3 if primary window holds and tip weakens |
| **Status** | `DONE` **ACCEPT** 2026-10-07 — May→Oct tip: E_N +0.123R still &gt;0 but EF −1.34pp; **Sep WR 27% E_N −0.455R = L3**. See `blotter/archive/EDX-P0-T04/SCORECARD.md` |

**P0 baseline to beat (locked):** E_N **+0.241R** · EF **+4.57 pp** (proxy) · WR **62.07%** · BM **+12.07 pp** · n **58** · side **WR-side** (R-side REJECTED)  
**Tip note:** May→Oct dilutes; do not DROP on tip alone.

---

## PHASE 0.5 — DATA INTEGRITY & BLOTTER (`EDX-P05`)

Required before believing P0 numbers or changing parameters.

### EDX-P05-T01 — Event aggregation audit

| | |
| --- | --- |
| **What changes** | None — audit T01 blotter (re-run preset only if export missing) |
| **Metric targeted** | event_id integrity; G0 single-ticket; 1R = SL distance |
| **Expected effect** | PASS/FAIL admissibility |
| **Test preset** | `EDX-P05-T01_integrity_G0_AUDUSD-M5_MayAug.set` (same geometry) |
| **Magic** | **8230151** |
| **Accept** | All events G0; SL/TP points match preset; no ticket-WR inflation |
| **Status** | `DONE` **PASS** 2026-10-07 — mag 8230151; SL/TP pts exact 300; concurrent≤1. `blotter/archive/EDX-P05-T01/` |

### EDX-P05-T02 — Cost components / Leak

| | |
| --- | --- |
| **What changes** | None — populate spread/commission/swap/slippage per event |
| **Metric targeted** | c_R, Leak, EF |
| **Expected effect** | Replace gross BM with EF; zone may move Fragile↔Negative |
| **Test preset** | T01 / P05-T01 blotter |
| **Accept** | Leak stated; costs_defaulted flagged if used |
| **Status** | `DONE` — Leak **7.50 pp** proxy · EF **+4.57** · Fragile · `costs_defaulted`. `EDX-P05-T02/` |

### EDX-P05-T03 — RR−R gap + side diagnosis lock

| | |
| --- | --- |
| **What changes** | None — compute AW, AL, R, RR−R from deals |
| **Metric targeted** | R, RR−R, AW, AL → **WR-side / R-side / both** |
| **Expected effect** | **Confirm or reject** the AL-too-large hypothesis |
| **Test preset** | T01 blotter |
| **Accept** | Explicit lock: WR-side \| R-side \| both, with numbers |
| **Reject criterion for R-side claim** | If RR−R ≈ 0 and AW≈AL≈1R → **reject R-side primary** |
| **Status** | `DONE` — RR−R=0 · AW=AL=1R · **WR-side LOCKED** · R-side **REJECTED**. `EDX-P05-T03/` |

---

## PHASE 1 — EDGE ISOLATION / DIAGNOSIS (`EDX-P1`)

Condition the health vector. Prefer **offline** tags on P0 blotter + price; re-run presets only if needed.

### EDX-P1-T01 — Session cells (within 12–20 + outside inventory)

| | |
| --- | --- |
| **What changes** | None — condition on entry hour / session bucket |
| **Metric targeted** | BM per cell (report cells with n≥30; else provisional) |
| **Expected effect** | Rank where edge vs losses live (profile: hour-12 weak) |
| **Test preset** | `EDX-P1-T01_sessionCells_G0_AUDUSD-M5_MayAug.set` |
| **Magic** | **8230111** |
| **Accept** | Ranked session statement + BM_worst note |
| **Status** | `DONE` **ACCEPT** — edge 14–20; losses **12–14** (n=32 BM−3.1). `blotter/archive/EDX-P1/SCORECARD.md` |

### EDX-P1-T02 — Day-of-week cells

| | |
| --- | --- |
| **What changes** | None — DOW condition (Tue already filtered) |
| **Metric targeted** | BM / E_N by DOW |
| **Expected effect** | Confirm Mon weakness; Fri strength |
| **Test preset** | `EDX-P1-T02_dowCells_G0_AUDUSD-M5_MayAug.set` |
| **Magic** | **8230112** |
| **Accept** | DOW table; candidates for P3 filters only if BM≤0 with adequate n |
| **Status** | `DONE` **ACCEPT** — Fri best; Mon BM−3.8 provisional (n=13). Same SCORECARD |

### EDX-P1-T03 — Volatility × trend regime (ATR tercile × ER)

| | |
| --- | --- |
| **What changes** | None — tag events per unified §4.5 |
| **Metric targeted** | BM_cell, BM_worst, regime concentration |
| **Expected effect** | Home regime vs hostile; REGIME_CONCENTRATED if &gt;70% |
| **Test preset** | Reuse T01 blotter + price tags (no new .set required) |
| **Accept** | BM_worst; concentration %; n per cell |
| **Status** | `DONE` **ACCEPT** — home **ATR_high\|ranging** E_N +0.44R; mid-ATR range soft; REGIME_CONCENTRATED 92% (OK w/ regime_filtered). `blotter/archive/EDX-P1/P1-T03_SCORECARD.md` |

### EDX-P1-T04 — Win vs loss anatomy (MAE/MFE, duration, streaks)

| | |
| --- | --- |
| **What changes** | None — path stats from deals/ticks if available |
| **Metric targeted** | Hold time W/L; MAE/MFE; worst streak vs expected; tail share |
| **Expected effect** | DEPENDENCE if streak &gt; 1.5× expected; TAIL_RISK if largest loss &gt; 15% gross profit |
| **Test preset** | T01 blotter |
| **Accept** | Anatomy memo; flags named |
| **Status** | `SKIPPED` for now — streak/hold already on P0 (max SL streak 3, no DEPENDENCE); MAE/MFE deferred until deal/tick export |

### EDX-P1-T05 — Isolation summary (ranked)

| | |
| --- | --- |
| **What changes** | None — synthesis |
| **Metric targeted** | WHERE edge lives / WHERE losses live |
| **Expected effect** | Ordered backlog for P2 (payoff) vs P3 (filters) vs skip |
| **Test preset** | — |
| **Accept** | Written ranked statement in archive `EDX-P1/` |
| **Status** | `DONE` — see `blotter/archive/EDX-P1/SCORECARD.md` (P3: StartHour13 justified; skip Mon provisional) |

---

## PHASE 2 — LOSS CONTAINMENT & EXIT / PAYOFF (`EDX-P2`)

Experiments targeting **AL** and realised **R**. Each reports **full health-vector Δ vs P0-T01**.  
A change that raises WR but drops **E_N or EF** is a **regression**.

> If P05-T03 **rejects** R-side, still run a minimal payoff neighborhood (T01–T03) for pool diversity, then prioritise P3 hygiene — do not endlessly chase AL.

### EDX-P2-T01 — SL/TP 240/240 (RR=1 ATR-downscale)

| | |
| --- | --- |
| **What changes** | `InpSL_Points=240`, `InpTP_Points=240` |
| **Metric targeted** | AL, R, RR−R, WR, E_N, EF, MaxDD |
| **Expected effect** | If AL was “too large” in price space vs AUD ATR, tighter wings may lift WR or cut DD; if R-side false, may hurt WR more than help |
| **Test preset** | `EDX-P2-T01_SLtighter240_RR1_AUDUSD-M5_MayAug.set` |
| **Magic** | **8230201** |
| **Beat** | E_N ≥ P0 and EF ≥ P0 (or gross BM if Leak same policy); no FREQUENCY_STALL |
| **Accept** | E_N & EF not down; side diagnosis updated |
| **Reject** | E_N or EF down vs P0; or WR↑ with E_N↓ |
| **Status** | `DONE` **REJECT** — E_N −0.048 · EF −11.8 · pnl −10.56. `blotter/archive/EDX-P2/SCORECARD.md` |

### EDX-P2-T02 — SL/TP 360/360 (RR=1 ATR-upscale)

| | |
| --- | --- |
| **What changes** | `InpSL_Points=360`, `InpTP_Points=360` |
| **Metric targeted** | WR, AL, hold time, E_N, EF |
| **Expected effect** | Wider stops reduce noise SL; may lower WR need via same BWR but change path DD |
| **Test preset** | `EDX-P2-T02_SLwider360_RR1_AUDUSD-M5_MayAug.set` |
| **Magic** | **8230202** |
| **Beat** | E_N ≥ P0 · EF ≥ P0 |
| **Accept / reject** | Same regression rule as T01 |
| **Status** | `DONE` **REJECT** — E_N −0.026 · EF −7.5 · pnl −1.30 |

### EDX-P2-T03 — SL300 / TP450 (RR=1.5 Growth neighborhood)

| | |
| --- | --- |
| **What changes** | `InpTP_Points=450` (SL 300) |
| **Metric targeted** | R, BWR, BM, E_N, EF, WR |
| **Expected effect** | Lower BWR (40%); tests whether payoff sleeve beats hit-rate on AUD |
| **Test preset** | `EDX-P2-T03_TPwider450_RR1.5_AUDUSD-M5_MayAug.set` |
| **Magic** | **8230203** |
| **Beat** | E_N ≥ P0 · EF ≥ P0 (pool KEEP if clears admission even if &lt; P0 E_N but EF>M later) |
| **Accept** | Pool label + vector Δ; do not accept on PF/$ alone |
| **Status** | `DONE` **REJECT** — WR 22% · E_N −0.444 · pnl −48.40 |

### EDX-P2-T04 — SL300 / TP240 (RR=0.8 trap check)

| | |
| --- | --- |
| **What changes** | `InpTP_Points=240` |
| **Metric targeted** | WR vs E_N (frontier trap detector) |
| **Expected effect** | WR may rise while E_N collapses — expected **REJECT** if trap |
| **Test preset** | `EDX-P2-T04_TPtighter240_RR0.8_AUDUSD-M5_MayAug.set` |
| **Magic** | **8230204** |
| **Accept** | Only if E_N & EF improve (unlikely) |
| **Reject** | WR↑ E_N↓ → documents trap; reinforces frozen objective |
| **Status** | `DONE` **INVALID** — OnInit refuse `TP_Points must be >= SL_Points` |

### EDX-P2-T05 — Exit summary (payoff backlog)

| | |
| --- | --- |
| **What changes** | None — synthesis of T01–T04 |
| **Metric targeted** | Best payoff geometry for stack |
| **Expected effect** | Lock RR sleeve for AUD (Harvest vs Growth vs scale) |
| **Test preset** | — |
| **Accept** | Written pick + rejected AL claim status |
| **Status** | `DONE` — **keep SL300/TP300**; R-side rejected; proceed **P3 filters** |

*Note:* Time-stops, BE moves, ATR trails, partial TP are **deferred** until EA inputs exist or a coded task is opened. Do not invent inputs the `.set` cannot express.

---

## PHASE 3 — ENTRY QUALITY (`EDX-P3` entry)

Tighten when/where we fade — trade quality before stacking.

### EDX-P3-T01 — Skip Monday

| | |
| --- | --- |
| **What changes** | `InpTradeMon=false` |
| **Metric targeted** | BM, E_N, EF, n (freq) |
| **Expected effect** | Drop Mon BM≤0 cell; n must stay ≥ 50% P0 |
| **Test preset** | `EDX-P3-T01_skipMon_G0_AUDUSD-M5_MayAug.set` |
| **Magic** | **8230301** |
| **Justify filter** | Only if Mon BM≤0 (P1) or EF↑ without FREQUENCY_STALL |
| **Accept** | EF↑ or E_N↑ vs P0 · n ≥ 0.5× n_P0 |
| **Reject** | FREQUENCY_STALL or E_N↓ |
| **Status** | `DONE` **ACCEPT** — E_N +0.277 · EF +6.33 · pnl +41.41 · n=47. `blotter/archive/EDX-P3/SCORECARD.md` |

### EDX-P3-T02 — StartHour 13 (cut hour-12)

| | |
| --- | --- |
| **What changes** | `InpStartHour=13` |
| **Metric targeted** | WR, BM, EF, n |
| **Expected effect** | Remove weakest hour pocket |
| **Test preset** | `EDX-P3-T02_startHour13_G0_AUDUSD-M5_MayAug.set` |
| **Magic** | **8230302** |
| **Accept / reject** | Same filter rules as T01 |
| **Status** | `DONE` **ACCEPT ★** — E_N **+0.368** · EF **+11.42** · pnl **+62.90** · h12=0 · n=57 |

### EDX-P3-T03 — BBDev 2.5

| | |
| --- | --- |
| **What changes** | `InpBBDev=2.5` |
| **Metric targeted** | WR, n, E_N, EF |
| **Expected effect** | Fewer, higher-quality fades |
| **Test preset** | `EDX-P3-T03_BBDev2.5_G0_AUDUSD-M5_MayAug.set` |
| **Magic** | **8230303** |
| **Accept** | E_N & EF ≥ P0 · n ≥ 0.5× n_P0 · note sample tier |
| **Status** | `DONE` **REJECT** — WR 50% · E_N ~0 · EF −7.5 · pnl +2.30 |

### EDX-P3-T04 — CooldownBars 6

| | |
| --- | --- |
| **What changes** | `InpCooldownBars=6` |
| **Metric targeted** | Streaks, DEPENDENCE, E_N |
| **Expected effect** | Less clustered re-entry after SL |
| **Test preset** | `EDX-P3-T04_cooldown6_G0_AUDUSD-M5_MayAug.set` |
| **Magic** | **8230304** |
| **Accept** | E_N/EF hold or ↑; streak pathology down |
| **Status** | `DONE` **NO_DELTA** — identical to P0 vector |

---

## PHASE 4 — FILTERS & REGIME GATES (`EDX-P4`)

Convert P1 regime cells into ATR/BBWidth gates **only** when justified.

### EDX-P4-T01 — ATR regime gate (enable + bounds from P1)

| | |
| --- | --- |
| **What changes** | `InpUseATRRegime=true` + min/max points from P1 BM_worst cells |
| **Metric targeted** | BM_worst, EF, n |
| **Expected effect** | Cut hostile ATR tercile |
| **Test preset** | *Create at task start:* `EDX-P4-T01_ATRgate_G0_AUDUSD-M5_MayAug.set` |
| **Justify** | Excluded cell BM≤0 with n≥30 **or** retained EF↑ without freq &lt;50% P0 |
| **Accept** | Filter rules pass; sample tier stated (n&lt;385 ⇒ no gate-eligible verdict) |
| **Status** | `PENDING` (inputs TBD after P1-T03) |

### EDX-P4-T02 — BB width regime gate (optional)

| | |
| --- | --- |
| **What changes** | `InpUseBBWidthRegime=true` + bounds from P1 |
| **Metric targeted** | EF, n, BM |
| **Test preset** | *Create at task start* |
| **Status** | `PENDING` |

---

## PHASE 5 — STACK BEST (`EDX-P5`)

Combine non-dominated ACCEPTS from P2–P4. One stack at a time.

### EDX-P5-T01 — Stack candidate v1

| | |
| --- | --- |
| **What changes** | `InpStartHour=13` + `InpTradeMon=false` (P3 ACCEPT ★ + ACCEPT); payoff 300/300 |
| **Metric targeted** | E_N, EF, M, n, MaxDD vs P0 **and** vs P3-T02 alone |
| **Expected effect** | Combine filters; reject stack if E_N &lt; T02 alone (interaction tax) |
| **Test preset** | `EDX-P5-T01_stack_start13_skipMon_G0_AUDUSD-M5_MayAug.set` |
| **Magic** | **8230501** |
| **Accept** | E_N ≥ P0 · EF ≥ P0 · n ≥ 0.5× n_P0; prefer E_N ≥ T02 (+0.368) |
| **Status** | `DONE` **ACCEPT_STACK** — E_N **+0.404R** · EF **+13.21** (proxy Robust) · pnl +57.10 · beats T02. `blotter/archive/EDX-P5-T01/SCORECARD.md` |

### EDX-P5-T02 — Stack on tip window (May→Oct)

| | |
| --- | --- |
| **What changes** | Same stack · longer window |
| **Metric targeted** | Regime survival vs P0-T04 |
| **Test preset** | `EDX-P5-T02_stack_start13_skipMon_G0_AUDUSD-M5_MayOct.set` |
| **Magic** | **8230502** |
| **Accept** | Not wipeout; L3 notes OK; prefer E_N>0 on full tip |
| **Status** | `DONE` **ACCEPT_TIP** — E_N **+0.213R** · EF **+3.16** Fragile · pnl +39.10 · beats P0-T04; Sep L3 WR18% E_N−0.636R. `blotter/archive/EDX-P5-T02/SCORECARD.md` |

---

## PHASE 6 — VALIDATION (`EDX-P6`)

Best candidate = **new submission**. No grandfathering.  
**Freeze:** StartHour=13 · TradeMon=false · SL/TP 300/300 · skip Tue (as stack).

### EDX-P6-T01 — Freeze candidate + long window re-score

| | |
| --- | --- |
| **What changes** | Freeze P5 stack inputs; long window |
| **Metric targeted** | Full vector on long sample |
| **Test preset** | `EDX-P6-T01_candidate_G0_AUDUSD-M5_long.set` |
| **Magic** | **8230601** |
| **Window** | **2026.03.23 → 2026.09.21** (set in Tester) |
| **Accept** | n tier stated; ready for G1–G5 checklist |
| **Status** | `DONE` **ACCEPT_FREEZE** — n=73 Insufficient · E_N **+0.151R** · EF **+0.53** Fragile · pnl +35.77. `blotter/archive/EDX-P6-T01/SCORECARD.md` |

### EDX-P6-T02 — Gate G1 (EF > M)

| | |
| --- | --- |
| **What changes** | None — score |
| **Metric targeted** | EF, M, binomial WR&gt;BWR+Leak |
| **Accept** | EF > M on full + recent window |
| **Status** | `DONE` **G1 FAIL** — EF 0.53 &lt; M 11.06; Sep E_N −0.429. `blotter/archive/EDX-P6-T02/SCORECARD.md` · **NOT PRODUCTION-WORTHY** |

### EDX-P6-T03 — Gate G2 walk-forward (WFE ≥ 0.5)

| | |
| --- | --- |
| **What changes** | Anchored WF protocol (unified §7.2) |
| **Metric targeted** | WFE, OOS E_N |
| **Accept** | WFE ≥ 0.5 · OOS E_N&gt;0 in ≥75% folds |
| **Status** | `SKIPPED` — blocked by G1 FAIL / n Insufficient (optional diagnostic later) |

### EDX-P6-T04 — Gate G3 regime robustness

| | |
| --- | --- |
| **What changes** | None — BM_worst / concentration |
| **Metric targeted** | G3 |
| **Accept** | BM_worst&gt;0 or regime_filtered hold with notes |
| **Status** | `SKIPPED` — blocked by G1 FAIL |

### EDX-P6-T05 — Gate G4 Monte Carlo

| | |
| --- | --- |
| **What changes** | MC-1/2/3 at operating f |
| **Metric targeted** | P95 MaxDD, P(ruin), median G |
| **Accept** | Unified G4 pass criteria |
| **Status** | `SKIPPED` — blocked by G1 FAIL |

### EDX-P6-T06 — Gate G5 perturbation + cost stress

| | |
| --- | --- |
| **What changes** | ±10% BBDev/SL/TP/Risk%; costs ×1.5 |
| **Metric targeted** | E_N stability; EF&gt;0 at ×1.5 |
| **Accept** | G5 pass |
| **Status** | `SKIPPED` — blocked by G1 FAIL |

```
PRODUCTION-WORTHY(AUDUSD) = G0 ∧ G1 ∧ G2 ∧ G3 ∧ G4 ∧ G5
```

Until then: **NOT PRODUCTION-WORTHY**. Live stays EURUSD `8210204` + INF.

---

## PHASE 7 — POOL & HANDOFF (`EDX-P7`)

### EDX-P7-T01 — Update AUDUSD candidate pool table

| | |
| --- | --- |
| **What changes** | Docs only — list KEEP sleeves (baseline, payoff, filters, stack) |
| **Metric targeted** | Admission labels |
| **Accept** | Pool table in this folder / BOOKA note |
| **Status** | `DONE` — `doc/assets/AUDUSD/candidate_pool.md` |

### EDX-P7-T02 — AIOS readiness note

| | |
| --- | --- |
| **What changes** | Docs + AIOS FT preset (post P8) |
| **Accept** | Boundary written; FT sign-off when operator clears |
| **Status** | `DONE` — **AUDUSD LIVE 2026-10-08** · mag **8230931** Risk 3% · FT twin 8230921 @ 0.5% · `AIOS_SIGNOFF.md` |

---

## PHASE 8 — CHAMP ENHANCE NO AIOS (`EDX-P8`)

Frozen geometry: **AUDUSD-CHAMP** · Start13 + skip Mon/Tue · SL/TP 300/300 · AOS OFF · magic authority **8230901**.  
Priority: measured Leak → tip/long survival → one ATR gate if justified → docs refresh. **No** payoff surgery · **no** AIOS.

### EDX-P8-T01 — Measured deal Leak (champ May→Aug)

| | |
| --- | --- |
| **What changes** | None — cost model from deals/journal on champ sleeve |
| **Metric targeted** | c_R, Leak, EF, M, zone |
| **Test preset** | `AUDUSD-CHAMP_Harvest_start13_skipMon_G0.set` (or task clone `EDX-P8-T01_champLeak_G0_AUDUSD-M5_MayAug.set` mag **8230801**) |
| **Window** | 2026.05.01 → 2026.08.31 |
| **Accept** | Leak stated without proxy **or** partial + named gaps; geometry untouched |
| **Status** | `DONE` **ACCEPT_LEAK_PARTIAL** — Leak **2.44 pp** (entry spread) · EF **+17.78** Robust* · gaps: commission/swap/slip. `blotter/archive/EDX-P8-T01/` |

### EDX-P8-T02 — Tip / long survival (same Leak policy)

| | |
| --- | --- |
| **What changes** | Same champ inputs · tip + long windows |
| **Metric targeted** | E_N, EF (measured Leak), monthly L3 |
| **Test presets** | `EDX-P8-T02_champTip_G0_AUDUSD-M5_MayOct.set` (**8230802**) · `EDX-P8-T02b_champLong_G0_AUDUSD-M5_long.set` (**8230803**) |
| **Windows** | May→tip · 2026.03.23→2026.09.21 |
| **Accept** | Not wipeout; E_N>0 preferred on tip |
| **Status** | `DONE` **ACCEPT_SURVIVAL** — tip E_N **+0.213** EF+8.16 Fragile · long **+0.151** EF+5.10 · pool WATCH. `blotter/archive/EDX-P8-T02/` |

### EDX-P8-T03 — One ATR gate (justify or SKIP)

| | |
| --- | --- |
| **What changes** | Offline ATR×ER on champ trades; if justified → `InpUseATRRegime=true` + bounds |
| **Justify** | Excluded cell BM≤0 n≥30 **or** EF↑ without FREQUENCY_STALL |
| **Test preset** | *Create only if justified:* `EDX-P8-T03_ATRgate_G0_AUDUSD-M5_MayAug.set` (**8230804**) |
| **Accept** | EF/E_N improve or tip L3 softens; else **SKIP** |
| **Status** | `DONE` **SKIP** — no n≥30 BM≤0 cell. `blotter/archive/EDX-P8-T03/` |

### EDX-P8-T04 — Docs / champ refresh

| | |
| --- | --- |
| **What changes** | Docs + champ `.set` header; bump to **8230911** only if T03 ACCEPT |
| **Accept** | Pool + BOOKA + champ authority updated; P8 closed |
| **Status** | `DONE` — champ **8230901** unchanged · `candidate_pool.md` · `blotter/archive/EDX-P8-T04/` |

---

## 4. Health vector (must report every scored task)

```text
n, WR, AW, AL, R, RR, RR-R, BWR, BM, FMI,
c_R, Leak, EF, M, E_N, PF, MaxDD,
freq_30d, f_declared, f_realised_mean,
lifecycle, ΔD,
side_diagnosis: WR-side | R-side | both,
verdict: EXPANSION_KEEP|WATCH|DROP | gate results
Δ vs EDX-P0-T01: <metric deltas>
```

---

## 5. Active queue

| Order | ID | Status |
| ---: | --- | --- |
| 1 | EDX-P0-T01 | DONE ACCEPT — baseline locked |
| 2 | EDX-P0-T02 | DONE |
| 3 | EDX-P0-T03 | DONE Fragile |
| 4 | EDX-P0-T04 | DONE ACCEPT — Sep L3 tip leak |
| 5 | EDX-P05-T01…T03 | DONE PASS / Leak proxy / WR-side lock |
| 6 | EDX-P1 (T01–T03, T05) | DONE — session + regime isolation complete; T04 skipped |
| 7 | EDX-P2-T01…T05 | DONE — all payoff variants REJECT/INVALID; keep 300/300 |
| 8 | EDX-P3-T01…T04 | DONE — T02 ★ / T01 ACCEPT; T03 REJECT; T04 no delta |
| 9 | EDX-P5-T01 | DONE ACCEPT_STACK — champion sleeve May→Aug |
| 10 | EDX-P5-T02 | DONE ACCEPT_TIP — tip E_N+0.213; Sep L3 |
| 11 | EDX-P6-T01 | DONE ACCEPT_FREEZE — E_N+0.151 Fragile n=73 |
| 12 | EDX-P6-T02 | DONE G1 FAIL — not production-worthy |
| 13 | EDX-P6-T03…T06 | SKIPPED (G1 block) |
| 14 | EDX-P7-T01…T02 | DONE — candidate_pool.md |
| 15 | EDX-P8-T01 | DONE ACCEPT_LEAK_PARTIAL — Leak 2.44 pp |
| 16 | EDX-P8-T02 | DONE ACCEPT_SURVIVAL — tip/long WATCH |
| 17 | EDX-P8-T03 | DONE SKIP — ATR not justified |
| 18 | EDX-P8-T04 | DONE — champ 8230901 authority refreshed |
| — | **Stream** | **P8 CLOSED** · **AUDUSD LIVE** (8230931 Risk 3%) — n not deny |

---

## 6. Document map

| File | Role |
| --- | --- |
| `doc/unified_edge_framework.md` | Maths / production gates |
| `doc/assets/AUDUSD/edge_framework.md` | AUDUSD binding + canvas caveat |
| `doc/assets/AUDUSD/system_profile.md` | EA behaviour |
| **`doc/assets/AUDUSD/edge_discovery.md`** | **This plan** |
| `Profiles/Tester/BMRG/AUDUSD/*.set` | Loadable presets |
| `doc/edge_discovery.md` | EURUSD stream (closed / separate) |

---

## 7. Versioning

- **0.1.0** — Initial AUDUSD discovery: WR/R hypothesis framing, P0–P7 tasks, dedicated preset dir, blotter auto-clear pointer, frozen E_N|EF&gt;M objective, survival + pool admission.
- **0.2.0** — EDX-P8 champ enhance (no AIOS): Leak → tip survival → optional ATR → docs.
- **0.3.0** — AUDUSD AIOS FT sign-off: n/G0–G5 not blockers; preset `AUDUSD-AIOS_LIVE_WITHHOLD_champ_G0` mag 8230921.
- **0.4.0** — AUDUSD LIVE promote: `AUDUSD-AIOS_SCALE_Risk3_champ_G0` mag **8230931** Risk 3%; FT twin 8230921 retained.
