# DE40 — Edge Framework

**Version:** 0.1.0  
**Status:** Normative for **DE40 / DE30 M15 expansion** benchmarking  
**Parent:** `doc/unified_edge_framework.md` v1.0  
**Companions:** [`system_profile.md`](./system_profile.md) · [`aios_roadmap.md`](./aios_roadmap.md) · [`README.md`](./README.md)  
**Preset:** `Profiles/Tester/BMRG/DE40/BMRG-M15-DE40-6M-P0_balanced_chart.set`  
**Magic:** **26101902** · AOS **OFF**  
**Primary evidence:** 2026.05.01 → 2026.10.18 · Tester cache · profile 2026-10-19  
**Chart card:** `doc/BMRG_M15_DE40_6M_chart_preset.md`  
**Review:** `blotter/archive/DE40-P0-CHART/`

This document **binds** the unified edge framework to the DE40/DE30 M15 **Balanced P0** extract. Where this file and the unified doc conflict on **DE40 procedure**, **this file wins**. Formulae remain those of the unified doc.

**Not** EURUSD M5 Harvest · **not** EURUSD M15 · **not** AUDUSD · **not** UK100 · **not** USDJPY · **not** AAPL. Do not mix scorecards or magics.

---

## 0. Canvas caveat

| Artifact | Role | Authority |
| --- | --- | --- |
| **This markdown** | Contract: score DE40 Balanced P0, gates, adapter, gap fillings | **Normative** |
| **`doc/unified_edge_framework.md`** | Shared maths, stages, G0–G5 | Normative for **formulae** only |
| **`doc/assets/DE40/system_profile.md`** | Class thesis · observed behaviour · rolling tables | Evidence / descriptive |
| **`Profiles/Tester/BMRG/DE40/*.set`** | Locked inputs | Geometry source |
| **`blotter/archive/DE40-*/`** | Immutable scored runs | Evidence of record |
| **`doc/BMRG_M15_DE40_6M_chart_preset.md`** | Design / probe card | Design prior only |
| **Canvas / chat charts / UI tiles** | Visual snapshot of a scorecard | **Display only** |

**Rules**

1. **Canvas ≠ verdict.**  
2. **System profile ≠ gate pass** until deal blotter measures full `c_R`. Tip EF under Leak **prior** is descriptive Stage-1 proxy only.  
3. Changing 1R definition, event aggregation, cost defaults, sleeve identity, or gate bindings **bumps this version**.  
4. **Tip charts are not admission.** May→Oct tip can support `EXPANSION_KEEP`; not production alone.  
5. **Probe ≠ blotter.** Ouroboros M15* probe (WR≈58.2% · EF≈+4.0 pp) is geometry design only — even when aligned with Tester.  
6. **Do not mix books.** Foreign magics under this contract (or 26101902 under another) is G0 fail.  
7. **2025 MISMATCH stub ≠ class death.** Broker depth from **2025.06.05**; Jun–Jul MISMATCH losses are L3 regime, not DROP while tip Stage 0 holds.  
8. **Fat spread ≠ thin SL.** Live spread ≈1020 pts → SL 5000 is structural. Thinning SL without a new preset is G0 / Leak fail.  
9. **Index book boundary.** UK100 / US30 / DE40 are separate sleeves — do not cross-cite EF.

---

## 1. Gaps in the unified framework — DE40 fillings

