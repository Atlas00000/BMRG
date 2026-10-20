# UK100-M5-AOS-P1 — REVIEW

**Task:** UK100-M5-AOS-P1 (T01–T03 · T05; T04 deferred)  
**Scored:** 2026-10-20  
**Verdict:** **ACCEPT** — L1 schema + tapes frozen · journal Leak_proxy landed · proceed P2  

---

## Deliverables

| Task | Artifact | Status |
| --- | --- | --- |
| P1-T01 | `doc/assets/UK100/aos_l1_tape_contract_M5.md` | DONE |
| P1-T02 | `build_m5_fire_tape.py` | DONE |
| P1-T03 | Tip / prior / long / tip_prior CSVs | DONE |
| P1-T04 | band_ride structure flags | DEFERRED |
| P1-T05 | `ouroboros_tag` on tip months | DONE (MATCH) |

### Asset tapes

| File | n |
| --- | ---: |
| `tapes/uk100_m5_tip_fire_tape_v0.csv` | 116 |
| `tapes/uk100_m5_prior_fire_tape_v0.csv` | 119 |
| `tapes/uk100_m5_long_fire_tape_v0.csv` | 235 |
| `tapes/uk100_m5_tip_prior_fire_tape_v0.csv` | 235 |

---

## QA (tip)

| Check | Result |
| --- | --- |
| n / WR / E_N | 116 / 52.6% / +0.183R |
| ATR present | 116/116 |
| Tue fires | 0 |
| Mon WR | 43.8% (n=32) |
| H12–13 WR | 40.4% (n=47) |
| Aug WR | 42.1% (n=38) |
| Protect Wed / H08–11 / BUY | 65.4% / 66.7% / 54.8% |
| near_atr_cap | 35 fires |
| Ouroboros tip | 116 MATCH |

## Cost proxy (interim OS)

| Metric | Value |
| --- | ---: |
| Spread med | 120 pts |
| Leak_proxy | **5.93 pp** |
| EF_proxy | **+2.22 pp** |
| Leak_prior / EF_prior | 4.0 / +4.1 pp |
| Measured | OPEN |

Zone remains **Positive** under journal proxy (thinner than prior).

---

## Next

`UK100-M5-AOS-P2-T01` ATR/Tue parity · `P2-T02` Mon ± H12–13 SOFT shadow CF.
