# BMRG Infra — Phase / Week Exit Criteria

**Task:** `INF-P0-T03`  
**Recipe:** `INF-P0-T03_access_phaseExits_doc`  
**Locked:** 2026-09-27  
**Board:** `doc/infra_roadmap.md`  
**Contracts:** `doc/infrascaleup.md`  
**Baseline:** `infra/baselines/ENGINE_BASELINE_v1.json`

None of these exits require live forward testing or `AOS_LIVE`.

---

## Shared iteration bar (W05–W06, W09)

| Check | Bar |
| --- | --- |
| n remaining | ≥ 100 (warn if &lt; 385) |
| W250 EF | ≥ **0.77** pp (`1.77 − 1`) |
| W250 MaxDD | ≤ baseline MaxDD + **2** pp (when MaxDD measured) |
| Fires vs baseline | warn &lt; **70%**; hard-concern &lt; **50%** |
| Payoff trap | WR↑ + E_N↓ → reject |
| G0–G5 | Not required for infra week accept |

Report always: WR, R, BWR, BM, Leak, EF, M, E_N, ΔD, MaxDD, skip-rate, fire-count.

---

## Week / phase exits

### INF-W01 · INF-P0 — Lock

| Metric / check | Pass |
| --- | --- |
| Limitation map | L-T01…L-T14 locked in `infra/LIMITATIONS.md` |
| Baseline | `ENGINE_BASELINE_v1.json`: EF=1.77, n=530, E_N=0.091, magic=8210204 |
| Migrate inventory | Covers blotter, L1 tape, L2skip, shadow CF |
| Live FT | Forbidden |

### INF-W02 · INF-P1 — Contract + schema

| Metric / check | Pass |
| --- | --- |
| Schemas | Adapter JSON Schema validates; rejects missing `equity_at_open` / `risk_ccy` |
| Migrations | `alembic upgrade/downgrade` clean; six PG schemas exist |
| Landing | Duplicate sha → idempotent; corrupt → quarantine |
| Events | Rebuild ≈ **530** Harvest events; 1R consistent with SL300 |
| Live FT | Forbidden |

### INF-W03 · INF-P2 — Ingest

| Metric / check | Pass |
| --- | --- |
| Coverage | ≥95% archive opens → adapter legs |
| Idempotency | Load twice → row counts unchanged |
| Costs | `costs_defaulted` vs measured flagged; Leak ≈ **2.2** pp under same policy |
| Replay EF | Long-window EF within **±0.05** pp of **1.77** (same Leak policy) |
| Live FT | Forbidden |

### INF-W04 · INF-P3 — Offline L1

| Metric / check | Pass |
| --- | --- |
| PIT | Leakage tests green (`t_close ≤ entry_time`) |
| Coverage | ≥95% events have feature join |
| Champ tags | Tue opens = 0; LON_NY+NY ≥95% |
| Skips | **Zero** policy skips (perception-only); fire count = baseline |
| Live FT | Forbidden |

### INF-W05 · INF-P4a — Train + shadow ledger

| Metric / check | Pass |
| --- | --- |
| WF | Fit through decay; never fit-only-on-decay |
| Model | New `model_semver`; never overwrite prior |
| Shadow | Actual fires = baseline; would-skip logged |
| Folds | Per-fold skip-rate, EF, E_N, MaxDD reported |
| Live FT / wire | Forbidden |

### INF-W06 · INF-P4b — CF eval

| Metric / check | Pass |
| --- | --- |
| Scorecard | Full framework vector on CF blotter |
| Iteration bar | Shared bar above |
| Frequency | Prefer fires ≥70%; &lt;50% → week FAIL |
| L3 sim | Outranks L2 when halted in harness |
| Live FT / wire | Forbidden |

### INF-W07 · INF-P5a — Obs + Docker

| Metric / check | Pass |
| --- | --- |
| Correlation | One `event_id` traceable ingest→score in JSONL |
| Metrics | `LATEST_EVAL.json` has fire/skip, nulls, stall, cost-drift keys |
| Compose | Smoke + pinned image digests; one-command replay |
| Live FT | Forbidden |

### INF-W08 · INF-P5b — Box + tests + access

| Metric / check | Pass |
| --- | --- |
| Box | `BOX.md` lists CPU/RAM/disk; queue runs one heavy job off tester |
| Tests | `make test` green: FX-01…16, contract, replay freeze, migration dry-run |
| Agent | `make report` → Readable `LATEST_EVAL.json` without Tester UI |
| Live FT | Forbidden |

### INF-W09 · INF-P6 — Phase-prove gate

| Metric / check | Pass |
| --- | --- |
| Prove | W250/W500 EF, E_N, MaxDD, skip-rate, fires vs baseline |
| Overfilter audit | Every skip cluster justified (hostile / modest-confidence) |
| Frequency | Fires &lt;50% → **NO-GO** (no wiring plan) |
| Verdict | `doc/infra_wiring_eligibility.md` = GO or NO-GO |
| Live preset | Still forbidden |

### INF-W10 · INF-P7 — Wiring design (post-GO)

| Metric / check | Pass |
| --- | --- |
| Design | `infra_wiring_plan.md`: permit/withhold, L3 precedence, rollback |
| Dry-run | Champ/challenger promote/reject correct |
| EXP | If present, differs from champion only on bookkeeping |
| Live AI gate / FT | Forbidden unless user explicitly authorises |

### INF-W11 · INF-P8 — Retrain loop

| Metric / check | Pass |
| --- | --- |
| Loop | Enqueue → train → shadow → no silent pin |
| Gate | Failed challenger never pins |
| T03 | Blocked unless wire authorised |
| Live FT | Default forbidden |

---

## Agent Done definition

A week is **DONE** only when:

1. All §2 rows for that week in `doc/infra_roadmap.md` are `DONE`  
2. Week exit checklist boxes are checked  
3. Artefacts exist at the paths named in the implementation table  
4. Archive note written under `blotter/archive/INF-W##/` or per-task `INF-P#-T##/`  

**Verdict:** ACCEPT · `INF-P0-T03`
