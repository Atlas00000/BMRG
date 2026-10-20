# EURUSD M15 — AIOS bad-cell registry

**Task:** EURUSD-AOS-P0-T02  
**Frozen seed:** 2026-10-18  
**Source:** `system_profile.md` · tip/YTD runs in `20261018.log` · `blotter/archive/EURUSD-M15-P2/TRADE_PROFILE.json`  
**Consumer:** L2det / L2 AI feature labels · shadow CF precision checks  

Seed actions are **candidates**. Arm only after shadow CF under `aios_roadmap.md` iteration bar. Never silently mutate magic **26101817** mid-book — new preset/magic for HARD maps.

---

## Registry

| Cell ID | Definition | Tip / YTD evidence | Seed action | Arm rule |
| --- | --- | --- | --- | --- |
| `SIDE_BUY` | BUY when sell cells dominate | Tip BUY n=23 WR **39.1%** E_N −0.12R · YTD WR **35.3%** | **Buy-caution SOFT** | Blanket BUY **DISARM** (stall) · **ARMED** as `BUY∧near_atr` / `BUY∧H13` (P2) |
| `DOW_THU` | Entry weekday = Thu | Tip n=8 WR **37.5%** E_N −0.16R | **SOFT skip** | **ARMED** `L2det_eur_m15_v1_Thu` (P2-T02) |
| `HOUR_13` | Entry hour = 13 | Tip n=8 WR **37.5%** E_N −0.16R | **SOFT skip** | Alone **HOLD** · **ARMED** as `BUY∧H13` only |
| `HOUR_19` | Entry hour = 19 (late session) | Tip n=3 WR **33.3%** E_N −0.25R | **SOFT skip** | **ARM_SOFT** thin optional |
| `MONTH_FEB` | Entry month = Feb | YTD n=10 WR **30.0%** E_N −0.33R | **SOFT size-down / skip** | YTD HOLD diagnostic — not tip arm |
| `MONTH_AUG` | Entry month = Aug | Tip n=7 WR **42.9%** E_N −0.04R | **SOFT size-down** | **HOLD_SOFT** (collateral) — not tip arm |
| `NEAR_ATR_CAP` | ATR ≥ 0.9×74 (~66.6) | Tip n=17 WR **47.1%** E_N +0.06R (not hostile alone) | Feature | Blanket **DISARM** · **ARMED** only AND BUY in v1b |
| `STREAK_CLUSTER` | Loss streak ≥ 3–4 open | Tip max L streak **4** · YTD **5** | L3 halt / pause align | Engine already pauses at 3; L3 adds EF/E_N frontier |
| `W10_PATH_MIN` | Rolling W10 E_N deep negative | Tip min W10 −0.33R · YTD −0.55R (Feb path) | L4 Compressing → L3 | Observer, not entry invent |
| `OCT_FRAGILE` | Oct FRAGILE tip | Tip n=2 · Ouroboros FRAGILE≈95% | Footnote / ATR already filters | Do not use as admission; do not lift ATR max |

---

## Strong cells (protect — do not over-skip)

| Cell ID | Evidence | OS note |
| --- | --- | --- |
| `SIDE_SELL` | Tip SELL WR **54.5%** · YTD **60.5%** | Precision check: false-positive skips here = REJECT map |
| `DOW_MON` | Tip WR **50%** · YTD **52%** | Protect |
| `DOW_FRI` | Tip WR **50%** · YTD **56%** | Protect |
| `HOUR_12` | Tip WR **50%** (n=18) | Protect session open of sleeve |
| `HOUR_14` | Tip WR **50%** (n=6) | Protect |
| `MONTH_JUL` | Tip WR **57.1%** E_N +0.29R | Protect tip carry |
| `MONTH_JAN_APR` | YTD strong | Protect on YTD-compare tasks |

---

## Explicit non-cells

| Anti-pattern | Why rejected |
| --- | --- |
| Skip all BUY forever | Regime / path may flip; YTD still has some BUY wins — use conditional caution |
| Re-enable BB-width / ATR≤68 (P1) | Starvation known (n≈6) |
| Disable Tue (already off) | Parity only |
| Raise ATR max to “get n back” | Breaks G3 declaration / FRAGILE filter |
| Import UK100 H08 / AAPL hour-18 / AUD Mon-12 as defaults | Wrong book fingerprint |
| Pin M5 aistack L2 | Wrong TF / magic book |
| Convert to Harvest RR=1.0 as OS | Geometry reopen — new sleeve card only |

---

## CF reporting (required when a cell is armed)

```text
cell_id
fires_total / fires_skipped
precision_vs_losers
false_skip_rate_on_SIDE_SELL_or_DOW_MON_FRI_or_HOUR_12
ΔE_N_tip_vs_baseline
ΔEF_tip_vs_baseline
fire_retention_pct
verdict: ARM | DISARM | HOLD_SOFT
```
