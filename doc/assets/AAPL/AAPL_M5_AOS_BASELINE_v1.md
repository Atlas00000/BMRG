# AAPL M5 — AIOS Baseline v1

**Task:** AAPL-M5-AOS-P0-T01  
**Frozen:** 2026-10-20  
**Engine:** Balanced TPgtSL · magic **26102011** · **AOS OFF**  
**Preset:** `Profiles/Tester/BMRG/AAPL/BMRG-M5-AAPL-6M-Balanced_TPgtSL.set`  
**Evidence:** Tester `logs/20261020.log` · deposit $500 · every tick  
**Source profile:** [`system_profile_M5.md`](./system_profile_M5.md)  
**Roadmap:** [`aios_roadmap_M5.md`](./aios_roadmap_M5.md)

Do **not** mutate this file mid-stream. Bump to v2 only after a re-scored Tester export with a new freeze date.

---

## Geometry (locked)

| Param | Value |
| --- | ---: |
| SL / TP | **190 / 280** |
| Designed RR / BWR | ≈**1.47** / **40.4%** |
| BB | 20 / **2.5** |
| ATR regime | **24–98** pts |
| BBw | **0.30–2.00%** |
| Session | **14:00–20:00** · skip Tue |
| MaxSpread / Cooldown | **40** / **6** |
| Lot | Fixed **1.0** |
| G0 | MaxLevels=1 · MaxEntries=1 |

---

## Primary OS compare window — tip May→Oct 2026

| Metric | Value |
| --- | ---: |
| Window | **2026.05.01 → 2026.10.19** |
| n | **77** |
| WR | **46.8%** |
| BM (des BWR) | **+6.3 pp** |
| E_N | **+0.16R** |
| R_real (approx) | ~1.75 |
| Net PnL | **+$44.50** (+8.9%) |
| Final balance | 544.50 |
| MaxDD (path) | ~**5.0%** |
| PF (approx) | ~1.54 |
| Stage-0 | **PASS** (WR>BWR · E_N>0 · TP>SL) |
| Stage-1 (true Leak) | **FAIL / Fragile** until deal export |

---

## Support windows (diagnostic — not sole DROP)

| Window | n | WR | E_N | Net | Read |
| --- | ---: | ---: | ---: | ---: | --- |
| Feb→Oct | 124 | 39.5% | −0.02R | +9.45 | H1 drag |
| Jan→Oct | 145 | 38.6% | −0.05R | −1.97 | L3 regime |
| 2025.01→2026.10 | 289 | 40.1% | ≈0R | +18.95 | Long thin |

---

## Cost / Leak (baseline freeze)

| Field | Value | Note |
| --- | ---: | --- |
| Preset meta Leak | 2.1 pp | **Inadmissible** for Robust |
| True Leak proxy | ~**15.3 pp** | med open spread ~29 / SL 190 |
| EF_proxy (tip) | ~**−9 pp** | BM − true Leak |
| Leak_source | `journal_spread_proxy` | Replace with `measured` on deal export |

---

## Protect / soft cells (seed)

| Class | Cells |
| --- | --- |
| **Protect** | May · Mon · tip BUY WR |
| **Soft / skip candidates** | Jan–Apr · Jul WR · Wed (long) · high-spread · overnight/`OTHER` path |

Full registry: [`aos_bad_cells_M5.md`](./aos_bad_cells_M5.md).
