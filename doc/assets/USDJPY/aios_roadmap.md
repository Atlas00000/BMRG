# USDJPY — AIOS Roadmap (M15 Balanced P0)

**Version:** 0.1.0  
**Status:** **P7 DONE / HITL SIGNED** — **USDJPYstack** · magic **26131807** · v1c LIVE_WITHHOLD · L2AI DISARM · measured Leak **OPEN**  






**Engine lock (OS baseline):** Balanced P0 · magic **26101828** · **AOS OFF**  
**Preset (engine):** `Profiles/Tester/BMRG/USDJPY/BMRG-M15-USDJPY-6M-P0_balanced_chart.set`  
**Research OS arm:** magic **26131807** · preset **`USDJPYstack.set`** · [`AIOS_SIGNOFF.md`](./AIOS_SIGNOFF.md) **HITL SIGNED**  
**Parents:** [`edge_framework.md`](./edge_framework.md) · [`system_profile.md`](./system_profile.md) · `doc/ai_OS.md` · `doc/unified_edge_framework.md`  
**Blotter:** `blotter/inbox/` → `blotter/archive/USDJPY-AOS-*/` after review  

**Not** EURUSD M5 aistack · **not** EURUSD M15 L2det · **not** UK100 L2det · **not** AUDUSD L2 pin · **not** a live replace.

---

## 0. Canvas caveat

| Artifact | Authority |
| --- | --- |
| This roadmap + scored blotters under `edge_framework.md` | **Normative** for USDJPY M15 AIOS work |
| `system_profile.md` | Evidence / descriptive |
| Canvas / chat charts / UI tiles | **Display only** |

Verdicts come from ledger + scorecard. Tip-only charts never promote a layer. Probe EF is never scored EF. Design alts (26101829 / 26101830) are context only — OS compares against **26101828**.

---

## 1. What this is / is not

| This is | This is not |
| --- | --- |
| A **USDJPY M15-owned AIOS** that permits / withholds / sizes / observes / adapts Balanced P0 | A new SL/TP or BBDev optimisation programme |
| Layered work with task IDs `USDJPY-AOS-P#-T##` | A replacement entry model or trend sleeve |
| Iteration vs a frozen P0 baseline | Immediate live attach or EUR/AUD/UK replace |
| Consumption of profile bad cells (Thu, H14, Jul, sell-volume without edge) | Re-ranking from profit / WR alone |
| Separate model store pin (`L2skip_usdjpy_*`) | Reuse of EUR / UK / AUD / AAPL L2 pins |
| Cost-first hygiene (Leak prior **11.4 pp** is the Stage-1 bottleneck) | Pretending probe WR 57.6% is the OS target |

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
Do **not** re-open Tokyo 02–12 or import EUR/GBPJPY SL floors.  
Do **not** claim Stage-1 Robust on Leak **prior** — measure first.

---

## 2. Working hypothesis (from USDJPY profile)

> Balanced P0 already has a real meanrev edge on the tip (May→Aug WR 48.2% / E_N +0.06R / +$6; YTD stronger at +0.13R / +$18).  
> Remaining leak is **conditional** plus **cost**: fires still occur in DOW / hour / calendar / side cells where BM ≤ 0 (Thu, H14, Jul), and sell-heavy fire count does not carry edge (buy-led expectancy). Tip EF under Leak **prior** is deeply negative (−8.6 pp) — **costs_fragile** until deals.  
> AI layers’ job: **withhold or size-down bad cells**, contain streak risk, keep **EF** alive after measured Leak — without rewriting the fade or borrowing foreign pins.

