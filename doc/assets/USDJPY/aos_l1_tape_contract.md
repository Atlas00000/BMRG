# USDJPY — L1 tape / feature schema v0

**Task:** USDJPY-AOS-P1-T01  
**Status:** Schema frozen 2026-10-19  
**Engine:** Balanced P0 · magic **26101828** · AOS OFF  
**First tapes:** `tapes/usdjpy_tip_fire_tape_v0.csv` (May→Aug filter · **n=46**) · `tapes/usdjpy_ytd_fire_tape_v0.csv` (Jan→Oct filter · **n=54**) · `tapes/usdjpy_long_fire_tape_v0.csv` (n=63)  
**Source Tester window:** 2025.01.01 → 2026.10.18 (calendar-filtered; dedicated tip n=56 path differs)  
**Parents:** [`aios_roadmap.md`](./aios_roadmap.md) · [`aos_bad_cells.md`](./aos_bad_cells.md) · [`edge_framework.md`](./edge_framework.md)

L1 **perceives** fires for L2det / L2skip. It does not invent entries or change SL/TP.

---

## 1. Event grain

| Rule | Binding |
| --- | --- |
| Unit | One G0 fire = one row (ticket = event) |
| Open | `[BMRG][TRADE] OPEN` (Tester journal) |
| Close | TP / SL (EOT excluded from train labels; keep in freq) |
| Label `y_lose` | `1` if SL (lose), `0` if TP (win) — avoid-loser target |
| Identity | `magic-USDJPY-{side}-{YYYYMMDDhhmmss}` |

---

## 2. Feature schema v0

### 2.1 Required (train + shadow)

| Field | Type | Source | Notes |
| --- | --- | --- | --- |
| `open_time` | datetime | journal | Server time |
| `side` | {BUY,SELL} | OPEN | |
| `entry` / `sl` / `tp` | float | OPEN | Geometry audit (SL≈100 / TP≈120 pts) |
| `spread_pts` | int | OPEN `spread=` | Entry friction |
| `atr_pts` | float | bar ATR at signal | vs max **70** |
| `bbw_pct` | float | bar BBw | diagnostic (gate OFF) |
| `dow` | {Mon…Fri} | open_time | Tue expected absent |
| `hour` | 0–23 | open_time | Sleeve **12–19** entries |
| `month` | YYYY-MM | open_time | |
| `hold_h` | float | close−open | label-time only / not for live L1 |
| `exit_reason` | TP\|SL\|EOT | close | |
| `win` | 0\|1 | TP=1 | |
| `y_lose` | 0\|1 | 1−win | avoid-loser target |
| `pnl_R_design` | float | +1.20 / −1 | until deal R_real |
| `nights_held` | 0\|1 | hold≥12h | expect **rare** (session-bound) |
| `near_atr_cap` | 0\|1 | atr ≥ 0.9×70 | stress / FRAGILE residual |
| `ouroboros_tag` | MATCH\|FRAGILE\| | month map | soft L1 |
| `cell_dow_thu` | 0\|1 | dow==Thu | bad-cell |
| `cell_hour_14` | 0\|1 | hour==14 | bad-cell |
| `cell_month_jul` | 0\|1 | month==2026-07 | bad-cell L3 |
| `cell_sell` | 0\|1 | side==SELL | fire-heavy / thin edge |
| `cell_sell_near_atr` | 0\|1 | SELL ∧ near_atr | conjunction seed |
| `cell_fragile` | 0\|1 | ouroboros_tag==FRAGILE | context |

### 2.2 Metadata (every row)

| Field | Value |
| --- | --- |
| `symbol` | USDJPY |
| `magic` | 26101828 |
| `preset_id` | BMRG-M15-USDJPY-6M-P0_balanced_chart |
| `window` | e.g. 2026.05.01-2026.08.31 |
| `tf` | M15 |

### 2.3 Deferred (P1-T04+)

| Field | Why deferred |
| --- | --- |
| `band_ride_flag` | Needs MAE path / structure detector (P1-T04 optional) |
| `er_cell` / ATR tercile | Needs richer bar join |
| `exit_spread_pts` | Needs deal export |
| `c_R_event` | Needs measured costs |
| `session_age_min` | Easy add: minutes since 12:00 |

---

## 3. Train / score policy

| Item | Rule |
| --- | --- |
| Primary train window | Tip May→Aug **plus** YTD Jan→Oct (label Jul stress) |
| Holdout | Last 20% of tip chronologically **or** Aug stub — state on each model |
| Target | `y_lose` (avoid-loser) |
| Class weights | Balance wins/losses if needed |
| Forbidden features | Future info (`hold_h`, `exit_reason`) at **decision** time — train labels only |
| Forbidden models | EUR / UK / AUD / DE40 / AAPL L2 pins |
| Protect false-skip report | BUY · Mon · Fri · H15 · H18–19 · May–Jun |

---

## 4. Tape files

| File | Content |
| --- | --- |
| `tapes/usdjpy_tip_fire_tape_v0.csv` | Tip filter n=46 labeled fires |
| `tapes/usdjpy_ytd_fire_tape_v0.csv` | YTD filter n=54 labeled fires |
| `tapes/usdjpy_long_fire_tape_v0.csv` | Full source run n=63 |
| `tapes/usdjpy_tip_ytd_fire_tape_v0.csv` | Combined (dedupe by open_time+side) |
| `blotter/archive/USDJPY-AOS-P1/` | Builder + COST_PROXY + TAPE_QA + copies |

Builder: `blotter/archive/USDJPY-AOS-P1/build_usdjpy_m15_fire_tape.py`.  
Log source: Tester `logs/YYYYMMDD.log` (USDJPY chunks · magic 26101828).

---

## 5. Acceptance (schema)

- [x] Fields cover bad-cell registry seeds (Thu / H14 / Jul / SELL∧near_atr / FRAGILE / near_atr)  
- [x] Tip tape n=46 labeled (long-filter; baseline dedicated was 56 — path note)  
- [x] YTD tape n=54 labeled  
- [x] Long tape n=63 · atr_missing tip=0  
- [x] Ouroboros month tags (P1-T05)  
- [ ] Deal columns when export available  
- [ ] P1-T04 structure flags (optional · OPEN)

Bump to schema v1 when deal `c_R` or structure flags land.
