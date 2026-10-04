# BMRG deployment — Railway (API + DB) · Vercel (client)

**Status (2026-10-04)**

| Surface | Platform | Status |
| --- | --- | --- |
| Read API (`server/`) | Railway | Linked as `bmrg-api` · **not deployed yet** |
| Postgres + Redis | Railway | **Running** in project `bmrg` |
| INF worker images (`infra/`) | Railway (optional) | Prepped · not required for console reads |
| Operator console (`client/`) | Vercel | Linked as `bmrg-client` · **PAUSED** (`ignoreCommand: exit 0` skips builds) |

### CLI link (already done)

| Tool | Version | Account | Linked target |
| --- | --- | --- | --- |
| `railway` | 5.63.1 | emilicelestine@gmail.com | Project **bmrg** · env **production** · service **bmrg-api** |
| `vercel` | 62.2.0 | celestineemili-5899 | `client/` → **bmrg-client** |

| Railway IDs | |
| --- | --- |
| Project | `fced28f4-e6ae-4b0d-92ec-847a5e7e4960` |
| Environment | `bc7f2ec7-a959-4fbb-a77c-37ec41eedeee` (production) |
| Service `bmrg-api` | `b9b653b2-911f-413a-9756-9c004d865cd8` |
| Dashboard | https://railway.com/project/fced28f4-e6ae-4b0d-92ec-847a5e7e4960 |

| Vercel | |
| --- | --- |
| Project | `bmrg-client` (`prj_BnmqoeviW0HXPObwEcefQBkQTRYA`) |
| Team | celestineemili-5899s-projects |
| Root dir | `client/` |

From repo root:

```bat
railway status
railway service
railway variables
```

From `client/`:

```bat
vercel project ls
vercel env ls
rem Deploy still paused — do not run vercel --prod yet
```

Infra is **Python + Docker Compose**, not a Node/pnpm app. There is no `infra/package.json` — do not expect `pnpm build` under `infra/`.

Local image build (requires Docker Desktop running):

```bat
cd infra
docker-compose --profile jobs build
```

If Compose fails with `invalid metadata: unexpected end of JSON input` (seen after Docker Desktop restarts), build images one-by-one:

```bat
cd infra
docker build -f images/worker/Dockerfile -t bmrg-worker:inf-w08 .
docker build -f images/ingest/Dockerfile -t bmrg-ingest:inf-w07 .
docker build -f images/features/Dockerfile -t bmrg-features:inf-w07 .
docker build -f images/trainer/Dockerfile -t bmrg-trainer:inf-w07 .
docker build -f images/scorer/Dockerfile -t bmrg-scorer:inf-w07 .
docker build -f images/eval/Dockerfile -t bmrg-eval:inf-w07 .
```

API image (from repo root):

```bat
docker build -f server/Dockerfile -t bmrg-api:local .
```

Client uses **npm** (`package-lock.json`). Prefer `npm run build` in `client/` until a pnpm lock is introduced.

---

## Architecture (target)

```text
MT5 VPS (EA)          Railway                         Vercel (paused)
─────────────         ─────────────────────────       ────────────────
BMRG chart attach  →  Postgres · Redis (plugins)
                      bmrg-api (server/)  ←──────────  client (later)
                      optional worker (infra/)
```

- **EA uptime** stays on MetaQuotes / Windows VPS — not Railway.
- **Railway** hosts INF data plane + the read API the console will call.
- **Vercel** hosts the static Vite SPA once UI work unpauses.

---

## 1. Railway — Postgres + Redis

1. Create a Railway project (e.g. `bmrg-infra`).
2. Add plugins / templates:
   - **PostgreSQL** (Postgres 16 class)
   - **Redis**
3. Note the generated variables (names vary by template):
   - `DATABASE_URL` or `POSTGRES_URL`
   - `REDIS_URL`
4. Map them onto the API service (next section) as:

| Service variable | Value |
| --- | --- |
| `BMRG_DATABASE_URL` | `${{Postgres.DATABASE_URL}}` (or paste; prefer `postgresql+psycopg2://…` / let SQLAlchemy accept `postgresql://`) |
| `BMRG_REDIS_URL` | `${{Redis.REDIS_URL}}` |

Local compose equivalents (dev only): `localhost:54329` postgres · `localhost:6379` redis — see `infra/.env.example`.

Optional schema migrate from a box with network access:

```bat
cd infra
set BMRG_DATABASE_URL=postgresql+psycopg2://...
alembic upgrade head
```

---

## 2. Railway — API service (`server/`)

