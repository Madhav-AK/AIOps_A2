from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

import os, socket
import redis
import joblib
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

MODEL_PATH = os.environ.get("MODEL_PATH", str(BASE_DIR / "data/model.joblib"))
POD_NAME = os.environ.get("POD_NAME", socket.gethostname())
NODE_NAME = os.environ.get("NODE_NAME", "unknown")

redis_cache = redis.Redis(
    host=os.environ.get("REDIS_HOST"),
    port=6379,
    decode_responses=True
)
CACHE_TTL = 500


app = FastAPI(title="TfidfVectorizer + MultinomialNB Classifier")
_bundle = None


@app.on_event("startup")
def load_model():
    global _bundle
    _bundle = joblib.load(MODEL_PATH)
    print(f"Loaded model on pod={POD_NAME} node={NODE_NAME}")


class PredictRequest(BaseModel):
    text: str


@app.get("/healthz")
def healthz():
    return {"status": "ok", "pod": POD_NAME, "node": NODE_NAME}


@app.post("/predict")
def predict(request: PredictRequest):
    if _bundle is None:
        raise HTTPException(status_code=503, detail="Model not loaded yet")

    cached_label = redis_cache.get(request.text)
    if cached_label is not None:
        return {"label": cached_label}

    model = _bundle["model"]
    label = str(model.predict([request.text])[0])
    redis_cache.set(request.text, label, ex=CACHE_TTL)
    return {"label": label}