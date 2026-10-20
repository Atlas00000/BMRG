# UK100 — Edge Framework

**Version:** 0.1.0  
**Status:** Normative for **UK100 (FTSE CFD) expansion** benchmarking  
**Parent:** `doc/unified_edge_framework.md` v1.0  
**Companions:** [`system_profile.md`](./system_profile.md) · [`README.md`](./README.md)  
**Preset:** `Profiles/Tester/BMRG/UK100/BMRG-M15-UK100-6M-P0_balanced_chart.set`  
**Magic:** **26101201** · AOS **OFF**  
**Primary evidence:** 2026.05.01 → 2026.08.31 · Tester `logs/20261012.log` · profile 2026-10-12  
**Chart card:** `doc/BMRG_M15_UK100_6M_chart_preset.md`

This document **binds** the unified edge framework to the UK100 M15 Balanced P0 extract. Where this file and the unified doc conflict on **UK100 procedure**, **this file wins**. Formulae remain those of the unified doc.

**Not** the EURUSD live binding (`doc/edge_framework.md`) · **not** AUDUSD · **not** AAPL. Do not mix scorecards or magics.

---

## 0. Canvas caveat

| Artifact | Role | Authority |
| --- | --- | --- |
| **This markdown** | Contract: score UK100 Balanced P0, gates, adapter, gap fillings | **Normative** |
| **`doc/unified_edge_framework.md`** | Shared maths, stages, G0–G5 | Normative for **formulae** only |
| **`doc/assets/UK100/system_profile.md`** | Class thesis · observed behaviour · rolling tables | Evidence / descriptive |
| **`Profiles/Tester/BMRG/UK100/*.set`** | Locked inputs | Geometry source |
| **`blotter/archive/UK100-*/`** | Immutable scored runs | Evidence of record |
| **Canvas / chat charts / UI tiles** | Visual snapshot of a scorecard | **Display only** |

**Rules**

1. **Canvas ≠ verdict.** A chart, canvas, or dashboard tile never overrides a blotter scored under this document.  
2. **System profile ≠ gate pass.** Profile WR / E_N / EF from journal TP/SL counts + Leak **prior** are **descriptive** until a deal blotter measures full `c_R` (spread + commission + swap + slippage).  
3. Changing 1R definition, event aggregation, cost defaults, sleeve identity, expansion/production tiers, or gate bindings **bumps this version**.  
4. Refresh any Canvas **from the scorecard only** after a scored run — never invent EF / Leak / zone on the canvas.  
5. **Tip charts are not admission.** May→Aug tip alone cannot promote to production if measured Leak / walk-forward / MC fail. Tip **can** support `EXPANSION_KEEP` when prior softness is labeled L3.  
6. **Truncated history is not multi-year.** Broker tip begins **2025.12.17**. Tester requests dated “from 2024” are truncated — scorecards must state `hist_from` and must not claim multi-year robustness.

---

## 1. Gaps in the unified framework — UK100 fillings

The unified doc is strategy- and symbol-agnostic. These bindings close the gaps for UK100 index CFD.

