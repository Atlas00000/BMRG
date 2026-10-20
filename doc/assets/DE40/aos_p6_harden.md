# DE40 — P6 hardening (L9 · L2 stress · ATR G3)

**Version:** 1.0.0  
**Tasks:** DE40-AOS-P6-T01 … T03  
**Date:** 2026-10-19  
**Evidence:** `blotter/archive/DE40-AOS-P6/P6_HARDEN.json`  
**Upstream:** [`aos_l2_policy.md`](./aos_l2_policy.md) BUY∧near_atr · research OS P4  

**Mode:** Policy + offline CF. No geometry change. L2 AI still DISARM. L2det MQH still absent.

---

## 0. Verdict

| Task | Verdict |
| --- | --- |
| P6-T01 L9 session soft veto | **PASS** — no new LIVE veto · Frankfurt/H08 HOLD · spread DISARM · H13 stays P2 HOLD |
| P6-T02 ±10% L2det stress | **PASS_WITH_NOTES** — do not loosen nearATR; keep 0.9 / 4070 |
| P6-T03 ATR max G3 | **PASS** — 4070 declared on P0 + P4 research OS |
| Phase | **P6_COMPLETE** |

---

## 1. P6-T01 — L9 session quality

Cash sleeve (session 08–17). Tip spread nunique=6 · std≈83 · p66=84 — some variance, but **spread > p66** loses tip E_N → **DISARM**.

| Policy | Tip verdict | ΔE_N | Prec | Ret% | Aug/SELL/Mon FP | n |
| --- | --- | ---: | ---: | ---: | --- | ---: |
| skip H08 (all) | **DISARM** | −0.036 | 0.38 | 66.2 | 7 / 9 / 5 | 26 |
| skip BUY∧H08 | **HOLD_SHADOW** | +0.001 | 0.42 | 84.4 | 3 / 0 / 2 | 12 |
| skip Frank open H08–09 | **HOLD_SHADOW** | +0.006 | 0.42 | 59.7 | 8 / 10 / 6 | 31 |
| skip H13 | **HOLD_SHADOW** | +0.070 | 0.58 | 84.4 | 3 / 2 / 1 | 12 |
| spread > tip p66 | **DISARM** | −0.011 | 0.38 | 89.6 | 3 / 2 / 2 | 8 |

Additive on **ARM-kept** (after BUY∧near_atr): H08 / Frank / H13 → HOLD_SHADOW only; spread still DISARM.

### Wire stance (P6)

| ID | Stance |
| --- | --- |
| `L9_skip_spread_tercile` | **DISARM** (negative tip ΔE_N) |
| `L9_skip_H08` / Frank open | **HOLD_SHADOW** — not LIVE (Aug/SELL collateral) |
| `L9_skip_BUY_H08` | **HOLD_SHADOW** — thin additive |
| `L9_skip_H13` | **HOLD_SHADOW** — already P2 HOLD; not stacked LIVE |

Overlay `L2det_de40_v1_BUY_near_atr` remains the research L2 path. L9 is additive soft layer, not a replace.

---

## 2. P6-T02 — ±10% L2det threshold stress

Baseline tip ARM (BUY∧nearATR frac=0.9 · cap=4070): kept E_N **+0.415R** · ret **80.5%**.

| Stress | frac / cap | kept E_N | Δ vs ARM | Ret% |
| --- | --- | ---: | ---: | ---: |
| near_frac −10% | 0.81 / 4070 | 0.432 | **+0.017** | 71.4 |
| near_frac +10% | 0.99 / 4070 | 0.320 | **−0.095** | 97.4 |
| atr_cap −10% | 0.90 / 3663 | 0.432 | +0.017 | 71.4 |
| atr_cap +10% | 0.90 / 4477 | 0.320 | **−0.095** | 97.4 |
| both loose / tight | — | 0.425 | +0.010 | 77.9 |

**Read:** Loosening nearATR (**+10%**) hurts tip E_N hard (skips almost vanish). Tightening is mild E_N gain but cuts frequency (~71% ret). Keep defaults **frac=0.9 · nearATR ref=4070**. Do not stress-test by changing SL/TP. Engine ATR max (4070) stays separate G3.

---

## 3. P6-T03 — ATR max / G3 declaration

| Preset | ATR regime | Max pts | G3 |
| --- | ---: | ---: | --- |
| `…P0_balanced_chart.set` (Presets + Profiles/Tester/BMRG/DE40/) | true | **4070** | OK |
| `…P4_research_OS_W50.set` (same) | true | **4070** | OK |

Filters apply **before** AOS entry — OS cannot lift ATR max.  
Declaration: `regime_filtered=true` · session 08–17 · skip Tue · ATR max **4070**.

---

## 4. Sign-off

P6 complete. Research stack stays:

```text
Engine Balanced P0 (26101902) AOS OFF chart
+ L2det BUY∧near_atr SHADOW offline (no MQH)
+ P4 research .set (26141904): L3/L4/W50/ledger · AiOsMode OFF
+ L9 Frankfurt/H08/H13 SHADOW only (not wired LIVE)
+ L2 AI DISARM
```

Next: **P7** promotion packet / HITL. Measured Leak still OPEN.
