# AOS L1 Tape Contract v0

**Tasks:** AOS-P1-T02 (offline) · AOS-P1-T03 (live)  
**Schema:** `doc/aos_l1_feature_schema.md`  
**Format:** JSONL (one TapeTick per line) + optional CSV mirror for Excel

---

## 1. File layout

```
blotter/archive/AOS-P1-T02/
  harvest_long_tape.jsonl     # bar or fire-joined ticks
  harvest_long_fires.csv      # one row per ENGINE OPEN + tape join
  TAPE_MANIFEST.md
```

Live (T03 later):

```
Common/Files/BMRG/aos_l1_tape_EURUSD_M5.jsonl   # append-only
```

---

## 2. JSONL record (minimal required fields v0)

```json
{
  "tape_schema": "aos_l1_v0",
  "t_close": "2025.01.02 15:25",
  "symbol": "EURUSD",
  "tf": "M5",
  "hour_server": 15,
  "dow": 4,
  "dow_name": "Thu",
  "session_id": "LON_NY",
  "is_tue": false,
  "spread_pts": 4,
  "side": "BUY",
  "signal_hit": true,
  "structure_id": "UNK",
  "event_flags": [],
  "in_blackout": false,
  "cell_ids": ["SES_LON_NY"],
  "engine_magic": 8210204,
  "atr_pts": null,
  "bb_width_pct": null
}
```

Nullable numerics allowed in offline v0 when not parsed from log.

---

## 3. Session tagging algorithm (must match EDX)

```
hour = server hour of signal/bar
if hour >= 8  and hour < 12 → LON_AM
if hour >= 12 and hour < 17 → LON_NY
if hour >= 17 and hour < 20 → NY
if hour >= 20 or hour < 8  → POST_NY or ASIA
```

Champion fires should almost all be `LON_NY` or `NY`, and `is_tue=false`.

---

## 4. Offline builder (T02)

**Input:** Harvest CLEAN or full tester segment with `[BMRG][TRADE] OPEN` lines (magic 8210204).  
**Output:** `harvest_long_fires.csv` / `.jsonl` with ≥95% of opens tagged.  
**Accept checks:**

| Check | Bar |
| --- | --- |
| Coverage | tagged_opens / opens ≥ 0.95 |
| Tue parity | count(`is_tue`)==0 on champ long |
| Session | share in {LON_NY, NY} ≥ 0.95 |

---

## 5. Live publisher (T03 — later)

EA or sidecar appends TapeTick each new bar; on OPEN, duplicate tick with `signal_hit=true` + `side`.  
Must not change engine n/WR vs baseline beyond noise (perception-only).
