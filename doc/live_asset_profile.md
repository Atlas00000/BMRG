# BMRG — Live Asset Profile (first VPS book)

**Version:** 0.2.0  
**Status:** Operator inventory — first EA live set + **GRP-P5 capital map**  
**As of:** 2026-10-22 · hosting `6917926` · account `28435`  
**Authority blotter:** [`blotter/archive/LIVE-20261021/REVIEW.md`](../blotter/archive/LIVE-20261021/REVIEW.md) · grouping [`GRP-P5-T01`](../blotter/archive/GRP-P5-T01/REVIEW.md)  
**Grouping roadmap:** [`asset_grouping_roadmap.md`](./asset_grouping_roadmap.md)  
**Canvas:** `bmrg-live-asset-profile.canvas.tsx` · champions `bmrg-group-champions.canvas.tsx` (display only)

This document freezes the **first live book** attached to BMRG on the VPS. Magics, presets, and geometry below are the attach contract. Tip / OS metrics are research evidence — they do **not** auto-admit PRODUCTION-WORTHY unless scored under the asset edge framework.

**Canvas ≠ verdict.** If numbers here disagree with a scored blotter or live Inputs, the blotter / Inputs win.

---

## 0. Book summary

| Field | Value |
| --- | --- |
| Charts / EAs | **7 / 7** |
| Cutover | 2026-10-20 ~16:38 — M15 index/equity → **M5 stacks**; USDJPY stayed **M15** |
| Risk (all current attaches) | **0.5%** |
| AOS mode (all) | **LIVE_WITHHOLD** · L3/L4 on · L2 AI **DISARM** |
| Production capital path | **EURUSD M5 INF** · **AUDUSD M5** (see §2 — currently FT twin, not SCALE) |
| Research OS on VPS | Apple · UK100 · JPN225 · DE30 · USDJPY |

### Bucket split

| Bucket | Symbols | Posture |
| --- | --- | --- |
| **Production live** | EURUSD | Harvest INF champion · magic `8210204` |
| **Live FX twin (size caution)** | AUDUSD | On VPS as FT twin `8230921` @ 0.5% — SCALE `8230931` @ 3% is signed but **not** currently attached |
| **Research OS / expansion** | Apple, UK100, JPN225, DE30, USDJPY | HITL-armed stacks · not FX-book replace · G4/G5 deferred |

---

## 1. Fleet table (attach identity)

| # | Broker symbol | Doc alias | TF | Magic | Preset | Risk | Class |
| ---: | --- | --- | --- | ---: | --- | ---: | --- |
| 1 | EURUSD | EURUSD | M5 | **8210204** | `LIVE-SHADOW_EURUSD_M5.set` (from 2026-10-29 · full inputs) | 0.5% | Production INF |
| 2 | AUDUSD | AUDUSD | M5 | **8230931** | `LIVE-SHADOW_AUDUSD_M5.set` (SHADOW · from 2026-10-29) | 3.0% | SCALE (VPS since 2026-10-21) |
| 3 | Apple | AAPL | M5 | **26162017** | `AAPL_5m_stack.set` (skips enforced — kept) | 0.5% | Research OS |
| 4 | UK100 | UK100 | M5 | **26121907** | `LIVE-SHADOW_UK100_M5.set` (SHADOW · from 2026-10-29) | 0.5% | Research OS |
| 5 | JPN225 | JP225 | M5 | **26161907** | `JPN225_5m_stack.set` (skips enforced — kept) | 0.5% | Research OS |
| 6 | DE30 | DE40 | M5 | **26151907** | `LIVE-SHADOW_DE30_M5.set` (SHADOW · from 2026-10-29) | 0.5% | Research OS |
| 7 | USDJPY | USDJPY | M15 | **26131807** | `USDJPYstack.set` (skips enforced — kept) | 0.5% | Research OS |

Posture decided 2026-10-29 · all charts on EA **1.28** · scorecard [`LIVE_SCORECARD.md`](LIVE_SCORECARD.md).

**Aliases:** broker `Apple` ↔ AAPL · `DE30` ↔ DE40 · `JPN225` ↔ JP225.

---

## 2. Asset cards

### 2.1 EURUSD — production INF

