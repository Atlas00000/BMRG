# BMRG read API — Railway service (Postgres/Redis optional probes)
FROM python:3.12-slim

WORKDIR /app

ENV PYTHONUNBUFFERED=1 \
    PORT=8080 \
    BMRG_DATA_ROOT=/data/bmrg

COPY server/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# App code
COPY server/app /app/app

# Seed read paths the console needs (fixtures + frozen baseline + common reports)
COPY infra/baselines /data/bmrg/infra/baselines
COPY infra/artefacts /data/bmrg/infra/artefacts
COPY infra/fixtures /data/bmrg/infra/fixtures
COPY infra/INF-P6-T02_skip_audit.md /data/bmrg/infra/INF-P6-T02_skip_audit.md
COPY client/fixtures /data/bmrg/client/fixtures
COPY blotter/CURRENT.md /data/bmrg/blotter/CURRENT.md

EXPOSE 8080
CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8080}"]
