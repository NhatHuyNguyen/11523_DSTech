# ---- stage 1: builder (tools stay here and are discarded) ----
FROM python:3.11 AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip wheel --no-cache-dir --wheel-dir /wheels -r requirements.txt

# ---- stage 2: runtime (only what is needed to run) ----
FROM python:3.11-slim
WORKDIR /app
COPY --from=builder /wheels /wheels
RUN pip install --no-cache-dir --no-index /wheels/*
COPY app.py .
COPY model/ ./model/
COPY docker-compose.yml .
EXPOSE 8000
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]