# DE40 — L1 tape / feature schema v0

**Task:** DE40-AOS-P1-T01  
**Status:** Schema frozen 2026-10-19  
**Engine:** Balanced P0 · magic **26101902** · AOS OFF · MT5 **DE30**  
**First tapes:** `tapes/de40_tip_fire_tape_v0.csv` (May→Oct · n=77) · `tapes/de40_ytd_fire_tape_v0.csv` (Jan→Oct · n=147)  
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
| Identity | `magic-DE30-{side}-{YYYYMMDDhhmmss}` |

---

## 2. Feature schema v0

### 2.1 Required (train + shadow)

| Field | Type | Source | Notes |
| --- | --- | --- | --- |
| `open_time` | datetime | journal | Server time |
| `side` | {BUY,SELL} | OPEN | |
| `entry` / `sl` / `tp` | float | OPEN | Geometry audit (SL≈5000 / TP≈6250 pts) |
| `spread_pts` | int | OPEN `spread=` | Entry friction |
| `atr_pts` | float | bar ATR at signal | vs max **4070** |
| `bbw_pct` | float | bar BBw | diagnostic (gate OFF) |
| `dow` | {Mon…Fri} | open_time | Tue expected absent |
| `hour` | 0–23 | open_time | Cash sleeve 8–16 entries |
| `month` | YYYY-MM | open_time | |
| `hold_h` | float | close−open | label-time only / not for live L1 |
| `exit_reason` | TP\|SL\|HALT\|EOT | close | HALT = daily-loss flatten (y_lose=1) |
| `win` | 0\|1 | TP=1 | |
| `pnl_R_design` | float | +1.25 / −1 | until deal R_real |
| `nights_held` | 0\|1 | hold≥12h | expect rare on cash sleeve |
| `near_atr_cap` | 0\|1 | atr ≥ 0.9×4070 | stress / FRAGILE residual |
| `ouroboros_tag` | MATCH\|MISMATCH\|FRAGILE\| | month map | soft L1 |
| `cell_month_feb` | 0\|1 | month==2026-02 | bad-cell |
| `cell_month_mar` | 0\|1 | month==2026-03 | bad-cell |
| `cell_mismatch` | 0\|1 | ouroboros_tag==MISMATCH | bad-cell |
| `cell_fragile` | 0\|1 | ouroboros_tag==FRAGILE | bad-cell |
| `cell_near_atr` | 0\|1 | near_atr_cap | bad-cell conjunction |

### 2.2 Metadata (every row)

| Field | Value |
| --- | --- |
| `symbol` | DE30 |
| `magic` | 26101902 |
| `preset_id` | BMRG-M15-DE40-6M-P0_balanced_chart |
| `window` | e.g. 2026.05.01-2026.10.18 |
| `tf` | M15 |

### 2.3 Deferred (P1-T04+)

| Field | Why deferred |
| --- | --- |
| `band_ride_flag` | Needs MAE path / structure detector (P1-T04 optional) |
| `er_cell` / ATR tercile | Needs richer bar join |
| `exit_spread_pts` | Needs deal export |
| `c_R_event` | Needs measured costs |
| `session_age_min` | Easy add: minutes since 08:00 |
| DOW/hour cell flags | Seed after tip tape QA (update `aos_bad_cells.md`) |

---

## 3. Train / score policy

| Item | Rule |
| --- | --- |
| Primary train window | Tip May→Oct **plus** YTD Jan→Oct (label stress months) |
| Holdout | Last 20% of tip chronologically **or** Sep–Oct — state on each model |
| Target | `y_lose` (avoid-loser) |
| Class weights | Balance wins/losses if needed |
| Forbidden features | Future info (`hold_h`, `exit_reason`) at **decision** time — train labels only |
| Forbidden models | EUR / UK / USDJPY / AUD / AAPL L2 pins |

---

## 4. Tape files

| File | Content |
| --- | --- |
| `tapes/de40_tip_fire_tape_v0.csv` | Tip n=77 labeled fires |
| `tapes/de40_ytd_fire_tape_v0.csv` | YTD n=147 labeled fires |
| `tapes/de40_tip_ytd_fire_tape_v0.csv` | Combined (dedupe by open_time+side) |
| `blotter/archive/DE40-AOS-P1/` | Builder + COST_PROXY + copies |
| Optional | `de40_stub2025_fire_tape_v0.csv` (MISMATCH footnote) |

Builder: `blotter/archive/DE40-AOS-P1/build_de40_m15_fire_tape.py`.  
Log source: Tester `logs/20261019.log` (DE30 chunks · magic 26101902).

---

## 5. Acceptance (schema)

- [x] Fields cover bad-cell registry seeds (Feb / Mar / MISMATCH / FRAGILE / near_atr)  
- [x] Tip tape n=77 with win/side/dow/hour/ATR/spread  
- [x] YTD tape n=147  
- [x] Ouroboros month tags (P1-T05)  
- [ ] Deal columns when export available  
- [ ] P1-T04 structure flags (optional · OPEN)

Bump to schema v1 when deal `c_R` or structure flags land.
