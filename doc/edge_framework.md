# BMRG Edge Framework

**Version:** 1.1.2  
**Status:** Normative for BMRG benchmarking  
**Parent:** `doc/unified_edge_framework.md` v1.0  
**Companions:** `system_profile.md` · `doc/edge_discovery.md` · `doc/candidate_pool.md` · `doc/ai_OS.md`  
**Canonical G0 champion (Harvest):** `Profiles/Tester/BMRG/EDX-P2-T04_SL300_TP300_RR1_champFilters_G0_long.set`  
**AI paper stack (not champ):** `Profiles/Tester/BMRG/aistack.set` (magic **8399001** · AOS overlay · STAY_PAPER)  
**Secondary (Growth / prior P25 base):** `Profiles/Tester/BMRG/EDX-P4-T01_champion_T05_currency_G0_long.set`  
**Legacy monthly preset:** `Profiles/Tester/BMRG/BMRG-EURUSD-M5-2026-09_EF-G1.set` (pre-filter; not current champ)


This document **binds** the unified edge framework to BMRG. Where this file and the unified doc conflict on BMRG procedure, **this file wins**. Formulae remain those of the unified doc.

---

## 0. Canvas caveat

| Artifact | Role | Authority |
| --- | --- | --- |
| **This markdown** | Contract: score BMRG, gates, adapter | **Normative** |
| **`unified_edge_framework.md`** | Shared maths, G0–G5 | Normative for formulae |
| **`system_profile.md`** | Behaviour / class thesis | Evidence |
| **`candidate_pool.md`** | Deployable sleeve registry | Operational evidence |
| **`edge_discovery.md`** | EDX experiment plan (engine isolation) | Process — main stream closed |
| **`ai_OS.md`** | AOS layers L1–L10 around frozen engine | Process — paper OS / promote |
| **Canvas** | Visual snapshot | **Display only** |

**Rules:** Canvas ≠ verdict. Blotter scored under this doc wins. Changing 1R / event / gate bindings bumps this version.

---

## 1. Gaps in the unified framework — BMRG fillings

| # | Unified gap | BMRG binding |
| --- | --- | --- |
| G-A | Grid trade event | §2. MaxLevels=1 → ticket = event. MaxLevels>1 → basket `event_id`; ticket WR forbidden. |
| G-B | 1R declaration | Hard SL points × volume × tick value. G0: `InpSL_Points` = event 1R. Scorecard states SL. |
| G-C | RR vs MID exit | Realised `R` always; never assume RR. TP=0 → MID_HEAVY. |
| G-D | EURUSD M5 costs | §4. Overnight swap mandatory (no session flatten). |
| G-E | Regime tags vs filters | Champ stack: `regime_filtered=true` for **session 12–20 + skip Tue**. ATR/ER cells still preferred when tagged. |
| G-F | Pips mode | **Inadmissible** Stage 1–3. Currency only. |
| G-G | Min-lot vs f | Report `f_declared` and `f_realised`. Stage 3 uses f_realised. |
| G-H | Session vs inventory | Entries gated; exits continue → overnight Leak in `c_R` / MC. |
| G-I | Pause / daily flat | Keep in blotter; tag `exit_reason`. |
| G-J | Preset identity | `preset_id`, magic, ea_version; mismatch → G0 fail. |
| G-K | Baseline frequency | Champ filters EURUSD M5: provisional **~35–80 events / 90d**; recalibrate from pool long n. |
| G-L | Mid rarity | Mid share &lt;5% → realisation `FIXED_RR_FADE`. |
| G-M | **Candidate pool** | Discovery admits sleeves with E_N>0 and WR>BWR (EF>0 preferred). Production-sized capital still needs G0–G5 on that member. See §9. |
| G-N | **Window policy** | Long = full EDX window to last **complete** month end. Trailing **3 complete months** = regime stress. Incomplete current month = footnote only. |

---

## 2. BMRG trade-event contract

### 2.1 Geometry modes

| Mode | Inputs | Event rule | Gates? |
| --- | --- | --- | --- |
| **G0** | MaxLevels=1, MaxEntries=1, hard SL | One lifecycle = one event | **Yes** (pool + P25) |
| **Grid basket** | Levels or entries > 1 | Basket flat = one event | Yes only if aggregated |
| **Mixed as tickets** | — | — | **G0 fail** |

### 2.2 Win / loss

Win: `pnl_R > 0` after costs. Loss: `pnl_R < 0`. Scratch: exclude from WR/R; keep in frequency/cost.

### 2.3 `exit_reason`

`TP` · `SL` · `MID` · `DAILY_FLAT` · `EQUITY_HALT` · `MANUAL` / `EOT` · `OTHER`

---

## 3. Stage 0 — Core identities

```
BWR = 1 / (1 + R)
E_N = WR × (R + 1) − 1 = (R + 1) × BM
BM  = WR − BWR
```

