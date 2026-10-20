# EURUSD-AOS-P1 — L1 perception

**task_id:** EURUSD-AOS-P1  
**archived_at:** 2026-10-18T15:50:00+01:00  
**engine:** P2 light · magic **26101817** · AOS OFF  
**verdict:** P1 DONE (T04 optional open) — schema + tip/YTD tapes + Ouroboros tags · journal Leak proxy closed  

## Deliverables

| Task | Artifact | Status |
| --- | --- | --- |
| P1-T01 | `doc/assets/EURUSD/aos_l1_tape_contract.md` | DONE |
| P1-T02 | `build_eurusd_m15_fire_tape.py` | DONE |
| P1-T03 | tip n=45 · YTD n=72 labeled · atr_missing=0 | DONE |
| P1-T04 | band-ride structure flags | OPEN (optional) |
| P1-T05 | `ouroboros_tag` on tape | DONE · tip MATCH 43 / FRAGILE 2 |

## Tapes

| File | n |
| --- | ---: |
| `doc/assets/EURUSD/tapes/eurusd_m15_tip_fire_tape_v0.csv` | 45 |
| `doc/assets/EURUSD/tapes/eurusd_m15_ytd_fire_tape_v0.csv` | 72 |
| `doc/assets/EURUSD/tapes/eurusd_m15_tip_ytd_fire_tape_v0.csv` | 72 unique |

## Cell QA (tip) — confirms bad-cell seeds

| Cell | n | WR | E_N |
| --- | ---: | ---: | ---: |
| BUY | 23 | 39.1% | −0.12R |
| Thu | 8 | 37.5% | −0.16R |
| H13 | 8 | 37.5% | −0.16R |
| H19 | 3 | 33.3% | −0.25R |
| Aug | 7 | 42.9% | −0.04R |
| near_atr | 17 | **47.1%** | +0.06R → blanket DISARM |
| nights_held | 75.6% | — | swap unpaid in proxy |

## Cost proxy (bonus · advances P0-T03)

| Metric | Value |
| --- | ---: |
| spread median | 4 pts |
| Leak_proxy | **1.19 pp** |
| EF_proxy | **+1.04 pp** |
| vs prior EF | −0.7 pp (prior was pessimistic) |
| measured+swap | **OPEN** |

## Next

P2-T01 ATR/Tue parity · P2-T02 Thu ± H13/H19 SOFT shadow CF.  
Do not arm L2 LIVE on proxy alone. Do not blanket near_atr or BUY.
