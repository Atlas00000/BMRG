# EURUSD — Edge Framework (M15 chart sleeve)

**Version:** 0.1.0  
**Status:** Normative for **EURUSD M15 expansion** benchmarking  
**Parent:** `doc/unified_edge_framework.md` v1.0  
**Companions:** [`system_profile.md`](./system_profile.md) · [`README.md`](./README.md)  
**Preset:** `Profiles/Tester/BMRG/EURUSD/BMRG-M15-EURUSD-6M-P2_light_selective_chart.set`  
**Magic:** **26101817** · AOS **OFF**  
**Primary evidence:** 2026.05.01 → 2026.10.17 · Tester `logs/20261018.log` · profile 2026-10-18  
**Chart card:** `doc/BMRG_M15_EURUSD_6M_chart_preset.md`  
**Review:** `blotter/archive/EURUSD-M15-P2/`

This document **binds** the unified edge framework to the EURUSD M15 **P2 light-selective** extract. Where this file and the unified doc conflict on **EURUSD M15 procedure**, **this file wins**. Formulae remain those of the unified doc.

**Not** the EURUSD **M5 Harvest** live binding (`doc/edge_framework.md` · magic `8210204`) · **not** AUDUSD · **not** UK100. Do not mix scorecards or magics.

---

## 0. Canvas caveat

| Artifact | Role | Authority |
| --- | --- | --- |
| **This markdown** | Contract: score EURUSD M15 P2, gates, adapter, gap fillings | **Normative** |
| **`doc/unified_edge_framework.md`** | Shared maths, stages, G0–G5 | Normative for **formulae** only |
| **`doc/assets/EURUSD/system_profile.md`** | Class thesis · observed behaviour · rolling tables | Evidence / descriptive |
| **`Profiles/Tester/BMRG/EURUSD/*.set`** | Locked inputs | Geometry source |
| **`blotter/archive/EURUSD-M15-*/`** | Immutable scored runs | Evidence of record |
| **`doc/BMRG_M15_EURUSD_6M_chart_preset.md`** | Design / probe card | Design prior only |
| **Canvas / chat charts / UI tiles** | Visual snapshot of a scorecard | **Display only** |

**Rules**

1. **Canvas ≠ verdict.** A chart, canvas, or dashboard tile never overrides a blotter scored under this document.  
2. **System profile ≠ gate pass.** Profile WR / E_N / EF from journal TP/SL counts + Leak **prior** are **descriptive** until a deal blotter measures full `c_R` (spread + commission + swap + slippage).  
3. Changing 1R definition, event aggregation, cost defaults, sleeve identity, expansion/production tiers, or gate bindings **bumps this version**.  
4. Refresh any Canvas **from the scorecard only** after a scored run — never invent EF / Leak / zone on the canvas.  
5. **Tip charts are not admission.** May→Oct tip alone cannot promote to production if measured Leak / walk-forward / MC fail. Tip **can** support `EXPANSION_KEEP` when prior softness (Feb) is labeled L3.  
6. **Probe ≠ blotter.** Ouroboros M15* probe (WR≈50% · EF≈+2.6 pp) is geometry design only — never scored as EF.  
7. **Do not mix books.** Root `doc/edge_framework.md` (M5 Harvest champ) and this file are different sleeves. Scoring M5 live magics under this contract (or P2 under the champ contract) is G0 fail.  
8. **Ladder memory.** P0 (26101815) and P1 (26101816) are **context**, not this scorecard’s identity. Scoring the wrong magic → G0 fail.

---

## 1. Gaps in the unified framework — EURUSD M15 fillings

The unified doc is strategy- and symbol-agnostic. These bindings close the gaps for this M15 chart sleeve.

