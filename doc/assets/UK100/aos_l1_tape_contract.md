# UK100 — L1 tape / feature schema v0

**Task:** UK100-AOS-P1-T01  
**Status:** Schema frozen 2026-10-12  
**Engine:** Balanced P0 · magic **26101201** · AOS OFF  
**First tape:** `tapes/uk100_tip_fire_tape_v0.csv` (tip May→Aug · n=51)  
**Parents:** [`aios_roadmap.md`](./aios_roadmap.md) · [`aos_bad_cells.md`](./aos_bad_cells.md) · [`edge_framework.md`](./edge_framework.md)

L1 **perceives** fires for L2det / L2skip. It does not invent entries or change SL/TP.

---

## 1. Event grain

| Rule | Binding |
| --- | --- |
| Unit | One G0 fire = one row (ticket = event) |
| Open | `[BMRG][TRADE] OPEN` (or deal export entry) |
| Close | TP / SL (EOT excluded from train labels; keep in freq) |
| Label `y_lose` | `1` if SL (lose), `0` if TP (win) — avoid-loser target |
| Identity | `magic-UK100-{side}-{YYYYMMDDhhmmss}` |

---

## 2. Feature schema v0

### 2.1 Required (train + shadow)

| Field | Type | Source | Notes |
| --- | --- | --- | --- |
| `open_time` | datetime | blotter / log | Server time |
| `side` | {BUY,SELL} | OPEN | |
| `entry` / `sl` / `tp` | float | OPEN | Geometry audit |
| `spread_pts` | int | OPEN `spread=` | Entry friction |
| `atr_pts` | float | bar ATR at signal | vs max 1470 |
| `bbw_pct` | float | bar BBw | diagnostic (gate OFF) |
| `dow` | {Mon…Fri} | open_time | Tue expected absent |
| `hour` | 0–23 | open_time | London sleeve 8–16 entries |
| `month` | YYYY-MM | open_time | |
| `hold_h` | float | close−open | label-time only / not for live L1 |
| `exit_reason` | TP\|SL\|EOT | close | |
| `win` | 0\|1 | TP=1 | |
| `pnl_R_design` | float | +1.25 / −1 | until deal R_real |
| `nights_held` | 0\|1 | hold≥12h | rare on UK100 |
| `near_atr_cap` | 0\|1 | atr ≥ 0.9×1470 | stress feature |
| `ouroboros_tag` | MATCH\|FRAGILE\| | month map | soft / optional |
| `cell_dow_thu` | 0\|1 | dow==Thu | bad-cell |
| `cell_hour_08` | 0\|1 | hour==8 | bad-cell |
| `cell_month_jul` | 0\|1 | month==2026-07 | seed; prefer ATR path later |
| `cell_buy` | 0\|1 | side==BUY | tip-hostile caution |

### 2.2 Metadata (every row)

| Field | Value |
| --- | --- |
| `symbol` | UK100 |
| `magic` | 26101201 |
| `preset_id` | BMRG-M15-UK100-6M-P0_balanced_chart |
| `window` | e.g. 2026.05.01-2026.08.31 |
| `tf` | M15 |

### 2.3 Deferred (P1-T04+)

| Field | Why deferred |
| --- | --- |
| `band_ride_flag` | Needs MAE path / structure detector |
| `er_cell` / ATR tercile | Needs richer bar join |
| `exit_spread_pts` | Needs deal export |
| `c_R_event` | Needs measured costs |
| `session_age_min` | Easy add: minutes since 08:00 |

---

## 3. Train / score policy

| Item | Rule |
| --- | --- |
| Primary train window | Tip May→Aug **plus** prior Jan→Apr when tape extended |
| Holdout | Last 20% of tip chronologically **or** Aug-only — state on each model |
| Target | `y_lose` (avoid-loser) |
| Class weights | Balance wins/losses if needed |
| Forbidden features | Future info (hold_h, exit_reason) at **decision** time — train labels only |
| Forbidden models | EUR/AUD/AAPL L2 pins |

---

## 4. Tape files

| File | Content |
| --- | --- |
| `tapes/uk100_tip_fire_tape_v0.csv` | Tip n=51 labeled fires |
| `tapes/uk100_prior_fire_tape_v0.csv` | Prior n=75 labeled fires |
| `tapes/uk100_tip_prior_fire_tape_v0.csv` | Combined n=126 |
| `blotter/archive/UK100-AOS-P0-T03/` | Builder + COST_PROXY + copies |
| Future | `uk100_hist_fire_tape_v0.csv` |

Builder: `blotter/archive/UK100-AOS-P0-T03/build_tip_cost_and_tape.py`.

---

## 5. Acceptance (schema)

- [x] Fields cover bad-cell registry seeds  
- [x] Tip tape n=51 with win/side/dow/hour/ATR/spread  
- [x] Prior tape n=75 appended  
- [ ] Deal columns when export available  

Bump to schema v1 when deal `c_R` or structure flags land.
