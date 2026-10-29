# BMRG — Asset Grouping Roadmap

**Version:** 1.0.8  
**Status:** ACTIVE · GRP-P0…P5 complete · **primary JP225+DE40**  








**Replaces:** [`diversification_roadmap.md`](./diversification_roadmap.md) (superseded — cluster DIV-P* phases discarded)  
**Parents:** [`live_asset_profile.md`](./live_asset_profile.md) · tip review canvas `bmrg-tip6m-sleeve-review.canvas.tsx`  
**Sleeve panel:** [`DIV_P2_RUNCARD.md`](./DIV_P2_RUNCARD.md) · artefacts `infra/artefacts/diversify/P2_LATEST/`  
**Code (planned):** `infra/src/grouping/` · artefacts `infra/artefacts/grouping/` · blotter `blotter/archive/GRP-*`

**Not:** one “best” combo · live `f` raise from tip E_N · SL/TP retune · treating EUR+AUD as diversified by default

---

## 0. Authority

| Artifact | Role |
| --- | --- |
| This roadmap + scored `GRP-*` blotters | **Normative** for group admission |
| Tip 6m sleeve tapes / SCORECARD | Input panel (membership search) |
| `live_asset_profile.md` | Attach identity (magic / preset) |
| Canvas / chat | **Display only** |

A sleeve with tip E_N > 0 is eligible for search. It does **not** auto-enter a live group.

---

## 1. Objective

Split the live book into **small groups** of size **k ∈ {2, 3, 5}** (and optional k=4) such that, over declared trading windows, the **joint** path has positive cycle expectancy — and emit a **range** of acceptable groups, not a single champion.

```
For each candidate set S (|S| = k) and cycle T ∈ {M, Q, Y, trailing}:

  R_S,t  = Σ_{i∈S} w_i · R_i,t          # equal weight first
  cycle  = sum of R_S over calendar T

maximise   P(cycle_ΣR > 0)  and  E[cycle_ΣR]
subject to CVaR_cycle within survivable band under declared f
           co-loss / twin-risk not worse than EUR-only baseline
           shared account fuse (daily-loss halt) modelled
           frequency mix not all-sparse or all-fuse-hungry

never maximise single-sleeve WR or tip $ alone
never promote from tip window without holdout / bootstrap bands
output a Pareto / threshold range of S — ops picks among them
```

### Frozen universe (first book)

| ID | Broker | TF | Magic | Tip tier (2026-05→10) |
| --- | --- | ---: | ---: | --- |
| EURUSD | EURUSD | M5 | 8210204 | Core |
| JP225 | JPN225 | M5 | 26161907 | Core |
| DE40 | DE30 | M5 | 26151907 | Core |
| AUDUSD | AUDUSD | M5 | 8230931 | Watch (Sep/Oct fade) |
| USDJPY | USDJPY | M15 | 26131807 | Watch (Fragile / sparse) |
| UK100 | UK100 | M5 | 26121907 | Caution (halt ~4 Sep) |
| AAPL | Apple | M5 | 26162017 | Caution (EF Below) |

Panel source: tip 6m live-preset Tester · designed `pnl_R` · `P2_LATEST/sleeves/*_live_fire_tape.csv`.

---

## 2. Working hypothesis

> Sleeve edges are real but **conditionally correlated**. USD-fade (EUR/AUD) and EU indexes (UK100/DE40) share bad days; JP225 and US-hours AAPL can offset EU open pain; USDJPY is session-gated FX, not a second AUD.  
> Account **daily-loss fuse** turns same-day twin SL into a book-wide pause — groups must model the fuse.  
> Optimal map is a **menu of 2–5 sleeve packs** with cycle-hit evidence, not equal-weight seven.

| Claim | Stance |
| --- | --- |
| Search all \(\binom{7}{k}\) for k=2…5 (112 sets) before any ML | **Require** |
| Output a **range** (Pareto / threshold set), not one combo | **Require** |
| EUR+AUD both at SCALE = default group | **Reject** |
| UK100+DE40 both at full f without co-loss PASS | **Reject** |
| Tip E_N rank = group rank | **Reject** |
| Halted / sparse sleeves (UK100, late USDJPY) need interrupted-panel flags | **Require** |

---

## 3. Math contract

### 3.1 Inputs

