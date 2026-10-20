# UK100 M5 — AIOS Roadmap

**Version:** 0.1.0  
**Status:** **P0–P7 complete** — research OS **HITL ARMED** (expansion only; not FX live replace)  
**Engine lock (OS baseline):** Balanced P0 M5 · magic **26101905** · **AOS OFF**  
**Research OS arm:** magic **26121907** · **`UK100_5m_stack.set`** · [`AIOS_SIGNOFF_M5.md`](./AIOS_SIGNOFF_M5.md)  
**Preset (engine):** `Profiles/Tester/BMRG/UK100/BMRG-M5-UK100-6M-P0_balanced_chart.set`
**Parents:** [`edge_framework.md`](./edge_framework.md) · [`system_profile_M5.md`](./system_profile_M5.md) · `doc/ai_OS.md` · `doc/unified_edge_framework.md`  
**Sibling (do not merge):** M15 AIOS [`aios_roadmap.md`](./aios_roadmap.md) · magic **26101201** / **26111307**  
**Blotter:** `blotter/inbox/` → `blotter/archive/UK100-M5-AOS-*/` after review  

**Not** EURUSD aistack · **not** AUDUSD L2 pin · **not** AAPL L2det · **not** M15 `L2det_uk` / `L2skip_uk` · **not** a live replace.

---

## 0. Canvas caveat

| Artifact | Authority |
| --- | --- |
| This roadmap + scored blotters under `edge_framework.md` | **Normative** for UK100 **M5** AIOS work |
| `system_profile_M5.md` | Evidence / descriptive |
| M15 `aios_roadmap.md` / L2det_uk pin | **Reference only** — wrong TF fingerprint |
| Canvas / chat charts / UI tiles | **Display only** |

Verdicts come from ledger + scorecard. Tip-only charts never promote a layer. Do not reuse M15 Thu / H08 / Jul map on M5.

---

## 1. What this is / is not

| This is | This is not |
| --- | --- |
| A **UK100 M5-owned AIOS** that permits / withholds / sizes / observes / adapts Balanced P0 M5 | A new SL/TP or BBDev optimisation programme |
| Layered work with task IDs `UK100-M5-AOS-P#-T##` | A replacement entry model or trend sleeve |
| Iteration vs a frozen M5 Balanced baseline | Immediate live attach or M15 OS twin |
| Consumption of **M5** profile bad cells (Mon, H12–13, Aug, Feb/Apr) | Copy-paste of M15 L2det v1b |
| Separate model store pin (`L2skip_uk_m5_*`) | Reuse of EUR / AUD / AAPL / M15 UK pins |

**Frozen OS objective:**

```
maximise E_N
subject to  EF hold vs baseline (−1 pp on primary tip health window is enough to keep iterating)
            MaxDD ≤ baseline MaxDD + 2 pp
never maximise WR, PF, or BM alone
never invent entries — only gate the engine fade
never lift ATR max 869 to “fix” frequency
```

**Investigation order (unchanged):** data → execution → regime → structure.  
Do **not** touch SL/TP/BBDev/ATR max as the first OS move.

---

## 2. Working hypothesis (from `system_profile_M5.md`)

> Balanced P0 M5 already has a **stronger** tip meanrev edge than M15 engine (May→Aug WR **52.6%** / E_N **+0.183R** / +$51 / EF_prior **+4.1 pp**).  
> Remaining leak is **conditional** and **different from M15**: Mon soft, midday **H12–13** soft, **Aug** local tax under MATCH, prior **Feb–Apr** regime cluster. Tip is **buy-led** (54.8% BUY) — opposite of soft M15 tip sell-led story.  
> AI layers’ job: **withhold or size-down those M5 cells**, contain streak / late-tip path risk, keep **EF** alive after measured Leak — without rewriting the fade or borrowing M15 Thu/H08 pins.

