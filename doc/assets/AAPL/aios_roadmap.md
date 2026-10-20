# AAPL — AIOS Roadmap

**Version:** 0.1.1  
**Status:** **Optional / active research** — candidate is baseline Harvest; AIOS not required for pool KEEP  
**Candidate (now):** [`candidate_pool.md`](./candidate_pool.md) · `BMRG-M15-AAPL-6M-Harvest_RR1.25.set` · magic **26092501** · **AOS OFF**  
**Engine lock (OS baseline when resumed):** same Harvest · AOS OFF until armed  
**Secondary sleeve (reference only):** Balanced **26092502** — not the candidate  
**Parents:** [`edge_framework.md`](./edge_framework.md) · [`system_profile.md`](./system_profile.md) · [`BUILD_PLAN.md`](./BUILD_PLAN.md) (compile/test) · `doc/ai_OS.md` (layer vocabulary) · `doc/unified_edge_framework.md`  
**Sibling (M5 — do not mix):** [`aios_roadmap_M5.md`](./aios_roadmap_M5.md) · Balanced **26102011** / [`BUILD_PLAN_M5.md`](./BUILD_PLAN_M5.md)  
**Presets:** `Profiles/Tester/BMRG/AAPL/`  
**Blotter:** `blotter/inbox/` → `blotter/archive/AAPL-AOS-*/` after review  

**Not** EURUSD aistack (`8210204` / `8399001`) · **not** AUDUSD L2 pin · **not** a live replace · **not** M5 L2det transplant.

---

## 0. Canvas caveat

| Artifact | Authority |
| --- | --- |
| This roadmap + scored blotters under `edge_framework.md` | **Normative** for Apple AIOS work |
| `system_profile.md` | Evidence / descriptive |
| Canvas / chat charts / UI tiles | **Display only** |

Verdicts come from ledger + scorecard. Tip-only charts never promote a layer.

---

## 1. What this is / is not

| This is | This is not |
| --- | --- |
| An **Apple-owned AIOS** that permits / withholds / sizes / observes / adapts Harvest | A new SL/TP or BBDev optimisation programme |
| Layered work with task IDs `AAPL-AOS-P#-T##` | A replacement entry model or trend sleeve |
| Iteration vs a frozen Harvest baseline | Immediate live attach |
| Consumption of profile bad cells (Thu, hour-18, 2023, 2026 H1, gap/`OTHER`) | Re-ranking from profit / WR alone |
| Separate model store pin (`L2skip_aapl_…`) | Reuse of EUR / AUD L2 pins |

**Frozen OS objective:**

```
maximise E_N
subject to  EF hold vs baseline (−1 pp on primary health window is enough to keep iterating)
            MaxDD ≤ baseline MaxDD + 2 pp
never maximise WR, PF, or BM alone
never invent entries — only gate the engine fade
```

**Investigation order (unchanged):** data → execution → regime → structure.  
Do **not** touch SL/TP/BBDev/BBw bounds as the first OS move.

---

## 2. Working hypothesis (from AAPL profile)

> Harvest already has a real meanrev edge (long 2020→2026 +85 / WR 54% / E_N +0.22R; 2025 strong; tip recovers).  
> Remaining leak is **conditional**: fires still occur in regimes / calendar / path cells where BM ≤ 0 or expectancy collapses.  
> AI layers’ job: **withhold or size-down those fires**, contain overnight gap path risk, keep **EF** alive — without rewriting the fade.

| Claim | Evidence | Stance for OS |
| --- | --- | --- |
| Edge exists | Harvest extensive + primary long KEEP; tip WR 75% | **Accept** — freeze as AAPL-AOS-P0 |
| Weakness is conditional / WR-side in bad cells | 2023 WR 40%; 2026 H1 soft; Thu WR 44% | **Accept** — L2 skip/size, don’t chase R |
| Hour ~18 weak | Profile soft pocket | **Accept** — L2det soft/hard candidate |
| Overnight / OTHER ~20–28% | Equity CFD fingerprint | **Accept** — L8 path advisor + L3 overnight-aware DD |
| Spread regime varies (med ~5 long vs ~27 tip) | Leak_proxy unstable | **Accept** — cost feature in L1; Leak in L4 |
| Fixing via SL/TP first | Would reopen EDX; RR already TP>SL | **Reject as first move** |
| Borrow EUR/AUD L2 | Different microstructure / session | **Reject** — Apple pin only |

---

## 3. Architecture (same layers as `doc/ai_OS.md`)