| Symbol | Definition |
| --- | --- |
| \(R_{i,t}\) | Sum of designed `pnl_R` for sleeve \(i\) with **close date** = \(t\) (else 0) |
| \(n_i / 30d\) | Tip frequency (trades per 30 calendar days) |
| \(E_N^{(i)}\), \(\mathrm{EF}_i\), \(\mathrm{maxDD}_i\) | Sleeve full-window metrics (features / filters) |
| \(w\) | Equal weight \(1/k\) until GRP-P3; then inv-vol / HRP / risk budget |

### 3.2 Group metrics (every candidate × every cycle)

| Metric | Definition |
| --- | --- |
| `sum_R` | \(\sum_t R_{S,t}\) over cycle |
| `positive_cycle` | `sum_R > 0` |
| `hit_rate` | Fraction of periods with `positive_cycle` (M / Q / Y) |
| `E_cycle` | Mean period `sum_R` |
| `CVaR_20` | Mean of worst 20% period returns |
| `maxDD_p` | Max drawdown of cumulative \(R_S\) |
| `co_loss` | Share of active days with ≥2 sleeves losing |
| `fuse_days` | Days with ≥2 losers and \(R_S < -1.0R\) (heuristic → calibrate later) |
| `freq_mix` | Spread of member `trades_per_30d` (flag all-high or all-low) |

### 3.3 Admission (range, not champion)

A set \(S\) enters the **acceptable range** if **all** hold on tip panel **and** survive bootstrap/holdout (GRP-P2):

1. `month_hit ≥ 0.67` **or** not worse than EUR-only month_hit by > 0.10  
2. `quarter_hit ≥ 0.67`  
3. `CVaR_20` ≥ EUR-only CVaR − tolerance (declare in scorecard)  
4. No hard-ban pair at full weight (see §5) unless stress PASS  
5. Confidence band on month_hit excludes pure noise (bootstrap lower bound ≥ floor) — **cleared in GRP-P2** (`P2_LATEST/ACCEPTABLE_RANGE.json`)

Rank OOS-stable by clean → boot_hit_p10 → val_sum_R → month_hit → sum_R — ops picks; do not auto-attach.

---

## 4. Phases

### GRP-P0 — Daily panel + exhaustive enum *(complete)*

Build from tip tapes; score every k=2…5 set under equal weight.

| Task | Deliverable | Status |
| --- | --- | --- |
| **P0-T01** | Daily \(R_{i,t}\) panel from `P2_LATEST/sleeves/*` | **DONE** |
| **P0-T02** | Enumerate \(\binom{7}{2}+\cdots+\binom{7}{5}\) = 112 sets | **DONE** |
| **P0-T03** | Period tables M/Q + hit / E / CVaR / maxDD per set | **DONE** |
| **P0-T04** | Seed filters: core / watch / caution tiers + hard bans | **DONE** |
| **P0-T05** | `ACCEPTABLE_RANGE.json` + `REVIEW.md` · archive `GRP-P0-T01` | **DONE** |

**Run:** `python -m src.grouping.run_enum` from `infra/`  
**Artefacts:** `infra/artefacts/grouping/LATEST/` · `blotter/archive/GRP-P0-T01/`  
**Result (tip):** 66 provisional accepted (50 soft-clean · 16 soft-flagged) · 46 rejected (mostly quarter_hit / hard_ban EUR+AUD). Top soft-clean: **JP225+DE40** (m/q hit 1.0 · sum_R +31).

### GRP-P1 — Dependence + twin stress *(complete)*

| Task | Deliverable | Status |
| --- | --- | --- |
| **P1-T01** | Pairwise ρ / co-loss on tip daily panel | **DONE** |
| **P1-T02** | Hard-ban & soft-penalty matrix (USD-fade · EU index) | **DONE** |
| **P1-T03** | Re-rank enum with penalties; adverse-month conditioned hit | **DONE** |

**Run:** `python -m src.grouping.run_stress` from `infra/` (requires P0 LATEST)  
**Artefacts:** `infra/artefacts/grouping/P1_LATEST/` · `blotter/archive/GRP-P1-T01/`  

**Result (tip):** Hard ban still **EURUSD+AUDUSD** (seed; measured co_loss 0.26). Soft: **DE40+UK100** (seed) + **JP225+AAPL** (measured co_loss 0.33). No EU-twin escalate to hard (UK/DE co_loss below 0.40). P0 66 → P1 kept 66 · **clean resilient 32**. Top: **JP225+DE40** (pen 0 · tip Sep/Oct hit 1.0 · sum_R +31).

### GRP-P2 — Offline sim: bootstrap + holdout *(complete)*

