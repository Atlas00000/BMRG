# BMRG Edge Discovery

**Version:** 1.1  
**Status:** **Main stream closed** — engine isolated; active workstream is AI OS (`doc/ai_OS.md`)  
**Governs:** EDX experiments below (archive / reopen only by named task)  
**Normative parents:** `doc/edge_framework.md` · `doc/unified_edge_framework.md`  
**EA under study:** `system_profile.md`  
**OS wrap:** `doc/ai_OS.md` v0.2 · `aistack` magic **8399001** (paper)  
**Blotter:** `blotter/inbox/` → archived automatically after review (see `.cursor/rules/blotter-clear-after-review.mdc`)

---

## 0. Objective and frozen rules

### Goal

Build and maintain a **pool of BMRG candidates** that stay economically alive across regimes — for compounding and retuning — not a single max-profit winner.

Primary live constraints (admission):

```
E_N > 0
WR > BWR          # above breakeven frontier (BM > 0)
EF > 0            # after Leak (preferred)
```

Stage-1 Robust (`EF > M`) and gates G0–G5 remain the bar for **large** production capital on a member; discovery’s job is to **supply a range** (growth / survival / balanced sleeves). See `doc/candidate_pool.md`.

**Not** sole objectives: raw profit, PF, or WR chasing.

### Discovery objective (every task)

```
Expand / refresh the candidate pool:
  keep presets with E_N > 0 and WR > BWR (and EF > 0);
  label POOL_KEEP | POOL_PROMOTE | POOL_DROP | DOMINATED;
  report full health vector — never profit alone.
```

Ranking flavour (optional): higher E_N among pool members with EF>M → growth sleeve.  
Survival flavour: lower BWR / thicker WR−BWR margin under stress, even if E_N is thinner.

Forbidden: discard a preset solely because final $ or E_N < champion if it still clears admission.

### Investigation order (before any structural tweak)

1. Data integrity (blotter, event_id, 1R, preset match)
2. Execution / costs (`c_R`, Leak, RR−R)
3. Regime (where BM lives)
4. Structural change (SL/TP/filters/code)

### Evidence tiers


| n events | Use                                  |
| -------- | ------------------------------------ |
| < 100    | No conclusions                       |
| 100–384  | Provisional only — cannot pass gates |
| ≥ 385    | Gate-eligible (Standard)             |
| ≥ 1068   | High confidence                      |


### Working hypothesis (confirm or reject)

> **Claim:** Weakness is **payoff-side (R / AL)**, not frequency-side — good trades exist, but **AL is too large**, compressing realised `R`, raising `BWR`, and eating `BM`/`EF`.

**Provisional stance superseded by P0+P1 G0 currency:**


| Side        | Evidence                                                                 | Status |
| ----------- | ------------------------------------------------------------------------ | ------ |
| **WR-side** | R≈RR on fixed TP/SL; BM thin vs BWR; more SL than TP                     | **Locked** |
| **R-side**  | AL-compression as primary claim                                          | **Rejected** |
| **Both**    | Grid / overnight can still inflate AL under non-G0                       | Open if MaxLevels>1 |


**P0+P1 result:** **WR-side** on G0 baseline. P2 reopened for **payoff neighborhood / survival sleeves** (G5 TP−10 killed EF) and pool diversity — not to resurrect the AL-compression claim as primary.

---

## 1. Task template (every EDX task)

Each task below follows:


| Field                             | Content                                             |
| --------------------------------- | --------------------------------------------------- |
| **ID**                            | `EDX-P#-T##`                                        |
| **What changes**                  | Inputs / procedure / code (or “none — score only”)  |
| **Metric targeted**               | Framework symbol(s)                                 |
| **Expected health-vector effect** | Directional claim on WR, R, BM, Leak, EF, E_N, n, … |
| **Test preset**                   | `.set` filename                                     |
| **Beat / pool bar**               | Pool: E_N>0 · WR>BWR (EF>0 preferred); Δ vs **Harvest** (champion) optional |

| **Accept / reject**               | `POOL_KEEP` / `POOL_DROP` / `costs_fragile` / gate PASS·FAIL |
| **Status**                        | `PENDING` / `RUNNING` / `DONE` / `REJECTED`         |


**Active task:** execute **only** the first `PENDING` task in order. Do not skip phases.

---

## 2. Preset naming and tester contract

```
EDX-P{phase}-T{task}_{change-summary}_{context}.set
```

**Always:**

