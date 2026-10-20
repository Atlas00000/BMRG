# EURUSD M15 — L3 / L4 policy (P3)

**Version:** 1.0.0  
**Tasks:** EURUSD-AOS-P3-T01 … T04  
**Date:** 2026-10-18  
**Evidence:** `blotter/archive/EURUSD-AOS-P3/P3_L3L4.json` · `health_path_*.csv`  
**Upstream:** [`aos_l2_policy.md`](./aos_l2_policy.md) v1b stack · [`aos_l2_size_table.md`](./aos_l2_size_table.md)  
**Mode:** **SHADOW / research OS** — not live attach · not M5 Harvest replace

L3 **outranks** L2det / L4 size. L2det skips still apply first on the fire; L3/L4 operate on the **remaining** path.

---

## 1. Bindings (EURUSD M15 expansion)

| Parameter | Value | Note |
| --- | ---: | --- |
| `InpAOS_DD_Limit` | **25%** | Preset · MaxDD from peak |
| Derisk | **20%** (0.8× DD) | f ≤ 0.5 |
| `InpEquityHaltPct` | **15%** | EA halt from start equity (monitor) |
| `InpAOS_BWR` / `R` / Leak | 44.4% / 1.25 / **1.19 pp** proxy | Leak_source=journal until deals+swap |
| Health windows | **W15 / W20** | Expansion main |
| `InpAOS_W250` when wiring | **50** (EA floor) | Preset 250 never arms on tip n~45 |
| Baseline fires / 90d | **25** | FREQUENCY_STALL if 90d-equiv &lt; 12.5 |
| Overnight | **~76%** tip holds ≥12h | MaxDD path includes multi-session inventory |

---

## 2. P3-T01 — L3 halt / derisk

| Trigger | Action | f |
| --- | --- | ---: |
| `dd_peak ≥ 25%` | `HALT_MAXDD` | 0 |
| `dd_peak ≥ 20%` | `DERISK_0.8_DD` | ≤0.5 |
| Lifecycle **BELOW** (W20 E_N≤0 **and** W15 EF_proxy≤0) | `HALT_f0_BELOW_FRONTIER` | 0 |
| Kill-switch | hard OFF | 0 |

**Unlatch (expansion research):** after `HALT_f0_BELOW_FRONTIER`, clear latch only when **W20 E_N > 0 for 2 consecutive evals** and dd_peak &lt; 20%.

### Offline sim (tip)

| Path | n | MaxDD | L3 trips | Notes |
| --- | ---: | ---: | ---: | --- |
| P0 tip (no L2det) | 45 | 3.0% | **1** `BELOW` @ EN20=−0.21 · EF15=−5.6 | Halt latches → many post-trip HALT bus ticks |
| **v1b kept** | 31 | **1.8%** | **0** | No MaxDD / no BELOW |
| Thu∨BUY∧H13 kept | 34 | 1.7% | **0** | Clean alt · no freq stall on path |

**Read:** L2det v1b **prevents** the P0 below-frontier trip on this tip. MaxDD never approaches 25% at 0.01 lot / $500. Overnight inventory does not blow DD on this research deposit — still measure swap before live claims.

---

## 3. P3-T02 — monitors (warn / investigate)

| Monitor | Condition | Bus |
| --- | --- | --- |
| Cost drift | entry spread ≫ tip median **4** (flag if &gt;8) or Leak_proxy↑ &gt; +2 pp | INVESTIGATE / COST_DRIFT_WARN |
| FREQUENCY_STALL | 90d-equiv fires &lt; 50% of 25 | **WARN** only — do not lift ATR max / drop CD |
| Loss streak ≥ 3 | engine pause align | STREAK_WARN |
| Loss streak ≥ 5 | escalate | STREAK_WATCH → INVESTIGATE |
| Overnight cluster | consecutive nights_held without recovery | note for measured swap / L8 (P4) |

### Sim monitors

