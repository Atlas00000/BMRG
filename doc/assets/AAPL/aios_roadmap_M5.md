# AAPL M5 — AIOS Roadmap (Balanced TPgtSL)

**Version:** 0.1.7  
**Status:** **P0–P7 complete** — research OS **HITL ARMED** (tip WATCH; not FX/M15 Harvest live replace)  
**Research OS arm:** magic **26162017** · **`AAPL_5m_stack.set`** · [`AIOS_SIGNOFF_M5.md`](./AIOS_SIGNOFF_M5.md)  
**Engine lock (OS baseline):** Balanced M5 · magic **26102011** · **AOS OFF**  
**Preset (engine):** `Profiles/Tester/BMRG/AAPL/BMRG-M5-AAPL-6M-Balanced_TPgtSL.set`  
**Parents:** [`edge_framework.md`](./edge_framework.md) · [`system_profile_M5.md`](./system_profile_M5.md) · [`BUILD_PLAN_M5.md`](./BUILD_PLAN_M5.md) · `doc/ai_OS.md` · `doc/unified_edge_framework.md`  
**Sibling (M15 — do not mix):** [`aios_roadmap.md`](./aios_roadmap.md) · Harvest **26092501** / L2det Thu·18  
**Pool role:** tip **WATCH** · candidate remains M15 Harvest — see [`candidate_pool.md`](./candidate_pool.md)  
**Blotter:** `blotter/inbox/` → `blotter/archive/AAPL-M5-AOS-*/` after review  

**Not** M15 Harvest OS · **not** EURUSD / AUDUSD / DE40 / UK100 L2 pins · **not** reuse of `AOS_L2det_aapl.mqh` Thu/18 map on M5 · **not** a live replace.

---

## 0. Canvas caveat

| Artifact | Authority |
| --- | --- |
| This roadmap + scored blotters under `edge_framework.md` | **Normative** for Apple **M5** AIOS work |
| `system_profile_M5.md` | Evidence / descriptive |
| Canvas / chat charts / UI tiles | **Display only** |

Verdicts come from ledger + scorecard. Tip-only charts never promote a layer. Preset meta Leak **2.1 pp** is never production Leak.

---

## 1. What this is / is not

| This is | This is not |
| --- | --- |
| An **Apple M5-owned AIOS** that permits / withholds / sizes / observes / adapts Balanced TPgtSL | A new SL/TP or BBDev optimisation programme |
| Layered work with task IDs `AAPL-M5-AOS-P#-T##` | A replacement entry model or trend sleeve |
| Iteration vs a frozen M5 Balanced baseline | Immediate live attach or M15 Harvest swap |
| Consumption of M5 profile bad cells (Jan–Apr · Jul WR · Wed · high-spread · overnight/`OTHER`) | Re-ranking from profit / WR alone |
| Separate model store pin (`L2skip_aapl_m5_*` / `L2det_aapl_m5_*`) | Reuse of M15 `L2det_aapl` Thu/18 · EUR / AUD / index pins |
| Regime-first hygiene after **deal-measured Leak** | Treating H1 soft as class failure · thinning SL under fat Apple CFD spread |

**Frozen OS objective:**

```
maximise E_N
subject to  EF hold vs baseline (−1 pp on primary tip health window is enough to keep iterating)
            MaxDD ≤ baseline MaxDD + 2 pp
never maximise WR, PF, or BM alone
never invent entries — only gate the engine fade
```

**Investigation order (unchanged):** data → execution → regime → structure.  
Do **not** touch SL/TP/BBDev/ATR/BBw/Cooldown as the first OS move.  
Do **not** thin SL below **190** (Leak collapses EF under ~27–29 pt med spread).  
Do **not** claim Stage-1 Robust on Leak **proxy** alone — measure first.  
Do **not** arm M15 `L2det_aapl` Thu/18 on M5 without M5 tape CF.

---

## 2. Working hypothesis (from M5 system profile + enhancement thesis)

> Balanced M5 already has a **usable tip Stage-0** meanrev edge (May→Oct WR **46.8%** / E_N **+0.16R** / +$44.50 / BM **+6.3 pp**). Class is fade, not trend.  
> Remaining leak is **conditional + cost**: **Jan–Apr** hostile · **Jul** WR fragile · **Wed** soft on long rolls · **true Leak ~15 pp** (EF_proxy ≈ **−9 pp**) · overnight/`OTHER` path (~16% exits).  
> AI layers’ job: **withhold or size-down regime-hostile / fat-cost fires**, protect **May / Mon / tip BUY**, contain gap-path MaxDD, lift **EF after measured Leak** — without rewriting the fade or borrowing M15 Thu/18.