| Claim | Evidence | Stance for OS |
| --- | --- | --- |
| Edge exists | Tip EXPANSION_KEEP · E_N +0.183R · EF_prior +4.1 pp | **Accept** — freeze as UK100-M5-AOS-P0 |
| Weakness is conditional | Mon WR 43.8% · H12–13 40.4% · Aug 42.1% · Feb–Apr soft | **Accept** — L2 skip/size, don’t chase R |
| Side is tip buy-led | BUY 54.8% · SELL 50.0% | **Accept** — never permanent AllowSell=false; SELL-caution only if CF proves |
| Morning cash is strong | H08–11 WR ~67% · Wed 65% | **Protect** — false-positive skips here = REJECT map |
| ATR max already filters FRAGILE | Gate ON · design required (unfiltered EF &lt; 0) | **Accept** — L1 feature; do **not** lift ATR max |
| Holds mostly intraday | Med win ~1.26h · ≥12h rare (~2%) | **Accept** — L8 gap path secondary |
| M15 L2det v1b fits M5 | Thu tip WR 50% (neutral) · H08 tip **strong** | **Reject** — wrong cells |
| Fixing via SL/TP first | Would reopen geometry; RR already TP&gt;SL | **Reject as first move** |
| Borrow EUR/AUD/AAPL/M15 pins | Wrong TF / session fingerprint | **Reject** — `L2skip_uk_m5_*` only |
| Probe WR 50.7% as OS target | Design prior only | **Reject** — beat Tester tip EF/E_N |

---

## 3. Architecture (same layers as `doc/ai_OS.md`)

```
L5 Retrain ──challenger──► L2 Policy (skip/size) ──permit──► Balanced ENGINE M5 (26101905)
L1 Tape ──────────────────►        ▲
                                   │
                          L3 Guardrails (hard veto)
                                   ▲
                          L4 Observer (W15/W20 → W50/W100)
                                   │
                          L6 Ledger (all decisions)
L8 MAE abort (secondary) · L9 session quality · L10 HITL promote
```

**Invariant:** L3 outranks L1/L2/L4/L5/L8–L10.

### UK100 M5 layer emphasis

| Layer | M5 focus |
| --- | --- |
| **L1** | ATR vs **869** · London session age · DOW/hour · side · BBDev · spread · cooldown 3 · MATCH/FRAGILE · short streak |
| **L2det** | **Mon** · **H12–13** · **Aug**-like stress · near-ATR-cap · optional SELL-caution if CF · never skip all mornings / Wed |
| **L2 AI** | Avoid-loser on Balanced M5 fires only; pin `L2skip_uk_m5_*` |
| **L3** | MaxDD · Below-frontier f=0 · kill-switch · streak-aware halt |
| **L4** | Dense n → W20/W50 first-class; W15 still useful on tip softness |
| **L5** | Retrain on decay / Compressing; WF through decay |
| **L6** | Full reason codes for CF scorecards |
| **L8** | Secondary (intraday); losers resolve faster than winners — MAE abort candidate |
| **L10** | Only promotion path to “UK100 M5 OS live research” |

---

## 4. Baseline lock (UK100-M5-AOS-P0)

Import Balanced health from scored logs / profile. **No OS code in P0.**

| Field | Tip May→Aug 2026 | Long Jan→Aug 2026 | Prior Jan→Apr (inside long) |
| --- | ---: | ---: | ---: |
| Magic / RR | **26101905** / 1.25 | same | same |
| n | **116** | 235 | ~119 |
| WR | **52.6%** | 48.9% | soft cluster (Feb–Apr) |
| E_N (des) | **+0.183R** | +0.101R | ≤0 months present |
| BM / EF_prior | +8.1 pp / **+4.1 pp** | +4.5 / +0.5 | diagnostic |
| Final Δ ($500) | **+$51.16** | +$57.25 | — |
| MaxDD (path proxy) | **~2.5%** | mid-single-digit | Feb–Apr dig |
| AOS | Off | Off | Off |

**OS compare window (default):** **tip May→Aug** — state which on every task. Prior / long = L3 diagnostics. Tip alone may KEEP expansion OS trials; never sole production admission.

