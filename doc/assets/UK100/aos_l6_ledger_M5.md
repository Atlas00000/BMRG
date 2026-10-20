# UK100 M5 — L6 decision ledger (P4)

**Version:** 1.0.0  
**Tasks:** UK100-M5-AOS-P4-T01 … T04  
**Date:** 2026-10-20  
**Evidence:** `blotter/archive/UK100-M5-AOS-P4/` · `tapes/uk100_m5_tip_ledger_v1b_shadow.csv`  
**EA wire:** `Include/AOS_L2det_uk_m5.mqh` · BMRG **v1.24** · research `.set` arms L2det LIVE_WITHHOLD + L3/L4/ledger  

**Mode:** Offline ledger **SIGNED** · Tester research OS ready · **not** HITL live · L2AI **DISARM**

---

## 1. Schema

Same EA-compatible columns as M15 [`aos_l6_ledger.md`](./aos_l6_ledger.md) §1, plus:

| Col | M5 note |
| --- | --- |
| `event_id` | `26121904-UK100-M5-{side}-{stamp}` |
| `l2det_reason` | `L2DET_SKIP_MON_AND_H12` · `L2DET_SKIP_SELL_AND_H12` · optional `L2DET_SKIP_AUG` |
| `model` | `none` or `L2skip_uk_m5_DISARM` |
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

---

## 3. Offline writer

```text
python blotter/archive/UK100-M5-AOS-P4/run_p4_ledger_stack.py
```

| File | Stack |
| --- | --- |
| `ledger_det_v1b.csv` | L1+L2det v1b+L3+L4+L6 (+L8 advise) |
| `ledger_det_v1b_aug.csv` | + Aug SOFT (HOLD calendar) |
| `ledger_det_v1b_plus_ai_shadow.csv` | + L2AI DISARM overlay |
| `tapes/uk100_m5_tip_ledger_v1b_shadow.csv` | Canonical copy |

### Tip scorecard (P4_STACK.json)

| Stack | n_fire | E_N | EF_proxy | L2 skips | L3 halt | L8 advise |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| **det_v1b** | **83** | **+0.383R** | **+11.08 pp** | 33 (prec 70%) | **0** | 23 (23/23 losers) |
| det_v1b + Aug | 54 | +0.500R | +16.3 pp | 62 | 0 | 23 |
| v1b + AI shadow | 83 | +0.383R | +11.08 pp | 33 + 2 AI shadow | 0 | 23 |

Preferred: **det_v1b**. Aug additive HOLD (calendar). AI DISARM (shadow skips do not change permit).

---

## 4. Research OS preset

Copies:

- `Presets/BMRG-M5-UK100-6M-P4_research_OS_W50.set`
- `Profiles/Tester/BMRG/BMRG-M5-UK100-6M-P4_research_OS_W50.set`
- `Profiles/Tester/BMRG/UK100/BMRG-M5-UK100-6M-P4_research_OS_W50.set`

| Input | Value |
| --- | --- |
| Magic | **26121904** |
| `InpAOS_Enable` | true |
| `InpAiOsMode` | **LIVE_WITHHOLD (2)** |
| `InpAiKillSwitch` | **false** |
| `InpAOS_UK_M5_L2detEnable` | **true** |
| `InpAOS_UK_M5_SkipMonAndH12` | true |
| `InpAOS_UK_M5_SkipSellAndH12` | true |
| `InpAOS_UK_M5_SkipAug` | false |
| `InpAOS_UK_L2detEnable` | **false** (M15 map off) |
| `InpAOS_L3_Enable` / L4 / Ledger | true |
| `InpAOS_W250` | **50** |
| `InpAOS_Leak` | **5.93** |
| Geometry / session / ATR max 869 | same as Balanced P0 M5 |

**Compile** `BMRG.mq5` (v1.24+) before Tester. Ledger → `COMMON\Files\BMRG_AOS_ledger_26121904.csv`.

---

## 5. L8 MAE abort advisor (P4-T04)

No tick MAE on tip tape. Shadow rules (advise-only):

| Code | Fingerprint |
| --- | --- |
| `L8_ADVISE_ABORT_FAST_SL` | loss · hold &lt; 1h · near_atr_cap |
| `L8_ADVISE_ABORT_FLASH_SL` | loss · hold &lt; 0.25h |

Tip v1b path: **23** advises · **23/23 losers** · **0 winners** — strong fingerprint; still advise-only (not LIVE abort).

---

## 6. Sign-off

| Item | Verdict |
| --- | --- |
| P4-T01 ledger schema + writer | **DONE** |
| P4-T02 det stack shadow | **DONE** · E_N +0.383R · trip-free |
| P4-T03 AI shadow | **DONE** · DISARM (2 shadow skips) |
| P4-T04 L8 advise | **DONE** · 23/23 loser precision |
| EA wire + research `.set` | **DONE** · Tester pending user run |
| HITL / P7 | **NOT** yet |

**Next:** P5 retrain/rollback store · then P6 harden · P7 HITL (magic **26121907**).