### 3.1 Designed geometries in the pool

| Sleeve | SL / TP | RR | BWR(RR) | Role |
| --- | --- | --- | --- | --- |
| **Harvest (champion)** | 300 / 300 | 1.0 | 50% | Hit-rate / **current primary** |
| Growth | 300 / 450 | 1.5 | 40% | Best long EF / secondary |
| Survival | 200 / 450 | 2.25 | ~30.8% | Low breakeven |
| Balanced-scale | 200 / 300 | 1.5 | 40% | Scale of Growth |
| Mid | 300 / 0 | realised | from R | Experimental |

Shared champ filters: **StartHour=12, EndHour=20, TradeTue=false**, BBDev=2.2, G0, currency.

### 3.2 Soft targets (G0, after costs)

| Metric | Soft target | Fail signal |
| --- | --- | --- |
| WR | > BWR (+ margin) | ≤ BWR after Leak |
| R | ≈ RR on FIXED_RR | R ≪ RR without WR lift |
| BM / EF | BM>0; EF>0 (prefer EF>M) | EF ≤ 0 |
| E_N | > 0 | ≤ 0 on W250/W500 |

### 3.3 Side diagnosis (locked)

**WR-side** on G0 pool (Growth + Harvest): R ≈ RR, AL ≈ 1R. Do not treat “tighter SL to fix AL” as the default structural fix; use filters / entry hygiene / sleeve blend.

---

## 4. Stage 1 — Cost & leak

### 4.1 Defaults (`costs_defaulted` until measured)

| Component | Default |
| --- | --- |
| Spread | Measured mean entry spread when available; else ~5.5 pts on champ logs |
| Round-turn proxy | **3 × spread** pts → `c_R = (3×spread)/SL_points` |
| Commission | Broker card (else 0 flagged) |
| Swap | Broker × nights (mandatory) |
| Slippage | Included in 3× proxy until fill blotter |

```
Leak = c_R / (R + 1)     # as WR-equivalent fraction → ×100 for pp
EF   = BM − Leak
```

### 4.2 Zones

| Zone | Condition | Action |
| --- | --- | --- |
| Negative | EF ≤ 0 | Reject / POOL_DROP or costs_fragile |
| Fragile | 0 &lt; EF ≤ M | Research / small-f only |
| Robust | EF > M | Eligible Stage 2/4 |

### 4.3 Champion snapshot (admissible — not a substitute for re-score)

| Metric | Harvest P2-T04 long | Growth P4-T01 long |
| --- | --- | --- |
| n / WR / R | 530 / 54.5% / 1.0 | 420 / 47.4% / 1.5 |
| BM / Leak / EF | ~+4.5 / ~2.2 / **1.77** | +7.4 / ~2.2 / **5.18** |
| E_N / 3M EF | +0.091R / **6.43** | +0.185R / 0.22 |
| Final | ~$533 | ~$621 |

---

## 5. Stage 2 — Health windows

| Window | Size | Role |
| --- | --- | --- |
| W100 | 100 | Investigation |
| W250 | 250 | Lifecycle |
| W500 | 500 | Confirm |
| Calendar 3M | trailing complete months | Sleeve weight / stress |

Lifecycle: Expanding / Stable / Compressing / Near frontier / Below frontier — same hooks as v1.0 (cut f / MaxLevels=1 / halt).

---

## 6. Stage 3 — Capital

| Item | Binding |
| --- | --- |
| f | 0.5% declared; use **f_realised** |
| Kelly | Quarter–half Kelly of shrunk WR; cap ≤1% without new Stage 4 |
| DD_limit | 25% default; EA halt 15% OK if tighter |
| Daily loss | 3% + flatten in path / MC |
| Ruin | P(equity ≤ 0.5 C₀) ≤ 1% |
| **Pool sizing** | Split small-f across ≥2 KEEP roles; do not put full f on 3M-only thin n |

---

## 7. Stage 4 — Gates

| Gate | BMRG notes |
| --- | --- |
| **G0** | Currency; G0 geometry; preset match; n≥385 for G1–G3 |
| **G1** | EF>M full + W500; WR > BWR+Leak; R bootstrap OK |
| **G2** | Anchored WF; WFE≥0.5; OOS E_N>0 in ≥75% folds |
| **G3** | BM_worst>0 on ATR×ER **or** `regime_filtered=true` (champ session+skipTue) |
| **G4** | MC-1/2/3; block 20; overnight path |
| **G5** | ±10% BBDev, SL, TP, Risk%; EF>0 at cost ×1.5 |

```
PRODUCTION-WORTHY(BMRG) = G0 ∧ G1 ∧ G2 ∧ G3 ∧ G4 ∧ G5
```

**Status (2026-09-27):** Operational engine champion = **Harvest P2-T04**. Growth sleeve **G0–G4 PASS**, **G5 FAIL** (TP−10). Harvest **G5 not yet re-run**. **NOT PRODUCTION-WORTHY.**

