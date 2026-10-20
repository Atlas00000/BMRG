# AUDUSD — AIOS Roadmap (CHAMP · M15 research OS)

**Version:** 0.1.7  
**Status:** **P0–P7 complete** — research OS **HITL ARMED** (M15 only; not live M5 SCALE replace)  
**Engine lock (OS baseline):** CHAMP Harvest · magic **8230901** · **AOS OFF** · M15  
**Preset (engine):** `doc/presets/AUDUSD-CHAMP_Harvest_start13_skipMon_G0.set`  
**Research OS arm:** magic **8231941** · **`AUDUSD_stack.set`** · [`AIOS_SIGNOFF.md`](./AIOS_SIGNOFF.md)  
**Live path (Track B):** magic **8230931** · SCALE Risk 3% (separate)  
**Parents:** [`edge_framework.md`](./edge_framework.md) · [`system_profile.md`](./system_profile.md) · `doc/ai_OS.md` · `doc/unified_edge_framework.md`  
**Blotter:** `blotter/inbox/` → `blotter/archive/AUDUSD-AOS-*/` after review  

**Not** a replace of live M5 AIOS SCALE (**8230931**) · **not** EURUSD M15/M5 L2 pins · **not** UK100 / DE40 / stock L2 · **not** SL/TP re-optimisation.

### Parallel track (live M5 — do not collide)

| Track | Magic | Role |
| --- | ---: | --- |
| **A — this roadmap** | **8230901** → OS **8231941** | M15 research OS build |
| **B — live improve** | **8230931** | Retrain weak `L2skip_aud_*` · stay LIVE_WITHHOLD · Risk 3% |

Track B uses the same layer vocabulary but **separate** tape/pin semver and blotter IDs `AUDUSD-LIVE-L2-*`. Do not mix magics.

---

## 0. Canvas caveat

| Artifact | Authority |
| --- | --- |
| This roadmap + scored blotters under `edge_framework.md` | **Normative** for AUDUSD CHAMP AIOS work |
| `system_profile.md` | Evidence / descriptive |
| Canvas / chat charts / UI tiles | **Display only** |

Verdicts come from ledger + scorecard. Tip-only charts never promote a layer. Probe EF is never scored EF. OS compares against **8230901** M15 tip.

---

## 1. What this is / is not

| This is | This is not |
| --- | --- |
| An **AUDUSD CHAMP-owned AIOS** that permits / withholds / sizes / observes / adapts the freeze | A new SL/TP or BBDev optimisation programme |
| Layered work with task IDs `AUDUSD-AOS-P#-T##` | A replacement entry model or trend sleeve |
| Iteration vs frozen **8230901** M15 baseline | Immediate live attach or M5 SCALE replace |
| Consumption of profile bad cells (Thu, May, Feb/Mar, band-ride) | Re-ranking from profit / WR alone |
| Separate model store pin (`L2skip_aud_m15_*`) | Reuse of EUR M5/M15 · UK100 · DE40 · live `L2skip_aud_p90_*` without CF |

**Frozen OS objective:**

```
maximise E_N
subject to  EF hold vs baseline (−1 pp on primary tip health window is enough to keep iterating)
            MaxDD ≤ baseline MaxDD + 2 pp
never maximise WR, PF, or BM alone
never invent entries — only gate the engine fade
```

**Investigation order (unchanged):** data → execution → regime → structure.  
Do **not** touch SL/TP/BBDev/session/weekday as the first OS move.  
Do **not** re-open EDX payoff / ATR-gate experiments as “OS”.

---

## 2. Working hypothesis (from AUDUSD system profile)

> CHAMP already has a real meanrev edge on the M15 tip (May→Aug WR **63.4%** / E_N **+0.268R** / +$133).  
> Remaining leak is **conditional**: fires still occur in DOW / calendar cells where BM ≤ 0 (Thu, May; Feb/Mar on long). Losers die fast (med **4.6h**); winners overnight (med **23.4h**).  
> Live M5 AIOS already exists at Risk 3% with a **weak** L2 pin (AUC ~0.46) — Track B retrain; Track A builds a clean M15-native OS.  
> AI layers’ job: **withhold or size-down bad-cell fires**, contain streak / DD path, keep **EF** alive after measured Leak — without rewriting the fade.

