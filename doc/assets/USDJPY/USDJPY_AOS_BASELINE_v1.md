# USDJPY — AOS Baseline v1 (engine freeze)

**Task:** USDJPY-AOS-P0-T01  
**Frozen:** 2026-10-19  
**Engine:** Balanced P0 · magic **26101828** · **AOS OFF**  
**Preset:** `Profiles/Tester/BMRG/USDJPY/BMRG-M15-USDJPY-6M-P0_balanced_chart.set`  
**Evidence:** Tester `logs/20261019.log` · `system_profile.md` · `blotter/archive/USDJPY-P0-CHART/`  
**Score under:** [`edge_framework.md`](./edge_framework.md)

**Purpose:** Immutable OS compare packet. Later layers must state Δ vs these rows. Not a production admission. Not scored EF (Leak = **prior** until deals).

---

## Identity

| Field | Value |
| --- | --- |
| Symbol / TF | USDJPY M15 |
| Geometry | SL **100** / TP **120** · RR **1.20** · BB 2.2 · CD 2 |
| Filters | 12–20 · skip Tue · ATR max **70** · MaxSpread 25 · BBw OFF |
| Deposit / model | $500 · every tick · ACCOUNT CURRENCY |
| regime_filtered | true |
| Leak_source | **prior** 11.4 pp (25pt RT / SL100) |

---

## Primary tip — 2026.05.01 → 2026.08.31

| Metric | Value |
| --- | ---: |
| n | **56** |
| WR | **48.2%** |
| R (design) | 1.20 |
| BWR / BM | 45.5% / **+2.8 pp** |
| E_N | **+0.061R** |
| Leak_prior / EF_prior | 11.4 pp / **−8.6 pp** |
| Final / Δ | 505.99 / **+$5.99** |
| Max win / loss streak | 3 / **7** |
| Zone (proxy) | **costs_fragile** |

### Tip monthly (gross)

| Month | n | WR | E_N |
| --- | ---: | ---: | ---: |
| 2026-05 | 13 | 53.8% | +0.185R |
| 2026-06 | 22 | 54.5% | +0.200R |
| 2026-07 | 18 | **33.3%** | **−0.267R** |
| 2026-08 | 3 | 66.7% | +0.467R |

### Tip sides / DOW (gross)

| Slice | n | WR | E_N |
| --- | ---: | ---: | ---: |
| BUY | 21 | **52.4%** | **+0.152R** |
| SELL | 35 | 45.7% | +0.006R |
| Mon | 16 | 56.2% | +0.238R |
| Wed | 17 | 47.1% | +0.035R |
| Thu | 13 | **30.8%** | **−0.323R** |
| Fri | 10 | 60.0% | +0.320R |

### Tip rolling (gross)

| Window | avg WR | avg E_N | min E_N |
| --- | ---: | ---: | ---: |
| W10 | 45.7% | +0.006R | −0.78R |
| W15 | 46.0% | +0.013R | −0.71R |
| W20 | 46.5% | +0.023R | −0.45R |
| W30 | 47.2% | +0.038R | −0.19R |

---

## Supporting YTD — 2026.01.01 → 2026.10.19

| Metric | Value |
| --- | ---: |
| n | **68** |
| WR / E_N | **51.5%** / **+0.132R** |
| BM / EF_prior | +6.0 pp / **−5.4 pp** |
| Final / Δ | 517.99 / **+$17.99** |

Sep fires = **0** (ATR≤70 on FRAGILE tip — expected).

---

## Prior footnote — 2026.01.01 → 2026.04.30

| Metric | Value |
| --- | ---: |
| n | **8** (ATR-starved — not a KEEP driver) |
| WR / E_N | 50.0% / +0.100R |
| Final / Δ | 501.20 / +$1.20 |

---

## OS compare rule

- **Default window:** tip May→Aug.  
- YTD = support / L3 diagnostics.  
- Prior n=8 = footnote only.  
- Probe (WR 57.6% / EF +0.8 pp) = **not** baseline.  
- Any OS task must report ΔE_N / ΔEF vs tip row above (or E_N hold while Leak pending).
