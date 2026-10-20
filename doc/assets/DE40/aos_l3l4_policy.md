# DE40 — L3 / L4 policy (P3)

**Version:** 1.0.0  
**Tasks:** DE40-AOS-P3-T01 … T04  
**Date:** 2026-10-19  
**Evidence:** `blotter/archive/DE40-AOS-P3/P3_L3L4.json` · `health_path_*.csv`  
**Upstream:** [`aos_l2_policy.md`](./aos_l2_policy.md) · [`aos_l2_size_table.md`](./aos_l2_size_table.md)  
**Mode:** **SHADOW / research OS** — not live attach · not FX/UK replace

L3 **outranks** L2det / L4 size. L2det skips still apply first on the fire; L3/L4 operate on the **remaining** path.

---

## 1. Bindings (DE40 expansion)

| Parameter | Value | Note |
| --- | ---: | --- |
| `InpAOS_DD_Limit` | **25%** | Preset · MaxDD from peak |
| Derisk | **20%** (0.8× DD) | f ≤ 0.5 |
| `InpEquityHaltPct` | **15%** | EA halt from start equity (monitor) |
| `InpAOS_BWR` / `R` / Leak | 44.4% / 1.25 / **9.8 pp prior** | Leak_source=prior until deals |
| Health windows | **W15 / W20** | Expansion main |
| W50 | optional when wiring | tip n=77 can start W50 late-path |
| `InpAOS_W250` when wiring | **50** (EA floor) | Preset 250 never arms on tip n~77 |
| Baseline tip E_N | **+0.315R** | EXPANDING bar |
| Baseline fires / 90d | **42** | FREQUENCY_STALL if 90d-equiv &lt; 21 |
| L2 overlay | **BUY∧near_atr** ARM | H13/v1b HOLD challengers |

**EF note:** Lifecycle EF uses **Leak prior 9.8 pp**. That makes tip W15 often **NEAR** even when E_N>0 (fat DE30 spread tax). Do not “fix” by swapping in journal proxy (~1.5 pp) for L3 decisions.

---

## 2. P3-T01 — L3 halt / derisk

| Trigger | Action | f |
| --- | --- | ---: |
| `dd_peak ≥ 25%` | `HALT_MAXDD` | 0 |
| `dd_peak ≥ 20%` | `DERISK_0.8_DD` | ≤0.5 |
| Lifecycle **BELOW** (W20 E_N≤0 **and** W15 EF_prior≤0) | `HALT_f0_BELOW_FRONTIER` | 0 |
| Kill-switch | hard OFF | 0 |

**Unlatch (expansion research):** after `HALT_f0_BELOW_FRONTIER`, clear latch only when **W20 E_N > 0 for 2 consecutive evals** and dd_peak &lt; 20%.

### Offline sim

| Path | n | MaxDD | L3 trips | Notes |
| --- | ---: | ---: | ---: | --- |
| P0 tip | 77 | **4.4%** | **0** | NEAR common (Leak prior) · max streak 4 |
| **BUY∧near_atr kept** | 62 | **3.1%** | **0** | Fewer NEAR · last EN20 **+0.24** |
| v1b HOLD kept | 53 | **2.7%** | **0** | Cleanest DD · more freq warns |
| P0 YTD | 147 | 13.4% | **1** BELOW | Feb path · latch → many HALT bus ticks |
| BUY∧near_atr YTD | 125 | 12.8% | **1** BELOW | Same Feb hole (calendar Feb not in ARM map) |

**Read:** Tip home sleeve never trips L3 at 0.1 lot / $500. YTD **needs** L3 BELOW halt (Feb regime) — overlay BUY∧near_atr does not remove Feb; optional Feb SOFT is YTD-path only (see P2). MaxDD never hits 25%.

---

## 3. P3-T02 — monitors (warn / investigate)

| Monitor | Condition | Bus |
| --- | --- | --- |
| Cost drift | rolling median entry spread ≫ tip journal median+40 | INVESTIGATE (journal only) |
| FREQUENCY_STALL | 90d-equiv fires &lt; 50% of 42 | **WARN** only — do not lift ATR max |
| Loss streak ≥ 3 | engine pause align | STREAK_WARN |
| Loss streak ≥ 5 | escalate | STREAK_WATCH → INVESTIGATE |

### Sim monitors

| Path | max loss streak | FREQUENCY_STALL ticks | Notes |
| --- | ---: | ---: | --- |
| P0 tip | 4 | 2 | Dense tip |
| BUY∧near_atr tip | **3** | 4 | Expected skip retention |
| v1b tip | 3 | 6 | More skips → more stall warns |
| P0 / arm YTD | **5** | — | Streak escalate · BELOW latch |

Stall warns after L2det are **expected** — not a reason to widen ATR max or session.

---

## 4. P3-T03 — L4 rolling health

| Window | Role |
| --- | --- |
| W15 | Fast lifecycle / EF_prior |
| W20 | Confirm BELOW / Expanding |
| W50 | Optional late tip / when wiring |
| W100/W250 | Adopt when n allows |

### Lifecycle → f (armed with L4 size)

| State | Rule (DE40 expansion) | f_mult |
| --- | --- | ---: |
| WARMUP | n_window &lt; 15 | 1.0 |
| EXPANDING | W15 E_N > baseline tip E_N (+0.315) and not falling | 1.0 |
| STABLE | W15 E_N ≥ 0 | 1.0 |
| COMPRESSING | W15 E_N falling **2** consecutive evals | 0.5 |
| NEAR | W15 EF_prior ≤ 1 pp **or** W15 E_N &lt; 0 | 0.25 |
| BELOW | W20 E_N ≤ 0 **and** W15 EF_prior ≤ 0 | 0.0 → L3 halt |

### End-of-window health (sim)

| Path | last W15 E_N | last W20 E_N | Dominant lives |
| --- | ---: | ---: | --- |
| P0 tip | +0.20 | +0.01 | EXPANDING + **NEAR** (Leak prior) |
| **BUY∧near_atr** | +0.20 | **+0.24** | EXPANDING · less NEAR |
| v1b HOLD | +0.20 | **+0.35** | EXPANDING |
| P0 YTD (post-latch) | +0.20 | +0.01 | BELOW cluster mid-path then NEAR |

CSV paths: `blotter/archive/DE40-AOS-P3/health_path_*.csv`.

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
InpAOS_Leak=9.8                  # prior metadata until deals
InpAOS_W250=50                   # expansion floor (not 250)
# L2det BUY∧near_atr: shadow ledger or future L2det_de40 include
```

Magic: keep engine **26101902**; OS experiment magic **26141907** at P7.

---

## 7. Verdict

| Item | Status |
| --- | --- |
| P3-T01 L3 policy | **SIGNED** for shadow · tip trip-free · YTD BELOW works |
| P3-T02 monitors | **SIGNED** |
| P3-T03 L4 W15/W20 | **SIGNED** · paths archived |
| P3-T04 bus | **SIGNED** |
| Live / LIVE_WITHHOLD | **NOT** armed |

**One-line:** Tip Balanced + BUY∧near_atr stays inside L3 with MaxDD ~3% and no BELOW; YTD Feb still trips BELOW (correct) — keep L3 latched research policy and do not lift ATR max to chase frequency.
