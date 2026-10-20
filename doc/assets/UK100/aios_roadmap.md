# UK100 — AIOS Roadmap

**Version:** 0.1.0  
**Status:** **P0–P7 complete** — research OS **HITL ARMED** (expansion only; not FX live replace)  
**Engine lock (OS baseline):** Balanced P0 · magic **26101201** · **AOS OFF**  
**Research OS arm:** magic **26111307** · `BMRG-M15-UK100-6M-P7_research_OS_ARMED.set` · [`AIOS_SIGNOFF.md`](./AIOS_SIGNOFF.md)  
**Preset (engine):** `Profiles/Tester/BMRG/UK100/BMRG-M15-UK100-6M-P0_balanced_chart.set`  
**Parents:** [`edge_framework.md`](./edge_framework.md) · [`system_profile.md`](./system_profile.md) · `doc/ai_OS.md` · `doc/unified_edge_framework.md`  
**Blotter:** `blotter/inbox/` → `blotter/archive/UK100-AOS-*/` after review  

**Not** EURUSD aistack · **not** AUDUSD L2 pin · **not** AAPL L2det · **not** a live replace.  
**Sibling M5 AIOS:** [`aios_roadmap_M5.md`](./aios_roadmap_M5.md) · magic **26101905** — separate stream · do not merge pins.

---

## 0. Canvas caveat

| Artifact | Authority |
| --- | --- |
| This roadmap + scored blotters under `edge_framework.md` | **Normative** for UK100 AIOS work |
| `system_profile.md` | Evidence / descriptive |
| Canvas / chat charts / UI tiles | **Display only** |

Verdicts come from ledger + scorecard. Tip-only charts never promote a layer. Truncated hist (`hist_from` ≥ 2025.12.17) is never multi-year evidence.

---

## 1. What this is / is not

| This is | This is not |
| --- | --- |
| A **UK100-owned AIOS** that permits / withholds / sizes / observes / adapts Balanced P0 | A new SL/TP or BBDev optimisation programme |
| Layered work with task IDs `UK100-AOS-P#-T##` | A replacement entry model or trend sleeve |
| Iteration vs a frozen Balanced baseline | Immediate live attach |
| Consumption of profile bad cells (Thu, H08, Jul, Feb, tip BUY) | Re-ranking from profit / WR alone |
| Separate model store pin (`L2skip_uk_*`) | Reuse of EUR / AUD / AAPL L2 pins |

**Frozen OS objective:**

```
maximise E_N
subject to  EF hold vs baseline (−1 pp on primary tip health window is enough to keep iterating)
            MaxDD ≤ baseline MaxDD + 2 pp
never maximise WR, PF, or BM alone
never invent entries — only gate the engine fade
```

**Investigation order (unchanged):** data → execution → regime → structure.  
Do **not** touch SL/TP/BBDev/ATR max as the first OS move.

---

## 2. Working hypothesis (from UK100 profile)

> Balanced P0 already has a real meanrev edge on the home tip (May→Aug WR 49% / E_N +0.10R / +$17).  
> Remaining leak is **conditional**: fires still occur in calendar / hour / side / path cells where BM ≤ 0 or expectancy collapses (Jul, Feb, Thu, H08, tip BUY).  
> AI layers’ job: **withhold or size-down those fires**, contain streak / below-frontier path risk, keep **EF** alive after measured Leak — without rewriting the fade.

| Claim | Evidence | Stance for OS |
| --- | --- | --- |
| Edge exists | Tip EXPANSION_KEEP · E_N +0.103R | **Accept** — freeze as UK100-AOS-P0 |
| Weakness is conditional | Jul WR 29% · Feb 35% · Thu 31% · H08 31% | **Accept** — L2 skip/size, don’t chase R |
| Side flips with regime | Tip sell-led · prior buy-led | **Accept** — side-caution SOFT only when hostile; never permanent AllowBuy=false |
| ATR max already filters FRAGILE | Gate ON · design intent | **Accept** — L1 feature; do not lift ATR max as OS “fix” |
| Holds mostly intrad ay | Med win ~1.6h · overnight rare | **Accept** — L8 gap path secondary vs AAPL |
| Fixing via SL/TP first | Would reopen geometry; RR already TP>SL | **Reject as first move** |
| Borrow EUR/AUD/AAPL L2 | Wrong session / microstructure | **Reject** — UK100 pin only |
| Probe WR 54% as OS target | Design prior only | **Reject** — beat Tester tip EF/E_N |

