# BMRG Client

Operator console (read-first). Design system: **Kyoto Ledger + Matcha Iron**.

## Run

```bat
cd client
npm install
npm run validate:openapi
npm run dev
```

Build check: `npm run build`

**Deploy:** Vercel prep is in-repo (`vercel.json`, `VITE_API_BASE`) but **shipping is paused** — see [`../DEPLOYMENT.md`](../DEPLOYMENT.md). Local dev keeps `VITE_API_BASE` empty so Vite `fs_bridge` serves `/api/*`.

## Routes

| Route | Page | Notes |
| --- | --- | --- |
| `/` | Home | Brand · champion · edge snapshot · posture · next action · pulse |
| `/performance` | Performance | Scorecard · windows · vs reference · accept · cadence · caveats |
| `/live` | Live desk | Attachment · mode · safety · book · journal · desk notices |
| `/review` | Review | Decisions · protection map · paper vs live · verdicts · size/halt · export |
| `/records` | Records | Pointer · inbox · archive · presets · FT prep (gated) · checklist |

Unknown paths redirect to `/`. Product map: [`design/PAGES.md`](design/PAGES.md) · theme: [`design/APP_THEME.md`](design/APP_THEME.md)

Former Health / Layers / Prove / Ops / Blotter / FT nav items are folded into the five pages above. Plan notes: [`doc/client_p3_p10_plan.md`](../doc/client_p3_p10_plan.md) · FT design: [`doc/client_ft_console.md`](../doc/client_ft_console.md)

## Foundations

| Path | Role |
| --- | --- |
| `design/PAGES.md` | Five-page product map |
| `design/APP_THEME.md` | Kyoto Ledger + Matcha Iron |
| `design/UI_PHILOSOPHY.md` | North star, kill list, tokens, motion |
| `design/tokens.css` | CSS variables |
| `design/backendMap.ts` | API enums → tones |
| `api/openapi.yaml` | Read contracts |
| `api/adapters/artefacts.ts` | INF JSON → DTOs |
| `api/fs_bridge.ts` | Vite middleware → `../infra/**` + fixtures |
| `src/api/` | fetch client · AuthProvider · useAsync |
| `src/lib/export.ts` | JSON/CSV download helpers |
| `src/features/auth/AuthGate.tsx` | Hard wall for mutate / FT |
| `src/components/*` | primitives · motion · shells · patterns |

No order tickets. Read-first; FT mutate stays gated (`AOS_LIVE_FT`).
