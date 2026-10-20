# USDJPY-AOS-P1 — L1 perception

**Date:** 2026-10-19  
**Tasks:** P1-T01 schema · P1-T02 builder · P1-T03 labels · P1-T05 Ouroboros tags · P1-T04 optional OPEN  
**Verdict:** **P1 DONE** — tip n=46 · YTD n=54 · long n=63 · journal Leak_proxy only  
**Next:** deal export (measured Leak) · P2-T01/T02 (Jul ± near_atr first; Thu path-sensitive)

## Artifacts

| File | Role |
| --- | --- |
| `build_usdjpy_m15_fire_tape.py` | Journal → tapes |
| `usdjpy_tip_fire_tape.csv` / `ytd` / `long` / `tip_ytd` | Archive copies |
| `COST_PROXY.json` | Tip journal 2×spread Leak_proxy ≈3.6 pp (**not** Stage-1) |
| `TAPE_QA.json` | Side / DOW / hour / month slices |
| `doc/assets/USDJPY/tapes/*_v0.csv` | Canonical tapes |
| `doc/assets/USDJPY/aos_l1_tape_contract.md` | Schema |

## Source windows (log)

| Tester run | Magic | Final | Used as |
| --- | ---: | ---: | --- |
| **2025.01.01 → 2026.10.18** | 26101828 | 521.87 | **Source** (filter tip/YTD by open_time) |
| 2025.05.01 → 2026.08.31 | 26101828 | 512.77 | Alternate (not selected) |

Dedicated May→Aug / Jan→Oct runs were not present; calendar filters applied on the long chunk.

## Tip fingerprint (for P2) — filtered May→Aug from long

| Metric | Tape | Dedicated baseline (P0) |
| --- | ---: | ---: |
| n | **46** | 56 |
| WR / E_N | **50.0%** / **+0.10R** | 48.2% / +0.061R |
| BUY | 18 / 55.6% / +0.22R | buy-led |
| SELL | 28 / 46.4% / +0.02R | sell-heavy / thin |
| **Jul** | 14 / **28.6%** / **−0.37R** | **still soft** |
| Thu | 9 / 55.6% / +0.22R | was soft on dedicated — **path flip** |
| **near_atr_cap** | 7 / **0%** / −1.0R | strong SOFT seed |
| H16 | 3 / 0% | thin soft |
| Tue | 0 | filter OK |
| atr_missing | 0 | |

**Read:** Jul + near_atr remain robust bad cells across path. Thu/Mon DOW ranks flipped vs dedicated tip — do **not** hard-arm Thu from this tape alone; shadow CF vs both fingerprints.

## Cost note

Journal median entry spread **4 pts** → Leak_proxy ≈ **3.6 pp** ≪ prior **11.4 pp**.  
**Do not** replace Leak prior with proxy for Stage-1 / P7. Prior remains authority until deal export.