| # | Unified gap | UK100 binding |
| --- | --- | --- |
| **U-A** | Trade event / grid | G0 only: MaxLevels=1 · MaxEntries=1 → **ticket = event**. Ticket WR with levels>1 is G0 fail. |
| **U-B** | 1R declaration | Hard SL at entry: `1R = InpSL_Points × volume × tick_value`. Designed SL = **2500** points. Point = **0.01** (Digits=2). Scorecard **must** state SL + lot. On this path 0.1 lot ≈ **$2.50 / 1R** (confirm on deal export). |
| **U-C** | RR vs realised R | Benchmark on **R**, never assume RR. Designed RR = **1.25**. Monitor `RR − R`. Expect `FIXED_RR_FADE` (MID ≈ 0; rare EOT on window end). |
| **U-D** | Instrument costs | Index CFD: **wide spread vs FX** (≈120–140 pts observed), contract size, possible overnight financing if held. Default until deal-measured: `c_R ≈ (k × entry_spread_pts) / SL_pts` with **k=2** round-turn floor (design card used RT≈160 pts → `c_R≈160/2500=0.064R` → Leak≈**2.9 pp** at R=1.25). Prefer measured entry+exit spreads. Preset `InpAOS_Leak=2.9` is **metadata**, not measured L1. |
| **U-E** | Regime tags vs filters | Declared `regime_filtered=true` via London **08:00–17:00** · **skip Tue** · ATR **max 1470** (≈ M15 p75). BB-width **OFF**. G3 may use that declaration. Soft Feb / Jul / tip BUY / Thu = **regime leak (L3)**, not auto class death. Ouroboros MATCH/FRAGILE monthly tags are **context**, not substitute for ATR×ER cells when tagged. |
| **U-F** | Geometry origin | SL/TP are **UK100-calibrated** (~2.1× M15 ATR p50≈1189), not a silent FX point transfer. Retune points only after Leak / RR−R fail — not from raw $ alone. Thin SL≈1200 rejected (Leak theatre). |
| **U-G** | Pips / points-only PnL | **Inadmissible** for Stage 1–3. ACCOUNT CURRENCY only. |
| **U-H** | Lot vs f | Broker `VOLUME_MIN=0.1` → research lot **0.1**. Report `f_declared` (preset risk% 0.5) and `f_realised = risk_ccy / equity_at_open`. On $500, 1R ≈ $2.50 → **f ≈ 0.5%**. Stage 3 always uses **f_realised**. |
| **U-I** | Session vs inventory | Entries gated to London cash; exits continue. Profile holds are **mostly intraday** (med win ~1.6h; hold≥12h ~5–6%) — overnight gap path is **secondary** vs AAPL, but still include any overnight events in Leak / MaxDD / MC. |
| **U-J** | Pause / daily flat / EOT | Keep in blotter; tag `exit_reason`. EOT excluded from WR/R; counted in frequency. |
| **U-K** | Preset / sleeve identity | Score **one magic per scorecard**: **26101201**. `preset_id` + magic + ea_version must match. Mismatch → G0 fail. Future Harvest/Growth alts need **new magic + preset_id**. |
| **U-L** | Baseline frequency | Provisional **~35–45 events / 90d** from tip (~13 / 30d) · prior denser (~19 / 30d). Recalibrate after longer blotter. `FREQUENCY_STALL` = 90d count &lt; **50%** of baseline (~18–22). ATR max binding is intentional — do not raise frequency by lifting ATR max without a new preset. |
| **U-M** | Mid rarity | Mid share &lt;5% → realisation `FIXED_RR_FADE`. Tip exit mix ≈ TP 49% / SL 51%. |
| **U-N** | Expansion vs production | UK100 is **asset expansion**, not live replace. Two verdict ladders (§7): `EXPANSION_*` (small-n OK) vs `PRODUCTION-WORTHY` (full G0–G5). |
| **U-O** | Sample-size vs unified tiers | **UK100 does not use n≥385 as a hard expansion criterion.** Report `n` and compute `M` (Wilson if n&lt;200). Verdicts key off **EF vs M**, walk-forward, and regime — not a fixed headcount floor. Tip n≈50 is usable Stage-0; still insufficient for production G1 alone. |
| **U-P** | Index / FX correlation | UK100 is **not** a USD-fade FX twin and **not** an equity single-name twin. Do not treat UK100 KEEP as diversification vs EUR/AUD/AAPL without a separate covariance engine. Do not stack full research f with live FX as “hedged.” |
| **U-Q** | AOS | Engine magic **26101201** stays **AOS OFF**. HITL research OS arm magic **26111307** (`AIOS_SIGNOFF.md`) — L2det v1b only; not FX live replace; not production admit. Do not score EUR/AUD L2 pins on UK100. |
| **U-R** | Window policy | **Primary** = May→Aug 2026 tip (or successor complete MATCH tip). **Prior** Jan→Apr = regime diagnostic. **Hist tip** (from 2025.12.17) = composite context — state truncation. Incomplete Oct FRAGILE tip = footnote only. Hostile months labeled L3, not silent DROP if primary tip holds after Leak. |
| **U-S** | Side of edge | Balanced = **mixed WR + R** (RR 1.25). Soft target: WR ≫ 44.4% with R≈RR. Do not “fix” by shrinking AL as default; do not convert to trend RR. Tip sell-led / prior buy-led is **regime side flip**, not a permanent side lock. |
| **U-T** | Hygiene pockets | Profile soft pockets: **Thu**, hour **08**, tip **BUY**, **Jul** (and prior **Feb**). Optional filter experiments need a **new preset_id / magic**; do not silently mutate 26101201 mid-book. |
| **U-U** | Probe vs Tester | Ouroboros M15* probe (WR 54.1% / EF +6.7 pp) is **design prior only**. Tester tip is blotter authority. Do not reject geometry solely because Tester &lt; probe; do not claim probe EF as scored EF. |
| **U-V** | Spread gate vs Leak | MaxSpread **200** is an entry filter, not a Leak estimate. Leak always from fills / cost model. |
| **U-W** | ATR selectivity | ATR max ≈ p75 is the main vol throttle (BB-width OFF). Do not disable ATR max and claim the same G3 declaration. Unfiltered sleeve = **new preset** + re-score. |
| **U-X** | Containment streaks | `InpMaxLossStreak=3` will pause; observed max streaks 6–7 on tip/prior are **expected under stress**. Streak &gt; 1.5× theoretical raises `DEPENDENCE` → block-bootstrap before any f increase. |