| Claim | Evidence | Stance for OS |
| --- | --- | --- |
| Tip edge exists (gross) | May→Oct n=77 · WR 46.8% · E_N +0.16R · +$44.50 | **Accept** — freeze as AAPL-M5-AOS-P0 |
| Stage-1 fails under true Leak | Leak ≈ 29/190 ≈ **15.3 pp** · EF_proxy **&lt; 0** | **Accept** — measure first; OS may cut high-spread cells |
| Weakness is conditional | Jan–Apr WR ~25–33% · Jul WR 20% · Wed long soft | **Accept** — L2 skip/size, don’t chase R |
| Protect cells | May WR 67% · Mon tip WR 62% · tip BUY WR 54% | **Accept** — report false-skip on these |
| Overnight fingerprint | ≥12h holds 43/77 · OTHER 15.6% | **Accept** — L8 after L2det |
| Frequency ≫ M15 | ~14 trades / 30d | **Accept** — denser W20; FREQUENCY_STALL bar still applies |
| Longer windows fail Stage-0 | Jan→Oct E_N −0.05R | **Accept** — **L3 regime**, not DROP tip sleeve |
| Fixing via SL/TP first | Would reopen geometry; thin SL kills EF | **Reject as first move** |
| Borrow M15 Thu/18 L2det | Wrong TF / bad-cell fingerprint | **Reject** — M5 pin only |
| Reject asset on Jan→Oct | H1 tax ≈ tip earnings | **Reject** — regime tax, not DROP |
| Trend conversion | Class is meanrev | **Reject** |

---

## 3. Architecture (same layers as `doc/ai_OS.md`)

```
L5 Retrain ──challenger──► L2 Policy (skip/size) ──permit──► M5 ENGINE (26102011)
L1 Tape ──────────────────►        ▲
                                   │
                          L3 Guardrails (hard veto)
                                   ▲
                          L4 Observer (W15/W20 → W50/W100)
                                   │
                          L6 Ledger (all decisions)
L8 MAE/gap abort (primary for equity CFD) · L9 session quality · L10 HITL promote
```

**Invariant:** L3 outranks L1/L2/L4/L5/L8–L10.

### Apple M5 layer emphasis

| Layer | M5 focus |
| --- | --- |
| **L1** | ATR 24–98 · BBw 0.30–2.00% · RTH 14–20 · DOW/hour · side · **spread vs MaxSpread 40** · overnight flag · month · optional earnings |
| **L2det** | Wed SOFT · H1 (Jan–Apr) SOFT/size · Jul stress SOFT · spread≥30 · optional hour-18 · **never** blanket May / Mon / tip BUY |
| **L2 AI** | Avoid-loser on M5 fires only; pin `L2skip_aapl_m5_*` |
| **L3** | MaxDD · Below-frontier f=0 · cost-drift (spread blowouts) · kill-switch · H1 regime tag |
| **L4** | W15/W20 first; denser M5 fire → adopt W50 earlier than M15 Harvest when n allows |
| **L5** | Retrain on decay / Compressing; WF through decay |
| **L6** | Full reason codes for CF scorecards |
| **L8** | **Primary** Apple M5 upside after L2 — fast MAE + gap-open abort advise |
| **L9** | RTH quality / spread tercile soft veto |
| **L10** | Only promotion path to “Apple M5 OS live research” |

---

## 4. Baseline lock (AAPL-M5-AOS-P0)

Import Balanced health from [`system_profile_M5.md`](./system_profile_M5.md) / [`AAPL_M5_AOS_BASELINE_v1.md`](./AAPL_M5_AOS_BASELINE_v1.md). **No OS code required for P0.**

| Field | Tip May→Oct | Jan→Oct | Long 2025.01→2026.10 |
| --- | ---: | ---: | ---: |
| Magic / RR / BWR | **26102011** / ≈1.47 / 40.4% | same | same |
| n | **77** | 145 | 289 |
| WR | **46.8%** | 38.6% | 40.1% |
| BM / E_N | **+6.3 pp** / **+0.16R** | −1.8 / −0.05R | −0.3 / ≈0R |
| Final Δ ($500) | **+$44.50** | −1.97 | +18.95 |
| MaxDD (path) | ~5.0% | ~9.0% | ~10.8% |
| True Leak (proxy) | ~**15.3 pp** | same class | ~14.2 pp (med~27) |
| EF_proxy | **&lt; 0** (~−9 pp) | fail | fail |
| AOS | Off | Off | Off |

