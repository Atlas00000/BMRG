# AAPL — Edge Framework

**Version:** 0.1.1  
**Status:** Normative for **Apple (AAPL CFD) expansion** benchmarking  
**Parent:** `doc/unified_edge_framework.md` v1.0  
**Companions:** [`system_profile.md`](./system_profile.md) · [`README.md`](./README.md)  
**Presets:** `Profiles/Tester/BMRG/AAPL/`  
**Magics:** **26092501** (Harvest) · **26092502** (Balanced) · AOS **OFF**  
**Primary evidence:** 2025.01.01 → 2026.08.31 · Tester `logs/20261012.log` · profile 2026-10-12

This document **binds** the unified edge framework to the Apple M15 Harvest / Balanced extracts. Where this file and the unified doc conflict on **AAPL procedure**, **this file wins**. Formulae remain those of the unified doc.

**Not** the EURUSD live binding (`doc/edge_framework.md`) · **not** AUDUSD (`doc/assets/AUDUSD/edge_framework.md`). Do not mix scorecards or magics.

---

## 0. Canvas caveat

| Artifact | Role | Authority |
| --- | --- | --- |
| **This markdown** | Contract: score Apple sleeves, gates, adapter, gap fillings | **Normative** |
| **`doc/unified_edge_framework.md`** | Shared maths, stages, G0–G5 | Normative for **formulae** only |
| **`doc/assets/AAPL/system_profile.md`** | Class thesis · observed behaviour · dual-sleeve tables | Evidence / descriptive |
| **`Profiles/Tester/BMRG/AAPL/*.set`** | Locked inputs | Geometry source |
| **Tester logs / future `blotter/archive/AAPL-*/`** | Immutable scored runs | Evidence of record |
| **Canvas / chat charts / UI tiles** | Visual snapshot of a scorecard | **Display only** |

**Rules**

1. **Canvas ≠ verdict.** A chart, canvas, or dashboard tile never overrides a blotter scored under this document.  
2. **System profile ≠ gate pass.** Profile WR / E_N / “true-leak pass” from journal spreads are **descriptive** until a deal blotter measures full `c_R` (spread + commission + swap + slippage).  
3. Changing 1R definition, event aggregation, cost defaults, sleeve identity, expansion/production tiers, or gate bindings **bumps this version**.  
4. Refresh any Canvas **from the scorecard only** after a scored run — never invent EF / Leak / zone on the canvas.  
5. **Tip charts are not admission.** May→Aug tip alone cannot promote EXPANSION_KEEP → production path if the primary long fails measured EF.

---

## 1. Gaps in the unified framework — AAPL fillings

The unified doc is strategy- and symbol-agnostic. These bindings close the gaps for Apple equity CFD.

