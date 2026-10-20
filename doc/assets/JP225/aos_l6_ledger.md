# JP225 — L6 decision ledger (P4)

**Version:** 1.0.0  
**Tasks:** JP225-AOS-P4-T01 … T04  
**Date:** 2026-10-19  
**Evidence:** `blotter/archive/JP225-AOS-P4/` · `tapes/jp225_tip_ledger_may_or_jul_shadow.csv`  
**Mode:** **OFFLINE SHADOW only** — **no** MQH wire · **no** research OS `.set` arm · L2AI **DISARM**

---

## 1. Schema

### EA-compatible columns (future COMMON Files CSV)

| Col | Type | Meaning |
| --- | --- | --- |
| `t` | datetime | Decision time (open) |
| `side` | BUY/SELL | Engine side |
| `layer` | enum | `ENGINE` · `L2DET` · `L2AI` · `L3` · `L4` · `L8` |
| `decision` | enum | `FIRE_OK` · `WOULD_SKIP` · `WOULD_SKIP_SHADOW` · `HALT` |
| `reason` | string | Pipe-joined codes |
| `life` | enum | WARMUP / EXPANDING / STABLE / COMPRESSING / NEAR / BELOW |
| `f_rec` | float | Recommended size factor |
| `w250_EF` | float | Rolling EF_measured pp (W15 in offline writer) |
| `w250_EN` | float | Rolling E_N |
| `ai_proba` | float | p_lose (empty — DISARM) |
| `ai_skip` | 0/1 | Model would-skip |
| `model` | string | `none` / `L2skip_jp225_DISARM` |
| `halt` | 0/1 | L3 halt latched |
| `derisk` | 0/1 | L3 derisk active |
| `mode` | string | `SHADOW` |

### JP225 extensions

| Col | Meaning |
| --- | --- |
| `event_id` | `{magic}-JPN225-{side}-{stamp}` |
| `open_time` / `exit_reason` / `win` / `pnl_R` / `nights_held` | CF fields |
| `l2det_skip` / `l2det_reason` | May∨Jul deterministic |
| `l8_advise` | Secondary MAE/overnight advisor |
| `final_permit` | 1 = counted in CF book |
| `stack` | Stack label |

---

## 2. Decision precedence (shadow)

```
L3 HALT              → final_permit = 0
L2det WOULD_SKIP     → final_permit = 0
L2AI WOULD_SKIP_SHADOW → final_permit = 1  (DISARM — log only)
L8 advise            → append reason; does not change permit
else FIRE_OK         → final_permit = 1
```

Canonical L2det: **May∨Jul** (`L2DET_SKIP_MAY` | `L2DET_SKIP_JUL`).

---

## 3. Offline writer

```text
python blotter/archive/JP225-AOS-P4/run_p4_ledger_stack.py
```

| File | Stack |
| --- | --- |
| `ledger_det_may_or_jul.csv` | Canonical L1+L2det+L3+L4+L6 (+L8) |
| `ledger_det_may_only.csv` | Lighter May-only arm |
| `ledger_det_may_or_jul_plus_ai_shadow.csv` | + L2AI DISARM overlay |
| `ledger_baseline_no_l2.csv` | L3/L4/L8 only (diagnostic) |
| `tapes/jp225_tip_ledger_may_or_jul_shadow.csv` | Canonical doc copy |

**Leak in EF:** measured **2.45 pp** (`LEAK_MEASURED.json`).

---

## 4. L8 (secondary · index sleeve)

Advise-only fingerprints (no tick MAE):

| Code | Trigger |
| --- | --- |
| `L8_ADVISE_ABORT_OVERNIGHT_SL` | loser · nights_held≥1 · hold_h≥12 |
| `L8_ADVISE_ABORT_FAST_SL_NEAR_ATR` | loser · hold_h&lt;1 · near_atr |
| `L8_ADVISE_ABORT_FLASH_SL` | loser · hold_h&lt;0.25 |

Never changes `final_permit` in P4.

---

## 5. Explicit non-goals (this phase)

- No `Include/AOS_L2det_jp225.mqh`
- No research OS preset arm (magic **26151907** waits for P7 HITL)
- No foreign L2 pins
- No live attach / FX-EU replace
