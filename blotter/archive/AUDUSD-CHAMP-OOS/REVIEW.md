# AUDUSD champion — quarterly / OOS survivability

**Scored:** 2026-10-07  
**Stack:** StartHour=13 · TradeMon=false · TradeTue=false · SL/TP 300/300 (freeze magic **8230601** ≡ champ inputs)  
**BWR:** **50%** (R≈1)  
**Deposit:** $400

## Runs (log 20261007 · indices 28–33)

| # | Window | Role | n | WR | E_N | EF* | PnL | maxDD≈R | Label |
| ---: | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| 29 | 2026.05.01→08.31 | **IS primary** | 47 | **70.2%** | **+0.404** | +13.2 | +57.10 | 2 | **SURVIVE** |
| 28 | 2026.01.01→04.30 | OOS 2026-H1a | 62 | 43.6% | **−0.129** | −13.5 | −18.53 | 14 | **FAIL** |
| 30 | 2025.01.01→04.30 | OOS 2025-Q1 | 54 | 51.9% | +0.037 | −2.4 | +2.57 | 9 | **MARGINAL** |
| 31 | 2025.05.01→08.01 | OOS 2025 mid† | 42 | 54.8% | +0.095 | −4.2 | +10.55 | 4 | **SURVIVE** |
| 32 | 2025.08.01→08.31 | OOS stress month‡ | 11 | **27.3%** | **−0.455** | −31.7 | −15.94 | 6 | **WIPEOUT** |
| 33 | 2025.09.01→12.31 | OOS 2025-Q4 | 47 | 51.1% | +0.021 | −0.9 | +4.21 | 8 | **MARGINAL** |

\*Leak proxy. †Tester **To** is 08.01 not 08.31 — incomplete “summer” quarter. ‡Single month, not a quarter; overlaps / fills Aug after truncated #31.

## Survivability read

| Metric | Value |
| --- | --- |
| OOS blocks (excl. IS) | 5 |
| Hold (SURVIVE/MARGINAL) | **3 / 5** (60%) |
| Fail / wipeout | **2 / 5** (2026 Q1–Apr · Aug-2025 month) |
| OOS E_N > 0 | 3 / 5 |
| IS still best | May→Aug 2026 unmatched |

**Verdict: MIXED — regime-sensitive survival, not robust.**

- Sleeve **does not die** on every out-of-window quarter: 2025 Q1 / mid / Q4 stay ≥BWR or barely above with tiny +E_N.
- **Hard fails:** early-2026 (WR 44% · −0.13R · DD≈14R path) and **Aug-2025** month (WR 27% · −0.46R) — same class of tip/regime leak as Sep-2026 L3.
- Almost all OOS EF* ≤ 0 (Fragile/Negative) → expansion KEEP only; **no** production survivability claim.
- Path DD on FAIL quarters (~9–14R cumulative) is the real survival risk under fixed Risk%.

## Implication for champ preset

`AUDUSD-CHAMP_*` remains **EXPANSION_KEEP ★ on May→Aug 2026** with **WATCH** on OOS: tradeable research edge is **windowed / regime_filtered**, not all-season. Do not promote live. Optional next: mark bad months (Aug/Sep-type) or ATR gate — not assumed fixed by this review.