---

## 3. Architecture (same layers as `doc/ai_OS.md`)

```
L5 Retrain ──challenger──► L2 Policy (skip/size) ──permit──► Balanced ENGINE (26101201)
L1 Tape ──────────────────►        ▲
                                   │
                          L3 Guardrails (hard veto)
                                   ▲
                          L4 Observer (W15/W20 → W100/W250)
                                   │
                          L6 Ledger (all decisions)
L8 MAE abort (secondary) · L9 session quality · L10 HITL promote
```

**Invariant:** L3 outranks L1/L2/L4/L5/L8–L10.

### UK100 layer emphasis

| Layer | UK100 focus |
| --- | --- |
| **L1** | ATR vs 1470 · London session age · DOW/hour · side · BBDev · spread · optional Ouroboros MATCH/FRAGILE · short streak |
| **L2det** | Thu · H08 · Jul-like / near-ATR-cap stress · buy-caution when sell cells dominate · never skip all buys blindly |
| **L2 AI** | Avoid-loser on Balanced fires only; pin `L2skip_uk_*` |
| **L3** | MaxDD · Below-frontier f=0 · kill-switch · streak-aware halt |
| **L4** | Small-n W15/W20 first; adopt W100/W250 when n allows |
| **L5** | Retrain on decay / Compressing; WF through decay, not only on it |
| **L6** | Full reason codes for CF scorecards |
| **L8** | Secondary (intraday book); MAE abort if path shows fast adverse vs SL |
| **L10** | Only promotion path to “UK100 OS live research” |

---

## 4. Baseline lock (UK100-AOS-P0)

Import Balanced health from scored logs / profile. **No OS code.**

| Field | Tip May→Aug 2026 | Prior Jan→Apr 2026 | Hist from 2025.12.17→2026.08 |
| --- | ---: | ---: | ---: |
| Magic / RR | **26101201** / 1.25 | same | same |
| n | **51** | 75 | 131 |
| WR | **49.0%** | 45.3% | 45.8% |
| E_N (des) | **+0.103R** | +0.020R | +0.031R |
| BM / EF_prior | +4.6 pp / **+1.7 pp** | +0.9 / −2.0 | +1.4 / −1.5 |
| Final Δ ($500) | **+$17.14** | +$4.48 | +$10.97 |
| MaxDD (path proxy) | — | — | ~5.3% |
| AOS | Off | Off | Off |

**OS compare window (default):** **tip May→Aug** — state which on every task. Prior / hist = L3 diagnostics. Tip alone may KEEP expansion OS trials; never sole production admission.

**Bad-cell registry:** [`aos_bad_cells.md`](./aos_bad_cells.md) (P0-T02).  
**Baseline packet:** [`UK100_AOS_BASELINE_v1.md`](./UK100_AOS_BASELINE_v1.md) (P0-T01).  
**Cost stub:** [`aos_cost_policy.md`](./aos_cost_policy.md) (P0-T03).

---

## 5. Iteration bar (loose on purpose)

**Accept** a layer experiment when **all** hold:

| Check | Bar |
| --- | --- |
| n remaining after skips | Report; no n≥385 floor (per UK100 edge_framework) |
| Tip-window E_N / EF | ≥ baseline − **1 pp** EF (or E_N hold if Leak pending) |
| MaxDD | ≤ baseline + **2 pp** |
| 90d fire count | ≥ 50% baseline (~18–22 / 90d) → else FREQUENCY_STALL **warn** |
| AL | Not worse unless E_N clearly improved |
| Bad-cell hit rate | Skips concentrated in registry cells (report precision/recall vs winners) |

**Reject immediately** when:

- WR↑ but E_N↓ or EF↓  
- Layer invents entries / changes SL/TP/ATR max as “OS”  
- Higher layer overrides L3 halt  
- Uses EUR/AUD/AAPL model pin on UK100  
- Permanently disables BUY because tip was sell-led  

