# DE40 M5 — L3 / L4 policy (P3)

**Version:** 1.0.0  
**Tasks:** DE40-M5-AOS-P3-T01 … T04  
**Date:** 2026-10-20  
**Evidence:** `blotter/archive/DE40-M5-AOS-P3/P3_L3L4.json` · `health_path_*.csv`  
**Upstream:** [`aos_l2_policy_M5.md`](./aos_l2_policy_M5.md) v1b · [`aos_l2_size_table_M5.md`](./aos_l2_size_table_M5.md)  
**Mode:** **SHADOW / research OS** — not live attach · no M15 L3 pin reuse

L3 **outranks** L2det / L4 size. L2det skips still apply first on the fire; L3/L4 operate on the **remaining** path.

---

## 1. Bindings (DE40 M5 expansion)

| Parameter | Value | Note |
| --- | ---: | --- |
| `InpAOS_DD_Limit` | **25%** | MaxDD from peak |
| Derisk | **20%** (0.8× DD) | f ≤ 0.5 |
| `InpEquityHaltPct` | **15%** | EA halt from start equity (monitor) |
| `InpAOS_BWR` / `R` / Leak | 44.4% / 1.25 / **7.0 pp prior** | Leak_source=prior until deals |
| Health windows | **W15 / W20 / W50** | Dense M5 — W20/W50 first-class |
| `InpAOS_W250` when wiring | **50** (EA min) | Research OS `.set` |
| Baseline fires / 90d | **65** | Tip pace ~67/90d · FREQUENCY_STALL if 90d-equiv &lt; 33 |
| Baseline tip E_N | **+0.207R** | EXPANDING threshold |
| L2 overlay | **v1b** `(BUY∧H14\|16)∨(BUY∧Oct)` | |

**EF note:** Lifecycle EF uses **Leak prior 7.0 pp**. Tip W15 often **NEAR** even when E_N>0 (DE30 spread tax). Do not “fix” by swapping journal proxy (~1.1 pp) for L3 decisions.

---

## 2. P3-T01 — L3 halt / derisk

| Trigger | Action | f |
| --- | --- | ---: |
| `dd_peak ≥ 25%` | `HALT_MAXDD` | 0 |
| `dd_peak ≥ 20%` | `DERISK_0.8_DD` | ≤0.5 |
| Lifecycle **BELOW** (W20 E_N≤0 **and** W15 EF_prior≤0) | `HALT_f0_BELOW_FRONTIER` | 0 |
| Kill-switch | hard OFF | 0 |

**Unlatch (expansion research):** after `HALT_f0_BELOW_FRONTIER`, clear latch only when **W20 E_N > 0 for 2 consecutive evals** and dd_peak &lt; 20%. Offline sim below **latches forever** (conservative) — bus `L3_HALT` tick counts are post-latch inflated; trip_count is the authority for “did L3 fire.”

### Offline sim

| Path | n | MaxDD | L3 trips | Trip time | Notes |
| --- | ---: | ---: | ---: | --- | --- |
| P0 tip | 123 | 10.7% | **1** BELOW | 2026-06-05 | Soft May→Jun · last life **BELOW** · EN20 −0.10 |
| **v1b kept** | 110 | **10.3%** | **1** BELOW | 2026-07-02 | Soft Jun→Jul · last life **NEAR** · EN20 **+0.13** |
| H14\|16 aggressive | 110 | 8.9% | **1** BELOW | same cluster | Cleaner DD · SELL FP risk |
| P0 YTD | 208 | 11.2% | **1** BELOW | **2026-02-19** | Feb path |
| v1b YTD | 187 | 10.2% | **1** BELOW | 2026-02-16 | Feb still trips (v1b not Feb map) |

**Read:** Tip **needs** L3 BELOW halt (May/Jun soft cluster) — v1b does **not** eliminate the tip trip (unlike UK100 M5). It **does** cut BELOW life ticks (11→5) and ends the tip in **NEAR** with positive EN20/EN50 instead of latched BELOW. MaxDD never approaches 25% at 0.1 lot / $500. YTD Feb hole requires L3 regardless of v1b.