**AI OS (paper):** BMRG v1.20 ships AOS overlay (`aistack` magic 8399001). Offline P0–P7 complete; tester long EF **5.45 Robust** vs engine **2.33** — still **STAY_PAPER** (no `AOS_LIVE`; OOS AUC weak; L10 unsigned). Score OS candidates under this framework the same as engine sleeves; OS may only permit/withhold/size/halt — never rewrite entries. See `doc/ai_OS.md` · `doc/aos_p7_promotion.md`.

Pool members may still run small-f research / paper blend.

---

## 8. Adapter bindings

### 8.1 Metadata

```text
ea_name: BMRG
designed_rr: <from SL/TP>
risk_definition: hard_stop_points
regime_filtered: true    # champ: session 12-20 + skip Tue
baseline_frequency: 60
costs_defaulted: <list>
preset_id: EDX-P2-T04_SL300_TP300_RR1_champFilters_G0_long   # champion; or pool member
geometry_mode: G0_SINGLE
symbol: EURUSD
timeframe: M5
magic: <InpMagic>
pool_role: Harvest|Growth|Survival|Scale|Mid|Other
```

### 8.2 Extra blotter fields

`exit_reason` · `level_index` · `bb_dev` · `spread_points_entry` · `session_ok` · `group_event_id` · `signal_tag`

### 8.3 event_id

```text
event_id = "{magic}-{symbol}-{side}-{YYYYMMDDhhmmss}-{first_ticket}"
```

---

## 9. Candidate pool protocol (discovery)

1. Score currency blotter (long and/or 3M per G-N).  
2. Label **POOL_KEEP** | **costs_fragile** | **POOL_DROP**.  
3. Update `doc/candidate_pool.md`.  
4. Forbidden: discard KEEP solely because E_N or $ &lt; champion.  
5. **Hygiene / G5 next:** hold **Harvest P2-T04** payoff + filters fixed unless task names another sleeve.  
6. Large production capital: still require G0–G5 on the chosen member.

### Forbidden evidence (unchanged +)

- Ticket WR with MaxLevels>1  
- Pips-mode for Stage 1–3  
- Preset mismatch claims  
- Optimising on profit/WR alone  
- Using incomplete current month as primary admission  

---

## 10. Benchmark protocol

1. G0 geometry; currency deposit.  
2. Confirm Inputs = claimed preset (SL/TP/session/Tue/magic).  
3. Blotter → events → WR, R, BWR, BM, Leak, EF, M, E_N.  
4. W100/W250/W500 + optional 3M stress.  
5. G0–G5 if production claim; else pool label.  
6. Refresh Canvas from scorecard only (display).

---

## 11. Monitoring runbook

| Trigger | Action |
| --- | --- |
| WR ≤ BWR on W250 | Cut sleeve f or swap to another KEEP role |
| EF ≤ 0 after Leak | costs_fragile / DROP |
| RR−R gap > 25% | Check MID mix / slippage / flats |
| FREQUENCY_STALL | Loosen cooldown/session only with EDX task |
| G5-style TP fragility | Do not shrink TP toward 405 without re-pool |

Order: data → execution → regime → structural.

---

## 12. Scorecard fields

```text
framework_unified: 1.0
framework_bmrg: 1.1.2
preset_id / pool_role / geometry_mode / window / n
aos_overlay: none|aistack|AOS_LIVE   # optional; score under same stages
WR, R, RR, RR-R, BWR, BM, Leak, EF, M, E_N
f_declared, f_realised_mean
lifecycle_W250, ΔD
G0..G5 or pool_label
verdict: PRODUCTION-WORTHY | NOT PRODUCTION-WORTHY | POOL_KEEP | ...
```

---

## 13. Document map

| File | Purpose |
| --- | --- |
| `doc/unified_edge_framework.md` | General maths & gates |
| `doc/edge_framework.md` | **This file — BMRG binding v1.1.2** |
| `doc/edge_discovery.md` | EDX task plan (**closed as main stream**) |
| `doc/ai_OS.md` | **AI OS layers + AOS tasks** (wraps engine · v0.2 EA-wired) |
| `doc/aos_aistack.md` | aistack preset / wiring contract |
| `doc/candidate_pool.md` | Sleeve registry |
| `system_profile.md` | Class + observed behaviour |
| `blotter/archive/` | Immutable scorecards (EDX + AOS) |

---

## 14. Versioning

- **1.1.2** — AOS companion + aistack paper status; scoring rules unchanged.  
- **1.1.1** — Operational champion → Harvest P2-T04 (300/300); Growth retained secondary.  
- **1.1** — Candidate pool, champ filters (12–20 / skip Tue), P25 Growth base, window policy, WR-side lock, G0–G4/G5 status.  
- Bump this version when bindings, event rules, cost defaults, or gate interpretations change.