| Claim | Evidence | Stance for OS |
| --- | --- | --- |
| Edge exists | Tip Stage 0 · EXPANSION_KEEP · E_N +0.268R | **Accept** — freeze as AUDUSD-AOS-P0 |
| Weakness is conditional | Thu WR 40% · May 37.5% · Feb/Mar soft | **Accept** — L2 skip/size, don’t chase R |
| Both sides contribute | BUY 61% · SELL 65% | **Accept** — never permanent AllowBuy=false |
| Overnight-heavy winners | Med win ~23h · ≥12h ~77% | **Accept** — L8 + swap in Leak |
| Thin fire rate (M15) | ~10–12 / 30d | **Accept** — small-n W15/W20; FREQUENCY_STALL looser than M5 |
| Fixing via SL/TP first | Would reopen EDX | **Reject as first move** |
| Borrow EUR / UK / DE40 L2 | Wrong book / TF / session | **Reject** — AUD M15 pin only |
| ATR max gate | P8-T03 SKIP | **Reject** as OS first move |
| Tip $ alone as OS target | Path-dependent | **Reject** — beat tip E_N/EF vs baseline |

---

## 3. Architecture (same layers as `doc/ai_OS.md`)

```
L5 Retrain ──challenger──► L2 Policy (skip/size) ──permit──► CHAMP ENGINE (8230901)
L1 Tape ──────────────────►        ▲
                                   │
                          L3 Guardrails (hard veto)
                                   ▲
                          L4 Observer (W15/W20 → W100/W250)
                                   │
                          L6 Ledger (all decisions)
L8 MAE/gap abort (overnight) · L9 session quality · L10 HITL promote
```

**Invariant:** L3 outranks L1/L2/L4/L5/L8–L10.

### AUDUSD CHAMP layer emphasis

| Layer | AUDUSD focus |
| --- | --- |
| **L1** | ATR vs tip dist · session age 13–20 · DOW/hour · side · BBDev 2.2 · CD · spread · nights_held · month tag · streak · hold_speed |
| **L2det** | **BUY∧May** (v1 ARM_SOFT) · BUY∧Thu alt · blanket Thu/May HOLD · band-ride/fast-lose label-only |
| **L2 AI** | Avoid-loser on CHAMP fires only; pin `L2skip_aud_m15_*` |
| **L3** | MaxDD · Below-frontier f=0 · kill-switch · streak-aware halt · overnight DD path |
| **L4** | Small-n **W15/W20** first; adopt W100/W250 when n allows (live Track B already uses W250) |
| **L5** | Retrain on decay / Compressing; WF through soft months, not only on them |
| **L6** | Full reason codes for CF scorecards |
| **L8** | Overnight MAE / gap-open advisor (primary for overnight inventory) |
| **L9** | Soft veto candidates: Thu · late stress · spread tercile |
| **L10** | Only promotion path to “AUDUSD M15 OS research arm” |

---

## 4. Baseline lock (AUDUSD-AOS-P0)

Import CHAMP health from scored logs / profile. **No OS code in P0.**

| Field | Tip May→Aug 2026 | Long Jan→Aug 2026 |
| --- | ---: | ---: |
| Magic / RR | **8230901** / 1.0 | same |
| n | **41** | 95 |
| WR | **63.4%** | 56.8% |
| E_N (des) | **+0.268R** | +0.137R |
| BM | **+13.4 pp** | +6.8 pp |
| Final Δ ($400) | **+$133.27** | +$149.30 |
| W20 min→last | 50→**75** | 40→75 |
| path DD~ | **3.0%** | 4.4% |
| Max W / L streak | 12 / 4 | — / 7 |
| AOS | Off | Off |

**OS compare window (default):** **tip May→Aug** — state which on every task. Long = support / L3 diagnostics.

**Bad-cell registry:** [`aos_bad_cells.md`](./aos_bad_cells.md) (P0-T02).  
**Baseline packet:** [`AUDUSD_AOS_BASELINE_v1.md`](./AUDUSD_AOS_BASELINE_v1.md) (P0-T01).  
**Cost stub:** [`aos_cost_policy.md`](./aos_cost_policy.md) (P0-T03).

---

## 5. Iteration bar (loose on purpose)

**Accept** a layer experiment when **all** hold:

