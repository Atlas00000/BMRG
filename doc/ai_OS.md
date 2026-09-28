# BMRG AI Operating System

**Version:** 0.2  
**Status:** **EA-wired (BMRG v1.20)** · offline P0–P7 complete · **STAY_PAPER** (no `AOS_LIVE`)  
**Governs:** All `AOS-*` tasks below  
**Engine (frozen):** Harvest champion — `EDX-P2-T04_SL300_TP300_RR1_champFilters_G0_long.set` (magic **8210204**)  
**AI stack preset:** `Profiles/Tester/BMRG/aistack.set` (magic **8399001**)  
**Evidence:** `system_profile.md` · `doc/edge_discovery.md` · `doc/edge_framework.md` · `doc/candidate_pool.md` · `blotter/archive/AOS-aistack-run/`  
**Normative scoring:** Framework **stages** 0–4 (`doc/unified_edge_framework.md` / `doc/edge_framework.md`)  
**This document:** AI OS **layers** L1–L10 (software around the engine)

---

## 0. What this is / is not

| This is | This is not |
| --- | --- |
| An **AI OS** that permits / withholds / sizes / observes / adapts the existing EA | A new EDX campaign or SL/TP re-optimisation programme |
| Layered software with task IDs `AOS-P#-T##` | A replacement entry model |
| Iteration with a **loose** bar vs AOS-P0 baseline | Production sign-off on every experiment |
| Consumption of EDX bad cells (Tue, thin LON AM, WR-side, …) | Re-ranking cells from profit alone |

**Frozen OS objective:**

```
maximise E_N
subject to  EF > 0  (hold vs baseline −1pp on W250 is enough to keep iterating)
            MaxDD acceptable (≤ baseline + 2pp on W250)
never maximise WR, PF, or BM alone
```

WR / PF / “AI confidence” are **diagnostics**, not objectives.

**Investigation order (unchanged):** data → execution → regime → structure.  
Do not touch SL/TP/BBDev as the first OS move.

---

## 1. Working hypothesis (from profile + EDX)

> The engine already has a real edge (Harvest KEEP both windows; Growth G0–G4).  
> Remaining leak is **conditional**: it still fires in regimes / structures where `BM_cell ≤ 0` (or barely >0 with high AL contribution).  
> AI layers’ job: **withhold those fires**, contain AL / MaxDD, keep **EF** alive as price evolves — without rewriting the fade.

| Claim | Evidence | Stance for OS |
| --- | --- | --- |
| Edge exists | Harvest long EF 1.77 n=530; 3M EF 6.43; Growth long EF 5.18 G0–G4 | **Accept** — baseline locked in AOS-P0 |
| Weakness is WR-side | R≈RR; more SL than TP; P25 buy-only EF≤0 | **Accept** — skip/size, don’t chase R |
| Bad calendar cells | Tuesday BM≤0; LON 08–12 thin; edge in LON–NY / NY | **Accept** — L2 skip map seeds |
| Bad path cells | Intraday round-trips BM≤0; overnight holds edge | **Accept** — L8 early-abort / hold advisor |
| Band-ride = loser | Continuation into SL −1R | **Accept** — L1 structure + L2 withhold |
| Fixing AL via SL/TP first | G5 TP−10 killed Growth EF | **Reject as first move** — regime gate first |

**Confirmed for OS design:** conditional leak hypothesis stands. OS does not reopen EDX as the main workstream.

---

## 2. Two vocabularies (do not mix)

| Vocabulary | Meaning | Examples |
| --- | --- | --- |
| **Framework stages** | How we **score** the EA / OS candidate | Stage 0 identities · Stage 1 EF/M · Stage 2 W100/250/500 · Stage 3 capital · Stage 4 G0–G5 |
| **AI OS layers** | Software we **build** around the engine | L1 Perception · L2 Policy · L3 Guardrails · L4 Observer · L5 Retrain · L6 Ledger · L7+ |

Promotion to live uses **stages**. Day-to-day experiments use **layers** + the loose iteration bar (§4).

---

## 3. Architecture — stacked layers (L1–L10)

```
                    ┌─────────────────────────────────────┐
                    │  L5 Adaptation / Retrain (versioned) │
                    └──────────────┬──────────────────────┘
                                   │ challenger models
┌──────────┐  tape   ┌─────────────▼─────────────┐  permit   ┌──────────────┐
│ L1 Perc. │────────►│ L2 Intelligence / Policy  │──────────►│ BMRG ENGINE  │
│ regime + │         │ skip / enter / size       │  signal   │ Harvest G0   │
│ structure│         └─────────────▲─────────────┘  only if  └──────┬───────┘
└────┬─────┘                       │                L2∧L3 OK        │
     │                             │                                │
     │         ┌───────────────────┴───────────────────┐            │
     │         │ L3 GUARDRAILS (hard · non-AI · veto)  │◄───────────┤
     │         │ MaxDD · stall · cost · frontier · kill│   halt f   │
     │         └───────────────────▲───────────────────┘            │
     │                             │ recommend                      │
     │         ┌───────────────────┴───────────────────┐            │
     └────────►│ L4 Edge-Health Observer (W100/250/500)│◄───────────┘
               │ EF · ΔD · Leak · RR−R · lifecycle     │  blotter
               └───────────────────▲───────────────────┘
                                   │
               ┌───────────────────┴───────────────────┐
               │ L6 Memory / Ledger (audit all decisions)│
               └───────────────────────────────────────┘
L7 basket/corr · L8 MAE/MFE abort · L9 session quality · L10 HITL promotion
```