Deploy **from the BMRG repo root** (Dockerfile copies `infra/`, `client/fixtures`, `blotter/CURRENT.md`).

### Config already in repo

| File | Role |
| --- | --- |
| `server/Dockerfile` | Slim Python 3.12 + uvicorn |
| `server/railway.toml` | Dockerfile builder · `/healthz` |
| `server/app/main.py` | Artefact map + DB/Redis probes |
| `server/.env.example` | Local env template |

### Steps

1. New Railway **service** in the same project → **GitHub repo** (or `railway up` from root).
2. Set **root directory** empty / repo root (not `server/`).
3. Builder: Dockerfile · path `server/Dockerfile` (or apply `server/railway.toml`).
4. Variables:

| Name | Example |
| --- | --- |
| `PORT` | Railway injects · default `8080` in image |
| `BMRG_DATA_ROOT` | `/data/bmrg` (image default) |
| `BMRG_DATABASE_URL` | `${{Postgres.DATABASE_URL}}` |
| `BMRG_REDIS_URL` | `${{Redis.REDIS_URL}}` |
| `BMRG_CORS_ORIGINS` | Local: `http://localhost:5173` · later add Vercel origin |

5. Generate a public domain (Railway → Settings → Networking).
6. Smoke:

```bat
curl https://<your-api>.up.railway.app/healthz
curl https://<your-api>.up.railway.app/api/baseline
```

`healthz` reports `db` / `redis` probe objects (`configured` / `ok`). Artefact routes mirror OpenAPI / Vite `fs_bridge`.

### Local API (without Railway)

```bat
cd server
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
set BMRG_DATA_ROOT=%CD%\..
uvicorn app.main:app --reload --port 8080
```

---

## 3. Railway — optional INF worker

Heavy train/eval jobs remain offline-box oriented. If you want a cloud worker later:

| File | Role |
| --- | --- |
| `infra/images/worker/Dockerfile` | RQ-style Redis list worker |
| `infra/railway.worker.toml` | Dockerfile pointer |

Create a **second** service with **root directory** `infra`, Dockerfile `images/worker/Dockerfile`, and the same Redis/Postgres variables. Not required for console reads.

Infra job images (ingest/features/trainer/scorer/eval/worker) build locally via:

```bat
cd infra
docker-compose --profile jobs build
```

---

## 4. Vercel — client (**PAUSED**)

Do **not** deploy the client until UI work settles. Prep is in place:

| File | Role |
| --- | --- |
| `client/vercel.json` | Vite SPA · `dist` · history fallback |
| `client/.env.example` | `VITE_API_BASE` |
| `client/src/api/client.ts` | Prefixes fetches with `VITE_API_BASE` |
| `client/vite.config.ts` | `fs_bridge` **dev only** |

### When unpaused

1. Import `client/` (or monorepo with Root Directory = `client`) into Vercel.
2. Framework: Vite · Build `npm run build` · Output `dist`.
3. Env (Production / Preview):

| Name | Value |
| --- | --- |
| `VITE_API_BASE` | `https://<bmrg-api>.up.railway.app` (no trailing slash) |

4. Add that Vercel origin to Railway `BMRG_CORS_ORIGINS`.
5. Deploy preview first; promote to production after a read-path smoke (Home · Performance · Live).

### Local client (current workflow)

```bat
cd client
npm install
npm run build
npm run dev
```

Leave `VITE_API_BASE` empty so Vite `fs_bridge` serves `/api/*` from disk.

---

## 5. Checklist

**Railway (do now)**

- [ ] Project created
- [ ] Postgres plugin
- [ ] Redis plugin
- [ ] `bmrg-api` service from `server/Dockerfile`
- [ ] Env vars linked
- [ ] `/healthz` and `/api/baseline` OK

**Vercel (later)**

- [ ] Pause lifted by operator
- [ ] Project linked to `client/`
- [ ] `VITE_API_BASE` set
- [ ] CORS updated on API
- [ ] Preview smoke of five pages

**Out of scope for these hosts**

- MT5 / EA / chart attach (MetaQuotes VPS)
- Enabling FT mutate (`AOS_LIVE_FT`)
- Order tickets / remote kill

---

## 6. Repo map

| Path | Deploy role |
| --- | --- |
| `server/` | Railway HTTP API |
| `infra/` | Compose · migrations · job images · optional worker |
| `client/` | Vercel SPA (paused) |
| `blotter/` | Pointer seed for API image (`CURRENT.md`) |
| `DEPLOYMENT.md` | This runbook |

Companions: `infra/BOX.md` · `infra/README.md` · `client/README.md` · `doc/project_report.md`.
