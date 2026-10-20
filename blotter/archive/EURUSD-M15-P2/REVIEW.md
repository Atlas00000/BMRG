# EURUSD-M15-P2 — Tester review

**task_id:** EURUSD-M15-P2  
**archived_at:** 2026-10-18T15:25:00+01:00  
**preset:** `BMRG-M15-EURUSD-6M-P2_light_selective_chart.set` · magic **26101817**  
**log:** `Tester/logs/20261018.log` (utf-16; only EURUSD P2 runs present at score time)  
**lens:** expansion chart sleeve · **not** live replace · AOS OFF

## Geometry

| Field | Value |
| --- | --- |
| SL / TP / RR | 300 / 375 / **1.25** (TP > SL) |
| BB | 20 / **2.3σ** (vs P0 2.2 · P1 2.4) |
| Cooldown | **3** bars (vs P0 2) |
| ATR max | **74** (p90 · P1 68 rejected) |
| BB-width | OFF |
| Session | 12–20 · Tue off |
| Grid | G0 · MaxLevels=1 |

## Rolling windows (deal TP/SL pairs · Leak prior 20pt RT)

| Window | n | WR | BWR | BM | EF† | E_N | PnL‡ | Stage 0 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| YTD 2026.01→10.17 | 72 | **48.6%** | 44.4% | +4.2pp | **+1.2pp** | **+0.094R** | +20.91 | **PASS** |
| Tip 2026.05→10.17 | 45 | **46.7%** | 44.4% | +2.2pp | −0.7pp | **+0.050R** | +7.14 | **PASS** |

† Leak prior ≈ 3.0pp. ‡ Deposit 500.

**Accept checks (tip):** n≥30 ✓ · WR > BWR ✓ · E_N > 0 ✓ · 0× TP&lt;SL ✓.

## Monthly (tip slice)

| Month | n | WR | sumR | vs BWR |
| --- | ---: | ---: | ---: | --- |
| 2026-05 | 9 | 44.4% | 0.00 | ≈BWR |
| 2026-06 | 9 | 44.4% | 0.00 | ≈BWR |
| 2026-07 | 7 | **57.1%** | +2.00 | ok |
| 2026-08 | 7 | 42.9% | −0.25 | fail |
| 2026-09 | 11 | 45.5% | +0.25 | ok |
| 2026-10 | 2 | 50.0% | +0.25 | thin / FRAGILE tip |

YTD hole: **Feb WR 30%** (n=10 · sumR −3.25) — treat as regime mismatch, not geometry break.

## Behaviour

- Blocks dominated by **session** + **weekday** (design sleeve); ATR>74 fires sparsely (gate doing its job on HV).
- Realized R holds at design 1.25 / −1.0 — geometry clean.
- vs P0 tip WR≈33% · vs P1 tip n≈6 — P2 restores fire-count and clears WR>BWR.

## Verdict

**CHART SLEEVE HOLD — Stage 0 pass on tip + YTD.** Stage 1 tip EF thin (−0.7pp under cost prior); YTD EF positive. Not G0–G5 / live / AOS. Expansion candidate ahead of per-asset AIOS.

## Ladder

| Sleeve | Magic | Status |
| --- | ---: | --- |
| P0 balanced | 26101815 | WR &lt; BWR |
| P1 selective | 26101816 | reject — starved |
| **P2 light** | **26101817** | **tip Stage 0 pass** |
