# DE40 — L6 decision ledger (P4)

**Version:** 1.0.0  
**Tasks:** DE40-AOS-P4-T01 … T04  
**Date:** 2026-10-19  
**Evidence:** `blotter/archive/DE40-AOS-P4/` · `tapes/de40_tip_ledger_arm_shadow.csv`  
**EA parity:** `Include/AOS.mqh` → `AOSLedger` / header columns  

**Mode:** Offline stack complete. MQL L2det for DE40 **not wired** (`AOS_L2det_de.mqh` absent) — BUY∧near_atr is CF/ledger-shadow only. Research `.set` arms L3/L4/ledger (W50).

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
| `model` | string | Pin / `none` / `L2skip_de40_DISARM` |
| `halt` | 0/1 | L3 halt latched |
| `derisk` | 0/1 | L3 derisk active |
| `mode` | string | `SHADOW` / `LIVE` |

### DE40 extensions (offline / promotion packets)

| Col | Meaning |
| --- | --- |
| `event_id` | Stable fire id (`26101902-DE30-…`) |
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
L2AI WOULD_SKIP_SHADOW → final_permit = 1  (DISARM — log only)
L8 advise      → append reason; does not change permit
else FIRE_OK   → final_permit = 1
```

L4 updates `life` / `f_rec` on the permitted path; does not invent skips.

**Armed L2det (offline):** `BUY ∧ near_atr_cap` only (P2 ARM).  
**v1b HOLD (not armed):** ARM ∪ H13 — Aug FP risk remains.

---

## 3. Offline writer

```text
python blotter/archive/DE40-AOS-P4/run_p4_ledger_stack.py
```

Outputs:

| File | Stack |
| --- | --- |
| `ledger_P0_engine.csv` | Engine only + L3/L4/L8 shadow |
| `ledger_det_arm_BUY_near_atr.csv` | L1+L2det ARM+L3+L4+L6 (+L8) |
| `ledger_det_hold_v1b.csv` | ARM ∪ H13 (HOLD) |
| `ledger_det_arm_plus_ai_shadow.csv` | + L2AI DISARM overlay |
| `tapes/de40_tip_ledger_arm_shadow.csv` | Canonical copy for docs |
| `P4_STACK.json` | Score summary |

---

## 4. Research OS preset

Copies:

- `Presets/BMRG-M15-DE40-6M-P4_research_OS_W50.set`
- `Profiles/Tester/BMRG/DE40/BMRG-M15-DE40-6M-P4_research_OS_W50.set`
- `blotter/archive/DE40-AOS-P4/` (archive copy)

| Input | Value |
| --- | --- |
| Magic | **26141904** |
| `InpAOS_Enable` | true |
| `InpAiOsMode` | **0 (OFF)** — no DE L2det MQH; L2det offline CF only |
| `InpAiKillSwitch` | **false** |
| `InpAOS_L3_Enable` / L4 / Ledger | true |
| `InpAOS_W250` | **50** |
| `InpAOS_Leak` | **9.8** |
| Geometry / session / ATR max | same as Balanced P0 |

**Compile** `BMRG.mq5` before Tester. Ledger → `COMMON\Files\BMRG_AOS_ledger_26141904.csv`.  
Foreign L2det inputs (EUR/UK/AUD/AAPL) remain **false**.

---

## 5. L8 MAE abort advisor (P4-T04)

Cash sleeve — **secondary**. No tick MAE on tip tape. Shadow rules (advise-only):

| Code | Fingerprint |
| --- | --- |
| `L8_ADVISE_ABORT_OVERNIGHT_SL` | loss · nights=1 · hold ≥ 12h |
| `L8_ADVISE_ABORT_FAST_SL_NEAR_ATR` | loss · hold &lt; 1h · near_atr_cap |
| `L8_ADVISE_ABORT_FLASH_SL` | loss · hold &lt; 1h (or &lt; 0.25h) |

Tip ARM stack: **16** advises · **16/16 losers** · **0 winners** — useful fingerprint, **not armed**.

---

## 6. Tip stack CF (prior Leak 9.8 pp)

| Stack | n_fire | L2 skip | WR% | E_N | EF_pp | L3 halt | L8 advise |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| P0 engine | 77 | 0 | 58.4 | +0.31 | +4.2 | 0 | 16 |
| **det ARM BUY∧near_atr** | **62** | **15** | **62.9** | **+0.42** | **+8.7** | 0 | 16 |
| det HOLD v1b | 53 | 24 | 66.0 | +0.49 | +11.8 | 0 | 16 |
| ARM + L2AI shadow | 62 | 15 (+18 AI log) | 62.9 | +0.42 | +8.7 | 0 | 16 |

L2AI: DISARM · 18 shadow would-skips · final_permit unchanged.

---

## 7. Sign-off

| Item | Verdict |
| --- | --- |
| Schema matches EA header | **PASS** |
| Offline writer | **PASS** |
| Det stack CF ledger | **PASS** (ARM = promotion path) |
| L2AI shadow on det fires | **PASS** (DISARM) |
| L8 advise-only | **PASS** (secondary) |
| LIVE_WITHHOLD L2det | **NOT ARMED** (no MQH) |
