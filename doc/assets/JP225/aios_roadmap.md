# JP225 / JPN225 — AIOS Roadmap (M15 Growth P1)

**Version:** 0.1.7  
**Status:** **P7 COMPLETE / HITL SIGNED** — research OS **ARMED** · magic **26151907** · preset **`JPN225stack`** · MQH `AOS_L2det_jp.mqh`  
**Engine lock (OS baseline):** Growth P1 wrLift fade · magic **26101904** · **AOS OFF**  
**Preset (engine):** `Profiles/Tester/BMRG/JP225/BMRG-M15-JP225-6M-P1_wrLift_fade_chart.set`  
**Research OS arm:** magic **26151907** · **`JPN225stack.set`** · [`AIOS_SIGNOFF.md`](./AIOS_SIGNOFF.md)  
**Parents:** [`edge_framework.md`](./edge_framework.md) · [`system_profile.md`](./system_profile.md) · `doc/ai_OS.md` · `doc/unified_edge_framework.md`  
**Blotter:** `blotter/inbox/` → `blotter/archive/JP225-AOS-*/` after review  
**Engine review:** `blotter/archive/JP225-P1-REVIEW/`

**Not** EURUSD / AUDUSD / UK100 / DE40 / USDJPY L2 pins · **not** a live replace · **not** SL/TP re-optimisation · **not** P1.5 as silent baseline mutate (re-freeze if promoted).

---

## 0. Canvas caveat

| Artifact | Authority |
| --- | --- |
| This roadmap + scored blotters under `edge_framework.md` | **Normative** for JP225 / JPN225 AIOS work |
| `system_profile.md` | Evidence / descriptive |
| Canvas / chat charts / UI tiles | **Display only** |

Verdicts come from ledger + scorecard. Tip-only charts never promote a layer. Probe EF is never scored EF. P0 (26101903) and P1.5 (26101905) are context / alts — OS compares against **26101904** until a formal re-freeze.

---

## 1. What this is / is not

| This is | This is not |
| --- | --- |
| A **JP225-owned AIOS** that permits / withholds / sizes / observes / adapts Growth P1 | A new SL/TP / BBDev / Fade programme |
| Layered work with task IDs `JP225-AOS-P#-T##` | A replacement entry model or trend sleeve |
| Iteration vs a frozen P1 baseline | Immediate live attach or FX/EU-index replace |
| Consumption of profile bad cells (May FRAGILE, Jul/Oct MISMATCH, tip OFFHOME mix) | Re-ranking from profit / WR alone |
| Separate model store pin (`L2skip_jp225_*` / `L2det_jp225_*`) | Reuse of EUR / UK / DE40 / AUD / AAPL / USDJPY L2 pins |
| Regime-first hygiene (MATCH tip already healthy; aggregate tip EF≤0) | Pretending probe WR 47% is the OS target · DROP on MISMATCH months |

**Frozen OS objective:**

```
maximise E_N
subject to  tip EF → > 0 after Leak (primary mission while Stage-1 fails)
            EF hold vs baseline (−1 pp once tip EF clears)
            MaxDD ≤ baseline MaxDD + 2 pp
never maximise WR, PF, or BM alone
never invent entries — only gate the engine fade
```

**Investigation order (unchanged):** data → execution → regime → structure.  
Do **not** touch SL/TP/BBDev/ATR max/Cooldown/Fade as the first OS move.  
Do **not** thin SL under fat Nikkei spread (~2300 pts).  
Do **not** claim Stage-1 Robust on Leak **prior** alone — measure first.  
Do **not** reject the asset solely on May/Jul/Oct regime tax.

---

## 2. Working hypothesis (from JP225 P1 review)

> Growth geometry is **sound** (SL 23260 / TP 34890 · RR 1.50 · realised R=1.50 · tp_lt_sl=0). Fat spread forces Growth RR; Balanced/Harvest fail Leak at design.  
> P1 fade + BB 2.3 only lifted tip WR **42.4% → 43.0%** — still Stage-1 fail (EF_prior **−1.3 pp**).  
> Remaining leak is **conditional / regime**: MATCH months (Aug WR 52% · Sep 50%) print EF **+5.7…+7.9 pp**; OFFHOME tip slice (May FRAGILE + Jul MISMATCH) sits WR **~39%** / EF **−5.0 pp**. Jun FRAGILE still pays — do not blanket-kill FRAGILE.  
> AI layers’ job: **withhold or size-down regime-hostile fires**, protect Aug/Sep MATCH stars (+ Jun when it pays), lift tip **EF through Leak**, contain long-path alternating months — without rewriting the fade or borrowing foreign pins.

