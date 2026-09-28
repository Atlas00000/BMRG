# EDX-P2-T01 — recent window check (Jul–Sep 2026)

**Scored:** 2026-09-25 11:58  
**Preset:** same Survival sleeve (SL200/TP450, magic 8210201, champ filters)  
**Window:** **2026.07.01 → 2026.09.24** (≈3 months; Sep truncated — not used alone)

Rationale: incomplete current month is not a fair backtest cell; use last **complete** months for recent stress.

## 3M health

| Metric | Value |
| --- | ---: |
| n | 43 (provisional; &lt;100) |
| WR | 32.6% |
| BWR | 30.8% |
| BM | +1.8 pp |
| E_N | +0.058R |
| Leak L1 | ~2.5 pp |
| EF | **−0.75** |
| Final | $400 → **$406.52** |
| Zone | Negative after Leak |

**Pool read:** WR still **> BWR** and E_N>0 on a thin recent sample, but **EF≤0** after Leak → tag `costs_fragile` / recent stress — does **not** revoke long-window POOL_KEEP; flags Survival sleeve needs Leak watch in late-2026.

## Sep-2026 alone (11:57) — do not use for admission

n=11, WR 9.1%, final $384.94. Incomplete month → **stress footnote only**.

## Window policy (going forward)

| Use | Window |
| --- | --- |
| Pool admission / compare sleeves | Long: 2025.01.01 → last **complete** month end |
| Recent regime stress | Trailing **3 complete months** |
| Avoid as primary | Incomplete current month (e.g. Sep-2026 mid-month) |
