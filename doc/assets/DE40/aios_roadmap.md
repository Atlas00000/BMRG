# DE40 — AIOS Roadmap (M15 Balanced P0)

**Version:** 0.1.0  
**Status:** **P0–P7 complete** — research OS **HITL ARMED** (`DE40stack` · magic **26141907**) · expansion only · not live replace  
**Engine lock (OS baseline):** Balanced P0 · magic **26101902** · **AOS OFF**  
**Preset (engine):** `Profiles/Tester/BMRG/DE40/BMRG-M15-DE40-6M-P0_balanced_chart.set`  
**Preset (P4 pre-HITL):** `…/BMRG-M15-DE40-6M-P4_research_OS_W50.set` · magic **26141904**  
**Research OS arm:** **`DE40stack.set`** · magic **26141907** · [`AIOS_SIGNOFF.md`](./AIOS_SIGNOFF.md)  
**Parents:** [`edge_framework.md`](./edge_framework.md) · [`system_profile.md`](./system_profile.md) · `doc/ai_OS.md` · `doc/unified_edge_framework.md`  
**Blotter:** `blotter/inbox/` → `blotter/archive/DE40-AOS-*/` after review  

**Not** EURUSD M5/M15 aistack · **not** UK100 L2det · **not** USDJPY / AUD L2 pins · **not** a live replace.

---

## 0. Canvas caveat

| Artifact | Authority |
| --- | --- |
| This roadmap + scored blotters under `edge_framework.md` | **Normative** for DE40 / DE30 AIOS work |
| `system_profile.md` | Evidence / descriptive |
| Canvas / chat charts / UI tiles | **Display only** |

Verdicts come from ledger + scorecard. Tip-only charts never promote a layer. Probe EF is never scored EF. Broker depth from **2025.06.05** — truncated hist is never multi-year evidence.

---

## 1. What this is / is not

| This is | This is not |
| --- | --- |
| A **DE40-owned AIOS** that permits / withholds / sizes / observes / adapts Balanced P0 | A new SL/TP or BBDev optimisation programme |
| Layered work with task IDs `DE40-AOS-P#-T##` | A replacement entry model or trend sleeve |
| Iteration vs a frozen P0 baseline | Immediate live attach or FX/UK replace |
| Consumption of profile bad cells (Feb, Mar, MISMATCH stubs, residual FRAGILE) | Re-ranking from profit / WR alone |
| Separate model store pin (`L2skip_de40_*` / `L2det_de40_*`) | Reuse of EUR / UK / USDJPY / AUD / AAPL L2 pins |
| Regime-first hygiene (tip already EF>0 under Leak prior) | Pretending 2025 stub death is class failure · thinning SL under fat spread |

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
Do **not** thin SL below ~5000 (Leak collapses EF under DE30 spread).  
Do **not** claim Stage-1 Robust on Leak **prior** alone — measure first (tip EF prior is healthy; still measure).

---

## 2. Working hypothesis (from DE40 profile)

> Balanced P0 already has a **strong** meanrev edge on the tip (May→Oct WR **58.4%** / E_N **+0.31R** / EF prior **+4.2 pp** / +$139). Probe and Tester tip **align**.  
> Remaining leak is **conditional / regime**: YTD diluted by **Feb–Mar**; 2025 Jun–Jul **MISMATCH** stub WR ~32%; residual **Sep–Oct FRAGILE** fires under ATR max; side/DOW/hour still **OPEN**.  
> AI layers’ job: **withhold or size-down regime-hostile fires**, protect Aug / MATCH tip stars, contain YTD MaxDD path, keep **EF** after measured Leak — without rewriting the fade or borrowing foreign pins.

| Claim | Evidence | Stance for OS |
| --- | --- | --- |
| Edge exists | Tip EXPANSION_KEEP · E_N +0.310R · EF prior +4.2 pp | **Accept** — freeze as DE40-AOS-P0 |
| Weakness is conditional | Feb WR 34% · Mar 0% · 2025 MISMATCH ~32% | **Accept** — L2 skip/size, don’t chase R |
| Tip is home | Aug WR 64% n=33 · Jun–Aug MATCH | **Accept** — protect cells |
| ATR max already filters FRAGILE | Gate ON · Sep/Oct thinned · still slight + | **Accept** — L1 feature; do not lift ATR as OS “fix” |
| Fat spread / fat SL | Spread≈1020 · SL 5000 · Leak prior 9.8 pp | **Accept** — measure Leak; never thin SL first |
| Probe ≈ Tester | WR 58.2% → 58.4% | **Accept** — probe = prior only; tip = authority |
| Side / DOW / hour | Tip **sell-led** · Mon/H08 stars · H13 soft | **Accept** — P1 tape filled; L2det seeds updated |
| Fixing via SL/TP first | Would reopen geometry; thin SL kills EF | **Reject as first move** |
| Borrow EUR / UK / USDJPY L2 | Wrong book / session / cost fingerprint | **Reject** — DE40 pin only |
| Reject asset on 2025 stub | MISMATCH months | **Reject** — regime tax, not DROP |

