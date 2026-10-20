# JP225 — L3 / L4 policy (P3)

**Version:** 1.0.0  
**Tasks:** JP225-AOS-P3-T01 … T04  
**Date:** 2026-10-19  
**Evidence:** `blotter/archive/JP225-AOS-P3/P3_L3L4.json` · `health_path_*.csv`  
**Upstream:** [`aos_l2_policy.md`](./aos_l2_policy.md) · [`aos_l2_size_table.md`](./aos_l2_size_table.md)  
**Mode:** **SHADOW / research OS** — not live attach · not FX/EU-index replace

L3 **outranks** L2det / L4 size. L2det skips still apply first on the fire; L3/L4 operate on the **remaining** path.

---

## 1. Bindings (JP225 expansion)

| Parameter | Value | Note |
| --- | ---: | --- |
| `InpAOS_DD_Limit` | **25%** | MaxDD from peak |
| Derisk | **20%** (0.8× DD) | f ≤ 0.5 |
| `InpEquityHaltPct` | **15%** | EA halt from start equity (monitor) |
| `InpAOS_BWR` / `R` / Leak | **40%** / **1.50** / **2.45 pp measured** | prior 4.3 = stress only · see `LEAK_MEASURED.json` |
| Deposit (sim) | **$500** | Matches Tester baseline |
| Health windows | **W15 / W20** | Expansion main |
| W50 | optional when wiring | tip kept n=43 can start late |
| `InpAOS_W250` when wiring | **50** (EA floor) | Preset 250 never arms on tip n~79 |
| Baseline tip E_N | **+0.076R** | EXPANDING bar (P1 pre-L2) |
| Baseline fires / 90d | **60** | FREQUENCY_STALL if 90d-equiv &lt; 30 |
| L2 overlay | **May∨Jul** ARM | Wed/H14 HOLD · SELL∧May narrow |
| Overnight | nights_held share ~9% · cluster max **1** | L8 **secondary** (P4) |

**EF note:** Lifecycle EF for new work uses **Leak measured 2.45 pp**. P3 health paths were scored under prior 4.3 — retain those CSVs as freeze; do not re-litigate P3 trips.

---

## 2. P3-T01 — L3 halt / derisk (OFFHOME-path aware)

| Trigger | Action | f |
| --- | --- | ---: |
| `dd_peak ≥ 25%` | `HALT_MAXDD` | 0 |
| `dd_peak ≥ 20%` | `DERISK_0.8_DD` | ≤0.5 |
| Lifecycle **BELOW** (W20 E_N≤0 **and** W15 EF_prior≤0) | `HALT_f0_BELOW_FRONTIER` | 0 |
| Kill-switch | hard OFF | 0 |
| Overnight cluster | **note only** → L8 (P4) | — |

**Unlatch (expansion research):** after `HALT_f0_BELOW_FRONTIER`, clear latch only when **W20 E_N > 0 for 2 consecutive evals** and dd_peak &lt; 20%.

### Offline sim

| Path | n | MaxDD | L3 trips | max L | Notes |
| --- | ---: | ---: | ---: | ---: | --- |
| P1 tip (no L2det) | 79 | 3.7% | **1** BELOW | **11** | EN20=−0.38 · EF15=−31 · heavy HALT latch |
| **May∨Jul kept** | **43** | **1.5%** | **1** BELOW | **4** | Soft mid-path EN20=0 · far fewer BELOW ticks |
| May-only kept | 56 | 2.4% | 1 BELOW | 4 | Weaker than May∨Jul |
| Wed HOLD kept | 59 | 2.3% | 1 BELOW | **7** | Aug collateral path |
| SELL∧May kept | 65 | 2.4% | 1 BELOW | 4 | Narrow arm |
| P1 Jan–Aug | 143 | 4.4% | 1 BELOW | 11 | Pre-tip stress |
| May∨Jul Jan–Aug | 107 | 2.7% | 1 BELOW | 6 | Overlay helps · L3 still needed |

**Read:** MaxDD never approaches 25% at proxy lot / $500. L2det **May∨Jul** shrinks DD, streak, and BELOW density but **does not eliminate** the need for L3 — one soft mid-path trip remains (EN20≈0). That is L3 doing its job, not a reject of the arm. Overnight cluster max **1** — no auto-halt on inventory.

---

## 3. P3-T02 — monitors (warn / investigate)

