# AUDUSD M15 — L3 / L4 policy (P3)

**Version:** 1.0.0  
**Tasks:** AUDUSD-AOS-P3-T01 … T04  
**Date:** 2026-10-19  
**Evidence:** `blotter/archive/AUDUSD-AOS-P3/P3_L3L4.json` · `health_path_*.csv`  
**Upstream:** [`aos_l2_policy.md`](./aos_l2_policy.md) v1 BUY∧May · [`aos_l2_size_table.md`](./aos_l2_size_table.md)  
**Mode:** **SHADOW / research OS** — not live attach · not M5 SCALE **8230931** replace

L3 **outranks** L2det / L4 size. L2det skips still apply first on the fire; L3/L4 operate on the **remaining** path.

---

## 1. Bindings (AUDUSD M15 expansion)

| Parameter | Value | Note |
| --- | ---: | --- |
| `InpAOS_DD_Limit` | **25%** | MaxDD from peak |
| Derisk | **20%** (0.8× DD) | f ≤ 0.5 |
| `InpEquityHaltPct` | **15%** | EA halt from start equity (monitor) |
| `InpAOS_BWR` / `R` / Leak | **50%** / **1.0** / **5.0 pp** proxy | Leak_source=journal until deals+swap |
| Deposit (sim) | **$400** | Matches Tester baseline |
| Health windows | **W15 / W20** | Expansion main (thin fire rate) |
| `InpAOS_W250` when wiring | **50** (EA floor) | Preset 250 never arms on tip n~41; live Track B keeps W250 |
| Baseline tip E_N | **+0.268R** | Expanding threshold |
| Baseline fires / 90d | **30** | FREQUENCY_STALL if 90d-equiv &lt; 15 |
| Spread median tip | **15** pts | Cost drift if &gt;19 |
| Overnight | **~59%** tip nights_held | MaxDD path includes multi-session inventory |

---

## 2. P3-T01 — L3 halt / derisk (overnight-aware)

| Trigger | Action | f |
| --- | --- | ---: |
| `dd_peak ≥ 25%` | `HALT_MAXDD` | 0 |
| `dd_peak ≥ 20%` | `DERISK_0.8_DD` | ≤0.5 |
| Lifecycle **BELOW** (W20 E_N≤0 **and** W15 EF_proxy≤0) | `HALT_f0_BELOW_FRONTIER` | 0 |
| Kill-switch | hard OFF | 0 |
| Overnight cluster (consecutive nights_held) | **note only** → L8 (P4) | — |

**Unlatch (expansion research):** after `HALT_f0_BELOW_FRONTIER`, clear latch only when **W20 E_N > 0 for 2 consecutive evals** and dd_peak &lt; 20%.

### Offline sim

| Path | n | MaxDD | L3 trips | Notes |
| --- | ---: | ---: | ---: | --- |
| P0 tip (no L2det) | 41 | 4.4% | **1** `BELOW` @ EN20=0 · EF15=−8.3 | Halt latches → post-trip HALT bus |
| **v1 BUY∧May kept** | 39 | **3.7%** | **0** | No MaxDD / no BELOW |
| alt BUY∧Thu kept | 36 | 2.9% | **0** | Clean alt |
| P0 long (diagnostic) | 95 | 6.5% | **1** BELOW | Feb/Mar soft — expected |
| v1 long kept (diag) | 93 | 6.5% | **1** BELOW | May filter does not clear pre-tip stress |

**Read:** L2det v1 **prevents** the tip below-frontier trip. MaxDD never approaches 25% at 0.01-lot proxy / $400. Long BELOW remains a **survival** signal for L3/L5 — not a reason to blanket-arm Feb/Mar. Overnight cluster max **7** on tip — feed L8 in P4; do not auto-halt on cluster alone.

---

## 3. P3-T02 — monitors (warn / investigate)

