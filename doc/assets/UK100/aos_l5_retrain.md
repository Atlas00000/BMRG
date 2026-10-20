# UK100 — L5 retrain / champ–challenger / rollback (P5)

**Version:** 1.0.0  
**Tasks:** UK100-AOS-P5-T01 … T03  
**Date:** 2026-10-12  
**Store:** `infra/artefacts/models/L2skip_uk/`  
**Train:** `python infra/src/train/train_l2_uk100.py`  
**Rollback:** `python infra/artefacts/models/L2skip_uk/rollback_l2skip_uk.py …`  

**Mode:** AI pin stays **SHADOW_ONLY / DISARM** until P7 HITL. Overlay champ is **L2det_uk_v1b** (EA), not this LR.

---

## 1. Roles (two tracks)

| Role | What | Current |
| --- | --- | --- |
| **Overlay champ** | Deterministic L2det v1b in EA | **ARMED** research OS (`InpAOS_UK_L2detEnable`) |
| **AI champ** | Baked / pinned `L2skip_uk_*` for LIVE_WITHHOLD | **none** (DISARM) |
| **AI challenger** | New train artifact under review | **EMPTY** |
| **Shadow artifact** | Latest train for research CF only | `LATEST/` pin |

L2det outranks L2 AI. Retrain never removes det maps.

---

## 2. Store layout (`L2skip_uk/`)

```text
L2skip_uk/
  README.md                 # store index
  STORE.json                # schema
  CHAMP.json                # AI champ pointer (null while DISARM)
  CHALLENGER.json           # AI challenger pointer
  LATEST/                   # active shadow pin + model copy
    PIN.json
    META.json
    metrics.json
    model.joblib
    README.md
  L2skip_uk_p_prior_<ts>/   # immutable run dirs
  ROLLBACK_LOG.jsonl
  rollback_l2skip_uk.py
  _drill/<ts>/DRILL_REPORT.json
```

Semver: `L2skip_uk_p_prior_YYYYMMDD_HHMMSS`.  
MQH export: **blocked** until challenger clears tip CF (P7).

---

## 3. P5-T01 — Retrain policy

### Triggers (any one)

| Trigger | Gate |
| --- | --- |
| Tape growth | ≥ **+30** labelled fires vs last train |
| Cost | `Leak_source` flips to **measured** |
| Drift | Tip rolling EF under L2det+engine &lt; baseline −1 pp for 2 tip months |
| Calendar | Quarterly review (or before P7 packet) |
| Feature | New L1 fields frozen in `aos_l1_tape_contract.md` |

### Forbidden triggers

- Chase WR / PF alone  
- Borrow EUR/AUD/AAPL coeffs  
- Retrain to “fix” a single bad week  
- Auto LIVE_WITHHOLD after train

### Train protocol

1. Fit on **prior** (Jan–Apr) · score **tip** OOS (May–Aug).  
2. Thr sweep on tip is for **reporting only** (document leak).  
3. Write immutable `L2skip_uk_p_prior_<ts>/` + refresh `LATEST` as `SHADOW_ONLY`.  
4. Do **not** set `CHALLENGER.json` automatically.

```text
python infra/src/train/train_l2_uk100.py
```

---

## 4. P5-T02 — Champ / challenger promote rules

### Shadow → challenger (AI)

All required:

| # | Rule |
| --- | ---: |
| 1 | Tip OOS AUC ≥ **0.55** |
| 2 | Best tip CF verdict **`SHADOW_CANDIDATE`** (ΔE_N>0 · prec≥0.55 · Wed FP≤1 · ret≥50%) |
| 3 | Stack **L2det ∨ L2AI** does not worsen tip E_N vs **L2det alone** by &gt; 0.02R |
| 4 | HITL note in blotter archive |
| 5 | `CHALLENGER.json` updated; mode still SHADOW_ONLY |

### Challenger → AI champ (LIVE_WITHHOLD candidate)

P7 only: promotion packet + HITL. Not in P5.

### Overlay champ changes

L2det map edits go through `aos_l2_policy.md` CF — not this store.

---

## 5. P5-T03 — Rollback drill

```text
python infra/artefacts/models/L2skip_uk/rollback_l2skip_uk.py status
python infra/artefacts/models/L2skip_uk/rollback_l2skip_uk.py drill
```

Drill steps: snapshot PIN → set **DISARM** → restore prior shadow semver → write `_drill/*/DRILL_REPORT.json`.

### EA rollback (research OS)

| Intent | Inputs |
| --- | --- |
| AI off | `InpAiKillSwitch=true` or `InpAiOsMode=OFF` |
| Det off | `InpAOS_UK_L2detEnable=false` |
| Full engine | `InpAOS_Enable=false` · P0 balanced `.set` |

---

## 6. Sign-off

| Task | Verdict |
| --- | --- |
| P5-T01 store + train entrypoint | **PASS** |
| P5-T02 promote rules | **PASS** (documented; no AI challenger yet) |
| P5-T03 rollback drill | **PASS** (see `_drill/`) |
| L2 AI LIVE_WITHHOLD | **NOT ARMED** |
| Next | P6 hardening |