| Claim | Evidence | Stance for OS |
| --- | --- | --- |
| Edge exists | Tip Stage 0 · EXPANSION_KEEP/WATCH · E_N +0.061R | **Accept** — freeze as USDJPY-AOS-P0 |
| Weakness is conditional | Thu WR 31% · Jul 33% · H14 soft · sell n-heavy / WR≈BWR | **Accept** — L2 skip/size, don’t chase R |
| Buy-led expectancy | BUY tip WR 52% / E_N +0.15R · SELL ≈BWR | **Accept** — sell-caution SOFT only; never permanent AllowSell=false |
| ATR max already filters FRAGILE | Gate ON · Sep = 0 fires | **Accept** — L1 feature; do not lift ATR max as OS “fix” |
| Session-bound holds | Med win ~1.2h · hold≥12h ~8–11% | **Accept** — L8 **secondary** (vs EUR overnight primary) |
| Dense tip fire rate | ~14 trades / 30d | **Accept** — small-n W15/W20; FREQUENCY_STALL vs tip baseline |
| High Leak prior vs thin BM | 11.4 pp vs BM +2.8 pp | **Accept** — measure Leak before arming hard L2; costs_fragile footnote |
| Fixing via SL/TP / Tokyo first | Would reopen geometry / failed probe | **Reject as first move** |
| Borrow EUR / UK / AUD L2 | Wrong book / session / side fingerprint | **Reject** — USDJPY pin only |
| Probe WR 57.6% as OS target | Design prior only | **Reject** — beat Tester tip EF/E_N |

---

## 3. Architecture (same layers as `doc/ai_OS.md`)

```
L5 Retrain ──challenger──► L2 Policy (skip/size) ──permit──► P0 ENGINE (26101828)
L1 Tape ──────────────────►        ▲
                                   │
                          L3 Guardrails (hard veto)
                                   ▲
                          L4 Observer (W15/W20 → W100/W250)
                                   │
                          L6 Ledger (all decisions)
L8 MAE abort (secondary · session book) · L9 session quality · L10 HITL promote
```

**Invariant:** L3 outranks L1/L2/L4/L5/L8–L10.

### USDJPY M15 layer emphasis

| Layer | USDJPY M15 focus |
| --- | --- |
| **L1** | ATR vs 70 · session age 12–20 · DOW/hour · side · BBDev 2.2 · CD · spread · nights_held (rare) · Ouroboros MATCH/FRAGILE · streak |
| **L2det** | **Armed:** near_atr · H16 · **v1c=near_atr∨H16** · SELL∧near_atr · **HOLD:** Jul · H14 · **DISARM:** Thu · never blanket SELL/BUY |
| **L2 AI** | `L2skip_usdjpy_*` SHADOW_ONLY until clean pre-tip train |
| **L3** | MaxDD 25 · derisk 20 · BELOW latch · streak-aware (tip max L=7) — **SIGNED P3** |
| **L4** | W15/W20 health · W50 when wiring · BELOW→halt · COMPRESSING→investigate — **SIGNED P3** |
| **L5** | Retrain store `L2skip_usdjpy/` · promote gates · rollback drill — **SIGNED P5** · AI DISARM |
| **L6** | Decision ledger · offline writer — **SIGNED P4** |
| **L8** | **Secondary** session MAE advise-only (9/9 losers tip) — **SIGNED P4** · not armed |
| **L9** | H14 DISARM · spread HOLD (low variance) · Jul HOLD — **SIGNED P6** · not LIVE |
| **L10** | HITL **SIGNED** — research OS **USDJPYstack** / **26131807** — not production admit |

---

## 4. Baseline lock (USDJPY-AOS-P0)

Import Balanced health from scored logs / profile. **No OS code.**

| Field | Tip May→Aug 2026 | YTD Jan→Oct 2026 | Prior Jan→Apr 2026 |
| --- | ---: | ---: | ---: |
| Magic / RR | **26101828** / 1.20 | same | same |
| n | **56** | 68 | 8 (footnote) |
| WR | **48.2%** | 51.5% | 50.0% |
| E_N (des) | **+0.061R** | +0.132R | +0.100R |
| BM / EF_prior | +2.8 pp / **−8.6 pp** | +6.0 / −5.4 | +4.5 / −6.9 |
| Final Δ ($500) | **+$5.99** | +$17.99 | +$1.20 |
| Max W / L streak | 3 / **7** | 5 / 7 | 3 / 3 |
| AOS | Off | Off | Off |

