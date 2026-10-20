# AUDUSD — Edge Framework

**Version:** 0.1.0  
**Status:** Normative for **AUDUSD Book A** benchmarking (research expansion)  
**Parent:** `doc/unified_edge_framework.md` v1.0  
**Companions:** `doc/assets/AUDUSD/system_profile.md` · `doc/presets/BOOKA.md`  
**Preset:** `Profiles/Tester/BMRG/BOOKA-Harvest_AUDUSD_M5_G0.set`  
**Magic:** **8221103** · AOS **OFF**  
**Primary evidence:** 2026.05.01 → 2026.08.31 · see `blotter/archive/BOOKA-AUDUSD-20261007/`

This document **binds** the unified edge framework to the AUDUSD Harvest extract. Where this file and the unified doc conflict on **AUDUSD procedure**, **this file wins**. Formulae remain those of the unified doc.

**Not** the EURUSD live / EDX binding (`doc/edge_framework.md` · magic `8210204`). Do not mix scorecards.

---

## 0. Canvas caveat

| Artifact | Role | Authority |
| --- | --- | --- |
| **This markdown** | Contract: score AUDUSD Book A, gates, adapter, gap fillings | **Normative** |
| **`doc/unified_edge_framework.md`** | Shared maths, stages, G0–G5 | Normative for **formulae** only |
| **`doc/assets/AUDUSD/system_profile.md`** | Class thesis · observed behaviour | Evidence / descriptive |
| **`doc/presets/BOOKA.md`** | Book A intent · geometry lock · asset order | Process |
| **`blotter/archive/BOOKA-AUDUSD-*/`** | Immutable scored runs | Evidence of record |
| **Canvas / chat charts / UI tiles** | Visual snapshot of a scorecard | **Display only** |

**Rules**

1. **Canvas ≠ verdict.** A chart, canvas, or dashboard tile never overrides a blotter scored under this document.  
2. **System profile ≠ gate pass.** Profile metrics (especially journal-derived WR/E_N without deal costs) are **descriptive** until Leak is measured.  
3. Changing 1R definition, event aggregation, cost defaults, expansion/production tiers, or gate bindings **bumps this version**.  
4. Refresh any Canvas **from the scorecard only** after a scored run — never invent EF/Leak on the canvas.

---

## 1. Gaps in the unified framework — AUDUSD fillings

The unified doc is strategy- and symbol-agnostic. These bindings close the gaps for this asset.

