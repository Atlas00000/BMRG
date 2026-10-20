# EURUSD — AIOS Roadmap (M15 P2)

**Version:** 0.1.0  
**Status:** **P0–P7 complete** — research OS **HITL ARMED** (M15 expansion only; not M5 Harvest replace)  
**Engine lock (OS baseline):** P2 light-selective · magic **26101817** · **AOS OFF**  
**Preset (engine):** `Profiles/Tester/BMRG/EURUSD/BMRG-M15-EURUSD-6M-P2_light_selective_chart.set`  
**Research OS arm:** magic **26121807** · `BMRG-M15-EURUSD-6M-P7_research_OS_ARMED.set` · [`AIOS_SIGNOFF.md`](./AIOS_SIGNOFF.md)  
**Parents:** [`edge_framework.md`](./edge_framework.md) · [`system_profile.md`](./system_profile.md) · `doc/ai_OS.md` · `doc/unified_edge_framework.md`  
**Blotter:** `blotter/inbox/` → `blotter/archive/EURUSD-AOS-*/` after review  

**Not** EURUSD M5 aistack (`8210204` / `8399001`) · **not** AUDUSD L2 pin · **not** UK100 L2det · **not** a live replace of M5 Harvest.

---

## 0. Canvas caveat

| Artifact | Authority |
| --- | --- |
| This roadmap + scored blotters under `edge_framework.md` | **Normative** for EURUSD M15 AIOS work |
| `system_profile.md` | Evidence / descriptive |
| Canvas / chat charts / UI tiles | **Display only** |

Verdicts come from ledger + scorecard. Tip-only charts never promote a layer. Probe EF is never scored EF. P0/P1 ladder magics are context only — OS compares against **26101817**.

---

## 1. What this is / is not

| This is | This is not |
| --- | --- |
| An **EURUSD M15-owned AIOS** that permits / withholds / sizes / observes / adapts P2 | A new SL/TP or BBDev optimisation programme |
| Layered work with task IDs `EURUSD-AOS-P#-T##` | A replacement entry model or trend sleeve |
| Iteration vs a frozen P2 baseline | Immediate live attach or M5 Harvest replace |
| Consumption of profile bad cells (BUY, Thu, H13/H19, Feb, Aug) | Re-ranking from profit / WR alone |
| Separate model store pin (`L2skip_eur_m15_*`) | Reuse of M5 / AUD / UK100 / AAPL L2 pins |

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
Do **not** re-stack P1 (ATR≤68 + BBw) — starvation known.

---

## 2. Working hypothesis (from EURUSD M15 profile)

> P2 light already has a real meanrev edge on the tip (May→Oct WR 46.7% / E_N +0.05R / +$7; YTD stronger).  
> Remaining leak is **conditional**: fires still occur in side / DOW / hour / calendar cells where BM ≤ 0 or expectancy collapses (BUY, Thu, H13·H19, Feb, Aug). Tip EF under Leak **prior** is thin/negative (−0.7 pp) — **costs_fragile** until deals.  
> AI layers’ job: **withhold or size-down those fires**, contain overnight path / streak risk, keep **EF** alive after measured Leak — without rewriting the fade.

| Claim | Evidence | Stance for OS |
| --- | --- | --- |
| Edge exists | Tip Stage 0 · EXPANSION_KEEP · E_N +0.050R | **Accept** — freeze as EURUSD-AOS-P0 |
| Weakness is conditional | BUY WR 39% · Thu 38% · Feb 30% · Aug soft | **Accept** — L2 skip/size, don’t chase R |
| Sell-led tip + YTD | SELL WR 55–61% | **Accept** — buy-caution SOFT only; never permanent AllowBuy=false |
| ATR max already filters FRAGILE | Gate ON · Oct thin | **Accept** — L1 feature; do not lift ATR max as OS “fix” |
| Overnight-heavy holds | Med win ~24h · hold≥12h ~66–86% | **Accept** — L8 + swap in Leak primary (vs UK100 cash) |
| Thin fire rate | ~8 trades / 30d | **Accept** — small-n W15/W20; FREQUENCY_STALL bar looser than M5 |
| Fixing via SL/TP / P1 stack first | Would reopen geometry / starve n | **Reject as first move** |
| Borrow M5 / AUD / UK100 L2 | Wrong TF / book / session fingerprint | **Reject** — EURUSD M15 pin only |
| Probe WR 50% as OS target | Design prior only | **Reject** — beat Tester tip EF/E_N |

---

## 3. Architecture (same layers as `doc/ai_OS.md`)