| Claim | Evidence | Stance for OS |
| --- | --- | --- |
| Geometry OK | R=1.50 exact · tp_lt_sl=0 · TP>SL frozen | **Accept** — freeze geometry |
| Edge exists on-home | MATCH Aug/Sep WR ~50–52% · EF +5.7…+7.9 pp | **Accept** — protect cells |
| Tip Stage-1 fails | Tip WR 43.0% · EF −1.3 pp · n=79 | **Accept** — OS primary = clear tip EF |
| Weakness is regime mix | May 30% · Jul 31% · Oct 33% vs Aug 52% | **Accept** — L2 skip/size, don’t chase R |
| Jun FRAGILE can pay | Jun WR 55% · EF +10.7 pp | **Accept** — never blanket FRAGILE skip |
| ATR max already filters HV | Gate ON · p75 19670 | **Accept** — L1 feature; do not lift as OS “fix” |
| Fade did not clear Leak | P1 vs P0 +0.6 pp WR only | **Accept** — OS next, not more fade knobs first |
| Fat spread / fat SL | Spread≈2300 · SL 23260 · Leak prior ~4.3 pp | **Accept** — measure Leak; never thin SL |
| Probe overstated WR | Probe ~47% vs blotter 43% | **Reject** probe as OS target |
| Borrow DE40 / UK / EUR L2 | Wrong book / session / cost fingerprint | **Reject** — JP225 pin only |
| DROP on MISMATCH months | Jul/Oct tax expected | **Reject** — regime tax, not class death |
| Live replace incumbents | Expansion list only | **Reject** |

---

## 3. Architecture (same layers as `doc/ai_OS.md`)

```
L5 Retrain ──challenger──► L2 Policy (skip/size) ──permit──► P1 ENGINE (26101904)
L1 Tape ──────────────────►        ▲
                                   │
                          L3 Guardrails (hard veto)
                                   ▲
                          L4 Observer (W15/W20 → W100/W250)
                                   │
                          L6 Ledger (all decisions)
L8 MAE abort (secondary · cash/index sleeve) · L9 session quality · L10 HITL promote
```

**Invariant:** L3 outranks L1/L2/L4/L5/L8–L10.

### JP225 / JPN225 layer emphasis

| Layer | JP225 focus |
| --- | --- |
| **L1** | ATR vs 19670 · session age 08–17 · DOW/hour · side · BBDev 2.3 · FadeConfirm · CD · spread vs 3000 · Ouroboros MATCH/MISMATCH/FRAGILE · streak |
| **L2det** | May-FRAGILE · Jul MISMATCH · **Wed** · H08/H09/H14 · SELL∧cell · **never** blanket Jun/near_atr/SELL · **never** blanket Aug/Sep MATCH |
| **L2 AI** | Avoid-loser on P1 fires only; pin `L2skip_jp225_*` |
| **L3** | MaxDD · Below-frontier f=0 · kill-switch · streak-aware halt · path through OFFHOME clusters |
| **L4** | Small-n W15/W20 first; tip n≈79 → adopt W50/W100 when n allows |
| **L5** | Retrain on decay / Compressing; WF through MISMATCH, not only on it |
| **L6** | Full reason codes for CF scorecards |
| **L8** | **Secondary** (cash-sleeve index); MAE abort advise-only until overnight share known |
| **L9** | London open soft veto · spread tercile vs MaxSpread 3000 · Tue already hard-off |
| **L10** | Only promotion path to “JP225 OS live research” |

---

## 4. Baseline lock (JP225-AOS-P0)

Import Growth P1 health from scored log. **No OS code in P0.**

| Field | Tip May→Aug 2026 | Jan→Aug 2026 | Long 2025.01→2026.10 |
| --- | ---: | ---: | ---: |
| Magic / RR | **26101904** / 1.50 | same | same |
| n | **79** | 143 | 360 |
| WR | **43.0%** | 42.0% | 41.7% |
| E_N (des R=1.50) | **+0.076R** | +0.049R | +0.042R |
| BM / EF_prior | +3.0 pp / **−1.3 pp** | +2.0 / −2.3 | +1.7 / −2.6 |
| Final Δ ($500) | **+$9.28** | +$17.18 | +$22.14 |
| AOS | Off | Off | Off |

