# BMRG Client — Information Architecture

**Task:** `UI-P0-T02`  
**Status:** DONE  
**Companions:** `doc/client_product_brief.md` · `doc/client_roadmap.md` · `client/src/App.tsx`

---

## 1. Sitemap

```mermaid
flowchart TB
  HOME[Home /]
  HOME --> HEALTH[/health]
  HOME --> LIVE[/live]
  HOME --> LAYERS[/layers]
  HOME --> PROVE[/prove]
  HOME --> OPS[/ops]
  HOME --> BLOTTER[/blotter]
  HOME --> FT[/ft]
  FT -.->|gated| FTSHIP[FT ship controls]
```

| Route | Nav label | Primary job | P0 state |
| --- | --- | --- | --- |
| `/` | Home | Status + next action (one composition) | **Proof surface** |
| `/health` | Health | Health vector · baseline Δ · windows · accept-bar | Placeholder |
| `/live` | Live | Identity · mode · fuses · journal bridge | Placeholder |
| `/layers` | Layers | L1–L10 map · ledger · L4 lifecycle | Placeholder |
| `/prove` | Prove | CF compare · skip audit · path≠paper · verdicts | Placeholder |
| `/ops` | Ops | Pin · promote/rollback · jobs · correlation | Placeholder |
| `/blotter` | Blotter | Inbox / archive / presets / CURRENT | Placeholder |
| `/ft` | FT | FT programme UX · auth gate · demo checklist | Placeholder (gated) |

Shell chrome (rail + identity meta) is shared; only the stage remounts.

---

## 2. Home composition (locked)

Home is **not** a dashboard of equal cards. One composition:

1. **Eyebrow + title** — product frame  
2. **MetricStrip** — EF / E_N / n / WR / MaxDD (tabular)  
3. **Primary signal plane** — Harvest identity + mode/life/decision chips  
4. **Next action** — single operational paragraph  
5. **ActionRail** — optional state lab / future shortcuts (asymmetric)

No balance hero. No widget grid.

---

## 3. Empty / error / loading states

| Condition | Pattern | Copy tone |
| --- | --- | --- |
| Section not built yet | `EmptyState` | “Surface not built” + deferral note |
| Artefact missing (W02+) | `EmptyState` | Name the path (`LATEST_EVAL.json`) — no crash |
| Loading | `Skeleton` / `SkeletonMetricStrip` | Geometry match; no clip art |
| Auth blocked mutate | Disabled `Button` + micro reason | “Requires AOS_LIVE_FT” |
| FT without auth | FT route reachable; ship controls disabled | Visible gate, not hidden trap |
| Network / parse fail (later) | Surface accent `warn` or `halt` | Short operational reason |

Never emoji, illustration, or Lorem.

---

## 4. Cross-route identity

Always visible in `AppShell` meta (and Live when built):

| Field | Example |
| --- | --- |
| Mode | `LIVE_WITHHOLD` |
| Magic | `8210204` |

Later: preset_id · ea_version · model semver on Live / Health headers.

---

## 5. Navigation rules

1. One primary nav — left rail (stacks horizontally on narrow viewports).  
2. Active route = signal hairline + dim wash (not bold fill pills).  
3. FT remains in nav so operators know it exists; capability gated separately.  
4. Deep links must render shell even when stage is EmptyState.  
5. Unknown paths → redirect to `/`.

---

## 6. Data domains (for later adapters)

| Route | Reads (AGENT_PATHS / artefacts) |
| --- | --- |
| Health | `ENGINE_BASELINE_v1.json` · `LATEST_EVAL.json` · window fixtures |
| Live | Journal / ledger paths · mode inputs (display) |
| Layers | `BMRG_AOS_ledger_<magic>.csv` · skip_ledger |
| Prove | CF scorecard · `INF-P6-T02` skip audit · prove JSON |
| Ops | `LATEST_LIVE/PIN.json` · `WIRE_AUTHORISATION.json` · `LATEST_JOB.json` |
| Blotter | `blotter/inbox` · `blotter/archive/<TASK>` · `CURRENT.md` · `doc/presets` |
| FT | FT docs + auth flags only until authorised |

---

## 7. Exit (P0 IA)

- [x] Full route map including FT  
- [x] Empty/error/loading patterns named  
- [x] Home composition locked as one composition  
- [x] Shell nav matches sitemap  