```
L5 Retrain ──challenger──► L2 Policy (skip/size) ──permit──► P2 ENGINE (26101817)
L1 Tape ──────────────────►        ▲
                                   │
                          L3 Guardrails (hard veto)
                                   ▲
                          L4 Observer (W15/W20 → W100/W250)
                                   │
                          L6 Ledger (all decisions)
L8 MAE/gap abort (primary · overnight) · L9 session quality · L10 HITL promote
```

**Invariant:** L3 outranks L1/L2/L4/L5/L8–L10.

### EURUSD M15 layer emphasis

| Layer | EURUSD M15 focus |
| --- | --- |
| **L1** | ATR vs 74 · session age 12–20 · DOW/hour · side · BBDev 2.3 · CD · spread · nights_held · optional Ouroboros MATCH/FRAGILE · streak |
| **L2det** | BUY caution · Thu · H13/H19 · Feb/Aug-like stress · near-ATR-cap · never skip all buys blindly |
| **L2 AI** | Avoid-loser on P2 fires only; pin `L2skip_eur_m15_*` |
| **L3** | MaxDD · Below-frontier f=0 · kill-switch · streak-aware halt · overnight DD path |
| **L4** | Small-n W15/W20 first; adopt W100/W250 when n allows |
| **L5** | Retrain on decay / Compressing; WF through decay, not only on it |
| **L6** | Full reason codes for CF scorecards |
| **L8** | **Primary** (overnight book); MAE abort / gap-open path advisor |
| **L9** | Late-session soft veto (H19) · spread tercile |
| **L10** | Only promotion path to “EURUSD M15 OS live research” |

---

## 4. Baseline lock (EURUSD-AOS-P0)

Import P2 health from scored logs / profile. **No OS code.**

| Field | Tip May→Oct 2026 | YTD Jan→Oct 2026 |
| --- | ---: | ---: |
| Magic / RR | **26101817** / 1.25 | same |
| n | **45** | 72 |
| WR | **46.7%** | 48.6% |
| E_N (des) | **+0.050R** | +0.094R |
| BM / EF_prior | +2.2 pp / **−0.7 pp** | +4.2 / +1.2 |
| Final Δ ($500) | **+$7.14** | +$20.91 |
| Max W / L streak | 3 / 4 | 4 / 5 |
| AOS | Off | Off |

**OS compare window (default):** **tip May→Oct** — state which on every task. YTD = support / L3 diagnostics. Tip alone may KEEP expansion OS trials; never sole production admission.

**Bad-cell registry:** [`aos_bad_cells.md`](./aos_bad_cells.md) (P0-T02).  
**Baseline packet:** [`EURUSD_AOS_BASELINE_v1.md`](./EURUSD_AOS_BASELINE_v1.md) (P0-T01).  
**Cost stub:** [`aos_cost_policy.md`](./aos_cost_policy.md) (P0-T03).

---

## 5. Iteration bar (loose on purpose)

**Accept** a layer experiment when **all** hold:

| Check | Bar |
| --- | --- |
| n remaining after skips | Report; no n≥385 floor (per EURUSD M15 edge_framework) |
| Tip-window E_N / EF | ≥ baseline − **1 pp** EF (or E_N hold if Leak pending) |
| MaxDD | ≤ baseline + **2 pp** |
| 90d fire count | ≥ 50% baseline (~10–15 / 90d) → else FREQUENCY_STALL **warn** |
| AL | Not worse unless E_N clearly improved |
| Bad-cell hit rate | Skips concentrated in registry cells (report precision/recall vs winners) |
| Protect cells | False-skip rate on SELL / Mon / Fri / H12 / Jul must be reported |

**Reject immediately** when:

- WR↑ but E_N↓ or EF↓  
- Layer invents entries / changes SL/TP/ATR max / BB / CD as “OS”  
- Re-enables P1 BBw or ATR≤68 without a new preset card  
- Higher layer overrides L3 halt  
- Uses M5 / AUD / UK100 / AAPL model pin on EURUSD M15  
- Permanently disables BUY because tip was sell-led  

**Promote (EURUSD-AOS-P7 only)** when: shadow CF beats/holds baseline · L3/L4 wired · ledger complete · HITL sign-off under `edge_framework.md`. Full G0–G5 for any live-capital claim — not for every weekly trial. Live capital stays on M5 Harvest until then.

---

## 6. Phase plan (task catalogue)

### PHASE 0 — ENGINE BASELINE LOCK (`EURUSD-AOS-P0`) — **DONE stubs** (measured Leak OPEN)