**OS compare window (default):** **tip May→Oct** (Tester → 2026.10.19). Jan→Oct / long = regime diagnostic — never sole DROP of tip sleeve.

**Bad-cell registry:** [`aos_bad_cells_M5.md`](./aos_bad_cells_M5.md) (P0-T02).  
**Cost stub:** [`aos_cost_policy_M5.md`](./aos_cost_policy_M5.md) (P0-T03).

---

## 5. Iteration bar (loose on purpose)

**Accept** a layer experiment when **all** hold:

| Check | Bar |
| --- | --- |
| n remaining after skips | Report; no n≥385 floor (per AAPL edge_framework) |
| Tip-window E_N / EF | ≥ baseline − **1 pp** EF (or E_N hold if Leak pending) |
| MaxDD | ≤ baseline + **2 pp** |
| 90d fire count | ≥ 50% of tip baseline rate → else FREQUENCY_STALL **warn** |
| AL | Not worse unless E_N clearly improved |
| Bad-cell hit rate | Skips concentrated in registry cells (report precision/recall vs winners) |
| Protect cells | False-skip rate on **May / Mon / tip BUY** must be reported |

**Reject immediately** when:

- WR↑ but E_N↓ or EF↓  
- Layer invents entries / changes SL/TP/ATR/BBw/session as “OS”  
- Thins SL below 190 or lifts MaxSpread as a Leak “fix”  
- Higher layer overrides L3 halt  
- Uses M15 `L2det_aapl` Thu/18 / EUR / AUD / DE40 / UK pin on M5 Apple  
- Permanently disables a side/DOW before tape exists  
- Claims Robust / production on Leak **proxy** alone  
- Rejects asset solely on Jan→Oct or Jul WR  

**Promote (AAPL-M5-AOS-P7 only)** when: tip May→Oct scored · shadow CF beats/holds baseline · L3/L4 wired · ledger complete · **measured Leak preferred** · HITL sign-off under `edge_framework.md`. Live capital stays off Apple M5 until then. Pool candidate stays M15 Harvest unless HITL re-ranks.

---

## 6. Phase plan (task catalogue)

### PHASE 0 — ENGINE BASELINE LOCK (`AAPL-M5-AOS-P0`) — **STUBS DONE** (measured Leak OPEN)

| Task | Layer | Deliverable | Status |
| --- | --- | --- | --- |
| **P0-T01** | — | Freeze `AAPL_M5_AOS_BASELINE_v1` (tip + Jan–Oct + long) | **DONE** 2026-10-20 |
| **P0-T02** | — | Bad-cell registry from M5 profile | **DONE** 2026-10-20 |
| **P0-T03** | — | Cost policy + Leak proxy stub; deal-measured still open | **DONE** stub 2026-10-20 · measured **OPEN** |

### PHASE 1 — L1 PERCEPTION (`AAPL-M5-AOS-P1`) — **DONE** 2026-10-20 (T04 deferred)

| Task | Layer | Deliverable | Status |
| --- | --- | --- | --- |
| **P1-T01** | L1 | Apple M5 feature schema v0 (`aos_l1_tape_contract_M5.md`) | **DONE** |
| **P1-T02** | L1 | Offline tape builder from Tester M5 fires / bars | **DONE** `build_aapl_m5_fire_tape.py` |
| **P1-T03** | L1 | Label fires: win/lose · DOW · hour · side · ATR · BBw · overnight · spread · month | **DONE** tip 77 · YTD 145 · long 289 |
| **P1-T04** | L1 | Structure flags v0 (band-ride / failed fade) — optional | **DEFERRED** |
| **P1-T05** | L1 | Earnings / H1-regime month flags (soft) | **DONE** `regime_tag` on tape |

### PHASE 2 — L2 POLICY (`AAPL-M5-AOS-P2`) — **DONE** 2026-10-20

