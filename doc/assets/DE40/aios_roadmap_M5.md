# DE40 M5 — AIOS Roadmap (Balanced P0)

**Version:** 0.1.7  
**Status:** **P0–P7 complete** — research OS **HITL ARMED** (expansion only; not FX/UK/M15 live replace)  
**Research OS arm:** magic **26151907** · **`DE40_5m_stack.set`** · [`AIOS_SIGNOFF_M5.md`](./AIOS_SIGNOFF_M5.md)  
**Engine lock (OS baseline):** Balanced P0 · magic **26101903** · **AOS OFF**  
**Preset (engine):** `Profiles/Tester/BMRG/DE40/BMRG-M5-DE40-6M-P0_balanced_chart.set`  
**Parents:** [`edge_framework.md`](./edge_framework.md) · [`system_profile_M5.md`](./system_profile_M5.md) · `doc/ai_OS.md` · `doc/unified_edge_framework.md`  
**Sibling (M15 — do not mix):** [`aios_roadmap.md`](./aios_roadmap.md) · magic **26101902** / **DE40stack 26141907**  
**Blotter:** `blotter/inbox/` → `blotter/archive/DE40-M5-AOS-*/` after review  

**Not** M15 DE40stack · **not** EURUSD / UK100 / USDJPY / AUD L2 pins · **not** a live replace · **not** an M15→M5 pin transplant.

---

## 0. Canvas caveat

| Artifact | Authority |
| --- | --- |
| This roadmap + scored blotters under `edge_framework.md` | **Normative** for DE40 **M5** AIOS work |
| `system_profile_M5.md` | Evidence / descriptive |
| Canvas / chat charts / UI tiles | **Display only** |

Verdicts come from ledger + scorecard. Tip-only charts never promote a layer. Probe EF is never scored EF. Broker depth from **2025.06.05** — truncated hist is never multi-year evidence.

---

## 1. What this is / is not

| This is | This is not |
| --- | --- |
| A **DE40 M5-owned AIOS** that permits / withholds / sizes / observes / adapts Balanced P0 | A new SL/TP or BBDev optimisation programme |
| Layered work with task IDs `DE40-M5-AOS-P#-T##` | A replacement entry model or trend sleeve |
| Iteration vs a frozen M5 P0 baseline | Immediate live attach or FX/UK/M15 replace |
| Consumption of M5 profile bad cells (Feb soft · May MISMATCH · Sep–Oct FRAGILE · Mar starvation) | Re-ranking from profit / WR alone |
| Separate model store pin (`L2skip_de40_m5_*` / `L2det_de40_m5_*`) | Reuse of M15 `L2det_de` / EUR / UK / AUD / AAPL pins |
| Regime-first hygiene (engine already EF>0 under Leak prior on Jan–Aug / May–Aug) | Treating Feb / May soft as class failure · thinning SL under fat spread |

**Frozen OS objective:**

```
maximise E_N
subject to  EF hold vs baseline (−1 pp on primary tip health window is enough to keep iterating)
            MaxDD ≤ baseline MaxDD + 2 pp
never maximise WR, PF, or BM alone
never invent entries — only gate the engine fade
```

**Investigation order (unchanged):** data → execution → regime → structure.  
Do **not** touch SL/TP/BBDev/ATR max/Cooldown as the first OS move.  
Do **not** thin SL below ~7000 (Leak collapses EF under DE30 spread).  
Do **not** claim Stage-1 Robust on Leak **prior** alone — measure first.  
Do **not** arm M15 `DE40stack` / `AOS_L2det_de.mqh` on M5 without M5 tape CF.

---

## 2. Working hypothesis (from M5 system profile)

> Balanced P0 M5 already has a **usable** meanrev edge on the scored blotter (Jan→Aug WR **57.1%** / E_N **+0.286R** / EF prior **+5.7 pp** / +$350.64). Probe and Tester tip-core **align**.  
> Remaining leak is **conditional / regime**: **Feb** soft (−0.10R) · **May MISMATCH** (E_N 0) · soft **Jun** · unscored **Sep–Oct FRAGILE**. ATR max already starves Mar / high-vol. Side/DOW/hour still **OPEN**.  
> AI layers’ job: **withhold or size-down regime-hostile fires**, protect **Jul–Aug MATCH** (and tip-core expectancy), contain soft-month MaxDD path, keep **EF** after measured Leak — without rewriting the fade or borrowing M15 / foreign pins.