| # | Unified gap | EURUSD M15 P2 binding |
| --- | --- | --- |
| **E-A** | Trade event / grid | G0 only: MaxLevels=1 · MaxEntries=1 → **ticket = event**. Ticket WR with levels>1 is G0 fail. |
| **E-B** | 1R declaration | Hard SL at entry: `1R = InpSL_Points × volume × tick_value`. Designed SL = **300** points. Point ≈ **0.00001**. Scorecard **must** state SL + lot. On this path 0.01 lot ≈ **$3.00 / 1R** (confirm on deal export). |
| **E-C** | RR vs realised R | Benchmark on **R**, never assume RR. Designed RR = **1.25**. Monitor `RR − R`. Expect `FIXED_RR_FADE` (MID ≈ 0; rare EOT on window end). Profile: realised win R = +1.25 · loss R = −1.0. |
| **E-D** | Instrument costs | EURUSD major: tight spread vs index/gold. Default until deal-measured: `c_R ≈ (k × entry_spread_pts) / SL_pts` with **k=2** round-turn floor. Design card RT≈**20 pts** → `c_R≈20/300=0.067R` → Leak≈**3.0 pp** at R=1.25. Prefer measured entry+exit spreads + commission + **overnight swap** (holds often ≥12h — see E-I). Preset `InpAOS_Leak=3.0` is **metadata**, not measured L1. |
| **E-E** | Regime tags vs filters | Declared `regime_filtered=true` via London/NY **12:00–20:00** · **skip Tue** · ATR **max 74** (≈ M15 p90). BB-width **OFF**. G3 may use that declaration. Soft **Feb** / **Aug** / tip **BUY** / **Thu** = **regime leak (L3)**, not auto class death. Ouroboros MATCH/FRAGILE monthly tags are **context**, not substitute for ATR×ER cells when tagged. Oct FRAGILE tip = footnote only. |
| **E-F** | Geometry origin | SL/TP are **EURUSD M15-calibrated** (~6.5× M15 ATR p50≈46), **not** a silent transfer of M5 Harvest RR=1.0 geometry. Retune points only after Leak / RR−R fail — not from raw $ alone. Do not import quiet-cross (EURGBP) or index SL floors. |
| **E-G** | Pips / points-only PnL | **Inadmissible** for Stage 1–3. ACCOUNT CURRENCY only. |
| **E-H** | Lot vs f | Research path floors to **0.01** lot on $500. Report `f_declared` (preset risk% 0.5) and `f_realised = risk_ccy / equity_at_open`. On $500, 1R ≈ $3 → **f ≈ 0.6%**. Stage 3 always uses **f_realised**. |
| **E-I** | Session vs inventory | Entries gated 12–20; exits continue. Profile holds are **overnight-capable** (tip med win ~24h; hold≥12h ~66–86%) — overnight swap / gap path is **primary** (unlike UK100 cash). Include overnight events in Leak / MaxDD / MC. |
| **E-J** | Pause / daily flat / EOT | Keep in blotter; tag `exit_reason`. EOT excluded from WR/R; counted in frequency. Fail-pause after loss streak=3 is expected. |
| **E-K** | Preset / sleeve identity | Score **one magic per scorecard**: **26101817**. `preset_id` + magic + ea_version must match. Mismatch → G0 fail. P0/P1 and future Harvest/Growth alts need **new magic + preset_id**. |
| **E-L** | Baseline frequency | Provisional **~20–30 events / 90d** from tip (~8 / 30d) · YTD similar (~7.6 / 30d). Recalibrate after longer blotter. `FREQUENCY_STALL` = 90d count &lt; **50%** of baseline (~10–15). ATR max + BB 2.3 + CD 3 binding is intentional — do not raise frequency by lifting ATR max / dropping CD without a new preset. |
| **E-M** | Mid rarity | Mid share &lt;5% → realisation `FIXED_RR_FADE`. Tip exit mix ≈ TP 46.7% / SL 53.3%. |
| **E-N** | Expansion vs production | EURUSD M15 P2 is **asset expansion** (list growth before AIOS), **not** live replace of M5 Harvest. Two verdict ladders (§7): `EXPANSION_*` (small-n OK) vs `PRODUCTION-WORTHY` (full G0–G5). |
| **E-O** | Sample-size vs unified tiers | **EURUSD M15 does not use n≥385 as a hard expansion criterion.** Report `n` and compute `M` (Wilson if n&lt;200). Verdicts key off **EF vs M**, walk-forward, and regime — not a fixed headcount floor. Tip n≈45 is usable Stage-0; still insufficient for production G1 alone. |
| **E-P** | Intra-EURUSD book correlation | M15 P2 and M5 Harvest are **same-symbol, different TF/geometry**. Do not treat M15 KEEP as diversification vs live M5. Do not stack full research f with live Harvest as “hedged.” |
| **E-Q** | AOS | Engine magic **26101817** stays **AOS OFF**. HITL research OS arm magic **26121807** (`AIOS_SIGNOFF.md`) — L2det v1b only; not M5 Harvest replace; not production admit. Do not score M5 aistack / AUD / UK100 L2 pins on this sleeve. |
| **E-R** | Window policy | **Primary** = May→Oct 2026 tip (or successor complete MATCH tip through Sep). **YTD** Jan→Oct = support. Incomplete Oct FRAGILE tip = footnote. Hostile months labeled L3, not silent DROP if primary tip holds Stage 0 after costs review. |
| **E-S** | Side of edge | Balanced = **mixed WR + R** (RR 1.25). Soft target: WR ≫ 44.4% with R≈RR. Do not “fix” by shrinking AL as default; do not convert to trend RR or Harvest RR=1.0 without a new sleeve card. Tip/YTD **sell-led** / BUY soft is **regime side diagnosis**, not a permanent AllowBuy=false lock. |
| **E-T** | Hygiene pockets | Profile soft pockets: **BUY**, **Thu**, hours **13 / 19**, **Feb**, **Aug**. Optional filter experiments need a **new preset_id / magic**; do not silently mutate 26101817 mid-book. |
| **E-U** | Probe vs Tester | Ouroboros M15* probe (WR 50% / EF +2.6 pp) is **design prior only**. Tester tip is blotter authority. Do not reject geometry solely because Tester &lt; probe; do not claim probe EF as scored EF. |
| **E-V** | Spread gate vs Leak | MaxSpread **30** is an entry filter, not a Leak estimate. Leak always from fills / cost model. |
| **E-W** | ATR / selectivity ladder | ATR max ≈ p90 + BB 2.3 + CD 3 is the P2 stack. **P1 path** (ATR≤68 + BBw ON + BB 2.4) is **rejected** (starvation). Do not re-enable BBw or tighten ATR to p75 without a new preset. Unfiltered / P0-return sleeve = **new preset** + re-score. |
| **E-X** | Containment streaks | `InpMaxLossStreak=3` will pause; observed max streaks 4–5 on tip/YTD are **expected under stress**. Streak &gt; 1.5× theoretical raises `DEPENDENCE` → block-bootstrap before any f increase. |
| **E-Y** | Sleeve ladder vs class death | P0 tip WR≪BWR is **hit-rate fail under under-selectivity**, not proof meanrev class is wrong on EURUSD. P1 starvation is **filter overfit**, not class death. Score P2 on its own magic; cite ladder only as context. |
| **E-Z** | Live M5 champ boundary | Live / EDX Harvest (`8210204`) stays under `doc/edge_framework.md`. This file never admits or denies that book. Cross-citing M5 EF as M15 EF (or vice versa) is forbidden. |

