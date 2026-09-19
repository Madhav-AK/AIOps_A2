FROM python:3.12-slim AS builder
WORKDIR /app
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
COPY requirements.txt .
RUN pip install --no-cache-dir -U pip
RUN pip install --no-cache-dir -r requirements.txt


FROM python:3.12-slim AS runner
WORKDIR /app
COPY --from=builder /opt/venv /opt/venv
COPY predictor.py .
COPY data/model.joblib ./data/model.joblib
ENV MODEL_PATH=/app/data/model.joblib
ENV PATH="/opt/venv/bin:$PATH"
EXPOSE 8080
CMD ["uvicorn", "predictor:app", "--host", "0.0.0.0", "--port", "8080"]