---

## 3. Architecture (same layers as `doc/ai_OS.md`)

```
L5 Retrain ──challenger──► L2 Policy (skip/size) ──permit──► P0 ENGINE (26101902)
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

### DE40 / DE30 layer emphasis

| Layer | DE40 focus |
| --- | --- |
| **L1** | ATR vs 4070 · session age 08–17 · DOW/hour · side · BBDev 2.2 · CD · spread vs 1500 · Ouroboros MATCH/MISMATCH/FRAGILE · streak |
| **L2det** | Feb-like · H13 · Mar FRAGILE · MISMATCH-tag SOFT (protect May) · BUY∧near_atr · **never** blanket Aug/SELL/Mon/H08 |
| **L2 AI** | Avoid-loser on P0 fires only; pin `L2skip_de40_*` |
| **L3** | MaxDD (YTD ~14% path) · Below-frontier f=0 · kill-switch · streak-aware halt |
| **L4** | Small-n W15/W20 first; tip W20 already healthy — adopt W100/W250 when n allows |
| **L5** | Retrain on decay / Compressing; WF through decay, not only on it |
| **L6** | Full reason codes for CF scorecards |
| **L8** | **Secondary** (cash-sleeve index); MAE abort advise-only until overnight share known |
| **L9** | Frankfurt open soft veto · spread tercile vs MaxSpread 1500 |
| **L10** | Only promotion path to “DE40 OS live research” |

---

## 4. Baseline lock (DE40-AOS-P0)

Import Balanced health from scored caches / profile. **No OS code.**

| Field | Tip May→Oct 2026 | YTD Jan→Oct 2026 | 2025 Jun→Aug stub |
| --- | ---: | ---: | ---: |
| Magic / RR | **26101902** / 1.25 | same | same |
| n | **77** | 147 | 38 |
| WR | **58.4%** | 50.3% | 31.6% |
| E_N (des) | **+0.310R** | +0.132R | −0.29R |
| BM / EF_prior | +14.0 pp / **+4.2 pp** | +5.9 / −3.9 | −12.8 / ≪0 |
| Final Δ ($500) | **+$138.90** | +$112.43 | −$76.5 |
| MaxDD≈ | **4.4%** | 13.9% | 16.8% |
| AOS | Off | Off | Off |

**OS compare window (default):** **tip May→Oct** — state which on every task. YTD = support / L3 diagnostics. 2025 stub = **MISMATCH footnote only** — never sole DROP. Tip alone may KEEP expansion OS trials; never sole production admission.

**Bad-cell registry:** [`aos_bad_cells.md`](./aos_bad_cells.md) (P0-T02).  
**Baseline packet:** [`DE40_AOS_BASELINE_v1.md`](./DE40_AOS_BASELINE_v1.md) (P0-T01).  
**Cost stub:** [`aos_cost_policy.md`](./aos_cost_policy.md) (P0-T03).

---

## 5. Iteration bar (loose on purpose)

**Accept** a layer experiment when **all** hold:

| Check | Bar |
| --- | --- |
| n remaining after skips | Report; no n≥385 floor (per DE40 edge_framework) |
| Tip-window E_N / EF | ≥ baseline − **1 pp** EF (or E_N hold if Leak pending) |
| MaxDD | ≤ baseline + **2 pp** (tip MaxDD≈4.4%) |
| 90d fire count | ≥ 50% tip baseline (~35–42 / 90d from ~14/30d) → else FREQUENCY_STALL **warn** |
| AL | Not worse unless E_N clearly improved |
| Bad-cell hit rate | Skips concentrated in registry cells (report precision/recall vs winners) |
| Protect cells | False-skip rate on **Aug / Jun–Jul MATCH / tip high-WR months** must be reported |

**Reject immediately** when:

- WR↑ but E_N↓ or EF↓  
- Layer invents entries / changes SL/TP/ATR max / BB / session as “OS”  
- Thins SL below ~5000 or lifts MaxSpread as a Leak “fix”  
- Higher layer overrides L3 halt  
- Uses EUR / UK / USDJPY / AUD / AAPL model pin on DE30  
- Permanently disables a side/DOW before tape exists  
- Claims Robust / production on Leak **prior** alone  
- Rejects asset solely on 2025 MISMATCH stub  

**Promote (DE40-AOS-P7 only)** when: shadow CF beats/holds baseline · L3/L4 wired · ledger complete · HITL sign-off under `edge_framework.md`. Full G0–G5 for any live-capital claim — not for every weekly trial. Live capital stays off DE40 until then.

---

## 6. Phase plan (task catalogue)

### PHASE 0 — ENGINE BASELINE LOCK (`DE40-AOS-P0`) — **STUBS DONE** (measured Leak OPEN)

| Task | Layer | Deliverable | Status |
| --- | --- | --- | --- |
| **P0-T01** | — | Freeze `DE40_AOS_BASELINE_v1` scorecard (tip + YTD + 2025 stub footnote) | **DONE** 2026-10-19 |
| **P0-T02** | — | Bad-cell registry from profile | **DONE** 2026-10-19 |
| **P0-T03** | — | Cost policy + Leak prior stub; deal-measured still open | **DONE** prior 2026-10-19 · measured **OPEN** |

### PHASE 1 — L1 PERCEPTION (`DE40-AOS-P1`) — **DONE** (T04 optional OPEN)

| Task | Layer | Deliverable | Status |
| --- | --- | --- | --- |
| **P1-T01** | L1 | DE40 M15 feature schema v0 (`aos_l1_tape_contract.md`) | **DONE** 2026-10-19 |
| **P1-T02** | L1 | Offline tape builder from Tester P0 fires / bars | **DONE** tip+YTD · `build_de40_m15_fire_tape.py` |
| **P1-T03** | L1 | Label fires: win/lose · DOW · hour · side · ATR · spread · month · HALT | **DONE** tip 77 + YTD 147 |
| **P1-T04** | L1 | Structure flags v0 (band-ride / failed fade) — optional | OPEN |
| **P1-T05** | L1 | Ouroboros MATCH/MISMATCH/FRAGILE month flag (soft) | **DONE** on tape columns |

### PHASE 2 — L2 POLICY (`DE40-AOS-P2`) — **DONE** 2026-10-19

| Task | Layer | Deliverable | Status |
| --- | --- | --- | --- |
| **P2-T01** | L2det | Parity: skip Tue + ATR max — OS mirror / no double-count | **DONE** PASS |
| **P2-T02** | L2det | SOFT skip map v1: Feb-like ± H13 shadow CF | **DONE** — H13 HOLD · Feb ARM YTD-only |
| **P2-T03** | L2det | Buy-caution SOFT CF (BUY∧near_atr — never blanket BUY) | **DONE** — **ARM BUY∧near_atr** |
| **P2-T04** | L2det | MISMATCH-tag / FRAGILE residual SOFT CF (protect May) | **DONE** — DISARM blanket MISMATCH |
| **P2-T05** | L2size | Lifecycle → f table (spec; wire after L4) | **DONE** SPEC (`aos_l2_size_table.md`) |
| **P2-T06** | L2 AI | Train `L2skip_de40` avoid-loser · shadow | **DONE** — **DISARM** (AUC≈0.51) |
| **P2-T07** | L2 AI | Stack CF vs P0 / L2det | **DONE** — best arm **BUY∧near_atr** · v1b HOLD |

### PHASE 3 — L3 + L4 (`DE40-AOS-P3`) — **DONE** 2026-10-19

| Task | Layer | Deliverable | Status |
| --- | --- | --- | --- |
| **P3-T01** | L3 | MaxDD / kill / Below-frontier halt policy (YTD-path aware) | **DONE** SIGNED · tip trip-free · YTD BELOW×1 |
| **P3-T02** | L3 | Cost-drift + FREQUENCY_STALL warn · streak | **DONE** SIGNED |
| **P3-T03** | L4 | Rolling health W15/W20 (+ W50 when wiring) | **DONE** paths in archive |
| **P3-T04** | L4→L3 | Recommend bus: Below → halt; Compressing → investigate | **DONE** SIGNED |

### PHASE 4 — LEDGER + STACK (`DE40-AOS-P4`) — **DONE / SIGNED**

| Task | Layer | Deliverable | Status |
| --- | --- | --- | --- |
| **P4-T01** | L6 | Decision ledger schema + offline writer | **DONE** · `aos_l6_ledger.md` |
| **P4-T02** | stack | Det stack `L1+L2det+L3+L4+L6` shadow run | **DONE** · ARM n=62 E_N+0.42 |
| **P4-T03** | stack | + L2 AI shadow on det fires | **DONE** · DISARM · 18 shadow |
| **P4-T04** | L8 | MAE abort advisor (shadow; **secondary** for cash sleeve) | **DONE** · 16/16 losers · not armed |

### PHASE 5 — RETRAIN LOOP (`DE40-AOS-P5`) — **DONE / SIGNED**

| Task | Layer | Deliverable | Status |
| --- | --- | --- | --- |
| **P5-T01** | L5 | Retrain policy + model store layout `L2skip_de40/` | **DONE** · `aos_l5_retrain.md` · `train_l2_de40.py` |
| **P5-T02** | L5 | Champ/challenger promote rules (shadow→candidate) | **DONE** · AI challenger EMPTY |
| **P5-T03** | L5 | Rollback drill | **DONE** · `_drill/` pass |

### PHASE 6 — HARDENING (`DE40-AOS-P6`) — **DONE / SIGNED**

| Task | Layer | Deliverable | Status |
| --- | --- | --- | --- |
| **P6-T01** | L9 | Session-quality soft veto (Frankfurt open / spread tercile) | **DONE** · no LIVE · see `aos_p6_harden.md` |
| **P6-T02** | G5-ish | ±10% bound stress on L2 thresholds (not SL/TP) | **DONE** · keep 0.9/4070 |
| **P6-T03** | — | Confirm ATR max declared for G3 when OS armed | **DONE** · 4070 on P0+P4 |

### PHASE 7 — PROMOTION (`DE40-AOS-P7`) — **DONE 2026-10-19 HITL**

| Task | Layer | Deliverable | Status |
| --- | --- | --- | --- |
| **P7-T01** | L10 | Promotion packet: CF · health · ledger · gates | **DONE** `promotion_packet.json` |
| **P7-T02** | L10 | HITL sign-off · research OS arm | **SIGNED** magic **26141907** · **`DE40stack`** |
| **P7-T03** | — | Paper / tiny-f attach checklist | **DONE** in `AIOS_SIGNOFF.md` |

---

## 7. Weekly implementation table

Calendar assumes **Week 0 = 2026-10-19** (P0 stubs) · **Week 1 = week of 2026-10-20** (Mon). Slip tasks forward; do not skip measured Leak / P1 tape to chase L2 AI. One primary task stream at a time; blotter clear-after-review applies.

| Week | Dates (2026) | Phase | Primary tasks | Exit criteria (done when) |
| ---: | --- | --- | --- | --- |
| **0** | Oct 19 | P0 | P0-T01 · P0-T02 · P0-T03 stub | Baseline + bad-cells + cost stub in `doc/assets/DE40/` |
| **1** | Oct 19–20 | P1 | P1-T01…T03 · T05 · tapes | **DONE** tip 77 + YTD 147 · bad-cells updated |
| **2** | Oct 19 | P2 | P2-T01…T07 CF | **DONE** ARM BUY∧near_atr · see `aos_l2_policy.md` |
| **3** | Oct 19 | P3 | P3-T01…T04 L3/L4 | **DONE** tip trip-free · see `aos_l3l4_policy.md` |
| **4** | Oct 20–26 | P3→P4 | Deal export measured Leak (opt) · start P4 | `Leak_source=measured` preferred before P7 |
| **5** | Oct 19 | P4 | P4-T01 ledger · P4-T02 det stack shadow | **DONE** ARM stack CF |
| **6** | Oct 19 | P4 | P4-T03 AI+det (AI DISARM) · P4-T04 L8 shadow | **DONE** · next=P5 |
| **7** | Oct 19 | P5 | P5-T01…T03 retrain/rollback | **DONE** · next=P6 |
| **8** | Oct 19 | P6 | P6-T01…T03 harden | **DONE** · next=P7 |
| **9** | Oct 19 | P7 | P7-T01 · P7-T02 HITL | **DONE** · `DE40stack` · magic 26141907 |
| **10** | buffer | P7 | P7-T03 checklist · Tester confirm | Monitor · measured Leak |

### Weekly operating rhythm

| Day | Action |
| --- | --- |
| Mon | Confirm week’s primary task · load P0 preset · note compare window (tip default) |
| Tue–Thu | Implement / run Tester / build tape or CF |
| Fri | Score under `edge_framework.md` · ACCEPT/REJECT · archive blotter · update this roadmap status |
| Ongoing | No EUR/UK/USDJPY/AUD pin · no SL/TP “quick fix” · no thin-SL under spread · Canvas display-only |

---

## 8. Preset / artifact naming

```text
Profiles/Tester/BMRG/DE40/DE40-AOS-P{phase}-T{task}_{layer}_{change}.set
blotter/archive/DE40-AOS-P{phase}-T{task}/
infra/artefacts/models/L2skip_de40/LATEST/
doc/assets/DE40/aos_bad_cells.md
doc/assets/DE40/aos_cost_policy.md
doc/assets/DE40/DE40_AOS_BASELINE_v1.md
doc/assets/DE40/aos_l1_tape_contract.md   # from P1
doc/assets/DE40/aos_l2_policy.md          # from P2
```

Research OS magic: keep engine **26101902**; OS experiment magics in **2614xxxx** (target arm **26141907**) — never collide with EUR (`2612xxxx` / `8210xxx`), UK (`2611xxxx`), USDJPY (`2613xxxx`), or AUD live.

---

## 9. Scorecard fields (every weekly exit)

```text
framework_unified: 1.0
framework_de40: 0.1.0
aos_task: DE40-AOS-P#-T##
preset_id / magic / window / n
aos_overlay: none | L2det | L2AI_shadow | L2AI_withhold | L3 | stack
baseline_ref: DE40_AOS_BASELINE_v1
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
| **`aios_roadmap.md`** | **This plan** |
| `edge_framework.md` | Normative scoring / gates |
| `system_profile.md` | Descriptive behaviour |
| `DE40_AOS_BASELINE_v1.md` | Frozen P0 numbers |
| `aos_bad_cells.md` | L2det seed registry |
| `aos_cost_policy.md` | Leak / deal-export stub |
| `aos_l1_tape_contract.md` | L1 feature schema v0 |
| `tapes/de40_*_fire_tape_v0.csv` | Tip / YTD / combined labeled fires |
| `aos_l2_policy.md` | L2det / L2AI ARM map (P2) |
| `aos_l2_size_table.md` | f multipliers (spec) |
| `aos_l3l4_policy.md` | L3 halt / L4 health bus (P3) |
| `AIOS_SIGNOFF.md` | HITL research OS arm (from P7) |
| `doc/ai_OS.md` | Layer vocabulary |
| `blotter/archive/DE40-P0-CHART/` | Engine review (pre-OS) |
| `blotter/archive/DE40-AOS-P1/` | Builder · COST_PROXY · TAPE_QA |
| `blotter/archive/DE40-AOS-P2/` | P2_CF · REVIEW · run_p2_cf.py |
| `blotter/archive/DE40-AOS-P3/` | P3_L3L4 · health_path_*.csv |
| `blotter/archive/DE40-AOS-P4/` | P4_STACK · ledger_*.csv · research `.set` |
| `blotter/archive/DE40-AOS-P5/` | REVIEW · tip_l2ai_scored · `_drill/` |
| `blotter/archive/DE40-AOS-P6/` | P6_HARDEN · run_p6_harden.py |
| `blotter/archive/DE40-AOS-P7/` | promotion_packet · `DE40stack.set` |
| `infra/artefacts/models/L2skip_de40/` | AI shadow store · rollback CLI (DISARM) |
| `Include/AOS_L2det_de.mqh` | DE L2det BUY∧nearATR wire |

---

## 11. Versioning

- **0.1.0** — Initial DE40 AIOS plan; P0→P6 · **P7 HITL ARMED `DE40stack`** (2026-10-19).  
- Bump when phase order, iteration bar, pin name, or baseline window changes.

---

## 12. One-line plan

**Freeze Balanced P0 (tip already strong), measure Leak, build a DE40-native skip/size OS aimed at Feb/Mar/MISMATCH/residual-FRAGILE cells while protecting Aug/MATCH tip stars, fill side/DOW from tape, shadow until tip EF holds after honest costs, then promote research OS only — never borrow foreign L2, never thin SL under fat spread, never replace live FX/UK books.**

---

## 13. Status line (update Fridays)

```text
2026-10-19 | P7 HITL SIGNED | ARM_RESEARCH_OS DE40stack magic 26141907 · L2det BUY∧near_atr · not live replace · stream P0-P7 closed
```