---

## 2. Trade-event contract

### 2.1 Geometry

| Mode | Inputs | Event rule | Gates? |
| --- | --- | --- | --- |
| **G0 P2 light** | MaxLevels=1, MaxEntries=1, SL300/TP375 | One lifecycle = one event | Yes |
| Grid basket | Levels or entries > 1 | Basket flat = one event | Out of EURUSD M15 expansion scope |
| Mixed as tickets | — | — | **G0 fail** |

### 2.2 Win / loss

- Win: `pnl_R > 0` after costs  
- Loss: `pnl_R < 0`  
- Scratch (`pnl_R = 0`): exclude from WR/R; keep in frequency/cost  

### 2.3 `exit_reason`

`TP` · `SL` · `MID` · `DAILY_FLAT` · `EQUITY_HALT` · `FAIL_PAUSE` · `MANUAL` / `EOT` · `OTHER`

Tolerance for TP/SL classification: |price move − designed distance| &lt; **3** points (0.3 pip at Point=0.00001). Else `OTHER`.

### 2.4 Identity metadata (required)

```text
ea_name: BMRG
symbol: EURUSD
timeframe: M15
magic: 26101817
preset_id: BMRG-M15-EURUSD-6M-P2_light_selective_chart
geometry_mode: G0_SINGLE
designed_rr: 1.25
risk_definition: hard_stop_points
lot_mode: 0.01_minlot
regime_filtered: true   # 12-20 + skip Tue + ATR max 74
baseline_frequency: 25  # events / 90d provisional
pool_role: Expansion_EURUSD_M15_P2_light
aos_overlay: none
sleeve_ladder: P0=26101815|P1=26101816|P2=26101817
costs_defaulted: <list or none>
```