| # | Unified gap | AAPL binding |
| --- | --- | --- |
| **P-A** | Trade event / grid | G0 only: MaxLevels=1 · MaxEntries=1 → **ticket = event**. Ticket WR with levels>1 is G0 fail. |
| **P-B** | 1R declaration | Hard SL at entry: `1R = InpSL_Points × volume × tick_value`. Harvest SL=**300** · Balanced SL=**320**. Scorecard **must** state sleeve + SL. Apple point = **0.01** price (300 pts = $3.00 per 1.0 lot on this broker path — confirm on deal export). |
| **P-C** | RR vs realised R | Benchmark on **R**, never assume RR. Harvest RR=**1.25** · Balanced RR=**1.50**. Monitor `RR − R`. Expect `FIXED_RR_FADE` plus material **`OTHER`** (gap / slip past SL). |
| **P-D** | Instrument costs | Equity CFD: **wide spread vs FX**, overnight financing, **open-gap risk**. Default until deal-measured: `c_R ≈ (k × entry_spread_pts) / SL_pts` with **k=2** round-turn floor, **plus** swap × nights, **plus** measured gap overrun beyond SL when exit ≠ TP/SL. Preset meta Leak **3.0–3.5 pp is inadmissible** as production Leak — journal med spread/SL ≈ **8.4–9.7 pp** is the interim proxy. |
| **P-E** | Regime tags vs filters | Declared `regime_filtered=true` via **US RTH 14:30–20:00** · **skip Tue** · ATR **50–180** · BB-width **0.40–1.50%**. G3 may use that declaration. Soft 2026 H1 / thin months = **regime leak (L3)**, not auto class death. Earnings weeks = equity-specific L3 cell (tag when available). |
| **P-F** | Geometry origin | SL/TP are **Apple-calibrated** (≈2.8–3.0× M15 ATR p50), not a silent EURUSD point transfer. Still monitor ATR drift; retune points only after Leak / RR−R fail — not from raw $ alone. |
| **P-G** | Pips / points-only PnL | **Inadmissible** for Stage 1–3. ACCOUNT CURRENCY only. |
| **P-H** | Lot vs f | Broker `VOLUME_MIN≈1.0` → **fixed lot 1.0**. Report `f_declared` (preset risk% unused in fixed mode) and `f_realised = risk_ccy / equity_at_open`. On $500, 1R ≈ $3.00–$3.20 → **f ≈ 0.6%**; on larger equity f shrinks. Stage 3 always uses **f_realised**. |
| **P-I** | Session vs inventory | Entries gated to RTH; exits continue → **overnight path mandatory** in Leak, MaxDD, and MC (gaps). |
| **P-J** | Pause / daily flat / OTHER | Keep in blotter; tag `exit_reason` including **`GAP_SL`** / `OTHER` when |move| ≠ TP/SL within tolerance. |
| **P-K** | Preset / sleeve identity | Score **one magic per scorecard**. Harvest **26092501** and Balanced **26092502** never pooled as one WR. `preset_id` + magic + ea_version must match. Mismatch → G0 fail. |
| **P-L** | Baseline frequency | Provisional **~8–10 events / 90d** (~2.7–2.8 / 30d on long window). Low by FX standards — BB-width gate is intentional. `FREQUENCY_STALL` = 90d count &lt; **50%** of baseline (~4–5). |
| **P-M** | Mid / OTHER rarity | MID expected ~0. OTHER share on long ≈ **20–28%** is **equity fingerprint**, not MID-exit logic. If OTHER &gt; 40% on a window → execution/gap audit before geometry change. |
| **P-N** | Expansion vs production | Apple is **asset expansion**, not live replace. Two verdict ladders (§7): `EXPANSION_*` (small-n OK) vs `PRODUCTION-WORTHY` (full G0–G5). |
| **P-O** | Sample-size vs unified tiers | **AAPL does not use n≥385 as a hard criterion.** Report `n` and compute `M` (Wilson if n&lt;200). Verdicts key off **EF vs M**, walk-forward, and regime — not a fixed headcount floor. Tip n&lt;15 = confirmation footnote only, never sole KEEP driver. |
| **P-P** | Equity / FX correlation | Apple is **not** a USD-fade FX twin. Do not treat AAPL KEEP as diversification vs EUR/AUD without a separate covariance engine. Do not stack full research f with live FX as “hedged.” |
| **P-Q** | AOS | Research sleeves stay **AOS OFF**. Do not score EUR L2 / AUD L2 pins on Apple magics. Asset AIOS only after expansion KEEP + deal-scored Leak and a dedicated train tape. |
| **P-R** | Window policy | **Primary** = 2025.01→2026.08 (or successor complete long). **Tip** May→Aug = confirmation. **Jan→Aug 2026** = regime diagnostic. Incomplete tip month = footnote. Hostile H1 labeled L3, not silent DROP if primary long holds after Leak. |
| **P-S** | Side of edge | Harvest = **WR-side** meanrev (target WR ≫ 44.4%). Balanced = **mixed WR + R** (may pass with lower WR if R holds). Do not “fix” Harvest by shrinking AL as default; do not convert either sleeve to trend RR. |
| **P-T** | Hygiene pockets | Profile soft pockets: **Thu**, hour **18**, **2026 H1 buys**. Optional filter experiments need a **new preset_id / magic**; do not silently mutate 26092501/02 mid-book. |
| **P-U** | Dual-sleeve ranking | Compare sleeves only on **identical windows + identical cost policy**. Prefer Harvest as primary expansion sleeve unless Balanced shows strictly better measured EF and MaxDD after costs. |
| **P-V** | Spread gate vs Leak | MaxSpread **40** is an entry filter, not a Leak estimate. Leak always from fills / cost model. |
| **P-W** | BB-width selectivity | Bars in-band ~30–36% — expected. Do not raise frequency by widening BBw max without a new preset and full re-score. |

