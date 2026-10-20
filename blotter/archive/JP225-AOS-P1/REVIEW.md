# JP225-AOS-P1 — L1 perception (fire tapes)

**Archived:** 2026-10-19  
**Engine:** Growth P1 · magic **26101904** · AOS OFF  
**Log:** `Tester/logs/20261019.log`  
**Schema:** `doc/assets/JP225/aos_l1_tape_contract.md`  
**Builder:** `build_jp225_m15_fire_tape.py`

## Tasks

| Task | Status |
| --- | --- |
| P1-T01 schema v0 | **DONE** |
| P1-T02 builder | **DONE** |
| P1-T03 labels (win/DOW/hour/side/ATR/spread/month) | **DONE** |
| P1-T04 structure flags | **OPEN** (optional) |
| P1-T05 Ouroboros month tags | **DONE** on tape |

## Tape counts

| Tape | n | Path |
| --- | ---: | --- |
| Tip May→Aug | **79** | `tapes/jp225_tip_fire_tape_v0.csv` |
| Jan→Aug | **143** | `tapes/jp225_janaug_fire_tape_v0.csv` |
| Long 2025→tip | **360** | `tapes/jp225_long_fire_tape_v0.csv` |
| Tip∪JanAug | 143 | `tapes/jp225_tip_janaug_fire_tape_v0.csv` |

## Tip QA highlights

| Slice | n | WR | E_N |
| --- | ---: | ---: | ---: |
| ALL | 79 | 43.0% | +0.08R |
| BUY | 31 | **48.4%** | **+0.21R** |
| SELL | 48 | 39.6% | −0.01R |
| Wed | 20 | **30.0%** | **−0.25R** |
| MATCH | 23 | **52.2%** | **+0.30R** |
| MISMATCH | 13 | 30.8% | −0.23R |
| May FRAGILE | 23 | 30.4% | −0.24R |
| near_atr_cap | 10 | **60.0%** | **+0.50R** |
| H08 / H14 | 8 / 22 | 25% / 36% | soft hours |

Med hold: win **1.48h** · lose **0.77h** · nights_held share **8.9%**.

## Cost proxy (journal — not measured)

| Field | Value |
| --- | ---: |
| Entry spread med / mean | **1400** / 1546 pts |
| Leak_proxy (2×med/SL) | **4.82 pp** |
| EF_proxy | −1.78 pp |
| Leak_prior / EF_prior | 4.3 pp / **−1.26 pp** |

Prior remains Stage-1 authority until deal export. Tester spreads understate live ~2300.

## Verdict

**P1 ACCEPT** — tapes + schema frozen · bad-cells updated (Wed / H08 / H14 / SELL-caution; near_atr **protect** alone).  
**Next:** JP225-AOS-P2 L2det CF (May → Jul → Wed → hours → SELL∧cell).  
P1-T04 structure flags remain optional OPEN.
