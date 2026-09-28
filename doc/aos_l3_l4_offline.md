# AOS L3 Guardrails + L4 Observer (offline v0)

**Phase:** AOS-P3  
**Mode:** Offline only (live EA hooks still deferred)  
**Engine:** Harvest 8210204 · labels `AOS-P2-T03/harvest_long_labeled.csv`  
**Baseline:** `AOS_BASELINE_v1` (EF 1.77 long)  
**DD_limit:** **25%** account equity (framework); EA `EquityHaltPct=15` is tighter OK

L3 **commands**. L4 **recommends**. L2 cannot override L3.

---

## 1. L3 Guardrail policy (AOS-P3-T01 / T02)

| Guard ID | Trigger | Action | Override? |
| --- | --- | --- | --- |
| `DERISK_0.8_DD` | Account MaxDD ≥ **0.8 × DD_limit** (20% if limit 25%) | Halve f (or ×0.5 on size modulator) | No |
| `HALT_MAXDD` | Account MaxDD ≥ **DD_limit** (25%) | Halt new entries | No |
| `HALT_f0_BELOW_FRONTIER` | W250 **E_N ≤ 0** | f = 0 | No |
| `WARN_FREQUENCY_STALL` | 90d fires &lt; 50% of baseline_90d | Warn; do not auto-widen L2 | L2 change only via AOS task |
| `WARN_COST_DRIFT` | Leak proxy &gt; baseline Leak + 1.5 pp sustained W250 | Warn → halt if EF≤0 | No |
| `KILL_SWITCH` | Manual / OS supervisor | Flat + disable | No |

**Invariant:** If L3 says halt, L2 skip/fire and L4 advise are ignored for new risk.

### Offline dry-run notes (R-path proxy — diagnostic)

Unit R equity path (±1R per TP/SL) is **not** identical to $400 account MaxDD%. It overstates early %DD. Use it to test **trip wiring**, not to claim live DD%.

Observed on Harvest labels:

| Finding | Detail |
| --- | --- |
| Peak unit-R | +48R · max excursion from peak **21R** |
| Mid-sample stress | W250 spent time in **Below / Near frontier** (late-2025 → early-2026) |
| Simulated L3 | Multiple `HALT_MAXDD` (R-proxy) + `HALT_f0_BELOW_FRONTIER` when E_N≤0 |
| End state | W250 EF **4.2** Fragile · lifecycle **Compressing** · f_rec **0.5** · L3 **NONE** |

Artifact: `blotter/archive/AOS-P3-T01/L3_trips_simulated.csv`

---

## 2. L3 FREQUENCY_STALL + cost (AOS-P3-T02)

| Metric | Offline Harvest | Bar |
| --- | ---: | --- |
| `fire_90d` (to last tape day) | **59** | |
| `baseline_90d` (provisional) | ~75 | from long density |
| Stall? | **false** (59 ≥ 37.5) | warn if &lt;50% |
| Leak | 2.2 pp proxy | cost-drift warn if +1.5 pp |

---

## 3. L4 Rolling health (AOS-P3-T03)

### Terminal windows (last events)

| Window | n | WR | E_N | EF | M | Zone |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| W100 | 100 | 61.0 | 0.220 | **8.8** | 9.56 | Fragile |
| W250 | 250 | 56.4 | 0.128 | **4.2** | 6.15 | Fragile |
| W500 | 500 | 53.6 | 0.072 | **1.4** | 4.37 | Fragile |

vs `AOS_BASELINE` long EF 1.77: terminal W250 **holds** (4.2 ≥ 0.77 loose floor).

ΔD proxy: EF(W250_now) − EF(W250 lagged 25 events) — see lifecycle CSV.

Artifact: `blotter/archive/AOS-P3-T03/rolling_W250_lifecycle.csv`

### Lifecycle label rules (v0)

| Label | Rule |
| --- | --- |
| Below frontier | W250 E_N ≤ 0 |
| Near frontier | W250 EF ≤ 0 (and E_N &gt; 0) |
| Compressing | Fragile zone or ΔEF ≤ −1 pp |
| Expanding | Robust zone or ΔEF ≥ +1 pp |
| Stable | else |

---

## 4. Recommend bus (AOS-P3-T04)

```text
L4.lifecycle → L2.f_rec (advisory)
  Expanding      → 1.00
  Stable         → 0.75
  Compressing    → 0.50
  Near frontier  → 0.25
  Below frontier → 0.00

L4.Below frontier → L3.HALT_f0_BELOW_FRONTIER (command)
L3.HALT_* always wins over L2.f_rec and L2.skip
```

**Accept check:** every Below-frontier row in offline CSV has `f_rec=0` and `L3` containing halt or was superseded by MaxDD halt — **PASS** on sampled stress period.

Current terminal recommend: **Compressing → f_rec 0.5** (not halted).

---

## 5. Task verdicts

| Task | Verdict |
| --- | --- |
| P3-T01 MaxDD / kill | **ACCEPT** offline policy + simulated trips |
| P3-T02 stall / cost | **ACCEPT** · fire90=59 · no stall |
| P3-T03 rolling health | **ACCEPT** · W100/250/500 published |
| P3-T04 recommend bus | **ACCEPT** · Below→f=0 locked |

Live wiring of L3 into EA = later (with AOS-P1-T03). Offline OS stack may proceed to **AOS-P4** training.
