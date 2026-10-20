# DE40 M5 — L6 decision ledger (P4)

**Version:** 1.0.0  
**Tasks:** DE40-M5-AOS-P4-T01 … T04  
**Date:** 2026-10-20  
**Evidence:** `blotter/archive/DE40-M5-AOS-P4/` · `tapes/de40_m5_tip_ledger_v1b_shadow.csv`  
**EA wire:** `Include/AOS_L2det_de_m5.mqh` · research `.set` arms L2det LIVE_WITHHOLD + L3/L4/ledger  

**Mode:** Offline ledger **SIGNED** · Tester research OS ready · **not** HITL live · L2AI **DISARM**

---

## 1. Schema

Same EA-compatible columns as M15 [`aos_l6_ledger.md`](./aos_l6_ledger.md) §1, plus:

| Col | M5 note |
| --- | --- |
| `event_id` | `26151904-DE30-M5-{side}-{stamp}` |
| `l2det_reason` | `L2DET_SKIP_BUY_H14_16` · `L2DET_SKIP_BUY_OCT` · optional `L2DET_SKIP_OCT` |
| `model` | `none` or `L2skip_de40_m5_DISARM` |
| `w250_EN` | Prefers W50 when n allows (dense TF) |

---

## 2. Decision precedence (shadow)

```
L3 HALT        → final_permit = 0
L2det WOULD_SKIP → final_permit = 0
L2AI WOULD_SKIP_SHADOW → final_permit = 1  (DISARM — log only)
L8 advise      → append reason; does not change permit
else FIRE_OK   → final_permit = 1
```

**L3 unlatch (P3):** after `HALT_f0_BELOW_FRONTIER`, clear when **W20 E_N > 0 for 2 consecutive** health evals and dd_peak &lt; 20%. Health path = L2det-passed fires (continues while halted). Forever-latch diagnostic is **REJECT** for research OS scoring.

---

## 3. Offline writer

```text
python blotter/archive/DE40-M5-AOS-P4/run_p4_ledger_stack.py
```

| File | Stack |
| --- | --- |
| `ledger_det_v1b.csv` | L1+L2det v1b+L3+L4+L6 (+L8 advise) · **unlatch ON** |
| `ledger_det_v1b_oct_all.csv` | + Oct all-sides HOLD |
| `ledger_det_v1b_plus_ai_shadow.csv` | + L2AI DISARM overlay |
| `ledger_det_v1b_forever_latch.csv` | Diagnostic — do not arm |
| `tapes/de40_m5_tip_ledger_v1b_shadow.csv` | Canonical copy |

### Tip scorecard (P4_STACK.json · Leak prior 7.0 pp)

| Stack | n_fire | E_N | EF_prior | L2 skips | L3 halt | L8 advise |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| **det_v1b** | **104** | **+0.298R** | **+6.25 pp** | 13 (prec 77%) | **6** | 14 (14/14 losers) |
| v1b + Oct all | 102 | +0.302R | +6.40 pp | 15 | 6 | 14 |
| v1b + AI shadow | 104 | +0.298R | +6.25 pp | 13 + 27 AI | 6 | 14 |
| forever latch | 36 | +0.06R | **−4.2 pp** | — | 85 | — |

Preferred: **det_v1b** (unlatch). ΔE_N vs tip baseline **+0.091R**. Oct-all HOLD (SELL FP). AI DISARM. Forever-latch **REJECT** for OS compare.

---

## 4. Research OS preset

Copies:

- `Presets/BMRG-M5-DE40-6M-P4_research_OS_W50.set`
- `Profiles/Tester/BMRG/DE40/BMRG-M5-DE40-6M-P4_research_OS_W50.set`
- `blotter/archive/DE40-M5-AOS-P4/BMRG-M5-DE40-6M-P4_research_OS_W50.set`

| Input | Value |
| --- | --- |
| Magic | **26151904** |
| `InpAOS_Enable` | true |
| `InpAiOsMode` | **LIVE_WITHHOLD (2)** |
| `InpAiKillSwitch` | **false** |
| `InpAOS_DE_M5_L2detEnable` | **true** |
| `InpAOS_DE_M5_SkipBuyH14_16` | true |
| `InpAOS_DE_M5_SkipBuyOct` | true |
| `InpAOS_DE_M5_SkipH14_16All` / `SkipOctAll` | false |
| `InpAOS_DE_L2detEnable` | **false** (M15 map off) |
| `InpAOS_W250` | **50** |
| `InpAOS_Leak` | **7.0** |
| `InpAOS_Ledger` | true |
| L2AI | OFF |

---

## 5. L8 (secondary)

Advise-only on tip: **14/14** on losers · **0** winners. Cash-sleeve MAE abort stays shadow until overnight share known.

---

## 6. Status

**SIGNED** — proceed P5 retrain/rollback · then P6/P7 HITL (`DE40M5stack` · **26151907**).