---

## 2. Trade-event contract

### 2.1 Geometry

| Mode | Inputs | Event rule | Gates? |
| --- | --- | --- | --- |
| **G0 Harvest** | MaxLevels=1, MaxEntries=1, SL300/TP375 | One lifecycle = one event | Yes |
| **G0 Balanced** | MaxLevels=1, MaxEntries=1, SL320/TP480 | One lifecycle = one event | Yes (separate scorecard) |
| Grid basket | Levels or entries > 1 | Basket flat = one event | Out of AAPL expansion scope |
| Mixed as tickets | — | — | **G0 fail** |

### 2.2 Win / loss

- Win: `pnl_R > 0` after costs  
- Loss: `pnl_R < 0`  
- Scratch (`pnl_R = 0`): exclude from WR/R; keep in frequency/cost  

### 2.3 `exit_reason`

`TP` · `SL` · `MID` · `GAP_SL` · `OTHER` · `DAILY_FLAT` · `EQUITY_HALT` · `FAIL_PAUSE` · `MANUAL` / `EOT`

Tolerance for TP/SL classification: |price move − designed distance| &lt; **0.05** price units (5 pts). Else `OTHER` / `GAP_SL`.

### 2.4 Identity metadata (required)

```text
ea_name: BMRG
symbol: Apple          # MT5 ticker; report AAPL in docs
timeframe: M15
magic: 26092501 | 26092502
preset_id: BMRG-M15-AAPL-6M-Harvest_RR1.25 | BMRG-M15-AAPL-6M-Balanced_RR1.5
geometry_mode: G0_SINGLE
designed_rr: 1.25 | 1.50
risk_definition: hard_stop_points
lot_mode: fixed_1.0
regime_filtered: true   # RTH 14:30-20:00 + skip Tue + ATR + BBw
baseline_frequency: 9   # events / 90d provisional
pool_role: Expansion_AAPL_Harvest | Expansion_AAPL_Balanced
aos_overlay: none
costs_defaulted: <list or none>
```

### 2.5 `event_id`

```text
event_id = "{magic}-Apple-{side}-{YYYYMMDDhhmmss}-{first_ticket}"
```

---

## 3. Stage 0 — Core identities (bound)

```
BWR = 1 / (1 + R)
BM  = WR − BWR
E_N = WR × (R + 1) − 1 = (R + 1) × BM
```

Use **realised R** for BWR/BM/E_N on scorecards. Designed BWR(RR) is a sleeve label only.

### 3.1 Designed geometry

| Field | Harvest | Balanced |
| --- | ---: | ---: |
| SL / TP | **300 / 375** | **320 / 480** |
| RR / BWR(RR) | **1.25 / 44.4%** | **1.50 / 40.0%** |
| BB | 20 / **2.5** | same |
| Session | **14:30–20:00** · skip Tue | same |
| ATR / BBw gates | 50–180 · 0.40–1.50% | same |
| Class | Meanrev fade · WR-side | Meanrev fade · mixed WR+R |

### 3.2 Soft targets (expansion · after costs when known)

| Metric | Harvest soft | Balanced soft | Fail / worry |
| --- | --- | --- | --- |
| WR | > BWR; after true Leak prefer ≳ **53%** | > BWR; after true Leak prefer ≳ **49%** | ≤ BWR+Leak on W20+ |
| R | ≈ 1.25 (±15% with gap noise) | ≈ 1.50 (±15%) | R ≪ RR without WR lift |
| BM | > 0; prefer ≥ +5 pp clean window | > 0; prefer ≥ +5 pp | BM ≤ 0 after costs |
| E_N | > 0; prefer ≥ **+0.10R** on primary long | > 0; prefer ≥ **+0.10R** | ≤ 0 on W20 **and** calendar year |
| Soft stress month | WR may &lt; BWR | same | Multi-month cluster << BWR → L3 review, not auto DROP if long EF>0 |
| RR − R | small | small | Gap > 25% of baseline → exit/gap audit |
| MaxDD (research $500 / 1 lot) | soft under ~8–10% | same | Approach EA halt / DD_limit |

