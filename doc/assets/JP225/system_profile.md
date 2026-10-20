# JP225 / JPN225 — System Profile (M15 Growth P1)

**Version:** 0.1.0  
**Status:** Descriptive evidence · expansion research  
**Engine:** Growth P1 wrLift fade · magic **26101904** · **AOS OFF**  
**Preset:** `Profiles/Tester/BMRG/JP225/BMRG-M15-JP225-6M-P1_wrLift_fade_chart.set`  
**AIOS plan:** [`aios_roadmap.md`](./aios_roadmap.md) · baseline [`JP225_AOS_BASELINE_v1.md`](./JP225_AOS_BASELINE_v1.md)  
**Normative scoring:** [`edge_framework.md`](./edge_framework.md)  
**Chart card:** `doc/BMRG_M15_JP225_6M_chart_preset.md`  
**Review:** `blotter/archive/JP225-P1-REVIEW/`

**Scope:** Research **asset-list expansion** (JP Nikkei CFD). **Not** a live replace for AUDUSD / EURUSD / UK100 / DE40. Own AIOS: **P0 stubs landed** — see roadmap; not required for expansion keep once tip EF clears (or MATCH-aware KEEP with regime label).

---

## 1. Class thesis

BMRG on JPN225 M15 is a **London-session mean-reversion fade** (FIXED_RR Growth) with **regime filtering** (ATR max ≈ p75 · skip Tue · 08–17). It wins when price stretches to BB extremes and reclaims toward mid under MATCH / paying FRAGILE cells. It loses when price **band-rides** (Nikkei impulse, risk-off trend days, MISMATCH / hostile FRAGILE cells) into the hard SL.

Soft or negative calendar months (**May FRAGILE**, **Jul/Oct MISMATCH**) are read first as **regime mismatch**, not class failure. **Jun FRAGILE** can still pay — do not equate FRAGILE tag with auto-skip.

---

## 2. Geometry & filters

| Piece | Value | Intent |
| --- | --- | --- |
| SL / TP | **23260 / 34890** | Growth RR **1.50** · clears ~2300 spread Leak |
| BB / CD / Fade | 20 / **2.3** / CD2 / Fade **ON** | P1 WR-lift after P0 EF fail |
| Session | **08:00–17:00** · **skip Tue** | London sleeve (Tokyo 02–09 failed probe) |
| ATR regime | ON · max **19670** (≈p75) | Cut May/Jun HV; Gate G3 declared |
| BB-width | OFF | Avoid fire starvation |
| Grid | G0 MaxLevels=1 / MaxEntries=1 | Clean events |
| Lot / MaxSpread | **0.1** / **3000** | Broker min · live spread≈2300 |
| AOS | **OFF** | Pure engine fingerprint |

**Why Growth not Balanced/Harvest:** under cost prior 2500, Balanced Leak eats BM; Harvest WR↑ but EF≤0; thin ATR-p50 SL Leak ~7.2 pp. Growth is the only design-viable geometry on this name.

---

## 3. Key metrics (Tester blotter 2026-10-19)

| Window | n | WR | EF_prior | E_N | Δ$ ($500) |
| --- | ---: | ---: | ---: | ---: | ---: |
| Tip May→Aug | **79** | **43.0%** | **−1.3 pp** | +0.076R | +9.28 |
| Jan→Aug | 143 | 42.0% | −2.3 pp | +0.049R | +17.18 |
| Long 2025→tip | 360 | 41.7% | −2.6 pp | +0.042R | +22.14 |
| MATCH Aug only | 23 | **52.2%** | **+7.9 pp** | +0.304R | — |

Geometry: realised R=**1.500** · tp_lt_sl=**0**.

**Stage 0 tip:** weak PASS (E_N>0 · WR>BWR). **Stage 1 tip:** FAIL (EF≤0 after Leak prior). Probe overstated WR (~47% design vs 43% blotter).

---

## 4. Regime map (Ouroboros meanrev H1)

| Month | Tag | P1 behaviour |
| --- | --- | --- |
| 2026-05 | FRAGILE | Tip hole WR 30% |
| 2026-06 | FRAGILE | **Pays** WR 55% |
| 2026-07 | MISMATCH | Tip hole WR 31% |
| 2026-08 | MATCH | **Home** WR 52% |
| 2026-09 | MATCH | Long WR 50% |
| 2026-10 | MISMATCH | Thin incomplete |

---

## 5. Expansion posture

| Question | Answer |
| --- | --- |
| Keep on expansion list? | **YES** — geometry + MATCH edge healthy |
| Live replace incumbents? | **NO** |
| AIOS now? | **P1 DONE** — next P2 L2det; OS mission = tip EF clear via regime / Wed / hour hygiene |
| Next engine alt? | Optional P1.5 light (**26101905**) — re-freeze if Stage-1 win AOS OFF |
| Side / DOW / hour | Tip: **BUY-led** · **Wed soft** · H08/H14 soft · SELL≈flat · near_atr **pays** |

---

## 6. One-line profile

**JP225 M15 BMRG is a London-filtered G0 Bollinger mean-reversion Growth fade (RR1.50 · fat SL · ATR≤p75 · Fade ON · AOS OFF); tip May→Aug 2026 realises WR 43% / E_N +0.08R / EF −1.3 pp under Leak prior — Stage-1 fail from OFFHOME mix while MATCH Aug prints EF +7.9 pp — expansion keep with a JP225-native AIOS to withhold May/Jul(Oct) cells, not a live replace.**
