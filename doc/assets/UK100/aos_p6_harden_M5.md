# UK100 M5 — P6 hardening (L9 · L2 stress · ATR G3)

**Version:** 1.0.0  
**Tasks:** UK100-M5-AOS-P6-T01 … T03  
**Date:** 2026-10-20  
**Evidence:** `blotter/archive/UK100-M5-AOS-P6/P6_HARDEN.json`  
**Upstream:** [`aos_l2_policy_M5.md`](./aos_l2_policy_M5.md) v1b · P4 wire  

**Mode:** Policy + offline CF. No geometry change. L2 AI still DISARM.  
**L9 focus:** midday / late / spread — **not** morning (H08–11 protected).

---

## 0. Verdict

| Task | Verdict |
| --- | --- |
| P6-T01 L9 session soft veto | **PASS** — morning DISARM; `H14+` + spread p66 **ARM_SOFT** (shadow) |
| P6-T02 ±10% / hour-bound L2 stress | **PASS** — keep **H12–13** nominal; do not widen/narrow |
| P6-T03 ATR max G3 | **PASS** — **869** declared on P0 + P4 research OS |
| Phase | **P6_COMPLETE** |

---

## 1. P6-T01 — L9 session quality

Tip spread median **120** · p66 still has skips (unlike flat M15 tip) → spread veto has signal.

### On full tip

| Policy | Tip verdict | ΔE_N | Prec | Ret% | H08–11 FP |
| --- | --- | ---: | ---: | ---: | ---: |
| **skip H14+** | **ARM_SOFT** | +0.03 | 0.56 | 84.5 | 0 |
| skip H12–13 BUY | HOLD_SHADOW | +0.01 | 0.50 | 82.8 | 0 |
| skip H12–13 all | HOLD_SHADOW | +0.19 | 0.60 | 59.5 | 0 |
| **skip morning H08–11** | **DISARM** | **−0.25** | 0.33 | 56.0 | **34** |
| **skip spread > p66** | **ARM_SOFT** | +0.03 | 0.62 | 93.1 | 0 |
| skip Mon all | HOLD_SHADOW | +0.08 | 0.56 | 72.4 | 10 |

### Additive on **v1b-kept** path

| Policy | Verdict | ΔE_N | Ret% |
| --- | --- | ---: | ---: |
| **add H14+** | **ARM_SOFT** | **+0.11** | 78.3 |
| **add spread > p66** | **ARM_SOFT** | +0.06 | 90.4 |
| add H12–13 BUY | DISARM | −0.01 | 83.1 |
| add SELL∧near_atr | HOLD_SHADOW | +0.00 | 94.0 |

### Wire stance (P6)

| ID | Stance |
| --- | --- |
| `L9_skip_morning_H08_11` | **DISARM** (protect — confirmed) |
| `L9_skip_H14_plus` | **ARM_SOFT / SHADOW** — optional ledger; **not** LIVE until P7 HITL |
| `L9_skip_spread_p66` | **ARM_SOFT / SHADOW** — revisit if fills flatten |
| `L9_skip_H12_13_BUY` | **DISARM** on v1b path (no additive lift) |
| Full H12–13 all-sides | Already partially covered by L2det v1b — do not double-wire as L9 |

L2det v1b remains the live research overlay. L9 is additive soft layer.

---

## 2. P6-T02 — L2 bound stress (hour window · nearATR ±10%)

Baseline tip v1b (H12–13): kept E_N **+0.383R** · ret **71.6%**.

| Stress | kept E_N | Δ vs v1b | Ret% |
| --- | ---: | ---: | ---: |
| **H12–13 nominal** | **0.383** | **0** | **71.6** |
| H12 only | 0.217 | **−0.17** | 84.5 |
| H13 only | 0.314 | −0.07 | 87.1 |
| H11–14 wide | 0.370 | −0.01 | 59.5 |
| v1b ∨ SELL∧near @0.81 | 0.382 | ≈0 | 60.3 |
| v1b ∨ SELL∧near @0.99 | 0.383 | 0 | 71.6 |
| atr_cap ±10% on SELL∧near | ≈0.382–0.383 | ≈0 | 60–72 |

**Read:** Narrowing to H12-only **hurts**. Widening to H11–14 stalls frequency without E_N gain. nearATR ±10% additive is noise. Keep EA defaults **(Mon∧H12–13)∨(SELL∧H12–13)**. Do not stress-test by changing SL/TP / ATR max 869.

---

## 3. P6-T03 — ATR max / G3 declaration

| Preset | ATR regime | Max pts | G3 |
| --- | ---: | ---: | --- |
| `…P0_balanced_chart.set` (Presets + Profiles) | true | **869** | OK |
| `…P4_research_OS_W50.set` | true | **869** | OK |

Filters apply **before** `AOSAllowEntry` — OS cannot lift ATR max.  
Declaration: `regime_filtered=true` · London 08–17 · skip Tue · ATR max **869**.

---

## 4. Sign-off

P6 complete. Research OS stack stays:

```text
Engine Balanced P0 M5 (26101905 geometry)
+ L2det_uk_m5_v1b LIVE_WITHHOLD (research magic 26121904)
+ L3/L4/W50/ledger
+ L9 H14+ / spread_p66 SHADOW only (not wired LIVE)
+ L2 AI DISARM
```

Next: **P7** promotion packet / HITL (magic **26121907**).
