# USDJPY — Edge Framework

**Version:** 0.1.0  
**Status:** Normative for **USDJPY M15 expansion** benchmarking  
**Parent:** `doc/unified_edge_framework.md` v1.0  
**Companions:** [`system_profile.md`](./system_profile.md) · [`README.md`](./README.md)  
**Preset:** `Profiles/Tester/BMRG/USDJPY/BMRG-M15-USDJPY-6M-P0_balanced_chart.set`  
**Magic:** **26101828** · AOS **OFF**  
**Primary evidence:** 2026.05.01 → 2026.08.31 · Tester `logs/20261019.log` · profile 2026-10-19  
**Chart card:** `doc/BMRG_M15_USDJPY_6M_chart_preset.md`  
**Review:** `blotter/archive/USDJPY-P0-CHART/`

This document **binds** the unified edge framework to the USDJPY M15 **Balanced P0** extract. Where this file and the unified doc conflict on **USDJPY procedure**, **this file wins**. Formulae remain those of the unified doc.

**Not** the EURUSD M5 Harvest live binding (`doc/edge_framework.md` · magic `8210204`) · **not** EURUSD M15 (`doc/assets/EURUSD/edge_framework.md`) · **not** AUDUSD · **not** UK100 · **not** AAPL. Do not mix scorecards or magics.

---

## 0. Canvas caveat

| Artifact | Role | Authority |
| --- | --- | --- |
| **This markdown** | Contract: score USDJPY Balanced P0, gates, adapter, gap fillings | **Normative** |
| **`doc/unified_edge_framework.md`** | Shared maths, stages, G0–G5 | Normative for **formulae** only |
| **`doc/assets/USDJPY/system_profile.md`** | Class thesis · observed behaviour · rolling tables | Evidence / descriptive |
| **`Profiles/Tester/BMRG/USDJPY/*.set`** | Locked inputs | Geometry source |
| **`blotter/archive/USDJPY-*/`** | Immutable scored runs | Evidence of record |
| **`doc/BMRG_M15_USDJPY_6M_chart_preset.md`** | Design / probe card | Design prior only |
| **Canvas / chat charts / UI tiles** | Visual snapshot of a scorecard | **Display only** |

**Rules**

1. **Canvas ≠ verdict.** A chart, canvas, or dashboard tile never overrides a blotter scored under this document.  
2. **System profile ≠ gate pass.** Profile WR / E_N / EF from journal TP/SL counts + Leak **prior** are **descriptive** until a deal blotter measures full `c_R` (spread + commission + swap + slippage).  
3. Changing 1R definition, event aggregation, cost defaults, sleeve identity, expansion/production tiers, or gate bindings **bumps this version**.  
4. Refresh any Canvas **from the scorecard only** after a scored run — never invent EF / Leak / zone on the canvas.  
5. **Tip charts are not admission.** May→Aug tip alone cannot promote to production if measured Leak / walk-forward / MC fail. Tip **can** support `EXPANSION_KEEP` / `WATCH` when Jul softness is labeled L3 and Stage 0 holds.  
6. **Probe ≠ blotter.** Ouroboros M15* probe (WR≈57.6% · EF≈+0.8 pp) is geometry design only — never scored as EF.  
7. **Do not mix books.** Root `doc/edge_framework.md` (M5 Harvest), EURUSD M15, UK100, AUD, AAPL, and this file are different sleeves. Scoring foreign magics under this contract (or 26101828 under another) is G0 fail.  
8. **High Leak prior is not class death.** Design Leak ≈ **11.4 pp** (25pt RT / SL100) is an expensive major vs thin BM — label **costs_fragile** until measured; do not DROP on prior alone while Stage 0 holds.  
9. **Yen geometry is not EUR/GBPJPY.** SL100 / ATR≤70 are yen-ATR-scaled. Importing EUR 300pt or GBPJPY 160pt floors without a new preset is G0 / class-geometry fail.

---

## 1. Gaps in the unified framework — USDJPY fillings

The unified doc is strategy- and symbol-agnostic. These bindings close the gaps for this yen-major M15 chart sleeve.

