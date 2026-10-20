# JP225 / JPN225 M5 — L3 / L4 policy (P3)

**Version:** 1.0.0  
**Tasks:** JP225-M5-AOS-P3-T01 … T04  
**Date:** 2026-10-20  
**Evidence:** `blotter/archive/JP225-M5-AOS-P3/P3_L3L4.json` · `health_path_*.csv`  
**Upstream:** [`aos_l2_policy_M5.md`](./aos_l2_policy_M5.md) v1c · [`aos_l2_size_table_M5.md`](./aos_l2_size_table_M5.md)  
**Mode:** **SHADOW / research OS** — not live attach · no M15 L3 pin reuse

L3 **outranks** L2det / L4 size. L2det skips still apply first on the fire; L3/L4 operate on the **remaining** path.

---

## 1. Bindings (JP225 M5 expansion)

| Parameter | Value | Note |
| --- | ---: | --- |
| `InpAOS_DD_Limit` | **25%** | MaxDD from peak |
| Derisk | **20%** (0.8× DD) | f ≤ 0.5 |
| `InpEquityHaltPct` | **15%** | EA halt from start equity (monitor) |
| `InpAOS_BWR` / `R` / Leak | **33.3%** / **2.00** / **3.3 pp prior** | Leak_source=prior until deals |
| Health windows | **W15 / W20 / W50** | Tip n=94 — W15/W20 first-class |
| `InpAOS_W250` when wiring | **50** (EA min) | Research OS `.set` |
| Baseline fires / 90d | **50** | Tip pace ~51/90d · FREQUENCY_STALL if 90d-equiv &lt; 25 |
| Baseline tip E_N | **+0.245R** | EXPANDING threshold |
| L2 overlay | **v1c** `(BUY∧MATCH)∨(BUY∧H09\|13\|16)` | |

**EF note:** Lifecycle EF uses **Leak prior 3.3 pp**. Do not “fix” by swapping journal proxy for L3 decisions.

---

## 2. P3-T01 — L3 halt / derisk

| Trigger | Action | f |
| --- | --- | ---: |
| `dd_peak ≥ 25%` | `HALT_MAXDD` | 0 |
| `dd_peak ≥ 20%` | `DERISK_0.8_DD` | ≤0.5 |
| Lifecycle **BELOW** (W20 E_N≤0 **and** W15 EF_prior≤0) | `HALT_f0_BELOW_FRONTIER` | 0 |
| Kill-switch | hard OFF | 0 |

**Unlatch (expansion research):** after `HALT_f0_BELOW_FRONTIER`, clear latch only when **W20 E_N > 0 for 2 consecutive evals** and dd_peak &lt; 20%. Offline sim below **latches forever** (conservative) — bus `L3_HALT` tick counts are post-latch inflated; **trip_count** is the authority for “did L3 fire.”

### Offline sim

| Path | n | MaxDD | L3 trips | Trip time | Notes |
| --- | ---: | ---: | ---: | --- | --- |
| P0 tip | 94 | 3.4% | **1** BELOW | **2026-09-02** | MATCH tax cluster · last life **EXPANDING** (post-path recover) |
| **v1c kept** | **69** | **1.3%** | **0** | — | **No tip trip** · last **EXPANDING** · EN50 **+0.50** |
| BUY∧MATCH kept | 78 | 1.6% | **0** | — | Safer nested leg · last STABLE |
| MATCH-all kept | 60 | 1.6% | 0 | — | SELL FP · not preferred |
| P0 YTD | 130 | 3.6% | **1** BELOW | **2026-03-18** | Feb/Apr prior hole |
| v1c YTD | 102 | 3.0% | **1** BELOW | same Mar | v1c not a prior-month fix |

**Read:** Tip **needs** L3 on raw P0 (Sep MATCH BELOW). **v1c eliminates the tip BELOW trip** and cuts MaxDD 3.4%→1.3%. YTD Mar trip remains — L3 still required for prior soft months. MaxDD never approaches 25% at 0.1 lot / $500.

---

## 3. P3-T02 — monitors (warn / investigate)

| Monitor | Condition | Bus |
| --- | --- | --- |
| Cost drift | rolling med20 entry spread ≫ 1400+500 pts | INVESTIGATE (journal only) |
| FREQUENCY_STALL | 90d-equiv fires &lt; 50% of **50** | **WARN** only — do not lift ATR band |
| Loss streak ≥ 3 | engine pause align | STREAK_WARN |
| Loss streak ≥ 5 | escalate | STREAK_WATCH → INVESTIGATE |

### Sim monitors

| Path | max loss streak | FREQUENCY_STALL ticks | Cost drift |
| --- | ---: | ---: | ---: |
| P0 tip | **6** | 8 | 0 |
| **v1c tip** | **4** | 15 | 0 |
| BUY∧MATCH | 5 | 15 | 0 |
| P0 / v1c YTD | 6 | 11 / 19 | 0 |

Stall ticks after L2det are **expected** (ret ~73%) — not a reason to widen ATR band or session. Streak 4–6 aligns with engine `InpMaxLossStreak=3` pause.

---

## 4. P3-T03 — L4 rolling health

| Window | Role |
| --- | --- |
| W15 | Fast lifecycle / EF_prior |
| W20 | Confirm BELOW / Expanding |
| **W50** | Confirm when n allows (tip 94 · v1c 69) |
| W100/W250 | Adopt when n allows |

### Lifecycle → f (armed with L4 size)

| State | Rule (JP225 M5 expansion) | f_mult |
| --- | --- | ---: |
| WARMUP | n_window &lt; 15 | 1.0 |
| EXPANDING | W15 E_N > baseline tip E_N (+0.245) and not falling | 1.0 |
| STABLE | W15 E_N ≥ 0 | 1.0 |
| COMPRESSING | W15 E_N falling **2** consecutive evals | 0.5 |
| NEAR | W15 EF_prior ≤ 1 pp **or** W15 E_N &lt; 0 | 0.25 |
| BELOW | W20 E_N ≤ 0 **and** W15 EF_prior ≤ 0 | 0.0 → L3 halt |

### End-of-window health (sim · post-path)

| Path | last W15 E_N | last W20 E_N | last W50 E_N | Dominant lives |
| --- | ---: | ---: | ---: | --- |
| P0 tip | +0.40 | +0.20 | +0.08 | EXPANDING · STABLE · **BELOW mid** (latched) |
| **v1c tip** | **+0.40** | **+0.20** | **+0.50** | EXPANDING · STABLE · **no BELOW** |
| P0 YTD | +0.40 | +0.20 | +0.08 | Mar BELOW then recover |

CSV paths: `blotter/archive/JP225-M5-AOS-P3/health_path_*.csv`.

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
| L2det v1c WOULD_SKIP | skip fire — **not** an L3 trip |

---

## 6. Explicit non-claims

- Not live capital · not M15 JPN225stack L3 thresholds as sole authority without M5 sim.  
- Journal Leak proxy is not L3 EF authority.  
- Forever-latch sim overstates bus HALT ticks — use **trip_count** + unlatch rule when wiring.  
- v1c is not a Feb/Apr fix — YTD still needs L3.

---

## 7. Status

**SIGNED** for research OS shadow — proceed P4 ledger/stack with v1c + these L3/L4 bindings.