| # | Unified gap | DE40 / DE30 P0 binding |
| --- | --- | --- |
| **D-A** | Trade event / grid | G0 only: MaxLevels=1 · MaxEntries=1 → **ticket = event**. |
| **D-B** | 1R declaration | Hard SL: `1R = InpSL_Points × volume × tick_value`. Designed SL = **5000** points. Point = **0.01** (Digits=2). Lot **0.1**. Scorecard must state SL + lot. |
| **D-C** | RR vs realised R | Benchmark on **R**. Designed RR = **1.25**. Tip realised R≈**1.24**. Expect `FIXED_RR_FADE`. |
| **D-D** | Instrument costs | DE30 fat spread. Default until measured: RT≈**1100 pts** → `c_R≈0.22R` → Leak≈**9.8 pp** at R=1.25. Prefer measured fills. Preset `InpAOS_Leak=9.8` = metadata only. |
| **D-E** | Regime tags vs filters | `regime_filtered=true` via **08:00–17:00** · **skip Tue** · ATR **max 4070** (≈p75). Soft **Feb / Mar / MISMATCH / FRAGILE residual** = L3 regime leak, not auto class death. Ouroboros monthly tags = context. |
| **D-F** | Geometry origin | SL/TP are **DE40 M15-calibrated** (~1.55× ATR p50≈3230) to clear spread tax. Not a silent UK100 2500pt transfer. Do not import FX SL floors. |
| **D-G** | Pips / points-only PnL | **Inadmissible** for Stage 1–3. ACCOUNT CURRENCY only. |
| **D-H** | Lot vs f | Research lot **0.1** (min volume). Report `f_realised` on deal export. |
| **D-I** | Session vs inventory | Entries gated 08–17; expect **cash-sleeve** holds (UK100-like). Overnight secondary until tape proves otherwise. |
| **D-J** | Pause / EOT | Tag `exit_reason`. Fail-pause after loss streak=3 expected under stress. |
| **D-K** | Preset / sleeve identity | Score **one magic:** **26101902**. Research OS future **26141907**. Mismatch → G0 fail. |
| **D-L** | Baseline frequency | Provisional **~35–45 events / 90d** from tip (~14 / 30d). `FREQUENCY_STALL` = 90d &lt; **50%** tip baseline. Do not raise frequency by lifting ATR max without new preset. |
| **D-M** | Mid rarity | Tip PnL clusters ≈ pure TP/SL → `FIXED_RR_FADE`. |
| **D-N** | Expansion vs production | DE40 is **asset expansion**, not live replace of FX/UK OS. Two ladders: `EXPANSION_*` vs `PRODUCTION-WORTHY`. |
| **D-O** | Sample-size | **No n≥385 hard floor** for expansion. Tip n≈77 usable Stage-0; insufficient alone for production G1. |
| **D-P** | Index correlation | DE40 vs UK100 / US30 / EUR risk — do not treat KEEP as automatic diversification without covariance engine. |
| **D-Q** | AOS | Engine **26101902** stays **AOS OFF** until P7. No foreign L2 pins. Native DE40 AIOS only — see [`aios_roadmap.md`](./aios_roadmap.md). |
| **D-R** | Window policy | **Primary** = May→Oct 2026 tip. **YTD** = support. **2025 stub** = MISMATCH footnote. Incomplete Oct = footnote. |
| **D-S** | Side of edge | Balanced = **mixed WR + R** (RR 1.25). Soft target WR ≳ **54–58%** after Leak prior. Side OPEN until tape. |
| **D-T** | Hygiene pockets | Feb · Mar FRAGILE · MISMATCH stubs · residual FRAGILE near ATR. Optional filters need **new preset_id / magic** — do not mutate 26101902 mid-book. |
| **D-U** | Probe vs Tester | Probe WR 58.2% ≈ Tester 58.4% — still probe = prior, tip = blotter authority. |
| **D-V** | Spread gate vs Leak | MaxSpread **1500** is entry filter, not Leak. |
| **D-W** | ATR / session selectivity | ATR≤p75 + 08–17 + Tue skip = P0 stack. Unfiltered / p90 sleeve = **new preset** + re-score. |
| **D-X** | Containment streaks | MaxLossStreak=3 armed; YTD path soft under Feb–Mar expected. |
| **D-Y** | Leak vs tip BM | Tip BM +14 pp clears Leak prior 9.8 pp → EF prior +4.2 pp. YTD does not. Measure before P7. |
| **D-Z** | Live / peer boundary | Live FX / UK research OS stay under their own frameworks. Cross-citing foreign EF as DE40 EF is forbidden. |

---

## 2. Trade-event contract

- G0 single-leg events only.  
- Score **basket / ticket** closes that realise TP or SL (FIXED_RR).  
- Exclude EOT orphans from WR/R; count in frequency.  
- Aggregation: one event per closed trade under magic 26101902.

---

## 3. Formulae (unchanged from unified)

```
BWR = 1 / (1 + R)
BM  = WR − BWR
Leak = c_R / (R + 1)
EF  = BM − Leak
E_N = WR × (R + 1) − 1
```

Designed: R≈1.25 · BWR=44.4% · Leak prior≈9.8 pp.

---

## 4. Cost binding

See [`aos_cost_policy.md`](./aos_cost_policy.md). Until deals: `Leak_source=prior`. Tip EF prior > 0 does **not** waive measured Leak for P7.

---

## 5. Stage gates (expansion)

| Stage | DE40 bar |
| --- | --- |
| **0** | n≥30 · WR>BWR · E_N>0 · TP≥SL · tip MaxDD contained |
| **1** | EF>0 preferred after **measured** Leak; tip prior already +4.2 pp as proxy only |
| **2+** | Walk-forward / regime cells / MC — required for production, not every OS weekly trial |

**Tip Stage 0:** **PASS** (n=77 · WR 58.4% · E_N +0.31R).  
**Tip Stage 1 prior:** preferred KEEP under prior; **measured OPEN**.

---

## 6. Expansion verdict ladder

| Verdict | Meaning |
| --- | --- |
| **EXPANSION_KEEP** | Tip Stage 0 (+ preferred EF prior) · stay on asset list · OS stream OK |
| **EXPANSION_WATCH** | Soft / costs_fragile / thin EF — iterate OS or re-measure |
| **EXPANSION_HOLD** | Insufficient evidence / FREQUENCY_STALL |
| **EXPANSION_DROP** | Tip Stage 0 fail with no regime excuse — rare; do not DROP on 2025 stub alone |
| **PRODUCTION-WORTHY** | Full G0–G5 + HITL — not claimed for DE40 yet |

Current engine posture: **EXPANSION_KEEP** (tip).

---

## 7. OS iteration (summary)

Full bars in [`aios_roadmap.md`](./aios_roadmap.md) §5. Short form:

- Accept layer if tip E_N/EF ≥ baseline −1 pp EF and MaxDD ≤ baseline +2 pp.  
- Reject WR↑ E_N↓, geometry “OS”, foreign pins, thin-SL, 2025-stub DROP.

---

## 8. Versioning

- **0.1.0** — Initial DE40 binding from Balanced P0 tip/YTD/stub score · AIOS P0 stubs.  
- Bump on geometry, cost default, window, or gate changes.