**MATCH-only (tip Aug):** n=23 · WR **52.2%** · EF **+7.9 pp** · E_N **+0.304R** — home proof.  
**OFFHOME tip (May+Jul):** drag that keeps aggregate Stage-1 ≤0.

**OS compare window (default):** **tip May→Aug** — state which on every task. Long = support / L3 diagnostics. MATCH-only = diagnostic protect-cell metric, never sole production admission. Incomplete Oct MISMATCH = footnote.

**P0 contrast (context, not baseline):** tip magic 26101903 · n=99 · WR 42.4% · EF −1.9 pp.  
**P1.5 light (alt engine):** magic **26101905** — if tip clears Stage 1 with AOS OFF, **re-freeze** baseline before OS spend.

**Bad-cell registry:** [`aos_bad_cells.md`](./aos_bad_cells.md) (P0-T02).  
**Baseline packet:** [`JP225_AOS_BASELINE_v1.md`](./JP225_AOS_BASELINE_v1.md) (P0-T01).  
**Cost stub:** [`aos_cost_policy.md`](./aos_cost_policy.md) (P0-T03).

---

## 5. Iteration bar (loose on purpose)

**Accept** a layer experiment when **all** hold:

| Check | Bar |
| --- | --- |
| n remaining after skips | Report; no n≥385 floor (expansion) |
| Tip-window E_N / EF | Prefer tip **EF > 0** after Leak; else ≥ baseline − **1 pp** EF (or E_N hold if Leak pending) |
| MaxDD | ≤ baseline + **2 pp** |
| 90d fire count | ≥ 50% tip baseline (~35–40 / 90d from ~20 / 30d) → else FREQUENCY_STALL **warn** |
| AL | Not worse unless E_N clearly improved |
| Bad-cell hit rate | Skips concentrated in registry cells (report precision/recall vs winners) |
| Protect cells | False-skip rate on **Aug / Sep MATCH / Jun-when-paying** must be reported |

**Reject immediately** when:

- WR↑ but E_N↓ or EF↓  
- Layer invents entries / changes SL/TP/ATR max / BB / Fade / session as “OS”  
- Thins SL below ~23260 or lifts MaxSpread as a Leak “fix”  
- Higher layer overrides L3 halt  
- Uses EUR / UK / DE40 / AUD / USDJPY / AAPL model pin on JPN225  
- Blanket-skips all FRAGILE (kills Jun) or all MATCH (kills home)  
- Claims Robust / production on Leak **prior** alone  
- Rejects asset solely on Jul/Oct MISMATCH or May FRAGILE  
- Promotes live replace of UK100 / DE40 / FX books  

**Promote (JP225-AOS-P7 only)** when: tip EF>0 after honest costs · shadow CF beats/holds baseline · L3/L4 wired · ledger complete · HITL sign-off under `edge_framework.md`. Full G0–G5 for any live-capital claim. Live capital stays off JP225 until then.

---

## 6. Phase plan (task catalogue)

### PHASE 0 — ENGINE BASELINE LOCK (`JP225-AOS-P0`) — **DONE** (measured Leak CLOSED)

| Task | Layer | Deliverable | Status |
| --- | --- | --- | --- |
| **P0-T01** | — | Freeze `JP225_AOS_BASELINE_v1` scorecard (tip + Jan–Aug + long footnote) | **DONE** 2026-10-19 |
| **P0-T02** | — | Bad-cell registry from P1 review / regime map | **DONE** 2026-10-19 |
| **P0-T03** | — | Cost policy + Leak prior stub → **measured** | **DONE** 2026-10-19 · `JP225-AOS-LEAK` · **2.45 pp** |

### PHASE 1 — L1 PERCEPTION (`JP225-AOS-P1`) — **DONE** 2026-10-19 (T04 optional OPEN)

| Task | Layer | Deliverable | Status |
| --- | --- | --- | --- |
| **P1-T01** | L1 | JP225 M15 feature schema v0 (`aos_l1_tape_contract.md`) | **DONE** 2026-10-19 |
| **P1-T02** | L1 | Offline tape builder from Tester P1 fires / bars | **DONE** · `build_jp225_m15_fire_tape.py` |
| **P1-T03** | L1 | Label fires: win/lose · DOW · hour · side · ATR · spread · month · HALT | **DONE** tip79 + janaug143 + long360 |
| **P1-T04** | L1 | Structure flags v0 (band-ride / failed fade) — optional | OPEN |
| **P1-T05** | L1 | Ouroboros MATCH/MISMATCH/FRAGILE month flag (soft) | **DONE** on tape columns |