- Geometry for discovery baseline: **G0** (`MaxLevels=1`, `MaxEntries=1`) unless the task explicitly studies grid.  
- Tester: EURUSD M5, every tick, **account currency** (never “profit in pips”).  
- Deposit large enough that Risk% is not permanently min-lot floored if measuring `f` (recommend ≥ 5,000–10,000 for Stage 3 realism; P0 may note `f_realised`).  
- After run: export deals → drop in `blotter/inbox/` (or paste scorecard). Agent scores, archives, clears inbox.

**Preset location:** `MQL5/Profiles/Tester/BMRG/`

---

## PHASE 0 — BASELINE SCORECARD (`EDX-P0`)

Reference every later preset is compared against. No strategy changes.

### EDX-P0-T01 — Full-sample G0 baseline health vector


|                     |                                                                                                                                                                                                                         |
| ------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **What changes**    | Nothing — score EF-G1 G0 geometry on long window                                                                                                                                                                        |
| **Metric targeted** | Full health vector: n, WR, AW, AL, R, RR−R, BWR, BM, FMI, Leak (c_R), EF, M, E_N, PF, MaxDD; plus W100/W250/W500                                                                                                        |
| **Expected effect** | Establishes reference; classifies zone Negative/Fragile/Robust; computes ΔD across W250 steps                                                                                                                           |
| **Test preset**     | `EDX-P0-T01_baseline_G0-EF-G1_EURUSD-M5_long.set`                                                                                                                                                                       |
| **Tester window**   | 2025.01.01 → 2026.09.24                                                                                                                                                                                                 |
| **Changed inputs**  | (baseline) MaxLevels=1, MaxEntries=1, BBDev=2.2, SL=300, TP=450, Risk%=0.5, session 08–20, Magic=8210001                                                                                                                |
| **Hypothesis**      | Under clean G0 + currency PnL, edge is thin; identify whether AL/R or WR dominates                                                                                                                                      |
| **Beat baseline**   | N/A — this **is** the baseline                                                                                                                                                                                          |
| **Accept**          | Blotter scored; health vector filled; zone named; WR-side vs R-side provisional call stated                                                                                                                             |
| **Reject**          | Pips mode used; MaxLevels≠1; n<100                                                                                                                                                                                      |
| **Status**          | `DONE` (2026-09-25 10:01 long window). Official **working P0 reference** locked in `blotter/archive/EDX-P0-T01/SCORECARD_LONG.md`. Caveat: still **pips mode** → Leak TBD / Stage 3 inadmissible until currency re-run. |


**Baseline values to beat (P0 reference):**


| Metric    | Value                                    |
| --------- | ---------------------------------------- |
| n         | 570                                      |
| WR        | 44.74%                                   |
| R (proxy) | ~1.5                                     |
| BM        | +4.74 pp                                 |
| E_N       | +0.118R                                  |
| PF proxy  | 1.21                                     |
| M         | ±4.08 pp                                 |
| Zone      | Fragile pending Leak (gross EF≈M)        |
| Side      | **WR-side** (R-side hypothesis rejected) |


### EDX-P0-T02 — Rolling windows + lifecycle + ΔD


|                     |                                                                                                    |
| ------------------- | -------------------------------------------------------------------------------------------------- |
| **What changes**    | None — analysis on T01 blotter                                                                     |
| **Metric targeted** | W100/W250/W500 health vectors; lifecycle state; ΔD                                                 |
| **Expected effect** | Detect Compressing / Near frontier / Below frontier                                                |
| **Test preset**     | Reuse T01 blotter (no new run if inbox has T01 archive)                                            |
| **Accept**          | Lifecycle state + ΔD documented vs unified §5.5                                                    |
| **Status**          | `DONE` — Near frontier/Fragile; ΔD=+1.2 pp; see `blotter/archive/EDX-P0-T01/EDX-P0-T02_ROLLING.md` |


### EDX-P0-T03 — Production-gate zone calc (Stage 1 numbers)


|                     |                                                                                          |
| ------------------- | ---------------------------------------------------------------------------------------- |
| **What changes**    | None — apply cost model defaults if costs unmeasured; flag `costs_defaulted`             |
| **Metric targeted** | BM, Leak, EF, M → zone                                                                   |
| **Expected effect** | Official P0 verdict: Negative / Fragile / Robust                                         |
| **Test preset**     | T01                                                                                      |
| **Accept**          | EF, M, zone written into scorecard                                                       |
| **Status**          | `DONE` — **Fragile** (G1 fail on W500); Leak=0 costs_defaulted; see `EDX-P0-T03_ZONE.md` |


