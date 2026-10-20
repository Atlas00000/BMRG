# AAPL M5 — P6 hardening (L9 · L2 stress · ATR/BBw G3)

**Version:** 1.0.0  
**Tasks:** AAPL-M5-AOS-P6-T01 … T03  
**Date:** 2026-10-20  
**Evidence:** `blotter/archive/AAPL-M5-AOS-P6/P6_HARDEN.json`  
**Upstream:** [`aos_l2_policy_M5.md`](./aos_l2_policy_M5.md) v1b · P4/P5 wire  

**Mode:** Policy + offline CF. No geometry change. L2 AI still DISARM.  
**L9 focus:** RTH edge / spread / overnight — **protect May / Mon / tip BUY**.  
**Sibling:** M15 Harvest OS — **do not merge** ATR (24–98 vs M15) or L2det maps (Jul∨Wed ≠ Thu/18).

---

## 0. Verdict

| Task | Verdict |
| --- | --- |
| P6-T01 L9 session soft veto | **PASS** — no new LIVE veto · H14/overnight **DISARM** · H18/H19 **HOLD_SHADOW** · spread≥30 **no L9 LIVE** |
| P6-T02 ±10% L2det bound stress | **PASS** — keep **Jul ∨ Wed**; widen Jul∨Wed∨H18/spread/Jun → FREQUENCY_STALL; protect probes confirm |
| P6-T03 ATR/BBw G3 | **PASS** — **24–98** / **0.30–2.00%** on P0 + P4 |
| Phase | **P6_COMPLETE** |

---

## 1. P6-T01 — L9 session quality

Tip spread median **≈29** · nuniq **4** · std **≈0.8** → tercile saturated.

### On full tip

| Policy | Tip verdict | ΔE_N | Prec | Ret% | May FP | Mon FP |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| skip H14 | **DISARM** | −0.053 | 0.00 | 96.1 | 1 | 0 |
| skip H18 | HOLD_SHADOW | +0.060 | 0.62 | 79.2 | 2 | 1 |
| skip H19 | HOLD_SHADOW | +0.036 | 0.57 | 72.7 | 3 | 1 |
| skip RTH edge H14/18/19 | REJECT_FREQUENCY_STALL | +0.047 | 0.55 | **48.1** | 6 | 2 |
| skip overnight held | REJECT_FREQUENCY_STALL | −0.575 | 0.35 | **44.2** | 7 | 8 |
| skip spread > p66 / ≥30 | ARM_SOFT (CF) | +0.080 | 0.61 | 70.1 | 1 | 0 |

### Additive on **v1b-kept** path

| Policy | Verdict | ΔE_N | Ret% | Note |
| --- | --- | ---: | ---: | --- |
| add H14 | **DISARM** | −0.054 | 95.5 | early RTH collateral |
| add H18 | HOLD_SHADOW | +0.106 | 77.3 | May FP=2 — already L2det optional |
| add H19 | **DISARM** | −0.006 | 79.5 | no lift |
| add RTH edge | HOLD_SHADOW | +0.049 | 52.3 | thin · May FP |
| add overnight | REJECT_FREQUENCY_STALL | −0.643 | 31.8 | leave to **L8** |
| add spread ≥30 | ARM_SOFT (CF) | +0.120 | 72.7 | **no L9 LIVE** — L2det optional OFF |

### Wire stance (P6)

| ID | Stance |
| --- | --- |
| `L9_skip_spread_tercile` | **DISARM** (saturated) |
| `L9_skip_spread_ge_30` | **NO L9 LIVE** — CF ARM_SOFT duplicates L2det `SkipHighSpread` (keep **false**) |
| `L9_skip_H14` | **DISARM** |
| `L9_skip_H18` / H19 | **HOLD_SHADOW** — H18 already optional on L2det; do not double-wire L9 LIVE |
| `L9_skip_rth_edge` | **DISARM** (FREQUENCY_STALL) |
| `L9_skip_overnight` | **DISARM** — L8 MAE/gap path owns overnight |

Overlay `L2det_aapl_m5_v1b` remains the research L2 path. L9 is additive soft layer, not a replace.

---

## 2. P6-T02 — L2 bound stress (Jul / Wed · not May/Mon/BUY)

Baseline tip v1b: kept E_N **+0.349R** · ret **57.1%** · May FP **1** · Mon FP **0**.

| Stress | kept E_N | Δ vs v1b | Ret% | Read |
| --- | ---: | ---: | ---: | --- |
| **v1b Jul ∨ Wed** | **0.349** | **0** | **57.1** | **keep** |
| Jul only | 0.317 | −0.033 | 80.5 | Wed leg earns its keep |
| Wed only | 0.237 | −0.113 | 67.5 | Jul leg earns its keep (fail band OK) |
| Jul ∨ Wed ∨ H18 | 0.455 | +0.106 | **44.2** | FREQUENCY_STALL — do not widen |
| Jul ∨ Wed ∨ spread≥30 | 0.469 | +0.120 | **41.6** | FREQUENCY_STALL |
| Jul ∨ Wed ∨ Jun | 0.374 | +0.025 | **46.8** | FREQUENCY_STALL |
| Jul ∨ Wed ∨ Aug | 0.274 | −0.075 | 42.9 | FREQUENCY_STALL + Mon FP |
| Jul ∨ H18 (no Wed) | 0.414 | +0.064 | 63.6 | HOLD — May FP=2 |
| Wed ∨ H18 (no Jul) | 0.299 | −0.051 | 51.9 | HOLD — May FP |
| **REJECT May** | **0.066** | **−0.284** | 84.4 | **protect confirmed** |
| **REJECT Mon** | **0.054** | **−0.295** | 79.2 | **protect confirmed** |
| **REJECT BUY** | **−0.024** | **−0.373** | 49.4 | **protect confirmed** |
| **REJECT nearATR** | **0.152** | **−0.197** | 94.8 | tip star confirmed |

**Read:** Keep EA defaults **Jul ∨ Wed**. Do not stack H18 / spread / Jun into LIVE. Never soft-veto May / Mon / BUY / nearATR. Do not stress-test by changing SL190/TP280 or ATR 24–98.

---

## 3. P6-T03 — ATR / BBw G3 declaration

| Preset | ATR | BBw % | G3 |
| --- | ---: | ---: | --- |
| `Presets/AAPL/…Balanced_TPgtSL.set` | **24–98** | **0.30–2.00** | OK |
| `Presets/…P4_research_OS_W50.set` | **24–98** | **0.30–2.00** | OK |
| archive P4 copy | **24–98** | **0.30–2.00** | OK |

Filters apply **before** `AOSAllowEntry` — OS cannot lift ATR/BBw.  
Declaration: `regime_filtered=true` · ATR **24–98** · BBw **0.30–2.00%** · MaxSpread **40**.

---

## 4. Sign-off

P6 complete. Research OS stack stays:

```text
engine 26102011 + L2det_aapl_m5_v1b (Jul∨Wed) + L3/L4 + L6 ledger + L8 shadow
L2 AI DISARM · L9 no LIVE · magic research 26162014 · target arm 26162017 (P7)
```

Next: **P7 DONE** · HITL · **`AAPL_5m_stack`** · magic **26162017**.
