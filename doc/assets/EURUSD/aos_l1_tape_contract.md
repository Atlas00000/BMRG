# EURUSD M15 — L1 tape / feature schema v0

**Task:** EURUSD-AOS-P1-T01  
**Status:** Schema frozen 2026-10-18  
**Engine:** P2 light · magic **26101817** · AOS OFF  
**First tapes:** `tapes/eurusd_m15_tip_fire_tape_v0.csv` · `tapes/eurusd_m15_ytd_fire_tape_v0.csv`  
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
| Identity | `magic-EURUSD-{side}-{YYYYMMDDhhmmss}` |

---

## 2. Feature schema v0

### 2.1 Required (train + shadow)

| Field | Type | Source | Notes |
| --- | --- | --- | --- |
| `open_time` | datetime | blotter / log | Server time |
| `side` | {BUY,SELL} | OPEN | |
| `entry` / `sl` / `tp` | float | OPEN | Geometry audit (300/375) |
| `spread_pts` | int | OPEN `spread=` | Entry friction |
| `atr_pts` | float | bar ATR at signal | vs max **74** |
| `bbw_pct` | float | bar BBw | diagnostic (gate OFF) |
| `dow` | {Mon…Fri} | open_time | Tue expected absent |
| `hour` | 0–23 | open_time | Sleeve 12–19 entries |
| `month` | YYYY-MM | open_time | |
| `hold_h` | float | close−open | label-time only / not for live L1 |
| `exit_reason` | TP\|SL\|EOT | close | |
| `win` | 0\|1 | TP=1 | |
| `y_lose` | 0\|1 | 1−win | avoid-loser target |
| `pnl_R_design` | float | +1.25 / −1 | until deal R_real |
| `nights_held` | 0\|1 | hold≥12h | **common** on this sleeve |
| `near_atr_cap` | 0\|1 | atr ≥ 0.9×74 | stress feature |
| `ouroboros_tag` | MATCH\|FRAGILE\| | month map | soft / optional |
| `cell_dow_thu` | 0\|1 | dow==Thu | bad-cell |
| `cell_hour_13` | 0\|1 | hour==13 | bad-cell |
| `cell_hour_19` | 0\|1 | hour==19 | bad-cell (thin) |
| `cell_month_feb` | 0\|1 | month==2026-02 | YTD L3 |
| `cell_month_aug` | 0\|1 | month==2026-08 | tip soft |
| `cell_buy` | 0\|1 | side==BUY | tip-hostile caution |

### 2.2 Metadata (every row)

| Field | Value |
| --- | --- |
| `symbol` | EURUSD |
| `magic` | 26101817 |
| `preset_id` | BMRG-M15-EURUSD-6M-P2_light_selective_chart |
| `window` | e.g. 2026.05.01-2026.10.17 |
| `tf` | M15 |

### 2.3 Deferred (P1-T04+)

| Field | Why deferred |
| --- | --- |
| `band_ride_flag` | Needs MAE path / structure detector (P1-T04 optional) |
| `er_cell` / ATR tercile | Needs richer bar join |
| `exit_spread_pts` | Needs deal export |
| `c_R_event` / `swap_ccy` | Needs measured costs (overnight-heavy) |
| `session_age_min` | Easy add: minutes since 12:00 |

---

## 3. Train / score policy

| Item | Rule |
| --- | --- |
| Primary train window | Tip May→Oct **plus** YTD Jan→Oct when extended |
| Holdout | Last 20% of tip chronologically **or** Sep–Oct — state on each model |
| Target | `y_lose` (avoid-loser) |
| Class weights | Balance wins/losses if needed |
| Forbidden features | Future info (`hold_h`, `exit_reason`, `nights_held`) at **decision** time — train labels only |
| Forbidden models | M5 / AUD / UK100 / AAPL L2 pins |

---

## 4. Tape files

| File | Content |
| --- | --- |
| `tapes/eurusd_m15_tip_fire_tape_v0.csv` | Tip n≈45 labeled fires |
| `tapes/eurusd_m15_ytd_fire_tape_v0.csv` | YTD n≈72 labeled fires |
| `tapes/eurusd_m15_tip_ytd_fire_tape_v0.csv` | Combined (dedupe by open_time+side) |
| `blotter/archive/EURUSD-AOS-P1/` | Builder + QA + copies |
| Future | deal-enriched tape when export lands |

Builder: `blotter/archive/EURUSD-AOS-P1/build_eurusd_m15_fire_tape.py`.

---

## 5. Acceptance (schema)

- [x] Fields cover bad-cell registry seeds (BUY / Thu / H13·H19 / Feb / Aug / near_atr)  
- [x] Tip + YTD tapes with win/side/dow/hour/ATR/spread/nights/ouroboros  
- [ ] P1-T04 structure flags (optional · deferred)  
- [ ] Deal columns when export available  

Bump to schema v1 when deal `c_R` / swap or structure flags land.