**OS compare window (default):** **tip May→Aug** — state which on every task. YTD = support / L3 diagnostics. Prior n=8 never sole KEEP. Tip alone may KEEP expansion OS trials; never sole production admission.

**Bad-cell registry:** [`aos_bad_cells.md`](./aos_bad_cells.md) (P0-T02).  
**Baseline packet:** [`USDJPY_AOS_BASELINE_v1.md`](./USDJPY_AOS_BASELINE_v1.md) (P0-T01).  
**Cost stub:** [`aos_cost_policy.md`](./aos_cost_policy.md) (P0-T03).

---

## 5. Iteration bar (loose on purpose)

**Accept** a layer experiment when **all** hold:

| Check | Bar |
| --- | --- |
| n remaining after skips | Report; no n≥385 floor (per USDJPY edge_framework) |
| Tip-window E_N / EF | ≥ baseline − **1 pp** EF (or E_N hold if Leak pending) |
| MaxDD | ≤ baseline + **2 pp** |
| 90d fire count | ≥ 50% tip baseline (~18–22 / 90d) → else FREQUENCY_STALL **warn** |
| AL | Not worse unless E_N clearly improved |
| Bad-cell hit rate | Skips concentrated in registry cells (report precision/recall vs winners) |
| Protect cells | False-skip rate on **BUY / Mon / Fri / H15 / H18–19 / May–Jun** must be reported |

**Reject immediately** when:

- WR↑ but E_N↓ or EF↓  
- Layer invents entries / changes SL/TP/ATR max / BB / session as “OS”  
- Re-opens Tokyo 02–12 or imports EUR 300 / GBPJPY 160 SL without a new preset card  
- Higher layer overrides L3 halt  
- Uses EUR / UK / AUD / AAPL model pin on USDJPY  
- Permanently disables SELL because tip was buy-led on expectancy  
- Claims Robust / production on Leak **prior** alone  

**Promote (USDJPY-AOS-P7 only)** when: shadow CF beats/holds baseline · L3/L4 wired · ledger complete · HITL sign-off under `edge_framework.md`. Full G0–G5 for any live-capital claim — not for every weekly trial. Live capital stays off USDJPY until then.

---

## 6. Phase plan (task catalogue)

### PHASE 0 — ENGINE BASELINE LOCK (`USDJPY-AOS-P0`) — **STUBS DONE** (measured Leak OPEN)

| Task | Layer | Deliverable | Status |
| --- | --- | --- | --- |
| **P0-T01** | — | Freeze `USDJPY_AOS_BASELINE_v1` scorecard (tip + YTD + prior footnote) | **DONE** 2026-10-19 |
| **P0-T02** | — | Bad-cell registry from profile | **DONE** 2026-10-19 |
| **P0-T03** | — | Cost policy + Leak prior stub; deal-measured still open | **DONE** prior 2026-10-19 · measured **OPEN** |

### PHASE 1 — L1 PERCEPTION (`USDJPY-AOS-P1`) — **DONE** (T04 optional open)

| Task | Layer | Deliverable | Status |
| --- | --- | --- | --- |
| **P1-T01** | L1 | USDJPY M15 feature schema v0 (`aos_l1_tape_contract.md`) | **DONE** 2026-10-19 |
| **P1-T02** | L1 | Offline tape builder from Tester P0 fires / bars | **DONE** tip+YTD+long from 2025.01→2026.10.18 |
| **P1-T03** | L1 | Label fires: win/lose · DOW · hour · side · ATR · spread · nights · month tag | **DONE** tip 46 + YTD 54 · atr_missing=0 |
| **P1-T04** | L1 | Structure flags v0 (band-ride / failed fade) — optional | OPEN |
| **P1-T05** | L1 | Ouroboros MATCH/FRAGILE month flag (soft) | **DONE** on tape columns |

### PHASE 2 — L2 POLICY (`USDJPY-AOS-P2`) — **DONE**