| Task | Layer | Deliverable | Status |
| --- | --- | --- | --- |
| **P0-T01** | — | Freeze `EURUSD_AOS_BASELINE_v1` scorecard (tip + YTD) | **DONE** 2026-10-18 |
| **P0-T02** | — | Bad-cell registry from profile | **DONE** 2026-10-18 |
| **P0-T03** | — | Cost policy + Leak prior stub; deal-measured still open | **DONE** prior 2026-10-18 · journal proxy **DONE** (P1) · measured **OPEN** |

### PHASE 1 — L1 PERCEPTION (`EURUSD-AOS-P1`) — **DONE** (T04 optional open)

| Task | Layer | Deliverable | Status |
| --- | --- | --- | --- |
| **P1-T01** | L1 | EURUSD M15 feature schema v0 (`aos_l1_tape_contract.md`) | **DONE** 2026-10-18 |
| **P1-T02** | L1 | Offline tape builder from Tester P2 fires / bars | **DONE** tip+YTD · `build_eurusd_m15_fire_tape.py` |
| **P1-T03** | L1 | Label fires: win/lose · DOW · hour · side · ATR · spread · nights · month tag | **DONE** tip 45 + YTD 72 · atr_missing=0 |
| **P1-T04** | L1 | Structure flags v0 (band-ride / failed fade) — optional | OPEN |
| **P1-T05** | L1 | Ouroboros MATCH/FRAGILE month flag (soft) | **DONE** tip MATCH 43 / FRAGILE 2 |

### PHASE 2 — L2 POLICY (`EURUSD-AOS-P2`) — **DONE**

| Task | Layer | Deliverable | Status |
| --- | --- | --- | --- |
| **P2-T01** | L2det | Parity: skip Tue + ATR max — OS mirror / no double-count | **DONE** PASS |
| **P2-T02** | L2det | SOFT skip map v1: Thu ± H13/H19 shadow CF | **DONE** — **ARM Thu** · H13 HOLD · H19 thin ARM |
| **P2-T03** | L2det | Buy-caution SOFT CF (never blanket BUY) | **DONE** — **ARM BUY∧near_atr** (+ BUY∧H13) · DISARM blanket BUY |
| **P2-T04** | L2det | Stress-month / near-ATR SOFT CF (Feb/Aug-like) | **DONE** — DISARM blanket near_atr · Aug HOLD · Feb YTD diag |
| **P2-T05** | L2size | Lifecycle → f table (spec; wire after L4) | **DONE** SPEC (`aos_l2_size_table.md`) |
| **P2-T06** | L2 AI | Train `L2skip_eur_m15` avoid-loser · shadow | **DONE** — **DISARM** (holdout) · SHADOW_ONLY pin |
| **P2-T07** | L2 AI | Stack CF vs P0 / L2det | **DONE** — best **v1b** Thu∨(BUY∧near_atr) |

### PHASE 3 — L3 + L4 (`EURUSD-AOS-P3`) — **DONE**

| Task | Layer | Deliverable | Status |
| --- | --- | --- | --- |
| **P3-T01** | L3 | MaxDD / kill / Below-frontier halt policy (overnight-aware) | **DONE** SIGNED · v1b tip trip-free |
| **P3-T02** | L3 | Cost-drift + FREQUENCY_STALL warn · streak | **DONE** SIGNED |
| **P3-T03** | L4 | Rolling health W15/W20 (+ W50 when wiring) | **DONE** paths in archive |
| **P3-T04** | L4→L3 | Recommend bus: Below → halt; Compressing → investigate | **DONE** SIGNED |

### PHASE 4 — LEDGER + STACK (`EURUSD-AOS-P4`) — **DONE**

| Task | Layer | Deliverable | Status |
| --- | --- | --- | --- |
| **P4-T01** | L6 | Decision ledger schema + offline writer | **DONE** (`aos_l6_ledger.md`) |
| **P4-T02** | stack | Det stack `L1+L2det+L3+L4+L6` shadow run | **DONE** tip E_N **0.234** · ret **69%** |
| **P4-T03** | stack | + L2 AI shadow on det fires | **DONE** DISARM · 5 shadow skips |
| **P4-T04** | L8 | MAE / gap abort advisor (shadow; **primary** for overnight book) | **DONE** 21 advise · 16 overnight · not armed |

### PHASE 5 — RETRAIN LOOP (`EURUSD-AOS-P5`) — **DONE**

