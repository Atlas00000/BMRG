# AAPL-M5-AOS-P1 — Review

**Date:** 2026-10-20  
**Tasks:** P1-T01 schema · P1-T02 tape builder · P1-T03 labels · P1-T05 regime flags · P1-T04 **DEFERRED** (band-ride)  
**Engine:** magic **26102011** · Apple M5 Balanced · AOS OFF  
**Log:** Tester `logs/20261020.log`

---

## Verdict

**ACCEPT P1** — tip/YTD/long fire tapes frozen · QA gates pass · L1 schema v0 locked.  
Proceed to **P2** L2det CF (Wed · H1 · Jul · spread≥30 · optional hour-18). Do **not** claim Stage-1 Robust (measured Leak still OPEN).

---

## QA gates

| Check | Result |
| --- | --- |
| Tip n ≥ 30 | **PASS** n=**77** |
| Tue_n == 0 | **PASS** |
| atr_missing == 0 | **PASS** |
| tip OPEN == TP+SL | **PASS** 36+41=77 |
| Leak ≠ Stage-1 Robust | **PASS** — journal proxy only |

---

## Tape inventory

| Tape | n | WR | E_N |
| --- | ---: | ---: | ---: |
| tip May→Oct | **77** | **46.8%** | **+0.16R** |
| tip-core May→Aug | 54 | 46.3% | +0.15R |
| sep–oct | 23 | 47.8% | +0.18R |
| prior Jan–Apr | 68 | 29.4% | −0.27R |
| YTD Jan→Oct | 145 | 38.6% | −0.04R |
| long 2025→tip | 289 | 40.1% | ≈0R |

Artifacts: `doc/assets/AAPL/tapes/aapl_m5_*_v0.csv` · this archive.

---

## Cost proxy (tip)

| Field | Value |
| --- | ---: |
| med entry spread | **29** pts |
| Leak 1× med/SL → framework | **6.17 pp** |
| Leak 2× | **12.34 pp** |
| Profile authority Leak | **~15.3 pp** |
| BM | **+6.33 pp** |
| EF @ profile Leak | **≈ −9.0 pp** |
| `spread_high_thr` | **≥30** (p80 floor; tip n=23 flagged) |

Measured deal Leak remains **OPEN**.

---

## Bad-cell tape confirmation (seed → CF candidates)

| Cell | Tip | YTD / prior | P2 stance |
| --- | --- | --- | --- |
| `DOW_WED` | n=25 WR 40% ≈0R | YTD WR **29%** −0.29R · prior WR **12%** | **SOFT** — stronger on long than tip |
| `H1_JAN_APR` | — | prior n=68 WR **29%** −0.27R | **SOFT** seasonal |
| `MONTH_JUL` | n=15 WR **20%** −0.51R | same | **SOFT** WR stress |
| `SPREAD_HIGH` (≥30) | n=23 WR **39%** −0.03R | YTD n=25 ≈0R | **SOFT** — tip discrimination OK |
| `HOUR_18` *(new from tape)* | n=16 WR **38%** −0.07R | YTD WR **30%** −0.25R | **SOFT optional** — CF before arm |
| Protect `MAY` | WR **67%** +0.65R | — | never blanket-skip |
| Protect `MON` | tip WR **62%** +0.55R | — | never blanket-skip |
| Protect tip `BUY` | WR **54%** +0.33R | — | no permanent sell-only |

Overnight: tip `nights_held` share **55.8%** · med hold win ≫ lose → elevates **L8** after L2det.

---

## Deferred

- **P1-T04** band-ride / structure flags — optional; not blocking P2.  
- Earnings calendar flag — use `regime_tag` / month until a calendar source exists.
