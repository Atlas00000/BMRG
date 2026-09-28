# bmrg-eval — INF-P5-T03 (base pin: IMAGE_LOCK.json python_base)
FROM python:3.12-slim
WORKDIR /infra
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY baselines ./baselines
COPY schemas ./schemas
COPY src ./src
COPY fixtures ./fixtures
ENV PYTHONUNBUFFERED=1
ENTRYPOINT ["python", "src/eval/run_p4b_e2e.py"]