| Check | Bar |
| --- | --- |
| n remaining after skips | Report; no production n floor for expansion OS |
| Tip-window E_N / EF | ≥ baseline − **1 pp** EF (or E_N hold if Leak pending) |
| MaxDD / path DD | ≤ baseline + **2 pp** |
| 90d fire count | ≥ 50% baseline (~20–25 / 90d on M15) → else FREQUENCY_STALL **warn** |
| AL | Not worse unless E_N clearly improved |
| Bad-cell hit rate | Skips concentrated in registry cells (report precision/recall vs winners) |
| Protect cells | False-skip rate on **SELL / Wed / Fri / H15·H18 / Jun–Aug** must be reported |

**Reject immediately** when:

- WR↑ but E_N↓ or EF↓  
- Layer invents entries / changes SL/TP/BB/session as “OS”  
- Re-opens ATR max / Mon-on without a new preset card  
- Higher layer overrides L3 halt  
- Uses EUR / UK / DE40 / live-M5 pin on AUD M15 without CF  
- Permanently disables BUY because tip was sell-led  

**Promote (AUDUSD-AOS-P7 only)** when: shadow CF beats/holds baseline · L3/L4 wired · ledger complete · HITL sign-off under `edge_framework.md`. Full G0–G5 for any live-capital claim on this M15 OS — live capital stays on **8230931** M5 until a separate live decision.

---

## 6. Phase plan (task catalogue)

### PHASE 0 — ENGINE BASELINE LOCK (`AUDUSD-AOS-P0`) — **DONE stubs** (measured Leak OPEN)

| Task | Layer | Deliverable | Status |
| --- | --- | --- | --- |
| **P0-T01** | — | Freeze `AUDUSD_AOS_BASELINE_v1` scorecard (tip + long) | **DONE** 2026-10-19 |
| **P0-T02** | — | Bad-cell registry from profile | **DONE** 2026-10-19 |
| **P0-T03** | — | Cost policy + Leak prior stub; deal-measured still open | **DONE** stub · measured **OPEN** |

### PHASE 1 — L1 PERCEPTION (`AUDUSD-AOS-P1`) — **DONE** 2026-10-19

| Task | Layer | Deliverable | Status |
| --- | --- | --- | --- |
| **P1-T01** | L1 | AUDUSD M15 feature schema v0 (`aos_l1_tape_contract.md`) | **DONE** |
| **P1-T02** | L1 | Offline tape builder from Tester CHAMP fires / bars | **DONE** |
| **P1-T03** | L1 | Label fires: tip n=41 · long n=95 · atr_missing=0 | **DONE** |
| **P1-T04** | L1 | Structure proxies `fast_lose` · `band_ride_proxy` | **DONE** |
| **P1-T05** | L1 | Soft regime `MATCH`/`MISMATCH` month flag | **DONE** |

### PHASE 2 — L2 POLICY (`AUDUSD-AOS-P2`) — **DONE**

| Task | Layer | Deliverable | Status |
| --- | --- | --- | --- |
| **P2-T01** | L2det | Parity: skip Mon/Tue + session — OS mirror / no double-count | **DONE** PASS |
| **P2-T02** | L2det | SOFT skip map v1: **Thu** shadow CF | **DONE** HOLD_SOFT (blanket) |
| **P2-T03** | L2det | Stress-month SOFT CF (May · Feb/Mar-like) | **DONE** **BUY∧May ARM_SOFT** |
| **P2-T04** | L2det | Fast-lose / band-ride SOFT CF (never blanket side cut) | **DONE** LABEL_ONLY |
| **P2-T05** | L2size | Lifecycle → f table (spec; wire after L4) | **DONE** SPEC |
| **P2-T06** | L2 AI | Train `L2skip_aud_m15` avoid-loser · shadow | **DONE** SHADOW_ONLY |
| **P2-T07** | L2 AI | Stack CF vs P0 / L2det | **DONE** preferred = L2det v1 |

### PHASE 3 — L3 + L4 (`AUDUSD-AOS-P3`) — **DONE**

| Task | Layer | Deliverable | Status |
| --- | --- | --- | --- |
| **P3-T01** | L3 | MaxDD / kill / Below-frontier halt policy (overnight-aware) | **DONE** SIGNED |
| **P3-T02** | L3 | Cost-drift + FREQUENCY_STALL warn · streak | **DONE** SIGNED |
| **P3-T03** | L4 | Rolling health W15/W20 (+ W50/W250 when wiring) | **DONE** SIGNED |
| **P3-T04** | L4→L3 | Recommend bus: Below → halt; Compressing → investigate | **DONE** SIGNED |