| # | Unified gap | USDJPY M15 P0 binding |
| --- | --- | --- |
| **J-A** | Trade event / grid | G0 only: MaxLevels=1 · MaxEntries=1 → **ticket = event**. Ticket WR with levels>1 is G0 fail. |
| **J-B** | 1R declaration | Hard SL at entry: `1R = InpSL_Points × volume × tick_value`. Designed SL = **100** points. Point ≈ **0.001** (Digits=3). Scorecard **must** state SL + lot. Confirm `$ / 1R` on deal export (risk% path → variable lot). |
| **J-C** | RR vs realised R | Benchmark on **R**, never assume RR. Designed RR = **1.20**. Monitor `RR − R`. Expect `FIXED_RR_FADE` (MID ≈ 0; no EOT orphans on scored tip). Profile: realised win R = +1.20 · loss R = −1.0. |
| **J-D** | Instrument costs | USDJPY major: tighter absolute spread than indices, but **Leak prior is high vs SL** because SL is only 100 pts. Default until deal-measured: `c_R ≈ (k × entry_spread_pts) / SL_pts` with **k=2** round-turn floor. Design card RT≈**25 pts** → `c_R≈25/100=0.25R` → Leak≈**11.4 pp** at R=1.20. Prefer measured entry+exit spreads + commission + swap when overnight. Preset `InpAOS_Leak=11.4` is **metadata**, not measured L1. |
| **J-E** | Regime tags vs filters | Declared `regime_filtered=true` via London/NY **12:00–20:00** · **skip Tue** · ATR **max 70** (≈ tight p50 band). BB-width **OFF**. G3 may use that declaration. Soft **Jul** / tip **Thu** / **H14** = **regime leak (L3)**, not auto class death. Ouroboros MATCH/FRAGILE monthly tags are **context**, not substitute for ATR×ER cells when tagged. Sep FRAGILE + **zero fires** under ATR≤70 = gate working, not sample failure. |
| **J-F** | Geometry origin | SL/TP are **USDJPY M15-calibrated** (~1.5× M15 ATR p50≈65), **not** a silent transfer of EURUSD 300pt or GBPJPY 160pt floors. Retune points only after Leak / RR−R fail — not from raw $ alone. Do not import quiet-cross or index SL floors. |
| **J-G** | Pips / points-only PnL | **Inadmissible** for Stage 1–3. ACCOUNT CURRENCY only. |
| **J-H** | Lot vs f | Research path uses risk% **0.5** (variable lot on $500). Report `f_declared` (0.5%) and `f_realised = risk_ccy / equity_at_open`. Stage 3 always uses **f_realised**. |
| **J-I** | Session vs inventory | Entries gated 12–20; exits continue. Profile holds are **mostly session-bound** (tip med win ~1.2h; hold≥12h ~8–11%) — overnight swap / gap path is **secondary** vs EURUSD M15 overnight book, but still include any overnight events in Leak / MaxDD / MC. |
| **J-J** | Pause / daily flat / EOT | Keep in blotter; tag `exit_reason`. EOT excluded from WR/R; counted in frequency. Fail-pause after loss streak=3 is expected (tip max loss streak **7**). |
| **J-K** | Preset / sleeve identity | Score **one magic per scorecard**: **26101828**. `preset_id` + magic + ea_version must match. Mismatch → G0 fail. Design alts RR1.25 (26101829) / BB2.0 fire-count (26101830) need **new magic + preset_id** + own scorecard. |
| **J-L** | Baseline frequency | Provisional **~35–45 events / 90d** from tip (~14 / 30d). YTD diluted by ATR-starved prior (~7 / 30d). Recalibrate after longer blotter. `FREQUENCY_STALL` = 90d count &lt; **50%** of tip baseline (~18–22). ATR max binding is intentional — do not raise frequency by lifting ATR max / opening Tokyo 02–12 without a new preset (Tokyo failed design probe). |
| **J-M** | Mid rarity | Mid share &lt;5% → realisation `FIXED_RR_FADE`. Tip exit mix ≈ TP 48.2% / SL 51.8%. |
| **J-N** | Expansion vs production | USDJPY is **asset expansion** (list growth before AIOS), **not** live replace of M5 Harvest / EUR M15 OS / AUD / UK. Two verdict ladders (§7): `EXPANSION_*` (small-n OK) vs `PRODUCTION-WORTHY` (full G0–G5). |
| **J-O** | Sample-size vs unified tiers | **USDJPY does not use n≥385 as a hard expansion criterion.** Report `n` and compute `M` (Wilson if n&lt;200). Verdicts key off **EF vs M**, walk-forward, and regime — not a fixed headcount floor. Tip n≈56 is usable Stage-0; still insufficient for production G1 alone. Prior Jan→Apr n=8 is **footnote only**, never sole KEEP driver. |
| **J-P** | Yen / FX book correlation | USDJPY is a **USD-fade / JPY twin-risk** asset vs EUR/AUD. Do not treat USDJPY KEEP as diversification vs live EUR/AUD without a separate covariance engine. Do not stack full research f with live FX as “hedged.” |
| **J-Q** | AOS | Engine magic **26101828** stays **AOS OFF**. No HITL research OS yet. Do not score EUR / UK / AUD L2 pins on this sleeve. Native USDJPY AIOS only after expansion KEEP + deal-scored Leak. |
| **J-R** | Window policy | **Primary** = May→Aug 2026 tip (or successor complete MATCH tip through Aug; Sep starved by design). **YTD** Jan→Oct = support. **Prior** Jan→Apr = thin ATR diagnostic (n=8). Long 2025→… = sparse context. Incomplete Oct stub = footnote. Hostile Jul labeled L3, not silent DROP if primary tip holds Stage 0 after costs review. |
| **J-S** | Side of edge | Balanced = **mixed WR + R** (RR 1.20). Soft target: WR ≫ 45.5% with R≈RR. Do not “fix” by shrinking AL as default; do not convert to trend RR or Harvest RR=1.0 without a new sleeve card. Tip/YTD **buy-led expectancy** with **sell-heavy fire count** is **regime side diagnosis**, not a permanent AllowSell=false lock. |
| **J-T** | Hygiene pockets | Profile soft pockets: **Thu**, hour **14**, **Jul**, sell-volume without edge thickness. Optional filter experiments need a **new preset_id / magic**; do not silently mutate 26101828 mid-book. |
| **J-U** | Probe vs Tester | Ouroboros M15* probe (WR 57.6% / EF +0.8 pp) is **design prior only**. Tester tip is blotter authority. Do not reject geometry solely because Tester ≪ probe; do not claim probe EF as scored EF. |
| **J-V** | Spread gate vs Leak | MaxSpread **25** is an entry filter, not a Leak estimate. Leak always from fills / cost model. |
| **J-W** | ATR / session selectivity | ATR max ≈ tight p50 + session 12–20 + Tue skip is the P0 stack. Tokyo 02–12 **failed** design probe — do not re-open without a new preset. Unfiltered / wider ATR≤92 sleeve = **new preset** + re-score. BB-width stays OFF. |
| **J-X** | Containment streaks | `InpMaxLossStreak=3` will pause; observed max loss streak **7** on tip is **expected under Jul stress**. Streak &gt; 1.5× theoretical raises `DEPENDENCE` → block-bootstrap before any f increase. |
| **J-Y** | Leak prior severity | USDJPY’s design Leak (**11.4 pp**) is **~3–4×** EUR M15 / UK100 priors because SL is short in points. Soft Stage-1 WR to clear prior Leak ≈ BWR+Leak ≈ **57%**. Tip WR 48% → EF_prior deeply negative is **cost geometry**, not meanrev class death. Measured Leak may be lower; until then zone = **costs_fragile**. |
| **J-Z** | Live / peer book boundary | Live Harvest (`8210204`), EUR M15 OS, AUD LIVE, UK research OS stay under their own frameworks. This file never admits or denies those books. Cross-citing foreign EF as USDJPY EF (or vice versa) is forbidden. |