```
L5 Retrain ──challenger──► L2 Policy (skip/size) ──permit──► Harvest ENGINE (26092501)
L1 Tape ──────────────────►        ▲
                                   │
                          L3 Guardrails (hard veto)
                                   ▲
                          L4 Observer (W15/W20 → W100/W250)
                                   │
                          L6 Ledger (all decisions)
L7 basket (later equities) · L8 MAE/gap abort · L9 session quality · L10 HITL promote
```

**Invariant:** L3 outranks L1/L2/L4/L5/L7–L10.

### Apple layer emphasis

| Layer | Apple focus |
| --- | --- |
| **L1** | ATR · BBw · RTH · DOW/hour · side · overnight · spread · optional earnings |
| **L2det** | Thu · hour-18 · optional buy-caution in hostile ATR/trend · never skip all buys blindly |
| **L2 AI** | Avoid-loser on Harvest fires only; pin `L2skip_aapl_*` |
| **L3** | MaxDD · Below-frontier f=0 · cost-drift · kill-switch |
| **L4** | Small-n W15/W20 first; adopt W100/W250 when n allows |
| **L5** | Retrain on decay / Compressing; WF through decay, not only on it |
| **L6** | Full reason codes for CF scorecards |
| **L8** | Early abort / hold advice on fast MAE + gap-open paths |
| **L10** | Only promotion path to “Apple OS live research” |

---

## 4. Baseline lock (AAPL-AOS-P0)

Import Harvest health from scored logs / profile. **No OS code.**

| Field | Extensive 2020.01→2026.08 | Primary long 2025.01→2026.08 | Tip May→Aug 2026 |
| --- | ---: | ---: | ---: |
| Magic / RR | 26092501 / 1.25 | same | same |
| n | **114** | 56 | 8 |
| WR | **54.4%** | 58.9% | 75.0% |
| E_N (des) | **+0.22R** | +0.33R | +0.69R |
| Final Δ | **+$85.47** | +$68.26 | +$20.91 |
| MaxDD (path) | ~3.7% | ~3.9% | ~0.7% |
| AOS | Off | Off | Off |

**OS compare window (default):** extensive **or** 2025→tip — state which on every task. Tip alone is confirmation only.

**Bad-cell registry (seed L2det):**

| Cell | Seed action |
| --- | --- |
| DOW_THU | SOFT skip candidate |
| HOUR_18 | SOFT/HARD skip candidate |
| YEAR_2023 / H1_2026 cluster | Regime tag → L4 Compressing / L2 size-down (not silent HARD skip of whole years in live) |
| GAP_OTHER high | L8 advise |
| BUY in high-ATR trend (optional) | Buy-caution SOFT — arm only if CF proves |

---

## 5. Iteration bar (loose on purpose)

**Accept** a layer experiment when **all** hold:

| Check | Bar |
| --- | --- |
| n remaining after skips | Report; no n≥385 floor (per AAPL edge_framework) |
| Health-window E_N / EF | ≥ baseline − **1 pp** EF (or E_N hold if Leak pending) |
| MaxDD | ≤ baseline + **2 pp** |
| 90d fire count | ≥ 50% baseline → else FREQUENCY_STALL **warn** |
| AL | Not worse unless E_N clearly improved |

**Reject immediately** when:

- WR↑ but E_N↓ or EF↓  
- Layer invents entries / changes SL/TP as “OS”  
- Higher layer overrides L3 halt  
- Uses EUR/AUD model pin on Apple  

**Promote (AAPL-AOS-P7 only)** when: shadow CF beats/holds baseline · L3/L4 wired · ledger complete · HITL sign-off under `edge_framework.md`. Full G0–G5 for any live-capital claim — not for every weekly trial.

---

## 6. Phase plan (task catalogue)

### PHASE 0 — ENGINE BASELINE LOCK (`AAPL-AOS-P0`)

| Task | Layer | Deliverable |
| --- | --- | --- |
| **P0-T01** | — | Freeze `AAPL_AOS_BASELINE_v1` scorecard (extensive + long + tip) |
| **P0-T02** | — | Bad-cell registry from profile (Thu, hour-18, 2023, 2026 H1, OTHER/gap) |
| **P0-T03** | — | Deal-export cost policy stub (`c_R` / Leak) — replace journal proxy |

### PHASE 1 — L1 PERCEPTION (`AAPL-AOS-P1`)

| Task | Layer | Deliverable |
| --- | --- | --- |
| **P1-T01** | L1 | Apple feature schema v0 (doc + field list) |
| **P1-T02** | L1 | Offline tape builder from Tester harvest fires / bars |
| **P1-T03** | L1 | Label fires: win/lose · DOW · hour · side · ATR · BBw · overnight · spread |
| **P1-T04** | L1 | Structure flags v0 (band-ride / failed fade) — optional if time |
| **P1-T05** | L1 | Earnings / event window flags (soft) |

