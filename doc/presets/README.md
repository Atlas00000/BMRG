# BMRG — significant presets (doc copies)

Project overview / testing doctrine: [`../../README.md`](../../README.md).

**Purpose:** In-repo snapshots of the presets that define baseline, aistack paper OS, and INF stack.  
**Canonical load path for Strategy Tester:** `MQL5/Profiles/Tester/BMRG/*.set`  
**These files:** documentation / diff / audit copies under `Experts/BMRG/doc/presets/`. Prefer regenerating from Profiles if they drift.

Tester: EURUSD **M5** · every tick · **ACCOUNT CURRENCY**. Expert: `Experts\BMRG\BMRG.ex5`.

---

## Index

| Role | File | Magic | Stack |
| --- | --- | --- | --- |
| **Harvest champion (engine baseline)** | `EDX-P2-T04_SL300_TP300_RR1_champFilters_G0_long.set` | **8210204** | Engine only · SL300/TP300 · 12–20 · skip Tue · G0 |
| EDX discovery baseline (pre-champ) | `EDX-P0-T01_baseline_G0-EF-G1_EURUSD-M5_long.set` | 8210001 | Engine · early EF-G1 lock |
| Growth sleeve (secondary ref) | `EDX-P4-T01_champion_T05_currency_G0_long.set` | 8210401 | Engine · not OS/INF default |
| AOS L0 baseline lock | `AOS-P0-T01_L0_baselineLock_Harvest_long.set` | 8310001 | AOS phase lock on Harvest geometry |
| **aistack (paper OS)** | `aistack.set` | **8399001** | AOS overlay · **STAY_PAPER** — not INF live wiring |
| aistack Harvest long twin | `AOS_aistack_Harvest_long.set` | 8399001 | Same family · Harvest long window framing |
| **INF LIVE_WITHHOLD** | `INF-LIVE_WITHHOLD_Harvest_long.set` | **8210204** | AOS ON · `InpAiOsMode=2` · baked L2 INF pin |
| INF LIVE_WITHHOLD · ddl30 | `INF-LIVE_WITHHOLD_Harvest_long_ddl30.set` | **8210204** | Same as LIVE_WITHHOLD · `InpMaxDailyLossPct=30` |
| INF export-only (no AI gate) | `EXP-P7-T03_export_Harvest_long.set` | 8210205 | Blotter refresh · engine logic unchanged |

Locked metrics for Harvest engine: `infra/baselines/ENGINE_BASELINE_v1.json` · `doc/ai_OS_baseline.md` (EF **1.77** · n **530** · E_N **+0.091R**).

---

## How to use

1. **Run in Tester** — load the twin under `Profiles/Tester/BMRG/` (MetaTrader only sees that tree).
2. **Diff / review** — compare against the copy here after any preset edit.
3. **Do not** treat `aistack` / `AOS_aistack_*` as INF wiring authority (`doc/infrascaleup.md`, `doc/aos_aistack.md`).
4. **INF ship path** — `INF-LIVE_WITHHOLD_Harvest_long.set` + EA ≥ v1.21; pin `L2skip_inf_p92_20260927_223519`.

---

## Sync note

If Profiles and `doc/presets/` disagree, **Profiles wins for execution**; update this folder to match and note the change in the task archive.