| Path | max loss streak | FREQUENCY_STALL ticks | cost drift |
| --- | ---: | ---: | --- |
| P0 | 4 | 0 (then HALT latch) | 0 |
| **v1b** | **3** | **2** | 0 |
| Thu∨BUY∧H13 | 3 | 0 | 0 |

Stall warns on v1b are **expected** (skip retention) — not a reason to widen gates.

---

## 4. P3-T03 — L4 rolling health

| Window | Role |
| --- | --- |
| W15 | Fast lifecycle / EF_proxy |
| W20 | Confirm BELOW / Expanding |
| W50 | Use when `InpAOS_W250=50` wired |
| W100/W250 | Adopt when n allows |

### Lifecycle → f (armed with L4 size)

| State | Rule (EURUSD M15 expansion) | f_mult |
| --- | --- | ---: |
| WARMUP | n_window &lt; 15 | 1.0 |
| EXPANDING | W15 E_N > baseline tip E_N (+0.05) and not falling | 1.0 |
| STABLE | W15 E_N ≥ 0 | 1.0 |
| COMPRESSING | W15 E_N falling **2** consecutive evals | 0.5 |
| NEAR | W15 EF_proxy ≤ 1 pp **or** W15 E_N &lt; 0 | 0.25 |
| BELOW | W20 E_N ≤ 0 **and** W15 EF_proxy ≤ 0 | 0.0 → L3 halt |

### End-of-tip health (sim)

| Path | last W15 E_N | last W20 E_N | Dominant lives |
| --- | ---: | ---: | --- |
| P0 | +0.20 | +0.01 | EXPANDING + **BELOW** mid-path latch |
| **v1b** | **+0.35** | **+0.35** | **EXPANDING/STABLE** · no BELOW |
| Thu∨BUY∧H13 | +0.05 | +0.13 | EXPANDING · no BELOW |

CSV paths: `blotter/archive/EURUSD-AOS-P3/health_path_*.csv`.

---

## 5. P3-T04 — L4 → L3 recommend bus

| L4 / monitor state | Bus action |
| --- | --- |
| BELOW | **L3_HALT** (f=0) |
| COMPRESSING | **INVESTIGATE** (regime/execution) · f=0.5 |
| NEAR or DERISK_0.8_DD | **DERISK** f≤0.5 |
| STREAK≥5 | **STREAK_WATCH** |
| FREQUENCY_STALL | **WARN** |
| COST_DRIFT | **INVESTIGATE** |
| EXPANDING / STABLE | **NONE** f=1.0 |
| L2det WOULD_SKIP | skip (f=0 for that fire) — not an L3 trip |

**Invariant:** L3 halt ⊃ L4 size ⊃ L2det skip on a single fire decision.

---

## 6. Research OS wiring checklist (when building `.set`)

```text
InpAOS_Enable=true
InpAOS_L3_Enable=true
InpAOS_L4_SizeMod=true
InpAiOsMode=0                    # L2 AI still OFF / DISARM
InpAOS_L2AI_Enable=false
InpAOS_DD_Limit=25
InpAOS_BWR=44.4
InpAOS_R=1.25
InpAOS_Leak=1.19                 # journal proxy metadata (not measured)
InpAOS_W250=50                   # expansion floor (not 250)
# L2det Thu / BUY∧near_atr: shadow ledger or future L2det_eur_m15 include
```

Magic: keep **26101817** engine; OS experiment magic **2612xxxx** if a separate preset is required.

---

## 7. Verdict

| Item | Status |
| --- | --- |
| P3-T01 L3 policy | **SIGNED** for shadow · v1b path trip-free on tip |
| P3-T02 monitors | **SIGNED** |
| P3-T03 L4 W15/W20 | **SIGNED** · paths archived |
| P3-T04 bus | **SIGNED** |
| Live / LIVE_WITHHOLD | **NOT** armed |
| Measured Leak + swap | **OPEN** — do not promote P7 on proxy alone |
