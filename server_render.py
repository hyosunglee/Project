import os
import httpx
from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI(title="Self-Learning API (Render Gateway)")

# 맥미니 주소 (ngrok 연결 후 여기에 입력)
MAC_MINI_URL = os.getenv("MAC_MINI_URL", "")

@app.get("/")
async def root():
    return {"status": "running", "mode": "gateway"}

@app.get("/healthz")
async def health():
    return {"status": "ok"}

@app.post("/predict")
async def predict(payload: dict):
    if not MAC_MINI_URL:
        return JSONResponse({"error": "Mac mini not connected"}, status_code=503)
    async with httpx.AsyncClient(timeout=30) as client:
        r = await client.post(f"{MAC_MINI_URL}/predict", json=payload)
        return r.json()

@app.post("/train")
async def train():
    if not MAC_MINI_URL:
        return JSONResponse({"error": "Mac mini not connected"}, status_code=503)
    async with httpx.AsyncClient(timeout=60) as client:
        r = await client.post(f"{MAC_MINI_URL}/train")
        return r.json()

@app.post("/loop")
async def loop():
    if not MAC_MINI_URL:
        return JSONResponse({"error": "Mac mini not connected"}, status_code=503)
    async with httpx.AsyncClient(timeout=60) as client:
        r = await client.post(f"{MAC_MINI_URL}/loop")
        return r.json()

@app.post("/seed")
async def seed(n: int = 10):
    if not MAC_MINI_URL:
        return JSONResponse({"error": "Mac mini not connected"}, status_code=503)
    async with httpx.AsyncClient(timeout=30) as client:
        r = await client.post(f"{MAC_MINI_URL}/seed?n={n}")
        return r.json()