---

## 2. Trade-event contract

### 2.1 Geometry

| Mode | Inputs | Event rule | Gates? |
| --- | --- | --- | --- |
| **G0 Balanced P0** | MaxLevels=1, MaxEntries=1, SL100/TP120 | One lifecycle = one event | Yes |
| Grid basket | Levels or entries > 1 | Basket flat = one event | Out of USDJPY expansion scope |
| Mixed as tickets | — | — | **G0 fail** |

### 2.2 Win / loss

- Win: `pnl_R > 0` after costs  
- Loss: `pnl_R < 0`  
- Scratch (`pnl_R = 0`): exclude from WR/R; keep in frequency/cost  

### 2.3 `exit_reason`

`TP` · `SL` · `MID` · `DAILY_FLAT` · `EQUITY_HALT` · `FAIL_PAUSE` · `MANUAL` / `EOT` · `OTHER`

Tolerance for TP/SL classification: |price move − designed distance| &lt; **3** points (0.003 price at Point=0.001). Else `OTHER`.

### 2.4 Identity metadata (required)

```text
ea_name: BMRG
symbol: USDJPY
timeframe: M15
magic: 26101828
preset_id: BMRG-M15-USDJPY-6M-P0_balanced_chart
geometry_mode: G0_SINGLE
designed_rr: 1.20
risk_definition: hard_stop_points
lot_mode: risk_pct_0.5
regime_filtered: true   # 12-20 + skip Tue + ATR max 70
baseline_frequency: 40  # events / 90d provisional (tip-scaled)
pool_role: Expansion_USDJPY_Balanced_P0
aos_overlay: none
sleeve_ladder: P0=26101828|alt_RR125=26101829|alt_BB20=26101830
costs_defaulted: <list or none>
```