| Claim | Evidence | Stance for OS |
| --- | --- | --- |
| Edge exists | Jan–Aug E_N +0.286R · May–Aug +0.282R · EF prior +5.5…+5.7 pp | **Accept** — freeze as DE40-M5-AOS-P0 |
| Weakness is conditional | Feb WR 40% · May WR 44.4% · Jun soft | **Accept** — L2 skip/size, don’t chase R |
| MATCH is home | Jul–Aug · Jun–Aug E_N **+0.350R** · Aug WR **68.8%** | **Accept** — protect cells |
| ATR max already filters FRAGILE | Gate ON · 469 blocks · Mar starved | **Accept** — L1 feature; do not lift ATR as OS “fix” |
| Fat spread / fat SL | Spread≈1020 · SL 7000 · Leak prior **7.0 pp** | **Accept** — measure Leak; never thin SL first |
| Probe ≈ Tester | 54.6% / +0.229R → May–Aug 57.0% / +0.282R | **Accept** — probe = prior only |
| Tip May→Oct / Sep–Oct | **MISSING** from current log | **Accept** — P0 footnote; fill before Stage-1 tip admit |
| Side / DOW / hour | Entries ~50/50 · cells OPEN | **Accept** — fill on P1 tape |
| Fixing via SL/TP first | Would reopen geometry; thin SL kills EF | **Reject as first move** |
| Borrow M15 L2det / DE40stack | Wrong TF / ATR / CD / Leak fingerprint | **Reject** — M5 pin only |
| Reject asset on Feb / May | Soft / MISMATCH months | **Reject** — regime tax, not DROP |

---

## 3. Architecture (same layers as `doc/ai_OS.md`)

```
L5 Retrain ──challenger──► L2 Policy (skip/size) ──permit──► P0 ENGINE (26101903)
L1 Tape ──────────────────►        ▲
                                   │
                          L3 Guardrails (hard veto)
                                   ▲
                          L4 Observer (W15/W20 → W100/W250)
                                   │
                          L6 Ledger (all decisions)
L8 MAE abort (secondary · cash sleeve) · L9 session quality · L10 HITL promote
```

**Invariant:** L3 outranks L1/L2/L4/L5/L8–L10.

### DE40 M5 layer emphasis

| Layer | M5 focus |
| --- | --- |
| **L1** | ATR vs **2380** · session age 08–17 · DOW/hour · side · BBDev 2.2 · CD **6** · spread vs 1500 · Ouroboros MATCH/MISMATCH/FRAGILE · streak |
| **L2det** | Feb-like · May MISMATCH SOFT (CF before blanket) · Sep–Oct FRAGILE residual · soft Jun · hour/DOW from tape · **never** blanket Aug / Jul–Aug MATCH |
| **L2 AI** | Avoid-loser on P0 fires only; pin `L2skip_de40_m5_*` |
| **L3** | MaxDD (OPEN until export) · Below-frontier f=0 · kill-switch · streak-aware halt |
| **L4** | Small-n W15/W20 first; denser M5 fire → adopt W50 earlier than M15 when n allows |
| **L5** | Retrain on decay / Compressing; WF through decay |
| **L6** | Full reason codes for CF scorecards |
| **L8** | **Secondary** (cash-sleeve); MAE abort advise-only until overnight share known |
| **L9** | Frankfurt open soft veto · spread tercile vs MaxSpread 1500 |
| **L10** | Only promotion path to “DE40 M5 OS live research” |

---

## 4. Baseline lock (DE40-M5-AOS-P0)

Import Balanced health from `system_profile_M5.md` / `blotter/archive/DE40-M5-P0/`. **No OS code.**

| Field | Tip May→Oct | Tip-core May→Aug | YTD Jan→Oct |
| --- | ---: | ---: | ---: |
| Magic / RR | **26101903** / 1.25 | same | same |
| n | **123** | **94** | **208** |
| WR | **53.7%** | **56.4%** | **52.9%** |
| E_N (des) | **+0.207R** | **+0.27R** | — |
| BM / EF_prior | +9.2 / **+2.2 pp** | ~+5.0 pp | soft (Feb/Oct) |
| Final Δ ($500) | **+$207.76** | — | +$341.27 |
| AOS | Off | Off | Off |
| Sep–Oct | n=29 · WR 44.8% · ≈0R | — | included |