### 3.3 Side diagnosis (locked)

| Sleeve | Diagnosis | Implication |
| --- | --- | --- |
| Harvest | **WR-side** | Protect / raise WR (filters, session, optional Thu/buy hygiene) before payoff surgery |
| Balanced | **Mixed WR + R** | May accept lower WR if realised R holds near 1.5; still meanrev, not trend |

---

## 4. Stage 1 — Cost, Leak, EF

### 4.1 Cost defaults (`costs_defaulted` until deal blotter)

| Component | AAPL default |
| --- | --- |
| Spread | Mean entry spread (pts) from blotter; else session median (~27–30 observed) |
| Round-turn proxy | **2 × spread_pts** → `c_R_spread = (2 × spread_pts) / SL_pts` (floor). Prefer measured entry+exit spreads when available |
| Commission | Broker card (else 0 flagged) |
| Swap / financing | Broker × nights held (**mandatory** — ≥70% trades hold ≥12h) |
| Slippage / gap | Measured fill delta; gap overrun beyond SL counted in event PnL and flagged `GAP_SL` |

```
Leak = c_R / (R + 1)     # report in pp of WR
EF   = BM − Leak
```

**Interim journal proxy (until deals):**  
`Leak_proxy ≈ (median_entry_spread_pts / SL_pts)` as a **single-leg lower bound**, or prefer `2×spread/SL` for round-turn. Profile used ~**8.4–9.7 pp** single-leg style — state which proxy on the scorecard.

**Double-counting:** only L1 inside EF. L2 = `M` threshold. L3–L5 = gates/monitors (unified §4.2). Preset `InpAOS_Leak` is **metadata**, not L1.

### 4.2 Uncertainty `M`

```
M = 1.96 × sqrt(WR × (1 − WR) / n)
```

For **n &lt; 200** use **Wilson** half-width (unified FX-07). Expansion scorecards must state which. Small `n` widens `M` (harder to clear `EF > M`) — that is the sample-size effect; there is **no separate n≥385 reject**.

### 4.3 Zones

| Zone | Condition | Expansion action | Production action |
| --- | --- | --- | --- |
| Negative | EF ≤ 0 | EXPANSION_DROP or costs_fragile | Reject |
| Fragile | 0 &lt; EF ≤ M | EXPANSION_KEEP / WATCH · research small-f | Not production-worthy |
| Robust | EF > M | Eligible deepen sample / Stage 2 | Eligible Stage 2/4 |

### 4.4 Provisional baselines (2025.01→2026.08 · journal-gross)

> Descriptive until deal export. R approximated from win/loss means; Leak from spread/SL proxy.

#### Harvest · magic 26092501

| Metric | Value | Note |
| --- | ---: | --- |
| n | 56 | Report only — not a hard floor |
| WR / R_real | 58.9% / ~1.37 | Profile |
| BWR(R) / BM | ~42.2% / ~**+16.7 pp** (if using R_real) · vs designed BWR 44.4% BM **+14.5 pp** | State which BWR on scorecard |
| E_N (designed R form) | **+0.33R** | Gross |
| Leak_proxy | ~**9.0 pp** | Replace with measured `c_R` |
| EF_proxy | ~**+5.5 pp** (BM_designed − Leak_proxy) | Illustrative |
| M (normal approx) | ~**±12.9 pp** | Wilson preferred → zone **Fragile** (EF ≤ M) |
| Zone (proxy) | **Fragile** | EXPANSION_KEEP candidate; deal Leak before stronger claims |

#### Balanced · magic 26092502