### PHASE 2 — L2 POLICY (`AAPL-AOS-P2`)

| Task | Layer | Deliverable |
| --- | --- | --- |
| **P2-T01** | L2det | Parity: skip Tue already OFF — verify OS mirror |
| **P2-T02** | L2det | SOFT skip map v1: Thu ± hour-18 (shadow CF) |
| **P2-T03** | L2det | Optional buy-caution SOFT (hostile vol/trend only) |
| **P2-T04** | L2size | Lifecycle → f table (spec; wire after L4) |
| **P2-T05** | L2 AI | Train `L2skip_aapl` avoid-loser · **shadow only** |
| **P2-T06** | L2 AI | Shadow CF scorecard vs P0 + vs L2det-only |

### PHASE 3 — L3 + L4 (`AAPL-AOS-P3`)

| Task | Layer | Deliverable |
| --- | --- | --- |
| **P3-T01** | L3 | MaxDD / kill / Below-frontier halt policy (Apple DD_limit) |
| **P3-T02** | L3 | Cost-drift + FREQUENCY_STALL warn |
| **P3-T03** | L4 | Rolling health W15/W20 (+ W100 when able) |
| **P3-T04** | L4→L3 | Recommend bus: Below → halt; Compressing → investigate |

### PHASE 4 — LEDGER + STACK (`AAPL-AOS-P4`)

| Task | Layer | Deliverable |
| --- | --- | --- |
| **P4-T01** | L6 | Decision ledger schema + offline writer |
| **P4-T02** | stack | Det stack `L1+L2det+L3+L4+L6` shadow run |
| **P4-T03** | stack | + L2 AI shadow on det fires |
| **P4-T04** | L8 | MAE/gap abort advisor (shadow) |

### PHASE 5 — RETRAIN LOOP (`AAPL-AOS-P5`)

| Task | Layer | Deliverable |
| --- | --- | --- |
| **P5-T01** | L5 | Retrain policy + model store layout `L2skip_aapl/` |
| **P5-T02** | L5 | Champ/challenger promote rules (shadow→candidate) |
| **P5-T03** | L5 | Rollback drill |

### PHASE 6 — HARDENING (`AAPL-AOS-P6`)

| Task | Layer | Deliverable |
| --- | --- | --- |
| **P6-T01** | L9 | Session-quality soft veto (RTH quality / spread tercile) |
| **P6-T02** | L7 | Multi-equity throttle stub (only if META/other equities join) |
| **P6-T03** | G5-ish | ±10% bound stress on L2 thresholds (not SL/TP first) |

### PHASE 7 — PROMOTION (`AAPL-AOS-P7`)

| Task | Layer | Deliverable |
| --- | --- | --- |
| **P7-T01** | L10 | Promotion packet: CF · health · ledger sample · edge_framework gates |
| **P7-T02** | L10 | HITL sign-off · research OS arm (still not FX-live replace) |
| **P7-T03** | — | Optional paper / tiny-f attach checklist |

---

## 7. Weekly implementation table

Calendar assumes **Week 1 = week of 2026-10-13** (Mon). Slip tasks forward; do not skip P0/P1 to chase L2 AI. One primary task stream at a time; blotter clear-after-review applies.