### 2.5 `event_id`

```text
event_id = "26101828-USDJPY-{side}-{YYYYMMDDhhmmss}-{first_ticket}"
```

---

## 3. Stage 0 — Core identities (bound)

```
BWR = 1 / (1 + R)
BM  = WR − BWR
E_N = WR × (R + 1) − 1 = (R + 1) × BM
```

Use **realised R** for BWR/BM/E_N on scorecards when deal PnL exists. Designed BWR(RR=1.20)=**45.5%** is the sleeve label; FIXED_RR path may use designed R until R_real is measured from currency PnL.

### 3.1 Designed geometry

| Field | Value | Intent |
| --- | --- | --- |
| SL / TP | **100 / 120** | RR = **1.20** · BWR(RR) = **45.5%** · TP > SL |
| BB | 20 / **2.2** | Entry threshold |
| Cooldown | **2** bars | Champ-pattern hygiene |
| Session | **12:00–20:00** · skip Tue | London/NY overlap (Tokyo failed probe) |
| ATR gate | max **70** ON · min 0 | Cut Sep FRAGILE high-vol |
| BB-width | OFF | Avoid fire starvation |
| Class | Meanrev fade · **mixed WR + R** | Not Harvest WR-theatre · not trend |

### 3.2 Soft targets (expansion · after costs when known)

| Metric | Soft target | Fail / worry signal |
| --- | --- | --- |
| WR | > BWR; prefer ≥ **57%** after 25pt Leak prior; Stage-0 ≥ **45.5%** | ≤ BWR on W20+ of primary tip |
| R | ≈ 1.20 (±10% on FIXED_RR) | R ≪ RR without WR lift |
| BM | > 0; prefer ≥ **+11–12 pp** to clear prior Leak | BM ≤ 0 after costs on primary |
| E_N | > 0; prefer ≥ **+0.05R** on tip | ≤ 0 on tip W20 **and** tip calendar months |
| Soft stress month | WR can ≪ BWR (Jul-like) | Multi-month cluster ≪ BWR → L3 review, not auto DROP if tip E_N>0 |
| RR − R | ~0 | Gap > 25% of baseline → exit/slip audit |
| Fire count tip | n ≥ **30** (Stage 0 floor) | Starvation (prior Jan→Apr path) |
| MaxDD (research $500 / risk%) | soft under ~8–10% | Approach EA halt / DD_limit |