**Bad-cell registry:** [`aos_bad_cells_M5.md`](./aos_bad_cells_M5.md) (P0-T02).  
**Baseline packet:** [`UK100_M5_AOS_BASELINE_v1.md`](./UK100_M5_AOS_BASELINE_v1.md) (P0-T01).  
**Cost stub:** [`aos_cost_policy_M5.md`](./aos_cost_policy_M5.md) (P0-T03).

---

## 5. Iteration bar (loose on purpose)

**Accept** a layer experiment when **all** hold:

| Check | Bar |
| --- | --- |
| n remaining after skips | Report; denser TF — expect tip base ~116; no n≥385 floor |
| Tip-window E_N / EF | ≥ baseline − **1 pp** EF (or E_N hold if Leak pending) |
| MaxDD | ≤ baseline + **2 pp** (~2.5% tip proxy → soft ≤4.5%) |
| 90d fire count | ≥ 50% baseline (~40–50 / 90d tip pace) → else FREQUENCY_STALL **warn** |
| AL | Not worse unless E_N clearly improved |
| Bad-cell hit rate | Skips concentrated in M5 registry cells (report precision vs winners) |
| Protect cells | False-skip rate on **Wed** / **H08–11** / tip **BUY** must be reported; high FP → REJECT |

**Reject immediately** when:

