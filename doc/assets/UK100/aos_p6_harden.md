# UK100 — P6 hardening (L9 · L2 stress · ATR G3)

**Version:** 1.0.0  
**Tasks:** UK100-AOS-P6-T01 … T03  
**Date:** 2026-10-12  
**Evidence:** `blotter/archive/UK100-AOS-P6/P6_HARDEN.json`  
**Upstream:** [`aos_l2_policy.md`](./aos_l2_policy.md) v1b · Tester wire P4  

**Mode:** Policy + offline CF. No geometry change. L2 AI still DISARM.

---

## 0. Verdict

| Task | Verdict |
| --- | --- |
| P6-T01 L9 session soft veto | **PASS** — spread DISARM; `BUY∧H08` **ARM_SOFT** candidate (shadow) |
| P6-T02 ±10% L2det stress | **PASS_WITH_NOTES** — do not loosen nearATR; nominal local best |
| P6-T03 ATR max G3 | **PASS** — 1470 declared on P0 + research OS |
| Phase | **P6_COMPLETE** |

---

## 1. P6-T01 — L9 session quality

Tip entry spread is **constant 120** → tercile soft veto has **no tip signal** → **DISARM**.

| Policy | Tip verdict | ΔE_N | Prec | Ret% | Wed FP |
| --- | --- | ---: | ---: | ---: | ---: |
| skip H08 (all sides) | ARM_SOFT | +0.14 | 0.69 | 74.5 | 1 |
| **skip BUY∧H08** | **ARM_SOFT** | **+0.19** | **0.82** | 78.4 | 1 |
| skip H08–09 London open | HOLD_SHADOW | +0.15 | 0.65 | 66.7 | 2 |
| skip hour≥14 | DISARM | −0.16 | 0.31 | 74.5 | 4 |
| spread > tip p66 | NO_SKIPS | — | — | 100 | 0 |

Additive on **v1b-kept** path:

| Policy | Verdict | ΔE_N |
| --- | --- | ---: |
| **BUY∧H08** | **ARM_SOFT** | +0.14 |
| H08 all | HOLD_SHADOW | +0.08 |
| H08–09 | HOLD_SHADOW | +0.07 |
| hour≥14 | DISARM | −0.05 |

### Wire stance (P6)

| ID | Stance |
| --- | --- |
| `L9_skip_spread_tercile` | **DISARM** (tip constant; revisit if fills vary) |
| `L9_skip_late_H14` | **DISARM** |
| `L9_skip_BUY_H08` | **ARM_SOFT / SHADOW** — optional ledger reason; **not** LIVE in EA until P7 HITL (Wed FP=1; P2 held) |
| `L9_skip_H08_all` | Prefer BUY∧H08 over all-sides |

L2det v1b remains the live research overlay. L9 is additive soft layer, not a replace.

---

## 2. P6-T02 — ±10% L2det threshold stress

Baseline tip v1b: kept E_N **+0.364R** · ret **64.7%**.

| Stress | frac / cap | kept E_N | Δ vs v1b | Ret% |
| --- | --- | ---: | ---: | ---: |
| near_frac −10% | 0.81 / 1470 | 0.417 | **+0.05** | 52.9 |
| near_frac +10% | 0.99 / 1470 | 0.243 | **−0.12** | 74.5 |
| atr_cap −10% | 0.90 / 1323 | 0.417 | +0.05 | 52.9 |
| atr_cap +10% | 0.90 / 1617 | 0.243 | −0.12 | 74.5 |
| both loose / tight | — | 0.364 | 0 | 64.7 |

**Read:** Loosening nearATR (**+10%**) hurts tip E_N. Tightening helps E_N but stalls frequency (~53% ret). Keep EA defaults **frac=0.9 · cap=1470**. Do not stress-test by changing SL/TP.

---

## 3. P6-T03 — ATR max / G3 declaration

| Preset | ATR regime | Max pts | G3 |
| --- | ---: | ---: | --- |
| `…P0_balanced_chart.set` | true | **1470** | OK |
| `…P4_research_OS_W50.set` (BMRG + UK100/) | true | **1470** | OK |

Filters apply **before** `AOSAllowEntry` — OS cannot lift ATR max.  
Declaration: `regime_filtered=true` · London 08–17 · skip Tue · ATR max **1470**.

---

## 4. Sign-off

P6 complete. Research OS stack stays:

```text
Engine Balanced P0
+ L2det_uk_v1b LIVE_WITHHOLD (research magic)
+ L3/L4/W50/ledger
+ L9 BUY∧H08 SHADOW only (not wired LIVE)
+ L2 AI DISARM
```

Next: **P7** promotion packet / HITL.
