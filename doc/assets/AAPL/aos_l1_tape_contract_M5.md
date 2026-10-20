# AAPL M5 — L1 tape / feature schema v0

**Task:** AAPL-M5-AOS-P1-T01  
**Status:** Schema frozen 2026-10-20  
**Engine:** Balanced TPgtSL · magic **26102011** · AOS OFF · MT5 **Apple** · **M5**  
**First tapes:** `tapes/aapl_m5_tip_fire_tape_v0.csv` (May→Oct · n=77) · `tapes/aapl_m5_ytd_fire_tape_v0.csv` (Jan→Oct · n=145) · prior / tip-core / long / sep–oct siblings  
**Parents:** [`aios_roadmap_M5.md`](./aios_roadmap_M5.md) · [`aos_bad_cells_M5.md`](./aos_bad_cells_M5.md) · [`edge_framework.md`](./edge_framework.md)  
**Sibling:** M15 Harvest tape (if any) — do not mix pins / SL190 vs M15 SL300

L1 **perceives** fires for L2det / L2skip. It does not invent entries or change SL/TP.

---

## 1. Event grain

| Rule | Binding |
| --- | --- |
| Unit | One G0 fire = one row |
| Open | `[BMRG][TRADE] OPEN` (Tester journal) |
| Close | TP / SL (EOT excluded from train labels; keep in freq) |
| Label `y_lose` | `1` if SL (lose), `0` if TP (win) — avoid-loser target |
| Identity | `magic-Apple-M5-{side}-{YYYYMMDDhhmmss}` |

---

## 2. Feature schema v0

### 2.1 Required (train + shadow)

| Field | Type | Source | Notes |
| --- | --- | --- | --- |
| `open_time` | datetime | journal | Server time |
| `side` | {BUY,SELL} | OPEN | |
| `entry` / `sl` / `tp` | float | OPEN | Geometry audit (SL≈190 / TP≈280 pts) |
| `spread_pts` | int | OPEN `spread=` | Entry friction · Leak proxy |
| `atr_pts` | float | bar ATR at signal | vs max **98** |
| `bbw_pct` | float | bar BBw | gate **0.30–2.00%** |
| `dow` | {Mon…Fri} | open_time | Tue expected absent |
| `hour` | 0–23 | open_time | RTH ≈ 14–20 |
| `month` | YYYY-MM | open_time | |
| `hold_h` | float | close−open | label-time only / not for live L1 |
| `exit_reason` | TP\|SL\|EOT | close | |
| `win` | 0\|1 | TP=1 | |
| `y_lose` | 0\|1 | SL=1 | avoid-loser target |
| `pnl_R_design` | float | +1.47 / −1 | until deal R_real |
| `nights_held` | 0\|1 | hold≥12h | tip overnight-heavy |
| `near_atr_cap` | 0\|1 | atr ≥ 0.9×98 | HV stress |
| `regime_tag` | MATCH\|SOFT\|FRAGILE\|HOSTILE\| | month map | soft L1 (P1-T05) |
| `cell_dow_wed` | 0\|1 | dow==Wed | bad-cell seed |
| `cell_h1` | 0\|1 | month in Jan–Apr 2026 | bad-cell seed |
| `cell_month_jul` | 0\|1 | month==2026-07 | bad-cell seed |
| `cell_spread_high` | 0\|1 | spread ≥ tip p66 (builder) | bad-cell seed |
| `cell_month_may` | 0\|1 | month==2026-05 | **protect** |
| `cell_dow_mon` | 0\|1 | dow==Mon | **protect** |
| `cell_buy` / `cell_sell` | 0\|1 | side | |

### 2.2 Metadata (every row)

| Field | Value |
| --- | --- |
| `symbol` | Apple |
| `magic` | 26102011 |
| `preset_id` | BMRG-M5-AAPL-6M-Balanced_TPgtSL |
| `window` | e.g. 2026.05.01-2026.10.19 |
| `tf` | M5 |

### 2.3 Deferred (P1-T04+)

| Field | Why deferred |
| --- | --- |
| `band_ride_flag` | Needs MAE path / structure detector (P1-T04 optional) |
| `exit_spread_pts` / `c_R_event` | Needs deal export |
| `earnings_week` | Soft calendar TBD — use `regime_tag` / month until then |
| Hour cell flags | Seeded after tip tape QA → update `aos_bad_cells_M5.md` if needed |

---

## 3. Train / score policy

| Item | Rule |
| --- | --- |
| Primary train window | Tip May→Oct **plus** YTD Jan→Oct (label H1 stress) |
| Holdout | Last 20% of tip chronologically **or** Sep–Oct — state on each model |
| Target | `y_lose` (avoid-loser) |
| Forbidden features | Future info (`hold_h`, `exit_reason`) at **decision** time |
| Forbidden models | M15 `L2det_aapl` Thu/18 · EUR / AUD / DE40 / UK pins |

---

## 4. Tape files

| File | Content |
| --- | --- |
| `tapes/aapl_m5_tip_fire_tape_v0.csv` | Tip May→Oct n=77 |
| `tapes/aapl_m5_ytd_fire_tape_v0.csv` | YTD Jan→Oct n=145 |
| `tapes/aapl_m5_prior_fire_tape_v0.csv` | Jan→Apr 2026 |
| `tapes/aapl_m5_tip_core_fire_tape_v0.csv` | May→Aug |
| `tapes/aapl_m5_sep_oct_fire_tape_v0.csv` | Sep–Oct |
| `tapes/aapl_m5_long_fire_tape_v0.csv` | 2025.01→2026.10 n=289 |
| `tapes/aapl_m5_tip_prior_fire_tape_v0.csv` | Tip + prior combined |
| `blotter/archive/AAPL-M5-AOS-P1/` | Builder · COST_PROXY · TAPE_QA · REVIEW |

Builder: `blotter/archive/AAPL-M5-AOS-P1/build_aapl_m5_fire_tape.py`.  
Log source: Tester `logs/20261020.log` (Apple M5 · magic **26102011** · tip/YTD/long to **2026.10.19**).

---

## 5. QA gates (P1 exit)

| Check | Result (2026-10-20) |
| --- | --- |
| Tip n ≥ 30 | **PASS** n=**77** |
| Tue_n == 0 | **PASS** |
| atr_missing == 0 | **PASS** |
| tip OPEN == TP+SL | **PASS** 36+41=77 |
| Leak journal ≠ Stage-1 Robust | **PASS** — profile ~15.3 pp authority · measured OPEN |

`spread_high_thr` = **30** (tip p80 floor). See `blotter/archive/AAPL-M5-AOS-P1/REVIEW.md`.