### EDX-P0-T04 — Monthly stress cell (Sep-2026) vs long baseline


|                     |                                                                                                                   |
| ------------------- | ----------------------------------------------------------------------------------------------------------------- |
| **What changes**    | Window only                                                                                                       |
| **Metric targeted** | WR, E_N, BM on 2026.09 (system_profile showed collapse)                                                           |
| **Expected effect** | Confirm whether “MATCH month” fails under G0                                                                      |
| **Test preset**     | `EDX-P0-T04_baseline_G0-EF-G1_EURUSD-M5_2026-09.set` *(create at task start = T01 inputs, window note in header)* |
| **Hypothesis**      | Sep-26 is a loss cell even at G0 → regime leak, not only grid artifact                                            |
| **Accept**          | n reported; if n<100 mark provisional; compare BM to T01                                                          |
| **Status**          | `DONE` — scored from T01 blotter; Sep WR 25% BM −15pp Negative (n=8 provisional); see `EDX-P0-T04_SEP2026.md`     |


---

## PHASE 0.5 — DATA INTEGRITY & BLOTTER (`EDX-P05`)

Required before believing P0 numbers or changing parameters.

### EDX-P05-T01 — Event aggregation audit


|            |                                                                              |
| ---------- | ---------------------------------------------------------------------------- |
| **Status** | `DONE` — PASS (all level=0; SL/TP 300/450 exact); see `EDX-P05_INTEGRITY.md` |


### EDX-P05-T02 — Cost components populated


|            |                                                                                             |
| ---------- | ------------------------------------------------------------------------------------------- |
| **Status** | `DONE` — default Leak ≈ **2.24 pp**; EF ≈ **+2.5 pp** → Fragile; see `EDX-P05_INTEGRITY.md` |


### EDX-P05-T03 — RR−R gap diagnostic


|            |                                                                                |
| ---------- | ------------------------------------------------------------------------------ |
| **Status** | `DONE` — RR−R≈0; side diagnosis **WR-side** locked; R-side hypothesis REJECTED |


---

## PHASE 1 — EDGE ISOLATION / DIAGNOSIS (`EDX-P1`)

Condition health vector on context. Prefer analysis on T01 blotter + price tags; new presets only when re-run required.

### EDX-P1-T01 — Session cells (Asia / London / NY / overlaps)


|            |                                                                   |
| ---------- | ----------------------------------------------------------------- |
| **Status** | `DONE` — edge in LON–NY / NY; LON thin; see `EDX-P1_ISOLATION.md` |


### EDX-P1-T02 — Day-of-week cells


|            |                                            |
| ---------- | ------------------------------------------ |
| **Status** | `DONE` — Tuesday BM≤0; Wednesday strongest |


### EDX-P1-T03 — Volatility terciles (ATR percentile)


|            |                                |
| ---------- | ------------------------------ |
| **Status** | `PENDING` (needs price tagger) |


### EDX-P1-T04 — Trend vs range (efficiency ratio)


|            |                                |
| ---------- | ------------------------------ |
| **Status** | `PENDING` (needs price tagger) |


### EDX-P1-T05 — Structure context (BB width / distance-in-σ)


|            |                                |
| ---------- | ------------------------------ |
| **Status** | `PENDING` (needs price tagger) |


### EDX-P1-T06 — Win vs loss anatomy (MAE/MFE, duration)


|            |                                                                           |
| ---------- | ------------------------------------------------------------------------- |
| **Status** | `PARTIAL` — duration only (win 26.7h / loss 17.6h); MAE/MFE pending ticks |


### EDX-P1-T07 — Loss clustering / DEPENDENCE / TAIL_RISK


|            |                                                       |
| ---------- | ----------------------------------------------------- |
| **Status** | `PARTIAL` — no DEPENDENCE; TAIL_RISK pending currency |


### EDX-P1-T08 — Isolation verdict memo


|            |                                                                    |
| ---------- | ------------------------------------------------------------------ |
| **Status** | `DONE` — WR-side; filters > payoff next; see `EDX-P1_ISOLATION.md` |


---

## PHASE 2 — LOSS CONTAINMENT & EXIT / PAYOFF (`EDX-P2`)

Target **AL**, realised **R**, and **breakeven frontier** (BWR). Each task = one preset. Full health vector — never PF/profit alone.

**Pool policy:** `POOL_KEEP` if E_N>0 and WR>BWR (EF>0 preferred). `POOL_DROP` if E_N≤0 or WR≤BWR or EF≤0. Dominated on $ / E_N vs Balanced ref ≠ automatic drop — may be a **Survival** sleeve (`doc/candidate_pool.md`).