- WR↑ but E_N↓ or EF↓  
- Layer invents entries / changes SL/TP/ATR max as “OS”  
- Higher layer overrides L3 halt  
- Uses EUR/AUD/AAPL/**M15 UK** model pin on M5  
- Permanently disables BUY because some future window flips sell-led  
- Arms M15 `DOW_THU` / `HOUR_08` without M5 CF  

**Promote (UK100-M5-AOS-P7 only)** when: shadow CF beats/holds baseline · L3/L4 wired · ledger complete · HITL sign-off under `edge_framework.md`. Full G0–G5 for any live-capital claim — not for every weekly trial.

---

## 6. Phase plan (task catalogue)

### PHASE 0 — ENGINE BASELINE LOCK (`UK100-M5-AOS-P0`) — **DONE**

| Task | Layer | Deliverable | Status |
| --- | --- | --- | --- |
| **P0-T01** | — | Freeze `UK100_M5_AOS_BASELINE_v1` scorecard (tip + long + prior note) | **DONE** 2026-10-20 |
| **P0-T02** | — | Bad-cell registry from `system_profile_M5.md` | **DONE** 2026-10-20 |
| **P0-T03** | — | Cost policy + Leak prior; deal-measured still open | **DONE** prior 2026-10-20 · journal proxy via P1 · measured **OPEN** |

### PHASE 1 — L1 PERCEPTION (`UK100-M5-AOS-P1`) — **DONE** (T04 deferred)

| Task | Layer | Deliverable | Status |
| --- | --- | --- | --- |
| **P1-T01** | L1 | M5 feature schema v0 (`aos_l1_tape_contract_M5.md`) | **DONE** 2026-10-20 |
| **P1-T02** | L1 | Offline tape builder from Tester Balanced M5 fires | **DONE** `build_m5_fire_tape.py` |
| **P1-T03** | L1 | Label fires: win/lose · DOW · hour · side · ATR vs 869 · spread · month | **DONE** tip 116 + prior 119 + long 235 |
| **P1-T04** | L1 | Structure flags v0 (band-ride / failed fade) — optional | **DEFERRED** (schema §2.3) |
| **P1-T05** | L1 | Ouroboros MATCH/FRAGILE month flag (soft) | **DONE** tip months MATCH |

### PHASE 2 — L2 POLICY (`UK100-M5-AOS-P2`) — **DONE**

| Task | Layer | Deliverable | Status |
| --- | --- | --- | --- |
| **P2-T01** | L2det | Parity: skip Tue + ATR max 869 — OS mirror / no double-count | **DONE** PASS |
| **P2-T02** | L2det | SOFT skip map v1: **Mon** ± **H12–13** shadow CF | **DONE** — Mon∧H12 ARM · full H12 HOLD · Mon∨H12 REJECT |
| **P2-T03** | L2det | Side-caution SOFT CF (SELL first if tip stays buy-led; no blanket) | **DONE** — **ARM SELL∧H12** · DISARM blanket SELL/BUY |
| **P2-T04** | L2det | Stress-month / near-ATR SOFT CF (**Aug** seed · Feb/Apr prior) | **DONE** — Aug HOLD · blanket near_atr DISARM |
| **P2-T05** | L2size | Lifecycle → f table (spec; wire after L4) | **DONE** SPEC (`aos_l2_size_table_M5.md`) |
| **P2-T06** | L2 AI | Train `L2skip_uk_m5` avoid-loser · shadow | **DONE** — **DISARM** (AUC_tip≈0.40) |
| **P2-T07** | L2 AI | Stack CF vs P0 / L2det | **DONE** — best **v1b** (Mon∧H12)∨(SELL∧H12) |

### PHASE 3 — L3 + L4 (`UK100-M5-AOS-P3`) — **DONE**

| Task | Layer | Deliverable | Status |
| --- | --- | --- | --- |
| **P3-T01** | L3 | MaxDD / kill / Below-frontier halt policy | **DONE** SIGNED · v1b tip trip-free |
| **P3-T02** | L3 | Cost-drift + FREQUENCY_STALL warn · streak | **DONE** SIGNED |
| **P3-T03** | L4 | Rolling health W20/W50 (+ W15 path) | **DONE** paths in archive |
| **P3-T04** | L4→L3 | Recommend bus: Below → halt; Compressing → investigate | **DONE** SIGNED |

### PHASE 4 — LEDGER + STACK (`UK100-M5-AOS-P4`) — **DONE**

| Task | Layer | Deliverable | Status |
| --- | --- | --- | --- |
| **P4-T01** | L6 | Decision ledger schema + offline writer | **DONE** `aos_l6_ledger_M5.md` |
| **P4-T02** | stack | Det stack `L1+L2det+L3+L4+L6` shadow run | **DONE** tip n_fire=83 E_N=+0.383 |
| **P4-T03** | stack | + L2 AI shadow on det fires | **DONE** DISARM · 2 shadow skips |
| **P4-T04** | L8 | MAE abort advisor (shadow; losers resolve ~0.66h med) | **DONE** 23/23 loser advises |

### PHASE 5 — RETRAIN LOOP (`UK100-M5-AOS-P5`) — **DONE**

| Task | Layer | Deliverable | Status |
| --- | --- | --- | --- |
| **P5-T01** | L5 | Retrain policy + model store `L2skip_uk_m5/` | **DONE** `aos_l5_retrain_M5.md` · `train_l2_uk100_m5.py` |
| **P5-T02** | L5 | Champ/challenger promote rules | **DONE** AI challenger EMPTY · overlay L2det champ |
| **P5-T03** | L5 | Rollback drill | **DONE** `_drill/` pass |

### PHASE 6 — HARDENING (`UK100-M5-AOS-P6`) — **DONE**

| Task | Layer | Deliverable | Status |
| --- | --- | --- | --- |
| **P6-T01** | L9 | Session-quality soft veto (midday / spread tercile — not morning) | **DONE** H14+/spread ARM_SOFT · morning DISARM |
| **P6-T02** | G5-ish | ±10% bound stress on L2 thresholds (not SL/TP) | **DONE** keep H12–13 · widen/narrow hurts |
| **P6-T03** | — | Confirm ATR max 869 declared for G3 when OS armed | **DONE** PASS |

### PHASE 7 — PROMOTION (`UK100-M5-AOS-P7`) — **DONE 2026-10-20 HITL**

| Task | Layer | Deliverable | Status |
| --- | --- | --- | --- |
| **P7-T01** | L10 | Promotion packet: CF · health · ledger · gates | **DONE** `promotion_packet.json` |
| **P7-T02** | L10 | HITL sign-off · research OS arm (magic **26121907**) | **SIGNED** · `UK100_5m_stack.set` · `AIOS_SIGNOFF_M5.md` |
| **P7-T03** | — | Paper / tiny-f attach checklist | **DONE** in sign-off |

---

## 7. Weekly implementation table

Calendar assumes **Week 1 = week of 2026-10-20** (Mon). Slip tasks forward; do not skip P0/P1 to chase L2 AI. One primary task stream at a time; blotter clear-after-review applies. **Do not block on / merge with M15 stream.**

| Week | Dates (2026) | Phase | Primary tasks | Exit criteria (done when) |
| ---: | --- | --- | --- | --- |
| **1** | Oct 20–26 | P0 | P0-T01 · P0-T02 · P0-T03 stub | Baseline + bad-cells + cost stub in `doc/assets/UK100/` |
| **2** | Oct 27–Nov 2 | P0→P1 | Deal export measured Leak · P1-T01 feature schema | `Leak_source=measured` on tip scorecard **or** documented OPEN · schema reviewed |
| **3** | Nov 3–9 | P1 | P1-T02 tape builder · P1-T03 label fires | Offline tape covers tip+long fires · labels QA’d |
| **4** | Nov 10–16 | P1 | P1-T04 (opt) · P1-T05 Ouroboros flags | Tape v0 frozen |
| **5** | Nov 17–23 | P2 | P2-T01 ATR/Tue parity · P2-T02 Mon/H12–13 SOFT shadow | CF ledger · E_N/EF vs baseline within bar **or** reject map |
| **6** | Nov 24–30 | P2 | P2-T03 side-caution · P2-T04 Aug / near-ATR map | Armed only if CF pass; else DISARMED |
| **7** | Dec 1–7 | P3 | P3-T01 L3 · P3-T02 stall/cost | Offline L3 trips on M5 path · policy md |
| **8** | Dec 8–14 | P3 | P3-T03 L4 health · P3-T04 bus | W20/W50 health CSV · Below→halt verified |
| **9** | Dec 15–21 | P4 | P4-T01 ledger · P4-T02 det stack shadow | Full det stack CF vs P0 |
| **10** | Dec 22–28 | P2/P4 | P2-T06 train `L2skip_uk_m5` · P2-T07 AI shadow CF | Model pin under `infra/artefacts/models/L2skip_uk_m5/` · shadow only |
| **11** | Dec 29–Jan 4 | P4 | P4-T03 AI+det · P4-T04 L8 shadow | Stack CF; L8 advise-only |
| **12** | Jan 5–11 | P5 | P5-T01…T03 retrain/rollback | Store + rollback drill documented |
| **13** | Jan 12–18 | P6 | P6-T01…T03 harden | Soft veto CF; ATR G3 note |
| **14** | Jan 19–25 | P7 | P7-T01 · P7-T02 HITL | KEEP OS research arm **or** stay shadow with named gaps |
| **15** | Jan 26–Feb 1 | buffer | Slip / re-runs · P7-T03 if armed | Clean archive; roadmap status update |

### Weekly operating rhythm

| Day | Action |
| --- | --- |
| Mon | Confirm week’s primary task · load M5 Balanced preset · note compare window (tip default) |
| Tue–Thu | Implement / run Tester / build tape or CF |
| Fri | Score under `edge_framework.md` · ACCEPT/REJECT · archive blotter · update this roadmap status |
| Ongoing | No foreign pins · no SL/TP “quick fix” · Canvas display-only · magics disjoint from M15 |

---

## 8. Preset / artifact naming

```text
Profiles/Tester/BMRG/UK100/UK100-M5-AOS-P{phase}-T{task}_{layer}_{change}.set
blotter/archive/UK100-M5-AOS-P{phase}/
  or UK100-M5-AOS-P{phase}-T{task}/
infra/artefacts/models/L2skip_uk_m5/LATEST/
doc/assets/UK100/aos_bad_cells_M5.md
doc/assets/UK100/aos_cost_policy_M5.md
doc/assets/UK100/UK100_M5_AOS_BASELINE_v1.md
doc/assets/UK100/aos_l1_tape_contract_M5.md   # from P1
doc/assets/UK100/aos_l2_policy_M5.md          # from P2
```

Research OS magic: keep engine **26101905**; OS experiment magics in **2612xxxx** (P7 target **26121907**) — never collide with M15 **2610/2611**** or EUR/AUD live.

---

## 9. Scorecard fields (every weekly exit)

```text
framework_unified: 1.0
framework_uk100: 0.1.0
aos_task: UK100-M5-AOS-P#-T##
tf: M5
preset_id / magic / window / n
aos_overlay: none | L2det | L2AI_shadow | L2AI_withhold | L3 | stack
baseline_ref: UK100_M5_AOS_BASELINE_v1
WR, R, BWR, BM, Leak, Leak_source, EF, M, E_N, PF
skips_n, skip_precision_bad_cell, fire_retention_pct
false_skip_Wed, false_skip_H08_11, false_skip_BUY
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
| `edge_framework.md` | Normative scoring / gates (shared asset) |
| `system_profile_M5.md` | Descriptive M5 behaviour |
| `UK100_M5_AOS_BASELINE_v1.md` | Frozen P0 numbers |
| `aos_bad_cells_M5.md` | L2det seed registry (M5 cells) |
| `aos_cost_policy_M5.md` | Leak · journal proxy 5.93 pp |
| `aos_l1_tape_contract_M5.md` | L1 schema v0 |
| `aos_l2_policy_M5.md` | L2 P2 complete — **v1b stack** ARM_SOFT · L2AI DISARM |
| `aos_l2_size_table_M5.md` | L2size f multipliers (spec) |
| `aos_l3l4_policy_M5.md` | L3 halt / L4 health bus (P3 signed) |
| `aos_l6_ledger_M5.md` | L6 ledger · stack CF · research `.set` (P4) |
| `aos_l5_retrain_M5.md` | L5 retrain · champ/challenger · rollback (P5) |
| `aos_p6_harden_M5.md` | P6 L9 session · L2 bound stress · ATR G3 |
| `AIOS_SIGNOFF_M5.md` | **HITL** research OS arm · `UK100_5m_stack` · magic **26121907** |
| `Include/AOS_L2det_uk_m5.mqh` | M5 L2det v1b wire (BMRG v1.24) |
| `infra/artefacts/models/L2skip_uk_m5/` | AI shadow store (DISARM) |
| `tapes/uk100_m5_*_fire_tape_v0.csv` | Tip / prior / long / combined |
| `aios_roadmap.md` | **M15** sibling (complete P0–P7) — do not merge scorecards |
| `doc/ai_OS.md` | Layer vocabulary |
| `blotter/archive/UK100-M5-P0-CHART/` | Engine review (pre-OS) |
| `blotter/archive/UK100-M5-AOS-P1/` | Builder · TAPE_QA · COST_PROXY |
| `infra/artefacts/models/L2skip_uk_m5/` | AI shadow store (from P2/P5) |

---

## 11. Versioning

- **0.1.0** — Initial UK100 M5 AIOS plan from system-profile enhancement thesis; P0-T01…T03 landed; weekly calendar from 2026-10-20.  
- Bump when phase order, iteration bar, pin name, or baseline window changes.

---

## 12. One-line plan

**Freeze Balanced P0 M5, measure Leak, build an M5-native skip/size OS aimed at Mon / H12–13 / Aug / Feb–Apr cells, protect morning + Wed, shadow until tip EF holds, then promote research OS only — never borrow M15 or FX L2, never retune geometry as the first move.**

---

## 13. Status line (update Fridays)

```text
2026-10-20 | P7 HITL SIGNED | ARM_RESEARCH_OS UK100_5m_stack magic 26121907 · L2det_uk_m5_v1b · not FX replace · stream P0-P7 closed
```
