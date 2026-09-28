# INF wiring plan (INF-P7)

**Recipe:** `INF-P7-T01_access_wiringDesign_L2L3`  
**Eligibility:** `doc/infra_wiring_eligibility.md` — **USER AUTHORISED GO** (2026-09-28)  
**Scope:** Design + dry-run. Permit/withhold only. **No entry rewrite. No silent live swap.**

---

## 1. Attachment model (L2 / L3)

```
Engine signal (Harvest) ──► L3 guardrails ──► L2 skip intelligence ──► order?
                              │                    │
                              │ halt/f=0           │ WOULD_SKIP / FIRE / ALLOW_UNCERTAIN
                              ▼                    ▼
                         HALT_NO_ENTRY         withhold or allow
```

| Layer | Authority | Action |
| --- | --- | --- |
| **L3** | Outranks L2 | MaxDD halt, Below-frontier f=0, cost-drift halt → **HALT_NO_ENTRY** (L2 moot) |
| **L2** | Shadow → live only when pinned | `WOULD_SKIP` → withhold new entry; else allow engine fire |
| **Engine** | Always owns SL/TP/size/session | Unchanged geometry; OS never rewrites entry |

### EA hooks (shipped BMRG v1.21)

| Hook | Behaviour |
| --- | --- |
| `InpAiOsMode` | `OFF` \| `SHADOW` \| `LIVE_WITHHOLD` |
| `InpAiModelSemver` | Must match baked `AOS_L2INF_SEMVER` (warn on mismatch) |
| `InpAiKillSwitch` | true → force L2 OFF |
| On new signal | If L3 halt → no order. Else if LIVE_WITHHOLD and L2 WOULD_SKIP → no order. Else engine opens as today. |

**SHADOW mode:** engine always fires; decisions logged to AOS ledger only.  
**Regenerate coeffs after retrain:** `python infra/src/train/export_l2_mqh.py` then recompile EA.

---

## 2. Model pin + rollback

| Artefact | Role |
| --- | --- |
| `artefacts/models/L2skip/<semver>/` | Immutable challenger/champ artefact |
| `artefacts/models/L2skip/LATEST_SHADOW/PIN.json` | Latest shadow (eval only) |
| `artefacts/models/L2skip/LATEST_LIVE/PIN.json` | Live withhold pin (created only after shadow gate ACCEPT) |
| `ops.model_version` | Registry row (semver, path, metrics, parent) |
| `ops.eval_run` | Scorecard path + verdict before any pin change |

### One-command rollback

```bat
cd infra
python src/train/promote.py --rollback
```

Effect: delete/replace `LATEST_LIVE/PIN.json` with prior parent semver (or clear to OFF); write `artefacts/reports/ROLLBACK.json`. Kill-switch equivalent: set live pin absent → EA treats as OFF.

### Promote (challenger → live pin)

```bat
python src/train/promote.py --promote <semver>
```

Requires latest `ops.eval_run` / scorecard verdict **ACCEPT** for that semver. Never overwrites prior semver directories.

---

## 3. Champion / challenger runbook

| Role | Definition |
| --- | --- |
| Champion | Current `LATEST_LIVE` pin (or engine-only if none) |
| Challenger | New train output under new `model_semver` |

**Promote bar (same protect-don't-overfilter §):**

1. CF long EF ≥ engine EF − 1pp  
2. Fires kept ≥ 70% (hard fail &lt;50%)  
3. No payoff trap  
4. Skip audit: no unjustified edge overfilter **or** operator waiver logged in eval_run  
5. MaxDD not worse by &gt;2pp vs engine  

Failed challenger → **never** pins; keep prior live / shadow pointers.

Dry-run fixture: `infra/fixtures/promote/dry_run.json` + `python src/train/promote.py --dry-run`.

---

## 4. Retrain data (feeds W11)

| Source | Path | Use |
| --- | --- | --- |
| Offline Harvest blotter | `fixtures/blotter/harvest_long_v1/` · tape | Baseline + CF |
| Realtime / new tester exports | `landing/inbox/` → normalise → tape rebuild | Incremental retrain |
| Mixed | `retrain_loop.py --sources offline,landing` | Union PIT tape then train |

Realtime rows never skip-label at train time; labels from realised TP/SL only.

---

## 5. Checklist

- [x] Pin paths defined (shadow vs live)  
- [x] Rollback one-command (`promote.py --rollback` + `InpAiKillSwitch`)  
- [x] L3 outranks L2  
- [x] Champ/challenger dry-run  
- [x] **EA LIVE_WITHHOLD hook shipped (v1.21)** — compiled 0 errors  
- [x] Tester preset `INF-LIVE_WITHHOLD_Harvest_long.set`  

---

## 6. Explicit non-goals

- No entry rewrite (SL/TP/size still engine-owned)  
- No silent model overwrite — re-export `.mqh` after retrain  
- Full FT / `AOS_LIVE` production programme still needs separate auth  