---

## 2. Trade-event contract

### 2.1 Geometry

| Mode | Inputs | Event rule | Gates? |
| --- | --- | --- | --- |
| **G0 Balanced P0** | MaxLevels=1, MaxEntries=1, SL2500/TP3125 | One lifecycle = one event | Yes |
| Grid basket | Levels or entries > 1 | Basket flat = one event | Out of UK100 expansion scope |
| Mixed as tickets | — | — | **G0 fail** |

### 2.2 Win / loss

- Win: `pnl_R > 0` after costs  
- Loss: `pnl_R < 0`  
- Scratch (`pnl_R = 0`): exclude from WR/R; keep in frequency/cost  

### 2.3 `exit_reason`

`TP` · `SL` · `MID` · `DAILY_FLAT` · `EQUITY_HALT` · `FAIL_PAUSE` · `MANUAL` / `EOT` · `OTHER`

Tolerance for TP/SL classification: |price move − designed distance| &lt; **0.25** index points (25 pts at Point=0.01). Else `OTHER`.

### 2.4 Identity metadata (required)

```text
ea_name: BMRG
symbol: UK100
timeframe: M15
magic: 26101201
preset_id: BMRG-M15-UK100-6M-P0_balanced_chart
geometry_mode: G0_SINGLE
designed_rr: 1.25
risk_definition: hard_stop_points
lot_mode: 0.1_minlot
regime_filtered: true   # London 08-17 + skip Tue + ATR max 1470
baseline_frequency: 40  # events / 90d provisional
pool_role: Expansion_UK100_Balanced_P0
aos_overlay: none
hist_from: <broker tip start, e.g. 2025.12.17>
costs_defaulted: <list or none>
```

### 2.5 `event_id`

```text
event_id = "26101201-UK100-{side}-{YYYYMMDDhhmmss}-{first_ticket}"
```

---

## 3. Stage 0 — Core identities (bound)

```
BWR = 1 / (1 + R)
BM  = WR − BWR
E_N = WR × (R + 1) − 1 = (R + 1) × BM
```

Use **realised R** for BWR/BM/E_N on scorecards when deal PnL exists. Designed BWR(RR=1.25)=**44.4%** is the sleeve label; FIXED_RR path may use designed R until R_real is measured.

### 3.1 Designed geometry

| Field | Value | Intent |
| --- | --- | --- |
| SL / TP | **2500 / 3125** | RR = **1.25** · BWR(RR) = **44.4%** |
| BB | 20 / **2.2** | Entry threshold |
| Session | **08:00–17:00** · skip Tue | London cash regime filter |
| ATR gate | max **1470** ON · min 0 | Cut high-vol FRAGILE |
| BB-width | OFF | Avoid fire starvation |
| Class | Meanrev fade · **mixed WR + R** | Not Harvest WR-theatre · not trend |

