# EDX-P8-T01 — Measured Leak (champ May→Aug)

**Scored:** 2026-10-07  
**Sleeve:** AUDUSD-CHAMP (Start13 + skip Mon/Tue · 300/300)  
**Evidence run:** magic **8230501** (= champ inputs) · **2026.05.01 → 2026.08.31**  
**Inbox deals:** none — journal entry bid/ask used.

## Cost model

| Component | Status |
| --- | --- |
| Entry spread → `c_R` | **Measured** (per event) |
| Commission | **Absent** |
| Swap | **Absent** |
| Slippage | **Absent** |

`c_R = spread_pts / 300` · `Leak = c_R / (R+1)` · median spread **14 pts**.

| | Prior proxy `3×spread/SL` | **P8 measured (1× entry)** |
| --- | ---: | ---: |
| Leak | 7.00 pp | **2.44 pp** |
| EF | +13.21 | **+17.78** |
| Zone | Robust* | **Robust** (EF 17.78 > M 12.66) |

\*Proxy overstated Leak vs entry-spread-only; full deal CSV still required for commission/swap/slip.

## Health vector

| Metric | Value |
| --- | ---: |
| n | 47 |
| WR / BWR | 70.21% / 50% |
| BM | +20.21 pp |
| E_N | **+0.404R** |
| c_R mean | 0.0487R |
| Leak | **2.44 pp** |
| EF / M | **+17.78** / ±12.66 |
| PnL | +57.10 |
| G1 proxy | **PASS** (n still Insufficient &lt;100) |

## Verdict

**ACCEPT_LEAK_PARTIAL** — geometry untouched · Leak no longer `costs_defaulted` for spread leg · gaps named.  
Production still blocked on n_tier + incomplete cost legs until deal export.

## Leak policy for P8-T02+

Use **mean entry-spread `c_R`** (same formula). Do not revert to 3× proxy unless deal CSV unavailable *and* documented.
