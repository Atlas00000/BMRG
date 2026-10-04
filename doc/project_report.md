# BMRG — Project Report (Infra · AI OS · Capabilities)

**As of:** ~2026-10 · EA **v1.21** · INF **W01–W11 DONE** · Client **P0–P10 shipped** (FT mutate **BLOCKED**)  
**Champion:** Harvest · magic **8210204** · EURUSD M5 · G0 single-leg  
**Rule:** OS may **permit / withhold / size / halt** — never invent or rewrite entries.

---

## 1. What the project is

BMRG is a **frozen profitable mean-reversion engine** (Bollinger fade) wrapped by an **AI Operating System** and an **offline infra box** that trains, proves, and pins protection layers.

| Piece | Role | Status |
| --- | --- | --- |
| **Harvest engine** | Signal + risk + G0 execution | Frozen baseline |
| **EDX** | Edge discovery / bad-cell map | Closed — consume only |
| **AI OS (AOS)** | L1–L10 protection stack | L2–L4/L6 live-capable; L7–L10 paper |
| **INF** | Offline schemas → train → CF → box → wire | W01–W11 **DONE** |
| **EA hook** | `LIVE_WITHHOLD` + baked INF L2 | Shipped |
| **Client console** | Read-first operator UI | P0–P10; FT gated |
| **FT programme** | Forward-test ops | Needs `AOS_LIVE_FT` |

Scoring language is always **EF · E_N · MaxDD · n · WR/R/BM/Leak** — not tester balance or “AI confidence.”

---

## 2. Engine (Harvest) capabilities

**Geometry / filters (locked)**

- SL **300** / TP **300** · RR **1.0** · BBDev **2.2**
- Session **12–20** · **skip Tuesday** · risk **0.5%**
- **G0:** `MaxLevels=1`, `MaxEntries=1` → **1 trade per basket**

**Locked long health** (`ENGINE_BASELINE_v1`)

| Metric | Value |
| --- | --- |
| n | 530 |
| WR | ~54.5% (BWR 50%) |
| EF | **1.77** doc / ~**2.33** INF replay |
| E_N | ~**+0.091 R** |
| Zone | Fragile |
| fires_90d | **35–80** → ~**0.5–1.3 baskets / trading day** |
| Stress 3M | EF ~6.43 · n=49 (thin) |

**Secondary sleeve:** Growth magic **8210401** (not OS default).  
**Paper OS evidence:** aistack magic **8399001** — **STAY_PAPER**.

---

## 3. AI Operating System (L1–L10)

Normative doc: `doc/ai_OS.md`. Invariant: **L3 outranks everything**.

| Layer | Job | Capability | Live status |
| --- | --- | --- | --- |
| **L1** | Perception | Regime / structure / session tape | Offline tape artefacts |
| **L2** | Policy | Skip / FIRE / ALLOW_UNCERTAIN from INF logistic | **LIVE_WITHHOLD** in EA |
| **L3** | Guardrails | MaxDD / frontier / kill / stall (hard, non-AI) | ON in INF preset |
| **L4** | Lifecycle size | `f_mult` from W250 health | ON · watch stuck `f=0.75` + EF=0 |
| **L5** | Retrain | Champ / challenger pins · no silent overwrite | Infra promote path |
| **L6** | Ledger | Decision audit CSV | `BMRG_AOS_ledger_<magic>.csv` |
| **L7** | Sleeve throttle | Multi-sleeve risk | STAY_PAPER |
| **L8** | MAE abort | Path-based early abort advice | STAY_PAPER |
| **L9** | Soft veto | Session / multi-horizon soft veto | STAY_PAPER |
| **L10** | HITL | Human promotion desk | STAY_PAPER |

**EA modes (`InpAiOsMode`)**

- **0 OFF** — engine only
- **1 SHADOW** — log WOULD_SKIP, still fire
- **2 LIVE_WITHHOLD** — WOULD_SKIP blocks new entry; FIRE/ALLOW pass to engine
- **Kill switch** — display/control via chart input (UI does not toggle remotely)

**Offline CF impact (paper, not live equity)**

Engine EF ~2.33 → CF ~**2.99** (+0.67); MaxDD ~21% → ~**16.8%**; ~7% fires skipped. Live path can diverge (deposit, halt latch, window start).

---

## 4. Infrastructure (INF)

Offline-first box under `infra/`. Plan: `doc/infra_roadmap.md` · contracts: `doc/infrascaleup.md`.

### Week board (complete)

