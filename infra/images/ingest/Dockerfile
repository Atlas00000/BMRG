# bmrg-ingest — INF-P5-T03 (base pin: IMAGE_LOCK.json python_base)
FROM python:3.12-slim
WORKDIR /infra
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY schemas ./schemas
COPY baselines ./baselines
COPY src ./src
COPY fixtures ./fixtures
ENV PYTHONUNBUFFERED=1
ENTRYPOINT ["python", "src/ingest/run_p2_e2e.py"]
