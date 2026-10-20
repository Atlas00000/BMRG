# AAPL M5 — L3 / L4 policy (P3)

**Version:** 1.0.0  
**Tasks:** AAPL-M5-AOS-P3-T01 … T04  
**Date:** 2026-10-20  
**Evidence:** `blotter/archive/AAPL-M5-AOS-P3/P3_L3L4.json` · `health_path_*.csv`  
**Upstream:** [`aos_l2_policy_M5.md`](./aos_l2_policy_M5.md) v1b · [`aos_l2_size_table_M5.md`](./aos_l2_size_table_M5.md)  
**Mode:** **SHADOW / research OS** — not live attach · no M15 L3 pin reuse

L3 **outranks** L2det / L4 size. L2det skips still apply first on the fire; L3/L4 operate on the **remaining** path.

---

## 1. Bindings (Apple M5 expansion)

| Parameter | Value | Note |
| --- | ---: | --- |
| `InpAOS_DD_Limit` | **25%** | MaxDD from peak |
| Derisk | **20%** (0.8× DD) | f ≤ 0.5 |
| `InpEquityHaltPct` | **15%** | EA halt from start equity (monitor) |
| `InpAOS_BWR` / `R` / Leak | 40.4% / ≈1.47 / **15.3 pp profile** | Leak_source=profile until deals |
| Health windows | **W15 / W20 / W50** | Tip n=77 — W15/W20 first-class |
| `InpAOS_W250` when wiring | **50** (EA min) | Research OS `.set` |
| Baseline fires / 90d | **42** | Tip pace ~42/90d · FREQUENCY_STALL if 90d-equiv &lt; 21 |
| Baseline tip E_N | **+0.157R** | EXPANDING threshold |
| L2 overlay | **v1b** `Jul ∨ Wed` | Jul-only = cleaner L3 path (see §2) |

**EF note:** Lifecycle EF uses **Leak profile 15.3 pp**. Tip W15 often **NEAR** even when E_N>0 (Apple CFD spread tax). Do not “fix” by swapping preset meta Leak 2.1 pp for L3 decisions.

---

## 2. P3-T01 — L3 halt / derisk

| Trigger | Action | f |
| --- | --- | ---: |
| `dd_peak ≥ 25%` | `HALT_MAXDD` | 0 |
| `dd_peak ≥ 20%` | `DERISK_0.8_DD` | ≤0.5 |
| Lifecycle **BELOW** (W20 E_N≤0 **and** W15 EF_profile≤0) | `HALT_f0_BELOW_FRONTIER` | 0 |
| Kill-switch | hard OFF | 0 |

**Unlatch (expansion research):** after `HALT_f0_BELOW_FRONTIER`, clear latch only when **W20 E_N > 0 for 2 consecutive evals** and dd_peak &lt; 20%. Offline sim below **latches forever** (conservative) — bus `L3_HALT` tick counts are post-latch inflated; trip_count is the authority for “did L3 fire.”

### Offline sim

| Path | n | MaxDD | L3 trips | Trip note | End life / EN20 |
| --- | ---: | ---: | ---: | --- | --- |
| P0 tip | 77 | 7.9% | **1** BELOW | Jul stress cluster | NEAR / +0.24 (latched) |
| **v1b kept** | 44 | **2.6%** | **1** BELOW | Fewer BELOW ticks 18→4 | BELOW / ≈0 |
| Jul-only kept | 62 | 2.6% | **0** | Jul cell = L3 driver | **NEAR / +0.24** |
| Jul∨H18 HOLD | 49 | 2.2% | **0** | HOLD map (May FP risk) | NEAR / +0.11 |
| P0 YTD | 145 | 13.4% | **1** BELOW | H1 early | NEAR / +0.24 (latched) |
| v1b YTD | 95 | 6.9% | **1** BELOW | H1 still trips (v1b ≠ H1 map) | BELOW / ≈0 |

