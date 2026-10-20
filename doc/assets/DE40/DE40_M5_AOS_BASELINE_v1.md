# DE40 M5 — AOS Baseline v1 (engine freeze)

**Task:** DE40-M5-AOS-P0-T01  
**Frozen:** 2026-10-20  
**Engine:** Balanced P0 · magic **26101903** · **AOS OFF**  
**Preset:** `Profiles/Tester/BMRG/DE40/BMRG-M5-DE40-6M-P0_balanced_chart.set`  
**Evidence:** Tester `logs/20261020.log` · `system_profile_M5.md` · `blotter/archive/DE40-M5-P0/`  
**Score under:** [`edge_framework.md`](./edge_framework.md)  
**Sibling:** [`DE40_AOS_BASELINE_v1.md`](./DE40_AOS_BASELINE_v1.md) (M15) — do not mix

**Purpose:** Immutable OS compare packet for **M5**. Later layers must state Δ vs these rows. Not a production admission. Not scored EF until `Leak_source=measured` (prior stub below). Tip May→Oct filled **2026-10-20** (Tester to **2026.10.19**) — that is the OS compare default; Jan–Aug / May–Aug remain support rows.

---

## Identity

| Field | Value |
| --- | --- |
| Symbol / TF | DE40 → MT5 **DE30** **M5** |
| Geometry | SL **7000** / TP **8750** · RR **1.25** · BB 2.2 · CD **6** |
| Filters | 08–17 · skip Tue · ATR max **2380** · MaxSpread 1500 · BBw OFF |
| Deposit / model | $500 · every tick · ACCOUNT CURRENCY · lot **0.1** |
| regime_filtered | true |
| Leak_source | **prior** 7.0 pp (c_R≈1100/7000 · R=1.25) |

---

## Primary support blotter — 2026.01.01 → 2026.08.31

| Metric | Value |
| --- | ---: |
| n | **168** |
| WR | **57.1%** |
| R (design) | **1.25** |
| BWR / BM | 44.4% / **+12.7 pp** |
| E_N | **+0.286R** |
| Leak_prior / EF_prior | 7.0 pp / **+5.7 pp** |
| Final / Δ | 850.64 / **+$350.64** |
| Entries | BUY 91 · SELL 85 |
| ATR>max blocks | **469** |
| Zone (proxy) | **expansion_keep_candidate** · EF prior > 0 |

### Monthly closes (gross · design R)

| Month | n | WR | E_N | EF_prior | Regime |
| --- | ---: | ---: | ---: | ---: | --- |
| 2026-01 | 36 | 63.9% | +0.438R | +12.4 pp | pre-tip strong |
| 2026-02 | 25 | **40.0%** | **−0.100R** | −11.4 pp | **PRIMARY soft** |
| 2026-03 | 1 | 0% | −1.0R | — | ATR starved |
| 2026-04 | 13 | 76.9% | +0.731R | +25.5 pp | recovery |
| 2026-05 | 18 | **44.4%** | **0.0R** | −7.0 pp | **MISMATCH** |
| 2026-06 | 19 | 47.4% | +0.066R | −4.1 pp | MATCH soft |
| 2026-07 | 24 | 58.3% | +0.312R | +6.9 pp | MATCH |
| 2026-08 | **32** | **68.8%** | **+0.547R** | +17.3 pp | **MATCH star** |
| 2026-09 | — | — | — | — | FRAGILE · **OPEN** |
| 2026-10 | — | — | — | — | FRAGILE · **OPEN** |

---

## OS compare default — tip May→Oct 2026 (Tester → 2026.10.19)

| Metric | Value |
| --- | ---: |
| n | **123** |
| WR | **53.7%** |
| BWR / BM | 44.4% / **+9.2 pp** |
| E_N | **+0.207R** |
| Leak_prior / EF_prior | 7.0 pp / **+2.2 pp** |
| Final / Δ (Tester) | **707.76** / **+$207.76** |
| Zone (proxy) | tip EF prior > 0 · thinner than tip-core |

### Tip monthly (tape)

| Month | n | WR | E_N | Regime |
| --- | ---: | ---: | ---: | --- |
| 2026-05 | 17 | 47.1% | +0.06R | MISMATCH |
| 2026-06 | 19 | 47.4% | +0.07R | MATCH soft |
| 2026-07 | 24 | 58.3% | +0.31R | MATCH |
| 2026-08 | **34** | **64.7%** | **+0.46R** | MATCH star |
| 2026-09 | 21 | 52.4% | +0.18R | FRAGILE |
| 2026-10 | 8 | **25%** | **−0.44R** | FRAGILE soft |

### Tip sides / DOW / hour (tape)

| Slice | n | WR | E_N |
| --- | ---: | ---: | ---: |
| SELL | 52 | **63.5%** | **+0.43R** |
| BUY | 71 | 46.5% | +0.05R |
| Wed | 30 | **63.3%** | **+0.43R** |
| H14 | 4 | 25% | −0.44R |
| H16 | 9 | 33% | −0.25R |
| near_atr_cap | 36 | **61.1%** | **+0.38R** |

### Sep–Oct alone

| Metric | Value |
| --- | ---: |
| n / WR / E_N | **29** / **44.8%** / ≈0R |
| Read | Dilutes tip vs tip-core; Oct drives soft |

---

## Support — May→Aug tip-core / MATCH / prior

| Window | n | WR | E_N | EF_prior |
| --- | ---: | ---: | ---: | ---: |
| Tip-core May→Aug (tape) | 94 | 56.4% | +0.27R | ~+5.0 pp |
| MATCH Jun→Aug (P0 closes) | 75 | 60.0% | +0.350R | +8.6 pp |
| Prior Jan→Apr (tape) | 82 | 52.4% | — | — |
| YTD Jan→Oct (tape) | 208 | 52.9% | — | EF prior soft (Feb/Oct) |

---

## Design probe prior (not Stage-1)

| Metric | Value |
| --- | ---: |
| n / WR / E_N / EF | ~141 / 54.6% / +0.229R / +3.2 pp |
| Use | Geometry prior only — never Δ authority |

---

## MaxDD / measured Leak

**OPEN** — deal export required. Journal tip spread p50=84 pts → Leak_proxy ≈1.1 pp (not Stage-1).

---

## Explicit non-claims

- Not a live admit · not M15 replace · not Stage-1 tip Robust.  
- Journal open p50 ≈84 pts ≪ live ≈1020 — Leak prior remains authority.  
- Soft Feb / May are regime taxes, not DROP drivers.