| Monitor | Condition | Bus |
| --- | --- | --- |
| Cost drift | entry spread ≫ tip median **15** (flag if &gt;19) or Leak_proxy↑ &gt; +2 pp | COST_DRIFT_WARN / INVESTIGATE |
| FREQUENCY_STALL | 90d-equiv fires &lt; 50% of 30 | **WARN** only — do not lift ATR max / drop CD / re-enable MonTue |
| Loss streak ≥ 3 | engine pause align | STREAK_WARN |
| Loss streak ≥ 5 | escalate | STREAK_WATCH → INVESTIGATE |
| Overnight cluster | consecutive nights_held without day-close recovery | note for measured swap / L8 (P4) |

### Sim monitors

| Path | max L | max overnight cluster | FREQ_STALL | cost drift |
| --- | ---: | ---: | ---: | --- |
| P0 tip | 4 | 7 | 0 (then HALT latch) | 0 |
| **v1** | **3** | 7 | **0** | 0 |
| BUY∧Thu alt | 3 | 6 | 0 | 0 |
| P0 long | **7** | 7 | 0 (HALT latch) | 0 |

v1 retention is high (~95%) so FREQUENCY_STALL does **not** fire on tip — unlike thinner EUR stacks. Long max-L **7** justifies streak-aware L3 alignment with engine pause.

---

## 4. P3-T03 — L4 rolling health

| Window | Role |
| --- | --- |
| W15 | Fast lifecycle / EF_proxy |
| W20 | Confirm BELOW / Expanding |
| W50 | Use when `InpAOS_W250=50` wired |
| W100/W250 | Adopt when n allows · live Track B already W250 |

### Lifecycle → f (armed with L4 size)

| State | Rule (AUDUSD M15 expansion) | f_mult |
| --- | --- | ---: |
| WARMUP | n_window &lt; 15 | 1.0 |
| EXPANDING | W15 E_N > baseline tip E_N (+0.268) and not falling | 1.0 |
| STABLE | W15 E_N ≥ 0 | 1.0 |
| COMPRESSING | W15 E_N falling **2** consecutive evals | 0.5 |
| NEAR | W15 EF_proxy ≤ 1 pp **or** W15 E_N &lt; 0 | 0.25 |
| BELOW | W20 E_N ≤ 0 **and** W15 EF_proxy ≤ 0 | 0.0 → L3 halt |

### End-of-tip health (sim)

| Path | last W15 E_N | last W20 E_N | Dominant lives |
| --- | ---: | ---: | --- |
| P0 | +0.33 | +0.50 | EXPANDING + mid-path **BELOW** latch |
| **v1** | **+0.33** | **+0.50** | **EXPANDING/STABLE** · 1 COMPRESSING · no BELOW |
| BUY∧Thu | +0.33 | +0.50 | EXPANDING/STABLE · no BELOW |

CSV paths: `blotter/archive/AUDUSD-AOS-P3/health_path_*.csv`.

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
InpAOS_DD_Limit=25
InpAOS_BWR=50
InpAOS_R=1.0
InpAOS_Leak=5.0                  # journal proxy metadata (not measured)
InpAOS_W250=50                   # expansion floor (not 250; not live Track B)
# L2det BUY∧May: Include/AOS_L2det_aud.mqh · InpAOS_AUD_L2detEnable
```

Magic: keep engine **8230901**; research OS **8231941** (P4 `.set`). Never collide with live **8230931**.

---

## 7. Verdict

| Item | Status |
| --- | --- |
| P3-T01 L3 policy | **SIGNED** for shadow · v1 tip trip-free |
| P3-T02 monitors | **SIGNED** |
| P3-T03 L4 W15/W20 | **SIGNED** · paths archived |
| P3-T04 bus | **SIGNED** |
| Live / LIVE_WITHHOLD | **NOT** armed |
| Measured Leak + swap | **OPEN** — do not promote P7 on proxy alone |
| Long BELOW / max-L 7 | **Diagnostic** — L5/regime, not tip reject of v1 |