### 2.5 `event_id`

```text
event_id = "26101817-EURUSD-{side}-{YYYYMMDDhhmmss}-{first_ticket}"
```

---

## 3. Stage 0 — Core identities (bound)

```
BWR = 1 / (1 + R)
BM  = WR − BWR
E_N = WR × (R + 1) − 1 = (R + 1) × BM
```

Use **realised R** for BWR/BM/E_N on scorecards when deal PnL exists. Designed BWR(RR=1.25)=**44.4%** is the sleeve label; FIXED_RR path may use designed R until R_real is measured from currency PnL.

### 3.1 Designed geometry

| Field | Value | Intent |
| --- | --- | --- |
| SL / TP | **300 / 375** | RR = **1.25** · BWR(RR) = **44.4%** · TP > SL |
| BB | 20 / **2.3** | Light selectivity vs P0 2.2 |
| Cooldown | **3** bars | Light selectivity vs P0 2 |
| Session | **12:00–20:00** · skip Tue | London/NY overlap regime filter |
| ATR gate | max **74** ON · min 0 | Cut high-vol FRAGILE (≈p90) |
| BB-width | OFF | Avoid P1 fire starvation |
| Class | Meanrev fade · **mixed WR + R** | Not Harvest WR-theatre · not trend |

### 3.2 Soft targets (expansion · after costs when known)

| Metric | Soft target | Fail / worry signal |
| --- | --- | --- |
| WR | > BWR; prefer ≥ **48–52%** after Leak prior | ≤ BWR+Leak on W20+ of primary tip |
| R | ≈ 1.25 (±10% on FIXED_RR) | R ≪ RR without WR lift |
| BM | > 0; prefer ≥ **+3–5 pp** on home tip | BM ≤ 0 after costs on primary |
| E_N | > 0; prefer ≥ **+0.05R** on tip | ≤ 0 on tip W20 **and** tip calendar months |
| Soft stress month | WR can ≈BWR / &lt; BWR (Feb/Aug-like) | Multi-month cluster ≪ BWR → L3 review, not auto DROP if tip E_N>0 |
| RR − R | ~0 | Gap > 25% of baseline → exit/slip audit |
| Fire count tip | n ≥ **30** (Stage 0 floor) | Starvation (P1 path) |
| MaxDD (research $500 / 0.01 lot) | soft under ~8–10% | Approach EA halt / DD_limit |

### 3.3 Side diagnosis (locked)

**Mixed WR + R** (Balanced RR 1.25). Edge = WR margin above 44.4% BWR **plus** modest R thickness. Tip/YTD may be sell-led with BUY below BWR — score both sides; do not flip AllowBuy/AllowSell without a new preset.

---

## 4. Stage 1 — Cost, Leak, EF

### 4.1 Cost defaults (`costs_defaulted` until deal blotter)

| Component | EURUSD M15 default |
| --- | --- |
| Spread | Mean entry spread (pts) from blotter; else session median (MaxSpread gate 30) |
| Round-turn proxy | **2 × spread_pts** → `c_R_spread = (2 × spread_pts) / 300` (floor). Design card RT≈20 pts → `c_R≈0.067R` |
| Commission | Broker card (else 0 flagged) |
| Swap / financing | Broker × nights held — **mandatory** (profile overnight-heavy) |
| Slippage | Measured fill delta; inside 2× spread proxy until fill fields exist |

```
Leak = c_R / (R + 1)     # report in pp of WR
EF   = BM − Leak
```

**Interim journal proxy (until deals):**  
Leak_prior ≈ **3.0 pp** (design). State `Leak_source=prior|proxy|measured` on every scorecard.

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

**Interim rule while Leak is prior only:** tip EF_prior ≤ 0 does **not** alone force `EXPANSION_DROP` if Stage 0 (WR>BWR · E_N>0 · n≥30) holds — label **costs_fragile / WATCH** until measured Leak. Persistent measured EF≤0 on primary tip → DROP.

### 4.4 Provisional baselines (2026-10-18 · journal-gross)