### PHASE 4 — LEDGER + STACK (`AUDUSD-AOS-P4`) — **DONE**

| Task | Layer | Deliverable | Status |
| --- | --- | --- | --- |
| **P4-T01** | L6 | Decision ledger schema + offline writer | **DONE** |
| **P4-T02** | stack | Det stack `L1+L2det+L3+L4+L6` shadow run | **DONE** E_N+0.333 |
| **P4-T03** | stack | + L2 AI shadow on det fires | **DONE** SHADOW n=3 |
| **P4-T04** | L8 | MAE / gap abort advisor (shadow; overnight primary) | **DONE** 6 advise · 4 overnight |

### PHASE 5 — RETRAIN LOOP (`AUDUSD-AOS-P5`) — **DONE**

| Task | Layer | Deliverable | Status |
| --- | --- | --- | --- |
| **P5-T01** | L5 | Retrain policy + model store `L2skip_aud_m15/` | **DONE** |
| **P5-T02** | L5 | Champ/challenger promote rules (shadow→candidate) | **DONE** eligible · HITL pending |
| **P5-T03** | L5 | Rollback drill | **DONE** pass |

### PHASE 6 — HARDENING (`AUDUSD-AOS-P6`) — **DONE**

| Task | Layer | Deliverable | Status |
| --- | --- | --- | --- |
| **P6-T01** | L9 | Session-quality soft veto (Thu / spread tercile) | **DONE** BUY∧Thu SHADOW |
| **P6-T02** | G5-ish | ±10% bound stress on L2 thresholds (not SL/TP) | **DONE** PASS |
| **P6-T03** | — | Confirm geometry still frozen on OS arm preset | **DONE** AUDUSD_stack |

### PHASE 7 — PROMOTION (`AUDUSD-AOS-P7`) — **DONE 2026-10-19 HITL**

| Task | Layer | Deliverable | Status |
| --- | --- | --- | --- |
| **P7-T01** | L10 | Promotion packet: CF · health · ledger · gates | **DONE** `promotion_packet.json` |
| **P7-T02** | L10 | HITL sign-off · research OS arm mag **8231941** | **SIGNED** `AUDUSD_stack` |
| **P7-T03** | — | Paper / tiny-f attach checklist (M15 research only) | **DONE** in `AIOS_SIGNOFF.md` |

---

## 6b. Track B — live M5 L2 improve (parallel)

| Task | Deliverable | Status |
| --- | --- | --- |
| **LIVE-T01** | Fresh tape from live/FT CHAMP fires (M5) | OPEN |
| **LIVE-T02** | Retrain challenger vs `L2skip_aud_p90_20261008_122523` | OPEN |
| **LIVE-T03** | Shadow CF on Risk 3% path · ACCEPT only if AUC/EF beat | OPEN |
| **LIVE-T04** | Bake + HITL if ACCEPT · else keep current pin | OPEN |

Do **not** change Risk% / W250 / geometry in Track B without a separate survival packet.

---

## 7. Weekly implementation table

Calendar assumes **Week 1 = week of 2026-10-20** (Mon). Slip tasks forward; do not skip P0 measured Leak / P1 to chase L2 AI. One primary task stream at a time; blotter clear-after-review applies.

