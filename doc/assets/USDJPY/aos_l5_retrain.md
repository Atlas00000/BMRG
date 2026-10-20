# USDJPY — L5 retrain / champ–challenger / rollback (P5)

**Version:** 1.0.0  
**Tasks:** USDJPY-AOS-P5-T01 … T03  
**Date:** 2026-10-19  
**Store:** `infra/artefacts/models/L2skip_usdjpy/`  
**Train:** `python infra/src/train/train_l2_usdjpy.py`  
**Rollback:** `python infra/artefacts/models/L2skip_usdjpy/rollback_l2skip_usdjpy.py …`  

**Mode:** AI pin stays **SHADOW_ONLY / DISARM** until P7 HITL. Overlay champ is **`L2det_usdjpy_v1c_near_atr_OR_H16`** (offline CF until MQH), not this LR.

---

## 1. Roles (two tracks)

| Role | What | Current |
| --- | --- | --- |
| **Overlay champ** | Deterministic near_atr∨H16 (P2/P4 ARM) | **ARMED offline** · no EA MQH yet |
| **AI champ** | Baked / pinned `L2skip_usdjpy_*` for LIVE_WITHHOLD | **none** (DISARM) |
| **AI challenger** | New train artifact under review | **EMPTY** |
| **Shadow artifact** | Latest train for research CF only | `LATEST/` pin |

L2det outranks L2 AI. Retrain never removes det maps. Never place EUR / UK / AUD / AAPL / DE / INF pins here.

---

## 2. Store layout (`L2skip_usdjpy/`)

```text
L2skip_usdjpy/
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
  L2skip_usdjpy_p_pretip_<ts>/   # immutable run dirs
  ROLLBACK_LOG.jsonl
  rollback_l2skip_usdjpy.py
  _drill/<ts>/DRILL_REPORT.json
```

Semver: `L2skip_usdjpy_p_pretip_YYYYMMDD_HHMMSS`.  
MQH export: **blocked** until challenger clears tip CF + chrono holdout (P7).

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
- Borrow EUR / UK / AUD / AAPL / DE / INF coeffs  
- Retrain to “fix” a single bad week  
- Auto LIVE_WITHHOLD after train  
- Tip-only thr reselection without chrono holdout  
- Tip-internal train as sole OOS claim (P2 contamination)  
- Thin SL / raise ATR max / reopen Tokyo to “help” the model  

### Train protocol

1. Fit on **pre-tip** from **long** tape (fires before tip start) · score **tip** OOS.  
   YTD-only pre-tip is n≈5 — too thin; long pre-tip currently n≈14 (document). Prefer ≥20 when hist grows.  
2. Thr sweep on tip is for **reporting only** (document leak).  
3. Chrono holdout (60/40 inside tip, retrain) — required for challenger eligibility.  
4. Write immutable `L2skip_usdjpy_p_pretip_<ts>/` + refresh `LATEST` as `SHADOW_ONLY`.  
5. Do **not** set `CHALLENGER.json` automatically.

```text
python infra/src/train/train_l2_usdjpy.py
```

### Protect cells (AI CF)

False-skip on **BUY / Fri / H12 / H15 / May / Jun** must be reported.  
`SHADOW_CANDIDATE` requires BUY FP≤1 · Fri FP≤1 · total protect FP≤3 · prec≥0.55 · ΔE_N>0 · ret≥50%.

---

## 4. P5-T02 — Champ / challenger promote rules

### Shadow → challenger (AI)

All required:

| # | Rule |
| --- | ---: |
| 1 | Tip OOS AUC ≥ **0.55** |
| 2 | Best tip CF verdict **`SHADOW_CANDIDATE`** |
| 3 | Chrono holdout verdict ∈ {`SHADOW_CANDIDATE`, `HOLD_SHADOW`} — **not** `DISARM` / stall |
| 4 | Stack **L2det ∨ L2AI** does not worsen tip E_N vs **L2det alone** by &gt; 0.02R |
| 5 | HITL note in blotter archive |
| 6 | `CHALLENGER.json` updated; mode still SHADOW_ONLY |

### Challenger → AI champ (LIVE_WITHHOLD candidate)

P7 only: promotion packet + HITL. Not in P5.

### Overlay champ changes

L2det map edits go through `aos_l2_policy.md` CF — not this store. MQH wiring is a separate EA task.

---

## 5. P5-T03 — Rollback drill

```text
python infra/artefacts/models/L2skip_usdjpy/rollback_l2skip_usdjpy.py status
python infra/artefacts/models/L2skip_usdjpy/rollback_l2skip_usdjpy.py drill
```

Drill steps: snapshot PIN → set **DISARM** → restore prior shadow semver → write `_drill/*/DRILL_REPORT.json`.

### EA rollback (research / chart)

| Intent | Inputs |
| --- | --- |
| AI off | `InpAiKillSwitch=true` or `InpAiOsMode=OFF` |
| Full engine | `InpAOS_Enable=false` · Balanced P0 `.set` |
| P4 health only | Keep L3/L4/ledger · AiOsMode=OFF · magic **26131804** |

**Never** arm USDJPY research OS on live FX / UK / AUD / DE books. Foreign L2det inputs stay **false**.

---

## 6. P5 smoke (this run)

| Semver | Pre-n | AUC tip | Best tip CF | Chrono holdout |
| --- | ---: | ---: | --- | --- |
| `L2skip_usdjpy_p_pretip_20261019_155324` | 14 | **0.471** | HOLD_SHADOW (BUY FP 6) | SHADOW_CANDIDATE |

Rules #1–#2 **block** challenger (AUC&lt;0.55 · not SHADOW_CANDIDATE).  
**Overlay champ remains `L2det_usdjpy_v1c`**.

---

## 7. Sign-off

| Task | Verdict |
| --- | --- |
| P5-T01 store + train entrypoint | **PASS** |
| P5-T02 promote rules | **PASS** (documented; no AI challenger yet) |
| P5-T03 rollback drill | **PASS** (see `_drill/`) |
| L2 AI LIVE_WITHHOLD | **NOT ARMED** |
| Next | P6 hardening |
