# AUDUSD-RISK3-Q — 3% risk quarterly / survival review

**Source:** `Tester/logs/20261008.log` runs #31–46 · magic `8230921` · AIOS LIVE_WITHHOLD · W=250 · `L2skip_aud_p90_20261008_122523`  
**Scored:** 2026-10-08 · journal-only (no deal blotter) · deposit assumed **$400**

## Scaling ladder (context)

| Risk% | Window | PnL | Halt | Verdict |
| ---: | --- | ---: | ---: | --- |
| 2 | Jan→Oct | +$27 | 0 | safe / underutilized |
| **3** | Jan→Oct | **+$84** | **0** | **survives long mix** |
| 5 | Jan→Oct | −$65 | **45575** | L3 halt — fails long mix |
| 3 | May→Aug | +$183 | 0 | scales in-regime |
| 5 | May→Aug | +$274 | 0 | in-regime OK; long fails |

## Quarterly @ Risk 3%

| Window | Tag | PnL | Ord | lot≈ | Halt | f | Survival |
| --- | --- | ---: | ---: | ---: | ---: | --- | --- |
| 2026.01→04 | OFF_Q1 | **−$12** | 125 | 0.026 | 0 | 0.75 | **survive** (mild bleed) |
| 2026.05→08 | IN_REGIME | **+$183** | 94 | 0.033 | 0 | 0.75 | **scale OK** |
| 2025.01→04 | OFF_2025Q1 | **−$14** | 72 | 0.028 | 0 | 0.75 | **survive** |
| 2025.05→08.01 | IN_2025 | **+$48** | 83 | 0.027 | 0 | 0.75 | **scale OK** (weaker tip) |
| 2025.08 only | OFF_AUG25 | **−$42** | 30 | 0.025 | 0 | 0.75 | **survive but sharp** (~−10% equity) |
| 2025.09→12 | THIN_Q4 | +$22 | 6 | 0.030 | 0 | 0.75 | n too thin — ignore |

## Verdict

**3% Risk: ACCEPT for research / expansion sizing** — not a production G0–G5 claim.

- **Off-regime:** does not halt; Q1s lose ~3–4% equity; Aug-25 pocket can take ~10% in a month — painful but under EquityHalt 15% / AOS DD 25%.
- **In-regime:** compounds hard (+46% May→Aug 2026; +12% May→Aug 2025 truncated).
- **Long mix (Jan→Oct):** 3% finishes +$84 Stable; **5% does not** (L3 → f→0). Binding constraint is the full path, not the tip quarter.
- L4 holds `f=0.75` throughout at 3% — AOS never needs to step down on the quarterly set.

**Do not promote 5%.** Tip/regime windows flatter it; off-regime + long window kill it.

**Caveats:** journal PnL only; MaxDD not exported; Aug-25 is one bad month not a full quarter; 2025 Q4 n=6 invalid; min-lot / L4 still bias f_realised.

## Rolling performance @ Risk 3% (from AOS close TP/SL)

`InpAOS_W250=250` → **W250 EF/EN stay 0** on all quarters (n≪250). Rolling metrics below use event windows W10/W20 on the close stream.

| Window | n | WR | W20 WR min→last | max loss streak | notes |
| --- | ---: | ---: | --- | ---: | --- |
| **2026 May→Aug** (in) | 45 | **71%** | 65→70% | 3 | scales clean |
| **2026 Jan→Oct** (mix) | 123 | 53% | **30→40%** | 7 | tip drags W20 ≤ BWR |
| **2026 Jan→Apr** (off) | 60 | 47% | 30→35% | 7 | bleed, no halt |
| **2025 Jan→Apr** (off) | 34 | 44% | 35→35% | 8 | similar off-regime |
| **2025 May→Aug** (in) | 40 | 58% | 55→55% | 4 | weaker tip than 2026 |
| **2025 Aug** (off pocket) | 13 | **23%** | W10→10% | 8 | WR collapse |

Tester Relative DD not in journal; path DD from R-sequence is model-only — use deal export for gate MaxDD.
