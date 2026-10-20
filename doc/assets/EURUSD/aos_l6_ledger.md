# EURUSD M15 — L6 decision ledger (P4)

**Version:** 1.0.0  
**Tasks:** EURUSD-AOS-P4-T01 … T04  
**Date:** 2026-10-18  
**Evidence:** `blotter/archive/EURUSD-AOS-P4/` · `tapes/eurusd_m15_tip_ledger_v1b_shadow.csv`  
**EA parity:** `Include/AOS.mqh` → `AOSLedger` / `AOSInit` header · `Include/AOS_L2det_eur.mqh`

**Mode:** MQL wire — EUR L2det gated by `InpAOS_EUR_L2detEnable` (default **false** so M5 Harvest keeps INF). Research `.set` arms L2det LIVE_WITHHOLD + L3/L4/ledger.

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
| `model` | string | Pin / `none` / `L2skip_eur_m15_DISARM` |
| `halt` | 0/1 | L3 halt latched |
| `derisk` | 0/1 | L3 derisk active |
| `mode` | string | `SHADOW` / `LIVE` |

### EURUSD extensions (offline / promotion packets)

| Col | Meaning |
| --- | --- |
| `event_id` | Stable fire id |
| `open_time` | Full open stamp |
| `exit_reason` | TP/SL/… (post-hoc for CF) |
| `win` / `pnl_R` / `nights_held` | Outcome (CF only) |
| `l2det_skip` / `l2det_reason` | Deterministic L2 |
| `l8_advise` | MAE / overnight abort advisor |
| `final_permit` | 1 = trade counted in CF book |
| `stack` | Stack label |

---

## 2. Decision precedence (shadow)

```
L3 HALT            → final_permit = 0
L2det WOULD_SKIP   → final_permit = 0
L2AI WOULD_SKIP_SHADOW → final_permit = 1  (DISARM — log only)
L8 advise          → append reason; does not change permit
else FIRE_OK       → final_permit = 1
```

L4 updates `life` / `f_rec` on the permitted path; does not invent skips.

---

## 3. Offline writer

```text
python blotter/archive/EURUSD-AOS-P4/run_p4_ledger_stack.py
```

Outputs:

| File | Stack |
| --- | --- |
| `ledger_det_v1b.csv` | L1+L2det v1b+L3+L4+L6 (+L8 advise) |
| `ledger_det_v1b_plus_ai_shadow.csv` | + L2AI DISARM overlay |
| `tapes/eurusd_m15_tip_ledger_v1b_shadow.csv` | Canonical copy for docs |
| `P4_STACK.json` | Tip CF summary |

---

## 4. Research OS preset

Copies:

- `Presets/BMRG-M15-EURUSD-6M-P4_research_OS_W50.set`
- `Profiles/Tester/BMRG/EURUSD/BMRG-M15-EURUSD-6M-P4_research_OS_W50.set`
- `blotter/archive/EURUSD-AOS-P4/` (same)

| Input | Value |
| --- | --- |
| Magic | **26121804** |
| Engine geometry | same as P2 light (26101817) |
| `InpAOS_Enable` | true |
| `InpAiOsMode` | **LIVE_WITHHOLD (2)** — L2det blocks in Tester |
| `InpAiKillSwitch` | **false** |
| `InpAOS_EUR_L2detEnable` | **true** (Thu ∨ BUY∧nearATR) |
| `InpAOS_L3_Enable` / L4 / Ledger | true |
| `InpAOS_W250` | **50** |
| `InpAOS_Leak` | **1.19** (journal proxy) |
| `InpAOS_BWR` / `InpAOS_R` | 44.4 / 1.25 |
| L2AI | OFF (DISARM pin; shadow CF only offline) |

**Compile** `BMRG.mq5` before Tester. Ledger → `COMMON\Files\BMRG_AOS_ledger_26121804.csv`.  
**Do not** load this `.set` on M5 Harvest live charts.

---

## 5. L8 MAE / overnight abort advisor (P4-T04)

No tick MAE on tip tape. Shadow rules (advise-only) — overnight-first for this book:

| Code | Fingerprint |
| --- | --- |
| `L8_ADVISE_ABORT_OVERNIGHT_SL` | loss · nights_held=1 · hold ≥ 12h |
| `L8_ADVISE_ABORT_FAST_SL_NEAR_ATR` | loss · hold &lt; 4h · near_atr_cap |
| `L8_ADVISE_ABORT_FLASH_SL` | loss · hold &lt; 1h |

Tip v1b: **21** advises · **21/21 losers** · **0 winners** · **16** overnight — useful fingerprint, **not armed**.

---

## 6. Sign-off

| Item | Verdict |
| --- | --- |
| Schema matches EA header | **PASS** |
| Offline writer | **PASS** |
| Det stack CF ledger | **PASS** (see REVIEW) |
| L2AI shadow on det fires | **PASS** (DISARM; 5 shadow skips) |
| L8 advise-only (overnight-primary) | **PASS** |
| LIVE_WITHHOLD on live M5 | **NOT ARMED** |
| Measured Leak+swap | **OPEN** |
