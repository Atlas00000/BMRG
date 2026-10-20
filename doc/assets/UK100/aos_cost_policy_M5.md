# UK100 M5 — AIOS cost / Leak policy

**Task:** UK100-M5-AOS-P0-T03  
**Status:** Design prior **CLOSED** · journal proxy **CLOSED** 2026-10-20 (P1) · deal-measured Leak **OPEN**  
**Binding:** [`edge_framework.md`](./edge_framework.md) §4  
**Baseline:** [`UK100_M5_AOS_BASELINE_v1.md`](./UK100_M5_AOS_BASELINE_v1.md)  
**Roadmap:** [`aios_roadmap_M5.md`](./aios_roadmap_M5.md)  
**Evidence:** `blotter/archive/UK100-M5-AOS-P1/COST_PROXY.json`

OS scorecards must state `Leak_source`. Do not promote L2 LIVE_WITHHOLD or P7 on prior alone if zone flips Negative after deals. M5 Leak prior is **higher** than M15 SL2500 books — denser SL (1800) raises `c_R`.

---

## 1. 1R (currency)

```
1R = InpSL_Points × volume × tick_value
```

| Field | Research default |
| --- | --- |
| SL points | **1800** |
| Volume | **0.1** |
| Point | 0.01 |
| Proxy 1R $ | ~**$1.80–2.40** (confirm on deal export; tip path used ~$2.41/R calibrated) |

---

## 2. Cost ladder (authority order)

| Rank | `Leak_source` | When to use |
| ---: | --- | --- |
| 1 | `measured` | Deal blotter with entry+exit friction |
| 2 | `journal_2x_entry_spread_median` | **Current interim OS** (tip OPEN spreads) |
| 3 | `prior` | Design card **4.0 pp** — footnotes / P0 freeze |

### 2.1 Journal proxy (tip May→Aug 2026 · P1)

| Component | Value |
| --- | ---: |
| Entry spread median | **120 pts** (n=116 · mean 121.4 · max 140) |
| Round-turn floor | `2 × 120 / 1800` → `c_R = 0.133R` |
| Leak_proxy | **5.93 pp** |
| BM (WR 52.6%) | +8.14 pp |
| EF_proxy | **+2.22 pp** |
| Zone | **Positive** (thinner than prior EF; still &gt; 0) |

Design prior (160 RT pts → Leak 4.0 pp → EF +4.1 pp) was **optimistic** vs journal 2×spread — same pattern as M15.

### 2.2 Design prior (P0 freeze footnote)

| Component | Value |
| --- | ---: |
| Round-turn cost prior | ~**160 pts** |
| Leak_prior | **4.0 pp** |
| Tip EF_prior | **+4.1 pp** |

### 2.3 Still missing

| Item | Need |
| --- | --- |
| Measured Leak | Entry+exit commission/swap/spread per closed trade |
| Zone flip check | If measured Leak ≥ BM → Fragile/Negative → no P7 |

---

## 3. OS reporting rule

Every M5 AIOS scorecard:

```text
Leak_source: prior | journal_2x_entry_spread_median | measured
Leak_pp: <value>
EF: BM − Leak
baseline_ref: UK100_M5_AOS_BASELINE_v1
```

Until measured lands, iterate on **ΔE_N** vs tip baseline; treat EF_prior as soft.

---

## 4. Explicit non-claims

- Do not use M15 Leak **2.9 / 4.27 pp** on M5 SL1800.  
- Do not “fix” Leak by thinning SL — geometry locked in P0.  
- ATR max 869 is not a cost lever.
