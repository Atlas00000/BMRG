# JP225 / JPN225 M5 — L6 decision ledger (P4)

**Version:** 1.0.0  
**Tasks:** JP225-M5-AOS-P4-T01 … T04  
**Date:** 2026-10-20  
**Evidence:** `blotter/archive/JP225-M5-AOS-P4/` · `tapes/jp225_m5_tip_ledger_v1c_shadow.csv`  
**EA wire:** `Include/AOS_L2det_jp_m5.mqh` · research `.set` arms L2det LIVE_WITHHOLD + L3/L4/ledger  

**Mode:** Offline ledger **SIGNED** · Tester research OS ready · **not** HITL live · L2AI **DISARM**

---

## 1. Schema

Same EA-compatible columns as M15 [`aos_l6_ledger.md`](./aos_l6_ledger.md) §1, plus:

| Col | M5 note |
| --- | --- |
| `event_id` | `26161904-JPN225-M5-{side}-{stamp}` |
| `l2det_reason` | `L2DET_SKIP_BUY_MATCH` · `L2DET_SKIP_BUY_H09_13_16` · optional `L2DET_SKIP_MATCH` |
| `model` | `none` or `L2skip_jp225_m5_DISARM` |
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

**L3 unlatch (P3):** after `HALT_f0_BELOW_FRONTIER`, clear when **W20 E_N > 0 for 2 consecutive** health evals and dd_peak &lt; 20%. Health path = L2det-passed fires. Forever-latch diagnostic retained; on tip v1c there is **no BELOW trip** so latch modes match.

---

## 3. Offline writer

```text
python blotter/archive/JP225-M5-AOS-P4/run_p4_ledger_stack.py
```

| File | Stack |
| --- | --- |
| `ledger_det_v1c.csv` | L1+L2det v1c+L3+L4+L6 (+L8 advise) · **unlatch ON** |
| `ledger_det_v1c_match_all.csv` | + MATCH all-sides HOLD |
| `ledger_det_v1c_plus_ai_shadow.csv` | + L2AI DISARM overlay |
| `ledger_det_v1c_forever_latch.csv` | Diagnostic |
| `tapes/jp225_m5_tip_ledger_v1c_shadow.csv` | Canonical copy |

### Tip scorecard (P4_STACK.json · Leak prior 3.3 pp)

| Stack | n_fire | E_N | EF_prior | L2 skips | L3 halt | L8 advise |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| **det_v1c** | **69** | **+0.478R** | **+12.64 pp** | 25 (prec 80%) | **0** | 21 (21/21 losers) |
| v1c + MATCH all | 51 | +0.647R | +18.3 pp | 43 | 0 | 21 |
| v1c + AI shadow | 69 | +0.478R | +12.64 pp | 25 + 3 AI | 0 | 21 |
| forever latch | 69 | +0.478R | +12.64 pp | — | 0 | — |

Preferred: **det_v1c** (unlatch). ΔE_N vs tip baseline **+0.234R**. MATCH-all **HOLD** (SELL FP from P2). AI **DISARM**. Forever-latch = v1c on tip (no BELOW).

---

## 4. Research OS preset

Copies:

- `Presets/BMRG-M5-JP225-6M-P4_research_OS_W50.set`
- `Profiles/Tester/BMRG/JP225/BMRG-M5-JP225-6M-P4_research_OS_W50.set`
- `blotter/archive/JP225-M5-AOS-P4/BMRG-M5-JP225-6M-P4_research_OS_W50.set`

| Input | Value |
| --- | --- |
| Magic | **26161904** |
| `InpAOS_Enable` | true |
| `InpAiOsMode` | **LIVE_WITHHOLD (2)** |
| `InpAiKillSwitch` | **false** |
| `InpAOS_JP_M5_L2detEnable` | **true** |
| `InpAOS_JP_M5_SkipBuyMatch` | true |
| `InpAOS_JP_M5_SkipBuyH09_13_16` | true |
| `InpAOS_JP_M5_SkipMatchAll` | false |
| `InpAOS_JP_L2detEnable` | **false** (M15 May∨Jul off) |
| `InpAOS_W250` | **50** |
| `InpAOS_Leak` | **3.3** |
| `InpAOS_BWR` / `R` | **33.3** / **2.00** |
| `InpAOS_Ledger` | true |
| L2AI | OFF |

---

## 5. L8 (secondary)

Advise-only on tip: **21/21** on losers · **0** winners. Cash-sleeve MAE abort stays shadow until overnight share known.

---

## 6. Status

**SIGNED** — proceed P5 retrain/rollback · then P6/P7 HITL (`JPN225_5m_stack` · **26161907**).