### PHASE 2 — L2 POLICY (`JP225-AOS-P2`) — **DONE** 2026-10-19

| Task | Layer | Deliverable | Status |
| --- | --- | --- | --- |
| **P2-T01** | L2det | Parity: skip Tue + ATR max + Fade — OS mirror / no double-count | **DONE** PASS |
| **P2-T02** | L2det | SOFT skip map v1: May-FRAGILE ± Wed shadow CF (protect Jun) | **DONE** — ARM May · HOLD Wed |
| **P2-T03** | L2det | MISMATCH Jul ± H14/H08 SOFT CF (protect Aug/Sep · H13/H15) | **DONE** — ARM Jul · ARM May∨Jul · HOLD H14 |
| **P2-T04** | L2det | SELL∧bad-cell conjunction CF (never blanket SELL; near_atr alone = HOLD) | **DONE** — ARM SELL∧May · DISARM near_atr |
| **P2-T05** | L2size | Lifecycle → f table (spec; wire after L4) | **DONE** SPEC |
| **P2-T06** | L2 AI | Train `L2skip_jp225` avoid-loser · shadow | **DONE** — **DISARM** AUC≈0.49 |
| **P2-T07** | L2 AI | Stack CF vs P1 / L2det | **DONE** — best arm **May∨Jul** · see `aos_l2_policy.md` |

### PHASE 3 — L3 + L4 (`JP225-AOS-P3`) — **DONE** 2026-10-19

| Task | Layer | Deliverable | Status |
| --- | --- | --- | --- |
| **P3-T01** | L3 | MaxDD / kill / Below-frontier halt policy (OFFHOME-path aware) | **DONE** — see `aos_l3l4_policy.md` |
| **P3-T02** | L3 | Cost-drift + FREQUENCY_STALL warn · streak | **DONE** — stall WARN on May∨Jul expected |
| **P3-T03** | L4 | Rolling health W15/W20 (+ W50 when wiring) | **DONE** · `health_path_*.csv` |
| **P3-T04** | L4→L3 | Recommend bus: Below → halt; Compressing → investigate | **DONE** |

### PHASE 4 — LEDGER + STACK (`JP225-AOS-P4`) — **DONE** 2026-10-19 (offline · no MQH)

| Task | Layer | Deliverable | Status |
| --- | --- | --- | --- |
| **P4-T01** | L6 | Decision ledger schema + offline writer | **DONE** · `aos_l6_ledger.md` |
| **P4-T02** | stack | Det stack `L1+L2det+L3+L4+L6` shadow run | **DONE** · May∨Jul EF **+0.89** measured |
| **P4-T03** | stack | + L2 AI shadow on det fires | **DONE** · DISARM · n_shadow=0 |
| **P4-T04** | L8 | MAE abort advisor (shadow; **secondary** for index sleeve) | **DONE** · 15 advises / 0 winners |

### PHASE 5 — RETRAIN LOOP (`JP225-AOS-P5`) — **DONE** 2026-10-19

| Task | Layer | Deliverable | Status |
| --- | --- | --- | --- |
| **P5-T01** | L5 | Retrain policy + model store layout `L2skip_jp225/` | **DONE** · `aos_l5_retrain.md` · train entrypoint |
| **P5-T02** | L5 | Champ/challenger promote rules (shadow→candidate) | **DONE** · AI challenger EMPTY (AUC 0.49) |
| **P5-T03** | L5 | Rollback drill | **DONE** · `_drill/*/DRILL_REPORT.json` pass |

### PHASE 6 — HARDENING (`JP225-AOS-P6`) — **DONE** 2026-10-19

| Task | Layer | Deliverable | Status |
| --- | --- | --- | --- |
| **P6-T01** | L9 | Session-quality soft veto (London open / spread tercile) | **DONE** · London/H08/H14 HOLD · spread DISARM |
| **P6-T02** | G5-ish | ±10% / arm-width stress on L2 (not SL/TP) | **DONE** · keep May∨Jul · Wed widen stall |
| **P6-T03** | — | Confirm ATR max declared for G3 when OS armed | **DONE** · 19670 on P0+P1 |

### PHASE 7 — PROMOTION (`JP225-AOS-P7`) — **DONE** 2026-10-19 · HITL SIGNED