**Reopened 2026-09-25:** G5 TP−10 flipped EF≤0; need payoff-range candidates on **filter champion** stack (session 12–20, skip Tue).

**Report Δ vs current champion** (`EDX-P2-T04` Harvest) for flavour; admission is the pool bar above. (Growth `EDX-P4-T01` remains secondary ref.)

*Geometry-only tasks T01–T05 runnable. T06–T09 still need code.*

### EDX-P2-T01 — Tighter SL (reduce AL)

| | |
| --- | --- |
| **What changes** | `InpSL_Points=200` (TP=450 → designed RR=2.25) |
| **Metric targeted** | AL, R, BWR, E_N, EF |
| **Expected effect** | Lower BWR; WR may fall; keep WR>BWR and E_N>0 |
| **Test preset** | `EDX-P2-T01_SL200_TP450_champFilters_G0_long.set` (magic **8210201**) |
| **Hypothesis** | Higher R improves survival below 40% WR |
| **Pool bar** | E_N>0, WR>BWR, EF>0 |
| **Status** | `DONE` — **POOL_KEEP (Survival)** · DOMINATED vs Balanced on E_N/EF · WR 34.2%>BWR 30.8% · E_N 0.111 · EF 0.87 Fragile · `archive/EDX-P2-T01/` |

### EDX-P2-T02 — Hold designed RR=1.5 with tighter risk

| | |
| --- | --- |
| **What changes** | SL=200, TP=300 (RR=1.5 preserved) |
| **Metric targeted** | AL, R≈RR, WR, E_N, BWR |
| **Expected effect** | Isolates distance scale vs RR shape |
| **Test preset** | `EDX-P2-T02_SL200_TP300_RR1.5_champFilters_G0_long.set` (magic **8210202**) |
| **Hypothesis** | Scale of stop, not RR, drives AL / survival |
| **Pool bar** | E_N>0, WR>BWR, EF>0 |
| **Status** | `DONE` — **POOL_KEEP** (3M Jul–Sep: WR 44.3%>BWR 40% E_N 0.107 EF 0.96 Fragile thin n=61); `archive/EDX-P2-T02/` |

### EDX-P2-T03 — Wider TP (payoff expansion)

| | |
| --- | --- |
| **What changes** | TP=600, SL=300 (RR=2.0) |
| **Metric targeted** | R, RR−R, WR, E_N |
| **Expected effect** | WR↓, R↑; E_N up only if payoff gain dominates; **G5 reopen priority** (opposite of TP−10 fail) |
| **Test preset** | `EDX-P2-T03_SL300_TP600_RR2_champFilters_G0_long.set` (magic **8210203**) |
| **Hypothesis** | Under-harvesting winners / need TP headroom for G5 |
| **Pool bar** | E_N>0, WR>BWR, EF>0 |
| **Status** | `DONE` — **POOL_DROP** (3M: WR 32%<BWR 33% E_N−0.04 EF−3.17); `archive/EDX-P2-T03/` |

### EDX-P2-T04 — Closer TP (reduce RR−R from missed TPs)

| | |
| --- | --- |
| **What changes** | TP=300, SL=300 (RR=1.0) |
| **Metric targeted** | WR, R, RR−R, E_N |
| **Expected effect** | WR↑, R↓ toward 1; **likely reject** given G5 TP−10 already EF≤0 |
| **Test preset** | `EDX-P2-T04_SL300_TP300_RR1_champFilters_G0_long.set` (magic **8210204**) |
| **Hypothesis** | Designed RR too ambitious vs mean distance → RR−R leak |
| **Status** | `DONE` — **POOL_KEEP · current champion** Harvest (Long: WR 54.5%>BWR 50% E_N 0.091 EF 1.77; 3M: WR 59% E_N 0.184 EF 6.43); `archive/EDX-P2-T04/` + `EDX-POOL_WINDOWS/` |

### EDX-P2-T05 — Prefer MID exit (disable far TP)

| | |
| --- | --- |
| **What changes** | `InpTP_Points=0` (SL remains); SMA mid-exit (code supports TP=0) |
| **Metric targeted** | R, MID share, AL, E_N |
| **Expected effect** | Realisation → MID_HEAVY; R typically <1.5; WR may ↑ |
| **Test preset** | `EDX-P2-T05_SL300_TPoff_MIDexit_champFilters_G0_long.set` (magic **8210205**) |
| **Hypothesis** | Fixed TP fights mean-rev class; MID improves E_N |
| **Status** | `DONE` — **costs_fragile** (3M: WR≈BWR E_N+0.01 EF−2.64); `archive/EDX-P2-T05/` |


