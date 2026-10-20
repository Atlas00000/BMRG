# USDJPY — P6 hardening (L9 · L2 stress · ATR G3)

**Version:** 1.0.0  
**Tasks:** USDJPY-AOS-P6-T01 … T03  
**Date:** 2026-10-19  
**Evidence:** `blotter/archive/USDJPY-AOS-P6/P6_HARDEN.json`  
**Upstream:** [`aos_l2_policy.md`](./aos_l2_policy.md) v1c · research OS P4  

**Mode:** Policy + offline CF. No geometry change. L2 AI still DISARM. L2det MQH still absent.

---

## 0. Verdict

| Task | Verdict |
| --- | --- |
| P6-T01 L9 session soft veto | **PASS** — no new LIVE veto · H14 DISARM · H16 already in v1c · spread HOLD (low variance) · Jul HOLD |
| P6-T02 ±10% L2det stress | **PASS_WITH_NOTES** — do not loosen nearATR; keep 0.9 / 70 + H16 |
| P6-T03 ATR max G3 | **PASS** — 70 declared on P0 + P4 research OS |
| Phase | **P6_COMPLETE** |

---

## 1. P6-T01 — L9 session quality

Session sleeve (12–20 · skip Tue). Tip spread nunique=**3** · std≈0.7 · p66=5 · median≈4 — **low variance**; tercile cut is fragile.

| Policy | Tip verdict | ΔE_N | Prec | Ret% | BUY/Fri FP | n |
| --- | --- | ---: | ---: | ---: | --- | ---: |
| skip H14 | **DISARM** | 0.0 | 0.50 | 82.6 | **3** / 1 | 8 |
| skip H16 | **ARM_SOFT** | +0.077 | 1.00 | 93.5 | 0 / 0 | 3 |
| spread > tip p66 | ARM_SOFT* | +0.055 | 0.67 | 87.0 | 1 / 0 | 6 |
| spread > 12.5 (½ MaxSpread) | NO_SKIPS | — | — | 100 | — | 0 |
| skip Jul | HOLD_SHADOW | +0.206 | 0.71 | 69.6 | 2 / 1 | 14 |

\*Tip CF ARM_SOFT but **nunique=3** — wire as **HOLD_SHADOW / not LIVE** (not G5-robust).

Additive on **v1c-kept**: H14 / spread / Jul → HOLD_SHADOW only.

### Wire stance (P6)

| ID | Stance |
| --- | --- |
| `L9_skip_H14` | **DISARM** (flat ΔE_N · BUY FP 3) |
| `L9_skip_H16` | **already inside v1c** — do not double-count as L9 |
| `L9_skip_spread_tercile` | **HOLD_SHADOW** — tip ARM fragile (low variance) · not LIVE |
| `L9_skip_Jul` | **HOLD_SHADOW** — already P2 HOLD; not stacked LIVE |

Overlay `L2det_usdjpy_v1c` remains the research L2 path. L9 is additive soft layer, not a replace.

---

## 2. P6-T02 — ±10% L2det threshold stress

Baseline tip v1c (nearATR frac=0.9 · cap=70 **OR** H16): kept E_N **+0.368R** · ret **80.4%**.

| Stress | frac / cap | kept E_N | Δ vs v1c | Ret% |
| --- | --- | ---: | ---: | ---: |
| near_frac −10% | 0.81 / 70 | 0.419 | **+0.052** | 67.4 |
| near_frac +10% | 0.99 / 70 | 0.234 | **−0.134** | 89.1 |
| atr_cap −10% | 0.90 / 63 | 0.419 | +0.052 | 67.4 |
| atr_cap +10% | 0.90 / 77 | 0.234 | **−0.134** | 89.1 |
| both loose / tight | — | 0.406 | +0.038 | 78.3 |
| near_only (no H16) | 0.90 / 70 | 0.297 | **−0.070** | 84.8 |

**Read:** Loosening nearATR (**+10%**) hurts tip E_N hard. Dropping H16 (near-only) also loses vs v1c (−0.07R) — matches P3 BELOW story. Keep defaults **frac=0.9 · nearATR ref=70 · OR H16**. Do not stress-test by changing SL/TP. Engine ATR max (70) stays separate G3.

---

## 3. P6-T03 — ATR max / G3 declaration

| Preset | ATR regime | Max pts | G3 |
| --- | ---: | ---: | --- |
| `…P0_balanced_chart.set` (Presets + Profiles/Tester/BMRG/USDJPY/) | true | **70** | OK |
| `…P4_research_OS_W50.set` (same) | true | **70** | OK |

Filters apply **before** AOS entry — OS cannot lift ATR max.  
Declaration: `regime_filtered=true` · session 12–20 · skip Tue · ATR max **70**. Do **not** reopen Tokyo.

---

## 4. Sign-off

P6 complete. Research stack stays:

```text
Engine Balanced P0 (26101828) AOS OFF chart
+ L2det v1c (near_atr∨H16) SHADOW offline (no MQH)
+ P4 research .set (26131804): L3/L4/W50/ledger · AiOsMode OFF
+ L9 H14/spread/Jul SHADOW only (not wired LIVE)
+ L2 AI DISARM
```

Next: **P7** promotion packet / HITL (target magic **26131807**). Measured Leak still OPEN.
