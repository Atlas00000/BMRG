# USDJPY — L3 / L4 policy (P3)

**Version:** 1.0.0  
**Tasks:** USDJPY-AOS-P3-T01 … T04  
**Date:** 2026-10-19  
**Evidence:** `blotter/archive/USDJPY-AOS-P3/P3_L3L4.json` · `health_path_*.csv`  
**Upstream:** [`aos_l2_policy.md`](./aos_l2_policy.md) · [`aos_l2_size_table.md`](./aos_l2_size_table.md)  
**Mode:** **SHADOW / research OS** — not live attach · not FX book replace

L3 **outranks** L2det / L4 size. L2det skips still apply first on the fire; L3/L4 operate on the **remaining** path.

---

## 1. Bindings (USDJPY M15 expansion)

| Parameter | Value | Note |
| --- | ---: | --- |
| `InpAOS_DD_Limit` | **25%** | Preset · MaxDD from peak |
| Derisk | **20%** (0.8× DD) | f ≤ 0.5 |
| `InpEquityHaltPct` | **15%** | EA halt from start equity (monitor) |
| `InpAOS_BWR` / `R` / Leak | **45.5%** / **1.20** / **11.4 pp prior** | Leak_source=prior until deals |
| Health windows | **W15 / W20** | Expansion main |
| W50 | optional when wiring | tip n=46 can start W50 late-path |
| `InpAOS_W250` when wiring | **50** (EA floor) | Preset 250 never arms on tip n~46 |
| Baseline tip E_N | **+0.10R** | path tip (P1/P2) |
| Baseline fires / 90d | **42** | FREQUENCY_STALL if 90d-equiv &lt; 21 |
| L2 overlay | **v1c = near_atr∨H16** ARM | near_atr slim · Jul HOLD |
| Tip max L streak | **7** (dedicated) / **9** (path P0 sim) | STREAK_WATCH ≥5 |

**EF note:** Lifecycle EF uses **Leak prior 11.4 pp**. That makes tip W15 often **NEAR** even when E_N>0 (costs_fragile). Do not “fix” by swapping in journal proxy (~3.6 pp) for L3 decisions.

**PnL note:** Equity path uses `lot × SL$ × pnl_R_design` proxy — not deal blotter. MaxDD ranks paths; absolute $ is approximate.

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
| P0 tip | 46 | 4.9% | **1** BELOW | EN20=−0.01 · EF15=−23.5 · latch → BELOW cluster · streak 9 |
| near_atr kept | 39 | 3.2% | **1** BELOW | Same early hole · last still BELOW |
| **v1c kept** | **37** | **2.2%** | **0** | No MaxDD / no BELOW · last EN20 **+0.21** |
| Jul HOLD kept | 32 | 1.4% | **0** | Cleanest DD · freq stall ticks |
| P0 YTD | 54 | 4.9% | **1** BELOW | Same trip family |
| near_atr YTD | 44 | 3.1% | **1** BELOW | Overlay alone insufficient |
| **v1c YTD** | **41** | **2.2%** | **0** | Trip-free on support window |

**Read:** L2det **v1c prevents** the P0 below-frontier trip on tip and YTD (same pattern as EURUSD v1b). Slim near_atr alone does **not**. MaxDD never approaches 25% at research lots / $500. Keep L3 latched policy — do not disable BELOW because tip looks soft under Leak prior.

---

## 3. P3-T02 — monitors (warn / investigate)

| Monitor | Condition | Bus |
| --- | --- | --- |
| Cost drift | rolling median entry spread ≫ tip journal median+8 | INVESTIGATE (journal only) |
| FREQUENCY_STALL | 90d-equiv fires &lt; 50% of 42 | **WARN** only — do not lift ATR max / reopen Tokyo |
| Loss streak ≥ 3 | engine pause align | STREAK_WARN |
| Loss streak ≥ 5 | escalate | STREAK_WATCH → INVESTIGATE |

### Sim monitors

| Path | max loss streak | FREQUENCY_STALL ticks | Notes |
| --- | ---: | ---: | --- |
| P0 tip | **9** | 0 (then HALT latch) | Needs streak watch |
| near_atr tip | 6 | 0 | Still BELOW trip |
| **v1c tip** | **4** | 0 | Streak contained · DERISK from NEAR (Leak prior) |
| Jul HOLD tip | 3 | **4** | Expected skip retention |
| v1c YTD | 4 | 0 | Trip-free |

Stall warns after Jul-skip are **expected** — not a reason to widen ATR max or session. NEAR/DERISK bus under Leak prior is structural until measured Leak — not a geometry cue.

---

## 4. P3-T03 — L4 rolling health

| Window | Role |
| --- | --- |
| W15 | Fast lifecycle / EF_prior |
| W20 | Confirm BELOW / Expanding |
| W50 | Optional late tip / when wiring |
| W100/W250 | Adopt when n allows |

### Lifecycle → f (armed with L4 size)

| State | Rule (USDJPY M15 expansion) | f_mult |
| --- | --- | ---: |
| WARMUP | n_window &lt; 15 | 1.0 |
| EXPANDING | W15 E_N > baseline tip E_N (+0.10) and not falling | 1.0 |
| STABLE | W15 E_N ≥ 0 | 1.0 |
| COMPRESSING | W15 E_N falling **2** consecutive evals | 0.5 |
| NEAR | W15 EF_prior ≤ 1 pp **or** W15 E_N &lt; 0 | 0.25 |
| BELOW | W20 E_N ≤ 0 **and** W15 EF_prior ≤ 0 | 0.0 → L3 halt |

### End-of-window health (sim)

| Path | last W15 E_N | last W20 E_N | Dominant lives |
| --- | ---: | ---: | --- |
| P0 tip | −0.12 | −0.23 | BELOW latch mid-path |
| near_atr | +0.03 | −0.01 | still BELOW end |
| **v1c** | **+0.17** | **+0.21** | EXPANDING + **NEAR** (Leak prior) · no BELOW |
| Jul HOLD | +0.32 | +0.43 | EXPANDING |
| v1c YTD | +0.17 | +0.21 | NEAR end · no BELOW |

CSV paths: `blotter/archive/USDJPY-AOS-P3/health_path_*.csv`.

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
InpAiOsMode=0                    # L2 AI still OFF / SHADOW
InpAOS_L2AI_Enable=false
InpAOS_DD_Limit=25
InpAOS_BWR=45.5
InpAOS_R=1.20
InpAOS_Leak=11.4                 # prior metadata until deals
InpAOS_W250=50                   # expansion floor (not 250)
# L2det v1c near_atr∨H16: shadow ledger or future L2det_usdjpy include
```

Magic: keep engine **26101828**; OS experiment magic **26131807** at P7.

---

## 7. Verdict

| Item | Status |
| --- | --- |
| P3-T01 L3 policy | **SIGNED** for shadow · **v1c tip+YTD trip-free** · P0 BELOW works |
| P3-T02 monitors | **SIGNED** |
| P3-T03 L4 W15/W20 | **SIGNED** · paths archived |
| P3-T04 bus | **SIGNED** |
| Live / LIVE_WITHHOLD | **NOT** armed |

**One-line:** Tip Balanced + **v1c** stays inside L3 with MaxDD ~2.2% and **no BELOW**; P0 alone (and near_atr alone) still trip BELOW under Leak prior — keep L3 latched and do not lift ATR max / reopen Tokyo to chase frequency.
