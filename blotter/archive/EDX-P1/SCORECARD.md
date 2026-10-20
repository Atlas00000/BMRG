# EDX-P1 — Isolation (session + DOW)

**Scored:** 2026-10-07  
**Runs in log:** mag **8230111** (P1-T01) · **8230112** (P1-T02) · May→Aug · final 444.39 (same G0 Harvest as P0)  
**Scored from:** 8230111 chunk · n=58 · R=1 · BWR=50%

## WHERE the edge lives (ranked)

| Rank | Cell | n | WR | BM | E_N |
| ---: | --- | ---: | ---: | ---: | ---: |
| 1 | **17–20 NY** | 12 | 91.7% | +41.7 pp | **+0.833R** |
| 2 | **14–17 LON–NY overlap** | 14 | 71.4% | +21.4 pp | **+0.429R** |
| 3 | Fri | 15 | 73.3% | +23.3 pp | +0.467R |
| 4 | Wed | 17 | 64.7% | +14.7 pp | +0.294R |
| 5 | Thu | 13 | 61.5% | +11.5 pp | +0.231R |

Session concentration (n×E_N among positive): best **17–20** share **62.5%** — not REGIME_CONCENTRATED (&gt;70%).

## WHERE the losses live

| Cell | n | WR | BM | E_N | Gate note |
| --- | ---: | ---: | ---: | ---: | --- |
| **12–14 LON open** | **32** | 46.9% | **−3.1 pp** | −0.062R | **n≥30 · BM≤0 → filter-justified** |
| Hour **12** | 24 | 41.7% | −8.3 pp | −0.167R | provisional (n&lt;30) |
| **Mon** | 13 | 46.2% | −3.8 pp | −0.077R | provisional (n&lt;30) |
| Tue | 0 | — | — | — | already filtered |

**BM_worst (n≥30):** `12-14_LON_open` (−3.1 pp).

---

## EDX-P1-T01 — Session cells → **ACCEPT**

Edge in mid/late session (14–20); losses at session open (12–14), driven by hour 12.

**P3 candidate:** `StartHour=13` (EDX-P3-T02) — justified by BM≤0 on n≥30 cell.

## EDX-P1-T02 — DOW cells → **ACCEPT**

Fri &gt; Wed &gt; Thu &gt; Mon. Tue n=0 (skip holds).

**P3 candidate:** skip Mon (EDX-P3-T01) — **provisional only** until n≥30 or EF↑ without FREQUENCY_STALL.

## P1 completion

| Task | Status |
| --- | --- |
| P1-T03 ATR×ER | **DONE** — see `P1-T03_SCORECARD.md` (home ATR_high\|ranging) |
| P1-T04 MAE/MFE | **SKIPPED** (streaks on P0; MAE deferred) |
| P1-T05 ranked summary | **DONE** (this file + T03) |

## Filter backlog (for P3)

1. **StartHour 13** — justified (n≥30, BM≤0)  
2. Skip Mon — soft / provisional  
3. BBDev 2.5 / cooldown — quality, not cell-BM justified yet