### 3.2 Soft targets (expansion · after costs when known)

| Metric | Soft target | Fail / worry signal |
| --- | --- | --- |
| WR | > BWR; prefer ≥ **48–52%** after Leak prior | ≤ BWR+Leak on W20+ of primary tip |
| R | ≈ 1.25 (±10% on FIXED_RR) | R ≪ RR without WR lift |
| BM | > 0; prefer ≥ **+4 pp** on home tip | BM ≤ 0 after costs on primary |
| E_N | > 0; prefer ≥ **+0.05R** on tip | ≤ 0 on tip W20 **and** tip calendar months |
| Soft stress month | WR can &lt; BWR (Jul-like) | Multi-month cluster ≪ BWR → L3 review, not auto DROP if tip EF>0 |
| RR − R | ~0 | Gap > 25% of baseline → exit/slip audit |
| MaxDD (research $500 / 0.1 lot) | soft under ~8–10% | Approach EA halt / DD_limit |

### 3.3 Side diagnosis (locked)

**Mixed WR + R** (Balanced RR 1.25). Edge = WR margin above 44.4% BWR **plus** modest R thickness. Tip may be sell-led and prior buy-led — score both sides; do not flip AllowBuy/AllowSell without a new preset.

---

## 4. Stage 1 — Cost, Leak, EF

### 4.1 Cost defaults (`costs_defaulted` until deal blotter)

| Component | UK100 default |
| --- | --- |
| Spread | Mean entry spread (pts) from blotter; else session median (~120–140 observed) |
| Round-turn proxy | **2 × spread_pts** → `c_R_spread = (2 × spread_pts) / 2500` (floor). Design card RT≈160 pts → `c_R≈0.064R` |
| Commission | Broker card (else 0 flagged) |
| Swap / financing | Broker × nights held when hold ≥1 session (rare on tip; still mandatory if present) |
| Slippage | Measured fill delta; inside 2× spread proxy until fill fields exist |

```
Leak = c_R / (R + 1)     # report in pp of WR
EF   = BM − Leak
```

**Interim journal proxy (until deals):**  
Leak_prior ≈ **2.9 pp** (design). State `Leak_source=prior|proxy|measured` on every scorecard.

**Double-counting:** only L1 inside EF. L2 = `M` threshold. L3–L5 = gates/monitors (unified §4.2). Preset `InpAOS_Leak` is **not** L1.

### 4.2 Uncertainty `M`

```
M = 1.96 × sqrt(WR × (1 − WR) / n)
```

For **n &lt; 200** use **Wilson** half-width (unified FX-07). Expansion scorecards must state which. Small `n` widens `M` (harder to clear `EF > M`) — that is the sample-size effect; there is **no separate n≥385 reject** on the expansion ladder.

### 4.3 Zones

| Zone | Condition | Expansion action | Production action |
| --- | --- | --- | --- |
| Negative | EF ≤ 0 | EXPANSION_DROP or costs_fragile | Reject |
| Fragile | 0 &lt; EF ≤ M | EXPANSION_KEEP / WATCH · research small-f | Not production-worthy |
| Robust | EF > M | Eligible deepen sample / Stage 2 | Eligible Stage 2/4 |

### 4.4 Provisional baselines (2026-10-12 · journal-gross)

> Descriptive until deal export. Assumes R ≈ 1.25 FIXED_RR; Leak **prior** 2.9 pp.

#### Primary tip · May→Aug 2026 · magic 26101201

| Metric | Value | Note |
| --- | ---: | --- |
| n | **51** | Report only — not a hard floor |
| WR / R | 49.0% / ≈1.25 | Dedicated tip run |
| BWR / BM | 44.4% / **+4.6 pp** | Gross |
| E_N | **+0.103R** | Gross |
| Leak_prior | **2.9 pp** | Replace with measured |
| EF_prior | **+1.7 pp** | Thin |
| M (normal approx) | ~**±13.7 pp** | Wilson preferred → zone **Fragile** (EF ≪ M) |
| Zone (proxy) | **Fragile** | EXPANSION_KEEP candidate; deal Leak before stronger claims |
| Final Δ | **+$17.14** (+3.4%) | Equity confirms direction |

