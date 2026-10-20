# JP225 / JPN225 M5 — L5 retrain / champ–challenger / rollback (P5)

**Version:** 1.0.0  
**Tasks:** JP225-M5-AOS-P5-T01 … T03  
**Date:** 2026-10-20  
**Store:** `infra/artefacts/models/L2skip_jp225_m5/`  
**Train:** `python infra/src/train/train_l2_jp225_m5.py`  
**Rollback:** `python infra/artefacts/models/L2skip_jp225_m5/rollback_l2skip_jp225_m5.py …`  

**Mode:** AI pin stays **SHADOW_ONLY / DISARM** until P7 HITL. Overlay champ is **`L2det_jp225_m5_v1c`** (EA), not this LR.  
**Sibling:** M15 [`aos_l5_retrain.md`](./aos_l5_retrain.md) / `L2skip_jp225/` — **do not merge pins**.

---

## 1. Roles (two tracks)

| Role | What | Current |
| --- | --- | --- |
| **Overlay champ** | Deterministic L2det M5 v1c in EA | **ARMED** research OS (`InpAOS_JP_M5_L2detEnable`) |
| **AI champ** | Baked / pinned `L2skip_jp225_m5_*` for LIVE_WITHHOLD | **none** (DISARM) |
| **AI challenger** | New train artifact under review | **EMPTY** |
| **Shadow artifact** | Latest train for research CF only | `LATEST/` pin · AUC≈0.49 · best **DISARM** |

L2det outranks L2 AI. Retrain never removes det maps. Never place EUR / UK / DE / AUD / AAPL / M15 JP pins here.

---

## 2. Store layout (`L2skip_jp225_m5/`)

```text
L2skip_jp225_m5/
  README.md
  STORE.json
  CHAMP.json                # AI champ (null while DISARM)
  CHALLENGER.json           # AI challenger (EMPTY)
  LATEST/                   # active shadow pin + model copy
  L2skip_jp225_m5_p_prior_<ts>/
  ROLLBACK_LOG.jsonl
  rollback_l2skip_jp225_m5.py
  _drill/<ts>/DRILL_REPORT.json
```

Semver: `L2skip_jp225_m5_p_prior_YYYYMMDD_HHMMSS`.  
MQH export: **blocked** until challenger clears tip CF (P7).

---

## 3. P5-T01 — Retrain policy

### Triggers (any one)

| Trigger | Gate |
| --- | --- |
| Tape growth | ≥ **+40** labelled fires vs last train |
| Cost | `Leak_source` flips to **measured** |
| Drift | Tip rolling EF under L2det+engine &lt; baseline −1 pp for 2 tip months |
| Calendar | Quarterly review (or before P7 packet) |
| Feature | New L1 fields frozen in `aos_l1_tape_contract_M5.md` |

### Forbidden triggers

- Chase WR / PF alone  
- Borrow EUR / UK / DE / AUD / AAPL / **M15 JP** coeffs  
- Retrain to “fix” a single bad week  
- Auto LIVE_WITHHOLD after train  

### Train protocol

1. Fit on **prior** (Jan–Apr) · score **tip** OOS (May→Oct).  
2. Thr sweep on tip is for **reporting only**.  
3. If tip OOS AUC &lt; **0.55** → force best verdict **DISARM**.  
4. Protect FP gates: Jul ≤1 · H10 ≤1 · SELL ≤3.  
5. Write immutable `L2skip_jp225_m5_p_prior_<ts>/` + refresh `LATEST` as `SHADOW_ONLY`.  
6. Do **not** set `CHALLENGER.json` automatically.

```text
python infra/src/train/train_l2_jp225_m5.py
```

### Freeze train (2026-10-20)

| Field | Value |
| --- | --- |
| Semver | `L2skip_jp225_m5_p_prior_20261020_130822` |
| Tip OOS AUC | **≈0.490** |
| Best tip CF | **DISARM** (AUC gate · ΔE_N +0.041 thin n=3) |
| Challenger | EMPTY |

---

## 4. P5-T02 — Champ / challenger promote rules

### Shadow → challenger (AI)

All required:

| # | Rule |
| --- | ---: |
| 1 | Tip OOS AUC ≥ **0.55** |
| 2 | Best tip CF verdict **`SHADOW_CANDIDATE`** (ΔE_N>0 · prec≥0.55 · Jul FP≤1 · H10 FP≤1 · SELL FP≤3 · ret≥50%) |
| 3 | Stack **L2det ∨ L2AI** does not worsen tip E_N vs **L2det alone** by &gt; 0.02R |
| 4 | HITL note in blotter archive |
| 5 | `CHALLENGER.json` updated; mode still SHADOW_ONLY |

### Challenger → AI champ (LIVE_WITHHOLD candidate)

P7 only: promotion packet + HITL. Not in P5.

### Overlay champ changes

L2det map edits go through `aos_l2_policy_M5.md` CF — not this store.

---

## 5. P5-T03 — Rollback drill

```text
python infra/artefacts/models/L2skip_jp225_m5/rollback_l2skip_jp225_m5.py status
python infra/artefacts/models/L2skip_jp225_m5/rollback_l2skip_jp225_m5.py drill
```

Drill steps: snapshot PIN → set **DISARM** → restore prior shadow semver → write `_drill/*/DRILL_REPORT.json`.  
**2026-10-20 drill:** **PASS**.

### EA rollback (research OS)

| Intent | Inputs |
| --- | --- |
| AI off | `InpAiKillSwitch=true` or `InpAiOsMode=OFF` |
| Det off | `InpAOS_JP_M5_L2detEnable=false` |
| Full engine | `InpAOS_Enable=false` · P0 M5 growth `.set` |

---

## 6. Sign-off

| Task | Verdict |
| --- | --- |
| P5-T01 store + train entrypoint | **PASS** |
| P5-T02 promote rules | **PASS** (documented; no AI challenger) |
| P5-T03 rollback drill | **PASS** |
| L2 AI LIVE_WITHHOLD | **NOT ARMED** |
| Next | P6 harden |