### EDX-P2-T06 — Time stop (bars)


|                     |                                                         |
| ------------------- | ------------------------------------------------------- |
| **What changes**    | Code + input: max hold bars (e.g. 24) → close at market |
| **Metric targeted** | AL, duration, swap Leak, E_N                            |
| **Expected effect** | Cut overnight/slow losers; may cut winners              |
| **Test preset**     | `EDX-P2-T06_timeStop24bars_G0_long.set`                 |
| **Hypothesis**      | AL inflated by long adverse holds / swap                |
| **Beat**            | E_N, EF; Leak↓                                          |
| **Status**          | `PENDING` *(blocked until code)*                        |


### EDX-P2-T07 — Breakeven move after +0.5R MFE


|                     |                                                 |
| ------------------- | ----------------------------------------------- |
| **What changes**    | Code: move SL to entry after MFE≥0.5R           |
| **Metric targeted** | AL, WR, R                                       |
| **Expected effect** | Fewer full −1R after partial favorable; R may ↓ |
| **Test preset**     | `EDX-P2-T07_BE_after_0.5R_G0_long.set`          |
| **Beat**            | E_N, EF vs P0                                   |
| **Status**          | `PENDING` *(blocked until code)*                |


### EDX-P2-T08 — ATR trail


|                     |                                        |
| ------------------- | -------------------------------------- |
| **What changes**    | Code: trail = 2.5×ATR                  |
| **Metric targeted** | R, RR−R, AL                            |
| **Expected effect** | Capture extension; reduce giveback     |
| **Test preset**     | `EDX-P2-T08_trailATR2.5_G0_LON-NY.set` |
| **Beat**            | E_N, EF vs P0                          |
| **Status**          | `PENDING` *(blocked until code)*       |


### EDX-P2-T09 — Partial TP ladder (50% at 1R, rest at RR)


|                     |                                             |
| ------------------- | ------------------------------------------- |
| **What changes**    | Code: partial close                         |
| **Metric targeted** | AW, R, event aggregation (still one event)  |
| **Expected effect** | Smoother R; lower variance                  |
| **Test preset**     | `EDX-P2-T09_partialTP_50pct_1R_G0_long.set` |
| **Beat**            | E_N, EF; σ_R↓ bonus                         |
| **Status**          | `PENDING` *(blocked until code)*            |


### EDX-P2-T10 — Payoff pool lock


|                     |                                                                 |
| ------------------- | --------------------------------------------------------------- |
| **What changes**    | Document P2 KEEP mix (no single winner required)                |
| **Metric targeted** | Pool admission on scored windows                                |
| **Expected effect** | Growth / Survival / Harvest / scale sleeves available           |
| **Test preset**     | See `doc/candidate_pool.md` (T01, T02, T04 KEEP; T05 fragile)   |
| **Accept**          | ≥2 roles with E_N>0 and WR>BWR                                  |
| **Status**          | `DONE` — pool locked from T01–T05 (3M+long); T03 DROP           |


---

## PHASE 2.5 — ENTRY QUALITY / SIGNAL HYGIENE (`EDX-P25`)

Separate from regime filters: improve **which** fades fire, holding payoff + champ filters fixed.

**Base (pool Growth / P25):** `EDX-P4-T01_champion_T05_currency_G0_long.set` — SL300/TP450, session 12–20, skip Tue, magic **8210401**.  
**Pool bar:** E_N>0, WR>BWR (EF>0 preferred). Report Δ vs Growth long; do not DROP solely for lower E_N if admission holds.

### EDX-P25-T01 — BBDev sensitivity (±)


|                     |                                                                                          |
| ------------------- | ---------------------------------------------------------------------------------------- |
| **What changes**    | BBDev=2.0 vs 2.4 vs base 2.2 (payoff + champ filters held)                               |
| **Metric targeted** | n, WR, E_N, EF                                                                           |
| **Expected effect** | Wider k → fewer events, possibly higher WR                                               |
| **Test presets**    | `EDX-P25-T01a_BBDev2.0_GrowthBase_G0_long.set` (magic **8212501**) · `EDX-P25-T01b_BBDev2.4_GrowthBase_G0_long.set` (**8212502**) |
| **Pool bar**        | E_N>0, WR>BWR (EF>0 preferred); Δ vs Growth long                                         |
| **Status**          | `DONE` — T01a **DROP** on 3M (EF≤0); Long KEEP dominated. T01b **KEEP** promising (Long→Aug31 EF 5.58; 3M→Sep24 EF 6.28) but n&lt;385 / end≠Sep24 — hold Growth base. `archive/EDX-P25-T01/` |


