# AUDUSD_AOS_BASELINE_v1 — engine freeze (OS compare)

**Version:** 1.0 · **Locked:** 2026-10-19  
**Task:** AUDUSD-AOS-P0-T01  
**Parents:** [`aios_roadmap.md`](./aios_roadmap.md) · [`system_profile.md`](./system_profile.md)

---

## Identity

| Field | Value |
| --- | --- |
| Sleeve | CHAMP Harvest · research engine |
| Magic | **8230901** |
| AOS | **OFF** |
| Preset | `Profiles/Tester/BMRG/AUDUSD/AUDUSD-CHAMP_Harvest_start13_skipMon_G0.set` |
| TF (OS primary) | **M15** |
| Geometry | SL/TP **300/300** · BBDev **2.2** · Start**13**–20 · skip Mon/Tue · Risk **0.5%** |
| Deposit (Tester) | **$400** · every tick · ACCOUNT CURRENCY |
| Evidence | `Tester/logs/20261019.log` · `blotter/archive/AUDUSD-M15-EXP/` |

**Not this baseline:** live **8230931** · FT **8230921** · Book A **8221103** · DE30 magics.

---

## Scoreboard (FIXED_RR R=1 · BWR 50%)

| Window | N | WR | BM | E_N† | Final | Δ$ | W20 min→last | path DD~ | Max L |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- | ---: | ---: |
| **Tip May→Aug 2026** | **41** | **63.4%** | **+13.4 pp** | **+0.268R** | **533.27** | **+$133.27** | 50→**75** | **3.0%** | 4 |
| Support Jan→Aug 2026 | 95 | 56.8% | +6.8 pp | +0.137R | 549.30 | +$149.30 | 40→75 | 4.4% | 7 |

† E_N = 2·WR − 1 (journal FIXED_RR). Leak / EF pending measured costs — see [`aos_cost_policy.md`](./aos_cost_policy.md).

**OS compare window (default):** **tip May→Aug**. State the window on every task. Jan→Aug = survival / L3 diagnostics.

---

## Supporting M5 context (not OS baseline)

| Source | N | WR | E_N | Note |
| --- | ---: | ---: | ---: | --- |
| EDX-P5 champ tip (M5) | ~47 | 70.2% | +0.404R | Geometry parent |
| Book A 8221103 tip (M5) | 58 | 62.1% | +0.241R | Pre-champ |

---

## Freeze rules

1. Do not change SL/TP/BBDev/session/weekday as an “OS” move.  
2. OS experiments use overlay magics **82319xx** / separate `.set` — engine compare stays **8230901**.  
3. Tip-only charts never promote a layer.  
4. Soft months (May, Feb/Mar) are regime cells — see [`aos_bad_cells.md`](./aos_bad_cells.md).