| Week | Dates (2026) | Phase | Primary tasks | Exit criteria (done when) |
| ---: | --- | --- | --- | --- |
| **0** | Oct 19 | P0 | P0-T01 · P0-T02 · P0-T03 stub | Baseline + bad-cells + cost stub in `doc/assets/AUDUSD/` |
| **1** | Oct 20–26 | P0→P1 | Deal export measured Leak · P1-T01 feature schema | `Leak_source=measured` on tip scorecard · schema reviewed |
| **2** | Oct 27–Nov 2 | P1 | P1-T02 tape builder · P1-T03 label fires | Offline tape covers tip+long fires · labels QA’d |
| **3** | Nov 3–9 | P1 | P1-T04 structure · P1-T05 month flags | Tape v0 frozen |
| **4** | Nov 10–16 | P2 | P2-T01 parity · P2-T02 Thu SOFT shadow | CF ledger · E_N/EF vs baseline within bar **or** reject map |
| **5** | Nov 17–23 | P2 | P2-T03 stress-month · P2-T04 fast-lose | Armed only if CF pass; else DISARMED |
| **6** | Nov 24–30 | P3 | P3-T01 L3 · P3-T02 stall/cost | Offline L3 trips on AUD path · policy md |
| **7** | Dec 1–7 | P3 | P3-T03 L4 health · P3-T04 bus | W15/W20 health CSV · Below→halt verified |
| **8** | Dec 8–14 | P4 | P4-T01 ledger · P4-T02 det stack shadow | Full det stack CF vs P0 |
| **9** | Dec 15–21 | P2/P4 | P2-T06 train `L2skip_aud_m15` · P2-T07 AI shadow CF | Model pin under `infra/artefacts/models/L2skip_aud_m15/` · shadow only |
| **10** | Dec 22–28 | P4 | P4-T03 AI+det · P4-T04 L8 shadow | Stack CF; L8 advise-only |
| **11** | Dec 29–Jan 4 | P5 | P5-T01…T03 retrain/rollback | Store + rollback drill documented |
| **12** | Jan 5–11 | P6 | P6-T01…T03 harden | Soft veto CF; geometry freeze note |
| **13** | Jan 12–18 | P7 | P7-T01 · P7-T02 HITL | KEEP OS research arm **or** stay shadow with named gaps |
| **14** | Jan 19–25 | buffer | Slip / Track B LIVE-T01…T04 | Clean archive; roadmap status update |

### Weekly operating rhythm

| Day | Action |
| --- | --- |
| Mon | Confirm week’s primary task · load CHAMP preset · note compare window (tip default) |
| Tue–Thu | Implement / run Tester / build tape or CF |
| Fri | Score under `edge_framework.md` · ACCEPT/REJECT · archive blotter · update this roadmap status |
| Ongoing | No foreign L2 pin · no SL/TP “quick fix” · Canvas display-only · don’t collide with **8230931** |

---

## 8. Preset / artifact naming

```text
Profiles/Tester/BMRG/AUDUSD/AUDUSD-AOS-P{phase}-T{task}_{layer}_{change}.set
blotter/archive/AUDUSD-AOS-P{phase}-T{task}/
infra/artefacts/models/L2skip_aud_m15/LATEST/
doc/assets/AUDUSD/aos_bad_cells.md
doc/assets/AUDUSD/aos_cost_policy.md
doc/assets/AUDUSD/AUDUSD_AOS_BASELINE_v1.md
doc/assets/AUDUSD/aos_l1_tape_contract.md   # from P1
doc/assets/AUDUSD/aos_l2_policy.md          # from P2 (DONE)
doc/assets/AUDUSD/aos_l2_size_table.md      # from P2-T05 SPEC
doc/assets/AUDUSD/aos_l3l4_policy.md        # from P3 (DONE)
doc/assets/AUDUSD/aos_l6_ledger.md          # from P4 (DONE)
doc/assets/AUDUSD/aos_l5_retrain.md         # from P5 (DONE)
doc/assets/AUDUSD/aos_p6_harden.md          # from P6 (DONE)
Presets/AUDUSD_stack.set                    # P7 HITL ARMED (alias …P7_research_OS_ARMED.set)
```

Research OS magic: keep engine **8230901**; OS experiment / arm magics in **82319xx** — never collide with live **8230931** / FT **8230921** / EURUSD INF.

---

## 9. Scorecard fields (every weekly exit)

```text
framework_unified: 1.0
framework_audusd: 0.1.0
aos_task: AUDUSD-AOS-P#-T##
preset_id / magic / window / n / tf
aos_overlay: none | L2det | L2AI_shadow | L2AI_withhold | L3 | stack
baseline_ref: AUDUSD_AOS_BASELINE_v1
WR, R, BWR, BM, Leak, Leak_source, EF, M, E_N, PF
skips_n, skip_precision_bad_cell, fire_retention_pct
false_skip_rate_on_SELL_or_WedFri_or_H15H18
ΔE_N_vs_baseline, ΔEF_vs_baseline, MaxDD
verdict: ACCEPT | REJECT | HOLD_SHADOW
canvas: display_only
live_collision: none | noted_8230931
```