### EDX-P25-T02 — Cooldown increase


|                     |                                                              |
| ------------------- | ------------------------------------------------------------ |
| **What changes**    | CooldownBars=6 (base=3)                                      |
| **Metric targeted** | DEPENDENCE, WR, frequency                                    |
| **Expected effect** | Less re-entry into same impulse                              |
| **Test preset**     | `EDX-P25-T02_cooldown6_GrowthBase_G0_long.set` (magic **8212503**) |
| **Pool bar**        | E_N>0, WR>BWR; no FREQUENCY_STALL                            |
| **Status**          | `DONE` — **KEEP** but neutral vs Growth (Long n408 EF 5.35 ≈ 5.18; no stall). Hold Cooldown=3. `archive/EDX-P25-T02/` |


### EDX-P25-T03 — One-side isolation (buy-only / sell-only)


|                     |                                                                                          |
| ------------------- | ---------------------------------------------------------------------------------------- |
| **What changes**    | AllowBuy xor AllowSell                                                                   |
| **Metric targeted** | BM by side                                                                               |
| **Expected effect** | Asymmetry discovery                                                                      |
| **Test presets**    | `EDX-P25-T03a_buyOnly_GrowthBase_G0_long.set` (**8212504**) · `EDX-P25-T03b_sellOnly_GrowthBase_G0_long.set` (**8212505**) |
| **Status**          | `DONE` — Buy long **DROP** (EF −0.38); Sell long KEEP dominated (EF 1.72 ≪ Growth 5.18). Sell>buy asymmetry; keep both sides. `archive/EDX-P25-T03/` |


---

## PHASE 3 — FILTERS & REGIME DETECTION (`EDX-P3`)

Convert P1 cells into entry filters. Payoff/entry champion frozen.

**Justification rule:** exclude cell only if `BM_cell ≤ 0` with `n ≥ 30`, **or** retained subset improves EF without frequency < 50% of P0 baseline (`FREQUENCY_STALL`).  
After filter: note evidence tier — **n < 385 ⇒ cannot claim gate pass**.

### EDX-P3-T01 — Session filter from P1


|                    |                                                                                    |
| ------------------ | ---------------------------------------------------------------------------------- |
| **Test preset**    | `EDX-P3-T01_session_1200-2000_G0_long.set` (StartHour=12)                          |
| **Changed inputs** | `InpStartHour=12` (was 8)                                                          |
| **Hypothesis**     | Drop thin LON morning; keep LON–NY/NY edge                                         |
| **Beat P0**        | E_N ≥ 0.118R, EF ↑, n ≥ ~285                                                       |
| **Status**         | `DONE` — **REJECT** (E_N/EF down vs P0; final 515 vs 591); see `EDX-P3_FILTERS.md` |


### EDX-P3-T02 — Skip Tuesday


|                    |                                                        |
| ------------------ | ------------------------------------------------------ |
| **Test preset**    | `EDX-P3-T02_skipTue_G0_long.set`                       |
| **Changed inputs** | `InpTradeTue=false`                                    |
| **Hypothesis**     | Tuesday BM≤0 cell removed → EF ↑                       |
| **Beat P0**        | E_N ≥ 0.118R, EF ↑, n ≥ ~285                           |
| **Status**         | `DONE` — **ACCEPT** (E_N +0.014R, EF +0.57 pp); modest |


### EDX-P3-T03 — BB width regime gate ON


|                     |                                             |
| ------------------- | ------------------------------------------- |
| **What changes**    | `InpUseBBWidthRegime=true` + bounds from P1 |
| **Metric targeted** | EF, n                                       |
| **Test preset**     | `EDX-P3-T03_BBwidthGate_G0_long.set`        |
| **Status**          | `PENDING`                                   |


### EDX-P3-T04 — Trend block (ER filter) — code if needed


|                     |                                           |
| ------------------- | ----------------------------------------- |
| **What changes**    | Skip entries when ER≥0.3                  |
| **Metric targeted** | BM_range vs full; EF                      |
| **Test preset**     | `EDX-P3-T04_blockTrend_ER0.3_G0_long.set` |
| **Hypothesis**      | Class: fade only in range                 |
| **Status**          | `PENDING` *(may need code)*               |