> Descriptive until deal export. Assumes R ≈ 1.25 FIXED_RR; Leak **prior** 3.0 pp.

#### Primary tip · May→Oct 2026 · magic 26101817

| Metric | Value | Note |
| --- | ---: | --- |
| n | **45** | Report only — not a hard production floor; Stage 0 ≥30 met |
| WR / R | 46.7% / ≈1.25 | Dedicated tip run |
| BWR / BM | 44.4% / **+2.2 pp** | Gross · thin |
| E_N | **+0.050R** | Gross · soft bar exact |
| Leak_prior | **3.0 pp** | Replace with measured (swap-heavy path) |
| EF_prior | **−0.7 pp** | Thin / negative under prior |
| M (normal approx) | ~**±14.6 pp** | Wilson preferred → zone **Fragile / costs_fragile** |
| Zone (proxy) | **Fragile / costs_fragile** | Stage 0 pass; deal Leak before stronger claims |
| Final Δ | **+$7.14** (+1.4%) | Equity confirms E_N direction |

#### Supporting YTD · Jan→Oct 2026

| Metric | Value | Note |
| --- | ---: | --- |
| n | 72 | Support |
| WR / E_N | 48.6% / **+0.094R** | Stronger than tip |
| EF_prior | **+1.2 pp** | Still ≪ M (~±11.5 pp) → Fragile |
| Label | Support · Feb L3 | Do not alone promote |

#### Ladder context (not this scorecard)

| Sleeve | Magic | Tip read |
| --- | ---: | --- |
| P0 | 26101815 | WR≪BWR — under-selective |
| P1 | 26101816 | n starved — over-selective |
| **P2** | **26101817** | Stage 0 pass — this contract |

**Design probe (not blotter):** n≈52 · WR 50% · EF≈+2.6 pp — geometry design only.

**Rule:** Do not promote “Robust” from these rows. Deal blotter first. Do not score probe as EF.

---

## 5. Stage 2 — Health windows

Unified W100/W250/W500 assume large n. EURUSD M15 expansion adds **small-n windows** until n≥250.

| Window | Size | Step | Role on EURUSD M15 |
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
| Compressing | Margin falling 2 evals | Investigate: Feb/Aug / BUY / Thu (§10) |
| Near frontier | 0 &lt; EF ≤ M (or Stage 0 OK + EF_prior≤0) | Cap research f; no live; measure Leak |
| Below frontier | measured EF≤0 on W20 **and** primary tip | Halt this preset; regime / cost review |

Unified Stage 2 halt rules apply unchanged once W250/W500 exist.

### 5.2 Profile rolling snapshot (gross · 2026-10-18)

| Family | Result |
| --- | --- |
| Tip months | Jul E_N +0.29R · May/Jun flat · Aug −0.04R · Sep thin + · Oct thin |
| Tip W10 / W15 / W20 / W30 avg E_N | ~+0.03 / +0.03 / +0.04 / +0.03R |
| YTD W10 / W20 / W30 avg E_N | ~+0.05 / +0.07 / +0.05R (min deep in Feb path) |
| Soft L3 | Feb −0.33R · Aug soft · BUY / Thu |

---

## 6. Stage 3 — Capital (research only)

| Item | Binding |
| --- | --- |
| Intent | Rank / size **research** capital only — **not** live FT attach · **not** M5 Harvest replace |
| Lot | **0.01** until risk-mode unlock / larger deposit |
| f_declared | 0.5% |
| f_realised | `risk_ccy / equity_at_open` per event (~0.6% on $500 @ 0.01) |
| Kelly | Quarter–half of shrunk WR; **cap research ≤0.5%** until G1 Robust |
| DD_limit | **25%** default; EA equity halt 15% OK if tighter |
| Daily loss | Preset daily-loss % + flatten in path / MC |
| Ruin | P(equity ≤ 0.5 C₀) ≤ 1% |
| Overnight | **Include overnight subset** (primary inventory path) |
| Cluster | Do **not** stack full research notional with live M5 Harvest / AUD as diversification |

Stage 3 ranking vs other expansion assets only after each has deal-scored EF and the same cost policy.

---

## 7. Stage 4 — Gates (two ladders)

### 7.1 Expansion ladder (asset list · pre-AIOS)

Use while building the research FX M15 list **before** EURUSD M15 AIOS / live claims.

