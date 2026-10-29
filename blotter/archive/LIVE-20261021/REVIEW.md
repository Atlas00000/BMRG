# LIVE-20261021 — VPS live book inventory (from hosting logs)

**task_id:** LIVE-20261021  
**kind:** VPS attach inventory from MetaQuotes hosting journals (not a full day P&L scorecard)  
**as_of:** 2026-10-21T16:57:19+01:00  
**account:** `28435` · hosting `6917926`  
**sources:** `logs/hosting.6917926.experts/{20261020,20261021}.log` · `logs/hosting.6917926.terminal/20261021.log`  
**verdict:** LOGGED — 7 charts / 7 EAs live; M5 cutover confirmed 2026-10-20 16:38  
**archived_at:** 2026-10-21T16:57:19+01:00  
**profile:** [`doc/live_asset_profile.md`](../../../doc/live_asset_profile.md) · canvas `bmrg-live-asset-profile.canvas.tsx`

Inbox empty — inventory scored from synced hosting logs only.

---

## Terminal posture

| Field | Value |
| --- | --- |
| Charts / EAs | **7 / 7** (stable through 17:38 hosting) |
| Signal | disabled |
| Ping | ~1.22 ms Access Server UK 1 |

**Cutover (2026-10-20 ~16:38):** M15 book removed → reloaded as **M5 stacks** for Apple / UK100 / JPN225 / DE30 / AUDUSD / EURUSD; **USDJPY stayed M15**.

---

## Live book (n=7) — observed init

| # | Symbol (VPS) | TF | Magic | Risk % | AOS | L2 mode | Model (baked / active) | Canonical preset |
| ---: | --- | --- | ---: | ---: | --- | --- | --- | --- |
| 1 | **EURUSD** | M5 | **8210204** | 0.50 | ON | LIVE_WITHHOLD | `L2skip_inf_p92_20260927_223519` | `INF-LIVE_WITHHOLD_Harvest_long_ddl30.set` |
| 2 | **AUDUSD** | M5 | **8230921** | 0.50 | ON | LIVE_WITHHOLD | `L2skip_aud_p90_20261008_122523` | `AUDUSD-AIOS_LIVE_WITHHOLD_champ_G0.set` (FT twin) |
| 3 | **Apple** | M5 | **26162017** | 0.50 | ON | LIVE_WITHHOLD | baked `L2det_aapl_m5_v1b_20261020` (input DISARM mismatch → baked) | `AAPL_5m_stack.set` |
| 4 | **UK100** | M5 | **26121907** | 0.50 | ON | LIVE_WITHHOLD | baked `L2det_uk_v1b_20261012` | `UK100_5m_stack.set` |
| 5 | **JPN225** | M5 | **26161907** | 0.50 | ON | LIVE_WITHHOLD | baked `L2det_jp225_m5_v1c_20261020` | `JPN225_5m_stack.set` |
| 6 | **DE30** | M5 | **26151907** | 0.50 | ON | LIVE_WITHHOLD | baked `L2det_de40_m5_v1b_20261020` | `DE40_5m_stack.set` |
| 7 | **USDJPY** | M15 | **26131807** | 0.50 | ON | LIVE_WITHHOLD | baked `L2det_usdjpy_v1c_near_atr_OR_H16_20261019` | `USDJPYstack.set` |

All inits: `fade=0`, G0-style single-level posture in bar logs.

---

## Delta vs LIVE-20261019

| Item | 2026-10-19 (declared) | 2026-10-21 (logs) |
| --- | --- | --- |
| Index / equity TF | mostly M15 | **M5 stacks** (except USDJPY M15) |
| AUDUSD magic | **8230931** SCALE Risk 3% | **8230921** FT twin Risk **0.5%** |
| EURUSD | M5 INF and/or M15 P7 | **M5 INF only** (`8210204`) |
| Apple | M15 Harvest `26092501` AOS OFF | **M5** `26162017` AOS ON stack |
| UK100 / JP / DE | M15 P7 magics | **M5** stack magics (`26121907` / `26161907` / `26151907`) |

---

## Today activity snapshot (2026-10-21 hosting)

| Time (hosting) | Event |
| --- | --- |
| 11:25 | DE30 SELL 0.1 @ 25413.81 → SL close 11:35 |
| 11:25 | UK100 SELL 0.1 @ 10738.28 → SL ~11:33 |
| ~11:35+ | UK100 / DE30 / JPN225 / USDJPY often **daily loss halt** |
| 15:45 | EURUSD SELL 0.01 @ 1.12369 (open into session; still open in last experts bars ~17:50 as SELL n=1) |
| 16:55–17:05 | Apple entries blocked `AOS L2DET_AAPL_M5_WED` |

---

## Ops flags

1. **AUDUSD is not SCALE Risk3** on VPS right now — FT twin **8230921** @ 0.5%. Confirm intentional vs `8230931`.
2. Several M5 stacks log **semver mismatch** (input `*_DISARM` vs baked L2det) — EA uses baked coeffs; expected for armed stacks.
3. Shared **daily loss halt** after UK100/DE30 SL cluster — expected account-level fuse behaviour.
4. Symbol aliases: broker **Apple** / **DE30** / **JPN225** ↔ docs AAPL / DE40 / JP225.

---

## Verdict

**LOGGED** — current VPS live set = `{EURUSD M5, AUDUSD M5, Apple M5, UK100 M5, JPN225 M5, DE30 M5, USDJPY M15}` with magics/presets above.