#### Prior · Jan→Apr 2026

| Metric | Value | Note |
| --- | ---: | --- |
| n | 75 | Diagnostic |
| WR / E_N | 45.3% / +0.020R | Barely above BWR |
| EF_prior | **−2.0 pp** | True-leak fail under prior |
| Label | **L3 regime** | Do not alone EXPANSION_DROP if tip EF>0 |

#### Hist composite · from 2025.12.17 → 2026.08

| Metric | Value | Note |
| --- | ---: | --- |
| n | 131 | Truncated hist — state `hist_from` |
| WR / E_N | 45.8% / +0.031R | Diluted by prior + Jul |
| EF_prior | −1.5 pp | Context only |

**Design probe (not blotter):** n≈74 · WR 54.1% · EF≈+6.7 pp — geometry design only.

**Rule:** Do not promote “Robust” from these rows. Deal blotter first. Do not score probe as EF.

---

## 5. Stage 2 — Health windows

Unified W100/W250/W500 assume large n. UK100 expansion adds **small-n windows** until n≥250.

| Window | Size | Step | Role on UK100 |
| --- | ---: | ---: | --- |
| **W10** | 10 | 5 | Fast / noisy (investigation only) |
| **W15** | 15 | 5–7 | Fast expansion signal |
| **W20** | 20 | 10 | **Expansion main** until n grows |
| **W30** | 30 | 15 | Expansion confirm (when n allows) |
| W100 | 100 | 25 | Adopt when n allows |
| W250 | 250 | 25 | Lifecycle (production path) |
| W500 | 500 | 25 | Confirm |
| Cal month / 30d | — | — | Soft stress · frequency · L3 label |
| Ouroboros month tag | — | — | MATCH / FRAGILE context (not gate substitute) |

### 5.1 Lifecycle (expansion-scaled)

Until n≥250, evaluate on **W20 confirmed by W15/W30** (and monthly E_N):

| State | Condition (expansion) | Action |
| --- | --- | --- |
| Expanding | EF>M (or BM>Leak_prior if costs pending) and ΔD≥0 on 2 evals | Continue sample |
| Stable | EF>M / BM>Leak_prior, \|ΔD\| small | Routine |
| Compressing | Margin falling 2 evals | Investigate: Jul/Feb regime vs execution (§10) |
| Near frontier | 0 &lt; EF ≤ M | Cap research f; no live |
| Below frontier | EF≤0 on W20 **and** primary tip | Halt this preset; regime / cost review |

Unified Stage 2 halt rules apply unchanged once W250/W500 exist.

### 5.2 Profile rolling snapshot (gross)

| Family | Result |
| --- | --- |
| Tip months | May/Jun/Aug E_N>0 · **Jul −0.36R** (L3) |
| Tip W10 / W15 / W20 avg E_N | ~+0.12 / +0.08 / +0.03R |
| Prior W20 avg E_N | ~+0.08R (min deep in Feb path) |
| Hist W30 avg E_N | ~+0.06R |

---

## 6. Stage 3 — Capital (research only)

| Item | Binding |
| --- | --- |
| Intent | Rank / size **research** capital only — **not** live FT attach |
| Lot | **0.1** until risk-mode unlock / larger deposit |
| f_declared | 0.5% |
| f_realised | `risk_ccy / equity_at_open` per event (~0.5% on $500) |
| Kelly | Quarter–half of shrunk WR; **cap research ≤0.5%** until G1 Robust |
| DD_limit | **25%** default; EA equity halt 15% OK if tighter |
| Daily loss | Preset daily-loss % + flatten in path / MC |
| Ruin | P(equity ≤ 0.5 C₀) ≤ 1% |
| Overnight | Include overnight subset when present; do not assume AAPL-scale gap risk |
| Cluster | Do **not** stack full research notional with live FX / AAPL as diversification |

Stage 3 ranking vs other expansion assets only after each has deal-scored EF and the same cost policy.

---

## 7. Stage 4 — Gates (two ladders)

### 7.1 Expansion ladder (asset list · pre-AIOS)

Use while building the research index/equity list **before** UK100 AIOS / live claims.