| Gate | Expansion pass |
| --- | --- |
| **E0** | Currency · G0 · preset/magic **26101817** match · costs policy stated · AOS OFF |
| **E1** | Gross or measured: WR > BWR · E_N > 0 · n ≥ 30 on **primary tip** · soft-stress month not wipeout of whole tip |
| **E2** | ≥1 secondary window (YTD) not contradicting class; YTD soft month EF/WR fail OK if labeled L3 |
| **E3** | `regime_filtered` documented (12–20 + Tue + ATR max); tip/YTD failures labeled L3 not silent DROP |
| **E4** | n and `M` recorded · probe not used as scored EF · P0/P1 ladder cited only as context · tip not required to match probe WR |

```
EXPANSION_KEEP   = E0 ∧ E1 ∧ E2 ∧ E3
EXPANSION_WATCH  = E0 ∧ E1 but thin/negative EF_prior, Fragile zone, or BUY/Thu soft without L3 note
EXPANSION_DROP   = measured EF≤0 on primary tip after honest costs, or class break (trend geometry, TP<SL, AOS-on contamination, P1 re-stack without new card)
```

**Provisional label (2026-10-18, journal-gross + Leak prior):**  
**EXPANSION_KEEP** (borderline → **WATCH** until measured Leak) · P2 light · magic **26101817** · AOS OFF — expansion keep, not production. Tip Stage 0 pass; EF_prior −0.7 pp → costs_fragile footnote.

### 7.2 Production ladder (unified G0–G5)

Unchanged maths from `doc/unified_edge_framework.md`. EURUSD M15 notes:

| Gate | EURUSD M15 notes |
| --- | --- |
| **G0** | Currency; G0; preset/magic match; costs recorded/defaulted · **no n≥385 floor** for expansion docs (n reported; `M` carries uncertainty). Production path still needs adequate n for G1 windows. |
| **G1** | EF>M full + W500 when able; WR > BWR+Leak; R bootstrap; **Leak from deals not preset meta / design prior** (include swap) |
| **G2** | Anchored WF; WFE≥0.5; OOS E_N>0 in ≥75% folds — re-select ATR/BB/CD on **IS only** if retuning |
| **G3** | BM_worst>0 **or** declared regime_filtered (12–20+Tue+ATR max); concentration flag if &gt;70% E_N in one ATR×ER (or Ouroboros) cell |
| **G4** | MC-1/2/3; block 20; **include overnight subset**; stress cost ×1.5 path |
| **G5** | ±10% BBDev, SL, TP, MaxSpread, ATR max, CooldownBars; EF>0 at cost ×1.5 |

```
PRODUCTION-WORTHY(EURUSD_M15_P2) = G0 ∧ G1 ∧ G2 ∧ G3 ∧ G4 ∧ G5
```

**Status (2026-10-18):** **NOT PRODUCTION-WORTHY** (Leak unmeasured · G1–G5 not run — not an n-floor reject alone). Live remains M5 Harvest / AUDUSD books — M15 is expansion only.

---

## 8. Adapter bindings (blotter)

Follow unified §8 plus:

| Extra field | Required | Note |
| --- | --- | --- |
| `exit_reason` | yes | §2.3 |
| `spread_points_entry` | yes* | *or costs_defaulted |
| `nights_held` | yes | swap — overnight-heavy sleeve |
| `session_ok` | no | 12–20 diagnostic |
| `atr_pts` | no | regime cell / ATR gate |
| `signal_tag` | no | buy/sell fade |
| `group_event_id` | yes | = event_id on G0 |
| `ouroboros_month_tag` | no | MATCH / FRAGILE context |
| `sleeve_ladder_note` | no | P0/P1 context if comparing |

Forbidden evidence: pips-mode Stage 1–3 · ticket WR with grid · preset/magic mismatch · profit-only optimise · tip-only production admission · scoring M5 Harvest / AUD / UK100 L2 on this sleeve · using `InpAOS_Leak` or probe EF as measured Leak/EF · pooling P0/P1/P2 into one WR · claiming M15 KEEP diversifies live M5.

---

## 9. Benchmark protocol