**Invariant:** L3 outranks L1/L2/L4/L5/L7–L10. Higher layers may advise; they never override a Guardrail halt.

### L1 — Perception

Live **regime / structure tape** every other layer consumes. No trade decisions here.

| Family | Tags (rich vocabulary) |
| --- | --- |
| Vol | ATR tercile · BB-width tercile · realised-vol spike · compression→expansion |
| Trend vs range | ER tercile · HH/HL vs LH/LL · range box · breakout · failed auction · band-ride |
| Session micro | Asia / LON AM / LON–NY / NY / post-NY · overlap quality · thin-liquidity flag |
| Calendar | DoW · month-of-year · week-of-month · holiday / roll windows |
| Event | High-impact news window · NFP/FOMC blackout · surprise vs quiet |
| Microstructure | Spread tercile · quote-flicker · gap-open · swap-night risk |
| Engine-local | Side (buy/sell) · BBDev distance · bars-since-last-entry · open inventory |

**Output schema (conceptual):** `TapeTick { t, symbol, regime_id, structure_id, session_id, event_flags[], features{} }`

### L2 — Intelligence / Policy

Only **permit or withhold** the engine’s existing fade signal. Optional **size modulator** after skip-gate exists.

| Mode | Behaviour |
| --- | --- |
| Deterministic skip map | Seed from EDX: Tue · (optional) LON 08–12 · other `BM_cell≤0` cells with n≥30 |
| AI classifier | P(lose \| tape, signal) → skip if above threshold; never invent entry |
| Size modulator | Map Stage-2 lifecycle → f multiplier: Expanding 1.0 · Stable 0.75 · Compressing 0.5 · Near frontier 0.25 · Below frontier **0** (L3 also forces 0) |

**Hypothesis:** skip `BM_cell ≤ 0`; do **not** skip merely “weaker” cells if cell EF > 0.

### L3 — Guardrails (hard · non-AI)

| Guard | Action |
| --- | --- |
| MaxDD ≥ 0.8 × DD_limit | De-risk f (halve) |
| MaxDD ≥ DD_limit | Halt new entries |
| FREQUENCY_STALL (90d fires &lt; 50% baseline) | Warn → if persistent, widen L2 only via AOS task |
| Cost-drift (Leak↑ beyond band) | Halt / flag |
| Below-frontier (E_N≤0 on W250) | f = 0 |
| Kill-switch | Flat + disable |

### L4 — Edge-health observer

Rolling **W100** (fast) / **W250** (decision) / **W500** (confirm): WR, R, BWR, BM, Leak, EF, M, E_N, ΔD, RR−R, MaxDD, fire count.  
Lifecycle label → recommend to L2/L5; **L3 commands**.

### L5 — Adaptation / retrain

Scheduled (e.g. monthly) + trigger (Compressing / Near frontier).  
Walk-forward: fit through decay, **never only on the decay window**.  
Champion / challenger; versioned artifacts; no silent overwrite of live L2.

### L6 — Memory / ledger

Every skip, fire, size-change, retrain, guardrail trip: `{t, layer, decision, features, reason_code, model_version}`.  
Human can answer: “why did it skip?”

### L7 — Correlation / basket / sleeve throttle

Multi-sleeve awareness (Harvest + Growth + Survival). Cap concurrent correlated risk; prefer champion weight; cut Survival when 3M costs_fragile.

### L8 — MAE/MFE early-abort advisor

Advisory only (L3 can promote to hard rule later): if MAE path matches known loser shape (fast adverse), recommend flatten / block add — **does not change entry model**. Aligns with EDX intraday-loss pocket.

### L9 — Session-quality / multi-horizon ensemble

Scores overlap quality + longer-horizon regime vote (M5 tape × H1/H4 context). Soft veto into L2; never bypasses L3.

### L10 — Human-in-the-loop promotion desk

Only path from “experiment OS” → “live OS”: review ledger + Stage-1 zone + light Stage-4. Blocks silent auto-promote.

---

## 4. Iteration bar (loose on purpose)

**Accept** a layer experiment when **all** hold:

| Check | Bar |
| --- | --- |
| Remaining n | ≥ 100 (Provisional+). Warn if n &lt; 385; do not kill |
| W250 EF | ≥ baseline EF − **1 pp** (hold = pass) |
| W250 MaxDD | ≤ baseline MaxDD + **2 pp** |
| 90d fire count | ≥ 50% baseline (FREQUENCY_STALL = **warn**, report, not instant fail) |
| AL | Not worse unless E_N clearly improved |