| Monitor | Condition | Bus |
| --- | --- | --- |
| Cost drift | rolling med entry spread ≫ tip journal med+500 | INVESTIGATE (journal; live ~2300 separate) |
| FREQUENCY_STALL | 90d-equiv fires &lt; 50% of 60 | **WARN** only — do not lift ATR max / drop Fade |
| Loss streak ≥ 3 | engine pause align | STREAK_WARN |
| Loss streak ≥ 5 | escalate | STREAK_WATCH → INVESTIGATE |
| Overnight cluster | consecutive nights_held | note → L8 (P4) |

### Sim monitors

| Path | max L | FREQ_STALL ticks | overnight cluster |
| --- | ---: | ---: | ---: |
| P1 tip | **11** | 0 (then HALT latch) | 1 |
| **May∨Jul** | **4** | **5** (expected ret~54%) | 1 |
| May-only | 4 | 0 | 1 |
| Wed HOLD | 7 | 0 | 1 |
| Jan–Aug P1 / arm | 11 / 6 | — | 1 |

Stall warns after May∨Jul are **expected** — not a reason to widen ATR or disable Fade.

---

## 4. P3-T03 — L4 rolling health

| Window | Role |
| --- | --- |
| W15 | Fast lifecycle / EF_prior |
| W20 | Confirm BELOW / Expanding |
| W50 | Optional late tip / when wiring |
| W100/W250 | Adopt when n allows |

### Lifecycle → f (armed with L4 size)

| State | Rule (JP225 expansion) | f_mult |
| --- | --- | ---: |
| WARMUP | n_window &lt; 15 | 1.0 |
| EXPANDING | W15 E_N > baseline tip E_N (+0.076) and not falling | 1.0 |
| STABLE | W15 E_N ≥ 0 | 1.0 |
| COMPRESSING | W15 E_N falling **2** consecutive evals | 0.5 |
| NEAR | W15 EF_prior ≤ 1 pp **or** W15 E_N &lt; 0 | 0.25 |
| BELOW | W20 E_N ≤ 0 **and** W15 EF_prior ≤ 0 | 0.0 → L3 halt |

### End-of-tip health (sim)

| Path | last W15 E_N | last W20 E_N | last EF15_pp | Dominant lives |
| --- | ---: | ---: | ---: | --- |
| P1 tip | +0.67 | +0.38 | +22.4 | EXPANDING late · mid **BELOW** latch |
| **May∨Jul** | **+0.67** | **+0.38** | **+22.4** | More EXPANDING/NONE · thinner BELOW |
| May-only | +0.67 | +0.38 | +22.4 | Similar end · denser BELOW mid |
| Wed HOLD | +0.33 | +0.13 | +9.0 | Weaker end · COMPRESSING tick |

CSV paths: `blotter/archive/JP225-AOS-P3/health_path_*.csv`.

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
| OVERNIGHT_CLUSTER | note → L8 (P4) — not auto-halt |

**Invariant:** L3 halt ⊃ L4 size ⊃ L2det skip on a single fire decision.

---

## 6. Research OS wiring checklist (when building `.set`)

```text
InpAOS_Enable=true
InpAOS_L3_Enable=true
InpAOS_L4_SizeMod=true
InpAiOsMode=0                    # L2 AI still OFF / SHADOW
InpAOS_L2AI_Enable=false
InpAiKillSwitch=true             # until HITL
InpAOS_DD_Limit=25
InpAOS_BWR=40
InpAOS_R=1.50
InpAOS_Leak=4.3                  # prior metadata (not measured)
InpAOS_W250=50                   # expansion floor (not 250)
# L2det May∨Jul: native JP225 pin / Filters — not EUR/DE40/UK
```

Magic: keep engine **26101904**; research OS **26151907** (P4+ `.set`). Never collide with DE40 `2614xxxx` / USDJPY `2613xxxx` / EUR / AUD live.

---

## 7. Explicit non-claims

- Shadow path equity ≠ live expectancy.  
- One BELOW trip on May∨Jul kept ≠ arm failure — L3 survival.  
- FREQUENCY_STALL after skips ≠ permission to lift ATR max.  
- No MQH/live arm until P7 HITL (P4 offline ledger done · still no MQH).  
- Leak measured **2.45 pp** — tip Stage-1 pass; live ~2300 pts = P7 re-check.