| Metric | Value | Note |
| --- | ---: | --- |
| n | 53 | Report only — not a hard floor |
| WR / R_real | 50.9% / ~1.57 | Profile |
| BM vs designed BWR | **+10.9 pp** | Gross |
| E_N | **+0.27R** | Gross |
| Leak_proxy | ~**8.4 pp** | |
| EF_proxy | ~**+2.5 pp** | Thinner than Harvest |
| M | ~**±13.5 pp** | EF ≪ M → Fragile |
| Zone (proxy) | **Fragile** | EXPANSION_KEEP / WATCH |

**Jan→Aug 2026 diagnostic (both sleeves):** WR 50% / 45.5% with Leak_proxy ~8–9 pp → **EF_proxy ≤ 0** → true-leak **fail**. Label **L3 regime**, do not alone EXPANSION_DROP if primary long EF_proxy > 0.

**Rule:** Do not promote “Robust” from these rows. Deal blotter first.

---

## 5. Stage 2 — Health windows

Unified W100/W250/W500 assume large n. AAPL expansion adds **small-n windows** until n≥250.

| Window | Size | Step | Role on AAPL |
| --- | ---: | ---: | --- |
| **W10** | 10 | 5 | Fast / noisy (use for investigation only) |
| **W15** | 15 | 5–7 | Fast expansion signal |
| **W20** | 20 | 10 | **Expansion main** until n grows |
| **W30** | 30 | 15 | Expansion confirm (when n allows) |
| W100 | 100 | 25 | Adopt when n allows |
| W250 | 250 | 25 | Lifecycle (production path) |
| W500 | 500 | 25 | Confirm |
| Cal month / 30d | — | — | Soft stress · frequency · L3 label |
| Year split | — | — | Regime weight (2025 vs 2026) |

### 5.1 Lifecycle (expansion-scaled)

Until n≥250, evaluate on **W20 confirmed by W15/W30** (and monthly / year E_N):

| State | Condition (expansion) | Action |
| --- | --- | --- |
| Expanding | EF>M (or BM>Leak_proxy if costs pending) and ΔD≥0 on 2 evals | Continue sample |
| Stable | EF>M / BM>Leak_proxy, \|ΔD\| small | Routine |
| Compressing | Margin falling 2 evals | Investigate: H1 regime vs execution (§10) |
| Near frontier | 0 &lt; EF ≤ M | Cap research f; no live |
| Below frontier | EF≤0 on W20 **and** long primary | Halt this preset; regime / cost review |

Unified Stage 2 halt rules apply unchanged once W250/W500 exist.

### 5.2 Profile rolling snapshot (gross · primary long)

| Family | Harvest | Balanced |
| --- | --- | --- |
| Year 2025 | WR 64.7% · E_N +0.46R · +$62 | WR 56.2% · E_N +0.41R · +$54 |
| Year 2026 | WR 50.0% · E_N +0.13R · +$10 | WR 42.9% · E_N +0.07R · +$4 |
| W10 avg E_N | ~+0.30R (min deep in 2026 H1) | ~+0.23R (min deeper) |
| W20 avg E_N | ~+0.26R | ~+0.18R |
| Tip May→Aug | WR 75% · n=8 | WR 62.5% · n=8 |

---

## 6. Stage 3 — Capital (research only)

| Item | Binding |
| --- | --- |
| Intent | Rank / size **research** capital only — **not** live FT attach |
| Lot | Fixed **1.0** until broker allows smaller / risk mode unlocked |
| f_realised | `risk_ccy / equity_at_open` per event |
| Kelly | Quarter–half of shrunk WR; **cap research** so P95 MaxDD stays ≤ DD_limit at 1.0 lot path |
| DD_limit | **25%** default; EA equity halt 15% OK if tighter |
| Daily loss | Preset daily-loss % + flatten in path / MC |
| Ruin | P(equity ≤ 0.5 C₀) ≤ 1% |
| Overnight | MC **must** include gap/`OTHER` path — shuffle-only MC understates Apple risk |
| Cluster | Do **not** stack full research notional with live FX books as diversification |

Stage 3 ranking vs other expansion equities only after each has deal-scored EF and the same cost policy.

---