**Reject immediately** when:

- WR↑ but E_N↓ or EF↓ (payoff trap)  
- Layers rewrite entries (new signal ≠ engine fade)  
- Higher layer overrides an L3 halt  

**Promote to live** (AOS-P7 only) when Stage 1 is at least Fragile-or-better, EF Stable/Expanding on W250, MaxDD inside mandate; **Robust (EF > M)** is the promotion target. Full G0–G5 for promote — **not** for every layer trial. Experiment n≠1068 blocker.

---

## 5. AOS-P0 baseline (engine lock)

Import Harvest health vector — the number the OS must beat or hold. **No OS code.**

| Field | Long (Harvest P2-T04) | 3M |
| --- | --- | --- |
| Preset / magic | `EDX-P2-T04_…` / **8210204** | same |
| n | 530 | 49 |
| WR / BWR / R | 54.5% / 50% / 1.0 | 59.2% / 50% / 1.0 |
| E_N | 0.091 | 0.184 |
| EF (Leak ~2.2) | **1.77** | **6.43** |
| Zone | Fragile (long) | Strong / thin n |
| Final $ | ~533 | ~425 |
| Champ filters | 12–20 · skip Tue · BBDev 2.2 · G0 | — |

Secondary ref (optional Δ): Growth P4-T01 EF 5.18 long (not the OS default engine).

### AOS-P0-T01 — Freeze baseline scorecard


| | |
| --- | --- |
| **Layer** | — (meta) |
| **What changes** | None — archive AOS baseline from EDX Harvest long + 3M |
| **Health fields** | Full vector locked as `AOS_BASELINE` |
| **Skip/fire** | Engine-only (100% of engine fires) |
| **Test preset** | `AOS-P0-T01_L0_baselineLock_Harvest_long.set` (= copy pointer to P2-T04; magic **8310001** bookkeeping only if re-run) |
| **Accept** | Baseline numbers written to `doc/ai_OS_baseline.md` or archive folder; board points here |
| **Status** | `DONE` — **ACCEPT** · `AOS_BASELINE_v1` locked · `doc/ai_OS_baseline.md` · `archive/AOS-P0-T01/` |


### AOS-P0-T02 — Bad-cell registry (consume EDX, don’t rediscover)


| | |
| --- | --- |
| **Layer** | Feeds L2 |
| **What changes** | Document skip seeds: Tue · LON 08–12 (optional soft) · intraday-loss note · buy-weak asymmetry |
| **Health fields** | None yet — registry only |
| **Expected** | L2 deterministic map v0 |
| **Test preset** | n/a (markdown artifact `doc/aos_bad_cells.md`) |
| **Accept** | Each cell cites EDX archive ID + BM_cell / n |
| **Status** | `DONE` — **ACCEPT** · `doc/aos_bad_cells.md` · `archive/AOS-P0-T02/` |


---

## 6. Task template

Every `AOS-P#-T##` states:

| Field | Content |
| --- | --- |
| **Layer** | L1…L10 |
| **What changes** | Inputs / model / rule (engine SL/TP frozen unless task says otherwise) |
| **Health-vector fields** | Which of WR,R,BM,Leak,EF,E_N,ΔD,MaxDD,n,fires must move / hold |
| **Skip/fire expected** | Directional rate vs AOS-P0 |
| **Test preset** | `AOS-P{phase}-T{task}_{layer}_{change}_{context}.set` |
| **Accept / reject** | Loose bar (§4) |
| **Status** | `PENDING` / `RUNNING` / `DONE` / `REJECTED` |

**Active rule:** execute only the first `PENDING` task in order. One at a time.

**Preset location:** `MQL5/Profiles/Tester/BMRG/`  
**Changed inputs only** in the preset header comment; hypothesis; expected skip rate; fields that must not regress vs AOS-P0.

---

## 7. PHASES

### PHASE 0 — ENGINE BASELINE LOCK (`AOS-P0`)

Tasks: **T01–T02** above. No layer code.

---

### PHASE 1 — L1 PERCEPTION (`AOS-P1`)

Define feature schema, labels, live bar tagging → tape for L2.

#### AOS-P1-T01 — Feature schema v0


| | |
| --- | --- |
| **Layer** | L1 |
| **What changes** | Spec only: feature list + dtypes + refresh cadence (closed M5 bar) |
| **Health fields** | None (contract) |
| **Skip/fire** | n/a |
| **Test preset** | `AOS-P1-T01_L1_featureSchema_v0_doc.set` (engine-identical; validates logging hooks later) |
| **Accept** | Schema merged; covers vol/trend/session/event/micro/engine-local |
| **Status** | `DONE` — **ACCEPT** · `doc/aos_l1_feature_schema.md` · `doc/aos_l1_tape_contract.md` · `archive/AOS-P1-T01/` |


