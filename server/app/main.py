"""BMRG read API — Railway-ready FastAPI surface over INF artefacts."""

from __future__ import annotations

import os
from pathlib import Path

import redis
from fastapi import FastAPI, Query, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, PlainTextResponse, Response
from sqlalchemy import create_engine, text

from .artefacts import ARTEFACT_FILES, content_type, resolve_bmrg_root, resolve_path

BMRG_ROOT = resolve_bmrg_root(os.environ.get("BMRG_DATA_ROOT"))
DATABASE_URL = os.environ.get("BMRG_DATABASE_URL") or os.environ.get("DATABASE_URL")
REDIS_URL = os.environ.get("BMRG_REDIS_URL") or os.environ.get("REDIS_URL")
CORS_ORIGINS = [
    o.strip()
    for o in os.environ.get("BMRG_CORS_ORIGINS", "http://localhost:5173,http://127.0.0.1:5173").split(",")
    if o.strip()
]

app = FastAPI(
    title="BMRG Artefact API",
    version="0.1.0",
    description="Read-first contracts for the operator console. No order placement.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS if "*" not in CORS_ORIGINS else ["*"],
    allow_credentials=True,
    allow_methods=["GET", "HEAD", "OPTIONS"],
    allow_headers=["*"],
)


def _probe_db() -> dict:
    if not DATABASE_URL:
        return {"configured": False, "ok": None}
    url = DATABASE_URL
    if url.startswith("postgresql://"):
        url = url.replace("postgresql://", "postgresql+psycopg2://", 1)
    try:
        engine = create_engine(url, pool_pre_ping=True)
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return {"configured": True, "ok": True}
    except Exception as exc:  # noqa: BLE001 — surface probe detail
        return {"configured": True, "ok": False, "detail": str(exc)[:200]}


def _probe_redis() -> dict:
    if not REDIS_URL:
        return {"configured": False, "ok": None}
    try:
        client = redis.from_url(REDIS_URL, socket_connect_timeout=2)
        client.ping()
        return {"configured": True, "ok": True}
    except Exception as exc:  # noqa: BLE001
        return {"configured": True, "ok": False, "detail": str(exc)[:200]}


@app.get("/healthz")
def healthz() -> dict:
    db = _probe_db()
    r = _probe_redis()
    return {
        "status": "ok",
        "service": "bmrg-api",
        "data_root": str(BMRG_ROOT),
        "db": db,
        "redis": r,
    }


@app.get("/api/healthz")
def api_healthz() -> dict:
    return healthz()


@app.api_route("/api/{path:path}", methods=["GET", "HEAD"])
def serve_artefact(path: str, request: Request, magic: int | None = Query(default=None)) -> Response:
    del magic  # reserved for ledger adapters; file map ignores query
    url = "/api/" + path.rstrip("/")
    # Keep trailing-path keys exact as map (no strip of known full keys)
    if url not in ARTEFACT_FILES and not path:
        url = "/api/"
    ref = ARTEFACT_FILES.get(url)
    if ref is None:
        # try without collapsing (path may include nested)
        ref = ARTEFACT_FILES.get("/api/" + path)
    if ref is None:
        return JSONResponse(
            status_code=404,
            content={"error": "unknown_route", "path": url, "detail": "Not in artefact map."},
        )

    file_path: Path = resolve_path(BMRG_ROOT, ref)
    if not file_path.exists():
        return JSONResponse(
            status_code=404,
            content={
                "error": "artefact_missing",
                "path": str(file_path.relative_to(BMRG_ROOT)).replace("\\", "/"),
                "detail": "Drop or generate the INF artefact, then reload.",
            },
        )

    try:
        raw = file_path.read_bytes()
    except OSError as exc:
        return JSONResponse(
            status_code=500,
            content={"error": "read_failed", "path": str(file_path), "detail": str(exc)},
        )

    if request.method == "HEAD":
        return Response(status_code=200, media_type=content_type(ref.kind))

    text = raw.decode("utf-8")
    if ref.kind in {"csv", "md", "jsonl"}:
        return PlainTextResponse(text, media_type=content_type(ref.kind))
    return Response(content=text, media_type=content_type(ref.kind))