**Promote (UK100-AOS-P7 only)** when: shadow CF beats/holds baseline · L3/L4 wired · ledger complete · HITL sign-off under `edge_framework.md`. Full G0–G5 for any live-capital claim — not for every weekly trial.

---

## 6. Phase plan (task catalogue)

### PHASE 0 — ENGINE BASELINE LOCK (`UK100-AOS-P0`) — **DONE** (measured Leak still open)

| Task | Layer | Deliverable | Status |
| --- | --- | --- | --- |
| **P0-T01** | — | Freeze `UK100_AOS_BASELINE_v1` scorecard (tip + prior + hist) | **DONE** 2026-10-12 |
| **P0-T02** | — | Bad-cell registry from profile | **DONE** 2026-10-12 |
| **P0-T03** | — | Cost policy + journal Leak_proxy; deal-measured still open | **DONE** proxy 2026-10-12 · measured **OPEN** |

### PHASE 1 — L1 PERCEPTION (`UK100-AOS-P1`) — **DONE** (T04 optional open)

| Task | Layer | Deliverable | Status |
| --- | --- | --- | --- |
| **P1-T01** | L1 | UK100 feature schema v0 (`aos_l1_tape_contract.md`) | **DONE** 2026-10-12 |
| **P1-T02** | L1 | Offline tape builder from Tester Balanced fires / bars | **DONE** tip+prior · hist **OPEN** |
| **P1-T03** | L1 | Label fires: win/lose · DOW · hour · side · ATR · spread · month tag | **DONE** tip 51 + prior 75 |
| **P1-T04** | L1 | Structure flags v0 (band-ride / failed fade) — optional | OPEN |
| **P1-T05** | L1 | Ouroboros MATCH/FRAGILE month flag (soft) | **DONE** on tip tape column |

### PHASE 2 — L2 POLICY (`UK100-AOS-P2`) — **DONE**

| Task | Layer | Deliverable | Status |
| --- | --- | --- | --- |
| **P2-T01** | L2det | Parity: skip Tue + ATR max — OS mirror / no double-count | **DONE** PASS |
| **P2-T02** | L2det | SOFT skip map v1: Thu ± H08 shadow CF | **DONE** — **ARM Thu** |
| **P2-T03** | L2det | Buy-caution SOFT CF | **DONE** — **ARM BUY∧near_atr** · DISARM blanket BUY |
| **P2-T04** | L2det | Stress-month / near-ATR SOFT CF | **DONE** — **ARM Jul** · DISARM blanket near_atr |
| **P2-T05** | L2size | Lifecycle → f table (spec; wire after L4) | **DONE** SPEC (`aos_l2_size_table.md`) |
| **P2-T06** | L2 AI | Train `L2skip_uk` avoid-loser · shadow | **DONE** — **DISARM** (AUC≈0.39) |
| **P2-T07** | L2 AI | Stack CF vs P0 / L2det | **DONE** — best **v1b** Thu∨(BUY∧near_atr) |

### PHASE 3 — L3 + L4 (`UK100-AOS-P3`) — **DONE**

| Task | Layer | Deliverable | Status |
| --- | --- | --- | --- |
| **P3-T01** | L3 | MaxDD / kill / Below-frontier halt policy | **DONE** SIGNED · v1b tip trip-free |
| **P3-T02** | L3 | Cost-drift + FREQUENCY_STALL warn · streak | **DONE** SIGNED |
| **P3-T03** | L4 | Rolling health W15/W20 (+ W50 when wiring) | **DONE** paths in archive |
| **P3-T04** | L4→L3 | Recommend bus: Below → halt; Compressing → investigate | **DONE** SIGNED |

### PHASE 4 — LEDGER + STACK (`UK100-AOS-P4`) — **DONE 2026-10-12**