#### AOS-P1-T02 — Offline tape builder (label historical bars)


| | |
| --- | --- |
| **Layer** | L1 |
| **What changes** | Tooling: tag Harvest blotter bars with regime/structure IDs |
| **Health fields** | Enables cell BM recompute (diagnostic) |
| **Skip/fire** | n/a |
| **Test preset** | `AOS-P1-T02_L1_offlineTape_Harvest_long.set` |
| **Accept** | ≥95% of engine entries have a tape row; Tue / session tags match EDX |
| **Status** | `DONE` — **ACCEPT** · 531/531 tagged · tue=0 · 100% LON_NY+NY · `archive/AOS-P1-T02/` |


#### AOS-P1-T03 — Live tape publisher (EA or sidecar)


| | |
| --- | --- |
| **Layer** | L1 |
| **What changes** | Runtime: emit TapeTick each new bar (file/IPC/MT5 global) |
| **Health fields** | Latency diagnostic only |
| **Skip/fire** | Engine fire rate unchanged (perception-only) |
| **Test preset** | `AOS-P1-T03_L1_liveTape_EURUSD_M5.set` |
| **Accept** | Tape continuity; no change in n/WR vs baseline beyond noise |
| **Status** | `DEFERRED` — **paused until OS offline stack done** (user 2026-09-25); do not block P2–P6 offline |


#### AOS-P1-T04 — Structure decoder (HH/HL · failed auction · band-ride)


| | |
| --- | --- |
| **Layer** | L1 |
| **What changes** | Structure_id vocabulary + rules/model |
| **Health fields** | Prepares L2; optional diagnostic BM by structure |
| **Skip/fire** | None yet |
| **Test preset** | `AOS-P1-T04_L1_structureDecoder_v0_long.set` |
| **Accept** | Band-ride / range / trend labels stable; ledger can show tag on each fire |
| **Status** | `DONE` — **ACCEPT** vocab + v0 stubs; runtime still `UNK` until swing code |


#### AOS-P1-T05 — Event / news window flags


| | |
| --- | --- |
| **Layer** | L1 |
| **What changes** | Calendar blackout features (even if initially manual CSV) |
| **Health fields** | Diagnostic BM in event vs quiet |
| **Test preset** | `AOS-P1-T05_L1_eventWindows_v0_long.set` |
| **Accept** | Flags present; no silent skip until L2 task owns it |
| **Status** | `DONE` — **ACCEPT** vocab locked; calendar empty (`in_blackout=false`) |


---

### PHASE 2 — L2 POLICY GATES (`AOS-P2`)

Deterministic skips first (EDX seeds), then AI classifiers, then size.

#### AOS-P2-T01 — Deterministic skip: Tuesday (already in engine — verify OS mirror)


| | |
| --- | --- |
| **Layer** | L2 |
| **What changes** | OS-level Tue skip assert (parity with InpTradeTue=false) |
| **Health fields** | Hold EF; fires = baseline |
| **Skip/fire** | 0 Tue fires (confirm) |
| **Test preset** | `AOS-P2-T01_L2gate_skipTue_parity_Harvest.set` |
| **Accept** | Parity with champion; no regression |
| **Status** | `DONE` — **ACCEPT** · offline tue opens=0 · parity with TradeTue=false · `archive/AOS-P2-T01/` |


#### AOS-P2-T02 — Deterministic soft-skip: LON 08–12 (opt-in)


| | |
| --- | --- |
| **Layer** | L2 |
| **What changes** | Optional gate: block engine signals in 08–12 even if EA session widened |
| **Health fields** | EF hold/−1pp; MaxDD; fire count warn if &lt;50% |
| **Skip/fire** | Expect −15–40% fires if session expanded; on champ 12–20 ≈ no-op |
| **Test preset** | `AOS-P2-T02_L2gate_skipLonAM_soft_Harvest.set` |
| **Accept** | Loose bar; report FREQUENCY_STALL warning if any |
| **Status** | `DONE` — **ACCEPT (no-op)** · LON_AM opens=0 on champ · armed only if session widened · `archive/AOS-P2-T02/` |


#### AOS-P2-T03 — Deterministic skip map v1 (all EDX BM_cell≤0 with n≥30)


| | |
| --- | --- |
| **Layer** | L2 |
| **What changes** | Unified skip table from `aos_bad_cells.md` |
| **Health fields** | EF, E_N, AL, MaxDD, n |
| **Skip/fire** | Skip only ≤0 BM cells; do not skip weak-but-positive EF cells |
| **Test preset** | `AOS-P2-T03_L2gate_skipMap_v1_Harvest_long.set` |
| **Accept** | Loose bar; ledger reason_codes populated |
| **Status** | `DONE` — **ACCEPT** · HARD=`DOW_TUE` only · `doc/aos_l2_policy_v0.md` · labeled csv · `archive/AOS-P2-T03/` |