**OS compare window (default):** **tip May→Oct** (Tester → 2026.10.19). Tip-core / Jan–Aug = support. Soft Feb / May / Oct = diagnostic — never sole DROP.

**Bad-cell registry:** [`aos_bad_cells_M5.md`](./aos_bad_cells_M5.md) (P0-T02).  
**Baseline packet:** [`DE40_M5_AOS_BASELINE_v1.md`](./DE40_M5_AOS_BASELINE_v1.md) (P0-T01).  
**Cost stub:** [`aos_cost_policy_M5.md`](./aos_cost_policy_M5.md) (P0-T03).

---

## 5. Iteration bar (loose on purpose)

**Accept** a layer experiment when **all** hold:

| Check | Bar |
| --- | --- |
| n remaining after skips | Report; no n≥385 floor (per DE40 edge_framework) |
| Tip-window E_N / EF | ≥ baseline − **1 pp** EF (or E_N hold if Leak pending) |
| MaxDD | ≤ baseline + **2 pp** (export baseline when available) |
| 90d fire count | ≥ 50% of tip-core baseline rate → else FREQUENCY_STALL **warn** |
| AL | Not worse unless E_N clearly improved |
| Bad-cell hit rate | Skips concentrated in registry cells (report precision/recall vs winners) |
| Protect cells | False-skip rate on **Aug / Jul–Aug MATCH / tip-core stars** must be reported |

**Reject immediately** when:

- WR↑ but E_N↓ or EF↓  
- Layer invents entries / changes SL/TP/ATR max / BB / session as “OS”  
- Thins SL below ~7000 or lifts MaxSpread as a Leak “fix”  
- Higher layer overrides L3 halt  
- Uses M15 `L2det_de` / EUR / UK / USDJPY / AUD / AAPL pin on M5 DE30  
- Permanently disables a side/DOW before tape exists  
- Claims Robust / production on Leak **prior** alone  
- Rejects asset solely on Feb soft or May MISMATCH  

**Promote (DE40-M5-AOS-P7 only)** when: tip May→Oct scored · shadow CF beats/holds baseline · L3/L4 wired · ledger complete · measured Leak preferred · HITL sign-off under `edge_framework.md`. Live capital stays off DE40 M5 until then.

---

## 6. Phase plan (task catalogue)

### PHASE 0 — ENGINE BASELINE LOCK (`DE40-M5-AOS-P0`) — **STUBS DONE** (measured Leak OPEN · tip May→Oct OPEN)

| Task | Layer | Deliverable | Status |
| --- | --- | --- | --- |
| **P0-T01** | — | Freeze `DE40_M5_AOS_BASELINE_v1` (Jan–Aug + May–Aug + MATCH + tip OPEN footnote) | **DONE** 2026-10-20 |
| **P0-T02** | — | Bad-cell registry from M5 profile | **DONE** 2026-10-20 |
| **P0-T03** | — | Cost policy + Leak prior stub; deal-measured still open | **DONE** prior 2026-10-20 · measured **OPEN** |

### PHASE 1 — L1 PERCEPTION (`DE40-M5-AOS-P1`) — **DONE** (T04 deferred)

| Task | Layer | Deliverable | Status |
| --- | --- | --- | --- |
| **P1-T00** | — | Tester tip **2026.05.01→10.19** (+ Sep–Oct) · baseline updated | **DONE** 2026-10-20 · tip n=123 · EF prior +2.2 pp |
| **P1-T01** | L1 | DE40 M5 feature schema v0 (`aos_l1_tape_contract_M5.md`) | **DONE** 2026-10-20 |
| **P1-T02** | L1 | Offline tape builder from Tester P0 fires / bars | **DONE** `build_de40_m5_fire_tape.py` |
| **P1-T03** | L1 | Label fires: win/lose · DOW · hour · side · ATR · spread · month · HALT | **DONE** tip 123 + YTD 208 + prior/core/sep–oct |
| **P1-T04** | L1 | Structure flags v0 (band-ride / failed fade) — optional | **DEFERRED** |
| **P1-T05** | L1 | Ouroboros MATCH/MISMATCH/FRAGILE month flag (soft) | **DONE** on tape columns |

### PHASE 2 — L2 POLICY (`DE40-M5-AOS-P2`) — **DONE** 2026-10-20

