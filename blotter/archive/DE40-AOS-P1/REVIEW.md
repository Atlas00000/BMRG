# DE40-AOS-P1 — L1 perception

**Date:** 2026-10-19  
**Tasks:** P1-T01 schema · P1-T02 builder · P1-T03 labels · P1-T05 Ouroboros tags · P1-T04 optional OPEN  
**Verdict:** **P1 DONE** — tip n=77 · YTD n=147 · bad-cells updated · journal Leak_proxy only  
**Next:** deal export (measured Leak) · P2-T01/T02 Feb±H13 shadow CF

## Artifacts

| File | Role |
| --- | --- |
| `build_de40_m15_fire_tape.py` | Journal → tapes |
| `de40_tip_fire_tape.csv` / `de40_ytd_fire_tape.csv` | Archive copies |
| `COST_PROXY.json` | Tip journal 2×spread Leak_proxy ≈1.5 pp (not Stage-1) |
| `TAPE_QA.json` | Side / DOW / hour / month slices |
| `doc/assets/DE40/tapes/*_v0.csv` | Canonical tapes |
| `doc/assets/DE40/aos_l1_tape_contract.md` | Schema |

## Tip fingerprint (for P2)

- Sell-led (SELL WR 62.5% / E_N +0.41R · BUY 54% / +0.22R)  
- Stars: Mon · H08 · H12 · H14 · Aug  
- Soft: H13 · Wed (weak) · Feb (YTD)  
- 2 YTD HALT flattens (daily-loss) labeled as losers  
- Tue n=0 (filter OK)

## Cost note

Journal median entry spread **84 pts** ≪ live ~1020 — **do not** replace Leak prior 9.8 pp with proxy for Stage-1 / P7.