| Task | Layer | Deliverable | Status |
| --- | --- | --- | --- |
| **P2-T01** | L2det | Parity: skip Tue + ATR max — OS mirror / no double-count | **DONE** PASS (Tue=0 · atr>70=0) |
| **P2-T02** | L2det | SOFT skip map v1: Thu ± H14 shadow CF | **DONE** Thu DISARM · H14 HOLD · H16 ARM_SOFT |
| **P2-T03** | L2det | Sell-caution SOFT CF (never blanket SELL) | **DONE** SELL∧near_atr ARM_SOFT · blanket REJECT |
| **P2-T04** | L2det | Stress-month / near-ATR SOFT CF (Jul-like) | **DONE** near_atr ARM · Jul HOLD · **v1c ARM** |
| **P2-T05** | L2size | Lifecycle → f table (spec; wire after L4) | **DONE** SPEC `aos_l2_size_table.md` |
| **P2-T06** | L2 AI | Train `L2skip_usdjpy` avoid-loser · shadow | **DONE** SHADOW_ONLY (train overlap tip) |
| **P2-T07** | L2 AI | Stack CF vs P0 / L2det | **DONE** preferred **v1c** ΔE_N +0.268 · ret 80% |

### PHASE 3 — L3 + L4 (`USDJPY-AOS-P3`) — **DONE**

| Task | Layer | Deliverable | Status |
| --- | --- | --- | --- |
| **P3-T01** | L3 | MaxDD / kill / Below-frontier halt policy (streak-aware) | **DONE** · v1c tip+YTD trip-free · P0 BELOW latch |
| **P3-T02** | L3 | Cost-drift + FREQUENCY_STALL warn · streak | **DONE** |
| **P3-T03** | L4 | Rolling health W15/W20 (+ W50 when wiring) | **DONE** · `health_path_*.csv` |
| **P3-T04** | L4→L3 | Recommend bus: Below → halt; Compressing → investigate | **DONE** · `aos_l3l4_policy.md` |

### PHASE 4 — LEDGER + STACK (`USDJPY-AOS-P4`) — **DONE**

| Task | Layer | Deliverable | Status |
| --- | --- | --- | --- |
| **P4-T01** | L6 | Decision ledger schema + offline writer | **DONE** · `aos_l6_ledger.md` |
| **P4-T02** | stack | Det stack `L1+L2det+L3+L4+L6` shadow run | **DONE** · v1c E_N +0.37 · 0 L3 halt |
| **P4-T03** | stack | + L2 AI shadow on det fires | **DONE** · SHADOW_ONLY n=9 |
| **P4-T04** | L8 | MAE abort advisor (shadow; **secondary** for session book) | **DONE** · 9/9 losers · not armed |

### PHASE 5 — RETRAIN LOOP (`USDJPY-AOS-P5`) — **DONE**

| Task | Layer | Deliverable | Status |
| --- | --- | --- | --- |
| **P5-T01** | L5 | Retrain policy + model store layout `L2skip_usdjpy/` | **DONE** · `train_l2_usdjpy.py` · pre-n=14 |
| **P5-T02** | L5 | Champ/challenger promote rules (shadow→candidate) | **DONE** · CHALLENGER EMPTY (AUC 0.47) |
| **P5-T03** | L5 | Rollback drill | **DONE** · `_drill/*/DRILL_REPORT.json` pass |

### PHASE 6 — HARDENING (`USDJPY-AOS-P6`) — **DONE**

| Task | Layer | Deliverable | Status |
| --- | --- | --- | --- |
| **P6-T01** | L9 | Session-quality soft veto (H14 / spread tercile) | **DONE** · no LIVE · H14 DISARM · spread HOLD |
| **P6-T02** | G5-ish | ±10% bound stress on L2 thresholds (not SL/TP) | **DONE** · PASS_WITH_NOTES · keep 0.9/70+H16 |
| **P6-T03** | — | Confirm ATR max declared for G3 when OS armed | **DONE** · ATR max **70** on P0+P4 |

### PHASE 7 — PROMOTION (`USDJPY-AOS-P7`) — **DONE / HITL SIGNED**

