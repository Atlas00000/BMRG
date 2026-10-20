# AUDUSD candidate pool (EDX handoff)

**Updated:** 2026-10-19 · **AUDUSD LIVE = AIOS SCALE Risk 3%** magic **8230931**  
**Research champ:** magic **8230901** AOS OFF · **FT twin (0.5%):** magic **8230921**  
**AIOS build:** [`aios_roadmap.md`](./aios_roadmap.md) — M15 research OS (arm mag **8231941** at P7) · Track B live L2 retrain  
**EURUSD live** `8210204` remains the production INF book — AUDUSD is a parallel live sleeve, not a replace.

## Admission labels

| Label | Meaning |
| --- | --- |
| **EXPANSION_KEEP** | Research sleeve; beat baseline on primary window; tip L3 OK |
| **WATCH** | Positive but Fragile / tip leak / thin n |
| **DROP** | Rejected for class / payoff / filter |
| **AIOS_FT** | Signed FT twin (Risk 0.5%) — not live size |
| **AIOS_LIVE** | AUDUSD live attach (Risk 3%) |

## Pool

| ID | Sleeve | Magic | Window scored | E_N | EF | Label | Notes |
| --- | --- | ---: | --- | ---: | ---: | --- | --- |
| BOOKA base | Start12 · Mon on · skip Tue · 300/300 | 8221103 | Book A protocol | — | — | WATCH | Harvest extract; AOS OFF |
| P0-T01 | Same as Book A geom | 8230101 | May→Aug | +0.241 | +4.57† | EXPANSION_KEEP | Baseline locked |
| P0-T04 | P0 tip | 8230104 | May→Oct | +0.123 | −1.34† | WATCH | Sep L3 |
| **CHAMP** | **Start13 · skip Mon · skip Tue · 300/300** | **8230901** | **May→Aug** | **+0.404** | **+17.78‡** | **EXPANSION_KEEP ★** | Research engine · AOS OFF |
| Champ tip | Same stack | 8230502 / 8230802 | May→Oct | +0.213 | +8.16‡ | WATCH | Sep L3 −0.636R |
| Champ long | Same stack | 8230601 / 8230803 | Mar23→Sep21 | +0.151 | +5.10‡ | WATCH | tip tax noted |
| **AIOS FT** | Champ + AOS · Risk **0.5%** · W250 · L2 AUD | **8230921** | — | — | — | **AIOS_FT** | Retained FT twin |
| **AIOS LIVE** | Same · **Risk 3%** | **8230931** | RISK3-Q | — | — | **AIOS_LIVE ★** | `AUDUSD-AIOS_SCALE_Risk3_champ_G0` · signed 2026-10-08 |

†Leak proxy `costs_defaulted` (3×spread).  
‡P8 policy: entry-spread `c_R` only (commission/swap/slip absent).

## Rejected / skipped

| Path | Verdict |
| --- | --- |
| P2 payoff SL/TP variants | REJECT — keep 300/300 |
| P3 extras beyond Start13 + skipMon | REJECT / no delta |
| R-side / AL hypothesis | REJECT |
| **P8-T03 ATR gate** | **SKIP** — no n≥30 BM≤0 cell on champ |

## Frozen champion inputs (research engine)

```
InpStartHour=13
InpEndHour=20
InpTradeMon=false
InpTradeTue=false
InpSL_Points=300
InpTP_Points=300
InpUseATRRegime=false
AOS=OFF   # research 8230901 only
```

| Role | Path | Magic |
| --- | --- | ---: |
| Research champion | `Profiles/Tester/BMRG/AUDUSD/AUDUSD-CHAMP_Harvest_start13_skipMon_G0.set` | **8230901** |
| **AUDUSD LIVE (Risk 3%)** | `Profiles/Tester/BMRG/AUDUSD/AUDUSD-AIOS_SCALE_Risk3_champ_G0.set` | **8230931** |
| AIOS FT twin (Risk 0.5%) | `Profiles/Tester/BMRG/AUDUSD/AUDUSD-AIOS_LIVE_WITHHOLD_champ_G0.set` | **8230921** |
| Doc twins | `doc/presets/AUDUSD-CHAMP_*` · `doc/presets/AUDUSD-AIOS_*` | same |
| Book A baseline harvest | `BOOKA-Harvest_AUDUSD_M5_G0.set` | 8221103 |

Primary research window: **2026.05.01 → 2026.08.31**.

## AIOS boundary (signed)

**2026-10-08 live:** AUDUSD on **8230931** · Risk **3%** · **W250** · AUD L2 · `AUDUSD-AIOS_SCALE_Risk3_champ_G0`.  
**FT twin:** **8230921** @ 0.5% retained for compare.  
**Not blockers:** n, full `G0∧G1∧…∧G5`.  
**Still true:** research **8230901** stays AOS OFF; EURUSD INF L2 untouched; AUD L2 AUC weak — monitor / retrain when tape grows.  
Detail: [`AIOS_SIGNOFF.md`](./AIOS_SIGNOFF.md).
