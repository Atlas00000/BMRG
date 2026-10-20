# AUDUSD M15 — L1 tape / feature schema v0

**Task:** AUDUSD-AOS-P1-T01  
**Status:** Schema frozen 2026-10-19  
**Engine:** CHAMP Harvest · magic **8230901** · AOS OFF · M15  
**First tapes:** `tapes/audusd_m15_tip_fire_tape_v0.csv` · `tapes/audusd_m15_long_fire_tape_v0.csv`  
**Parents:** [`aios_roadmap.md`](./aios_roadmap.md) · [`aos_bad_cells.md`](./aos_bad_cells.md) · [`edge_framework.md`](./edge_framework.md)

L1 **perceives** fires for L2det / L2skip. It does not invent entries or change SL/TP.

---

## 1. Event grain

| Rule | Binding |
| --- | --- |
| Unit | One G0 fire = one row (ticket = event) |
| Open | `[BMRG][TRADE] OPEN` |
| Close | TP / SL (EOT excluded from train labels) |
| Label `y_lose` | `1` if SL (lose), `0` if TP (win) — avoid-loser target |
| Identity | `8230901-AUDUSD-{side}-{YYYYMMDDhhmmss}` |

---

## 2. Feature schema v0

### 2.1 Required (train + shadow)

| Field | Type | Source | Notes |
| --- | --- | --- | --- |
| `open_time` | datetime | log | Server time |
| `side` | {BUY,SELL} | OPEN | |
| `entry` / `sl` / `tp` | float | OPEN | Geometry audit (300/300) |
| `spread_pts` | int | OPEN `spread=` | Entry friction |
| `atr_pts` | float | bar ATR at signal | no ATR max gate on CHAMP |
| `bbw_pct` | float | bar BBw | diagnostic |
| `dow` | {Mon…Fri} | open_time | Mon/Tue expected absent |
| `hour` | 0–23 | open_time | Sleeve 13–19 entries |
| `month` | YYYY-MM | open_time | |
| `hold_h` | float | close−open | label-time only / not for live L1 |
| `exit_reason` | TP\|SL\|EOT | close | |
| `win` | 0\|1 | TP=1 | |
| `y_lose` | 0\|1 | 1−win | avoid-loser target |
| `pnl_R_design` | float | +1 / −1 | until deal R_real |
| `nights_held` | 0\|1 | hold≥12h | **common** on winners |
| `near_atr_high` | 0\|1 | atr ≥ tip ATR p75 | stress proxy (no hard ATR max) |
| `regime_tag` | MATCH\|MISMATCH\| | month map | soft (P1-T05) |
| `cell_dow_thu` | 0\|1 | dow==Thu | bad-cell |
| `cell_month_may` | 0\|1 | month==*-05 | bad-cell |
| `cell_month_feb` | 0\|1 | month==*-02 | long L3 |
| `cell_month_mar` | 0\|1 | month==*-03 | long L3 |
| `cell_buy` | 0\|1 | side==BUY | mild caution (not tip-hostile) |
| `fast_lose` | 0\|1 | lose ∧ hold_h&lt;6 | structure (P1-T04) |
| `band_ride_proxy` | 0\|1 | lose ∧ hold_h&lt;8 | structure (P1-T04) |

### 2.2 Metadata (every row)

| Field | Value |
| --- | --- |
| `symbol` | AUDUSD |
| `magic` | 8230901 |
| `preset_id` | AUDUSD-CHAMP_Harvest_start13_skipMon_G0 |
| `window` | e.g. 2026.05.01-2026.08.31 |
| `tf` | M15 |

### 2.3 Deferred

| Field | Why deferred |
| --- | --- |
| MAE path / true band-ride | Needs tick path (future) |
| `exit_spread_pts` / `c_R_event` / `swap_ccy` | Deal export (measured Leak OPEN) |
| `session_age_min` | Easy add: minutes since 13:00 |

---

## 3. Train / score policy

| Item | Rule |
| --- | --- |
| Primary train window | Tip May→Aug **plus** long Jan→Aug when extended |
| Holdout | Last 20% of tip chronologically **or** Aug — state on each model |
| Target | `y_lose` (avoid-loser) |
| Forbidden at decision time | `hold_h`, `exit_reason`, `nights_held`, `fast_lose`, `band_ride_proxy` (label / offline only) |
| Forbidden models | EUR / UK / DE40 / live-M5 pin without CF |

---

## 4. Tape files

| File | Content |
| --- | --- |
| `tapes/audusd_m15_tip_fire_tape_v0.csv` | Tip n=41 labeled fires |
| `tapes/audusd_m15_long_fire_tape_v0.csv` | Long n=95 labeled fires |
| `tapes/audusd_m15_tip_long_fire_tape_v0.csv` | Combined (dedupe) |
| `blotter/archive/AUDUSD-AOS-P1/` | Builder + QA + copies |

Builder: `blotter/archive/AUDUSD-AOS-P1/build_audusd_m15_fire_tape.py`.

---

## 5. Acceptance (schema)

- [x] Fields cover bad-cell registry seeds (Thu / May / Feb / Mar)  
- [x] Tip + long tapes with win/side/dow/hour/ATR/spread/nights/regime  
- [x] P1-T04 structure proxies (`fast_lose`, `band_ride_proxy`)  
- [x] P1-T05 `regime_tag`  
- [ ] Deal columns when export available  

Bump to schema v1 when deal `c_R` / swap land.
