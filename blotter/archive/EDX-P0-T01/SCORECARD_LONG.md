# EDX-P0-T01 SCORECARD — long window (primary)

**Scored:** 2026-09-25 10:01  
**Preset:** EDX-P0-T01_baseline_G0-EF-G1_EURUSD-M5_long.set  
**Log:** Agent 20260925.log lines ~897711–1161789  

## Contract checks

| Rule | Required | Actual | Pass |
| --- | --- | --- | --- |
| Geometry G0 | MaxLevels=1, MaxEntries=1 | 1 / 1 (level1 opens=0) | YES |
| BBDev / SL / TP | 2.2 / 300 / 450 | match | YES |
| Magic | 8210001 | 8210001 | YES |
| Window | 2025.01.01–2026.09.24 | match | YES |
| Profit mode | Account currency | **still pips** (deposit 400) | **NO** |
| Evidence tier | ≥385 Standard | **n=570 exits** | YES |

Pips mode ⇒ Stage 1 Leak/c_R and Stage 3 wealth path **not admissible** without cost reconstruction. Stage 0 vector below is the **working P0 reference** with `costs_defaulted` / Leak treated as TBD.

## Health vector (G0: ticket ≈ event; R proxy = RR = 1.5)

| Metric | Full sample |
| --- | ---: |
| n opens | 572 |
| n TP+SL | 570 |
| buy / sell opens | 271 / 301 |
| WR | **44.74%** |
| AW | ~+1.5R (TP-dominated; MID=1) |
| AL | ~1.0R |
| R | ~1.5 |
| RR | 1.5 |
| RR−R | ~0 |
| BWR | 40.00% |
| BM | **+4.74 pp** |
| FMI | 4.74/40 ≈ **0.119** |
| Leak | **TBD** (pips; flag costs_defaulted) |
| EF | ≤ BM − Leak → **≤ +4.74 pp** before costs |
| M (95%) | **±4.08 pp** |
| E_N | **+0.118R** |
| PF proxy | **1.21** |
| Final (pips) | 400 → **591.23** (+47.8%) |

### Production-gate zone (gross, Leak=0)

EF ≈ 4.74 pp vs M ≈ 4.08 pp → **barely Robust on gross only**.  
Any realistic Leak ≥ ~0.7 pp → **Fragile**. Treat live verdict as **Fragile pending currency blotter + costs**.

### Rolling windows (calendar proxy)

| Window | TP | SL | WR | E_N proxy |
| --- | ---: | ---: | ---: | ---: |
| 2025 H1 | 109 | 128 | 46.0% | +0.150R |
| 2025 H2 | 63 | 85 | 42.6% | +0.065R |
| 2026 YTD | 83 | 102 | 44.9% | +0.122R |

Lifecycle (provisional): **Stable-to-mild Compressing** into H2; 2026 recovers vs H2. Trade-count W250/ΔD deferred to EDX-P0-T02.

Prior Jul–Sep-only cell (archived earlier): WR 32.5%, Negative — **regime/path cell**, not the long baseline.

## Side diagnosis

**WR-side thin margin** — not R-side.

- Realised R ≈ designed RR (MID share ~0%); AL ≈ 1R, AW ≈ 1.5R.
- Edge exists only because WR sits ~5 pp above BWR; payoff geometry is not the failure mode on this sample.
- Working hypothesis “AL too large compressing R” → **REJECTED** for G0 long baseline (revisit if currency costs show AL > 1R).

## Baseline values to beat (`TBD_P0` → locked provisional)

| Metric | P0 reference |
| --- | ---: |
| n | 570 |
| WR | 44.74% |
| R | 1.5 |
| BM | +4.74 pp |
| E_N | +0.118R |
| PF | 1.21 |
| Zone | Fragile (pending Leak) / gross-only barely Robust |
| Side | WR-side |

