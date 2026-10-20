# DE40 — AOS Baseline v1 (engine freeze)

**Task:** DE40-AOS-P0-T01  
**Frozen:** 2026-10-19  
**Engine:** Balanced P0 · magic **26101902** · **AOS OFF**  
**Preset:** `Profiles/Tester/BMRG/DE40/BMRG-M15-DE40-6M-P0_balanced_chart.set`  
**Evidence:** Tester cache `BMRG.DE30.M15.*.tst` · `system_profile.md` · `blotter/archive/DE40-P0-CHART/`  
**Score under:** [`edge_framework.md`](./edge_framework.md)

**Purpose:** Immutable OS compare packet. Later layers must state Δ vs these rows. Not a production admission. Not scored EF until `Leak_source=measured` (prior stub below).

---

## Identity

| Field | Value |
| --- | --- |
| Symbol / TF | DE40 → MT5 **DE30** M15 |
| Geometry | SL **5000** / TP **6250** · RR **1.25** · BB 2.2 · CD 2 |
| Filters | 08–17 · skip Tue · ATR max **4070** · MaxSpread 1500 · BBw OFF |
| Deposit / model | $500 · every tick · ACCOUNT CURRENCY · lot **0.1** |
| regime_filtered | true |
| Leak_source | **prior** 9.8 pp (c_R≈1100/5000 · R=1.25) |

---

## Primary tip — 2026.05.01 → 2026.10.18

| Metric | Value |
| --- | ---: |
| n | **77** |
| WR | **58.4%** |
| R (realised proxy) | **1.24** |
| BWR / BM | 44.4% / **+14.0 pp** |
| E_N | **+0.310R** |
| Leak_prior / EF_prior | 9.8 pp / **+4.2 pp** |
| Final / Δ | 638.90 / **+$138.90** |
| MaxDD≈ | **4.4%** |
| PF≈ | **1.75** |
| Zone (proxy) | **expansion_keep** · tip EF prior > 0 |

### Tip monthly (gross)

| Month | n | WR | Net $ | E_N≈ | Regime |
| --- | ---: | ---: | ---: | ---: | --- |
| 2026-05 | 9 | **67%** | +26.3 | +0.50R | MISMATCH tag · local win |
| 2026-06 | 12 | 50% | +8.3 | +0.12R | MATCH |
| 2026-07 | 6 | 50% | +4.1 | +0.12R | MATCH · thin |
| 2026-08 | **33** | **64%** | **+81.4** | +0.43R | MATCH strongest |
| 2026-09 | 13 | 54% | +16.0 | +0.21R | FRAGILE · ATR-thinned |
| 2026-10 | 4 | 50% | +2.8 | +0.12R | FRAGILE · incomplete |

### Tip rolling (gross · R from $/|AL|)

| Window | avg WR | avg E_N | min E_N |
| --- | ---: | ---: | ---: |
| W10 | 58.7% | **+0.32R** | −0.11R |
| W15 | 59.4% | **+0.33R** | **+0.04R** |
| W20 | 60.0% | **+0.34R** | **+0.01R** |
| W30 | 61.5% | **+0.38R** | +0.12R |

### Tip sides / DOW / hour

**OPEN** — deal export / journal required (P1). Do not invent.

---

## Supporting YTD — 2026.01.01 → 2026.10.18

| Metric | Value |
| --- | ---: |
| n | **147** |
| WR / E_N | **50.3%** / **+0.132R** |
| BM / EF_prior | +5.9 pp / **−3.9 pp** |
| Final / Δ | 612.43 / **+$112.43** |
| MaxDD≈ | **13.9%** |
| PF≈ | ~1.26 |

### YTD soft months (OS diagnostic)

| Month | n | WR | Net $ | Note |
| --- | ---: | ---: | ---: | --- |
| 2026-01 | 29 | 45% | +1.4 | Soft |
| 2026-02 | 29 | **34%** | **−39.1** | **PRIMARY bad cell** |
| 2026-03 | 4 | **0%** | **−23.1** | FRAGILE · thinned |
| 2026-04 | 8 | 75% | +32.3 | Recovery |

---

## 2025 stub footnote — broker from 2025.06.05

| Metric | Value |
| --- | ---: |
| Window | ~2025.06 → 2025.08 (depth-bound) |
| n / WR / E_N | 38 / **31.6%** / **−0.29R** |
| Net | **−$76.5** |
| Regime | **MISMATCH** Jun–Jul |
| Use | Footnote only — **never** sole DROP / KEEP driver |

---

## OS compare rule

- **Default window:** tip May→Oct.  
- YTD = support / L3 diagnostics (Feb–Mar path).  
- 2025 stub = MISMATCH footnote only.  
- Probe (WR 58.2% / EF +4.0 pp) = **not** baseline (aligned, but tip is authority).  
- Any OS task must report ΔE_N / ΔEF vs tip row above (or E_N hold while Leak pending).