### 3.3 Side diagnosis (locked)

**Mixed WR + R** (Balanced RR 1.20). Edge = WR margin above 45.5% BWR **plus** modest R thickness. Tip/YTD may be **buy-led on expectancy** with sell-heavy fire count — score both sides; do not flip AllowBuy/AllowSell without a new preset.

---

## 4. Stage 1 — Cost, Leak, EF

### 4.1 Cost defaults (`costs_defaulted` until deal blotter)

| Component | USDJPY M15 default |
| --- | --- |
| Spread | Mean entry spread (pts) from blotter; else session median (MaxSpread gate 25) |
| Round-turn proxy | **2 × spread_pts** → `c_R_spread = (2 × spread_pts) / 100` (floor). Design card RT≈25 pts → `c_R≈0.25R` |
| Commission | Broker card (else 0 flagged) |
| Swap / financing | Broker × nights held when hold ≥1 session (secondary on tip; still mandatory if present) |
| Slippage | Measured fill delta; inside 2× spread proxy until fill fields exist |

```
Leak = c_R / (R + 1)     # report in pp of WR
EF   = BM − Leak
```

**Interim journal proxy (until deals):**  
Leak_prior ≈ **11.4 pp** (design). State `Leak_source=prior|proxy|measured` on every scorecard.

**Double-counting:** only L1 inside EF. L2 = `M` threshold. L3–L5 = gates/monitors (unified §4.2). Preset `InpAOS_Leak` is **not** L1.

### 4.2 Uncertainty `M`

```
M = 1.96 × sqrt(WR × (1 − WR) / n)
```

For **n &lt; 200** use **Wilson** half-width (unified FX-07). Expansion scorecards must state which. Small `n` widens `M` (harder to clear `EF > M`) — that is the sample-size effect; there is **no separate n≥385 reject** on the expansion ladder.

### 4.3 Zones

| Zone | Condition | Expansion action | Production action |
| --- | --- | --- | --- |
| Negative | EF ≤ 0 | EXPANSION_DROP or **costs_fragile** | Reject |
| Fragile | 0 &lt; EF ≤ M | EXPANSION_KEEP / WATCH · research small-f | Not production-worthy |
| Robust | EF > M | Eligible deepen sample / Stage 2 | Eligible Stage 2/4 |

**Interim rule while Leak is prior only:** tip EF_prior ≤ 0 does **not** alone force `EXPANSION_DROP` if Stage 0 (WR>BWR · E_N>0 · n≥30) holds — label **costs_fragile / WATCH** until measured Leak. Persistent **measured** EF≤0 on primary tip → DROP.

### 4.4 Provisional baselines (2026-10-19 · journal-gross)

> Descriptive until deal export. Assumes R ≈ 1.20 FIXED_RR; Leak **prior** 11.4 pp.

#### Primary tip · May→Aug 2026 · magic 26101828

| Metric | Value | Note |
| --- | ---: | --- |
| n | **56** | Report only — not a hard production floor; Stage 0 ≥30 met |
| WR / R | 48.2% / ≈1.20 | Dedicated tip run |
| BWR / BM | 45.5% / **+2.8 pp** | Gross · thin vs Leak prior |
| E_N | **+0.061R** | Gross · soft bar cleared |
| Leak_prior | **11.4 pp** | Replace with measured |
| EF_prior | **−8.6 pp** | Deeply negative under prior |
| M (normal approx) | ~**±13.1 pp** | Wilson preferred → zone **Negative / costs_fragile** |
| Zone (proxy) | **costs_fragile** | Stage 0 pass; deal Leak before stronger claims |
| Final Δ | **+$5.99** (+1.2%) | Equity confirms E_N direction |

#### Supporting YTD · Jan→Oct 2026

| Metric | Value | Note |
| --- | ---: | --- |
| n | 68 | Support |
| WR / E_N | 51.5% / **+0.132R** | Stronger than tip |
| EF_prior | **−5.4 pp** | Still ≤ 0 under prior |
| Label | Support · Jul L3 | Do not alone promote |