| Task | Layer | Deliverable | Status |
| --- | --- | --- | --- |
| **P2-T01** | L2det | Parity: skip Tue + ATR max 2380 — OS mirror / no double-count | **DONE** PASS |
| **P2-T02** | L2det | Late-session SOFT: H14/H16 shadow CF | **DONE** — H14\|16 ARM · prefer BUY∧ |
| **P2-T03** | L2det | Buy-caution SOFT CF (never blanket BUY) | **DONE** — **ARM BUY∧H14\|16** · BUY∧Oct |
| **P2-T04** | L2det | FRAGILE Oct / Sep–Oct / MISMATCH CF (protect Aug/SELL) | **DONE** — BUY∧Oct ARM · blanket DISARM |
| **P2-T05** | L2size | Lifecycle → f table (spec; wire after L4) | **DONE** SPEC (`aos_l2_size_table_M5.md`) |
| **P2-T06** | L2 AI | Train `L2skip_de40_m5` avoid-loser · shadow | **DONE** — **DISARM** (AUC≈0.51) |
| **P2-T07** | L2 AI | Stack CF vs P0 / L2det | **DONE** — best **v1b** (BUY∧H14\|16)∨(BUY∧Oct) |

### PHASE 3 — L3 + L4 (`DE40-M5-AOS-P3`) — **DONE / SIGNED** 2026-10-20

| Task | Layer | Deliverable | Status |
| --- | --- | --- | --- |
| **P3-T01** | L3 | MaxDD / kill / Below-frontier halt policy | **DONE** SIGNED · tip 1× BELOW · MaxDD≪25% |
| **P3-T02** | L3 | Cost-drift + FREQUENCY_STALL warn · streak | **DONE** SIGNED |
| **P3-T03** | L4 | Rolling health W15/W20/W50 | **DONE** paths in archive |
| **P3-T04** | L4→L3 | Recommend bus: Below → halt; Compressing → investigate | **DONE** SIGNED |

### PHASE 4 — LEDGER + STACK (`DE40-M5-AOS-P4`) — **DONE / SIGNED** 2026-10-20

| Task | Layer | Deliverable | Status |
| --- | --- | --- | --- |
| **P4-T01** | L6 | Decision ledger schema + offline writer | **DONE** · `aos_l6_ledger_M5.md` |
| **P4-T02** | stack | Det stack `L1+L2det+L3+L4+L6` shadow run | **DONE** tip n_fire=104 E_N=+0.298 |
| **P4-T03** | stack | + L2 AI shadow on det fires | **DONE** DISARM · 27 shadow |
| **P4-T04** | L8 | MAE abort advisor (shadow; **secondary** for cash sleeve) | **DONE** 14/14 loser advises |

### PHASE 5 — RETRAIN LOOP (`DE40-M5-AOS-P5`) — **DONE / PASS** 2026-10-20

| Task | Layer | Deliverable | Status |
| --- | --- | --- | --- |
| **P5-T01** | L5 | Retrain policy + model store `L2skip_de40_m5/` | **DONE** · `aos_l5_retrain_M5.md` · `train_l2_de40_m5.py` |
| **P5-T02** | L5 | Champ/challenger promote rules | **DONE** AI challenger EMPTY · overlay L2det champ |
| **P5-T03** | L5 | Rollback drill | **DONE** `_drill/` pass |

### PHASE 6 — HARDENING (`DE40-M5-AOS-P6`) — **DONE / PASS** 2026-10-20

| Task | Layer | Deliverable | Status |
| --- | --- | --- | --- |
| **P6-T01** | L9 | Session-quality soft veto (Frankfurt open / spread tercile) | **DONE** · no LIVE · see `aos_p6_harden_M5.md` |
| **P6-T02** | G5-ish | ±10% bound stress on L2 thresholds (not SL/TP) | **DONE** · keep v1b · Sep note-only |
| **P6-T03** | — | Confirm ATR max **2380** declared for G3 when OS armed | **DONE** · 2380 on P0+P4 |

### PHASE 7 — PROMOTION (`DE40-M5-AOS-P7`) — **DONE 2026-10-20 HITL**

| Task | Layer | Deliverable | Status |
| --- | --- | --- | --- |
| **P7-T01** | L10 | Promotion packet: CF · health · ledger · gates | **DONE** `promotion_packet.json` |
| **P7-T02** | L10 | HITL sign-off · research OS arm (magic **26151907**) | **SIGNED** · `DE40_5m_stack.set` · `AIOS_SIGNOFF_M5.md` |
| **P7-T03** | — | Paper / tiny-f attach checklist | **DONE** in sign-off |