| | |
| --- | --- |
| **Role** | Primary FX production book |
| **Preset** | `doc/presets/LIVE-SHADOW_EURUSD_M5.set` (2026-10-29 · full 120 inputs from VPS dump · was `INF-LIVE_WITHHOLD_Harvest_long_ddl30.set`) · scorecard `doc/LIVE_SCORECARD.md` |
| **Magic / TF** | **8210204** · M5 |
| **Geometry** | SL/TP **300/300** · RR 1.0 · BB(20, 2.2) |
| **Session** | 12–20 · skip Tue |
| **Risk / f** | 0.5% |
| **AOS** | ON · **SHADOW** (L2 AI logs would-skip, does not withhold) · W250 · ddl 30% · gate-block logging ON |
| **L2 pin** | `L2skip_inf_p92_20260927_223519` — shadow only; retrain NO_SHIP (`blotter/archive/INF-L2-RETRAIN-20261029/`) · retrain after ≥150 shadow-logged outcomes |
| **Leak / BWR** | 2.2 pp / 50% (meta) |
| **Engine baseline** | long n=530 · WR 54.5% · E_N +0.091R · EF **1.77** pp · Fragile vs M (`doc/ai_OS_baseline.md`) |
| **Recent tip** | n=49 · WR 59.2% · E_N +0.184R · EF **6.43** pp |
| **Framework** | `doc/edge_framework.md` · root Harvest champion |
| **Not** | M15 EURUSD P7 research OS (`26121807`) |

### 2.2 AUDUSD — FT twin on VPS (SCALE signed separately)

| | |
| --- | --- |
| **Role** | Parallel FX sleeve · Track B AIOS |
| **Attached now** | `AUDUSD-AIOS_LIVE_WITHHOLD_champ_G0.set` · magic **8230921** · Risk **0.5%** |
| **Signed SCALE (not on VPS now)** | `AUDUSD-AIOS_SCALE_Risk3_champ_G0.set` · **8230931** · Risk **3%** (`AIOS_SIGNOFF.md` 2026-10-08) |
| **Geometry** | SL/TP **300/300** · RR 1.0 · StartHour **13** · skip Mon/Tue |
| **AOS** | ON · LIVE_WITHHOLD · W250 |
| **L2 pin** | `L2skip_aud_p90_20261008_122523` |
| **Leak / BWR** | 2.4 pp / 50% |
| **Framework** | `doc/assets/AUDUSD/edge_framework.md` · sign-off `AIOS_SIGNOFF.md` |
| **Ops note** | Confirm whether VPS should stay on FT twin or reload SCALE Risk3 |

### 2.3 Apple (AAPL) — M5 research OS

| | |
| --- | --- |
| **Role** | Equity CFD expansion · tip_WATCH pool |
| **Preset** | `AAPL_5m_stack.set` · magic **26162017** |
| **Engine freeze** | Balanced P0 M5 · magic 26102011 |
| **Geometry** | SL **190** / TP **280** · RR ≈1.47 · BB(20, 2.5) |
| **Session** | 14–20 · skip Tue · MaxSpread 40 |
| **ATR / BBw** | 24–98 · 0.30–2.00% |
| **L2det** | `L2det_aapl_m5_v1b` LIVE_WITHHOLD (Jul ∨ Wed) · L2 AI DISARM |
| **Leak / BWR** | **15.3** pp (profile authority) / 40.4% |
| **Tip engine** | n=77 · WR 46.8% · E_N +0.16R · Stage-1 Fragile under true Leak |
| **Tip OS (P4 det)** | n_fire=41 · WR 53.7% · E_N **+0.327R** · life NEAR · EF_profile −2.1 pp |
| **Verdict** | ARM_RESEARCH_OS · HITL 2026-10-20 |
| **Framework** | `doc/assets/AAPL/edge_framework.md` |

### 2.4 UK100 — M5 research OS

| | |
| --- | --- |
| **Role** | Index expansion (FTSE) |
| **Preset** | `UK100_5m_stack.set` · magic **26121907** |
| **Engine freeze** | Balanced P0 M5 · 26101905 |
| **Geometry** | SL **1800** / TP **2250** · RR 1.25 |
| **Session** | 08–17 · skip Tue · ATR max **869** |
| **L2det** | `L2det_uk_m5_v1b` ((Mon∧H12-13)∨(SELL∧H12-13)) · L2 AI DISARM |
| **Leak / BWR** | **5.93** pp (journal proxy) / 44.4% |
| **Tip engine** | n=116 · WR 52.6% · E_N +0.183R · EF_journal +2.22 pp |
| **Tip OS (v1b)** | n_fire=83 · WR 61.5% · E_N **+0.383R** · EF +11.1 pp · life EXPANDING |
| **Verdict** | ARM_RESEARCH_OS |
| **Framework** | `doc/assets/UK100/edge_framework.md` |

