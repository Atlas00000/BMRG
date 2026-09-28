# bmrg-worker — INF-P5-T04 Redis list worker
FROM python:3.12-slim
WORKDIR /infra
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY baselines ./baselines
COPY schemas ./schemas
COPY src ./src
COPY fixtures ./fixtures
ENV PYTHONUNBUFFERED=1
ENV BMRG_REDIS_URL=redis://redis:6379/0
ENTRYPOINT ["python", "src/jobqueue/worker.py"]