#### Prior · Jan→Apr 2026

| Metric | Value | Note |
| --- | ---: | --- |
| n | **8** | ATR-starved — footnote only |
| WR / E_N | 50.0% / +0.10R | Not a KEEP driver |

#### Long hist · 2025.01→2026.10

| Metric | Value | Note |
| --- | ---: | --- |
| n | 83 | Sparse 2025 fires |
| WR / E_N | 49.4% / +0.087R | Diluted context |
| EF_prior | −7.5 pp | Context only |

**Design probe (not blotter):** n≈66 · WR 57.6% · EF≈+0.8 pp — geometry design only.

**Rule:** Do not promote “Robust” from these rows. Deal blotter first. Do not score probe as EF.

---

## 5. Stage 2 — Health windows

Unified W100/W250/W500 assume large n. USDJPY expansion adds **small-n windows** until n≥250.

| Window | Size | Step | Role on USDJPY |
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
| Compressing | Margin falling 2 evals | Investigate: Jul / Thu / H14 / sell-volume (§10) |
| Near frontier | 0 &lt; EF ≤ M (or Stage 0 OK + EF_prior≤0) | Cap research f; no live; measure Leak |
| Below frontier | measured EF≤0 on W20 **and** primary tip | Halt this preset; regime / cost review |

Unified Stage 2 halt rules apply unchanged once W250/W500 exist.

### 5.2 Profile rolling snapshot (gross · 2026-10-19)

| Family | Result |
| --- | --- |
| Tip months | May/Jun E_N +0.19 / +0.20R · **Jul −0.27R (L3)** · Aug thin + |
| Tip W10 / W15 / W20 / W30 avg E_N | ~+0.01 / +0.01 / +0.02 / +0.04R |
| YTD W10 / W20 / W30 avg E_N | ~+0.05 / +0.04 / +0.06R (min deep in Jul path) |
| Soft L3 | Jul · Thu · H14 · sell fire without edge |
| Sep | **0 fires** under ATR≤70 (FRAGILE cut — correct) |

---

## 6. Stage 3 — Capital (research only)

| Item | Binding |
| --- | --- |
| Intent | Rank / size **research** capital only — **not** live FT attach · **not** EUR/AUD/UK replace |
| Lot | Risk% path until unlock / larger deposit |
| f_declared | 0.5% |
| f_realised | `risk_ccy / equity_at_open` per event |
| Kelly | Quarter–half of shrunk WR; **cap research ≤0.5%** until G1 Robust |
| DD_limit | **25%** default; EA equity halt 15% OK if tighter |
| Daily loss | Preset daily-loss % + flatten in path / MC |
| Ruin | P(equity ≤ 0.5 C₀) ≤ 1% |
| Overnight | Include overnight subset when present; tip is mostly session-bound |
| Cluster | Do **not** stack full research notional with live EUR/AUD as diversification (yen/USD cluster) |

Stage 3 ranking vs other expansion assets only after each has deal-scored EF and the same cost policy.

---

## 7. Stage 4 — Gates (two ladders)

### 7.1 Expansion ladder (asset list · pre-AIOS)

Use while building the research FX M15 list **before** USDJPY AIOS / live claims.

| Gate | Expansion pass |
| --- | --- |
| **E0** | Currency · G0 · preset/magic **26101828** match · costs policy stated · AOS OFF · yen geometry (not EUR/GBPJPY floors) |
| **E1** | Gross or measured: WR > BWR · E_N > 0 · n ≥ 30 on **primary tip** · soft-stress month not wipeout of whole tip |
| **E2** | ≥1 secondary window (YTD) not contradicting class; YTD/prior soft month EF/WR fail OK if labeled L3 |
| **E3** | `regime_filtered` documented (12–20 + Tue + ATR max); tip/YTD failures labeled L3 not silent DROP; Sep starve noted as gate |
| **E4** | n and `M` recorded · probe not used as scored EF · Leak_source stated · tip not required to match probe WR |

