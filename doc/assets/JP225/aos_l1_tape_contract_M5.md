# JP225 / JPN225 M5 — L1 tape / feature schema v0

**Task:** JP225-M5-AOS-P1-T01  
**Status:** Schema frozen 2026-10-20  
**Engine:** Growth P0 · magic **26101906** · AOS OFF · MT5 **JPN225** · **M5**  
**First tapes:** tip n=**94** · YTD n=**130** · prior 36 · MATCH 34 · OFFHOME 60  
**Parents:** [`aios_roadmap_M5.md`](./aios_roadmap_M5.md) · [`aos_bad_cells_M5.md`](./aos_bad_cells_M5.md) · [`edge_framework.md`](./edge_framework.md)  
**Sibling:** [`aos_l1_tape_contract.md`](./aos_l1_tape_contract.md) (M15) — do not mix pins / ATR / RR

L1 **perceives** fires for L2det / L2skip. It does not invent entries or change SL/TP/ATR band.

---

## 1. Event grain

| Rule | Binding |
| --- | --- |
| Unit | One G0 fire = one row |
| Open | `[BMRG][TRADE] OPEN` (Tester journal) |
| Close | TP / SL (EOT excluded from train labels; keep in freq) |
| Label `y_lose` | `1` if SL (lose), `0` if TP (win) — avoid-loser target |
| Identity | `26101906-JPN225-M5-{side}-{YYYYMMDDhhmmss}` |

---

## 2. Feature schema v0

### 2.1 Required (train + shadow)

| Field | Type | Source | Notes |
| --- | --- | --- | --- |
| `open_time` | datetime | journal | Server time |
| `side` | {BUY,SELL} | OPEN | |
| `entry` / `sl` / `tp` | float | OPEN | Geometry audit (SL≈25000 / TP≈50000 pts) |
| `spread_pts` | int | OPEN `spread=` | Entry friction |
| `atr_pts` | float | bar ATR at signal | vs band **7610–11285** |
| `bbw_pct` | float | bar BBw | diagnostic (gate OFF) |
| `dow` | {Mon…Fri} | open_time | Tue expected absent |
| `hour` | 0–23 | open_time | London sleeve 8–16 entries |
| `month` | YYYY-MM | open_time | |
| `session_age_min` | int | minutes since 08:00 | soft L9 |
| `hold_h` | float | close−open | label-time only / not for live L1 |
| `exit_reason` | TP\|SL\|HALT\|EOT | close | HALT = daily-loss flatten (y_lose=1) |
| `win` | 0\|1 | TP=1 | |
| `y_lose` | 0\|1 | 1−win | avoid-loser target |
| `pnl_R_design` | float | +2.00 / −1 | until deal R_real |
| `nights_held` | 0\|1 | hold≥12h | expect uncommon on cash sleeve |
| `near_atr_cap` | 0\|1 | atr ≥ 0.9×**11285** | near band max |
| `below_atr_floor` | 0\|1 | atr ≤ 1.1×**7610** | near band min |
| `ouroboros_tag` | MATCH\|MISMATCH\|FRAGILE\| | month map | soft L1 (P1-T05) |
| `cell_month_aug` | 0\|1 | month==*-08 | **PRIMARY** MATCH tax |
| `cell_month_sep` | 0\|1 | month==*-09 | **PRIMARY** MATCH tax |
| `cell_month_feb` | 0\|1 | month==2026-02 | soft pre-tip |
| `cell_month_apr` | 0\|1 | month==2026-04 | soft pre-tip |
| `cell_month_jul` | 0\|1 | month==*-07 | **protect** star |
| `cell_match` | 0\|1 | ouroboros_tag==MATCH | bad-cell |
| `cell_mismatch` | 0\|1 | ouroboros_tag==MISMATCH | protect when Jul/Oct |
| `cell_fragile` | 0\|1 | ouroboros_tag==FRAGILE | soft — **not** blanket (Jun pays) |
| `cell_near_atr` | 0\|1 | near_atr_cap | conjunction only |
| `cell_buy` / `cell_sell` | 0\|1 | side | |

### 2.2 Metadata (every row)

| Field | Value |
| --- | --- |
| `symbol` | JPN225 |
| `magic` | 26101906 |
| `preset_id` | BMRG-M5-JP225-6M-P0_growth_chart |
| `window` | e.g. 2026.05.01-2026.10.19 |
| `tf` | M5 |

### 2.3 Deferred (P1-T04+)

| Field | Why deferred |
| --- | --- |
| `band_ride_flag` / MAE path | Needs tick path (P1-T04 optional) |
| `exit_spread_pts` / `c_R_event` | Deal export |
| DOW/hour cell flags | Seed after tip tape QA → update `aos_bad_cells_M5.md` |

**Offline-only (not live L1):** `hold_h`, `exit_reason`, `nights_held`.

---

## 3. Train / score policy

| Item | Rule |
| --- | --- |
| Primary train window | Tip May→Oct **plus** YTD Jan→Oct (label MATCH tax + Feb/Apr) |
| Holdout | Last 20% of tip chronologically **or** Aug–Sep — state on each model |
| Target | `y_lose` (avoid-loser) |
| Forbidden at decision | Future info (`hold_h`, `exit_reason`, …) |
| Forbidden models | M15 `L2det_jp` / May∨Jul / EUR / UK / DE / AUD / AAPL pins |
| Protect cells | False-skip on **Jul / Jun / Oct / OFFHOME** must be reported |

---

## 4. Tape files

| File | Content |
| --- | --- |
| `tapes/jp225_m5_tip_fire_tape_v0.csv` | Tip May→Oct |
| `tapes/jp225_m5_ytd_fire_tape_v0.csv` | YTD Jan→Oct |
| `tapes/jp225_m5_prior_fire_tape_v0.csv` | Jan→Apr |
| `tapes/jp225_m5_match_fire_tape_v0.csv` | Aug–Sep MATCH tax |
| `tapes/jp225_m5_offhome_fire_tape_v0.csv` | May–Jul+Oct OFFHOME |
| `blotter/archive/JP225-M5-AOS-P1/` | Builder · COST_PROXY · TAPE_QA |

Builder: `blotter/archive/JP225-M5-AOS-P1/build_jp225_m5_fire_tape.py`.  
Log source: Tester `logs/20261020.log` (JPN225 M5 · magic **26101906**).

---

## 5. QA gates (P1 exit)

| Check | Result (2026-10-20) |
| --- | --- |
| Tip n ≥ 30 | **PASS** n=94 |
| YTD n | **PASS** n=130 |
| Tue_n == 0 | **PASS** |
| atr_missing == 0 | **PASS** |
| ouroboros_nonempty tip | **PASS** 94/94 |
| Leak journal ≠ Stage-1 | **PASS** — prior **3.3 pp** authority (journal Leak_proxy ≈3.7 pp optimistic vs live) |

### Tip cell highlights (from TAPE_QA)

| Slice | n | WR | E_N | Role |
| --- | ---: | ---: | ---: | --- |
| SELL | 48 | 47.9% | **+0.44R** | Protect |
| BUY | 46 | 34.8% | +0.04R | Caution conjunction |
| Thu | 22 | 54.5% | **+0.64R** | Protect |
| Wed | 22 | 31.8% | −0.05R | Soft seed |
| H08 / H10 | 19 / 9 | 52.6% / 88.9% | +0.58 / +1.67 | Protect |
| H09 / H13 / H16 | 6 / 20 / 6 | soft | ≤0 | Soft seeds |
| MATCH Aug–Sep | 34 | 26.5% | −0.21R | Primary soft |
| OFFHOME | 60 | 50% | +0.50R | Protect |
