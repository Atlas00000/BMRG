# AAPL M5 — AIOS Bad-Cell Registry

**Task:** AAPL-M5-AOS-P0-T02  
**Frozen:** 2026-10-20 · **P1-updated** from tip/YTD tapes  
**Engine:** magic **26102011** · Balanced M5  
**Source:** [`system_profile_M5.md`](./system_profile_M5.md) · [`tapes/`](./tapes/) · `blotter/archive/AAPL-M5-AOS-P1/TAPE_QA.json`  
**Roadmap:** [`aios_roadmap_M5.md`](./aios_roadmap_M5.md)

Do **not** import M15 Thu as default M5 cell. Hour-18 is now **M5-tape-confirmed** (optional SOFT) — still CF before arm; not a silent M15 transplant.

---

## Seed map (L2det candidates) — P1 confirmed

| Cell ID | Tip tape | YTD / prior | Seed action | Protect note |
| --- | --- | --- | --- | --- |
| `DOW_WED` | n=25 WR 40% ≈0R | YTD WR **29%** −0.29R · prior WR **12%** | **SOFT** | Stronger long than tip |
| `H1_JAN_APR` | — | prior n=68 WR **29%** −0.27R | **SOFT** seasonal · L3 tag | Never silent year-kill |
| `MONTH_JUL` | n=15 WR **20%** −0.51R | same | **SOFT** WR stress | Do not HARD on WR alone |
| `SPREAD_HIGH` | thr **≥30** · n=23 WR **39%** −0.03R | YTD n=25 ≈0R | **SOFT** | Tip spreads tight 27–31; thr=p80 floor 30 |
| `HOUR_18` | n=16 WR **38%** −0.07R | YTD WR **30%** −0.25R | **SOFT optional** | M5-native from tape — CF before arm |
| `OVERNIGHT_GAP` | nights share **55.8%** · win hold ≫ lose | long ~58% | **L8** advise | Not L2det first |
| `BUY_H1` | — | prior BUY WR ~30% | Optional H1 buy-caution | **Never** blanket skip all BUY |

---

## Protect cells (false-skip must be reported)

| Cell ID | Evidence | Rule |
| --- | --- | --- |
| `MONTH_MAY` | WR **67%** · E_N **+0.65R** · +$14.8 | Do not blanket-skip May |
| `DOW_MON` | Tip Mon WR **62%** · +$12.5 | Do not blanket-skip Mon |
| `SIDE_BUY_TIP` | Tip BUY WR **54%** · +$20.8 | No permanent sell-only without tape |

---

## Explicit non-cells (do not transplant)

| Foreign cell | Why rejected as M5 default |
| --- | --- |
| M15 `DOW_THU` / `HOUR_18` | Harvest M15 fingerprint — CF required before any M5 trial |
| EUR / AUD / DE40 / UK L2 pins | Wrong microstructure / session / TF |
| “Convert to trend” | Class is meanrev FIXED_RR_FADE |

---

## Scoring notes

- Skips must concentrate in seed cells; report precision vs losers and false-skip on protect cells.  
- Jul is WR-fragile but $-rescued — treat as SOFT until CF.  
- H1 cluster = **L3 regime** label on scorecards, not auto EXPANSION_DROP of tip sleeve.