### EDX-P3-T05 — Stacked filters champion


|                     |                                                                                                                      |
| ------------------- | -------------------------------------------------------------------------------------------------------------------- |
| **What changes**    | Combine accepted P3 filters only (StartHour=12 + TradeTue=false)                                                     |
| **Metric targeted** | EF, M, n tier                                                                                                        |
| **Expected effect** | Candidate for Stage 4                                                                                                |
| **Test preset**     | `EDX-P3-T05_session12-20_skipTue_G0_long.set`                                                                        |
| **Accept**          | EF > P0 and EF > M provisional; n≥285 (50% of P0)                                                                    |
| **Status**          | `DONE` — **ACCEPT (champion)** n=420 WR 47.4% E_N +0.185R EF +5.14 pp (Leak 2.24) → Robust*; see `EDX-P3_FILTERS.md` |


---

## PHASE 4 — VALIDATION (`EDX-P4`)

Best candidate = new submission. **No grandfathering.**

### EDX-P4-T01 — G1 production gate


|                     |                                                                                                      |
| ------------------- | ---------------------------------------------------------------------------------------------------- |
| **What changes**    | None — score champion blotter                                                                        |
| **Metric targeted** | EF > M; binomial WR > BWR+Leak; bootstrap R                                                          |
| **Test preset**     | `EDX-P4-T01_champion_T05_currency_G0_long.set` (= T05 stack, magic 8210401)                          |
| **Accept**          | G1 PASS                                                                                              |
| **Status**          | `DONE` — **G1 PASS** (currency; EF 5.18 > M 4.78; WR 47.4% > BWR+Leak; R=1.5); `archive/EDX-P4-T01/` |


### EDX-P4-T02 — G2 anchored walk-forward


|                     |                                                                               |
| ------------------- | ----------------------------------------------------------------------------- |
| **What changes**    | WF protocol; IS objective = max E_N s.t. EF>M                                 |
| **Metric targeted** | WFE ≥ 0.5; OOS E_N>0 in ≥75% folds                                            |
| **Test preset**     | Champion + fold windows documented in archive                                 |
| **Accept**          | G2 PASS                                                                       |
| **Status**          | `DONE` — **G2 PASS** (4/4 OOS E_N>0; mean WFE 0.83); see `SCORECARD_G2_G4.md` |


### EDX-P4-T03 — G3 regime robustness


|                     |                                                                         |
| ------------------- | ----------------------------------------------------------------------- |
| **What changes**    | None / metadata regime_filtered if intentional                          |
| **Metric targeted** | BM_worst > 0; concentration ≤70% unless declared                        |
| **Accept**          | G3 PASS                                                                 |
| **Status**          | `DONE` — **G3 PASS** (`regime_filtered=true`: session 12–20 + skip Tue) |


### EDX-P4-T04 — G4 Monte Carlo (shuffle + block + stress)


|                     |                                                                                     |
| ------------------- | ----------------------------------------------------------------------------------- |
| **What changes**    | None                                                                                |
| **Metric targeted** | P95 MaxDD, median G, P(ruin)                                                        |
| **Accept**          | G4 PASS per unified §7.3                                                            |
| **Status**          | `DONE` — **G4 PASS** (MC-2 P95 DD $60≤$100, P(ruin)=0; MC-3 P(ruin)=0.04%, medG≥C₀) |


### EDX-P4-T05 — G5 perturbation ±10% + cost ×1.5


|                     |                                                                                                             |
| ------------------- | ----------------------------------------------------------------------------------------------------------- |
| **What changes**    | Parameter/cost stress presets                                                                               |
| **Metric targeted** | E_N sign; EF>0 at ×1.5 cost                                                                                 |
| **Test presets**    | `EDX-P4-T05a_…` … `EDX-P4-T05h_…` (family; magics 8210501–508)                                              |
| **Accept**          | G5 PASS                                                                                                     |
| **Status**          | `DONE` — **G5 FAIL** (TP−10 EF −1.60; BBDev+10 & SL+10 missing; magic≠params in log); `archive/EDX-P4-T05/` |


### EDX-P4-T06 — Verdict assembly


|                     |                                                    |
| ------------------- | -------------------------------------------------- |
| **What changes**    | None                                               |
| **Metric targeted** | PRODUCTION-WORTHY = G0∧G1∧G2∧G3∧G4∧G5              |
| **Accept**          | Scorecard published; Canvas updated (display only) |
| **Status**          | `PENDING`                                          |


---

## PHASE 5 — STACKING / REALISATION PREP (`EDX-P5`) *(after production-worthy only)*

