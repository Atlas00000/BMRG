# AAPL M5 — L6 decision ledger (P4)

**Version:** 1.0.0  
**Tasks:** AAPL-M5-AOS-P4-T01 … T04  
**Date:** 2026-10-20  
**Evidence:** `blotter/archive/AAPL-M5-AOS-P4/` · `tapes/aapl_m5_tip_ledger_v1b_shadow.csv`  
**EA wire:** `Include/AOS_L2det_aapl_m5.mqh` · research `.set` arms L2det LIVE_WITHHOLD + L3/L4/ledger  

**Mode:** Offline ledger **SIGNED** · Tester research OS ready · **not** HITL live · L2AI **DISARM**

---

## 1. Schema

EA-compatible columns plus M5 fields:

| Col | M5 note |
| --- | --- |
| `event_id` | `26162014-Apple-M5-{side}-{stamp}` |
| `l2det_reason` | `L2DET_AAPL_M5_JUL` · `L2DET_AAPL_M5_WED` · optional H18/SPREAD/H1 |
| `model` | `none` or `L2skip_aapl_m5_DISARM` |
| `l8_advise` | `L8_ADVISE_OVERNIGHT_LOSS` · `L8_ADVISE_ABORT_FAST_SL` · `L8_HOLD` |
| `w250_EN` | Prefers W50 when n allows |

---

## 2. Decision precedence (shadow)

```
L3 HALT        → final_permit = 0
L2det WOULD_SKIP → final_permit = 0
L2AI WOULD_SKIP_SHADOW → final_permit = 1  (DISARM — log only)
L8 advise      → append reason; does not change permit
else FIRE_OK   → final_permit = 1
```

**L3 unlatch (P3):** after `HALT_f0_BELOW_FRONTIER`, clear when **W20 E_N > 0 for 2 consecutive** health evals and dd_peak &lt; 20%. Health path = L2det-passed fires (continues while halted). Forever-latch diagnostic is **REJECT** for research OS scoring when it diverges.

---

## 3. Offline writer

```text
python blotter/archive/AAPL-M5-AOS-P4/run_p4_ledger_stack.py
```

| File | Stack |
| --- | --- |
| `ledger_det_v1b.csv` | L1+L2det v1b+L3+L4+L6 (+L8 advise) · **unlatch ON** |
| `ledger_det_jul_only.csv` | Jul-only nest (0 L3 halt on tip) |
| `ledger_det_jul_h18_HOLD.csv` | Jul∨H18 HOLD (May FP risk) |
| `ledger_det_v1b_plus_ai_shadow.csv` | + L2AI DISARM overlay |
| `ledger_det_v1b_forever_latch.csv` | Diagnostic |
| `tapes/aapl_m5_tip_ledger_v1b_shadow.csv` | Canonical copy |

### Tip scorecard (P4_STACK.json · Leak profile 15.3 pp)

| Stack | n_fire | E_N | EF_profile | L2 skips | L3 halt | L8 advise |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| **det_v1b** | **41** | **+0.327R** | −2.1 pp | 33 (prec 64%) | **3** | **21** (21/21 losers) |
| jul_only | 62 | +0.317R | −2.5 pp | 15 (prec 80%) | **0** | 21 |
| jul∨H18 HOLD | 49 | **+0.414R** | **+1.4 pp** | 28 | 0 | 21 |
| v1b + AI shadow | 41 | +0.327R | −2.1 pp | 33 + 19 AI | 3 | 21 |

Preferred research arm: **det_v1b** (P2 ARM). ΔE_N vs tip baseline **+0.171R**.  
Jul∨H18 has best EF but remains **HOLD** (May FP from P2). Jul-only clears L3 — optional tighter nest. AI **DISARM**. EF still fragile under profile Leak until measured.

---

## 4. Research OS preset

Copies:

- `Presets/BMRG-M5-AAPL-6M-P4_research_OS_W50.set`
- `Profiles/Tester/BMRG/AAPL/BMRG-M5-AAPL-6M-P4_research_OS_W50.set`
- `blotter/archive/AAPL-M5-AOS-P4/BMRG-M5-AAPL-6M-P4_research_OS_W50.set`

| Input | Value |
| --- | --- |
| Magic | **26162014** |
| `InpAOS_Enable` | true |
| `InpAiOsMode` | **LIVE_WITHHOLD (2)** |
| `InpAiKillSwitch` | **false** |
| `InpAOS_AAPL_M5_L2detEnable` | **true** |
| `InpAOS_AAPL_M5_SkipJul` / `SkipWed` | true |
| `InpAOS_AAPL_M5_SkipHour18` / H1 / spread | false |
| `InpAOS_AAPL_L2detEnable` | **false** (M15 map off) |
| `InpAOS_W250` | **50** |
| `InpAOS_Leak` | **15.3** |
| `InpAOS_BWR` / `R` | 40.4 / 1.47 |
| `InpAOS_Ledger` | true |
| L2AI | OFF |

---

## 5. L8 (primary for equity CFD)

Advise-only on tip: **21/21** on losers · **0** winners.  
Reasons: overnight loss path + fast/flash SL. Does **not** change `final_permit` until armed post-HITL.

---

## 6. Status

**P4 ACCEPT** — P5 DONE (L2skip DISARM) · next **P6** · measured Leak still OPEN · not M15/FX replace.