| Task | Layer | Deliverable | Status |
| --- | --- | --- | --- |
| **P4-T01** | L6 | Decision ledger schema + offline writer | **DONE** `aos_l6_ledger.md` |
| **P4-T02** | stack | Det stack `L1+L2det+L3+L4+L6` shadow run | **DONE** tip n_fire=33 E_N=0.36 |
| **P4-T03** | stack | + L2 AI shadow on det fires | **DONE** DISARM · 1 shadow skip |
| **P4-T04** | L8 | MAE abort advisor (shadow; secondary for intraday book) | **DONE** 5/5 loser advises |

### PHASE 5 — RETRAIN LOOP (`UK100-AOS-P5`) — **DONE 2026-10-12**

| Task | Layer | Deliverable | Status |
| --- | --- | --- | --- |
| **P5-T01** | L5 | Retrain policy + model store layout `L2skip_uk/` | **DONE** `aos_l5_retrain.md` · `train_l2_uk100.py` |
| **P5-T02** | L5 | Champ/challenger promote rules (shadow→candidate) | **DONE** AI challenger EMPTY · overlay L2det champ |
| **P5-T03** | L5 | Rollback drill | **DONE** `_drill/` pass |

### PHASE 6 — HARDENING (`UK100-AOS-P6`) — **DONE 2026-10-12**

| Task | Layer | Deliverable | Status |
| --- | --- | --- | --- |
| **P6-T01** | L9 | Session-quality soft veto (London open / spread tercile) | **DONE** BUY∧H08 ARM_SOFT shadow · spread DISARM |
| **P6-T02** | G5-ish | ±10% bound stress on L2 thresholds (not SL/TP) | **DONE** keep 0.9/1470 · loosen hurts |
| **P6-T03** | — | Confirm ATR max declared for G3 when OS armed | **DONE** PASS |

### PHASE 7 — PROMOTION (`UK100-AOS-P7`) — **DONE 2026-10-13 HITL**

| Task | Layer | Deliverable | Status |
| --- | --- | --- | --- |
| **P7-T01** | L10 | Promotion packet: CF · health · ledger · gates | **DONE** `promotion_packet.json` |
| **P7-T02** | L10 | HITL sign-off · research OS arm | **SIGNED** magic **26111307** · `AIOS_SIGNOFF.md` |
| **P7-T03** | — | Paper / tiny-f attach checklist | **DONE** in sign-off |

---

## 7. Weekly implementation table

Calendar assumes **Week 1 = week of 2026-10-13** (Mon). Slip tasks forward; do not skip P0/P1 to chase L2 AI. One primary task stream at a time; blotter clear-after-review applies.

| Week | Dates (2026) | Phase | Primary tasks | Exit criteria (done when) |
| ---: | --- | --- | --- | --- |
| **1** | Oct 13–19 | P0 | P0-T01 · P0-T02 · P0-T03 stub | Baseline + bad-cells + cost stub in `doc/assets/UK100/` |
| **2** | Oct 20–26 | P0→P1 | Deal export measured Leak · P1-T01 feature schema | `Leak_source=measured` on tip scorecard · schema reviewed |
| **3** | Oct 27–Nov 2 | P1 | P1-T02 tape builder · P1-T03 label fires | Offline tape covers tip+prior fires · labels QA’d |
| **4** | Nov 3–9 | P1 | P1-T04 (opt) · P1-T05 Ouroboros flags | Tape v0 frozen |
| **5** | Nov 10–16 | P2 | P2-T01 ATR/Tue parity · P2-T02 Thu/H08 SOFT shadow | CF ledger · E_N/EF vs baseline within bar **or** reject map |
| **6** | Nov 17–23 | P2 | P2-T03 buy-caution · P2-T04 stress-month map | Armed only if CF pass; else DISARMED |
| **7** | Nov 24–30 | P3 | P3-T01 L3 · P3-T02 stall/cost | Offline L3 trips on UK100 path · policy md |
| **8** | Dec 1–7 | P3 | P3-T03 L4 health · P3-T04 bus | W15/W20 health CSV · Below→halt verified |
| **9** | Dec 8–14 | P4 | P4-T01 ledger · P4-T02 det stack shadow | Full det stack CF vs P0 |
| **10** | Dec 15–21 | P2/P4 | P2-T06 train `L2skip_uk` · P2-T07 AI shadow CF | Model pin under `infra/artefacts/models/L2skip_uk/` · shadow only |
| **11** | Dec 22–28 | P4 | P4-T03 AI+det · P4-T04 L8 shadow | Stack CF; L8 advise-only |
| **12** | Dec 29–Jan 4 | P5 | P5-T01…T03 retrain/rollback | Store + rollback drill documented |
| **13** | Jan 5–11 | P6 | P6-T01…T03 harden | Soft veto CF; ATR G3 note |
| **14** | Jan 12–18 | P7 | P7-T01 · P7-T02 HITL | KEEP OS research arm **or** stay shadow with named gaps |
| **15** | Jan 19–25 | buffer | Slip / re-runs · P7-T03 if armed | Clean archive; roadmap status update |