```
EXPANSION_KEEP   = E0 ∧ E1 ∧ E2 ∧ E3
EXPANSION_WATCH  = E0 ∧ E1 but thin/negative EF_prior, Fragile/costs_fragile zone, or Thu/Jul soft without L3 note
EXPANSION_DROP   = measured EF≤0 on primary tip after honest costs, or class break (trend geometry, TP<SL, AOS-on contamination, EUR/GBPJPY SL import without new card)
```

**Provisional label (2026-10-19, journal-gross + Leak prior):**  
**EXPANSION_KEEP** (borderline → **WATCH** until measured Leak) · Balanced P0 · magic **26101828** · AOS OFF — expansion keep, not production. Tip Stage 0 pass; EF_prior −8.6 pp → **costs_fragile** footnote.

### 7.2 Production ladder (unified G0–G5)

Unchanged maths from `doc/unified_edge_framework.md`. USDJPY notes:

| Gate | USDJPY notes |
| --- | --- |
| **G0** | Currency; G0; preset/magic match; costs recorded/defaulted · **no n≥385 floor** for expansion docs (n reported; `M` carries uncertainty). Production path still needs adequate n for G1 windows. |
| **G1** | EF>M full + W500 when able; WR > BWR+Leak; R bootstrap; **Leak from deals not preset meta / design prior** |
| **G2** | Anchored WF; WFE≥0.5; OOS E_N>0 in ≥75% folds — re-select ATR/session on **IS only** if retuning |
| **G3** | BM_worst>0 **or** declared regime_filtered (12–20+Tue+ATR max); concentration flag if &gt;70% E_N in one ATR×ER (or Ouroboros) cell |
| **G4** | MC-1/2/3; block 20; include overnight subset when present; stress cost ×1.5 path |
| **G5** | ±10% BBDev, SL, TP, MaxSpread, ATR max, CooldownBars; EF>0 at cost ×1.5 |

```
PRODUCTION-WORTHY(USDJPY_Balanced_P0) = G0 ∧ G1 ∧ G2 ∧ G3 ∧ G4 ∧ G5
```

**Status (2026-10-19):** **NOT PRODUCTION-WORTHY** (Leak unmeasured · G1–G5 not run — not an n-floor reject alone). Live remains EURUSD / AUDUSD books — USDJPY is expansion only.

---

## 8. Adapter bindings (blotter)

Follow unified §8 plus:

| Extra field | Required | Note |
| --- | --- | --- |
| `exit_reason` | yes | §2.3 |
| `spread_points_entry` | yes* | *or costs_defaulted |
| `nights_held` | yes* | swap when overnight |
| `session_ok` | no | 12–20 diagnostic |
| `atr_pts` | no | regime cell / ATR gate |
| `signal_tag` | no | buy/sell fade |
| `group_event_id` | yes | = event_id on G0 |
| `ouroboros_month_tag` | no | MATCH / FRAGILE context |
| `sleeve_ladder_note` | no | alt magics context if comparing |

Forbidden evidence: pips-mode Stage 1–3 · ticket WR with grid · preset/magic mismatch · profit-only optimise · tip-only production admission · scoring EUR/UK/AUD L2 on this sleeve · using `InpAOS_Leak` or probe EF as measured Leak/EF · pooling alt magics into one WR · claiming USDJPY KEEP diversifies live EUR/AUD · importing EUR/GBPJPY SL floors mid-book · re-opening Tokyo session without a new preset.

---

## 9. Benchmark protocol

1. Load `BMRG-M15-USDJPY-6M-P0_balanced_chart` · symbol **USDJPY** · M15 · every tick · ACCOUNT CURRENCY.  
2. Confirm Inputs = preset (SL100/TP120, BBDev 2.2, CD 2, 12–20, skip Tue, ATR max 70, BBw off, MaxSpread 25, magic 26101828, AOS off).  
3. Run **primary tip** window first; YTD as secondary; prior Jan→Apr as thin diagnostic only.  
4. Export deals → `blotter/inbox/` → archive `blotter/archive/USDJPY-P0-CHART-<date>/`.  
5. Aggregate events → WR, R, BWR, BM, Leak, EF, M, E_N, RR−R, side/DOW.  
6. Emit W10/W15/W20 (+ W100+ when able), calendar months, Ouroboros tags as footnotes.  
7. Apply **expansion ladder**; only then schedule production G0–G5.  
8. Update `system_profile.md` evidence tables from scorecard.  
9. Refresh Canvas from scorecard only (display).

