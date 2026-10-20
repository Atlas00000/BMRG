# JP225 — L1 tape / feature schema v0

**Task:** JP225-AOS-P1-T01  
**Status:** Schema frozen 2026-10-19  
**Engine:** Growth P1 wrLift fade · magic **26101904** · AOS OFF · MT5 **JPN225**  
**First tapes:** `tapes/jp225_tip_fire_tape_v0.csv` (May→Aug · n=79) · `tapes/jp225_janaug_fire_tape_v0.csv` (Jan→Aug · n=143) · `tapes/jp225_long_fire_tape_v0.csv` (2025.01→2026.10 · n=360)  
**Parents:** [`aios_roadmap.md`](./aios_roadmap.md) · [`aos_bad_cells.md`](./aos_bad_cells.md) · [`edge_framework.md`](./edge_framework.md)

L1 **perceives** fires for L2det / L2skip. It does not invent entries or change SL/TP/Fade.

---

## 1. Event grain

| Rule | Binding |
| --- | --- |
| Unit | One G0 fire = one row (ticket = event) |
| Open | `[BMRG][TRADE] OPEN` (Tester journal) |
| Close | TP / SL (EOT excluded from train labels; keep in freq) |
| Label `y_lose` | `1` if SL (lose), `0` if TP (win) — avoid-loser target |
| Identity | `26101904-JPN225-{side}-{YYYYMMDDhhmmss}` |

---

## 2. Feature schema v0

### 2.1 Required (train + shadow)

| Field | Type | Source | Notes |
| --- | --- | --- | --- |
| `open_time` | datetime | journal | Server time |
| `side` | {BUY,SELL} | OPEN | |
| `entry` / `sl` / `tp` | float | OPEN | Geometry audit (SL≈23260 / TP≈34890 pts) |
| `spread_pts` | int | OPEN `spread=` | Entry friction |
| `atr_pts` | float | bar ATR at signal | vs max **19670** |
| `bbw_pct` | float | bar BBw | diagnostic (gate OFF) |
| `dow` | {Mon…Fri} | open_time | Tue expected absent |
| `hour` | 0–23 | open_time | London sleeve 8–16 entries |
| `month` | YYYY-MM | open_time | |
| `session_age_min` | int | minutes since 08:00 | soft L9 |
| `hold_h` | float | close−open | label-time only / not for live L1 |
| `exit_reason` | TP\|SL\|HALT\|EOT | close | HALT = daily-loss flatten (y_lose=1) |
| `win` | 0\|1 | TP=1 | |
| `y_lose` | 0\|1 | 1−win | avoid-loser target |
| `pnl_R_design` | float | +1.50 / −1 | until deal R_real |
| `nights_held` | 0\|1 | hold≥12h | expect uncommon on cash sleeve |
| `near_atr_cap` | 0\|1 | atr ≥ 0.9×19670 | stress / FRAGILE residual |
| `ouroboros_tag` | MATCH\|MISMATCH\|FRAGILE\| | month map | soft L1 (P1-T05) |
| `cell_month_may` | 0\|1 | month==*-05 | bad-cell |
| `cell_month_jul` | 0\|1 | month==*-07 | bad-cell |
| `cell_month_oct` | 0\|1 | month==*-10 | bad-cell (thin) |
| `cell_mismatch` | 0\|1 | ouroboros_tag==MISMATCH | bad-cell |
| `cell_fragile` | 0\|1 | ouroboros_tag==FRAGILE | soft — **not** blanket (Jun pays) |
| `cell_may_fragile` | 0\|1 | May ∧ FRAGILE | primary conjunction |
| `cell_near_atr` | 0\|1 | near_atr_cap | bad-cell conjunction seed |

### 2.2 Metadata (every row)

| Field | Value |
| --- | --- |
| `symbol` | JPN225 |
| `magic` | 26101904 |
| `preset_id` | BMRG-M15-JP225-6M-P1_wrLift_fade_chart |
| `window` | e.g. 2026.05.01-2026.08.31 |
| `tf` | M15 |

### 2.3 Deferred (P1-T04+)

| Field | Why deferred |
| --- | --- |
| `band_ride_flag` / MAE path | Needs tick path (P1-T04 optional) |
| `exit_spread_pts` / `c_R_event` | Deal export · see `LEAK_MEASURED.json` / tip_deal_costs |
| DOW/hour cell flags | Seed after tip tape QA → update `aos_bad_cells.md` |

**Offline-only (not live L1):** `hold_h`, `exit_reason`, `nights_held`, any structure proxy from hold time.

---

## 3. Train / score policy

| Item | Rule |
| --- | --- |
| Primary train window | Tip May→Aug **plus** Jan→Aug (label stress months) |
| Support | Long 2025→tip for L3 path / rare Oct |
| Holdout | Last 20% of tip chronologically **or** Aug — state on each model |
| Target | `y_lose` (avoid-loser) |
| Forbidden at decision | Future info (`hold_h`, `exit_reason`, …) |
| Forbidden models | EUR / UK / DE40 / AUD / USDJPY / AAPL L2 pins |
| Protect cells | False-skip on Aug/Sep MATCH and paying Jun must be reported |

---

## 4. Tape files

| File | Content |
| --- | --- |
| `tapes/jp225_tip_fire_tape_v0.csv` | Tip n=79 labeled fires |
| `tapes/jp225_janaug_fire_tape_v0.csv` | Jan→Aug n=143 |
| `tapes/jp225_long_fire_tape_v0.csv` | Long n=360 |
| `tapes/jp225_tip_janaug_fire_tape_v0.csv` | Combined tip+janaug (dedupe) |
| `blotter/archive/JP225-AOS-P1/` | Builder + COST_PROXY + TAPE_QA + copies |

Builder: `blotter/archive/JP225-AOS-P1/build_jp225_m15_fire_tape.py`.  
Log source: Tester `logs/20261019.log` (JPN225 chunks · magic 26101904).

---

## 5. Acceptance (schema)

- [x] Fields cover bad-cell registry seeds (May / Jul / Oct / MISMATCH / FRAGILE / near_atr)  
- [x] Tip tape n=79 with win/side/dow/hour/ATR/spread  
- [x] Jan–Aug tape n=143 · long n=360  
- [x] Ouroboros month tags (P1-T05)  
- [ ] Deal columns when export available  
- [ ] P1-T04 structure flags (optional · OPEN)

Bump to schema v1 when deal `c_R` or structure flags land.