1. Load `BMRG-M15-EURUSD-6M-P2_light_selective_chart` · symbol **EURUSD** · M15 · every tick · ACCOUNT CURRENCY.  
2. Confirm Inputs = preset (SL300/TP375, BBDev 2.3, CD 3, 12–20, skip Tue, ATR max 74, BBw off, magic 26101817, AOS off).  
3. Run **primary tip** window first; YTD as secondary.  
4. Export deals → `blotter/inbox/` → archive `blotter/archive/EURUSD-M15-P2-<date>/`.  
5. Aggregate events → WR, R, BWR, BM, Leak, EF, M, E_N, RR−R, side/DOW.  
6. Emit W10/W15/W20 (+ W100+ when able), calendar months, Ouroboros tags as footnotes.  
7. Apply **expansion ladder**; only then schedule production G0–G5.  
8. Update `system_profile.md` evidence tables from scorecard.  
9. Refresh Canvas from scorecard only (display).

---

## 10. Monitoring / investigation (EURUSD M15)

| Trigger | Response |
| --- | --- |
| WR ≤ BWR+Leak on W20 (tip) | Investigate BUY / Thu / H13·H19 / ATR·BB·CD binding |
| EF ≤ 0 after measured Leak on primary tip | costs_fragile or EXPANSION_DROP |
| Tip OK, Feb / Aug soft | Label **regime mismatch (L3)**; do not silent DROP |
| Desire to re-stack P1 (ATR≤68 + BBw) | Reject without new preset — starvation known |
| RR−R gap > 25% | Exit mix / slippage audit |
| FREQUENCY_STALL | Confirm ATR/session/CD gates — widen only via new preset task |
| Max loss streak > 1.5× expected | Block-bootstrap before any f / lot increase |
| Desire to “fix” with trend RR or TP&lt;SL | Reject — class break |
| Desire to pin M5 aistack / AUD L2 | Reject — wrong book AIOS |
| Desire to replace live M5 Harvest with this sleeve | Reject — expansion only |

Investigation order (unified): **data → execution → regime → structural**.

---

## 11. Scorecard fields

```text
framework_unified: 1.0
framework_eurusd_m15: 0.1.0
preset_id / magic / geometry_mode / window / n
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
regime_note: <optional L3 Feb/Aug / Ouroboros note>
sleeve_ladder_note: <optional P0/P1 context>
canvas: display_only
```

---

## 12. Document map

| File | Purpose |
| --- | --- |
| `doc/unified_edge_framework.md` | General maths & production gates |
| `doc/edge_framework.md` | EURUSD **M5 Harvest** champion binding (do not use for M15 P2) |
| `doc/assets/AUDUSD/edge_framework.md` | AUDUSD Book A binding |
| `doc/assets/UK100/edge_framework.md` | UK100 expansion binding |
| `doc/assets/AAPL/edge_framework.md` | Apple expansion binding |
| **`doc/assets/EURUSD/edge_framework.md`** | **This file — EURUSD M15 P2 expansion binding** |
| `doc/assets/EURUSD/system_profile.md` | Class + observed behaviour |
| `doc/assets/EURUSD/README.md` | Asset doc index |
| `doc/BMRG_M15_EURUSD_6M_chart_preset.md` | Chart / design card |
| `Profiles/Tester/BMRG/EURUSD/` | Loadable presets |
| `blotter/archive/EURUSD-M15-P2/` | Immutable P2 review |

---

## 13. Versioning

- **0.1.0** — Initial EURUSD M15 P2 binding: canvas caveat; gap table E-A…E-Z; Stage 0–4; small-n windows; Leak prior 3.0 pp vs measured; overnight-mandatory costs; tip vs YTD L3; P0/P1 ladder context; expansion vs production ladders; provisional EXPANSION_KEEP / costs_fragile WATCH footnote on tip (journal-gross).  
- Bump when cost defaults, 1R, event rules, ladder criteria, baseline frequency, or sleeve geometry change.

---

## 14. One-line contract

**Score EURUSD M15 as a London/NY-filtered G0 Bollinger mean-reversion fade (Balanced RR1.25 · BB2.3 · CD3 · ATR≤p90 · AOS OFF) under unified identities; use expansion gates while n and measured Leak are thin; never let Canvas, probe tables, Leak prior, P0/P1 ladder noise, or M5 Harvest scorecards override a blotter scored here; production-worthy only after full G0–G5 — live capital stays on the M5 champ book until then.**
