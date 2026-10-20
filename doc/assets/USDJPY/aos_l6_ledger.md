# USDJPY — L6 decision ledger (P4)

**Version:** 1.0.0  
**Tasks:** USDJPY-AOS-P4-T01 … T04  
**Date:** 2026-10-19  
**Evidence:** `blotter/archive/USDJPY-AOS-P4/` · `tapes/usdjpy_tip_ledger_v1c_shadow.csv`  
**EA parity:** `Include/AOS.mqh` → `AOSLedger` / header columns  

**Mode:** Offline stack complete. MQL L2det for USDJPY **not wired** (`AOS_L2det_usdjpy.mqh` absent) — **v1c** is CF/ledger-shadow only. Research `.set` arms L3/L4/ledger (W50).

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
| `w250_EF` | float | Rolling EF_prior pp (wired window = W50 research) |
| `w250_EN` | float | Rolling E_N |
| `ai_proba` | float | p_lose (L2AI; empty if none) |
| `ai_skip` | 0/1 | Model would-skip |
| `model` | string | Pin / `none` / `L2skip_usdjpy_SHADOW` |
| `halt` | 0/1 | L3 halt latched |
| `derisk` | 0/1 | L3 derisk active |
| `mode` | string | `SHADOW` / `LIVE` |

### USDJPY extensions (offline / promotion packets)

| Col | Meaning |
| --- | --- |
| `event_id` | Stable fire id (`26101828-USDJPY-…`) |
| `open_time` | Full open stamp |
| `exit_reason` | TP/SL/… (post-hoc for CF) |
| `win` / `pnl_R` / `hold_h` / `nights_held` | Outcome (CF only) |
| `l2det_skip` / `l2det_reason` | Deterministic L2 |
| `l8_advise` | MAE abort advisor |
| `final_permit` | 1 = trade counted in CF book |
| `stack` | Stack label |

---

## 2. Decision precedence (shadow)

```
L3 HALT        → final_permit = 0
L2det WOULD_SKIP → final_permit = 0
L2AI WOULD_SKIP_SHADOW → final_permit = 1  (SHADOW_ONLY — log only)
L8 advise      → append reason; does not change permit
else FIRE_OK   → final_permit = 1
```

L4 updates `life` / `f_rec` on the permitted path; does not invent skips.

**Armed L2det (offline):** `near_atr_cap OR hour==16` (**v1c**, P2 ARM).  
**Slim near_atr:** ARM but P3 showed BELOW trip remains — prefer v1c.  
**Jul HOLD:** not armed (protect FP).

---

## 3. Offline writer

```text
python blotter/archive/USDJPY-AOS-P4/run_p4_ledger_stack.py
```

Outputs:

| File | Stack |
| --- | --- |
| `ledger_P0_engine.csv` | Engine only + L3/L4/L8 shadow |
| `ledger_det_arm_near_atr.csv` | Slim near_atr |
| `ledger_det_arm_v1c.csv` | **Canonical** L1+L2det v1c+L3+L4+L6 (+L8) |
| `ledger_det_hold_Jul.csv` | Jul HOLD challenger |
| `ledger_det_v1c_plus_ai_shadow.csv` | + L2AI SHADOW overlay |
| `tapes/usdjpy_tip_ledger_v1c_shadow.csv` | Canonical copy for docs |
| `P4_STACK.json` | Score summary |

---

## 4. Research OS preset

Copies:

- `Presets/BMRG-M15-USDJPY-6M-P4_research_OS_W50.set`
- `Profiles/Tester/BMRG/USDJPY/BMRG-M15-USDJPY-6M-P4_research_OS_W50.set`
- `blotter/archive/USDJPY-AOS-P4/` (archive copy)

| Input | Value |
| --- | --- |
| Magic | **26131804** |
| `InpAOS_Enable` | true |
| `InpAiOsMode` | **0 (OFF)** — no USDJPY L2det MQH; L2det offline CF only |
| `InpAiKillSwitch` | **false** |
| `InpAOS_L3_Enable` / L4 / Ledger | true |
| `InpAOS_W250` | **50** |
| `InpAOS_Leak` | **11.4** |
| Geometry / session / ATR max | same as Balanced P0 |

**Compile** `BMRG.mq5` before Tester. Ledger → `COMMON\Files\BMRG_AOS_ledger_26131804.csv`.  
Foreign L2det inputs (EUR/UK/AUD/AAPL/DE) remain **false**.  
P7 research arm target magic remains **26131807**.

---

## 5. L8 MAE abort advisor (P4-T04)

Session sleeve — **secondary** (overnight share ~6.5% tip). No tick MAE on tip tape. Shadow rules (advise-only):

| Code | Fingerprint |
| --- | --- |
| `L8_ADVISE_ABORT_OVERNIGHT_SL` | loss · nights=1 · hold ≥ 12h |
| `L8_ADVISE_ABORT_FAST_SL_NEAR_ATR` | loss · hold &lt; 1h · near_atr_cap |
| `L8_ADVISE_ABORT_FLASH_SL` | loss · hold &lt; 1h (or &lt; 0.25h) |

Tip v1c stack: **9** advises · **9/9 losers** · **0 winners** — useful fingerprint, **not armed**.

---

## 6. Tip stack CF (prior Leak 11.4 pp)

| Stack | n_fire | L2 skip | L3 halt | WR% | E_N | EF_pp | L8 advise |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| P0 engine | 34 | 0 | **12** | 50.0 | +0.10 | −6.9 | 9 |
| near_atr slim | 32 | 6 | **8** | 53.1 | +0.17 | −3.7 | 9 |
| **det ARM v1c** | **37** | **9** | **0** | **62.2** | **+0.37** | **+5.3** | 9 |
| Jul HOLD | 32 | 14 | 0 | 59.4 | +0.31 | +2.5 | 9 |
| v1c + L2AI shadow | 37 | 9 (+9 AI log) | 0 | 62.2 | +0.37 | +5.3 | 9 |

P0 n_fire &lt; 46 because BELOW latch zeros post-trip permits (matches P3).  
L2AI: SHADOW_ONLY · 9 shadow would-skips · `final_permit` unchanged.  
v1c skip precision vs losers: **100%**. Fire retention: **80.4%**.

---

## 7. Sign-off

| Item | Verdict |
| --- | --- |
| Schema matches EA header | **PASS** |
| Offline writer | **PASS** |
| Det stack CF ledger | **PASS** (v1c = promotion path) |
| L2AI shadow on det fires | **PASS** (SHADOW_ONLY) |
| L8 advise-only | **PASS** (secondary) |
| LIVE_WITHHOLD L2det | **NOT ARMED** (no MQH) |