---

## 3. P3-T02 — monitors (warn / investigate)

| Monitor | Condition | Bus |
| --- | --- | --- |
| Cost drift | rolling med20 entry spread ≫ 84+40 pts | INVESTIGATE (journal only) |
| FREQUENCY_STALL | 90d-equiv fires &lt; 50% of **65** | **WARN** only — do not lift ATR max |
| Loss streak ≥ 3 | engine pause align | STREAK_WARN |
| Loss streak ≥ 5 | escalate | STREAK_WATCH → INVESTIGATE |

### Sim monitors

| Path | max loss streak | FREQUENCY_STALL ticks | Cost drift |
| --- | ---: | ---: | ---: |
| P0 tip | **7** | 10 | 0 |
| **v1b tip** | **7** | 10 | 0 |
| H14\|16 aggressive | 6 | 10 | 0 |
| P0 / v1b YTD | 7 | 20 | 0 |

Stall ticks after L2det are **expected** — not a reason to widen ATR max or session. Streak 7 aligns with engine `InpMaxLossStreak=3` pause (L3 STREAK_WATCH is escalate, not replace).

---

## 4. P3-T03 — L4 rolling health

| Window | Role |
| --- | --- |
| W15 | Fast lifecycle / EF_prior |
| W20 | Confirm BELOW / Expanding |
| **W50** | Dense-TF confirm (tip n=123 supports) |
| W100/W250 | Adopt when n allows |

### Lifecycle → f (armed with L4 size)

| State | Rule (DE40 M5 expansion) | f_mult |
| --- | --- | ---: |
| WARMUP | n_window &lt; 15 | 1.0 |
| EXPANDING | W15 E_N > baseline tip E_N (+0.207) and not falling | 1.0 |
| STABLE | W15 E_N ≥ 0 | 1.0 |
| COMPRESSING | W15 E_N falling **2** consecutive evals | 0.5 |
| NEAR | W15 EF_prior ≤ 1 pp **or** W15 E_N &lt; 0 | 0.25 |
| BELOW | W20 E_N ≤ 0 **and** W15 EF_prior ≤ 0 | 0.0 → L3 halt |

### End-of-window health (sim · post-path)

| Path | last W15 E_N | last W20 E_N | last W50 E_N | Dominant lives (pre-latch mix) |
| --- | ---: | ---: | ---: | --- |
| P0 tip | −0.25 | −0.10 | +0.13 | EXPANDING + **NEAR** + BELOW late |
| **v1b tip** | **+0.05** | **+0.13** | **+0.31** | EXPANDING · NEAR · fewer BELOW |
| P0 YTD | −0.25 | +0.01 | +0.13 | Feb BELOW cluster then NEAR |

CSV paths: `blotter/archive/DE40-M5-AOS-P3/health_path_*.csv`.

---

## 5. P3-T04 — L4 → L3 recommend bus

| L4 / monitor state | Bus action |
| --- | --- |
| BELOW | **L3_HALT** (f=0) |
| COMPRESSING | **INVESTIGATE** (regime/execution) · f=0.5 |
| NEAR or DERISK_0.8_DD | **DERISK** f≤0.5 |
| STREAK≥5 | **STREAK_WATCH** |
| FREQUENCY_STALL | **WARN** only |
| EXPANDING / STABLE | **NONE** f=1.0 |
| L2det v1b WOULD_SKIP | skip fire — **not** an L3 trip |

---

## 6. Explicit non-claims

- Not live capital · not M15 DE40stack L3 thresholds as sole authority without M5 sim.  
- Journal Leak proxy is not L3 EF authority.  
- Forever-latch sim overstates bus HALT ticks — use **trip_count** + unlatch rule when wiring.  
- v1b is not a Feb fix — YTD still needs L3.

---

## 7. Status

**SIGNED** for research OS shadow — proceed P4 ledger/stack with v1b + these L3/L4 bindings.
