# JP225 / JPN225 — P1 WR-lift review (expansion candidate)

**Framing:** asset-list expansion research · **not** live replacement · AIOS **P0 stubs landed**  
**AIOS pack:** `doc/assets/JP225/aios_roadmap.md` · baseline freeze this magic  
**Preset:** `Profiles/Tester/BMRG/JP225/BMRG-M15-JP225-6M-P1_wrLift_fade_chart.set`  
**Magic:** 26101904 · Log: `Tester/logs/20261019.log` · Scored: 2026-10-19  
**Leak prior:** 2500 pts RT / SL 23260 → Leak ≈ 4.3pp · R_design = 1.50

## Verdict

| Gate | Result |
| --- | --- |
| Geometry (TP>SL, RR≈1.50, tp_lt_sl=0) | **PASS** |
| Stage 0 tip (E_N>0, WR>BWR) | **weak PASS** (tip E_N +0.08R) |
| Stage 1 tip (EF>0 after Leak) | **FAIL** (tip EF −1.3pp) |
| Live / replace incumbent | **NO** |
| Keep as expansion sleeve + iterate | **YES** → next P1.5 light (26101905) |

P1 fade + BB 2.3 gave a **slight** WR lift vs P0 (43.0% vs 42.4%) but not enough to clear Leak. Failure is **hit-rate / regime mix**, not broken geometry or deposit.

## Preset / system behaviour

- G0 single-leg · London 08–17 · Tue off · ATR max 19670 (≈p75) · AOS **OFF**
- FadeConfirm ON · BBDev 2.3 · CD 2 · SL/TP **frozen** 23260/34890
- Lot 0.1 (broker min) · MaxSpread 3000 · deposit unchanged
- Realised R = **1.500** exact on all scored windows · no RR crush

## Rolling windows (P1 magic 26101904)

| Window | n | WR | EF | E_N | Balance | Notes |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| Tip May–Aug | **79** | **43.0%** | **−1.3pp** | +0.08R | 509.28 | Stage 1 fail |
| Jul–Aug | 36 | 44.4% | **+0.1pp** | +0.11R | 505.56 | Aug carries |
| Jan–Aug | 143 | 42.0% | −2.3pp | +0.05R | 517.18 | Q1 drag |
| 2025.01→2026.10 | 360 | 41.7% | −2.6pp | +0.04R | 522.14 | long · alternating months |

### vs P0 (26101903) tip

| | P0 tip | P1 tip |
| --- | ---: | ---: |
| n | 99 | 79 |
| WR | 42.4% | 43.0% |
| EF | −1.9pp | −1.3pp |
| Starve? | no | mild (−20 fires), not starved |

## Regime read (why tip fails)

Ouroboros meanrev fit on tip months:

| Month | Tag | P1 WR | P1 EF |
| --- | --- | ---: | ---: |
| 2026-05 | FRAGILE | 30.4% | −13.9pp |
| 2026-06 | FRAGILE | **55.0%** | **+10.7pp** |
| 2026-07 | MISMATCH | 30.8% | −13.5pp |
| 2026-08 | MATCH | **52.2%** | **+7.9pp** |
| 2026-09 | MATCH (long run) | 50.0% | +5.7pp |
| 2026-10 | MISMATCH (tip incomplete) | 33.3% | −11.0pp |

**MATCH-only (Aug±Sep):** WR ~50–52% · EF **+5.7…+7.9pp** · E_N ≈ +0.25…+0.30R — engine is on-home viable.  
**OFFHOME slice on tip:** WR 39.3% · EF −5.0pp — May FRAGILE + Jul MISMATCH pull the tip below Stage 1.

Jun FRAGILE still pays (high-vol ranging can fade); May/Jul do not. Aggregate tip EF≤0 is a **regime-mix** problem, not proof the sleeve is dead.

## Expansion posture (pre-AIOS)

1. Keep JP225 on the **research expansion list** — geometry + MATCH behaviour are healthy for a fat-spread index.
2. Do **not** promote to live / do not displace UK100·DE40·EURUSD·AUDUSD books.
3. Do **not** arm AIOS yet — clear Stage 1 engine tip first (P1.5 or later).
4. Next sleeve: `BMRG-M15-JP225-6M-P1p5_light_chart.set` (BB 2.3 · CD 4 · ATR≤18620 · Fade OFF · magic **26101905**).
5. Score tip + MATCH-only separately; treat MISMATCH/FRAGILE months as expected variance until a JP225 AIOS exists.

## Pass criteria for next blotter

`WR > BWR + Leak` (~44%+) · `EF > 0` · `n ≥ 40` · `tp_lt_sl = 0` · deposit/lot unchanged.