| Gate | Expansion pass |
| --- | --- |
| **E0** | Currency · G0 · preset/magic match · costs policy stated · `hist_from` if truncated |
| **E1** | Gross or measured: WR > BWR · E_N > 0 on **primary tip** · soft-stress month not wipeout of whole tip |
| **E2** | ≥1 secondary window (prior or hist) not contradicting class; prior EF≤0 OK if labeled L3 |
| **E3** | `regime_filtered` documented (London + Tue + ATR max); tip/prior failures labeled L3 not silent DROP |
| **E4** | n and `M` recorded · probe not used as scored EF · tip not required to match probe WR |

```
EXPANSION_KEEP   = E0 ∧ E1 ∧ E2 ∧ E3
EXPANSION_WATCH  = E0 ∧ E1 but thin EF, Fragile zone, or conflicting sides without L3 note
EXPANSION_DROP   = measured EF≤0 on primary tip, or class break (trend geometry, TP<SL, AOS-on contamination)
```

**Provisional label (2026-10-12, journal-gross + Leak prior):**  
**EXPANSION_KEEP** · Balanced P0 · magic **26101201** · AOS OFF — expansion queue, not production.

### 7.2 Production ladder (unified G0–G5)

Unchanged maths from `doc/unified_edge_framework.md`. UK100 notes:

| Gate | UK100 notes |
| --- | --- |
| **G0** | Currency; G0; preset/magic match; costs recorded/defaulted · **no n≥385 floor** for expansion docs (n reported; `M` carries uncertainty). Production path still needs adequate n for G1 windows. |
| **G1** | EF>M full + W500 when able; WR > BWR+Leak; R bootstrap; **Leak from deals not preset meta / design prior** |
| **G2** | Anchored WF; WFE≥0.5; OOS E_N>0 in ≥75% folds — re-select ATR/points on **IS only** if retuning |
| **G3** | BM_worst>0 **or** declared regime_filtered (London+Tue+ATR max); concentration flag if &gt;70% E_N in one ATR×ER (or Ouroboros) cell |
| **G4** | MC-1/2/3; block 20; include overnight subset when present; stress cost ×1.5 path |
| **G5** | ±10% BBDev, SL, TP, MaxSpread, ATR max; EF>0 at cost ×1.5 |

```
PRODUCTION-WORTHY(UK100_Balanced_P0) = G0 ∧ G1 ∧ G2 ∧ G3 ∧ G4 ∧ G5
```

**Status (2026-10-12):** **NOT PRODUCTION-WORTHY** (Leak unmeasured · G1–G5 not run — not an n-floor reject alone). Live remains EURUSD / AUDUSD books — UK100 is expansion only.

---

## 8. Adapter bindings (blotter)

Follow unified §8 plus:

| Extra field | Required | Note |
| --- | --- | --- |
| `exit_reason` | yes | §2.3 |
| `spread_points_entry` | yes* | *or costs_defaulted |
| `nights_held` | yes* | swap when overnight |
| `session_ok` | no | London diagnostic |
| `atr_pts` | no | regime cell / ATR gate |
| `signal_tag` | no | buy/sell fade |
| `group_event_id` | yes | = event_id on G0 |
| `hist_from` | yes* | *when window request &gt; broker tip |
| `ouroboros_month_tag` | no | MATCH / FRAGILE context |

Forbidden evidence: pips-mode Stage 1–3 · ticket WR with grid · preset/magic mismatch · profit-only optimise · tip-only production admission · truncated hist as multi-year · scoring FX/AUD L2 on UK100 · using `InpAOS_Leak` or probe EF as measured Leak/EF · pooling future alt sleeves into one WR.

---

## 9. Benchmark protocol

1. Load `BMRG-M15-UK100-6M-P0_balanced_chart` · symbol **UK100** · M15 · every tick · ACCOUNT CURRENCY.  
2. Confirm Inputs = preset (SL2500/TP3125, BBDev 2.2, 08–17, skip Tue, ATR max 1470, lot 0.1, magic 26101201, AOS off).  
3. Run **primary tip** window first; prior and hist tip as secondary (record `hist_from`).  
4. Export deals → `blotter/inbox/` → archive `blotter/archive/UK100-P0-<date>/`.  
5. Aggregate events → WR, R, BWR, BM, Leak, EF, M, E_N, RR−R, side/DOW.  
6. Emit W10/W15/W20 (+ W100+ when able), calendar months, Ouroboros tags as footnotes.  
7. Apply **expansion ladder**; only then schedule production G0–G5.  
8. Update `system_profile.md` evidence tables from scorecard.  
9. Refresh Canvas from scorecard only (display).