**Read:** Tip **needs** L3 BELOW halt on the raw engine (Jul cluster). **v1b** cuts MaxDD hard and shrinks BELOW life ticks but does **not** eliminate the tip trip. **Jul-only** clears tip L3 trips — keep as nested ARM / optional tighter stack; v1b remains P2 preferred for tip E_N CF. MaxDD never approaches 25% at lot 1.0 / $500 on tip. YTD H1 hole requires L3 (and optional H1 L2det later) regardless of v1b.

---

## 3. P3-T02 — monitors (warn / investigate)

| Monitor | Condition | Bus |
| --- | --- | --- |
| Cost drift | rolling med20 entry spread ≫ 29+5 pts | INVESTIGATE (journal only · tip spreads tight) |
| FREQUENCY_STALL | 90d-equiv fires &lt; 50% of **42** | **WARN** only — do not lift ATR/BBw |
| Loss streak ≥ 3 | engine pause align | STREAK_WARN |
| Loss streak ≥ 5 | escalate | STREAK_WATCH → INVESTIGATE |

### Sim monitors

| Path | max loss streak | FREQUENCY_STALL ticks | Cost drift |
| --- | ---: | ---: | ---: |
| P0 tip | **8** | 6 | 0 |
| **v1b tip** | **4** | 12 | 0 |
| Jul-only | 4 | 12 | 0 |
| P0 YTD | **10** | 6 | 0 |
| v1b YTD | 7 | 12 | 0 |

Stall ticks after L2det are **expected** (57% retention) — not a reason to widen ATR/BBw. Streak 8 on P0 aligns with engine `InpMaxLossStreak=3` pause (L3 STREAK_WATCH escalates, does not replace).

---

## 4. P3-T03 — L4 rolling health

| Window | Role |
| --- | --- |
| W15 | Fast lifecycle / EF_profile |
| W20 | Confirm BELOW / Expanding |
| **W50** | Dense-TF confirm when n allows (tip n=77 borderline) |
| W100/W250 | Adopt when n grows |

### Lifecycle → f (armed with L4 size)

| State | Rule (Apple M5 expansion) | f_mult |
| --- | --- | ---: |
| WARMUP | n_window &lt; 15 | 1.0 |
| EXPANDING | W15 E_N > baseline tip E_N (+0.157) and not falling | 1.0 |
| STABLE | W15 E_N ≥ 0 | 1.0 |
| COMPRESSING | W15 E_N falling **2** consecutive evals | 0.5 |
| NEAR | W15 EF_profile ≤ 1 pp **or** W15 E_N &lt; 0 | 0.25 |
| BELOW | W20 E_N ≤ 0 **and** W15 EF_profile ≤ 0 | 0.0 → L3 halt |

### End-of-window health (sim · post-path)

| Path | last W15 E_N | last W20 E_N | last W50 E_N | Dominant lives |
| --- | ---: | ---: | ---: | --- |
| P0 tip | +0.15 | +0.24 | +0.09 | NEAR heavy · BELOW mid |
| **v1b tip** | ≈0 | ≈0 | — | EXPANDING ↑ · BELOW ↓ · latched end |
| Jul-only | +0.15 | **+0.24** | +0.24 | NEAR · **0 BELOW** |
| P0 YTD | +0.15 | +0.24 | +0.09 | H1 BELOW cluster then recover |

CSV paths: `blotter/archive/AAPL-M5-AOS-P3/health_path_*.csv`.

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

## 6. Sign-off

| Item | Status |
| --- | --- |
| P3-T01…T04 | **SIGNED** 2026-10-20 |
| L3 needed on tip P0 | **Yes** (1 BELOW) |
| v1b improves MaxDD / BELOW ticks | **Yes** · trip remains |
| Jul-only clears tip L3 | **Yes** — optional tighter nest |
| Next | **P4** ledger + det stack + L8 |

**One-line:** Freeze DD25 / derisk20 / W15·W20·W50 / Leak 15.3 profile; tip needs L3 BELOW; v1b Jul∨Wed shrinks DD and BELOW mass; Jul-only is the cleanest L3 path — wire L3/L4 bus in P4 stack without retuning geometry.
