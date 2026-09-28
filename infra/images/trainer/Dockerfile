# bmrg-trainer — INF-P5-T03 (base pin: IMAGE_LOCK.json python_base)
FROM python:3.12-slim
WORKDIR /infra
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY src ./src
ENV PYTHONUNBUFFERED=1
ENTRYPOINT ["python", "src/train/train_l2shadow.py"]