---

## 7. Weekly implementation table

Calendar assumes **Week 0 = 2026-10-20** (P0 stubs). Slip tasks forward; do not skip measured Leak / tip fill / P1 tape to chase L2 AI. One primary task stream at a time; blotter clear-after-review applies.

| Week | Dates (2026) | Phase | Primary tasks | Exit criteria (done when) |
| ---: | --- | --- | --- | --- |
| **0** | Oct 20 | P0 | P0-T01 · P0-T02 · P0-T03 stub | **DONE** |
| **1** | Oct 20 | P1 | P1-T00…T03 · T05 | **DONE** tip 123 · YTD 208 · bad-cells updated |
| **2** | Oct 20 | P2 | P2-T01…T07 CF | **DONE** v1b ARM · see `aos_l2_policy_M5.md` |
| **3** | buffer | — | Deal export measured Leak (opt) | `Leak_source=measured` preferred before P7 |
| **4** | Oct 20 | P3 | P3-T01…T04 L3/L4 | **DONE** tip 1× BELOW · v1b ends NEAR · see `aos_l3l4_policy_M5.md` |
| **5** | Oct 20 | P4 | P4-T01…T04 ledger/stack | **DONE** det_v1b n=104 E_N+0.298 · `.set` 26151904 |
| **7** | Oct 20 | P5 | P5-T01…T03 retrain/rollback | **DONE** AUC≈0.51 DISARM · drill PASS |
| **8** | Oct 20 | P6 | P6-T01…T03 harden | **DONE** ATR 2380 · L9 no LIVE · v1b keep |
| **9** | Oct 20 | P7 | P7-T01 · P7-T02 HITL | **DONE** `DE40_5m_stack` · magic **26151907** |
| **10** | buffer | P7 | P7-T03 checklist · Tester confirm | Monitor · measured Leak OPEN |

### Weekly operating rhythm

| Day | Action |
| --- | --- |
| Mon | Confirm week’s primary task · load M5 P0 preset · note compare window (**tip May→Oct**) |
| Tue–Thu | Implement / run Tester / build tape or CF |
| Fri | Score under `edge_framework.md` · ACCEPT/REJECT · archive blotter · update this roadmap status |
| Ongoing | No M15/EUR/UK/AUD pin · no SL/TP “quick fix” · no thin-SL under spread · Canvas display-only |

---

## 8. Preset / artifact naming

```text
Profiles/Tester/BMRG/DE40/DE40-M5-AOS-P{phase}-T{task}_{layer}_{change}.set
blotter/archive/DE40-M5-AOS-P{phase}/
infra/artefacts/models/L2skip_de40_m5/LATEST/
doc/assets/DE40/aos_bad_cells_M5.md
doc/assets/DE40/aos_cost_policy_M5.md
doc/assets/DE40/DE40_M5_AOS_BASELINE_v1.md
doc/assets/DE40/aos_l1_tape_contract_M5.md   # from P1
doc/assets/DE40/aos_l2_policy_M5.md          # from P2
Include/AOS_L2det_de_m5.mqh                 # from P2 wire (separate from AOS_L2det_de.mqh)
```

Research OS magic: keep engine **26101903**; OS experiment magics in **2615xxxx** (target arm **26151907**) — never collide with M15 DE40 (`26101902` / `2614xxxx`), EUR, UK, USDJPY, or AUD.

---

## 9. Scorecard fields (every weekly exit)

```text
framework_unified: 1.0
framework_de40: 0.1.0
aos_task: DE40-M5-AOS-P#-T##
preset_id / magic / window / n
aos_overlay: none | L2det | L2AI_shadow | L2AI_withhold | L3 | stack
baseline_ref: DE40_M5_AOS_BASELINE_v1
WR, R, BWR, BM, Leak, Leak_source, EF, M, E_N, PF
skips_n, skip_precision_bad_cell, fire_retention_pct
false_skip_rate_on_Aug_or_MATCH_home
ΔE_N_vs_baseline, ΔEF_vs_baseline, MaxDD
verdict: ACCEPT | REJECT | HOLD_SHADOW
canvas: display_only
```

---

## 10. Document map