#### AOS-P2-T04 — AI skip classifier v0 (logistic / GBDT on tape)


| | |
| --- | --- |
| **Layer** | L2 |
| **What changes** | Model P(lose); threshold → skip |
| **Health fields** | AL↓ target; EF hold; E_N; fire≥50% warn |
| **Skip/fire** | Target skip 10–30% of would-be losers; not &gt;50% of all fires without review |
| **Test preset** | `AOS-P2-T04_L2gate_aiSkip_v0_Harvest_long.set` |
| **Accept** | Loose bar; reject if WR↑ EF↓ |
| **Status** | `DEFERRED` → **AOS-P4** (labels ready; no live AI gate; skip-Mon trial rejected) · `archive/AOS-P2-T04/` |


#### AOS-P2-T05 — Size modulator v0 (lifecycle → f)


| | |
| --- | --- |
| **Layer** | L2 |
| **What changes** | f multipliers from L4 lifecycle (after T03 or T04 exists) |
| **Health fields** | MaxDD↓ preferred; EF hold; E_N |
| **Skip/fire** | Fire count ≈ unchanged; size changes |
| **Test preset** | `AOS-P2-T05_L2size_lifecycle_v0_Harvest_long.set` |
| **Accept** | Loose bar; Below-frontier → f=0 respects L3 |
| **Status** | `DONE` — **ACCEPT SPEC** · table in `aos_l2_policy_v0.md` · wire after L4 · `archive/AOS-P2-T05/` |


#### AOS-P2-T06 — Side asymmetry soft-gate (buy caution)


| | |
| --- | --- |
| **Layer** | L2 |
| **What changes** | Optional higher skip threshold on buys (P25 buy-only Leak fail on Growth) |
| **Health fields** | EF, BM by side, fire mix |
| **Skip/fire** | Mild buy skip ↑; never sell-only rewrite |
| **Test preset** | `AOS-P2-T06_L2gate_buyCaution_Harvest_long.set` |
| **Accept** | Loose bar; reject if becomes sell-only strategy |
| **Status** | `DONE` — **DISARMED on Harvest** · Buy EF≥Sell · skip-all-buys stalls · `archive/AOS-P2-T06/` |


---

### PHASE 3 — L3 GUARDRAILS + L4 OBSERVER (`AOS-P3`)

#### AOS-P3-T01 — L3 MaxDD / de-risk / kill-switch wiring


| | |
| --- | --- |
| **Layer** | L3 |
| **What changes** | Hard hooks in EA or OS supervisor (0.8× / 1.0× DD_limit) |
| **Health fields** | MaxDD path; f_realised |
| **Skip/fire** | Fires stop when halted |
| **Test preset** | `AOS-P3-T01_L3guard_maxDD_Harvest_long.set` |
| **Accept** | Simulated DD trip halts; L2 cannot override |
| **Status** | `DONE` — **ACCEPT** offline · `doc/aos_l3_l4_offline.md` · trips `archive/AOS-P3-T01/` · live EA hook deferred |


#### AOS-P3-T02 — L3 FREQUENCY_STALL + cost-drift monitors


| | |
| --- | --- |
| **Layer** | L3 |
| **What changes** | Warn/halt channels |
| **Health fields** | fire_90d, Leak |
| **Test preset** | `AOS-P3-T02_L3guard_stallCost_Harvest_long.set` |
| **Accept** | Alerts fire in dry-run; policy documented |
| **Status** | `DONE` — **ACCEPT** · fire90=59 · no stall · `archive/AOS-P3-T02/` |


#### AOS-P3-T03 — L4 rolling health vector (W100/W250/W500)


| | |
| --- | --- |
| **Layer** | L4 |
| **What changes** | Observer service / EA module publishing vector + lifecycle |
| **Health fields** | All Stage-2 symbols |
| **Skip/fire** | None (observe only) |
| **Test preset** | `AOS-P3-T03_L4obs_rollingHealth_Harvest_long.set` |
| **Accept** | Matches offline score within tolerance; ΔD available |
| **Status** | `DONE` — **ACCEPT** · W100/250/500 Fragile · lifecycle CSV `archive/AOS-P3-T03/` |


#### AOS-P3-T04 — L4 → L3/L2 recommendation bus


| | |
| --- | --- |
| **Layer** | L4→L3/L2 |
| **What changes** | Compressing / Near / Below → size or halt recommendations |
| **Health fields** | Lifecycle accuracy vs offline |
| **Test preset** | `AOS-P3-T04_L4toL3_recommendBus_Harvest_long.set` |
| **Accept** | Below frontier always yields L3 f=0; no override path |
| **Status** | `DONE` — **ACCEPT** · Below→f=0 locked · terminal f_rec=0.5 Compressing · `archive/AOS-P3-T04/` |


---

### PHASE 4 — AVOIDANCE TRAINING (`AOS-P4`)

Train L2 on labelled engine trades (win/loss, MAE/MFE, regime, session, structure).