| # | Unified gap | AUDUSD Book A binding |
| --- | --- | --- |
| **A-A** | Trade event / grid | G0 only: MaxLevels=1 · MaxEntries=1 → **ticket = event**. Ticket WR with levels>1 is G0 fail. |
| **A-B** | 1R declaration | Hard SL: `1R = InpSL_Points × volume × tick value` at entry. Designed SL = **300** points. Scorecard states SL. |
| **A-C** | RR vs realised R | Benchmark on **R**, never assume RR. Designed RR = **1.0**. Monitor `RR − R`. FIXED_RR_FADE expected (MID ≈ 0). |
| **A-D** | Instrument costs | AUDUSD M5: spread often wider than EURUSD. Default until deal-measured: **3 × entry_spread_pts / 300** → `c_R`. Commission + **overnight swap mandatory** (holds often ≥12h). |
| **A-E** | Regime tags vs filters | Declared `regime_filtered=true` via session **12–20** + **skip Tue**. G3 may use that declaration; still prefer ATR×ER cells when tagged. Tip softness (e.g. Sep) = **regime leak (L3)**, not auto class death. |
| **A-F** | Point transfer | SL/TP **EURUSD-calibrated**. AUDUSD ATR mismatch is an expected L3/L4 diagnostic. Retune points only after Leak/RR−R fail — not from raw $ alone. |
| **A-G** | Pips mode | **Inadmissible** for Stage 1–3. ACCOUNT CURRENCY only. |
| **A-H** | Min-lot vs f | Report `f_declared` (0.5%) and `f_realised`. $400 often floors to 0.01 lot → Stage 3 uses **f_realised**. |
| **A-I** | Session vs inventory | Entries gated 12–20; exits continue → overnight path in Leak / MC. |
| **A-J** | Pause / daily flat | Keep in blotter; tag `exit_reason` (`DAILY_FLAT`, `EQUITY_HALT`, …). |
| **A-K** | Preset identity | `preset_id`, magic **8221103**, ea_version must match. Mismatch → G0 fail. |
| **A-L** | Baseline frequency | Provisional **~40–60 events / 90d** from May→Aug (~14–15 / 30d). Recalibrate after longer blotter. FREQUENCY_STALL = 90d count &lt; 50% of baseline. |
| **A-M** | Mid rarity | Mid share &lt;5% → realisation `FIXED_RR_FADE`. |
| **A-N** | Expansion vs production | Book A AUDUSD is **asset expansion**, not live replace. Use **two verdict ladders** (§7): `EXPANSION_*` (small-n OK) vs `PRODUCTION-WORTHY` (full G0–G5). |
| **A-O** | Sample-size vs unified tiers | Unified Standard tier needs n≥385. Expansion soft scorecard allows **Provisional** labels at n≥30 with Wilson `M`, but **cannot** claim PRODUCTION-WORTHY or Robust production gate. |
| **A-P** | USD-fade cluster | AUDUSD correlates with EURUSD/GBPUSD. Expansion KEEP ≠ independent Stage-3 capital. Diversification engine is out of scope here. |
| **A-Q** | AOS | Book A / research champ (**8230901**) stays AOS OFF. **AUDUSD live** = magic **8230931** Risk 3% (`AUDUSD-AIOS_SCALE_Risk3_champ_G0`). FT twin **8230921** @ 0.5%. n / full G0–G5 **not** live deny rules. Do not score L2 on research magics. AUD L2 pin `L2skip_aud_p90_20261008_122523`. |
| **A-R** | Window policy | Primary = stated tester window (currently May→Aug). Trailing complete months = stress. Incomplete tip month = footnote. Prior longer windows (May→Oct / Jan→Oct) = **regime context**, not automatic reject. |
| **A-S** | Side of edge | Class is **WR-side** meanrev (RR=1). Soft target: WR ≫ BWR; do not “fix” by shrinking AL as default. |
| **A-T** | Hygiene pockets | Profile flags Mon + hour-12 weak. Optional filter experiments need a **new preset_id**; do not silently change 8221103 mid-book. |

---

## 2. Trade-event contract

### 2.1 Geometry

| Mode | Inputs | Event rule | Gates? |
| --- | --- | --- | --- |
| **G0** (required) | MaxLevels=1, MaxEntries=1, hard SL 300 | One lifecycle = one event | Yes |
| Grid basket | Levels or entries > 1 | Basket flat = one event | Out of Book A scope |
| Mixed as tickets | — | — | **G0 fail** |

### 2.2 Win / loss

- Win: `pnl_R > 0` after costs  
- Loss: `pnl_R < 0`  
- Scratch (`pnl_R = 0`): exclude from WR/R; keep in frequency/cost  

### 2.3 `exit_reason`

`TP` · `SL` · `MID` · `DAILY_FLAT` · `EQUITY_HALT` · `FAIL_PAUSE` · `MANUAL` / `EOT` · `OTHER`

### 2.4 Identity metadata (required)

```text
ea_name: BMRG
symbol: AUDUSD
timeframe: M5
magic: 8221103
preset_id: BOOKA-Harvest_AUDUSD_M5_G0
geometry_mode: G0_SINGLE
designed_rr: 1.0
risk_definition: hard_stop_points
regime_filtered: true          # session 12-20 + skip Tue
baseline_frequency: 50         # events / 90d provisional
pool_role: BookA_Harvest_AUD
aos_overlay: none
costs_defaulted: <list or none>
```

### 2.5 `event_id`

```text
event_id = "8221103-AUDUSD-{side}-{YYYYMMDDhhmmss}-{first_ticket}"
```

---

## 3. Stage 0 — Core identities (bound)

```
BWR = 1 / (1 + R)
BM  = WR − BWR
E_N = WR × (R + 1) − 1 = (R + 1) × BM
```

### 3.1 Designed geometry

| Field | Value | Intent |
| --- | --- | --- |
| SL / TP | **300 / 300** | RR = 1.0 · BWR(RR) = **50%** |
| BB | 20 / **2.2** | Entry threshold |
| Session | **12–20** · skip Tue | Regime filter |
| Class | Mean reversion fade | WR-side edge |