| Task | Layer | Deliverable | Status |
| --- | --- | --- | --- |
| **P2-T01** | L2det | Parity: skip Tue + ATR/BBw gates — OS mirror / no double-count | **DONE** PASS |
| **P2-T02** | L2det | SOFT map v1: Wed ± high-spread / H18 (shadow CF) | **DONE** — Wed ARM · H18/spread HOLD |
| **P2-T03** | L2det | H1 / Jul stress SOFT CF (never blanket May/Mon) | **DONE** — **ARM Jul∨Wed v1b** · H1 HOLD |
| **P2-T04** | L2size | Lifecycle → f table (spec; wire after L4) | **DONE** SPEC (`aos_l2_size_table_M5.md`) |
| **P2-T05** | L2 AI | Train `L2skip_aapl_m5` avoid-loser · **shadow only** | **DONE** — **DISARM** (AUC≈0.50) |
| **P2-T06** | L2 AI | Shadow CF scorecard vs P0 + vs L2det-only | **DONE** — best **v1b Jul∨Wed** |
| **P2-T07** | wire | `Include/AOS_L2det_aapl_m5.mqh` + M5 presets | **DONE** · magics 26162011/12 |

### PHASE 3 — L3 + L4 (`AAPL-M5-AOS-P3`) — **DONE / SIGNED** 2026-10-20

| Task | Layer | Deliverable | Status |
| --- | --- | --- | --- |
| **P3-T01** | L3 | MaxDD / kill / Below-frontier halt policy (Apple M5 DD_limit) | **DONE** SIGNED · tip 1× BELOW · MaxDD≪25% |
| **P3-T02** | L3 | Cost-drift + FREQUENCY_STALL warn | **DONE** SIGNED |
| **P3-T03** | L4 | Rolling health W15/W20/W50 | **DONE** paths in archive |
| **P3-T04** | L4→L3 | Recommend bus: Below → halt; Compressing → investigate | **DONE** SIGNED |

### PHASE 4 — LEDGER + STACK (`AAPL-M5-AOS-P4`) — **DONE / SIGNED** 2026-10-20

| Task | Layer | Deliverable | Status |
| --- | --- | --- | --- |
| **P4-T01** | L6 | Decision ledger schema + offline writer | **DONE** · `aos_l6_ledger_M5.md` |
| **P4-T02** | stack | Det stack `L1+L2det+L3+L4+L6` shadow run | **DONE** tip n_fire=41 E_N=+0.327 |
| **P4-T03** | stack | + L2 AI shadow on det fires | **DONE** DISARM · 19 shadow |
| **P4-T04** | L8 | MAE/gap abort advisor (shadow) | **DONE** 21/21 loser advises |

### PHASE 5 — RETRAIN LOOP (`AAPL-M5-AOS-P5`)

| Task | Layer | Deliverable | Status |
| --- | --- | --- | --- |
| **P5-T01** | L5 | Retrain policy + model store `L2skip_aapl_m5/` | **DONE** — AUC≈0.501 · DISARM · `aos_l5_retrain_M5.md` |
| **P5-T02** | L5 | Champ/challenger promote rules | **DONE** — documented; challenger EMPTY |
| **P5-T03** | L5 | Rollback drill | **DONE** — PASS |

### PHASE 6 — HARDENING (`AAPL-M5-AOS-P6`) — **DONE / PASS** 2026-10-20

| Task | Layer | Deliverable | Status |
| --- | --- | --- | --- |
| **P6-T01** | L9 | Session-quality soft veto (RTH / spread tercile) | **DONE** · no LIVE · see `aos_p6_harden_M5.md` |
| **P6-T02** | G5-ish | ±10% bound stress on L2 thresholds (not SL/TP) | **DONE** · keep v1b Jul∨Wed |
| **P6-T03** | — | Confirm ATR 24–98 / BBw 0.30–2.00 declared for G3 when OS armed | **DONE** · PASS |

### PHASE 7 — PROMOTION (`AAPL-M5-AOS-P7`) — **DONE 2026-10-20 HITL**

| Task | Layer | Deliverable | Status |
| --- | --- | --- | --- |
| **P7-T01** | L10 | Promotion packet: CF · health · ledger · edge_framework gates | **DONE** `promotion_packet.json` |
| **P7-T02** | L10 | HITL sign-off · research OS arm (still not M15/FX replace) | **SIGNED** · `AAPL_5m_stack.set` · magic **26162017** |
| **P7-T03** | — | Optional paper / tiny-f attach checklist | **DONE** in `AIOS_SIGNOFF_M5.md` |

---

## 7. Weekly implementation table

Calendar assumes **Week 0 = 2026-10-20** (P0 stubs). Slip tasks forward; do **not** skip measured Leak / P1 tape to chase L2 AI. One primary task stream at a time; blotter clear-after-review applies.

