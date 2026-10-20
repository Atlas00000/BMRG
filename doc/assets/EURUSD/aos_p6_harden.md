# EURUSD M15 — P6 hardening (L9 · L2 stress · ATR G3)

**Version:** 1.0.0  
**Tasks:** EURUSD-AOS-P6-T01 … T03  
**Date:** 2026-10-18  
**Evidence:** `blotter/archive/EURUSD-AOS-P6/P6_HARDEN.json`  
**Upstream:** [`aos_l2_policy.md`](./aos_l2_policy.md) v1b · research OS P4  

**Mode:** Policy + offline CF. No geometry change. L2 AI still DISARM.

---

## 0. Verdict

| Task | Verdict |
| --- | --- |
| P6-T01 L9 session soft veto | **PASS** — spread weak; H19 / BUY∧H19 **ARM_SOFT** (already P2 thin) · keep SHADOW |
| P6-T02 ±10% L2det stress | **PASS_WITH_NOTES** — do not loosen nearATR; keep 0.9 / 74 |
| P6-T03 ATR max G3 | **PASS** — 74 declared on P2 + P4 research OS |
| Phase | **P6_COMPLETE** |

---

## 1. P6-T01 — L9 session quality

Tip entry spread nunique ≤ 2 → tercile soft veto has little tip signal → **DISARM** (HOLD_SHADOW only if used alone).

| Policy | Tip verdict | ΔE_N | Prec | Ret% | SELL FP | MonFri FP | n |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| **skip H19 (all)** | **ARM_SOFT** | +0.021 | 0.67 | 93.3 | 0 | 1 | 3 |
| **skip BUY∧H19** | **ARM_SOFT** | +0.021 | 0.67 | 93.3 | 0 | 1 | 3 |
| skip H18–19 late | **ARM_SOFT** | +0.075 | 0.80 | 88.9 | 0 | 1 | 5 |
| skip H13 | HOLD_SHADOW | +0.045 | 0.63 | 82.2 | 2 | 1 | 8 |
| spread > tip p66 | HOLD_SHADOW | +0.016 | 0.57 | 84.4 | 2 | 2 | 7 |

Additive on **v1b-kept** path: H19 / BUY∧H19 → HOLD_SHADOW (thin). Late H18–19 additive stays ARM_SOFT shadow (n=3).

### Wire stance (P6)

| ID | Stance |
| --- | --- |
| `L9_skip_spread_tercile` | **DISARM** (tip low variance; revisit if fills vary) |
| `L9_skip_H13` | **HOLD_SHADOW** (SELL collateral — already P2 HOLD) |
| `L9_skip_H19` / `BUY∧H19` | **ARM_SOFT / SHADOW** — optional ledger reason; **not** LIVE in EA until P7 HITL (thin n=3) |
| `L9_skip_late_H18_19` | Prefer H19 atom over broad late block |

L2det v1b remains the live research overlay. L9 is additive soft layer, not a replace.

---

## 2. P6-T02 — ±10% L2det threshold stress

Baseline tip v1b: kept E_N **+0.234R** · ret **68.9%**.

| Stress | frac / cap | kept E_N | Δ vs v1b | Ret% |
| --- | --- | ---: | ---: | ---: |
| near_frac −10% | 0.81 / 74 | 0.212 | **−0.02** | 57.8 |
| near_frac +10% | 0.99 / 74 | 0.095 | **−0.14** | 82.2 |
| atr_cap −10% | 0.90 / 66.6 | 0.212 | −0.02 | 57.8 |
| atr_cap +10% | 0.90 / 81.4 | 0.095 | **−0.14** | 82.2 |
| both loose / tight | — | 0.234 | 0 | 68.9 |

**Read:** Loosening nearATR (**+10%**) hurts tip E_N hard. Tightening is mild E_N loss but stalls frequency (~58% ret). Keep EA defaults **frac=0.9 · cap=74**. Do not stress-test by changing SL/TP.

---

## 3. P6-T03 — ATR max / G3 declaration

| Preset | ATR regime | Max pts | G3 |
| --- | ---: | ---: | --- |
| `…P2_light_selective_chart.set` | true | **74** | OK |
| `…P4_research_OS_W50.set` (Presets + Profiles/Tester/BMRG/EURUSD/) | true | **74** | OK |

Filters apply **before** `AOSAllowEntry` — OS cannot lift ATR max.  
Declaration: `regime_filtered=true` · session 12–20 · skip Tue · ATR max **74**.

---

## 4. Sign-off

P6 complete. Research OS stack stays:

```text
Engine P2 light (26101817)
+ L2det_eur_m15_v1b LIVE_WITHHOLD (research magic 26121804)
+ L3/L4/W50/ledger
+ L9 H19 SHADOW only (not wired LIVE)
+ L2 AI DISARM
```

Next: **P7** promotion packet / HITL. Measured Leak+swap still OPEN.