---

## 10. Monitoring / investigation (UK100)

| Trigger | Response |
| --- | --- |
| WR ≤ BWR+Leak on W20 (tip) | Investigate Thu / H08 / BUY / ATR max binding |
| EF ≤ 0 after measured Leak on primary tip | costs_fragile or EXPANSION_DROP |
| Tip OK, prior EF≤0 | Label **regime mismatch (L3)**; do not silent DROP |
| Jul-like month wipeout, tip still E_N>0 | L3 note; optional future AIOS skip cell |
| RR−R gap > 25% | Exit mix / slippage audit |
| FREQUENCY_STALL | Confirm ATR/session gates — widen only via new preset task |
| Max loss streak > 1.5× expected | Block-bootstrap before any f / lot increase |
| Desire to “fix” with trend RR or TP&lt;SL | Reject — class break |
| Desire to pin EUR/AUD L2 | Reject — wrong asset AIOS |

Investigation order (unified): **data → execution → regime → structural**.

---

## 11. Scorecard fields

```text
framework_unified: 1.0
framework_uk100: 0.1.0
preset_id / magic / geometry_mode / window / n / hist_from
aos_overlay: none
WR, R, RR, RR-R, BWR, BM, Leak, Leak_source, EF, M, E_N, PF
side_WR_buy, side_WR_sell
f_declared, f_realised_mean, lot
lifecycle_window: W15|W20|W30|W250
ΔD
ladder: expansion|production
gates: E0..E4 and/or G0..G5
verdict: EXPANSION_KEEP | EXPANSION_WATCH | EXPANSION_DROP
       | PRODUCTION-WORTHY | NOT PRODUCTION-WORTHY
regime_note: <optional L3 Feb/Jul / Ouroboros note>
canvas: display_only
```

---

## 12. Document map

| File | Purpose |
| --- | --- |
| `doc/unified_edge_framework.md` | General maths & production gates |
| `doc/edge_framework.md` | EURUSD / BMRG champion binding (do not use for UK100) |
| `doc/assets/AUDUSD/edge_framework.md` | AUDUSD Book A binding (do not use for UK100) |
| `doc/assets/AAPL/edge_framework.md` | Apple expansion binding (do not use for UK100) |
| **`doc/assets/UK100/edge_framework.md`** | **This file — UK100 expansion binding** |
| `doc/assets/UK100/system_profile.md` | Class + observed behaviour |
| `doc/assets/UK100/aios_roadmap.md` | AIOS P0–P7 plan (gates still scored here) |
| `doc/assets/UK100/README.md` | Asset doc index |
| `doc/BMRG_M15_UK100_6M_chart_preset.md` | Chart / design card |
| `Profiles/Tester/BMRG/UK100/` | Loadable presets |
| `blotter/archive/UK100-*/` | Immutable UK100 reviews |

---

## 13. Versioning

- **0.1.0** — Initial UK100 binding: canvas caveat; gap table U-A…U-X; Stage 0–4; small-n windows; Leak prior 2.9 pp vs measured; truncated-hist rule; tip vs prior L3; expansion vs production ladders; provisional EXPANSION_KEEP on Balanced P0 tip (journal-gross).  
- Bump when cost defaults, 1R, event rules, ladder criteria, baseline frequency, or sleeve geometry change.

---

## 14. One-line contract

**Score UK100 M15 as a London-filtered G0 Bollinger mean-reversion fade (Balanced RR1.25 · ATR≤p75 · AOS OFF) under unified identities; use expansion gates while n and measured Leak are thin; never let Canvas, probe tables, truncated “2024” hist, or preset meta-Leak override a blotter scored here; production-worthy only after full G0–G5 — live capital stays off UK100 until then.**