| Week | Dates (2026) | Phase | Primary tasks | Exit criteria (done when) |
| ---: | --- | --- | --- | --- |
| **1** | Oct 13–19 | P0 | P0-T01 baseline freeze · P0-T02 bad-cell registry | `AAPL_AOS_BASELINE_v1` + bad-cell md in `doc/assets/AAPL/` · archive folder |
| **2** | Oct 20–26 | P0→P1 | P0-T03 deal/cost stub · P1-T01 feature schema | Cost policy written · schema reviewed |
| **3** | Oct 27–Nov 2 | P1 | P1-T02 tape builder · P1-T03 label Harvest fires | Offline tape covers ≥ extensive window fires · labels QA’d |
| **4** | Nov 3–9 | P1 | P1-T04 structure (opt) · P1-T05 earnings flags | Tape v0 frozen; optional flags documented if deferred |
| **5** | Nov 10–16 | P2 | P2-T01 Tue parity · P2-T02 Thu/hour-18 SOFT map shadow | CF ledger: skips listed · E_N/EF vs baseline within loose bar **or** reject map |
| **6** | Nov 17–23 | P2 | P2-T03 buy-caution trial · P2-T04 size-table spec | Buy-caution ARMED only if CF pass; else DISARMED · size table written |
| **7** | Nov 24–30 | P3 | P3-T01 L3 MaxDD/halt · P3-T02 stall/cost warn | Offline L3 trips simulated on Apple path · policy md |
| **8** | Dec 1–7 | P3 | P3-T03 L4 rolling health · P3-T04 L4→L3 bus | W15/W20 health CSV · Below→halt verified |
| **9** | Dec 8–14 | P4 | P4-T01 ledger · P4-T02 det stack shadow | Full det stack CF scorecard vs P0 |
| **10** | Dec 15–21 | P4→P2 | P2-T05 train `L2skip_aapl` · P2-T06 AI shadow CF | Model pin under `infra/artefacts/models/L2skip_aapl/` · shadow only |
| **11** | Dec 22–28 | P4 | P4-T03 AI+det shadow · P4-T04 L8 MAE/gap shadow | Stack CF; L8 advise-only |
| **12** | Dec 29–Jan 4 | P5 | P5-T01 retrain policy · P5-T02 champ/challenger · P5-T03 rollback | Store + rollback drill documented |
| **13** | Jan 5–11 | P6 | P6-T01 session-quality · P6-T03 threshold stress | Soft veto CF; stress note |
| **14** | Jan 12–18 | P7 | P7-T01 promotion packet · P7-T02 HITL | KEEP OS research arm **or** stay shadow with named gaps |
| **15** | Jan 19–25 | buffer | Slip / re-run fails · P7-T03 paper checklist if armed | Clean archive; roadmap status update |

### Weekly operating rhythm

| Day | Action |
| --- | --- |
| Mon | Confirm week’s primary task · load Harvest preset · note compare window |
| Tue–Thu | Implement / run Tester / build tape or CF |
| Fri | Score under `edge_framework.md` · ACCEPT/REJECT · archive blotter · update this roadmap status line |
| Ongoing | No EUR/AUD pin · no SL/TP “quick fix” · Canvas display-only |

---

## 8. Preset / artifact naming

```text
Profiles/Tester/BMRG/AAPL/AAPL-AOS-P{phase}-T{task}_{layer}_{change}.set
blotter/archive/AAPL-AOS-P{phase}-T{task}/
infra/artefacts/models/L2skip_aapl/LATEST/
doc/assets/AAPL/aos_bad_cells.md          # from P0-T02
doc/assets/AAPL/aos_l1_tape_contract.md   # from P1
doc/assets/AAPL/aos_l2_policy.md          # from P2
```

Research OS magic bookkeeping: keep engine **26092501**; OS experiment magics in **2610xxxx** range if a separate `.set` is required — never collide with EUR/AUD live.

---

## 9. Scorecard fields (every weekly exit)

```text
framework_aapl: 0.1.1
roadmap: aios_roadmap 0.1.0
task_id: AAPL-AOS-P#-T##
baseline_ref: AAPL_AOS_BASELINE_v1
window: <extensive|long|tip>
n_engine / n_after_skip
WR, R, E_N, EF_proxy|EF, MaxDD
CF_delta_E_N / CF_delta_EF
layers_armed: L2det|L2ai|L3|L4|L8|...
verdict: ACCEPT | REJECT | DEFER
canvas: display_only
```

---

## 10. Document map

| File | Role |
| --- | --- |
| **`aios_roadmap.md`** | **This file — M15 weekly AIOS plan** |
| `aios_roadmap_M5.md` | **M5** sibling (Balanced tip WATCH) — do not merge scorecards |
| `BUILD_PLAN.md` | M15 compile/test L2det Thu·18 |
| `edge_framework.md` | Normative scoring / gates |
| `system_profile.md` | Engine behaviour evidence |
| `doc/ai_OS.md` | Shared layer vocabulary (EUR path reference) |
| `Profiles/Tester/BMRG/AAPL/` | Engine + AOS presets |

---

## 11. Versioning

- **0.1.0** — Initial Apple AIOS roadmap: hypothesis, phases P0–P7, 15-week implementation table from 2026-10-13, loose iteration bar, Apple-specific bad cells.  
- **0.1.1** — Cross-link M5 sibling roadmap/build; status optional-active (2026-10-20).  
- Bump when week plan, baseline window, or phase exits change.

---

## 12. One-line contract

**Freeze Apple Harvest as the OS engine; spend the next ~15 weeks building an Apple-only AIOS that skips conditional losers and guards overnight path risk — starting with baseline + tape + L2det, then L3/L4, then shadow L2 AI — scored under `edge_framework.md`, never by Canvas or SL/TP retunes.**