| Task | Deliverable | Status |
| --- | --- | --- |
| **P2-T01** | Block bootstrap of months/weeks → hit-rate bands | **DONE** |
| **P2-T02** | Holdout: fit on May–Aug, validate Sep–Oct (soft months) | **DONE** |
| **P2-T03** | Fuse model stub (ddl % → pause) on multi-sleeve loss days | **DONE** |
| **P2-T04** | Narrow acceptable range to OOS-stable sets | **DONE** |

**Run:** `python -m src.grouping.run_bootstrap` from `infra/` (requires P1)  
**Artefacts:** `infra/artefacts/grouping/P2_LATEST/` · `blotter/archive/GRP-P2-T01/`  

**Gates:** boot month-hit p10 ≥ 0.50 · Sep–Oct sum_R ≥ 0 · Sep–Oct hit ≥ 0.50 · fuse hit-drop ≤ 0.34  
**Result:** P1 clean-resilient 32 → **OOS-stable 24** (8 fail holdout_val_sum, mostly AUD-heavy). Provisional cleared for tip panel. Top by val_sum: **EURUSD+DE40+USDJPY**; highest sum_R still **JP225+DE40** (+31).

### GRP-P3 — Weights inside admitted groups *(complete)*

| Task | Deliverable | Status |
| --- | --- | --- |
| **P3-T01** | Equal vs inv-vol vs risk-parity on each range member | **DONE** |
| **P3-T02** | Optional HRP distance on daily R | **DONE** |
| **P3-T03** | f budget: production sleeve vs research members | **DONE** |

**Run:** `python -m src.grouping.run_weights` from `infra/` (requires P2)  
**Artefacts:** `infra/artefacts/grouping/P3_LATEST/` · `blotter/archive/GRP-P3-T01/`  

**Result:** On tip OOS-stable set, **equal weight wins 24/24** under f_budget ranking (raw: equal 23 · HRP 1). Inv-vol / risk-parity / HRP do not beat equal on month_hit→sum_R for this panel. f_budget caps (EURUSD floor 0.25 / cap 0.50 · research 0.40 · caution 0.25) nudge a few packs (e.g. EURUSD+JP225 → 0.56/0.44). Top: **JP225+DE40** equal 50/50 · sum_R +31.

### GRP-P4 — Search enhancements *(complete)*

Membership for n=7 is already enumerated; P4 enhances the **OOS-stable 24** with tail stress, a multi-objective Pareto front, and a lightweight surrogate.

| Task | Deliverable | Status |
| --- | --- | --- |
| **P4-T03** | Tail co-loss / lower-tail dependence beyond Pearson | **DONE** |
| **P4-T01** | Multi-objective Pareto over hit / E / CVaR / fuse / tail | **DONE** |
| **P4-T02** | Surrogate ranker (features → predicted month-hit / OOS fragility) | **DONE** |

**Run:** `python -m src.grouping.run_p4` from `infra/` (requires P2)  
**Artefacts:** `infra/artefacts/grouping/P4_LATEST/` · `blotter/archive/GRP-P4-T01/`  

**Result:**  
- Tail (q=0.2): no new hard escalations (EUR+AUD already hard; tip tail_dep 0.61). **8 new soft** proposals (e.g. DE40+AUDUSD, AUD+AAPL, EUR+USDJPY).  
- Pareto front **5** champions: `JP225+DE40` (max ΣR) · `DE40+USDJPY` (holdout) · `JP225+USDJPY` (CVaR) · `EURUSD+DE40+USDJPY+AAPL` (min DD) · `USDJPY+UK100` (min tail).  
- Surrogate ridge LOO R² **0.62** · strongest coef **has_aud (−)** — aligns with P2 AUD holdout fails.

### GRP-P5 — Ops promote *(complete)*

| Task | Deliverable | Status |
| --- | --- | --- |
| **P5-T01** | HITL: pick 1–N groups from acceptable range + weights | **DONE** |
| **P5-T02** | Update `live_asset_profile.md` capital / group map | **DONE** |
| **P5-T03** | VPS attach policy (full / light / off per sleeve) | **DONE** |

**Run:** `python -m src.grouping.run_promote` from `infra/`  
**Artefacts:** `infra/artefacts/grouping/P5_LATEST/` · `blotter/archive/GRP-P5-T01/`  

