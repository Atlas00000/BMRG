# JP225 / JPN225 M5 — AOS Baseline v1 (engine freeze)

**Task:** JP225-M5-AOS-P0-T01  
**Frozen:** 2026-10-20  
**Engine:** Growth P0 · magic **26101906** · **AOS OFF**  
**Preset:** `Profiles/Tester/BMRG/JP225/BMRG-M5-JP225-6M-P0_growth_chart.set`  
**Evidence:** Tester `logs/20261020.log` · [`system_profile_M5.md`](./system_profile_M5.md) · `blotter/archive/JP225-M5-P0-REVIEW/`  
**Score under:** [`edge_framework.md`](./edge_framework.md)  
**Sibling:** [`JP225_AOS_BASELINE_v1.md`](./JP225_AOS_BASELINE_v1.md) (M15) — do not mix

**Purpose:** Immutable OS compare packet for **M5**. Later layers must state Δ vs these rows. Not a production admission. Not scored EF until `Leak_source=measured` (prior stub below). Tip May→Oct is the OS compare default.

---

## Identity

| Field | Value |
| --- | --- |
| Symbol / TF | JP225 → MT5 **JPN225** **M5** |
| Geometry | SL **25000** / TP **50000** · RR **2.00** · BB **2.5** · CD **3** · Fade **OFF** |
| Filters | 08–17 · skip Tue · ATR **band 7610–11285** · MaxSpread **3000** · BBw OFF |
| Deposit / model | $500 · every tick · lot **0.1** (`VOLUME_MIN`) |
| regime_filtered | true |
| Leak_source | **prior** **3.3 pp** (c_R≈2500/25000 · R=2.00) |

---

## OS compare default — tip May→Oct 2026 (Tester → 2026.10.19)

| Metric | Value |
| --- | ---: |
| n | **94** |
| WR | **41.5%** |
| R (design / med) | **2.00** / **2.00** |
| BWR / BM | 33.3% / **+8.2 pp** |
| E_N | **+0.245R** |
| Leak_prior / EF_prior | 3.3 pp / **+4.9 pp** |
| Final / Δ | **535.34** / **+$35.34** |
| MaxDD proxy | **~3.4%** |
| tp_lt_sl | **0** |
| Zone (proxy) | **expansion_keep_candidate** · tip EF prior > 0 |

### Tip monthly (closes)

| Month | n | WR | E_N | EF_prior | Regime |
| --- | ---: | ---: | ---: | ---: | --- |
| 2026-05 | 13 | 38.5% | +0.15R | +1.8 pp | FRAGILE · pays light |
| 2026-06 | 17 | **47.1%** | **+0.41R** | +10.4 pp | FRAGILE · **pays** |
| 2026-07 | 20 | **60.0%** | **+0.80R** | +23.4 pp | MISMATCH · **star** |
| 2026-08 | 17 | 29.4% | −0.12R | −7.2 pp | MATCH · **tax** |
| 2026-09 | 17 | 23.5% | −0.29R | −13.1 pp | MATCH · **tax** |
| 2026-10 | 10 | 50.0% | +0.50R | +13.4 pp | MISMATCH · pays |

---

## Support — YTD Jan→Oct 19

| Metric | Value |
| --- | ---: |
| n | **130** |
| WR | **38.5%** |
| BM / E_N / EF_prior | +5.1 pp / **+0.154R** / **+1.8 pp** |
| Final / Δ | 530.06 / +$30.06 |
| BUY / SELL | 59 / 71 |
| Soft pre-tip | Feb WR 20% · Apr WR 10% |

---

## Regime pockets (tip months)

| Pocket | n | WR | E_N | EF_prior | OS read |
| --- | ---: | ---: | ---: | ---: | --- |
| **OFFHOME** (May–Jul+Oct) | **60** | **50.0%** | **+0.50R** | **+13.4 pp** | **HOME — protect** |
| **MATCH** Aug–Sep | **34** | 26.5% | **−0.21R** | **−10.2 pp** | **TAX — L2 seed** |

**Critical:** Opposite of M15 (MATCH home · OFFHOME tax). Do not import M15 May∨Jul arm map.

---

## Design probe (prior only — not OS target)

| Metric | Value |
| --- | ---: |
| n / WR / E_N / EF | ~107 / ~38.3% / ~+0.15R / ~+1.7 pp |

Tip blotter is stronger in the same direction — freeze tip as authority.

---

## Freeze rules

1. Geometry SL/TP/RR/BB/CD/ATR band/session frozen for OS Δ.  
2. Every OS scorecard states window = **tip May→Oct** (or explicitly YTD/support).  
3. `Leak_source=prior` until deal-measured packet exists.  
4. Never score Canvas tiles as promote evidence.  
5. Sibling M15 baseline (`JP225_AOS_BASELINE_v1`) is **not** transferable.