### 3.2 Soft targets (expansion · after costs when known)

| Metric | Soft target | Fail / worry signal |
| --- | --- | --- |
| WR | > BWR; prefer ≥ 55% | ≤ BWR after Leak on W20+ |
| R | ≈ RR (±10% on FIXED_RR) | R ≪ RR without WR lift |
| BM | > 0; prefer ≥ +5 pp clean window | BM ≤ 0 |
| E_N | > 0; prefer ≥ +0.05R | ≤ 0 on W20/W30 **and** a calendar month |
| Soft stress month | WR ≳ 45–50% | Wipeout → regime/ATR review, not auto EXPANSION_DROP |
| RR − R | ~0 | Gap > 25% of baseline → execution/exit audit |

### 3.3 Side diagnosis (locked)

**WR-side.** Edge = WR margin above 50% BWR at R≈1. Filters / session / optional Mon·hour-12 hygiene before payoff surgery.

---

## 4. Stage 1 — Cost, Leak, EF

### 4.1 Cost defaults (`costs_defaulted` until deal blotter)

| Component | AUDUSD default |
| --- | --- |
| Spread | Mean entry spread (pts) from blotter; else session median |
| Round-turn proxy | **3 × spread_pts** → `c_R = (3 × spread_pts) / 300` |
| Commission | Broker card (else 0 flagged) |
| Swap | Broker × nights held (**mandatory** — long holds common) |
| Slippage | Inside 3× proxy until fill fields exist |

```
Leak = c_R / (R + 1)     # as fraction of WR → report in pp
EF   = BM − Leak
```

**Double-counting:** only L1 inside EF. L2 = `M` threshold. L3–L5 = gates/monitors (unified §4.2).

### 4.2 Uncertainty `M`

```
M = 1.96 × sqrt(WR × (1 − WR) / n)     # pp when WR as fraction×100 consistently
```

For **n &lt; 200** use **Wilson** half-width (unified FX-07). Expansion scorecards must state which.

### 4.3 Zones

| Zone | Condition | Expansion action | Production action |
| --- | --- | --- | --- |
| Negative | EF ≤ 0 | EXPANSION_DROP or costs_fragile | Reject |
| Fragile | 0 &lt; EF ≤ M | EXPANSION_KEEP / research small-f | Not production-worthy |
| Robust | EF > M | Eligible deepen sample / Stage 2 | Eligible Stage 2/4 |

### 4.4 Provisional baseline (May→Aug 2026 · journal-gross)

> Descriptive until deal export. Assumes R ≈ 1.0 FIXED_RR; Leak **illustrative** at spread≈10 pts → `c_R ≈ 0.10`, Leak ≈ **5.0 pp**.

| Metric | Value | Note |
| --- | ---: | --- |
| n | 58 | **Insufficient** for production G0 (need ≥385 combined) |
| WR / R | 62.1% / ≈1.0 | Profile |
| BWR / BM | 50% / **+12.1 pp** | Gross |
| E_N | **+0.241R** | Gross |
| Leak (default proxy) | ~5.0 pp | Replace with measured |
| EF (proxy) | ~**+7.1 pp** | Gross−proxy |
| M (normal approx) | ~**±12.5 pp** | n small → Wilson preferred |
| Zone (proxy) | **Fragile / Insufficient n** | EXPANSION_KEEP candidate, not production |

**Rule:** Do not promote “Robust” from this row. Deal blotter first.

---

## 5. Stage 2 — Health windows

Unified W100/W250/W500 assume large n. AUDUSD Book A adds **small-n windows** until n≥250.

| Window | Size | Step | Role on AUDUSD |
| --- | ---: | ---: | --- |
| **W15** | 15 | 7 | Fast / noisy investigation |
| **W20** | 20 | 10 | Expansion main until n grows |
| **W30** | 30 | 15 | Expansion confirm |
| W100 | 100 | 25 | Adopt when n allows |
| W250 | 250 | 25 | Lifecycle (production path) |
| W500 | 500 | 25 | Confirm |
| Cal 30d / month | — | — | Soft stress · frequency |
| Trailing 3 complete months | — | — | Regime weight |

### 5.1 Lifecycle (expansion-scaled)