### 2.5 JPN225 (JP225) — M5 research OS

| | |
| --- | --- |
| **Role** | Nikkei expansion · Growth geometry |
| **Preset** | `JPN225_5m_stack.set` · magic **26161907** |
| **Engine freeze** | Growth P0 M5 · 26101906 |
| **Geometry** | SL **25000** / TP **50000** · RR 2.00 |
| **Session** | 08–17 · skip Tue · ATR **7610–11285** · MaxSpread 3000 |
| **L2det** | `L2det_jp225_m5_v1c` · L2 AI DISARM |
| **Leak / BWR** | **3.3** pp prior / 33.3% |
| **Tip engine** | n=94 · WR 41.5% · E_N +0.245R · EF_prior +4.9 pp |
| **Tip OS (v1c)** | n_fire=69 · WR 49.3% · E_N **+0.478R** · EF_prior +12.6 pp · life EXPANDING |
| **Verdict** | ARM_RESEARCH_OS |
| **Framework** | `doc/assets/JP225/edge_framework.md` |

### 2.6 DE30 (DE40) — M5 research OS

| | |
| --- | --- |
| **Role** | DAX expansion |
| **Preset** | `DE40_5m_stack.set` · magic **26151907** |
| **Engine freeze** | Balanced P0 M5 · 26101903 |
| **Geometry** | SL **7000** / TP **8750** · RR 1.25 |
| **Session** | 08–17 · skip Tue · ATR max **2380** · MaxSpread 1500 |
| **L2det** | `L2det_de40_m5_v1b` ((BUY∧H14\|16)∨(BUY∧Oct)) · L2 AI DISARM |
| **Leak / BWR** | **7.0** pp prior / 44.4% |
| **Tip engine** | n=123 · WR 53.7% · E_N +0.207R · EF_prior +2.2 pp |
| **Tip OS (P4)** | n_fire=104 · WR 57.7% · E_N **+0.298R** · EF_prior +6.2 pp · life STABLE |
| **Verdict** | ARM_RESEARCH_OS |
| **Framework** | `doc/assets/DE40/edge_framework.md` |
| **Not** | M15 `DE40stack` magic `26141907` |

### 2.7 USDJPY — M15 research OS

| | |
| --- | --- |
| **Role** | FX expansion · only M15 sleeve in this book |
| **Preset** | `USDJPYstack.set` · magic **26131807** |
| **Engine freeze** | Balanced P0 M15 · 26101828 |
| **Geometry** | SL **100** / TP **120** · RR 1.20 · BB 2.2 |
| **Session** | 12–20 · skip Tue · ATR max **70** |
| **L2det** | `L2det_usdjpy_v1c` (nearATR∨H16) · L2 AI DISARM |
| **Leak / BWR** | **11.4** pp prior / 45.5% |
| **Tip engine (path)** | n=46 · WR 50% · E_N +0.10R · EF_prior −6.9 pp |
| **Tip OS (v1c offline)** | n_fire=37 · WR 62.2% · E_N **+0.368R** · EF +5.3 pp |
| **Verdict** | ACCEPT_ARM_RESEARCH_OS · HITL 2026-10-19 |
| **Framework** | `doc/assets/USDJPY/edge_framework.md` |

---

## 3. Tip OS expectancy board (research evidence)

Comparable tip windows from P7 promotion packets / INF baseline (not same calendar for every asset).

| Asset | Window note | Engine E_N | OS fire E_N | Leak (pp) | OS posture |
| --- | --- | ---: | ---: | ---: | --- |
| EURUSD | Harvest tip / long | +0.091 (long) | +0.184 (tip) | 2.2 | Production INF |
| AUDUSD | AIOS FT / SCALE docs | — | LIVE pin W250 | 2.4 | FT twin on VPS |
| Apple | May→Oct tip | +0.160 | +0.327 | 15.3 | Fragile Stage-1 |
| UK100 | May→Aug tip | +0.183 | +0.383 | 5.93 | EXPANDING |
| JPN225 | May→Oct tip | +0.245 | +0.478 | 3.3 | EXPANDING |
| DE30 | May→Oct tip | +0.207 | +0.298 | 7.0 | STABLE |
| USDJPY | tip path / v1c | +0.100 | +0.368 | 11.4 | OS lifts EF>0 |

---