| Task | Layer | Deliverable | Status |
| --- | --- | --- | --- |
| **P7-T01** | L10 | Promotion packet: CF · health · ledger · gates | **DONE** · `promotion_packet.json` |
| **P7-T02** | L10 | HITL sign-off · research OS arm | **SIGNED** · **USDJPYstack** · magic **26131807** |
| **P7-T03** | — | Paper / tiny-f attach checklist | **DONE** · in `AIOS_SIGNOFF.md` |

---

## 7. Weekly implementation table

Calendar assumes **Week 0 = 2026-10-19** (P0 stubs) · **Week 1 = week of 2026-10-20** (Mon). Slip tasks forward; do not skip measured Leak / P1 to chase L2 AI. One primary task stream at a time; blotter clear-after-review applies.

| Week | Dates (2026) | Phase | Primary tasks | Exit criteria (done when) |
| ---: | --- | --- | --- | --- |
| **0** | Oct 19 | P0 | P0-T01 · P0-T02 · P0-T03 stub | Baseline + bad-cells + cost stub in `doc/assets/USDJPY/` |
| **1** | Oct 20–26 | P0→P1 | Deal export measured Leak · P1-T01 feature schema | `Leak_source=measured` on tip scorecard · schema reviewed |
| **2** | Oct 27–Nov 2 | P1 | P1-T02 tape builder · P1-T03 label fires | Offline tape covers tip+YTD fires · labels QA’d |
| **3** | Nov 3–9 | P1 | P1-T04 (opt) · P1-T05 Ouroboros flags | Tape v0 frozen |
| **4** | Nov 10–16 | P2 | P2-T01 ATR/Tue parity · P2-T02 Thu/H14 SOFT shadow | CF ledger · E_N/EF vs baseline within bar **or** reject map |
| **5** | Nov 17–23 | P2 | P2-T03 sell-caution · P2-T04 stress-month map | Armed only if CF pass; else DISARMED |
| **6** | Nov 24–30 | P3 | P3-T01 L3 · P3-T02 stall/cost | Offline L3 trips on USDJPY path · policy md |
| **7** | Dec 1–7 | P3 | P3-T03 L4 health · P3-T04 bus | W15/W20 health CSV · Below→halt verified |
| **8** | Dec 8–14 | P4 | P4-T01 ledger · P4-T02 det stack shadow | Full det stack CF vs P0 |
| **9** | Dec 15–21 | P2/P4 | P2-T06 train `L2skip_usdjpy` · P2-T07 AI shadow CF | Model pin under `infra/artefacts/models/L2skip_usdjpy/` · shadow only |
| **10** | Dec 22–28 | P4 | P4-T03 AI+det · P4-T04 L8 shadow | Stack CF; L8 advise-only |
| **11** | Dec 29–Jan 4 | P5 | P5-T01…T03 retrain/rollback | Store + rollback drill documented |
| **12** | Jan 5–11 | P6 | P6-T01…T03 harden | Soft veto CF; ATR G3 note |
| **13** | Jan 12–18 | P7 | P7-T01 · P7-T02 HITL | KEEP OS research arm **or** stay shadow with named gaps |
| **14** | Jan 19–25 | buffer | Slip / re-runs · P7-T03 if armed | Clean archive; roadmap status update |

### Weekly operating rhythm

| Day | Action |
| --- | --- |
| Mon | Confirm week’s primary task · load P0 preset · note compare window (tip default) |
| Tue–Thu | Implement / run Tester / build tape or CF |
| Fri | Score under `edge_framework.md` · ACCEPT/REJECT · archive blotter · update this roadmap status |
| Ongoing | No EUR/UK/AUD pin · no SL/TP “quick fix” · no Tokyo reopen · Canvas display-only |

---

## 8. Preset / artifact naming