#### AOS-P4-T01 — Labelled dataset from Harvest blotter + tape


| | |
| --- | --- |
| **Layer** | L2/L6 |
| **What changes** | Dataset build (no live gate change) |
| **Health fields** | n labels ≥ baseline events |
| **Test preset** | `AOS-P4-T01_L2data_labelledHarvest_long.set` |
| **Accept** | Labels join tape; class balance reported |
| **Status** | `DONE` — **ACCEPT** · n=530 · TP/SL 289/241 · `archive/AOS-P4-T01/` |


#### AOS-P4-T02 — Train avoid-loser model (walk-forward folds)


| | |
| --- | --- |
| **Layer** | L2 |
| **What changes** | Challenger model artifact `L2skip_v1` |
| **Health fields** | Offline: predicted AL↓, precision/recall on losers |
| **Skip/fire** | Simulated skip rate in-band |
| **Test preset** | `AOS-P4-T02_L2train_avoidLoser_wf_Harvest.set` |
| **Accept** | OOS loser-recall useful; no fit-only-on-decay |
| **Status** | `DONE` — **CONDITIONAL ACCEPT** · AUC 0.55 · fold-2 hurt · `L2skip_v1.joblib` · `doc/aos_l2skip_v1.md` |


#### AOS-P4-T03 — Shadow mode (log skips, still fire)


| | |
| --- | --- |
| **Layer** | L2+L6 |
| **What changes** | Decisions logged; engine unrestricted |
| **Health fields** | Counterfactual EF if skips applied |
| **Skip/fire** | Actual fires = baseline; shadow skips recorded |
| **Test preset** | `AOS-P4-T03_L2shadow_skipLog_Harvest_long.set` |
| **Accept** | Counterfactual passes loose bar → eligible for live gate |
| **Status** | `DONE` — **ACCEPT** · CF EF 2.33→4.91 · loose PASS · `archive/AOS-P4-T03/` |


#### AOS-P4-T04 — Live avoid-gate (enable L2skip_v1)


| | |
| --- | --- |
| **Layer** | L2 |
| **What changes** | Withhold engine when model says skip |
| **Health fields** | EF, E_N, AL, MaxDD, fires |
| **Skip/fire** | Expect AL↓; fires ≥50% warn |
| **Test preset** | `AOS-P4-T04_L2gate_avoidLoser_live_Harvest_long.set` |
| **Accept** | Loose bar (§4) |
| **Status** | `DEFERRED` — weak AUC + live hooks paused; shadow-only |


---

### PHASE 5 — L5 RETRAIN LOOP (`AOS-P5`)

#### AOS-P5-T01 — Retrain cadence + triggers


| | |
| --- | --- |
| **Layer** | L5 |
| **What changes** | Policy: monthly + Compressing/Near-frontier |
| **Health fields** | Process only |
| **Test preset** | `AOS-P5-T01_L5_retrainPolicy_v0.set` |
| **Accept** | Written runbook; no silent prod overwrite |
| **Status** | `DONE` — **ACCEPT** · `doc/aos_l5_retrain_loop.md` · `archive/AOS-P5-T01/` |


#### AOS-P5-T02 — Champion/challenger promote rule


| | |
| --- | --- |
| **Layer** | L5 |
| **What changes** | Auto-compare: challenger W250 EF ≥ baseline EF and MaxDD not worse → candidate |
| **Health fields** | EF, MaxDD |
| **Test preset** | `AOS-P5-T02_L5_champChallenger_Harvest.set` |
| **Accept** | Dry-run promotes/rejects correctly; G2–G5 **not** required to *try* |
| **Status** | `DONE` — **ACCEPT** · dry-run 5/5 · `archive/AOS-P5-T02/champ_challenger_dryrun.json` |


#### AOS-P5-T03 — Versioned model store + rollback


| | |
| --- | --- |
| **Layer** | L5+L6 |
| **What changes** | Artifact store; pin live version; one-click rollback |
| **Test preset** | `AOS-P5-T03_L5_modelStore_rollback.set` |
| **Accept** | Rollback restores prior skip rate within noise |
| **Status** | `DONE` — **ACCEPT** · `models/L2skip/` pin v0 · rollback 0.2658→0.0 |


---

### PHASE 6 — FULL STACK + PRESETS (`AOS-P6`)

#### AOS-P6-T01 — Stack preset: L1+L2det+L3+L4+L6


| | |
| --- | --- |
| **Layer** | L1–L4,L6 |
| **What changes** | End-to-end deterministic OS (no AI yet) |
| **Health fields** | Full vector vs AOS-P0 |
| **Skip/fire** | Per skip map |
| **Test preset** | `AOS-P6-T01_stack_L1L2detL3L4L6_Harvest_long.set` |
| **Accept** | Loose bar |
| **Status** | `DONE` — **ACCEPT** · EF 2.33→3.01 n355 · `doc/aos_p6_stack.md` · `archive/AOS-P6-T01/` |


#### AOS-P6-T02 — Stack preset: + L2 AI skip