| Task | Layer | Deliverable | Status |
| --- | --- | --- | --- |
| **P7-T01** | L10 | Promotion packet: CF · health · ledger · gates · tip EF>0 | **DONE** · `promotion_packet.json` |
| **P7-T02** | L10 | HITL sign-off · research OS arm | **SIGNED** · magic **26151907** · **JPN225stack** |
| **P7-T03** | — | Paper / tiny-f attach checklist | **DONE** · see `AIOS_SIGNOFF.md` |

---

## 7. Weekly implementation table

Calendar assumes **Week 0 = 2026-10-19** (P0 stubs). Slip tasks forward; do not skip measured Leak / P1 tape to chase L2 AI. Optional **P1.5 engine blotter** may run in parallel as a *new baseline candidate* — if it wins Stage 1 with AOS OFF, re-freeze before P2. One primary OS task stream at a time; blotter clear-after-review applies.

| Week | Dates (2026) | Phase | Primary tasks | Exit criteria (done when) |
| ---: | --- | --- | --- | --- |
| **0** | Oct 19 | P0 | P0-T01 · P0-T02 · P0-T03 stub | Baseline + bad-cells + cost stub in `doc/assets/JP225/` |
| **1** | Oct 19 | P1 | P1-T01…T03 · T05 · tapes | **DONE** tip79 + janaug143 + long360 · bad-cells updated |
| **2** | Oct 19 | P2 | P2-T01…T07 CF | **DONE** ARM May∨Jul · HOLD Wed/H14 · DISARM L2AI · see `aos_l2_policy.md` |
| **3** | Oct 19 | P3 | P3-T01…T04 L3/L4 | **DONE** May∨Jul MaxDD 1.5% · 1 BELOW · see `aos_l3l4_policy.md` |
| **3b** | Oct 19 | LEAK | Deal-fill Leak measure | **DONE** Leak **2.45 pp** · tip EF **+0.59** |
| **4** | Oct 19 | P4 | P4-T01…T04 ledger+stack (offline) | **DONE** · no MQH · see `aos_l6_ledger.md` |
| **5** | Oct 19 | P5 | P5-T01…T03 retrain / store | **DONE** · AUC 0.49 DISARM · drill pass |
| **6** | Oct 19 | P6 | P6-T01…T03 harden | **DONE** · see `aos_p6_harden.md` |
| **7** | Oct 19 | P7 | P7-T01…T03 HITL | **DONE** · **JPN225stack** · magic 26151907 |
| **8** | Oct 20+ | buffer | Tester confirm ledger | Run tip May→Aug on JPN225stack |

### Weekly operating rhythm

| Day | Action |
| --- | --- |
| Mon | Confirm week’s primary task · load P1 preset · note compare window (tip default) |
| Tue–Thu | Implement / run Tester / build tape or CF |
| Fri | Score under `edge_framework.md` · ACCEPT/REJECT · archive blotter · update this roadmap status |
| Ongoing | No foreign L2 pin · no SL/TP “quick fix” · no thin-SL under ~2300 spread · Canvas display-only · expansion not live replace |

---

## 8. Preset / artifact naming

```text
Profiles/Tester/BMRG/JP225/JP225-AOS-P{phase}-T{task}_{layer}_{change}.set
blotter/archive/JP225-AOS-P{phase}-T{task}/
infra/artefacts/models/L2skip_jp225/LATEST/
doc/assets/JP225/aos_bad_cells.md
doc/assets/JP225/aos_cost_policy.md
doc/assets/JP225/JP225_AOS_BASELINE_v1.md
doc/assets/JP225/aos_l1_tape_contract.md   # from P1
doc/assets/JP225/aos_l2_policy.md          # from P2
```

Research OS magic: keep engine **26101904**; OS experiment magics in **2615xxxx** (target arm **26151907**) — never collide with EUR (`2612xxxx` / `8210xxx`), UK (`2611xxxx`), USDJPY (`2613xxxx`), DE40 (`2614xxxx`), or AUD live.

---

## 9. Scorecard fields (every weekly exit)