```text
Profiles/Tester/BMRG/USDJPY/USDJPY-AOS-P{phase}-T{task}_{layer}_{change}.set
blotter/archive/USDJPY-AOS-P{phase}-T{task}/
infra/artefacts/models/L2skip_usdjpy/LATEST/
doc/assets/USDJPY/aos_bad_cells.md
doc/assets/USDJPY/aos_cost_policy.md
doc/assets/USDJPY/USDJPY_AOS_BASELINE_v1.md
doc/assets/USDJPY/aos_l1_tape_contract.md   # from P1
doc/assets/USDJPY/aos_l2_policy.md          # from P2
doc/assets/USDJPY/aos_l3l4_policy.md        # from P3
doc/assets/USDJPY/aos_l6_ledger.md          # from P4
Presets/BMRG-M15-USDJPY-6M-P4_research_OS_W50.set  # magic 26131804
doc/assets/USDJPY/aos_l5_retrain.md         # from P5
infra/artefacts/models/L2skip_usdjpy/       # store + rollback
doc/assets/USDJPY/aos_p6_harden.md          # from P6
doc/assets/USDJPY/AIOS_SIGNOFF.md           # from P7
Presets/USDJPYstack.set                     # magic 26131807 HITL
Include/AOS_L2det_usdjpy.mqh                # v1c MQH
```

Research OS magic: keep engine **26101828**; OS experiment magics in **2613xxxx** (target arm **26131807**) — never collide with EUR (`2612xxxx` / `8210xxx`) or UK (`2611xxxx`) or AUD live.

---

## 9. Scorecard fields (every weekly exit)

```text
framework_unified: 1.0
framework_usdjpy: 0.1.0
aos_task: USDJPY-AOS-P#-T##
preset_id / magic / window / n
aos_overlay: none | L2det | L2AI_shadow | L2AI_withhold | L3 | stack
baseline_ref: USDJPY_AOS_BASELINE_v1
WR, R, BWR, BM, Leak, Leak_source, EF, M, E_N, PF
skips_n, skip_precision_bad_cell, fire_retention_pct
false_skip_rate_on_BUY_or_MonFri_or_H15_H18H19
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
| `USDJPY_AOS_BASELINE_v1.md` | Frozen P0 numbers |
| `aos_bad_cells.md` | L2det seed registry |
| `aos_cost_policy.md` | Leak / deal-export stub |
| `aos_l1_tape_contract.md` | L1 feature schema v0 (P1-T01) |
| `tapes/` | Tip / YTD fire tapes (after re-smoke) |
| `aos_l2_policy.md` | L2det / L2AI ARM map (from P2) |
| `aos_l3l4_policy.md` | L3 halt + L4 health bus (from P3) |
| `aos_l6_ledger.md` | L6 ledger + stack CF (from P4) |
| `aos_l5_retrain.md` | L5 retrain / champ–challenger / rollback (from P5) |
| `aos_p6_harden.md` | L9 / L2 stress / ATR G3 (from P6) |
| `AIOS_SIGNOFF.md` | HITL **SIGNED** — **USDJPYstack** / **26131807** |
| `doc/ai_OS.md` | Layer vocabulary |
| `blotter/archive/USDJPY-P0-CHART/` | Engine review (pre-OS) |
| `infra/artefacts/models/L2skip_usdjpy/` | AI shadow store (future) |

---

## 11. Versioning

- **0.1.0** — Initial USDJPY AIOS plan from profile/edge thesis; P0-T01…T03 stubs landed; weekly calendar from 2026-10-19/20.  
- Bump when phase order, iteration bar, pin name, or baseline window changes.

---

## 12. One-line plan

**Freeze Balanced P0, measure Leak (costs_fragile first), build a USDJPY-native skip/size OS aimed at Thu/H14/Jul/sell-volume cells while protecting buy-led tip stars, shadow until tip EF holds after honest costs, then promote research OS only — never borrow foreign L2, never retune yen geometry as the first move, never replace live FX books.**

---

## 13. Status line (update Fridays)

```text
2026-10-19 | P7 HITL SIGNED | USDJPYstack · magic 26131807 · v1c LIVE_WITHHOLD · L2AI DISARM · Leak prior · stream CLOSED
```
