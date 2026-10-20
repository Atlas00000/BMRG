# JP225 — AOS Baseline v1 (engine freeze)

**Task:** JP225-AOS-P0-T01  
**Frozen:** 2026-10-19  
**Engine:** Growth P1 wrLift fade · magic **26101904** · **AOS OFF**  
**Preset:** `Profiles/Tester/BMRG/JP225/BMRG-M15-JP225-6M-P1_wrLift_fade_chart.set`  
**Evidence:** Tester `logs/20261019.log` · `blotter/archive/JP225-P1-REVIEW/` · chart card `doc/BMRG_M15_JP225_6M_chart_preset.md`  
**Score under:** [`edge_framework.md`](./edge_framework.md)

**Purpose:** Immutable OS compare packet. Later layers must state Δ vs these rows. Not a production admission.  
**Leak footnote (2026-10-19):** tip deal-fill measured **2.45 pp** (`Leak_source=measured` · `LEAK_MEASURED.json`). Frozen rows below keep **prior** numbers for historical Δ; new scorecards use measured unless stress-testing prior.

---

## Identity

| Field | Value |
| --- | --- |
| Symbol / TF | JP225 → MT5 **JPN225** M15 |
| Geometry | SL **23260** / TP **34890** · RR **1.50** · BB **2.3** · CD 2 · Fade **ON** |
| Filters | 08–17 · skip Tue · ATR max **19670** · MaxSpread 3000 · BBw OFF |
| Deposit / model | $500 · every tick · ACCOUNT CURRENCY · lot 0.1 |
| regime_filtered | true |
| Leak_source (freeze row) | **prior** ~4.3 pp (2500 pt RT / SL23260) |
| Leak_source (authority now) | **measured** **2.45 pp** · tip EF **+0.59 pp** |

---

## Primary tip — 2026.05.01 → 2026.08.31

| Metric | Value |
| --- | ---: |
| n | **79** |
| WR | **43.0%** |
| R (realised ≈ design) | **1.500** |
| BWR / BM | 40.0% / **+3.0 pp** |
| E_N | **+0.076R** |
| Leak_prior / EF_prior | 4.3 pp / **−1.3 pp** |
| Final / Δ | 509.28 / **+$9.28** |
| tp_lt_sl opens | **0** |
| Zone (proxy) | **regime_fragile** (Stage 0 weak · Stage 1 fail) |

### Tip monthly (gross)

| Month | Tag | n | WR | EF_prior | E_N |
| --- | --- | ---: | ---: | ---: | ---: |
| 2026-05 | FRAGILE | 23 | **30.4%** | **−13.9 pp** | −0.239R |
| 2026-06 | FRAGILE | 20 | **55.0%** | **+10.7 pp** | +0.375R |
| 2026-07 | MISMATCH | 13 | **30.8%** | **−13.5 pp** | −0.231R |
| 2026-08 | MATCH | 23 | **52.2%** | **+7.9 pp** | +0.304R |

### Tip regime slices

| Slice | n | WR | EF_prior | E_N |
| --- | ---: | ---: | ---: | ---: |
| MATCH (Aug) | 23 | **52.2%** | **+7.9 pp** | +0.304R |
| OFFHOME (May+Jun+Jul) | 56 | 39.3% | −5.0 pp | −0.018R |
| ALL tip | 79 | 43.0% | −1.3 pp | +0.076R |

---

## Supporting Jan→Aug — 2026.01.01 → 2026.08.31

| Metric | Value |
| --- | ---: |
| n | **143** |
| WR / E_N | **42.0%** / **+0.049R** |
| BM / EF_prior | +2.0 pp / **−2.3 pp** |
| Final / Δ | 517.18 / **+$17.18** |

---

## Long footnote — 2025.01.01 → 2026.10.18

| Metric | Value |
| --- | ---: |
| n | **360** |
| WR / E_N | **41.7%** / **+0.042R** |
| BM / EF_prior | +1.7 pp / **−2.6 pp** |
| Final / Δ | 522.14 / **+$22.14** |
| Sep MATCH | n=20 · WR 50% · EF +5.7 pp |
| Oct MISMATCH | n=6 · WR 33% · incomplete tip |

Long = alternating monthly path · L3 diagnostic only · never sole KEEP.

---

## P0 contrast (not baseline)

| Metric | P0 tip 26101903 | P1 tip 26101904 |
| --- | ---: | ---: |
| n | 99 | 79 |
| WR | 42.4% | 43.0% |
| EF_prior | −1.9 pp | −1.3 pp |

Slight WR lift; Stage 1 still fail. Geometry unchanged.

---

## OS compare rule

- **Default window:** tip May→Aug.  
- Jan–Aug / long = support / L3 diagnostics.  
- MATCH-only = protect-cell metric, never sole production admission.  
- Probe (WR≈47% / EF≈+3 pp) = **not** baseline.  
- P1.5 (26101905) = **new baseline** only after formal re-freeze if tip Stage 1 clears with AOS OFF.  
- Any OS task must report ΔE_N / ΔEF vs tip row above (or E_N hold while Leak pending) · plus `tip_EF_cleared`.
