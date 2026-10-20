# UK100 — AIOS cost / Leak policy

**Task:** UK100-AOS-P0-T03  
**Status:** Journal proxy **CLOSED** 2026-10-12 · full deal-measured Leak **OPEN**  
**Binding:** [`edge_framework.md`](./edge_framework.md) §4  
**Baseline:** [`UK100_AOS_BASELINE_v1.md`](./UK100_AOS_BASELINE_v1.md)  
**Evidence:** `blotter/archive/UK100-AOS-P0-T03/COST_PROXY.json`

OS scorecards must state `Leak_source`. Do not promote L2 LIVE_WITHHOLD or P7 on prior/proxy alone if zone flips Negative after deals.

---

## 1. 1R (currency)

```
1R = InpSL_Points × volume × tick_value
```

| Field | Research default |
| --- | --- |
| SL points | **2500** |
| Volume | **0.1** |
| Point | 0.01 |
| Proxy 1R $ | ~**$2.50** (confirm on deal export) |

---

## 2. Cost ladder (authority order)

| Rank | `Leak_source` | When to use |
| ---: | --- | --- |
| 1 | `measured` | Deal blotter with entry+exit friction |
| 2 | `journal_2x_entry_spread_median` | **Current interim** (tip OPEN spreads) |
| 3 | `prior` | Design card 2.9 pp — footnotes only |

### 2.1 Journal proxy (tip May→Aug 2026)

| Component | Value |
| --- | ---: |
| Entry spread median | **120 pts** (n=51 · constant on this run) |
| Round-turn floor | `2 × 120 / 2500` → `c_R = 0.096R` |
| Leak_proxy | **4.27 pp** |
| BM (WR 49%) | +4.58 pp |
| EF_proxy | **+0.31 pp** |
| Zone | **Fragile** |

Design prior (160 RT pts → Leak 2.9 pp → EF +1.7 pp) was **optimistic** vs journal 2×spread.

### 2.2 Still missing for `measured`

Commission · exit spread · swap × nights · slippage fill delta.

---

## 3. Formulae

```
Leak = c_R / (R + 1)     # R ≈ 1.25 → denom 2.25
EF   = BM − Leak
```

`InpAOS_Leak=2.9` in the preset is **metadata only** — never counted as measured L1.

---

## 4. Deal-export checklist (closes measured)

1. Strategy Tester → Report → Deals export for tip May→Aug (magic 26101201).  
2. Drop into `blotter/inbox/` → archive `blotter/archive/UK100-AOS-P0-T03-deals/` (or successor).  
3. Compute per-event: spread_pts, pnl_ccy, pnl_R, nights_held, exit_reason.  
4. Publish `Leak_source=measured` mean/median on tip.  
5. Re-score EF; bump baseline to v2 if zone changes.

---

## 5. OS rules while measured is open

| Allowed | Forbidden |
| --- | --- |
| Shadow L2det CF using E_N + EF_proxy footnote | Claim Robust EF or PRODUCTION-WORTHY |
| Compare ΔE_N vs `UK100_AOS_BASELINE_v1` | Train LIVE_WITHHOLD as if costs fully known |
| Prefer journal proxy over design prior in CF footnotes | Use EUR/AUD Leak defaults as UK100 truth |