| | |
| --- | --- |
| **Layer** | +L2 AI |
| **Test preset** | `AOS-P6-T02_stack_L2ai_Harvest_long.set` |
| **Accept** | Loose bar; ledger complete |
| **Status** | `DONE` — **ACCEPT** shadow · CF EF 4.90 · live AI **DEFERRED** · `archive/AOS-P6-T02/` |


#### AOS-P6-T03 — Enable L7 sleeve throttle (Harvest primary)


| | |
| --- | --- |
| **Layer** | L7 |
| **What changes** | Weight Harvest &gt; Growth; block Mid |
| **Test preset** | `AOS-P6-T03_L7_sleeveThrottle_HarvestPrimary.set` |
| **Accept** | No Mid fires; Growth optional |
| **Status** | `DONE` — **ACCEPT** · Harvest 1.0 · Mid/Survival blocked · `archive/AOS-P6-T03/` |


#### AOS-P6-T04 — Enable L8 MAE early-abort advisor (shadow then live)


| | |
| --- | --- |
| **Layer** | L8 |
| **What changes** | Path-based abort advice / optional hard rule under L3 |
| **Health fields** | AL, MaxDD, RR−R |
| **Test preset** | `AOS-P6-T04_L8_maeAbort_shadow_Harvest.set` → `…_live_…` |
| **Accept** | Loose bar; must not rewrite entries |
| **Status** | `DONE` — **ACCEPT** shadow spec · live **DEFERRED** · `archive/AOS-P6-T04/` |


#### AOS-P6-T05 — L9 multi-horizon ensemble soft veto


| | |
| --- | --- |
| **Layer** | L9 |
| **Test preset** | `AOS-P6-T05_L9_multiHorizon_softVeto_Harvest.set` |
| **Accept** | Loose bar |
| **Status** | `DONE` — **ACCEPT** spec · unarmed until H1/H4 tape · `archive/AOS-P6-T05/` |


---

### PHASE 7 — LIVE PROMOTION (`AOS-P7`) — only phase that uses full framework gates

One OS candidate vs engine-only baseline. Iteration stays loose until this phase.

#### AOS-P7-T01 — OS vs engine A/B scorecard (currency)


| | |
| --- | --- |
| **Layer** | Full stack |
| **What changes** | None — score AOS stack preset vs AOS-P0 |
| **Health fields** | Full Stage 0–2 |
| **Test preset** | `AOS-P7-T01_promote_OSvsEngine_Harvest_long.set` |
| **Accept** | EF&gt;0 to keep iterating; EF&gt;M target to promote |
| **Status** | `DONE` — **ACCEPT** · OS EF 3.01 · **KEEP_ITERATING** (EF&lt;M) · `doc/aos_p7_promotion.md` |


#### AOS-P7-T02 — Light Stage 4: G3 regime + G4 block on skip-adjusted blotter


| | |
| --- | --- |
| **Layer** | Promotion |
| **Test preset** | `AOS-P7-T02_promote_G3G4light_Harvest.set` |
| **Accept** | G3 OK under regime_filtered; G4 light pass |
| **Status** | `DONE` — **ACCEPT** · G3 PASS · G4 light MC-2 PASS · `archive/AOS-P7-T02/` |


#### AOS-P7-T03 — G5 cost / param stress on OS (not engine re-tune)


| | |
| --- | --- |
| **Layer** | Promotion |
| **What changes** | ±10% stress **through OS** (engine geometry held; costs ×1.5) |
| **Test preset** | `AOS-P7-T03_promote_G5stress_OS_Harvest.set` |
| **Accept** | EF&gt;0 under stress to promote; else stay paper |
| **Status** | `DONE` — **ACCEPT** · G5 core PASS (cost×1.5 EF 1.91) · `archive/AOS-P7-T03/` |


#### AOS-P7-T04 — L10 HITL sign-off


| | |
| --- | --- |
| **Layer** | L10 |
| **What changes** | Human checklist + ledger sample audit |
| **Test preset** | n/a (promotion packet) |
| **Accept** | Signed `AOS_LIVE_v{N}`; rollback plan attached |
| **Status** | `DONE` — **PACKET READY / UNSIGNED** · **STAY_PAPER** · `archive/AOS-P7-T04/promotion_packet.json` |


---

## 8. Execution board (current)


| Phase | Next task | Ready? |
| --- | --- | --- |
| AOS-P0 … P7 | **Complete** (offline paper) | `aos_p7_promotion.md` |
| **Verify** | `tools/aos_phase_verify.py` · **ALL PASS** | `archive/AOS-VERIFY/` |
| **Wire** | BMRG **v1.20** · `Include/AOS.mqh` · compile 0 err | DONE |
| **aistack** | Tester scored · magic **8399001** | `archive/AOS-aistack-run/` |
| Promote | L10 sign + hold Robust W250 + stronger L1 | **STAY_PAPER** |


### Live tester snapshot (`aistack` · 2026-09-25)

