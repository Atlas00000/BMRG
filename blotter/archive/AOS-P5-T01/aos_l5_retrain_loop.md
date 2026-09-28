# AOS L5 Retrain Loop v0

**Phase:** AOS-P5  
**Layer:** L5 Adaptation / Retrain (+ L6 version pin)  
**Engine:** Harvest 8210204 · baseline `AOS_BASELINE_v1` EF **1.77**  
**Model store:** `models/L2skip/`  
**Live pin:** `L2skip_v0_engine` (AI skip OFF) · shadow `L2skip_v1`

L5 **never** silently overwrites live L2. Challengers enter shadow first. L10 owns live promote. L3 still outranks.

---

## T01 — Retrain cadence + triggers

### Cadence

| Trigger | When | Action |
| --- | --- | --- |
| **MONTHLY** | Calendar day 1 (or first trading day) | Spawn challenger train job → new `L2skip_v{N}` under `models/L2skip/versions/` |
| **LIFECYCLE** | L4 W250 label ∈ {Compressing, Near frontier} for **≥ 2** consecutive observer samples | Same as monthly (may coincide) |
| **BELOW_FRONTIER** | L4 / L3 E_N ≤ 0 | **Do not retrain on decay-only window.** Halt risk (L3). Retrain only with expanding history that **includes** pre-decay data |
| **MANUAL** | Human / AOS task | Explicit version bump |

### Fit rules (hard)

```text
1. Walk-forward expanding (or rolling with min_train ≥ 150 events).
2. NEVER fit only on the Compressing / Below-frontier slice.
3. Entry-time features only (no exit lookahead).
4. Write challenger to versions/ — do NOT edit LIVE.json in the train job.
5. Promote path: train → shadow metrics → T02 decide → (optional) L10 live pin.
```

### No silent prod overwrite

| Allowed | Forbidden |
| --- | --- |
| Append new `versions/L2skip_v{N}/` | Overwrite `LIVE.json` from train script |
| Update `shadow_version` with REVIEW | Delete prior champion without rollback log |
| Human / L10 pin after T02 pass | Auto-pin on AUC alone |

Runbook owner: AOS task agent. Ledger every retrain attempt (`layer=L5`, `reason_code=RETRAIN_*`).

---

## T02 — Champion / challenger promote rule

### Try-candidate bar (G2–G5 **not** required)

| Check | Pass if |
| --- | --- |
| W250 EF (challenger CF or shadow) | ≥ `AOS_BASELINE` EF (**1.77**) |
| MaxDD | ≤ DD_limit + **2 pp** (25% → 27%) |
| Remaining n | ≥ 100 (loose) |
| Payoff trap | WR↑ with EF↓ → **REJECT** |

### Live-pin bar (stricter — still needs L10)

| Check | Pass if |
| --- | --- |
| Try-candidate | PASS |
| OOS AUC | ≥ **0.60** |
| Fold harm | No WF fold where kept EF ≪ all EF under stress |
| L3 conflict | Not relying on skip during Below-frontier (L3 owns halt) |
| L10 | Human desk ACK |

### Verdict vocab

| Verdict | Meaning |
| --- | --- |
| `REJECT` | Keep champion pin |
| `PROMOTE_SHADOW_CANDIDATE` | Set `shadow_version` only |
| `PROMOTE_LIVE_CANDIDATE` | Eligible for L10 pin (not auto) |
| `KEEP_CHAMPION` | No change |

### Dry-run (AOS-P5-T02) — **PASS**

| Case | Verdict |
| --- | --- |
| `L2skip_v1` shadow CF | **PROMOTE_SHADOW_CANDIDATE** (AUC / fold harm block live) |
| Fold-2 only | **REJECT** |
| Engine baseline hold | **KEEP_CHAMPION** |
| Hypothetical v2 strong | **PROMOTE_LIVE_CANDIDATE** |
| EF ok / DD breach | **REJECT** |

Artifact: `blotter/archive/AOS-P5-T02/champ_challenger_dryrun.json`

---

## T03 — Versioned model store + rollback

### Layout

```text
models/L2skip/
  LIVE.json                 # pinned_version + shadow_version
  rollback.py               # one-command pin restore
  rollback_log.jsonl
  versions/
    L2skip_v0_engine/       # champion live (noop AI)
      META.json
    L2skip_v1/              # shadow challenger
      L2skip_v1.joblib
      metrics.json
      shadow_cf.json
      META.json
```

### LIVE pin (current)

```json
{
  "pinned_version": "L2skip_v0_engine",
  "shadow_version": "L2skip_v1"
}
```

### Rollback dry-run — **PASS**

1. Simulated bad pin → `L2skip_v1`  
2. `python models/L2skip/rollback.py L2skip_v0_engine`  
3. Skip rate **0.2658 → 0.0** (within noise of engine-only)  
4. Snapshot: `archive/AOS-P5-T03/model_store_snapshot/`

---

## Task verdicts

| Task | Verdict |
| --- | --- |
| P5-T01 | **ACCEPT** — runbook locked |
| P5-T02 | **ACCEPT** — dry-run 5/5 |
| P5-T03 | **ACCEPT** — store + rollback OK |

**Next:** AOS-P6 stack presets (deterministic OS first; AI stack remains shadow).