```text
framework_unified: 1.0
framework_jp225: 0.1.0
aos_task: JP225-AOS-P#-T##
preset_id / magic / window / n
aos_overlay: none | L2det | L2AI_shadow | L2AI_withhold | L3 | stack
baseline_ref: JP225_AOS_BASELINE_v1
WR, R, BWR, BM, Leak, Leak_source, EF, M, E_N, PF
skips_n, skip_precision_bad_cell, fire_retention_pct
false_skip_rate_on_Aug_Sep_MATCH_or_Jun_pay
ΔE_N_vs_baseline, ΔEF_vs_baseline, MaxDD
tip_EF_cleared: true|false
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
| `JP225_AOS_BASELINE_v1.md` | Frozen P1 numbers |
| `aos_bad_cells.md` | L2det seed registry |
| `aos_cost_policy.md` | Leak **measured** 2.45 pp |
| `LEAK_MEASURED.json` | Deal-fill packet (authority) |
| `aos_l6_ledger.md` | L6 schema + P4 stack (offline) |
| `aos_l5_retrain.md` | L5 retrain / champ–challenger / rollback |
| `aos_p6_harden.md` | L9 / L2 stress / ATR G3 |
| `AIOS_SIGNOFF.md` | HITL · research OS arm |
| `promotion_packet.json` | P7 packet |
| `aos_l1_tape_contract.md` | L1 feature schema v0 |
| `tapes/jp225_*_fire_tape_v0.csv` | Tip / Jan–Aug / long / combined labeled fires |
| `aos_l2_policy.md` | L2det / L2AI ARM map (P2) |
| `aos_l2_size_table.md` | f multipliers (spec) |
| `aos_l3l4_policy.md` | L3 halt / L4 health / bus (P3) |
| `blotter/archive/JP225-AOS-P2/` | P2_CF · REVIEW · run_p2_cf.py |
| `blotter/archive/JP225-AOS-P3/` | P3_L3L4 · health_path_*.csv · REVIEW |
| `blotter/archive/JP225-AOS-LEAK/` | LEAK_MEASURED · tip_deal_costs · REVIEW |
| `blotter/archive/JP225-AOS-P4/` | P4_STACK · ledger_*.csv · REVIEW |
| `blotter/archive/JP225-AOS-P5/` | tip_l2ai_scored · _drill · REVIEW |
| `blotter/archive/JP225-AOS-P6/` | P6_HARDEN · REVIEW |
| `blotter/archive/JP225-AOS-P7/` | promotion_packet · JPN225stack · REVIEW |
| `Include/AOS_L2det_jp.mqh` | May∨Jul L2det wire |
| `Presets/JPN225stack.set` | Research OS arm preset |
| `infra/artefacts/models/L2skip_jp225/` | Store · LATEST · rollback · DISARM |
| `AIOS_SIGNOFF.md` | HITL research OS arm (from P7) |
| `doc/ai_OS.md` | Layer vocabulary |
| `doc/BMRG_M15_JP225_6M_chart_preset.md` | Design / probe card |
| `blotter/archive/JP225-P1-REVIEW/` | Engine P1 review (pre-OS) |

---

## 11. Versioning

- **0.1.0** — Initial JP225 AIOS plan; P0 stubs from P1 blotter (2026-10-19).  
- **0.1.1** — P1 tapes + schema; bad-cells add Wed/H08/H14/SELL-caution; near_atr alone = protect (2026-10-19).  
- **0.1.2** — P2 L2det ARM May∨Jul (tip EF cleared +9.2 pp) · DISARM L2AI (2026-10-19).  
- **0.1.3** — P3 L3/L4 signed · May∨Jul path MaxDD 1.5% · BELOW latch retained (2026-10-19).  
- **0.1.4** — Leak measured 2.45 pp · tip EF +0.59 · P4 offline ledger/stack · no MQH (2026-10-19).  
- **0.1.5** — P5 L2skip_jp225 store · AUC 0.49 DISARM · rollback drill pass (2026-10-19).  
- **0.1.6** — P6 harden · L9 HOLD · May∨Jul stress · ATR G3 19670 · no MQH (2026-10-19).  
- **0.1.7** — P7 HITL · JPN225stack · magic 26151907 · AOS_L2det_jp.mqh (2026-10-19).  
- Bump when phase order, iteration bar, pin name, engine magic, or baseline window changes.

---

## 12. One-line plan

**Freeze Growth P1, measure Leak (tip EF clears at 2.45 pp), arm JP225-native May∨Jul research OS via JPN225stack / magic 26151907 after HITL — protect Aug–Sep MATCH and paying Jun, never borrow foreign L2, never thin SL, never replace live FX/EU books.**

---

## 13. Status line (update Fridays)

```text
2026-10-19 | P7 COMPLETE | HITL SIGNED · JPN225stack · magic 26151907 · May∨Jul LIVE_WITHHOLD · Leak 2.45pp · L2AI DISARM · next=Tester confirm
```