| File | Purpose |
| --- | --- |
| **`aios_roadmap_M5.md`** | **This plan** |
| `aios_roadmap.md` | M15 sibling (closed P7) — do not mix |
| `edge_framework.md` | Normative scoring / gates |
| `system_profile_M5.md` | Descriptive behaviour |
| `DE40_M5_AOS_BASELINE_v1.md` | Frozen P0/P1 tip numbers |
| `aos_bad_cells_M5.md` | L2det seed registry (P1-updated) |
| `aos_cost_policy_M5.md` | Leak / deal-export stub |
| `aos_l1_tape_contract_M5.md` | L1 feature schema v0 |
| `tapes/de40_m5_*_fire_tape_v0.csv` | Tip / YTD / prior / tip-core / sep–oct |
| `aos_l2_policy_M5.md` | L2det / L2AI ARM map (P2) |
| `aos_l2_size_table_M5.md` | f multipliers (spec) |
| `Include/AOS_L2det_de_m5.mqh` | M5 L2det v1b wire |
| `aos_l3l4_policy_M5.md` | L3 halt / L4 health bus (P3) |
| `blotter/archive/DE40-M5-AOS-P2/` | P2_CF · REVIEW · run_p2_cf.py |
| `blotter/archive/DE40-M5-AOS-P3/` | P3_L3L4 · health_path_*.csv |
| `aos_l6_ledger_M5.md` | L6 ledger + stack CF (P4) |
| `blotter/archive/DE40-M5-AOS-P4/` | P4_STACK · ledger_*.csv · research `.set` |
| `aos_l5_retrain_M5.md` | L5 retrain · champ/challenger · rollback |
| `infra/artefacts/models/L2skip_de40_m5/` | AI shadow store · rollback CLI |
| `blotter/archive/DE40-M5-AOS-P5/` | metrics · `_drill/` |
| `aos_p6_harden_M5.md` | L9 soft veto · L2 ±10% · ATR G3 |
| `blotter/archive/DE40-M5-AOS-P6/` | P6_HARDEN · run_p6_harden.py |
| `AIOS_SIGNOFF_M5.md` | **HITL** research OS arm · `DE40_5m_stack` · magic **26151907** |
| `blotter/archive/DE40-M5-AOS-P7/` | promotion_packet · `DE40_5m_stack.set` |
| `doc/ai_OS.md` | Layer vocabulary |
| `blotter/archive/DE40-M5-P0/` | Engine extract (pre-OS) |
| `blotter/archive/DE40-M5-AOS-P0/` | P0 review |
| `blotter/archive/DE40-M5-AOS-P1/` | Builder · COST_PROXY · TAPE_QA |
| `infra/artefacts/models/L2skip_de40_m5/` | AI shadow store (from P5) |

---

## 11. Versioning

- **0.1.0** — Initial DE40 M5 AIOS plan; P0 stubs frozen from Jan–Aug blotter (2026-10-20).  
- **0.1.1** — P1 tip May→Oct + YTD tapes · bad-cells updated · OS compare = tip (2026-10-20).  
- **0.1.2** — P2 L2det v1b ARM · L2 AI DISARM · `AOS_L2det_de_m5.mqh` wire (2026-10-20).  
- **0.1.3** — P3 L3/L4 SIGNED · tip BELOW trip retained · v1b end-health lift (2026-10-20).  
- **0.1.4** — P4 ledger + det_v1b stack · research `.set` magic 26151904 (2026-10-20).  
- **0.1.5** — P5 train/store/rollback · AI DISARM · L2det overlay champ (2026-10-20).  
- **0.1.6** — P6 harden · L9 no LIVE · v1b keep · ATR 2380 G3 (2026-10-20).  
- **0.1.7** — P7 HITL · `DE40_5m_stack` · magic 26151907 · stream closed (2026-10-20).  
- Bump when phase order, iteration bar, pin name, or baseline window changes.

---

## 12. One-line plan

**Freeze Balanced P0 M5 (Jan–Aug / May–Aug already EF>0 under Leak prior), fill tip May→Oct, measure Leak, build an M5-native skip/size OS aimed at Feb / May MISMATCH / residual FRAGILE while protecting Jul–Aug MATCH stars, fill side/DOW from tape, shadow until tip EF holds after honest costs, then promote research OS only — never borrow M15 DE40stack or foreign L2, never thin SL under fat spread, never replace live FX/UK/M15 books.**

---

## 13. Status line (update Fridays)

```text
2026-10-20 | P7 HITL SIGNED | ARM_RESEARCH_OS DE40_5m_stack magic 26151907 · L2det_de40_m5_v1b · not FX/M15 replace · stream P0-P7 closed
```
