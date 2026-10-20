# JP225 — L5 retrain / champ–challenger / rollback (P5)

**Version:** 1.0.0  
**Tasks:** JP225-AOS-P5-T01 … T03  
**Date:** 2026-10-19  
**Store:** `infra/artefacts/models/L2skip_jp225/`  
**Train:** `python infra/src/train/train_l2_jp225.py`  
**Rollback:** `python infra/artefacts/models/L2skip_jp225/rollback_l2skip_jp225.py …`  

**Mode:** AI pin stays **SHADOW_ONLY / DISARM** until P7 HITL. Overlay champ is **`L2det_jp225_v1_May_OR_Jul`** (offline CF · no MQH), not this LR.

---

## 1. Roles (two tracks)

| Role | What | Current |
| --- | --- | --- |
| **Overlay champ** | Deterministic May∨Jul (P2 ARM) | **ARMED offline** · no EA MQH |
| **AI champ** | Baked / pinned `L2skip_jp225_*` for LIVE_WITHHOLD | **none** (DISARM) |
| **AI challenger** | New train artifact under review | **EMPTY** |
| **Shadow artifact** | Latest train for research CF only | `LATEST/` pin |

L2det outranks L2 AI. Retrain never removes det maps. Never place EUR / UK / AUD / DE40 / AAPL / INF pins here.

---

## 2. Store layout (`L2skip_jp225/`)

```text
L2skip_jp225/
  README.md
  STORE.json
  CHAMP.json                # AI champ pointer (null while DISARM)
  CHALLENGER.json           # AI challenger pointer
  LATEST/                   # active shadow pin + model copy
    PIN.json
    META.json
    metrics.json
    model.joblib
    README.md
  L2skip_jp225_p_pretip_<ts>/   # immutable run dirs
  ROLLBACK_LOG.jsonl
  rollback_l2skip_jp225.py
  _drill/<ts>/DRILL_REPORT.json
```

Semver: `L2skip_jp225_p_pretip_YYYYMMDD_HHMMSS`.  
MQH export: **blocked** until challenger clears tip CF + chrono holdout (P7).

---

## 3. P5-T01 — Retrain policy

### Triggers (any one)

| Trigger | Gate |
| --- | --- |
| Tape growth | ≥ **+30** labelled fires vs last train |
| Cost | `Leak_source` flips to **measured** ← **fired 2026-10-19** |
| Drift | Tip rolling EF under L2det+engine &lt; baseline −1 pp for 2 tip months |
| Calendar | Quarterly review (or before P7 packet) |
| Feature | New L1 fields frozen in `aos_l1_tape_contract.md` |

### Forbidden triggers

- Chase WR / PF alone  
- Borrow EUR / UK / AUD / DE40 / AAPL / INF coeffs  
- Retrain to “fix” a single bad week  
- Auto LIVE_WITHHOLD after train  
- Tip-only thr reselection without chrono holdout  
- Thin SL / raise ATR max to “help” the model  

### Train protocol

1. Fit on **pre-tip** (Jan–Apr from Jan–Aug tape) · score **tip** OOS.  
2. Thr sweep on tip is for **reporting only** (document leak).  
3. Chrono holdout (60/40 inside tip, retrain) — required for challenger eligibility.  
4. Write immutable `L2skip_jp225_p_pretip_<ts>/` + refresh `LATEST` as `SHADOW_ONLY`.  
5. Do **not** set `CHALLENGER.json` automatically.  
6. Score EF with **Leak measured 2.45 pp**.

```text
python infra/src/train/train_l2_jp225.py
```

---

## 4. P5-T02 — Champ / challenger promote rules

### Shadow → challenger (AI)

All required:

| # | Rule |
| --- | ---: |
| 1 | Tip OOS AUC ≥ **0.55** |
| 2 | Best tip CF verdict **`SHADOW_CANDIDATE`** (ΔE_N>0 · prec≥0.55 · Aug FP≤1 · Jun FP≤1 · SELL FP≤1 · ret≥50%) |
| 3 | Chrono holdout verdict ∈ {`SHADOW_CANDIDATE`, `HOLD_SHADOW`} — **not** `DISARM` / stall |
| 4 | Stack **L2det ∨ L2AI** does not worsen tip E_N vs **L2det alone** by &gt; 0.02R |
| 5 | HITL note in blotter archive |
| 6 | `CHALLENGER.json` updated; mode still SHADOW_ONLY |

### Challenger → AI champ (LIVE_WITHHOLD candidate)

P7 only: promotion packet + HITL. Not in P5.

### Overlay champ changes

L2det map edits go through `aos_l2_policy.md` CF — not this store. MQH wiring is a separate EA task (still deferred).

---

## 5. P5-T03 — Rollback drill

```text
python infra/artefacts/models/L2skip_jp225/rollback_l2skip_jp225.py status
python infra/artefacts/models/L2skip_jp225/rollback_l2skip_jp225.py drill
```

Drill steps: snapshot PIN → set **DISARM** → restore prior shadow semver → write `_drill/*/DRILL_REPORT.json`.

### EA rollback (research / chart)

| Intent | Inputs |
| --- | --- |
| AI off | `InpAiKillSwitch=true` or `InpAiOsMode=OFF` |
| Full engine | `InpAOS_Enable=false` · Growth P1 `.set` |
| P4 health only | Keep L3/L4/ledger offline · AiOsMode=OFF · magic 26101904 |

**Never** arm JP225 research OS on live FX / EU / UK books. Foreign L2det inputs stay **false**.

---

## 6. Sign-off

| Task | Verdict |
| --- | --- |
| P5-T01 store + train entrypoint | **PASS** |
| P5-T02 promote rules | **PASS** (documented; no AI challenger yet) |
| P5-T03 rollback drill | **PASS** (see `_drill/`) |
| L2 AI LIVE_WITHHOLD | **NOT ARMED** |
| Next | P6 hardening |