---

## 10. Document map

| File | Purpose |
| --- | --- |
| **`aios_roadmap.md`** | **This plan** |
| `edge_framework.md` | Normative scoring / gates |
| `system_profile.md` | Descriptive behaviour (M15 CHAMP) |
| `AUDUSD_AOS_BASELINE_v1.md` | Frozen P0 numbers |
| `aos_bad_cells.md` | L2det seed registry |
| `aos_cost_policy.md` | Leak prior · deal-export stub |
| `AIOS_SIGNOFF.md` | **P7** research OS **8231941** + live M5 SCALE **8230931** |
| `candidate_pool.md` | KEEP / LIVE labels |
| `doc/ai_OS.md` | Layer vocabulary |
| `blotter/archive/AUDUSD-M15-EXP/` | Engine review (pre-OS) |
| `blotter/archive/AUDUSD-AOS-P0/` | P0 stubs |
| `blotter/archive/AUDUSD-AOS-P1/` | Builder · TAPE_QA · COST_PROXY · tip/long tapes |
| `blotter/archive/AUDUSD-AOS-P2/` | P2_CF · L2AI scored · REVIEW |
| `blotter/archive/AUDUSD-AOS-P3/` | P3_L3L4 · health_path_*.csv · REVIEW |
| `blotter/archive/AUDUSD-AOS-P4/` | P4_STACK · ledger_*.csv · research .set · REVIEW |
| `doc/assets/AUDUSD/tapes/` | Fire tapes v0 · tip ledger v1 shadow |
| `doc/assets/AUDUSD/aos_l2_policy.md` | L2det v1 BUY∧May · AI SHADOW |
| `doc/assets/AUDUSD/aos_l3l4_policy.md` | L3 halt · L4 W15/W20 · bus |
| `doc/assets/AUDUSD/aos_l6_ledger.md` | L6 schema · research OS · L8 advise |
| `Include/AOS_L2det_aud.mqh` | MQL L2det v1 (default Enable=false) |
| `blotter/archive/AUDUSD-AOS-P5/` | retrain REVIEW · rollback drill |
| `doc/assets/AUDUSD/aos_l5_retrain.md` | L5 store · promote · rollback |
| `infra/artefacts/models/L2skip_aud_m15/` | M15 AI store (SHADOW_ONLY) |
| `blotter/archive/AUDUSD-AOS-P*/` | Later phase archives |
| `infra/artefacts/models/L2skip_aud/` | Live M5 pin store (Track B) — do not mix |

---

## 11. Versioning

- **0.1.0** — Initial AUDUSD CHAMP M15 AIOS plan; P0 stubs from system_profile / M15-EXP (2026-10-19).  
- **0.1.1** — P1 tapes + schema + journal Leak_proxy (2026-10-19).  
- **0.1.2** — P2 L2det v1 BUY∧May ARM_SOFT · `L2skip_aud_m15` SHADOW_ONLY (2026-10-19).  
- **0.1.3** — P3 L3/L4 signed · v1 tip trip-free · W15/W20 bus (2026-10-19).  
- **0.1.4** — P4 ledger + det_v1 stack · L8 advise · `AOS_L2det_aud` · research .set **8231941** (2026-10-19).  
- **0.1.5** — P5 retrain store · promote rules · rollback drill · AI eligible pending HITL (2026-10-19).  
- **0.1.6** — HITL challenger · P6 harden · armed **AUDUSD_stack** magic **8231941** (2026-10-19).  
- **0.1.7** — P7 HITL SIGNED · `ARM_RESEARCH_OS` · stream P0–P7 closed (2026-10-19).  
- Bump when phase order, iteration bar, pin name, baseline window, or live-collision rules change.

---

## 12. One-line plan

**Freeze CHAMP M15, measure Leak, build an AUDUSD-native skip/size OS aimed at Thu/May/Feb–Mar/band-ride cells, shadow until tip E_N/EF holds, then promote research OS only — never borrow foreign L2, never retune geometry as the first move, never replace live M5 SCALE 8230931 without a separate HITL.**

---

## 13. Status line (update Fridays)

```text
2026-10-19 | P7 HITL SIGNED | ARM_RESEARCH_OS magic 8231941 · AUDUSD_stack · not M5 replace · stream P0-P7 closed
```
