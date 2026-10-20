# DE40 M5 — P6 hardening (L9 · L2 stress · ATR G3)

**Version:** 1.0.0  
**Tasks:** DE40-M5-AOS-P6-T01 … T03  
**Date:** 2026-10-20  
**Evidence:** `blotter/archive/DE40-M5-AOS-P6/P6_HARDEN.json`  
**Upstream:** [`aos_l2_policy_M5.md`](./aos_l2_policy_M5.md) v1b · P4/P5 wire  

**Mode:** Policy + offline CF. No geometry change. L2 AI still DISARM.  
**L9 focus:** Frankfurt open / spread tercile — **protect Aug / SELL**.  
**Sibling:** M15 [`aos_p6_harden.md`](./aos_p6_harden.md) — **do not merge** ATR (2380 vs 4070) or L2det maps.

---

## 0. Verdict

| Task | Verdict |
| --- | --- |
| P6-T01 L9 session soft veto | **PASS** — no new LIVE veto · Frankfurt/H08 **DISARM** · H13/spread **HOLD_SHADOW** |
| P6-T02 ±10% L2det bound stress | **PASS_WITH_NOTES** — keep **(BUY∧H14\|16)∨(BUY∧Oct)**; do not widen Sep; never skip nearATR |
| P6-T03 ATR max G3 | **PASS** — **2380** declared on P0 + P4 research OS |
| Phase | **P6_COMPLETE** |

---

## 1. P6-T01 — L9 session quality

Tip spread median **≈92** · p66 has signal, but SELL FP blocks ARM_SOFT.

### On full tip

| Policy | Tip verdict | ΔE_N | Prec | Ret% | Aug FP | SELL FP |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| skip H08 | **DISARM** | −0.016 | 0.25 | 96.7 | 2 | 0 |
| skip BUY∧H08 | **DISARM** | −0.026 | 0.00 | 97.6 | 2 | 0 |
| skip Frank open H08–09 | **DISARM** | −0.039 | 0.37 | 84.6 | 4 | **7** |
| skip H13 | HOLD_SHADOW | +0.009 | 0.50 | 90.2 | 2 | 2 |
| skip spread > p66 | HOLD_SHADOW | +0.036 | 0.56 | 85.4 | 1 | **6** |
| skip H14+ (all) | HOLD_SHADOW | +0.056 | 0.56 | 79.7 | 3 | **7** |

### Additive on **v1b-kept** path

| Policy | Verdict | ΔE_N | Ret% | Note |
| --- | --- | ---: | ---: | --- |
| add H08 / Frank open | **DISARM** | negative | — | Aug collateral |
| add H13 | HOLD_SHADOW | +0.007 | 90.0 | thin |
| add spread > p66 | **DISARM** | −0.003 | 89.1 | no lift on kept |
| add H14+ | **DISARM** | −0.010 | 86.4 | L2det already covers BUY∧ |

### Wire stance (P6)

| ID | Stance |
| --- | --- |
| `L9_skip_spread_tercile` | **DISARM / no LIVE** (SELL FP; no additive lift on v1b) |
| `L9_skip_H08` / Frank open | **DISARM** — Aug / Frank collateral |
| `L9_skip_BUY_H08` | **DISARM** |
| `L9_skip_H13` | **HOLD_SHADOW** — not LIVE |
| `L9_skip_H14_plus` | **DISARM as L9** — already in L2det BUY∧; do not double-wire |

Overlay `L2det_de40_m5_v1b` remains the research L2 path. L9 is additive soft layer, not a replace.

---

## 2. P6-T02 — L2 bound stress (hour / month · not nearATR)

Baseline tip v1b: kept E_N **+0.289R** · ret **89.4%** · SELL FP **0**.

| Stress | kept E_N | Δ vs v1b | Ret% | Read |
| --- | ---: | ---: | ---: | --- |
| **v1b nominal** | **0.289** | **0** | **89.4** | **keep** |
| BUY∧H14 only (+Oct) | 0.263 | −0.025 | 92.7 | narrowing hurts |
| BUY∧H16 only (+Oct) | 0.274 | −0.014 | 91.9 | narrowing hurts |
| BUY∧H13–16 wide | 0.289 | ≈0 | 83.7 | no lift · ret cost |
| BUY∧H14–17 wide | 0.307 | +0.019 | 85.4 | HOLD — Sep-ish collateral risk |
| BUY∧H14\|16 ∨ BUY∧Sep–Oct | 0.309 | **+0.020** | **79.7** | **note only** — P2 said never blanket Sep |
| BUY∧H14\|16 only (no Oct) | 0.263 | −0.025 | 92.7 | Oct leg earns its keep |
| BUY∧Oct only | 0.250 | −0.039 | 95.1 | H14\|16 leg earns its keep |
| H14\|16 all sides ∨ BUY∧Oct | 0.295 | +0.006 | 86.2 | HOLD — 2 SELL FP |
| BUY∧H14\|16 ∨ Oct all | 0.292 | +0.003 | 87.8 | HOLD — 1 SELL FP |
| **REJECT probe BUY∧nearATR** | **0.194** | **−0.095** | 79.7 | **confirms tip star** |

**Read:** Keep EA defaults **(BUY∧H14\|16)∨(BUY∧Oct)**. Do not widen into Sep at P6. Do not arm all-sides H14\|16 / Oct. Never soft-veto nearATR. Do not stress-test by changing SL/TP / ATR max 2380.

---

## 3. P6-T03 — ATR max / G3 declaration

| Preset | ATR regime | Max pts | G3 |
| --- | ---: | ---: | --- |
| `…P0_balanced_chart.set` (Presets) | true | **2380** | OK |
| `…P4_research_OS_W50.set` (Presets + Profiles) | true | **2380** | OK |

Filters apply **before** `AOSAllowEntry` — OS cannot lift ATR max.  
Declaration: `regime_filtered=true` · Frankfurt/London 08–17 · skip Tue · ATR max **2380**.

---

## 4. Sign-off

P6 complete. Research OS stack stays:

```text
Engine Balanced P0 M5 (26101903 geometry · ATR≤2380)
+ L2det_de40_m5_v1b LIVE_WITHHOLD (research magic 26151904)
+ L3/L4/W50/ledger
+ L9 H13 / spread SHADOW only (not wired LIVE)
+ L2 AI DISARM (L2skip_de40_m5)
```

Next: **P7 DONE** · HITL · **`DE40_5m_stack`** · magic **26151907**.
