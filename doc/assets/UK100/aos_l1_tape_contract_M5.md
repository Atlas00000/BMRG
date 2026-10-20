# UK100 M5 — L1 tape / feature schema v0

**Task:** UK100-M5-AOS-P1-T01  
**Status:** Schema frozen 2026-10-20  
**Engine:** Balanced P0 M5 · magic **26101905** · AOS OFF  
**First tape:** `tapes/uk100_m5_tip_fire_tape_v0.csv` (tip May→Aug · n=116)  
**Parents:** [`aios_roadmap_M5.md`](./aios_roadmap_M5.md) · [`aos_bad_cells_M5.md`](./aos_bad_cells_M5.md) · [`edge_framework.md`](./edge_framework.md)  
**Sibling:** M15 [`aos_l1_tape_contract.md`](./aos_l1_tape_contract.md) — do not merge rows or cell columns

L1 **perceives** M5 fires for L2det / L2skip. It does not invent entries or change SL/TP.

---

## 1. Event grain

| Rule | Binding |
| --- | --- |
| Unit | One G0 fire = one row (ticket = event) |
| Open | `[BMRG][TRADE] OPEN` (or deal export entry) |
| Close | TP / SL (EOT excluded from train labels; keep in freq) |
| Label `y_lose` | `1` if SL (lose), `0` if TP (win) — avoid-loser target |
| Identity | `magic-UK100-M5-{side}-{YYYYMMDDhhmmss}` |

---

## 2. Feature schema v0

### 2.1 Required (train + shadow)

| Field | Type | Source | Notes |
| --- | --- | --- | --- |
| `open_time` | datetime | blotter / log | Server time |
| `side` | {BUY,SELL} | OPEN | |
| `entry` / `sl` / `tp` | float | OPEN | Geometry audit (SL1800 / TP2250) |
| `spread_pts` | int | OPEN `spread=` | Entry friction |
| `atr_pts` | float | bar ATR at signal | vs max **869** |
| `bbw_pct` | float | bar BBw | diagnostic (gate OFF) |
| `dow` | {Mon…Fri} | open_time | Tue expected absent |
| `hour` | 0–23 | open_time | London sleeve 8–16 entries |
| `month` | YYYY-MM | open_time | |
| `hold_h` | float | close−open | label-time only / not for live L1 |
| `exit_reason` | TP\|SL\|EOT | close | |
| `win` | 0\|1 | TP=1 | |
| `pnl_R_design` | float | +1.25 / −1 | until deal R_real |
| `nights_held` | 0\|1 | hold≥12h | rare on UK100 M5 |
| `near_atr_cap` | 0\|1 | atr ≥ 0.9×**869** | stress feature |
| `ouroboros_tag` | MATCH\|FRAGILE\| | month map | soft / optional (P1-T05) |
| `cell_dow_mon` | 0\|1 | dow==Mon | bad-cell |
| `cell_hour_12_13` | 0\|1 | hour∈{12,13} | bad-cell |
| `cell_month_aug` | 0\|1 | month==2026-08 | bad-cell seed |
| `cell_month_feb` | 0\|1 | month==2026-02 | prior seed |
| `cell_month_apr` | 0\|1 | month==2026-04 | prior seed |
| `cell_buy` | 0\|1 | side==BUY | tip **protect** feature (not skip seed) |
| `cell_sell` | 0\|1 | side==SELL | side-caution candidate |

### 2.2 Metadata (every row)

| Field | Value |
| --- | --- |
| `symbol` | UK100 |
| `magic` | 26101905 |
| `preset_id` | BMRG-M5-UK100-6M-P0_balanced_chart |
| `window` | e.g. 2026.05.01-2026.08.31 |
| `tf` | M5 |

### 2.3 Deferred (P1-T04+)

| Field | Why deferred |
| --- | --- |
| `band_ride_flag` | Needs MAE path / structure detector (P1-T04 optional) |
| `er_cell` / ATR tercile | Needs richer bar join |
| `exit_spread_pts` | Needs deal export |
| `c_R_event` | Needs measured costs |
| `session_age_min` | Easy add: minutes since 08:00 |

### 2.4 Explicit non-columns (M15 imports)

Do **not** add `cell_dow_thu` / `cell_hour_08` / `cell_month_jul` as M5 skip seeds. Thu tip is neutral; H08–11 is protect; Jul overall tip is OK.

---

## 3. Train / score policy

| Item | Rule |
| --- | --- |
| Primary train window | Tip May→Aug **plus** prior Jan→Apr when tape extended |
| Holdout | Last 20% of tip chronologically **or** Aug-only — state on each model |
| Target | `y_lose` (avoid-loser) |
| Class weights | Balance wins/losses if needed |
| Forbidden features | Future info (hold_h, exit_reason) at **decision** time — train labels only |
| Forbidden models | EUR/AUD/AAPL/**M15 UK** L2 pins |

---

## 4. Tape files

| File | Content |
| --- | --- |
| `tapes/uk100_m5_tip_fire_tape_v0.csv` | Tip n=116 labeled fires |
| `tapes/uk100_m5_prior_fire_tape_v0.csv` | Prior Jan→Apr labeled fires (from long run) |
| `tapes/uk100_m5_tip_prior_fire_tape_v0.csv` | Combined tip+prior |
| `tapes/uk100_m5_long_fire_tape_v0.csv` | Full Jan→Aug long (diagnostic) |
| `blotter/archive/UK100-M5-AOS-P1/` | Builder + copies + TAPE_QA |

Builder: `blotter/archive/UK100-M5-AOS-P1/build_m5_fire_tape.py`.

---

## 5. Acceptance (schema + tapes)

- [x] Fields cover M5 bad-cell registry seeds  
- [x] Tip tape n=116 with win/side/dow/hour/ATR/spread  
- [x] Prior tape from long Jan→Apr  
- [x] `ouroboros_tag` on tip months (P1-T05)  
- [ ] `band_ride_flag` (P1-T04 optional — deferred)  
- [ ] Deal columns when export available  

Bump to schema v1 when deal `c_R` or structure flags land.
