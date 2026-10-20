# JP225 — P6 hardening (L9 · L2 stress · ATR G3)

**Version:** 1.0.0  
**Tasks:** JP225-AOS-P6-T01 … T03  
**Date:** 2026-10-19  
**Evidence:** `blotter/archive/JP225-AOS-P6/P6_HARDEN.json`  
**Upstream:** [`aos_l2_policy.md`](./aos_l2_policy.md) May∨Jul · Leak measured 2.45 pp  

**Mode:** Policy + offline CF. No geometry change. L2 AI DISARM. No MQH / research OS `.set`.

---

## 0. Verdict

| Task | Verdict |
| --- | --- |
| P6-T01 L9 session soft veto | **PASS** — no LIVE L9 · London/H08/H14 HOLD_SHADOW · spread DISARM |
| P6-T02 L2det arm-width / ±10% soft stress | **PASS_WITH_NOTES** — keep May∨Jul · Wed widen stalls · near_atr alone DISARM |
| P6-T03 ATR max G3 | **PASS** — 19670 on P0 + P1 (P1.5 alt = 18620 · not OS) |
| Phase | **P6_COMPLETE** |

---

## 1. P6-T01 — L9 session quality

Cash/index sleeve (session 08–17). Tip spread nunique=3 · std≈356 · p66=1400 — some variance, but **spread > p66** loses tip E_N → **DISARM**.

| Policy | Tip verdict | ΔE_N | Prec | Ret% | Aug/Jun FP | n |
| --- | --- | ---: | ---: | ---: | --- | ---: |
| skip H08 | **HOLD_SHADOW** | +0.051 | 0.75 | 89.9 | 1 / 1 | 8 |
| skip BUY∧H08 | **NO_SKIPS** | 0 | — | 100 | — | 0 |
| skip London open H08–09 | **HOLD_SHADOW** | +0.096 | 0.73 | 81.0 | 1 / 2 | 15 |
| skip H14 | **HOLD_SHADOW** | +0.065 | 0.64 | 72.2 | 4 / 3 | 22 |
| spread > tip p66 | **DISARM** | −0.076 | 0.43 | 82.3 | 8 / 0 | 14 |

Additive on **May∨Jul-kept**: H08 / London HOLD_SHADOW; H14 / spread DISARM or thin.

### Wire stance (P6)

| ID | Stance |
| --- | --- |
| `L9_skip_spread_tercile` | **DISARM** (negative tip ΔE_N · Aug collateral) |
| `L9_skip_H08` / London open | **HOLD_SHADOW** — not LIVE (Jun FP) |
| `L9_skip_BUY_H08` | **NO_SKIPS** on tip — unused |
| `L9_skip_H14` | **HOLD_SHADOW** — already P2 HOLD; not stacked LIVE |

Overlay `L2det_jp225_v1_May_OR_Jul` remains the research L2 path. L9 is additive soft layer, not a replace.

---

## 2. P6-T02 — L2det stress (arm width + soft ±10%)

Baseline tip May∨Jul: kept E_N **+0.337R** · ret **54.4%** · ΔE_N vs tip **+0.261** (HOLD_SHADOW under measured FP gates; P2 ARM retained).

| Stress | kept E_N | Δ vs tip | Ret% | Read |
| --- | ---: | ---: | ---: | --- |
| may_fragile / may_all | 0.205 | +lift | 70.9 | Still lifts tip · thinner than champ |
| jul_only | 0.136 | +lift | 83.5 | Still lifts · weaker |
| sell∧may | 0.231 | +lift | 82.3 | Narrow atom OK |
| **may∨jul∨wed** | 0.364 | — | **41.8** | **REJECT_FREQUENCY_STALL** — do not widen |
| nearATR soft ±10% | — | — | — | alone stays **DISARM** (P2) |
| AI thr ±10% (0.75) | — | −0.06 | — | stays DISARM / no LIVE |

**Read:** Keep primary **May∨Jul**. Do not LIVE-wire Wed widen. Do not promote near_atr or L2AI. SL/TP untouched. Engine ATR max 19670 is G3, not an L2 knob.

---

## 3. P6-T03 — ATR max / G3 declaration

| Preset | ATR regime | Max pts | G3 |
| --- | ---: | ---: | --- |
| `…P0_growth_chart.set` (Presets + Profiles/Tester) | true | **19670** | OK |
| `…P1_wrLift_fade_chart.set` (same) | true | **19670** | OK |
| `…P1p5_light_chart.set` (alt) | true | 18620 | **not OS** until re-freeze |

Filters apply **before** AOS entry — OS cannot lift ATR max.  
Declaration: `regime_filtered=true` · session 08–17 · skip Tue · ATR max **19670**.  
No research OS `.set` yet (P7).

---

## 4. Sign-off

P6 complete. Research stack stays:

```text
Engine Growth P1 (26101904) AOS OFF chart
+ L2det May∨Jul SHADOW offline (no MQH)
+ P4 ledger offline · L3/L4 policy signed
+ L9 London/H08/H14 SHADOW only (not wired LIVE)
+ L2 AI DISARM (AUC 0.49)
```

Next: **P7** promotion packet / HITL (target magic **26151907**). Still **no** live FX/EU replace.