## 7. Stage 4 — Gates (two ladders)

### 7.1 Expansion ladder (asset list · pre-AIOS)

Use while building the research equity list **before** Apple AIOS / live claims.

| Gate | Expansion pass |
| --- | --- |
| **E0** | Currency · G0 · preset/magic match · costs policy stated · sleeve named |
| **E1** | Gross or measured: WR > BWR · E_N > 0 on **primary long** · tip not required to carry alone |
| **E2** | ≥1 secondary window (tip or prior year) not contradicting class; Jan→Aug soft OK if labeled L3 |
| **E3** | `regime_filtered` documented (RTH + Tue + ATR + BBw); tip/H1 failures labeled L3 not silent DROP |
| **E4** | n and `M` recorded on scorecard · tip n&lt;15 never sole KEEP driver |

```
EXPANSION_KEEP   = E0 ∧ E1 ∧ E2 ∧ E3
EXPANSION_WATCH  = E0 ∧ E1 but thin n, Fragile EF, or sleeve conflict
EXPANSION_DROP   = measured EF≤0 on primary long, or class break (trend geometry, TP<SL, AOS-on contamination)
```

**Provisional labels (2026-10-12, journal-gross):**  
- Harvest baseline (**26092501**, AOS OFF) → **EXPANSION_KEEP** · **current pool candidate** ([`candidate_pool.md`](./candidate_pool.md))  
- Balanced long → **WATCH** (reference only; not the candidate)  
- AOS L2det presets → experiments only · not pool candidates  
- Neither sleeve → production

### 7.2 Production ladder (unified G0–G5)

Unchanged maths from `unified_edge_framework.md`. AAPL notes:

| Gate | AAPL notes |
| --- | --- |
| **G0** | Currency; G0; preset/magic match; costs recorded/defaulted · **no n≥385 floor** (n reported; `M` carries uncertainty) |
| **G1** | EF>M full + W500; WR > BWR+Leak; R bootstrap; **Leak from deals not preset meta** |
| **G2** | Anchored WF; WFE≥0.5; OOS E_N>0 in ≥75% folds — re-select ATR/BBw/points on **IS only** if retuning |
| **G3** | BM_worst>0 **or** declared regime_filtered; concentration flag if &gt;70% E_N in one ATR×ER (or earnings) cell |
| **G4** | MC-1/2/3; block 20; **overnight gap path mandatory**; stress gap overrun |
| **G5** | ±10% BBDev, SL, TP, MaxSpread, ATR/BBw bounds; EF>0 at cost ×1.5 |

```
PRODUCTION-WORTHY(AAPL_sleeve) = G0 ∧ G1 ∧ G2 ∧ G3 ∧ G4 ∧ G5
```

**Status (2026-10-12):** **NOT PRODUCTION-WORTHY** (Leak unmeasured · G1–G5 not run — not an n-floor reject). Live remains EURUSD / AUDUSD books — Apple is expansion only.

---

## 8. Adapter bindings (blotter)

Follow unified §8 plus:

| Extra field | Required | Note |
| --- | --- | --- |
| `exit_reason` | yes | §2.3 |
| `spread_points_entry` | yes* | *or costs_defaulted |
| `nights_held` | yes* | swap / financing |
| `session_ok` | no | RTH diagnostic |
| `atr_pts` / `bb_width_pct` | no | regime cell |
| `signal_tag` | no | buy/sell fade |
| `group_event_id` | yes | = event_id on G0 |
| `sleeve` | yes | Harvest \| Balanced |

Forbidden evidence: pips-mode Stage 1–3 · ticket WR with grid · preset/magic mismatch · pooling both magics · profit-only optimise · tip-only admission · scoring FX L2 on Apple · using `InpAOS_Leak` as measured Leak.

---

## 9. Benchmark protocol

