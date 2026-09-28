# AOS L1 Feature Schema v0

**Task:** AOS-P1-T01  
**Layer:** L1 Perception  
**Status:** LOCKED for L2 consumption  
**Cadence:** one row per **closed M5 bar** (shift 1), symbol EURUSD  
**Companions:** `doc/aos_l1_tape_contract.md` · `doc/aos_bad_cells.md` · `doc/ai_OS_baseline.md`

L1 **does not** decide skip/fire. It only emits a typed tape. L2+ consume it.

---

## 1. TapeTick identity

| Field | Type | Notes |
| --- | --- | --- |
| `tape_schema` | string | `"aos_l1_v0"` |
| `t_close` | datetime UTC/server | Bar close time (M5) |
| `symbol` | string | `EURUSD` |
| `tf` | string | `M5` |
| `bar_index` | int64 | Optional monotonic id |
| `engine_magic` | int64 | Champion **8210204** when tagging Harvest fires |

---

## 2. Feature families

### 2.1 Session / calendar (always available offline)

| Feature | Type | Encoding | L2 / bad-cell link |
| --- | --- | --- | --- |
| `hour_server` | int8 | 0–23 | session buckets |
| `dow` | int8 | 0=Sun … 6=Sat (MT5) or ISO documented in tape header | `DOW_TUE` |
| `session_id` | enum string | see §3 | `SES_*` |
| `is_tue` | bool | `dow == Tuesday` | hard skip parity |
| `week_of_month` | int8 | 1–5 | soft calendar |
| `month` | int8 | 1–12 | late-cycle soft |

### 2.2 Vol / BB (from engine indicators)

| Feature | Type | Source | Notes |
| --- | --- | --- | --- |
| `atr_pts` | float64 | iATR | points |
| `atr_tercile` | int8 | 1–3 rolling | L1 vol; deferred fill OK in v0 offline |
| `bb_upper` `bb_mid` `bb_lower` | float64 | iBands | |
| `bb_width_pct` | float64 | (U−L)/mid×100 | already in EA logs |
| `bb_width_tercile` | int8 | 1–3 | deferred if no history window |
| `bb_dev_design` | float64 | InpBBDev (2.2) | constant per preset |
| `close` | float64 | bar close | |
| `dist_below_lower_σ` | float64 | (lower−close)/σ | buy fade distance |
| `dist_above_upper_σ` | float64 | (close−upper)/σ | sell fade distance |

### 2.3 Trend / range / structure

| Feature | Type | Encoding | Notes |
| --- | --- | --- | --- |
| `structure_id` | enum string | §4 | HH/HL, LH/LL, range, breakout, failed_auction, band_ride, unknown |
| `er_tercile` | int8 | 1–3 | Efficiency ratio; **deferred** until P1 tooling |
| `trend_side` | enum | `up` `down` `flat` `unk` | from swing structure |

### 2.4 Microstructure

| Feature | Type | Notes |
| --- | --- | --- |
| `spread_pts` | int | at bar / at signal |
| `spread_tercile` | int8 | 1–3 rolling |
| `gap_flag` | bool | open gap vs prior close |
| `swap_night_risk` | bool | inventory may hold past rollover |

### 2.5 Event windows

| Feature | Type | Notes |
| --- | --- | --- |
| `event_flags` | string[] | §5; empty OK in v0 |
| `in_blackout` | bool | any high-impact flag active |

### 2.6 Engine-local (at signal / fire rows)

| Feature | Type | Notes |
| --- | --- | --- |
| `side` | enum | `BUY` `SELL` `NONE` |
| `signal_hit` | bool | engine fade true this bar |
| `bars_since_entry` | int | cooldown context |
| `open_inventory` | bool | position open for magic |
| `cell_ids` | string[] | mapped bad/edge cells e.g. `DOW_TUE`,`SES_LON_NY` |

---

## 3. `session_id` vocabulary

| ID | Server hours (inclusive start, exclusive end unless noted) | EDX link |
| --- | --- | --- |
| `ASIA` | 00–08 | filtered by champ time gate |
| `LON_AM` | 08–12 | soft caution `SES_LON_AM` |
| `LON_NY` | 12–17 | edge `SES_LON_NY` |
| `NY` | 17–20 | edge `SES_NY` |
| `POST_NY` | 20–24 | outside champ window |
| `UNK` | — | parse failure |

Champion engine only **fires** in `LON_NY` ∪ `NY` (12–20) and not Tue.

---

## 4. `structure_id` vocabulary (AOS-P1-T04)

| ID | Meaning (v0 rules — refine later) |
| --- | --- |
| `SWING_HH_HL` | Higher high + higher low (up structure) |
| `SWING_LH_LL` | Lower high + lower low (down) |
| `RANGE_BOX` | Swings contained in recent box |
| `BREAKOUT` | Close beyond box with extension |
| `FAILED_AUCTION` | Breakout then close back inside |
| `BAND_RIDE` | Close outside band continuing away from mid (anti-mean-rev) |
| `MEAN_PRESS` | Close beyond band toward mid (fade-friendly) |
| `UNK` | Insufficient bars / not computed |

v0 offline may emit `UNK` for structure until swing engine lands; session/DoW still required.

---

## 5. `event_flags` vocabulary (AOS-P1-T05)

| Flag | Meaning |
| --- | --- |
| `NFP` | Non-farm payroll window |
| `FOMC` | FOMC / Fed |
| `CPI` | CPI release |
| `HIGH_IMPACT` | Generic calendar blackout |
| `HOLIDAY_LIQ` | Holiday liquidity |
| `ROLL` | Futures/FX roll caution |

v0: flags optional; `in_blackout=false` default. CSV calendar may fill later — no hard skip until L2 task owns it.

---

## 6. Refresh / join rules

1. Emit on **new closed bar** only (no tick spam).  
2. **Fire rows:** when engine logs `[BMRG][TRADE] OPEN`, attach the prior closed-bar TapeTick (shift 1).  
3. Join key: `(symbol, t_signal_bar_close)` or nearest prior tape `t_close`.  
4. Missing tape on a fire → L6 reason `TAPE_MISS` (T02 accept requires &lt;5% miss).

---

## 7. Accept (T01)

| Check | Status |
| --- | --- |
| Covers vol / trend / session / event / micro / engine-local | **PASS** |
| Enums align with `aos_bad_cells.md` | **PASS** |
| No skip decisions in L1 | **PASS** |