## 4. Shared live ops rules

1. **One magic per chart** — never mix blotters across magics in this table.  
2. **G0** — MaxLevels=1 · MaxEntries=1 on all live attaches.  
3. **L2 AI stays DISARM** on research stacks; L2det LIVE_WITHHOLD only.  
4. **Daily loss halt** is account-level — one sleeve’s SL cluster can pause others (seen 2026-10-21 after UK100/DE30).  
5. **Semver mismatch** warnings (`*_DISARM` input vs baked L2det) are expected on armed stacks — EA uses baked coeffs.  
6. **Not in this book:** GBP pairs, US30, XAU, other US names, AUD M15 `8231941`, EURUSD M15 P7.

---

## 5. Doc map

| Asset | Edge framework | Roadmap / sign-off | Preset path |
| --- | --- | --- | --- |
| EURUSD | `doc/edge_framework.md` | `doc/ai_OS_baseline.md` | `doc/presets/INF-LIVE_*` |
| AUDUSD | `doc/assets/AUDUSD/edge_framework.md` | `AIOS_SIGNOFF.md` | `doc/presets/AUDUSD-AIOS_*` |
| AAPL | `doc/assets/AAPL/` | `AAPL-M5-AOS-P7` | `Presets/AAPL_5m_stack.set` |
| UK100 | `doc/assets/UK100/` | `UK100-M5-AOS-P7` | `Presets/UK100_5m_stack.set` |
| JP225 | `doc/assets/JP225/` | `JP225-M5-AOS-P7` | `Presets/JPN225_5m_stack.set` |
| DE40 | `doc/assets/DE40/` | `DE40-M5-AOS-P7` | `Presets/DE40_5m_stack.set` |
| USDJPY | `doc/assets/USDJPY/` | `USDJPY-AOS-P7` | `Presets/USDJPYstack.set` |

---

## 6. Capital / group map (GRP-P5)

**Authority:** [`blotter/archive/GRP-P5-T01/DECISION.json`](../blotter/archive/GRP-P5-T01/DECISION.json)  
**Panel:** tip 6m 2026.05.01→2026.10.20 · designed R · equal weights  
**Not:** live `f` raise · auto VPS detach of non-cluster sleeves without operator confirm

### 6.1 Primary cluster

| Field | Value |
| --- | --- |
| Group | **JP225 + DE40** |
| Policy | `max_sum_R` (Pareto) |
| Weights | equal **50 / 50** |
| Magics | JP225 `26161907` · DE40 `26151907` |
| Tip metrics | m_hit 1.0 · q_hit 1.0 · sum_R **+31.0** · maxDD −2.5 · Sep–Oct +3.0 · tail 0.33 |
| EURUSD | Remains **standalone production** (not inside this cluster) |

### 6.2 Alternate policy menu

| Group | Policy | When to use |
| --- | --- | --- |
| DE40+USDJPY | max_holdout_val | Prefer Sep–Oct resilience |
| JP225+USDJPY | best_CVaR | Prefer path / shallow DD |
| EURUSD+DE40+USDJPY+AAPL | min_maxDD | Need EUR inside cluster; keep AAPL light |
| USDJPY+UK100 | min_tail | Watch only — UK halt history |

### 6.3 VPS attach posture (primary map)

| Sleeve | Posture | Note |
| --- | --- | --- |
| EURUSD | **full** | Production INF |
| JP225 | **full** | Primary cluster |
| DE40 | **full** | Primary cluster |
| USDJPY | **light** | Optional for alternate maps |
| AAPL | **light** | Only if min_maxDD map selected |
| UK100 | **cf_pending_L3v1c** | Dual-window BELOW retune (EA≥1.25) · re-CF magic 26121907 — see `doc/UK100_L3_RETUNE_CF.md` |
| AUDUSD | **ft_twin_only** | Hard-ban with EUR in groups; not SCALE in clusters |

Hard ban remains **EURUSD+AUDUSD** full-weight in any group.

---

## 7. Change log

| Ver | Date | Note |
| --- | --- | --- |
| 0.1.0 | 2026-10-21 | First live book freeze from hosting logs + P7 packets · AUDUSD observed as FT twin |
| 0.2.0 | 2026-10-22 | GRP-P5 capital map · primary JP225+DE40 · attach postures |
| 0.2.1 | 2026-10-22 | UK100 L3v1c dual-window BELOW retune (EA 1.25) · CF pending `doc/UK100_L3_RETUNE_CF.md` |