1. Load one preset from `Profiles/Tester/BMRG/AAPL/` · symbol **Apple** · M15 · every tick · ACCOUNT CURRENCY.  
2. Confirm Inputs = preset (sleeve SL/TP, BBDev 2.5, RTH, skip Tue, ATR/BBw on, lot 1.0, magic, AOS off).  
3. Run **primary long** window first; tip and Jan→Aug as secondary.  
4. Export deals → `blotter/inbox/` → archive `blotter/archive/AAPL-<SLEEVE>-<date>/`.  
5. Aggregate events → WR, R, BWR, BM, Leak, EF, M, E_N, RR−R, OTHER share.  
6. Emit W10/W15/W20 (+ W100+ when able), calendar months, year split.  
7. Apply **expansion ladder** per sleeve; only then schedule production G0–G5.  
8. Update `system_profile.md` evidence tables from scorecard.  
9. Refresh Canvas from scorecard only (display).

---

## 10. Monitoring / investigation (AAPL)

| Trigger | Response |
| --- | --- |
| WR ≤ BWR+Leak on W20 | Investigate Thu / hour-18 / buy-side / ATR·BBw |
| EF ≤ 0 after measured Leak on primary | costs_fragile or EXPANSION_DROP |
| Tip strong, Jan→Aug EF≤0, long OK | Label **regime mismatch (L3)**; do not silent DROP |
| OTHER share > 40% | Gap / slippage / session-TZ audit |
| RR−R gap > 25% | Exit mix / gap overrun audit |
| FREQUENCY_STALL | Confirm BBw/ATR gates — widen only via new preset task |
| Max loss streak > 1.5× expected | Block-bootstrap before any f / lot increase |
| Earnings week wipeout cluster | Tag L3 cell; optional future AIOS skip |
| Desire to “fix” with trend RR | Reject — class break |

Investigation order (unified): **data → execution → regime → structural**.

---

## 11. Scorecard fields

```text
framework_unified: 1.0
framework_aapl: 0.1.0
preset_id / magic / sleeve / geometry_mode / window / n
aos_overlay: none
WR, R, RR, RR-R, BWR, BM, Leak, Leak_source, EF, M, E_N, PF
OTHER_share, overnight_share
f_realised_mean, lot
lifecycle_window: W15|W20|W30|W250
ΔD
ladder: expansion|production
gates: E0..E4 and/or G0..G5
verdict: EXPANSION_KEEP | EXPANSION_WATCH | EXPANSION_DROP
       | PRODUCTION-WORTHY | NOT PRODUCTION-WORTHY
regime_note: <optional L3 H1 / earnings note>
canvas: display_only
```

---

## 12. Document map

| File | Purpose |
| --- | --- |
| `doc/unified_edge_framework.md` | General maths & production gates |
| `doc/edge_framework.md` | EURUSD / BMRG champion binding (do not use for AAPL) |
| `doc/assets/AUDUSD/edge_framework.md` | AUDUSD Book A binding (do not use for AAPL) |
| **`doc/assets/AAPL/edge_framework.md`** | **This file — Apple expansion binding** |
| `doc/assets/AAPL/system_profile.md` | Class + dual-sleeve observed behaviour |
| `doc/assets/AAPL/README.md` | Asset doc index |
| `Profiles/Tester/BMRG/AAPL/` | Loadable presets |
| `blotter/archive/AAPL-*/` | Immutable Apple reviews (when archived) |

---

## 13. Versioning

- **0.1.0** — Initial AAPL binding: canvas caveat; gap table P-A…P-W; dual-sleeve Stage 0–4; small-n windows; true-Leak proxy vs preset meta; overnight/gap MC; expansion vs production ladders; provisional KEEP on Harvest/Balanced long (journal-gross).  
- **0.1.1** — Drop unified **n≥385** as a hard AAPL criterion (G0 / P-O / baselines). Sample size informs `M` only.  
- Bump when cost defaults, 1R, event rules, ladder criteria, baseline frequency, or sleeve geometry change.

---

## 14. One-line contract

**Score Apple M15 as a RTH-filtered G0 Bollinger mean-reversion fade (Harvest WR-side · Balanced mixed) under unified identities; use expansion gates while n and measured Leak are thin; never let Canvas, tip-only charts, or preset meta-Leak override a blotter scored here; production-worthy only after full G0–G5 per sleeve — live capital stays off Apple until then.**
