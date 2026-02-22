import os
import httpx
from fastapi import FastAPI, Header, HTTPException
from fastapi.responses import JSONResponse

app = FastAPI(title="Self-Learning API (Render Gateway)")

MAC_MINI_URL = os.getenv("MAC_MINI_URL", "")
API_KEY = os.getenv("API_KEY", "")

def verify_key(x_api_key: str = Header(None)):
    if not API_KEY:
        return  # 환경변수 미설정 시 개발 모드
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")

@app.get("/")
async def root():
    return {"status": "running", "mode": "gateway"}

@app.get("/healthz")
async def health():
    return {"status": "ok"}

@app.post("/predict")
async def predict(payload: dict, _ = Header(None, alias="x-api-key")):
    verify_key(_)
    if not MAC_MINI_URL:
        return JSONResponse({"error": "Mac mini not connected"}, status_code=503)
    async with httpx.AsyncClient(timeout=30) as client:
        r = await client.post(f"{MAC_MINI_URL}/predict", json=payload)
        return r.json()

@app.post("/train")
async def train(_ = Header(None, alias="x-api-key")):
    verify_key(_)
    if not MAC_MINI_URL:
        return JSONResponse({"error": "Mac mini not connected"}, status_code=503)
    async with httpx.AsyncClient(timeout=60) as client:
        r = await client.post(f"{MAC_MINI_URL}/train")
        return r.json()

@app.post("/loop")
async def loop(_ = Header(None, alias="x-api-key")):
    verify_key(_)
    if not MAC_MINI_URL:
        return JSONResponse({"error": "Mac mini not connected"}, status_code=503)
    async with httpx.AsyncClient(timeout=60) as client:
        r = await client.post(f"{MAC_MINI_URL}/loop")
        return r.json()

@app.post("/seed")
async def seed(n: int = 10, _ = Header(None, alias="x-api-key")):
    verify_key(_)
    if not MAC_MINI_URL:
        return JSONResponse({"error": "Mac mini not connected"}, status_code=503)
    async with httpx.AsyncClient(timeout=30) as client:
        r = await client.post(f"{MAC_MINI_URL}/seed?n={n}")
        return r.json()