| Week | Focus | Status |
| --- | --- | --- |
| W01 | Limitation map + baseline lock | DONE |
| W02 | Contracts + Postgres schema | DONE |
| W03 | Ingest pipeline | DONE |
| W04 | PIT / L1 tape | DONE |
| W05 | WF harness + L2 train + shadow ledger | DONE |
| W06 | CF eval + L3/L4 sim | DONE |
| W07 | Observability + Docker compose | DONE |
| W08 | Box tests + agent access | DONE |
| W09 | Prove gate (USER GO) | DONE |
| W10 | Wiring design | DONE |
| W11 | Retrain loop | DONE |

### Planes / stack

| Plane | Owns |
| --- | --- |
| P-ACCESS | Limitations · phase exits |
| P-DATA | Schemas · landing · ingest |
| P-STORE | Postgres (raw/core/features/train/score/ops) |
| P-FEAT | PIT features · regime tape |
| P-TRAIN | Walk-forward · L2 models · CF |
| P-BOX | Docker · Redis queue · workers |
| P-OBS | Baselines · scorecards · JSONL correlation |

**Runtime services (local docker-compose)**

- **Postgres** (host map `54329`)
- **Redis** queue
- Profiled workers: ingest / features / trainer / scorer / eval / job worker

**Artefacts operators care about**

- `ENGINE_BASELINE_v1.json`
- `LATEST_LIVE/PIN.json` · SHADOW · PRIOR
- `LATEST_EVAL.json` · CF scorecard · skip ledger / audit
- `WIRE_AUTHORISATION.json` (allows / forbids)
- Model pin e.g. `L2skip_inf_p92_20260927_223519`

**Auth boundary**

- Shipped: EA LIVE_WITHHOLD under wire auth
- Still forbidden without extra auth: **`AOS_LIVE_FT`**

---

## 5. Client console (operator UI)

Vite + React · design **Ledger Noir + Signal Teal** · read-first · no order tickets.

| Route | Capability |
| --- | --- |
| `/` | System pulse · baseline |
| `/health` | Health vector · windows · accept bar · export |
| `/live` | EA identity · mode · fuses · journal (kill display-only) |
| `/layers` | L1–L10 map · ledger filters · L4 stuck detect · L7–L10 paper |
| `/prove` | Engine vs CF · skip audit · path≠paper · verdicts |
| `/ops` | Pins · promote dry-run · jobs · correlation · gated mutate |
| `/blotter` | CURRENT · archive · presets · review assist |
| `/ft` | Attach checklist · metrics contract · **BLOCKED** stubs |

**Data path:** Vite `fs_bridge` → INF artefacts + fixtures (no Tester UI dependency).  
**Roles:** Viewer / Operator; mutate needs allow-list; FT needs `AOS_LIVE_FT`.

---

## 6. Testing & ops doctrine

Industry loop: **contract tests → CF prove → multi-window path → blotter archive**.

- Blotter: `inbox/` → review → `archive/<TASK_ID>/` · `CURRENT.md` pointer
- Identity: magic + preset + ea_version on Live/Health
- Path honesty: CF ≠ live equity forecast
- Demo chart attach ≠ FT programme
- Hosting recommendation: **Windows/MT VPS for EA uptime**; **Railway-class cloud for INF only** (not MT5)

---

## 7. Works today / does not

**Works**

- Harvest G0 engine + INF offline prove stack
- EA **LIVE_WITHHOLD** with baked L2
- L3/L4/L6 on INF preset
- Client observe/explain/gated ops UI
- pytest infra suite (historically 49 passed)

**Does not (by design or gate)**

- UI order entry / remote kill
- Silent FT enable
- aistack as production wiring
- L7–L10 as live gates
- Treating Tester balance as accept bar
- Reopening EDX as a campaign

---

## 8. Current operational posture

- **Demo account** chart-attached Harvest + AOS ON · LIVE_WITHHOLD · kill=0
- Expectancy of activity: ~**0–1+ basket/day** session days; quiet days normal
- AOS ledger may stay empty until skip/fire decisions are written
- Client last archived: **UI-P3-P10** · FT still **BLOCKED**
- Infra services are optional local Docker; EA continuity is the VPS problem, not Railway

---

## 9. One-line summary

**Frozen Harvest edge + INF-proven L2 withhold + hard L3 guardrails + audit ledger, observed through a read-first console — forward-test and higher OS layers stay gated until explicit auth.**

---

## Companions

| Doc | Use |
| --- | --- |
| [`README.md`](../README.md) | Public snapshot |
| [`ai_OS.md`](./ai_OS.md) | Layer stack (normative) |
| [`edge_framework.md`](./edge_framework.md) | Scoring authority |
| [`infra_roadmap.md`](./infra_roadmap.md) | INF week board |
| [`client_roadmap.md`](./client_roadmap.md) | UI week board |
| [`client_p3_p10_plan.md`](./client_p3_p10_plan.md) | Client P3–P10 plan |
| [`infra/AGENT_PATHS.md`](../infra/AGENT_PATHS.md) | Agent Read table |