| Task | Layer | Deliverable | Status |
| --- | --- | --- | --- |
| **P5-T01** | L5 | Retrain policy + model store layout `L2skip_eur_m15/` | **DONE** `aos_l5_retrain.md` · `train_l2_eurusd_m15.py` |
| **P5-T02** | L5 | Champ/challenger promote rules (shadow→candidate) | **DONE** AI challenger EMPTY · overlay L2det champ |
| **P5-T03** | L5 | Rollback drill | **DONE** `_drill/` pass |

### PHASE 6 — HARDENING (`EURUSD-AOS-P6`) — **DONE**

| Task | Layer | Deliverable | Status |
| --- | --- | --- | --- |
| **P6-T01** | L9 | Session-quality soft veto (H19 / spread tercile) | **DONE** H19 ARM_SOFT shadow · spread DISARM |
| **P6-T02** | G5-ish | ±10% bound stress on L2 thresholds (not SL/TP) | **DONE** keep 0.9/74 · do not loosen |
| **P6-T03** | — | Confirm ATR max declared for G3 when OS armed | **DONE** ATR max **74** on P2+P4 |

### PHASE 7 — PROMOTION (`EURUSD-AOS-P7`) — **DONE 2026-10-18 HITL**

| Task | Layer | Deliverable | Status |
| --- | --- | --- | --- |
| **P7-T01** | L10 | Promotion packet: CF · health · ledger · gates | **DONE** `promotion_packet.json` |
| **P7-T02** | L10 | HITL sign-off · research OS arm | **SIGNED** magic **26121807** · `AIOS_SIGNOFF.md` |
| **P7-T03** | — | Paper / tiny-f attach checklist | **DONE** in sign-off |

---

## 7. Weekly implementation table

Calendar assumes **Week 1 = week of 2026-10-20** (Mon). Slip tasks forward; do not skip P0 measured Leak / P1 to chase L2 AI. One primary task stream at a time; blotter clear-after-review applies.

| Week | Dates (2026) | Phase | Primary tasks | Exit criteria (done when) |
| ---: | --- | --- | --- | --- |
| **0** | Oct 18 | P0 | P0-T01 · P0-T02 · P0-T03 stub | Baseline + bad-cells + cost stub in `doc/assets/EURUSD/` |
| **1** | Oct 20–26 | P0→P1 | Deal export measured Leak · P1-T01 feature schema | `Leak_source=measured` on tip scorecard · schema reviewed |
| **2** | Oct 27–Nov 2 | P1 | P1-T02 tape builder · P1-T03 label fires | Offline tape covers tip+YTD fires · labels QA’d |
| **3** | Nov 3–9 | P1 | P1-T04 (opt) · P1-T05 Ouroboros flags | Tape v0 frozen |
| **4** | Nov 10–16 | P2 | P2-T01 ATR/Tue parity · P2-T02 Thu/H13·H19 SOFT shadow | CF ledger · E_N/EF vs baseline within bar **or** reject map |
| **5** | Nov 17–23 | P2 | P2-T03 buy-caution · P2-T04 stress-month map | Armed only if CF pass; else DISARMED |
| **6** | Nov 24–30 | P3 | P3-T01 L3 · P3-T02 stall/cost | Offline L3 trips on EURUSD path · policy md |
| **7** | Dec 1–7 | P3 | P3-T03 L4 health · P3-T04 bus | W15/W20 health CSV · Below→halt verified |
| **8** | Dec 8–14 | P4 | P4-T01 ledger · P4-T02 det stack shadow | Full det stack CF vs P0 |
| **9** | Dec 15–21 | P2/P4 | P2-T06 train `L2skip_eur_m15` · P2-T07 AI shadow CF | Model pin under `infra/artefacts/models/L2skip_eur_m15/` · shadow only |
| **10** | Dec 22–28 | P4 | P4-T03 AI+det · P4-T04 L8 shadow | Stack CF; L8 advise-only |
| **11** | Dec 29–Jan 4 | P5 | P5-T01…T03 retrain/rollback | Store + rollback drill documented |
| **12** | Jan 5–11 | P6 | P6-T01…T03 harden | Soft veto CF; ATR G3 note |
| **13** | Jan 12–18 | P7 | P7-T01 · P7-T02 HITL | KEEP OS research arm **or** stay shadow with named gaps |
| **14** | Jan 19–25 | buffer | Slip / re-runs · P7-T03 if armed | Clean archive; roadmap status update |

### Weekly operating rhythm

| Day | Action |
| --- | --- |
| Mon | Confirm week’s primary task · load P2 preset · note compare window (tip default) |
| Tue–Thu | Implement / run Tester / build tape or CF |
| Fri | Score under `edge_framework.md` · ACCEPT/REJECT · archive blotter · update this roadmap status |
| Ongoing | No M5/AUD/UK100 pin · no SL/TP “quick fix” · no P1 re-stack · Canvas display-only |