| Week | Dates (2026) | Phase | Primary tasks | Exit criteria (done when) |
| ---: | --- | --- | --- | --- |
| **0** | Oct 20 | P0 | P0-T01 · P0-T02 · P0-T03 stub | **DONE** |
| **1** | Oct 20 | P1 | P1-T01…T03 · T05 (T04 defer) | **DONE** tip 77 · YTD 145 · long 289 · HOUR_18 seeded |
| **2** | buffer | P0 | Deal-export Leak (opt) | `Leak_source=measured` preferred before P7 |
| **3** | Oct 20 | P2 | P2-T01…T07 CF + wire | **DONE** v1b Jul∨Wed ARM · AI DISARM |
| **4** | Oct 20 | P3 | P3-T01…T04 L3/L4 | **DONE** tip 1× BELOW · v1b DD 2.6% · see `aos_l3l4_policy_M5.md` |
| **5** | Oct 20 | P4 | P4-T01…T04 ledger/stack · L8 | **DONE** det_v1b n=41 E_N+0.327 · `.set` 26162014 |
| **6** | Oct 20 | P5 | P5-T01…T03 | **DONE** store + drill · AUC DISARM |
| **7** | Oct 20 | P6 | P6-T01…T03 | **DONE** L9 no LIVE · v1b keep · ATR/BBw G3 |
| **8** | Oct 20 | P7 | P7-T01 · P7-T02 HITL | **DONE** `AAPL_5m_stack` · magic **26162017** |
| **9** | buffer | P7 | P7-T03 checklist · Tester confirm | Monitor · measured Leak OPEN |

### Weekly operating rhythm

| Day | Action |
| --- | --- |
| Mon | Confirm week’s primary task · load M5 Balanced preset · note compare window (**tip May→Oct**) |
| Tue–Thu | Implement / run Tester / build tape or CF |
| Fri | Score under `edge_framework.md` · ACCEPT/REJECT · archive blotter · update this roadmap status |
| Ongoing | No M15 Thu/18 / EUR / AUD pin · no SL/TP “quick fix” · no thin-SL under spread · Canvas display-only |

---

## 8. Preset / artifact naming

```text
Profiles/Tester/BMRG/AAPL/AAPL-M5-AOS-P{phase}-T{task}_{layer}_{change}.set
blotter/archive/AAPL-M5-AOS-P{phase}/
  or AAPL-M5-AOS-P{phase}-T{task}/
infra/artefacts/models/L2skip_aapl_m5/LATEST/
doc/assets/AAPL/aos_bad_cells_M5.md
doc/assets/AAPL/aos_cost_policy_M5.md
doc/assets/AAPL/AAPL_M5_AOS_BASELINE_v1.md
doc/assets/AAPL/aos_l1_tape_contract_M5.md   # from P1
doc/assets/AAPL/aos_l2_policy_M5.md          # from P2
Include/AOS_L2det_aapl_m5.mqh               # from P2 — separate from AOS_L2det_aapl.mqh
```

Research OS magic: keep engine **26102011**; **HITL arm magic 26162017** (`AAPL_5m_stack`) — never collide with M15 Harvest (`26092501` / `261012xx`), EUR, AUD, DE40, or UK.

---

## 9. Scorecard fields (every weekly exit)

```text
framework_aapl: 0.1.1
roadmap: aios_roadmap_M5 0.1.0
aos_task: AAPL-M5-AOS-P#-T##
tf: M5
preset_id / magic / window / n
aos_overlay: none | L2det | L2AI_shadow | L2AI_withhold | L3 | stack | L8
baseline_ref: AAPL_M5_AOS_BASELINE_v1
WR, R, BWR, BM, Leak, Leak_source, EF, M, E_N, PF
skips_n, skip_precision_bad_cell, fire_retention_pct
false_skip_May, false_skip_Mon, false_skip_BUY_tip
ΔE_N_vs_baseline, ΔEF_vs_baseline, MaxDD
verdict: ACCEPT | REJECT | HOLD_SHADOW
canvas: display_only
m15_pin_used: false   # must stay false
```

---

## 10. Document map

