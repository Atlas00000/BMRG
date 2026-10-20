# UK100 M5 — AIOS bad-cell registry

**Task:** UK100-M5-AOS-P0-T02  
**Frozen seed:** 2026-10-20  
**Source:** `system_profile_M5.md` · Tester `logs/20261020.log` tip May→Aug · long Jan→Aug  
**Consumer:** L2det / L2 AI feature labels · shadow CF precision checks  
**Sibling:** M15 [`aos_bad_cells.md`](./aos_bad_cells.md) — **do not copy armed maps**

Seed actions are **candidates**. Arm only after shadow CF under `aios_roadmap_M5.md` iteration bar. Never silently mutate magic **26101905** mid-book — new preset/magic for HARD maps (`2612xxxx`).

---

## Registry

| Cell ID | Definition | Tip / prior evidence | Seed action | Arm rule |
| --- | --- | --- | --- | --- |
| `DOW_MON` | Entry weekday = Mon | Tip n=32 WR **43.8%** (below BWR) | **SOFT skip** | **HOLD** alone (H08–11 FP) · **ARMED** as Mon∧H12 in v1b |
| `HOUR_12_13` | Entry hour ∈ {12,13} | Tip n=47 WR **40.4%** E_N soft | **SOFT skip** | Full H12 **HOLD** · **ARMED** via SELL∧H12 / Mon∧H12 in v1b |
| `MONTH_AUG` | Entry month = Aug | Tip n=38 WR **42.1%** E_N **−0.053R** | **SOFT skip** or size-down | **HOLD** calendar (P2) |
| `MONTH_FEB` | Entry month = Feb | Prior n=40 WR **40.0%** E_N −0.100R | **SOFT size-down** | Prior diagnostic; not tip arm |
| `MONTH_APR` | Entry month = Apr | Prior n=24 WR **37.5%** E_N −0.156R | **SOFT size-down** | Prior diagnostic |
| `MONTH_MAR` | Entry month = Mar | Prior n=6 WR 33.3% | Observe only | Starved — ATR/session already binding |
| `NEAR_ATR_CAP` | ATR ≥ 0.9×869 | Design stress | Feature / optional SOFT | Blanket **DISARM** · SELL∧near_atr **HOLD** |
| `SIDE_SELL_TIP` | SELL when tip-hostile | Tip SELL WR 50.0% (OK) | **SOFT caution** | **ARMED** as SELL∧H12 in v1b |
| `STREAK_CLUSTER` | Loss streak ≥ 3–4 open | Tip max L streak **5** | L3 halt / pause align | Engine pause@3; L3 adds frontier |
| `W15_PATH_LATE` | Late tip W15/W20 E_N &lt; 0 | Tip late prints ~−0.21 to −0.25 | L4 Compressing → L3 | Observer, not entry invent |

---

## Strong cells (protect — do not over-skip)

| Cell ID | Evidence | OS note |
| --- | --- | --- |
| `DOW_WED` | Tip WR **65.4%** | Precision check: false-positive skips here = REJECT map |
| `HOUR_08_11` | Tip WR **~66.7%** | **Protect** — opposite of M15 H08 soft |
| `SIDE_BUY_TIP` | Tip BUY WR **54.8%** | Protect unless path L3 halt |
| `MONTH_MAY_JUN` | Tip WR 64% / 56% | Home MATCH strength |
| `MONTH_JUL` | Tip WR **53.8%** overall | Do **not** import M15 Jul skip without CF (Jul SELL-only soft) |

---

## Explicit non-cells (rejected imports)

| Anti-pattern | Why rejected |
| --- | --- |
| Arm M15 `DOW_THU` on M5 | Tip Thu WR **50.0%** — neutral, not soft |
| Arm M15 `HOUR_08` on M5 | Tip H08–09 WR **66.7%** — protect |
| Skip all SELL forever | Tip SELL ≥ BWR; regime can flip |
| Disable Tue (already off) | Parity only |
| Raise ATR max 869 to “get n back” | Breaks G3 / FRAGILE filter (unfiltered EF &lt; 0) |
| Import AAPL hour-18 / AUD Mon-12 as defaults | Wrong book; Mon soft here is UK100-M5 native — still CF before HARD |
| Attach `L2det_uk` / `L2skip_uk` (M15) to magic **26101905** | Wrong TF fingerprint |

---

## CF reporting (required when a cell is armed)

```text
cell_id
tf: M5
fires_total / fires_skipped
precision_vs_losers
false_skip_rate_on_DOW_WED
false_skip_rate_on_HOUR_08_11
false_skip_rate_on_SIDE_BUY_TIP
ΔE_N_tip_vs_baseline
ΔEF_tip_vs_baseline
fire_retention_pct
verdict: ARM | DISARM | HOLD_SOFT
m15_map_reused: false
```
