# UK100 — L6 decision ledger (P4)

**Version:** 1.0.0  
**Tasks:** UK100-AOS-P4-T01 … T04  
**Date:** 2026-10-12  
**Evidence:** `blotter/archive/UK100-AOS-P4/` · `tapes/uk100_tip_ledger_v1b_shadow.csv`  
**EA parity:** `Include/AOS.mqh` → `AOSLedger` / `AOSInit` header  

**Mode:** MQL wire **v1.23** — `Include/AOS_L2det_uk.mqh` · research `.set` arms L2det LIVE_WITHHOLD + L3/L4/ledger.

---

## 1. Schema

### EA-compatible columns (COMMON Files CSV)

| Col | Type | Meaning |
| --- | --- | --- |
| `t` | datetime | Decision time (open) |
| `side` | BUY/SELL | Engine side |
| `layer` | enum | `ENGINE` · `L2DET` · `L2AI` · `L3` · `L4` · `L8` |
| `decision` | enum | `FIRE_OK` · `WOULD_SKIP` · `WOULD_SKIP_SHADOW` · `HALT` · `SIZE_MOD` |
| `reason` | string | Pipe-joined codes |
| `life` | enum | WARMUP / EXPANDING / STABLE / COMPRESSING / NEAR / BELOW |
| `f_rec` | float | Recommended size factor |
| `w250_EF` | float | Rolling EF_proxy pp (wired window = W50 research) |
| `w250_EN` | float | Rolling E_N |
| `ai_proba` | float | p_lose (L2AI; empty if none) |
| `ai_skip` | 0/1 | Model would-skip |
| `model` | string | Pin / `none` / `L2skip_uk_DISARM` |
| `halt` | 0/1 | L3 halt latched |
| `derisk` | 0/1 | L3 derisk active |
| `mode` | string | `SHADOW` / `LIVE` |

### UK100 extensions (offline / promotion packets)

| Col | Meaning |
| --- | --- |
| `event_id` | Stable fire id |
| `open_time` | Full open stamp |
| `exit_reason` | TP/SL/… (post-hoc for CF) |
| `win` / `pnl_R` | Outcome (CF only) |
| `l2det_skip` / `l2det_reason` | Deterministic L2 |
| `l8_advise` | MAE abort advisor |
| `final_permit` | 1 = trade counted in CF book |
| `stack` | Stack label |

---

## 2. Decision precedence (shadow)

```
L3 HALT        → final_permit = 0
L2det WOULD_SKIP → final_permit = 0
L2AI WOULD_SKIP_SHADOW → final_permit = 1  (DISARM — log only)
L8 advise      → append reason; does not change permit
else FIRE_OK   → final_permit = 1
```

L4 updates `life` / `f_rec` on the permitted path; does not invent skips.

---

## 3. Offline writer

```text
python blotter/archive/UK100-AOS-P4/run_p4_ledger_stack.py
```

Outputs:

| File | Stack |
| --- | --- |
| `ledger_det_v1b.csv` | L1+L2det v1b+L3+L4+L6 (+L8 advise) |
| `ledger_det_v1b_jul.csv` | + Jul SOFT |
| `ledger_det_v1b_plus_ai_shadow.csv` | + L2AI DISARM overlay |
| `tapes/uk100_tip_ledger_v1b_shadow.csv` | Canonical copy for docs |

---

## 4. Research OS preset

Copies:

- `Profiles/Tester/BMRG/BMRG-M15-UK100-6M-P4_research_OS_W50.set`
- `Profiles/Tester/BMRG/UK100/BMRG-M15-UK100-6M-P4_research_OS_W50.set`

| Input | Value |
| --- | --- |
| Magic | **26111304** |
| `InpAOS_Enable` | true |
| `InpAiOsMode` | **LIVE_WITHHOLD (2)** — L2det blocks in Tester |
| `InpAiKillSwitch` | **false** |
| `InpAOS_UK_L2detEnable` | **true** (Thu ∨ BUY∧nearATR) |
| `InpAOS_UK_SkipJul` | false |
| `InpAOS_L3_Enable` / L4 / Ledger | true |
| `InpAOS_W250` | **50** |
| `InpAOS_Leak` | **4.27** |
| Geometry / session / ATR max | same as Balanced P0 |

**Compile** `BMRG.mq5` (v1.23+) before Tester. Ledger → `COMMON\Files\BMRG_AOS_ledger_26111304.csv`.

---

## 5. L8 MAE abort advisor (P4-T04)

No tick MAE on tip tape. Shadow rules (advise-only):

| Code | Fingerprint |
| --- | --- |
| `L8_ADVISE_ABORT_FAST_SL` | loss · hold &lt; 1h · near_atr_cap |
| `L8_ADVISE_ABORT_FLASH_SL` | loss · hold &lt; 0.25h |

Tip v1b: **5** advises · **5/5 losers** · **0 winners** — useful fingerprint, n too small to arm.

---

## 6. Sign-off

| Item | Verdict |
| --- | --- |
| Schema matches EA header | **PASS** |
| Offline writer | **PASS** |
| Det stack CF ledger | **PASS** (see REVIEW) |
| L2AI shadow on det fires | **PASS** (DISARM; 1 shadow skip) |
| L8 advise-only | **PASS** (secondary) |
| LIVE_WITHHOLD | **NOT ARMED** |