Until n≥250, evaluate on **W20 confirmed by W30** (and monthly E_N):

| State | Condition (expansion) | Action |
| --- | --- | --- |
| Expanding | EF>M (or BM>0 if Leak pending) and ΔD≥0 on 2 evals | Continue sample |
| Stable | EF>M / BM>0, |ΔD| small | Routine |
| Compressing | Margin falling 2 evals | Investigate: regime tip vs execution (§9) |
| Near frontier | 0 &lt; EF ≤ M | Cap research f; no live |
| Below frontier | EF≤0 on W20 **and** W30 | Halt this preset; regime/ATR review |

Unified Stage 2 halt rules apply unchanged once W250/W500 exist.

### 5.2 Profile rolling snapshot (gross, May→Aug)

| Family | Result |
| --- | --- |
| Months | All four E_N > 0 (May +0.38R … Aug +0.20R) |
| 30d roll | Full pockets E_N ≥ +0.08R; stub Aug17 n=6 flats |
| W15 / W20 / W30 | E_N ≥ 0 throughout sample |

---

## 6. Stage 3 — Capital (research only)

| Item | Binding |
| --- | --- |
| Intent | Rank / size **research** capital only — **not** live FT attach |
| f_declared | 0.5% |
| f_realised | From equity_at_open × risk_ccy; expect min-lot floor |
| Kelly | Quarter–half of shrunk WR; **cap research ≤0.5%** until G1 Robust |
| DD_limit | 25% default; EA equity halt 15% OK if tighter |
| Daily loss | 3% + flatten in path / MC |
| Ruin | P(equity ≤ 0.5 C₀) ≤ 1% |
| Cluster | Do **not** stack full f with EUR/GBP Book A as “diversified” |

Stage 3 ranking among Book A assets is allowed only after each has deal-scored EF and the same cost policy.

---

## 7. Stage 4 — Gates (two ladders)

### 7.1 Expansion ladder (Book A · asset list)

Use while building the research asset list **before** per-symbol AIOS / live claims.

| Gate | Expansion pass |
| --- | --- |
| **E0** | Currency · G0 · preset/magic match · costs policy stated |
| **E1** | Gross or measured: WR > BWR · E_N > 0 on primary window · soft-stress month not wipeout |
| **E2** | ≥1 secondary window (other calendar length) not contradicting class (regime tip OK if primary holds) |
| **E3** | `regime_filtered` documented; tip failures labeled L3 not silent DROP |
| **E4** | n recorded; if n&lt;100 verdict = EXPANSION_KEEP / WATCH only |

```
EXPANSION_KEEP   = E0 ∧ E1 ∧ E2 ∧ E3
EXPANSION_WATCH  = E0 ∧ E1 but thin n or Fragile EF
EXPANSION_DROP   = EF≤0 after measured Leak on primary, or class break (not mere tip regime)
```

**May→Aug provisional label:** **EXPANSION_KEEP** (gross) · pending Leak → may move to WATCH if EF≤0.

### 7.2 Production ladder (unified G0–G5)

Unchanged maths from `unified_edge_framework.md`. AUDUSD notes:

| Gate | AUDUSD notes |
| --- | --- |
| **G0** | Currency; G0; preset match; n≥385 IS+OOS combined |
| **G1** | EF>M full + W500; WR > BWR+Leak; R bootstrap |
| **G2** | Anchored WF; WFE≥0.5; OOS E_N>0 in ≥75% folds — **re-select ATR/points on IS only** if retuning |
| **G3** | BM_worst>0 **or** declared regime_filtered (session+Tue); concentration flag if &gt;70% in one ATR×ER cell |
| **G4** | MC-1/2/3; block 20; **overnight** path mandatory |
| **G5** | ±10% BBDev, SL, TP, Risk%; EF>0 at cost ×1.5; SL/TP perturbation interprets point-transfer risk |

```
PRODUCTION-WORTHY(AUDUSD) = G0 ∧ G1 ∧ G2 ∧ G3 ∧ G4 ∧ G5
```

**Status (2026-10-07):** **NOT PRODUCTION-WORTHY** (n insufficient · Leak unmeasured · G1–G5 not run). Live remains EURUSD `8210204` + INF.

---