| File | Purpose |
| --- | --- |
| **`aios_roadmap_M5.md`** | **This plan** |
| `BUILD_PLAN_M5.md` | Compile / Tester slice for M5 OS |
| `edge_framework.md` | Normative scoring / gates (shared asset) |
| `system_profile_M5.md` | Descriptive M5 behaviour |
| `AAPL_M5_AOS_BASELINE_v1.md` | Frozen P0 numbers |
| `aos_bad_cells_M5.md` | L2det seed registry (M5 cells) |
| `aos_cost_policy_M5.md` | Leak · journal proxy ~15.3 pp |
| `aos_l1_tape_contract_M5.md` | L1 schema v0 (P1) |
| `aos_l2_policy_M5.md` | L2det / L2AI ARM map (P2) |
| `aos_l2_size_table_M5.md` | f multipliers (spec) |
| `aos_l3l4_policy_M5.md` | L3 halt / L4 health bus (P3) |
| `aos_l6_ledger_M5.md` | L6 ledger · stack CF · research `.set` (P4) |
| `aos_l5_retrain_M5.md` | L5 store · champ/challenger · rollback (P5) |
| `aos_p6_harden_M5.md` | L9 · L2 stress · ATR/BBw G3 (P6) |
| `AIOS_SIGNOFF_M5.md` | **HITL** research OS arm · `AAPL_5m_stack` · magic **26162017** |
| `Include/AOS_L2det_aapl_m5.mqh` | M5 L2det v1b wire |
| `infra/artefacts/models/L2skip_aapl_m5/` | L2 AI shadow store (P5) |
| `blotter/archive/AAPL-M5-AOS-P3/` | P3_L3L4 · health_path_*.csv |
| `blotter/archive/AAPL-M5-AOS-P4/` | P4_STACK · ledger_*.csv · research `.set` |
| `blotter/archive/AAPL-M5-AOS-P5/` | metrics · REVIEW · `_drill/` |
| `blotter/archive/AAPL-M5-AOS-P6/` | P6_HARDEN · SUMMARY · REVIEW |
| `blotter/archive/AAPL-M5-AOS-P7/` | promotion_packet · `AAPL_5m_stack.set` |
| `tapes/aapl_m5_*_v0.csv` | Tip / YTD / prior / long |
| `blotter/archive/AAPL-M5-AOS-P2/` | P2_CF · REVIEW · run_p2_cf.py |
| `aios_roadmap.md` | **M15** sibling — do not merge scorecards |
| `BUILD_PLAN.md` | M15 Harvest compile slice |
| `candidate_pool.md` | Pool lock (Harvest KEEP · M5 WATCH) |
| `doc/ai_OS.md` | Layer vocabulary |

---

## 11. Versioning

- **0.1.0** — Initial Apple M5 AIOS plan from system-profile enhancement thesis; P0-T01…T03 stubs; weekly calendar from 2026-10-20.  
- **0.1.1** — P1 tapes + schema + COST_PROXY · bad-cells P1-updated (HOUR_18 optional) · T04 deferred (2026-10-20).  
- **0.1.2** — P2 L2det v1b Jul∨Wed ARM · L2AI DISARM · `AOS_L2det_aapl_m5.mqh` wire (2026-10-20).  
- **0.1.3** — P3 L3/L4 SIGNED · tip BELOW trip · v1b MaxDD cut · Jul-only 0 trips (2026-10-20).  
- **0.1.4** — P4 ledger + det_v1b stack · research `.set` magic 26162014 · L8 21/21 (2026-10-20).  
- **0.1.5** — P5 L2skip store + train AUC≈0.501 DISARM · rollback drill PASS · `aos_l5_retrain_M5.md` (2026-10-20).  
- **0.1.6** — P6 harden · L9 no LIVE · v1b Jul∨Wed keep · ATR/BBw G3 PASS · `aos_p6_harden_M5.md` (2026-10-20).  
- **0.1.7** — P7 HITL · `AAPL_5m_stack` · magic 26162017 · stream closed (2026-10-20).  
- Bump when phase order, iteration bar, pin name, or baseline window changes.

---

## 12. One-line plan

**Freeze Balanced M5 (tip Stage-0 gross OK · true Leak blocks Stage-1), measure Leak, build an M5-native skip/size OS aimed at Wed / H1 / Jul / fat-spread cells while protecting May / Mon / tip BUY, elevate L8 for overnight gaps, shadow until tip EF holds after honest costs, then promote research OS only — never borrow M15 Thu/18 or FX L2, never retune geometry as the first move, never replace the M15 Harvest candidate without HITL.**

---

## 13. Status line (update Fridays)

```text
2026-10-20 | P7 HITL SIGNED | ARM_RESEARCH_OS AAPL_5m_stack magic 26162017 · L2det_aapl_m5_v1b · not FX/M15 Harvest replace · stream P0-P7 closed
```