---

## 10. Monitoring / investigation (USDJPY)

| Trigger | Response |
| --- | --- |
| WR ≤ BWR+Leak on W20 (tip) | Investigate Thu / H14 / Jul / ATR·session binding / sell-volume |
| EF ≤ 0 after measured Leak on primary tip | costs_fragile or EXPANSION_DROP |
| Tip OK, Jul soft | Label **regime mismatch (L3)**; do not silent DROP |
| Sep zero fires | Confirm ATR gate — expected on FRAGILE tip |
| Desire to open Tokyo 02–12 | Reject without new preset — probe failed |
| Desire to import EUR 300 / GBPJPY 160 SL | Reject — wrong ATR scale |
| RR−R gap > 25% | Exit mix / slippage audit |
| FREQUENCY_STALL | Confirm ATR/session gates — widen only via new preset task |
| Max loss streak > 1.5× expected | Block-bootstrap before any f / lot increase |
| Desire to “fix” with trend RR or TP&lt;SL | Reject — class break |
| Desire to pin EUR/UK/AUD L2 | Reject — wrong book AIOS |
| Desire to replace live Harvest with this sleeve | Reject — expansion only |

Investigation order (unified): **data → execution → regime → structural**.

---

## 11. Scorecard fields

```text
framework_unified: 1.0
framework_usdjpy: 0.1.0
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
regime_note: <optional L3 Jul/Thu / Ouroboros / Sep-starve note>
sleeve_ladder_note: <optional alt magic context>
canvas: display_only
```

---

## 12. Document map

| File | Purpose |
| --- | --- |
| `doc/unified_edge_framework.md` | General maths & production gates |
| `doc/edge_framework.md` | EURUSD **M5 Harvest** champion binding (do not use for USDJPY) |
| `doc/assets/EURUSD/edge_framework.md` | EURUSD M15 expansion binding |
| `doc/assets/AUDUSD/edge_framework.md` | AUDUSD Book A binding |
| `doc/assets/UK100/edge_framework.md` | UK100 expansion binding |
| `doc/assets/AAPL/edge_framework.md` | Apple expansion binding |
| **`doc/assets/USDJPY/edge_framework.md`** | **This file — USDJPY M15 P0 expansion binding** |
| `doc/assets/USDJPY/system_profile.md` | Class + observed behaviour |
| `doc/assets/USDJPY/README.md` | Asset doc index |
| `doc/BMRG_M15_USDJPY_6M_chart_preset.md` | Chart / design card |
| `Profiles/Tester/BMRG/USDJPY/` | Loadable presets |
| `blotter/archive/USDJPY-P0-CHART/` | Immutable P0 review |

---

## 13. Versioning

- **0.1.0** — Initial USDJPY M15 P0 binding: canvas caveat; gap table J-A…J-Z; Stage 0–4; small-n windows; Leak prior 11.4 pp vs measured (costs_fragile); yen ATR-scaled geometry; tip vs YTD / Jul L3; Sep starve as gate; expansion vs production ladders; provisional EXPANSION_KEEP / WATCH footnote on tip (journal-gross).  
- Bump when cost defaults, 1R, event rules, ladder criteria, baseline frequency, or sleeve geometry change.

---

## 14. One-line contract

**Score USDJPY M15 as a London/NY-filtered G0 Bollinger mean-reversion fade (Balanced RR1.20 · BB2.2 · ATR≤70 · AOS OFF) under unified identities; use expansion gates while n and measured Leak are thin; treat the high 25pt Leak prior as costs_fragile not class death; never let Canvas, probe tables, EUR/GBPJPY SL floors, foreign L2 pins, or tip charts override a blotter scored here; production-worthy only after full G0–G5 — live capital stays off USDJPY until then.**
