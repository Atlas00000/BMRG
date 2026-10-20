# DE40 M5 — L1 tape / feature schema v0

**Task:** DE40-M5-AOS-P1-T01  
**Status:** Schema frozen 2026-10-20  
**Engine:** Balanced P0 · magic **26101903** · AOS OFF · MT5 **DE30** · **M5**  
**First tapes:** `tapes/de40_m5_tip_fire_tape_v0.csv` (May→Oct · n=123) · `tapes/de40_m5_ytd_fire_tape_v0.csv` (Jan→Oct · n=208) · tip-core / prior / sep–oct siblings  
**Parents:** [`aios_roadmap_M5.md`](./aios_roadmap_M5.md) · [`aos_bad_cells_M5.md`](./aos_bad_cells_M5.md) · [`edge_framework.md`](./edge_framework.md)  
**Sibling:** [`aos_l1_tape_contract.md`](./aos_l1_tape_contract.md) (M15) — do not mix pins / ATR caps

L1 **perceives** fires for L2det / L2skip. It does not invent entries or change SL/TP.

---

## 1. Event grain

| Rule | Binding |
| --- | --- |
| Unit | One G0 fire = one row |
| Open | `[BMRG][TRADE] OPEN` (Tester journal) |
| Close | TP / SL (EOT excluded from train labels; keep in freq) |
| Label `y_lose` | `1` if SL (lose), `0` if TP (win) — avoid-loser target |
| Identity | `magic-DE30-M5-{side}-{YYYYMMDDhhmmss}` |

---

## 2. Feature schema v0

### 2.1 Required (train + shadow)

| Field | Type | Source | Notes |
| --- | --- | --- | --- |
| `open_time` | datetime | journal | Server time |
| `side` | {BUY,SELL} | OPEN | |
| `entry` / `sl` / `tp` | float | OPEN | Geometry audit (SL≈7000 / TP≈8750 pts) |
| `spread_pts` | int | OPEN `spread=` | Entry friction |
| `atr_pts` | float | bar ATR at signal | vs max **2380** |
| `bbw_pct` | float | bar BBw | diagnostic (gate OFF) |
| `dow` | {Mon…Fri} | open_time | Tue expected absent |
| `hour` | 0–23 | open_time | Cash sleeve 8–16 entries |
| `month` | YYYY-MM | open_time | |
| `hold_h` | float | close−open | label-time only / not for live L1 |
| `exit_reason` | TP\|SL\|HALT\|EOT | close | HALT = daily-loss flatten (y_lose=1) |
| `win` | 0\|1 | TP=1 | |
| `pnl_R_design` | float | +1.25 / −1 | until deal R_real |
| `nights_held` | 0\|1 | hold≥12h | tip nights share ~14% |
| `near_atr_cap` | 0\|1 | atr ≥ 0.9×2380 | stress / FRAGILE residual |
| `ouroboros_tag` | MATCH\|MISMATCH\|FRAGILE\| | month map | soft L1 |
| `cell_month_feb` | 0\|1 | month==2026-02 | bad-cell |
| `cell_month_may` | 0\|1 | month==2026-05 | bad-cell |
| `cell_mismatch` | 0\|1 | ouroboros_tag==MISMATCH | bad-cell |
| `cell_fragile` | 0\|1 | ouroboros_tag==FRAGILE | bad-cell |
| `cell_near_atr` | 0\|1 | near_atr_cap | conjunction only |
| `cell_buy` / `cell_sell` | 0\|1 | side | |

### 2.2 Metadata (every row)

| Field | Value |
| --- | --- |
| `symbol` | DE30 |
| `magic` | 26101903 |
| `preset_id` | BMRG-M5-DE40-6M-P0_balanced_chart |
| `window` | e.g. 2026.05.01-2026.10.19 |
| `tf` | M5 |

### 2.3 Deferred (P1-T04+)

| Field | Why deferred |
| --- | --- |
| `band_ride_flag` | Needs MAE path / structure detector (P1-T04 optional) |
| `exit_spread_pts` / `c_R_event` | Needs deal export |
| `session_age_min` | Easy add: minutes since 08:00 |
| DOW/hour cell flags | Seeded after tip tape QA → update `aos_bad_cells_M5.md` |

---

## 3. Train / score policy

| Item | Rule |
| --- | --- |
| Primary train window | Tip May→Oct **plus** YTD Jan→Oct (label stress months) |
| Holdout | Last 20% of tip chronologically **or** Sep–Oct — state on each model |
| Target | `y_lose` (avoid-loser) |
| Forbidden features | Future info (`hold_h`, `exit_reason`) at **decision** time |
| Forbidden models | M15 `L2det_de` / EUR / UK / USDJPY / AUD / AAPL pins |

---

## 4. Tape files

| File | Content |
| --- | --- |
| `tapes/de40_m5_tip_fire_tape_v0.csv` | Tip May→Oct n=123 |
| `tapes/de40_m5_ytd_fire_tape_v0.csv` | YTD Jan→Oct n=208 |
| `tapes/de40_m5_tip_core_fire_tape_v0.csv` | May→Aug n=94 |
| `tapes/de40_m5_prior_fire_tape_v0.csv` | Jan→Apr n=82 |
| `tapes/de40_m5_sep_oct_fire_tape_v0.csv` | Sep–Oct n=29 |
| `tapes/de40_m5_tip_prior_fire_tape_v0.csv` | Tip + prior combined |
| `blotter/archive/DE40-M5-AOS-P1/` | Builder · COST_PROXY · TAPE_QA · copies |

Builder: `blotter/archive/DE40-M5-AOS-P1/build_de40_m5_fire_tape.py`.  
Log source: Tester `logs/20261020.log` (DE30 M5 · magic 26101903 · tip/YTD to **2026.10.19**).

---

## 5. QA gates (P1 exit)

| Check | Result (2026-10-20) |
| --- | --- |
| Tip n ≥ 30 | **PASS** n=123 |
| Tue_n == 0 | **PASS** |
| atr_missing == 0 | **PASS** |
| ouroboros_nonempty == n | **PASS** |
| Leak journal ≠ Stage-1 | **PASS** — prior 7.0 pp authority |