### EDX-P5-T01 — f calibration (quarter Kelly pessimistic)


|                     |                                           |
| ------------------- | ----------------------------------------- |
| **What changes**    | RiskPercent to quarter-Kelly of (WR−M, R) |
| **Metric targeted** | f, P95 MaxDD                              |
| **Test preset**     | `EDX-P5-T01_fQuarterKelly_G0_long.set`    |
| **Status**          | `PENDING`                                 |


### EDX-P5-T02 — Grid re-introduction test (optional)


|                     |                                                                        |
| ------------------- | ---------------------------------------------------------------------- |
| **What changes**    | MaxLevels=2 **only if** G0 champion passed; score as **basket events** |
| **Metric targeted** | Basket E_N, EF — must not use ticket WR                                |
| **Test preset**     | `EDX-P5-T02_gridL2_basketEvents_long.set`                              |
| **Accept**          | Basket EF > M; else keep G0 only                                       |
| **Status**          | `PENDING`                                                              |


---

## 3. Execution board (current)


| Phase    | Next task                      | Preset ready?                       |
| -------- | ------------------------------ | ----------------------------------- |
| P0 / P05 | **Complete**                   | —                                   |
| P1       | Core DONE; ATR/ER/MAE deferred | —                                   |
| P3       | T05 champion locked            | Done                                |
| P4       | **G0–G4 PASS · G5 FAIL** (Growth) | Awaiting Harvest G5 re-run       |
| P2       | **T01–T05 done · pool locked** | Dual windows filled                 |
| P25      | **T01–T03 complete**           | Was Growth-base; champ now Harvest  |
| **→ AOS** | **Active stream**             | `doc/ai_OS.md` · `aistack`          |


### What you do now

**EDX main stream is closed.** Operational engine remains Harvest; active work is the **AI OS** wrap (not new SL/TP discovery).

**Current champion:** `EDX-P2-T04_SL300_TP300_RR1_champFilters_G0_long.set` — magic **8210204** · SL300/TP300 · RR=1 · BWR 50%.

| Role | Preset | Notes |
| --- | --- | --- |
| **Champion (engine)** | Harvest P2-T04 | Primary; next G5 / hygiene base |
| Secondary | Growth P4-T01 | Best long EF; G0–G4 / G5 fail |
| Blend | + Survival | Regime stress |
| **Paper OS** | `aistack` magic **8399001** | AOS L2AI+L3+L4 · long EF 5.45 Robust in tester · **STAY_PAPER** |

**Suggested next (pick one):**  
1. Continue AOS — stronger L1 features / P5 retrain / L10 (see `doc/ai_OS.md` board).  
2. G5 re-run on **Harvest** (±10% BBDev/SL/TP/Risk%, cost ×1.5).  
3. P2-T06–T09 only when coded.

Docs: `system_profile.md` · `doc/edge_framework.md` v1.1.2 · `doc/candidate_pool.md` · `doc/ai_OS.md` v0.2.

---

## 4. Delta report format (every completed task)

```text
TASK: EDX-P#-T##
PRESET: ... / pool_role: Growth|Survival|Harvest|Scale|Mid|Other
n, WR, AW, AL, R, RR, RR-R, BWR, BM, FMI, Leak, EF, M, E_N, PF, MaxDD
Δ vs Harvest (P2-T04 champion): ...
ZONE: Negative|Fragile|Robust
SIDE_DIAGNOSIS: WR|R|BOTH
POOL: KEEP|DROP|costs_fragile|DOMINATED (flavour note)
GATES: G0..G5 or n/a
ARCHIVE: blotter/archive/EDX-P#-T##/
```

---

## 5. Document map


| File                                           | Role                         |
| ---------------------------------------------- | ---------------------------- |
| `doc/edge_discovery.md`                        | This plan (EDX — engine isolation; **main stream closed**) |
| `doc/ai_OS.md`                                 | AI OS wrap plan (AOS layers · **active** · v0.2 EA-wired) |
| `doc/aos_aistack.md`                           | aistack preset / wiring      |
| `doc/candidate_pool.md`                        | Deployable sleeve registry   |
| `doc/edge_framework.md`                        | BMRG scoring contract v1.1.2 |
| `doc/unified_edge_framework.md`                | Maths / gates                |
| `system_profile.md`                            | Class + pool behavioural map |
| `blotter/`                                     | Inbox / archive (EDX + AOS)  |
| `.cursor/rules/blotter-clear-after-review.mdc` | Auto-clear after review      |