### Weekly operating rhythm

| Day | Action |
| --- | --- |
| Mon | Confirm week’s primary task · load Balanced preset · note compare window (tip default) |
| Tue–Thu | Implement / run Tester / build tape or CF |
| Fri | Score under `edge_framework.md` · ACCEPT/REJECT · archive blotter · update this roadmap status |
| Ongoing | No EUR/AUD/AAPL pin · no SL/TP “quick fix” · Canvas display-only |

---

## 8. Preset / artifact naming

```text
Profiles/Tester/BMRG/UK100/UK100-AOS-P{phase}-T{task}_{layer}_{change}.set
blotter/archive/UK100-AOS-P{phase}-T{task}/
infra/artefacts/models/L2skip_uk/LATEST/
doc/assets/UK100/aos_bad_cells.md
doc/assets/UK100/aos_cost_policy.md
doc/assets/UK100/UK100_AOS_BASELINE_v1.md
doc/assets/UK100/aos_l1_tape_contract.md   # from P1
doc/assets/UK100/aos_l2_policy.md          # from P2
```

Research OS magic: keep engine **26101201**; OS experiment magics in **2611xxxx** if a separate `.set` is required — never collide with EUR/AUD live.

---

## 9. Scorecard fields (every weekly exit)

```text
framework_unified: 1.0
framework_uk100: 0.1.0
aos_task: UK100-AOS-P#-T##
preset_id / magic / window / hist_from / n
aos_overlay: none | L2det | L2AI_shadow | L2AI_withhold | L3 | stack
baseline_ref: UK100_AOS_BASELINE_v1
WR, R, BWR, BM, Leak, Leak_source, EF, M, E_N, PF
skips_n, skip_precision_bad_cell, fire_retention_pct
ΔE_N_vs_baseline, ΔEF_vs_baseline, MaxDD
verdict: ACCEPT | REJECT | HOLD_SHADOW
canvas: display_only
```

---

## 10. Document map

| File | Purpose |
| --- | --- |
| **`aios_roadmap.md`** | **This plan** |
| `edge_framework.md` | Normative scoring / gates |
| `system_profile.md` | Descriptive behaviour |
| `UK100_AOS_BASELINE_v1.md` | Frozen P0 numbers |
| `aos_bad_cells.md` | L2det seed registry |
| `aos_cost_policy.md` | Leak / deal-export stub |
| `aos_l5_retrain.md` | L5 retrain · champ/challenger · rollback (P5) |
| `doc/ai_OS.md` | Layer vocabulary |
| `blotter/archive/UK100-P0-CHART/` | Engine review (pre-OS) |
| `infra/artefacts/models/L2skip_uk/` | AI shadow store (DISARM) |

---

## 11. Versioning

- **0.1.0** — Initial UK100 AIOS plan from chat enhancement thesis; P0-T01…T03 stubs landed; weekly calendar from 2026-10-13.  
- Bump when phase order, iteration bar, pin name, or baseline window changes.

---

## 12. One-line plan

**Freeze Balanced P0, measure Leak, build a UK100-native skip/size OS aimed at Thu/H08/Jul/Feb/hostile-side cells, shadow until tip EF holds, then promote research OS only — never borrow foreign L2 or retune geometry as the first move.**

---

## 13. Status line (update Fridays)

```text
2026-10-13 | P7 HITL SIGNED | ARM_RESEARCH_OS magic 26111307 · L2det v1b · not FX replace · stream P0-P7 closed
```