## 8. Adapter bindings (blotter)

Follow unified §8 plus:

| Extra field | Required | Note |
| --- | --- | --- |
| `exit_reason` | yes | §2.3 |
| `spread_points_entry` | yes* | *or costs_defaulted |
| `nights_held` | yes* | swap |
| `session_ok` | no | diagnostic |
| `signal_tag` | no | buy/sell fade |
| `group_event_id` | yes | = event_id on G0 |

Forbidden evidence: pips-mode Stage 1–3 · ticket WR with grid · preset mismatch · profit-only optimise · incomplete tip month as primary admission · scoring AOS on 8221103.

---

## 9. Benchmark protocol

1. Load `BOOKA-Harvest_AUDUSD_M5_G0` · AUDUSD M5 · every tick · ACCOUNT CURRENCY.  
2. Confirm Inputs = preset (SL/TP 300, BBDev 2.2, 12–20, skip Tue, magic 8221103, AOS off).  
3. Export deals → `blotter/inbox/` → archive `blotter/archive/BOOKA-AUDUSD-<date>/`.  
4. Aggregate events → WR, R, BWR, BM, Leak, EF, M, E_N, RR−R.  
5. Emit W15/W20/W30 (+ W100+ when able) and calendar months.  
6. Apply **expansion ladder**; only then schedule production G0–G5.  
7. Update `system_profile.md` evidence tables from scorecard.  
8. Refresh Canvas from scorecard only (display).

---

## 10. Monitoring / investigation (AUDUSD)

| Trigger | Response |
| --- | --- |
| WR ≤ BWR on W20 | Investigate Mon / hour-12 / ATR scale |
| EF ≤ 0 after Leak | costs_fragile or EXPANSION_DROP |
| Tip month wipeout, primary OK | Label **regime mismatch (L3)**; optional ATR retune task — do not silent DROP |
| RR−R gap > 25% | Exit mix / slippage / flatten audit |
| FREQUENCY_STALL | Session/cooldown only via new preset task |
| Max loss streak > 1.5× expected | Block-bootstrap before any f increase |
| Correlation spike with live EUR | Do not raise Book A f as diversification |

Investigation order (unified): **data → execution → regime → structural**.

---

## 11. Scorecard fields

```text
framework_unified: 1.0
framework_audusd: 0.1.0
preset_id / magic / geometry_mode / window / n
aos_overlay: none
WR, R, RR, RR-R, BWR, BM, Leak, EF, M, E_N, PF
f_declared, f_realised_mean
lifecycle_window: W20|W30|W250
ΔD
ladder: expansion|production
gates: E0..E4 and/or G0..G5
verdict: EXPANSION_KEEP | EXPANSION_WATCH | EXPANSION_DROP
       | PRODUCTION-WORTHY | NOT PRODUCTION-WORTHY
regime_note: <optional L3 tip note>
canvas: display_only
```

---

## 12. Document map

| File | Purpose |
| --- | --- |
| `doc/unified_edge_framework.md` | General maths & production gates |
| `doc/edge_framework.md` | EURUSD / BMRG champion binding (do not use for AUD) |
| **`doc/assets/AUDUSD/edge_framework.md`** | **This file — AUDUSD Book A binding** |
| `doc/assets/AUDUSD/system_profile.md` | Class + observed behaviour |
| `doc/assets/AUDUSD/edge_discovery.md` | EDX task plan (active) |
| `Profiles/Tester/BMRG/AUDUSD/` | EDX loadable presets |
| `doc/presets/BOOKA.md` | Book A geometry & asset list |
| `blotter/archive/BOOKA-AUDUSD-*/` | Immutable AUD reviews |

---

## 13. Versioning

- **0.1.0** — Initial AUDUSD binding: canvas caveat, gap table A-A…A-T, expansion vs production ladders, small-n windows, May→Aug provisional baseline, point-transfer / overnight / cluster fillings.  
- Bump when cost defaults, 1R, event rules, ladder criteria, or baseline frequency change.

---

## 14. One-line contract

**Score AUDUSD Book A as a WR-side G0 mean-reversion fade under unified identities; use expansion gates while n and Leak are thin; never let Canvas or tip-regime noise override a blotter scored here; production-worthy only after full G0–G5 — live FT stays on EURUSD.**
