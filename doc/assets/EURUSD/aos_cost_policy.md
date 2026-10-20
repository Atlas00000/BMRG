# EURUSD M15 — AIOS cost / Leak policy

**Task:** EURUSD-AOS-P0-T03  
**Status:** Design prior stub **CLOSED** 2026-10-18 · journal 2×spread proxy **CLOSED** 2026-10-18 · full deal-measured Leak **OPEN** (swap still required)  
**Binding:** [`edge_framework.md`](./edge_framework.md) §4  
**Baseline:** [`EURUSD_AOS_BASELINE_v1.md`](./EURUSD_AOS_BASELINE_v1.md)  

OS scorecards must state `Leak_source`. Do not promote L2 LIVE_WITHHOLD or P7 on prior alone if zone flips Negative after deals. Overnight swap is **mandatory** on this sleeve (holds often ≥12h).

---

## 1. 1R (currency)

```
1R = InpSL_Points × volume × tick_value
```

| Field | Research default |
| --- | --- |
| SL points | **300** |
| Volume | **0.01** |
| Point | ≈0.00001 |
| Proxy 1R $ | ~**$3.00** (confirm on deal export) |

---

## 2. Cost ladder (authority order)

| Rank | `Leak_source` | When to use |
| ---: | --- | --- |
| 1 | `measured` | Deal blotter with entry+exit friction + **swap × nights** |
| 2 | `journal_2x_entry_spread_median` | **Current interim OS** (tip OPEN spreads) |
| 3 | `prior` | Design card **3.0 pp** — footnotes only (optimistic friction floor was high) |

### 2.1 Journal proxy (tip May→Oct 2026 · P1 tape)

Evidence: `blotter/archive/EURUSD-AOS-P1/COST_PROXY.json`

| Component | Value |
| --- | ---: |
| Entry spread median | **4 pts** (n=45 · mean 4.3 · max 6) |
| Round-turn floor | `2 × 4 / 300` → `c_R = 0.0267R` |
| Leak_proxy | **1.19 pp** |
| BM (WR 46.7%) | +2.22 pp |
| EF_proxy | **+1.04 pp** |
| Zone | **Fragile** (EF ≪ M) |
| nights_held share | **75.6%** — swap still unpaid in this proxy |

Design prior (20 pt RT → Leak 3.0 pp → EF −0.7 pp) was **pessimistic vs journal spreads**. Prefer journal proxy for OS Δ until deals+swap land.

`InpAOS_Leak=3.0` in the preset is **metadata only** — never counted as measured L1.

### 2.2 Still missing for `measured`

Commission · exit spread · **swap × nights_held** · slippage fill delta.

Overnight is primary inventory risk on this sleeve — measured Leak without swap is incomplete.

---

## 3. Formulae

```
Leak = c_R / (R + 1)     # R ≈ 1.25 → denom 2.25
EF   = BM − Leak
```

---

## 4. Deal-export checklist (closes measured)

1. Strategy Tester → Report → Deals export for tip May→Oct (magic **26101817**).  
2. Drop into `blotter/inbox/` → archive `blotter/archive/EURUSD-AOS-P0-T03-deals/` (or successor).  
3. Compute per-event: spread_pts, pnl_ccy, pnl_R, nights_held, exit_reason, swap_ccy.  
4. Re-score tip under `edge_framework.md` with `Leak_source=measured`.  
5. Update `EURUSD_AOS_BASELINE_v1` → v2 if Leak materially changes zone.  
6. Only then arm L2 LIVE_WITHHOLD / schedule P7.

---

## 5. OS trial reporting

Every CF / weekly exit must include:

```text
Leak_source: prior | journal_2x_entry_spread_median | measured
Leak_pp / EF_pp / zone
nights_held_mean (tip)
costs_defaulted: <list or none>
```