**HITL freeze:** Primary **JP225+DE40** (equal 50/50 · max_sum_R). Secondaries: DE40+USDJPY · JP225+USDJPY · EURUSD+DE40+USDJPY+AAPL · USDJPY+UK100 (watch). EURUSD stays standalone production; AUDUSD ft_twin_only; UK100 off pending halt review.

**HITL does not discharge the rest of the OOS-stable set.** Full **24-pack pool** (7-asset universe): [`doc/GRP_OOS_STABLE_POOL.md`](GRP_OOS_STABLE_POOL.md).

---

## 5. Hard bans & soft penalties (seed)

| Rule | Type | Note |
| --- | --- | --- |
| EURUSD + AUDUSD both full weight | Hard ban default | USD-fade twin |
| UK100 + DE40 both full weight | Soft → hard until co-loss PASS | EU index twin + fuse |
| Group of only Caution sleeves | Soft penalty | AAPL + UK100 alone |
| Group with halted panel (UK100 post-4 Sep) | Flag interrupted | Don’t treat as full tip Q |
| All members `trades_per_30d` > 20 | Soft penalty | Fuse concentration |
| All members `trades_per_30d` < 10 | Soft penalty | Sparse / noisy cycle |

Core seed packs to always score (not auto-promote):

- `{EURUSD, JP225}` · `{EURUSD, DE40}` · `{EURUSD, JP225, DE40}`  
- `{EURUSD, JP225, USDJPY}` · `{DE40, JP225, AAPL}` (light AAPL)

---

## 6. Anti-patterns

1. Crowning one combo from tip without bootstrap/holdout.  
2. Ignoring account fuse on same-day multi-SL.  
3. Mixing magics inside one sleeve series.  
4. Calling EUR+AUD “diversified.”  
5. Raising live `f` from a grouping scorecard.  
6. Using LLM portfolio picks without running §3 metrics.  
7. Treating DIV-P0 proxy clusters as current authority.

---

## 7. Inputs already in hand

| Asset | Tip n | E_N | EF zone | m_hit | Note |
| --- | ---: | ---: | --- | ---: | --- |
| JP225 | 72 | 0.42 | Strong | 0.67 | Best edge quality |
| AAPL | 46 | 0.34 | Below | 0.40 | Leak 15.3 |
| USDJPY | 49 | 0.30 | Fragile | 0.80 | Sparse late tip |
| DE40 | 112 | 0.29 | Strong | 0.83 | Highest sum_R |
| AUDUSD | 63 | 0.21 | Strong | 0.67 | Sep/Oct fade · maxDD −10R |
| EURUSD | 110 | 0.18 | Strong | 0.83 | Production confirm |
| UK100 | 121 | 0.17 | Fragile | 0.60 | Halt ~2026-09-04 |

---

## 8. Run (as modules land)

```bat
cd infra
python -m src.grouping.run_enum
python -m src.grouping.run_stress
python -m src.grouping.run_bootstrap
python -m src.grouping.run_weights
python -m src.grouping.run_p4
python -m src.grouping.run_promote
```

Outputs: `grouping/LATEST/` · `P1`…`P5_LATEST/` · archives `blotter/archive/GRP-P*-T01/`.

Sleeve refresh (unchanged): `python -m src.diversify.run_p2_scorer --log … --from 2026-05-01 --to 2026-10-20 --match-tester-window`

---

## 9. Change log

| Ver | Date | Note |
| --- | --- | --- |
| 1.0.0 | 2026-10-22 | Initial asset grouping roadmap · replaces diversification_roadmap DIV-P* |
| 1.0.1 | 2026-10-22 | GRP-P4 search enhancements paused |
| 1.0.2 | 2026-10-22 | GRP-P0 enum complete · 66 provisional groups |
| 1.0.3 | 2026-10-22 | GRP-P1 dependence / twin stress · clean resilient 32 |
| 1.0.4 | 2026-10-22 | GRP-P2 bootstrap + holdout + fuse · OOS-stable 24 |
| 1.0.5 | 2026-10-22 | GRP-P3 weights · equal dominates tip · f_budget caps |
| 1.0.6 | 2026-10-22 | GRP-P4 resumed |
| 1.0.7 | 2026-10-22 | GRP-P4 complete · Pareto 5 · tail soft +8 · surrogate R² 0.62 |
| 1.0.8 | 2026-10-22 | GRP-P5 HITL · primary JP225+DE40 · live profile capital map |
| 1.0.9 | 2026-10-22 | OOS-stable pool MD · HITL = default map, not discard (`GRP_OOS_STABLE_POOL.md`) |
