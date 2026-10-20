# AUDUSD-AOS-P1 — L1 perception

**Done:** 2026-10-19  
**Engine:** CHAMP **8230901** · M15 · AOS OFF  
**Log:** `Tester/logs/20261019.log`

## Tasks

| Task | Status |
| --- | --- |
| P1-T01 schema | **DONE** `doc/assets/AUDUSD/aos_l1_tape_contract.md` |
| P1-T02 builder | **DONE** `build_audusd_m15_fire_tape.py` |
| P1-T03 labels | **DONE** tip n=**41** · long n=**95** · atr_missing=0 |
| P1-T04 structure | **DONE** proxies `fast_lose` · `band_ride_proxy` |
| P1-T05 regime | **DONE** `regime_tag` MATCH/MISMATCH |

## Tape QA (tip)

| Cell | n | WR | E_N |
| --- | ---: | ---: | ---: |
| All | 41 | **63.4%** | **+0.268** |
| Thu | 10 | 40.0% | −0.20 |
| May | 9 | 44.4% | −0.11 |
| fast_lose | 9 | 0% | −1.0 |
| MATCH / MISMATCH | 32 / 9 | — | — |
| nights_held | 58.5% | — | — |

## Cost proxy (journal · not measured)

| Metric | Value |
| --- | ---: |
| spread med | 15 pts |
| Leak_proxy (2×med/SL/(R+1)) | **5.0 pp** |
| Leak_prior (P8) | 2.4 pp |
| EF_proxy / EF_prior | +8.4 / +11.0 pp |
| Leak_source | `journal_2x_entry_spread_median` |

Measured deal Leak still **OPEN**.

## Artifacts

- `doc/assets/AUDUSD/tapes/audusd_m15_*_fire_tape_v0.csv`
- `TAPE_QA.json` · `COST_PROXY.json`

**Verdict:** P1 **ACCEPT** · next **P2-T01/T02** (Thu SOFT shadow).  
Live **8230931** untouched.
