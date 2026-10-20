# Book A — Harvest (extract)

**Status:** research · presets shipped · log-scored 2026-10-06 · **not a live replace**  
**Created:** 2026-10-06  
**Family:** `meanrev` · sleeve: Harvest · **AOS OFF** (per-symbol AIOS later)  
**Framework:** score under `docs/framework/unified_edge_framework.md` (EF · E_N · MaxDD · n)  
**Authority for load:** `MQL5/Profiles/Tester/BMRG/` (twins of files below)

---

## Intent

Expand the **research asset list** by transferring champion Harvest **geometry** (not live magic / INF) across meanrev Tier-1 FX for independent Stage-0…4 work. Live FT stays on EURUSD `8210204` + INF LIVE_WITHHOLD.

| Order | Symbol | Preset | Magic |
| ---: | --- | --- | ---: |
| 1 | **EURUSD** | `BOOKA-Harvest_EURUSD_M5_G0.set` | **8221101** |
| 2 | **GBPUSD** | `BOOKA-Harvest_GBPUSD_M5_G0.set` | **8221102** |
| 3 | **AUDUSD** | `BOOKA-Harvest_AUDUSD_M5_G0.set` | **8221103** |

Per-asset docs live under `doc/assets/<SYM>/` — keep separate from root EURUSD `system_profile.md` / `doc/edge_framework.md`.  
AUDUSD: `doc/assets/AUDUSD/system_profile.md` · `edge_framework.md` · `edge_discovery.md` · **`candidate_pool.md`**.  
EDX presets: `Profiles/Tester/BMRG/AUDUSD/` (not mixed into EURUSD EDX).  
**AUDUSD EDX:** champion StartHour=13 + skip Mon · May→Aug E_N+0.404 · P8 Leak 2.44 pp · tip WATCH.  
**Research champ (AOS OFF):** `AUDUSD-CHAMP_Harvest_start13_skipMon_G0.set` · **8230901**.  
**AIOS FT (SIGNED 2026-10-08):** `AUDUSD-AIOS_LIVE_WITHHOLD_champ_G0.set` · **8230921** · n/G0–G5 not FT blockers · see `doc/assets/AUDUSD/AIOS_SIGNOFF.md`.

Do **not** mix these blotters with EDX champion `8210204` or INF LIVE_WITHHOLD runs.

---

## Locked geometry (all three)

| Field | Value | Note |
| --- | --- | --- |
| TF | **M5** | BMRG home |
| Event | **G0** MaxLevels=1 · MaxEntries=1 | One ticket ≈ one trade event |
| RR | **1.0** (SL 300 / TP 300 points) | BWR 50%; points transferred from EURUSD champ — recalibrate later if ATR mismatch |
| BB | period 20 · **BBDev 2.2** | |
| Session | **12:00–20:00** server | |
| Weekday | **skip Tue** | |
| `regime_filtered` | **true** | By design via session + Tue (metadata for G3) |
| Risk | Risk% **0.5** · equity base | |
| AOS | **OFF** · kill-switch on | Book A = engine extract only |

---

## Tester protocol (per symbol)

1. Expert: `Experts\BMRG\BMRG.ex5`  
2. Symbol / TF as in table · **every tick** · **ACCOUNT CURRENCY** (not pips)  
3. Window (aligned to Ouroboros bar tip): **2026.03.23 → 2026.09.21** (adjust To if history shorter)  
4. Load matching `Profiles\Tester\BMRG\BOOKA-Harvest_<SYM>_M5_G0.set`  
5. Export deals → `blotter/inbox/` · score EF / E_N / MaxDD / n · archive under `blotter/archive/BOOKA-<SYM>/`

Run **one symbol at a time**. Accept/reject each blotter before the next.

---

## Correlation caveat (accepted for research)

EURUSD / GBPUSD / AUDUSD are a **USD-fade cluster** (H1 ~30d ρ ≈ 0.65–0.83). Book A is for **per-symbol edge discovery**, not a diversified live book. Diversification engine is planned in Ouroboros `features.md` — do not treat three ACCEPT verdicts as independent Stage-3 capital.

---

## Out of scope (this book)

- AIOS / INF LIVE_WITHHOLD  
- Book B Survival geometry  
- Symbol-specific SL/TP ATR retune (follow-up if Leak or RR−R gap fails)  
- Multi-symbol simultaneous Tester / portfolio f
