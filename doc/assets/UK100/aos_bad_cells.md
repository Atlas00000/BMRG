# UK100 — AIOS bad-cell registry

**Task:** UK100-AOS-P0-T02  
**Frozen seed:** 2026-10-12  
**Source:** `system_profile.md` · dedicated tip/prior runs in `20261012.log`  
**Consumer:** L2det / L2 AI feature labels · shadow CF precision checks  

Seed actions are **candidates**. Arm only after shadow CF under `aios_roadmap.md` iteration bar. Never silently mutate magic **26101201** mid-book — new preset/magic for HARD maps.

---

## Registry

| Cell ID | Definition | Tip / prior evidence | Seed action | Arm rule |
| --- | --- | --- | --- | --- |
| `DOW_THU` | Entry weekday = Thu | Tip n=13 WR **30.8%** E_N −0.31R | **SOFT skip** | **ARMED** shadow `L2det_uk_v1_Thu` (P2-T02 · prec 69% · ΔE_N +0.14R) |
| `HOUR_08` | Entry hour = 08 (London open) | Tip n=13 WR **30.8%** E_N −0.31R | **SOFT skip** candidate | **HOLD** — tip OK but Wed/SELL collateral; OR-union prior-hostile |
| `MONTH_JUL` | Entry month = Jul (stress) | Tip n=7 WR **28.6%** E_N −0.36R | **SOFT skip** | **ARMED** tip seed `L2det_uk_v1_Jul` · replace calendar later |
| `MONTH_FEB` | Entry month = Feb | Prior n=23 WR **34.8%** E_N −0.22R | **SOFT size-down** | Prior diagnostic; do not alone DROP tip |
| `SIDE_BUY_TIP` | BUY when tip-hostile | Tip BUY WR **38.5%** | **Buy-caution SOFT** | **ARMED** as `BUY∧near_atr` only · blanket BUY **DISARM** (prior) |
| `STREAK_CLUSTER` | Loss streak ≥ 3–4 open | Tip max L streak **6** | L3 halt / pause align | Engine already pauses at 3; L3 adds EF/E_N frontier |
| `NEAR_ATR_CAP` | ATR ≥ 0.9×1470 | Tip stress | Feature | Blanket DISARM · **BUY∧near_atr ARMED** |
| `W10_PATH_MIN` | Rolling W10 E_N deep negative | Tip min W10 E_N −0.33R · prior −0.78R | L4 Compressing → L3 | Observer, not entry invent |

---

## Strong cells (protect — do not over-skip)

| Cell ID | Evidence | OS note |
| --- | --- | --- |
| `DOW_WED` | Tip WR **81.8%** E_N +0.84R | Precision check: false-positive skips here = REJECT map |
| `SIDE_SELL_TIP` | Tip SELL WR **60%** | Protect unless path L3 halt |
| `HOUR_14` | Tip WR **66.7%** (n=12) | Protect |
| `MONTH_MAY_JUN` | Tip WR ~55% | Home MATCH strength |

---

## Explicit non-cells

| Anti-pattern | Why rejected |
| --- | --- |
| Skip all BUY forever | Prior BUY WR 54% — regime flip |
| Disable Tue (already off) | Parity only |
| Raise ATR max to “get n back” | Breaks G3 declaration / FRAGILE filter |
| Import AAPL hour-18 / AUD Mon-12 as defaults | Wrong book fingerprint |

---

## CF reporting (required when a cell is armed)

```text
cell_id
fires_total / fires_skipped
precision_vs_losers
false_skip_rate_on_DOW_WED_or_SELL_TIP
ΔE_N_tip_vs_baseline
ΔEF_tip_vs_baseline
fire_retention_pct
verdict: ARM | DISARM | HOLD_SOFT
```