---

## 8. Preset / artifact naming

```text
Profiles/Tester/BMRG/EURUSD/EURUSD-AOS-P{phase}-T{task}_{layer}_{change}.set
blotter/archive/EURUSD-AOS-P{phase}-T{task}/
infra/artefacts/models/L2skip_eur_m15/LATEST/
doc/assets/EURUSD/aos_bad_cells.md
doc/assets/EURUSD/aos_cost_policy.md
doc/assets/EURUSD/EURUSD_AOS_BASELINE_v1.md
doc/assets/EURUSD/aos_l1_tape_contract.md   # from P1
doc/assets/EURUSD/aos_l2_policy.md          # from P2
```

Research OS magic: keep engine **26101817**; OS experiment magics in **2612xxxx** if a separate `.set` is required — never collide with M5 live (`8210xxx` / `8399xxx`) or AUD/UK100.

---

## 9. Scorecard fields (every weekly exit)

```text
framework_unified: 1.0
framework_eurusd_m15: 0.1.0
aos_task: EURUSD-AOS-P#-T##
preset_id / magic / window / n
aos_overlay: none | L2det | L2AI_shadow | L2AI_withhold | L3 | stack
baseline_ref: EURUSD_AOS_BASELINE_v1
WR, R, BWR, BM, Leak, Leak_source, EF, M, E_N, PF
skips_n, skip_precision_bad_cell, fire_retention_pct
false_skip_rate_on_SELL_or_MonFri_or_H12
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
| `EURUSD_AOS_BASELINE_v1.md` | Frozen P0 numbers |
| `aos_bad_cells.md` | L2det seed registry |
| `aos_cost_policy.md` | Leak / journal proxy · deal-export stub |
| `aos_l1_tape_contract.md` | L1 feature schema v0 |
| `aos_l2_policy.md` | L2det / L2AI ARM map (P2) |
| `aos_l2_size_table.md` | Lifecycle f multipliers (spec · P3 bus signed) |
| `aos_l3l4_policy.md` | L3 halt · L4 health · recommend bus (P3) |
| `aos_l6_ledger.md` | L6 schema · research OS preset · L8 advise (P4) |
| `aos_l5_retrain.md` | L5 retrain · champ/challenger · rollback (P5) |
| `aos_p6_harden.md` | L9 session · L2 ±10% stress · ATR G3 (P6) |
| `AIOS_SIGNOFF.md` | HITL research OS arm · magic **26121807** (P7) |
| `tapes/` | Tip / YTD / combined fire tapes v0 · tip ledger shadow |
| `doc/ai_OS.md` | Layer vocabulary |
| `blotter/archive/EURUSD-M15-P2/` | Engine review (pre-OS) |
| `blotter/archive/EURUSD-AOS-P1/` | Builder · COST_PROXY · TAPE_QA |
| `blotter/archive/EURUSD-AOS-P2/` | P2_CF · tip_l2ai_scored |
| `blotter/archive/EURUSD-AOS-P3/` | P3_L3L4 · health_path_*.csv |
| `blotter/archive/EURUSD-AOS-P4/` | P4_STACK · ledger_*.csv · research `.set` |
| `blotter/archive/EURUSD-AOS-P5/` | REVIEW · `_drill/` |
| `blotter/archive/EURUSD-AOS-P6/` | P6_HARDEN · run_p6_harden.py |
| `blotter/archive/EURUSD-AOS-P7/` | promotion_packet · P7 ARMED `.set` |
| `infra/artefacts/models/L2skip_eur_m15/` | AI shadow store · rollback CLI (DISARM) |

---

## 11. Versioning

- **0.1.0** — Initial EURUSD M15 AIOS plan; P0 stubs + P1 tapes (2026-10-18).  
- Bump when phase order, iteration bar, pin name, or baseline window changes.

---

## 12. One-line plan

**Freeze P2 light, measure Leak (swap-aware), build an EURUSD M15-native skip/size OS aimed at BUY/Thu/H13·H19/Feb·Aug cells, shadow until tip EF holds, then promote research OS only — never borrow foreign L2, never re-stack P1, never retune geometry as the first move, never replace live M5 Harvest.**

---

## 13. Status line (update Fridays)

```text
2026-10-18 | P7 HITL SIGNED | ARM_RESEARCH_OS magic 26121807 · L2det v1b · not M5 replace · stream P0-P7 closed
```
