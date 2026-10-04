# BMRG server (read API)

FastAPI surface that mirrors the Vite `fs_bridge` artefact map for Railway.

## Local

```bat
cd server
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
pip install SQLAlchemy==2.0.36
set BMRG_DATA_ROOT=..
uvicorn app.main:app --reload --port 8080
```

Health: `GET http://127.0.0.1:8080/healthz`

## Railway

Deploy from **repo root** using `server/Dockerfile` + `server/railway.toml`.  
See [`../DEPLOYMENT.md`](../DEPLOYMENT.md).