| Window | Opens | WR | EF | Zone | vs engine (same calendar) |
| --- | ---: | ---: | ---: | --- | --- |
| Long 2025.01→2026.09 | 480 | 57.7% | **5.45** | **Robust** | engine EF 2.33 Fragile · **ΔEF +3.12** · n 530→477 |
| Jul→Sep | 294 | 56.3% | **4.05** | Fragile | engine EF 1.58 · **ΔEF +2.47** |
| 2026 YTD | 190 | 59.3% | **7.06** | **Robust** | ~flat vs engine recent |

Ledger (Jul run): FIRE 294 · SKIP **139** (32%) · L4 end **Compressing** f_rec 0.5 · W250 EF 4.2 · L3 trips 0.  
Rolling: long W250 EF **4.6** (path min **+1.8** vs engine path min **−3.8**). W100 ≈ engine (~8–9).  
Caveat: OOS AUC ~0.55; min-lot floors L4 size; **not** `AOS_LIVE`.

### What you do now

**Paper stack is live in tester.** Next: stronger L1 features → P5 retrain → hold Robust W250 → L10 sign-off.  
EDX main stream remains **closed**; engine champion still Harvest 8210204.

Key docs: `doc/aos_aistack.md` · `doc/aos_p7_promotion.md` · `Include/AOS.mqh` · `blotter/archive/AOS-aistack-run/`

---

## 9. Delta report format (every completed AOS task)

```text
TASK: AOS-P#-T##
LAYER: L#
PRESET: ...
ENGINE: Harvest 8210204 (or named)
n, fires_90d, WR, R, BWR, BM, Leak, EF, M, E_N, ΔD, MaxDD, AL
vs AOS_BASELINE: ΔEF, ΔMaxDD, Δfires, ΔE_N, ΔAL
SKIP_RATE: ...
ZONE: Negative|Fragile|Robust
LIFECYCLE_W250: ...
L3_TRIPS: ...
ACCEPT|REJECT|WARN (FREQUENCY_STALL|n<385|...)
ARCHIVE: blotter/archive/AOS-P#-T##/
```

---

## 10. Document map

| File | Role |
| --- | --- |
| `doc/ai_OS.md` | **This plan** — layers + AOS tasks |
| `system_profile.md` | Engine behaviour / class thesis |
| `doc/edge_discovery.md` | Isolated edge (closed as main stream) |
| `doc/edge_framework.md` | Stage scoring contract |
| `doc/candidate_pool.md` | Sleeve registry (Harvest champion) |
| `doc/aos_bad_cells.md` | L2 skip seeds (AOS-P0-T02) |
| `doc/ai_OS_baseline.md` | Frozen `AOS_BASELINE_v1` |
| `doc/aos_l1_feature_schema.md` | L1 feature + enum vocab |
| `doc/aos_l1_tape_contract.md` | JSONL tape + offline/live paths |
| `doc/aos_l2_policy_v0.md` | L2 skip/size policy (offline) |
| `doc/aos_l2skip_v1.md` | L2skip_v1 train + shadow (AOS-P4) |
| `doc/aos_l3_l4_offline.md` | L3 guards + L4 observer (AOS-P3) |
| `doc/aos_l5_retrain_loop.md` | L5 cadence / promote / rollback (AOS-P5) |
| `doc/aos_p6_stack.md` | Full stack presets offline (AOS-P6) |
| `doc/aos_p7_promotion.md` | Promote gates + STAY_PAPER (AOS-P7) |
| `doc/aos_aistack.md` | AI-enhanced stack preset + EA wiring contract |
| `models/L2skip/` | Versioned L2skip store + `LIVE.json` |
| `tools/aos_phase_verify.py` | P0–P7 + aistack regression check |
| `Include/AOS.mqh` · `AOS_L2skip_v1.mqh` | Runtime overlay (BMRG v1.20+) |
| `blotter/archive/AOS-*/` | Immutable OS experiment archives |
| `blotter/archive/AOS-aistack-run/` | Live tester extract · magic 8399001 |

---

## 11. Rules of engagement (sticky)

1. One AOS task at a time; ends with preset + loose accept/reject.  
2. Layers consume EDX findings — they do not re-run Edge Discovery.  
3. L3 Guardrails outrank every intelligence layer.  
4. Retrain is versioned; champion/challenger; never fit only on the decay window.  
5. Speak framework numbers (WR, R, BWR, BM, Leak, EF, M, E_N, ΔD, MaxDD, f) — not “AI confidence” as a substitute.  
6. OS may only **permit / withhold / size / halt** the Harvest (or named pool) engine — never replace the fade.  
7. Tester lift ≠ `AOS_LIVE`; L10 + Robust hold required to promote.

---

## 12. Versioning

- **0.2** — EA-wired v1.20; aistack tester evidence; board STAY_PAPER with live ΔEF.  
- **0.1** — Initial layer plan + AOS-P0…P7 offline path.  
