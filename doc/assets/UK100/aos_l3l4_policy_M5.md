# UK100 M5 — L3 / L4 policy (P3)

**Version:** 1.0.0  
**Tasks:** UK100-M5-AOS-P3-T01 … T04  
**Date:** 2026-10-20  
**Evidence:** `blotter/archive/UK100-M5-AOS-P3/P3_L3L4.json` · `health_path_*.csv`  
**Upstream:** [`aos_l2_policy_M5.md`](./aos_l2_policy_M5.md) v1b stack · [`aos_l2_size_table_M5.md`](./aos_l2_size_table_M5.md)  
**Mode:** **SHADOW / research OS** — not live attach · no M15 L3 pin reuse

L3 **outranks** L2det / L4 size. L2det skips still apply first on the fire; L3/L4 operate on the **remaining** path.

---

## 1. Bindings (UK100 M5 expansion)

| Parameter | Value | Note |
| --- | ---: | --- |
| `InpAOS_DD_Limit` | **25%** | MaxDD from peak |
| Derisk | **20%** (0.8× DD) | f ≤ 0.5 |
| `InpEquityHaltPct` | **15%** | EA halt from start equity (monitor) |
| `InpAOS_BWR` / `R` / Leak | 44.4% / 1.25 / **5.93 pp** proxy | Leak_source=journal until deals |
| Health windows | **W15 / W20 / W50** | Dense M5 — W20/W50 first-class |
| `InpAOS_W250` when wiring | **50** (EA min) | Research OS `.set` |
| Baseline fires / 90d | **80** | Tip pace ~85/90d · FREQUENCY_STALL if 90d-equiv &lt; 40 |
| Baseline tip E_N | **+0.183R** | EXPANDING threshold |

---

## 2. P3-T01 — L3 halt / derisk

| Trigger | Action | f |
| --- | --- | ---: |
| `dd_peak ≥ 25%` | `HALT_MAXDD` | 0 |
| `dd_peak ≥ 20%` | `DERISK_0.8_DD` | ≤0.5 |
| Lifecycle **BELOW** (W20 E_N≤0 **and** W15 EF_proxy≤0) | `HALT_f0_BELOW_FRONTIER` | 0 |
| Kill-switch | hard OFF | 0 |

**Unlatch (expansion research):** after `HALT_f0_BELOW_FRONTIER`, clear latch only when **W20 E_N > 0 for 2 consecutive evals** and dd_peak &lt; 20%.

### Offline sim (tip May→Aug)

| Path | n | MaxDD | L3 trips | Notes |
| --- | ---: | ---: | ---: | --- |
| P0 tip (no L2det) | 116 | 1.9% | **1** `BELOW` @ EN20=−0.10 · EF15=−17 | Halt latches · last life **BELOW** |
| **v1b kept** | 83 | **1.6%** | **0** | No MaxDD / no BELOW · last **EXPANDING** |
| H12 aggressive kept | 69 | 1.3% | **0** | Cleaner life · more freq warns |

**Read:** L2det v1b **prevents** the P0 below-frontier trip on this tip (Aug soft cluster). MaxDD never approaches 25% at 0.1 lot / $500.

---

## 3. P3-T02 — monitors (warn / investigate)

| Monitor | Condition | Bus |
| --- | --- | --- |
| Cost drift | rolling med20 entry spread ≫ 120+40 pts | INVESTIGATE |
| FREQUENCY_STALL | 90d-equiv fires &lt; 50% of **80** | **WARN** only — do not lift ATR max |
| Loss streak ≥ 3 | engine pause align | STREAK_WARN |
| Loss streak ≥ 5 | escalate | STREAK_WATCH → INVESTIGATE |

### Sim monitors

| Path | max loss streak | FREQUENCY_STALL ticks | Cost drift |
| --- | ---: | ---: | ---: |
| P0 | 5 | 13 | 0 |
| **v1b** | **5** | 13 | 0 |
| H12 aggressive | 4 | 23 | 0 |

Stall ticks on v1b are **expected** (skip retention + sparse weeks) — not a reason to widen ATR max. Tip spreads stayed near 120 (no cost drift).

---

## 4. P3-T03 — L4 rolling health

| Window | Role |
| --- | --- |
| W15 | Fast lifecycle / EF_proxy |
| W20 | Confirm BELOW / Expanding |
| **W50** | Dense-TF confirm (tip n=116 supports) |
| W100/W250 | Adopt when n allows |

### Lifecycle → f (armed with L4 size)

| State | Rule (UK100 M5 expansion) | f_mult |
| --- | --- | ---: |
| WARMUP | n_window &lt; 15 | 1.0 |
| EXPANDING | W15 E_N > baseline tip E_N (+0.183) and not falling | 1.0 |
| STABLE | W15 E_N ≥ 0 | 1.0 |
| COMPRESSING | W15 E_N falling **2** consecutive evals | 0.5 |
| NEAR | W15 EF_proxy ≤ 1 pp **or** W15 E_N &lt; 0 | 0.25 |
| BELOW | W20 E_N ≤ 0 **and** W15 EF_proxy ≤ 0 | 0.0 → L3 halt |

### End-of-tip health (sim)

| Path | last W15 E_N | last W20 E_N | last W50 E_N | Dominant lives |
| --- | ---: | ---: | ---: | --- |
| P0 | −0.25 | −0.21 | +0.08 | EXPANDING mid · **BELOW** late (Aug) |
| **v1b** | **+0.35** | **+0.46** | **+0.31** | **EXPANDING** · no BELOW |
| H12 aggressive | +0.50 | +0.35 | +0.31 | EXPANDING |

CSV paths: `blotter/archive/UK100-M5-AOS-P3/health_path_*.csv`.

---

## 5. P3-T04 — L4 → L3 recommend bus

| L4 / monitor state | Bus action |
| --- | --- |
| BELOW | **L3_HALT** (f=0) |
| COMPRESSING | **INVESTIGATE** (regime/execution) · f=0.5 |
| NEAR or DERISK_0.8_DD | **DERISK** f≤0.5 |
| STREAK≥5 | **STREAK_WATCH** |
| FREQUENCY_STALL | **WARN** |
| EXPANDING / STABLE | **NONE** f=1.0 |
| L2det v1b WOULD_SKIP | skip (f=0 for that fire) — not an L3 trip |

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
InpAOS_Leak=5.93                 # journal proxy metadata
InpAOS_W250=50                   # expansion floor (not 250)
# L2det v1b: (Mon∧H12-13)∨(SELL∧H12-13) — wire AOS_L2det_uk_m5 at P4
```

Magic: keep engine **26101905**; OS experiment magics **2612xxxx** (P7 target **26121907**).

---

## 7. Verdict

| Item | Status |
| --- | --- |
| P3-T01 L3 policy | **SIGNED** for shadow · v1b path trip-free on tip |
| P3-T02 monitors | **SIGNED** |
| P3-T03 L4 W15/W20/W50 | **SIGNED** · paths archived |
| P3-T04 bus | **SIGNED** |
| Live / LIVE_WITHHOLD | **NOT** armed |

**Next:** P4 ledger + det stack shadow · optional `AOS_L2det_uk_m5.mqh` wire.
