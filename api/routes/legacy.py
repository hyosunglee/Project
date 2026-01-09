import os
import threading
import json
import random
import time
from datetime import datetime
from queue import Queue, Empty
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from apscheduler.schedulers.background import BackgroundScheduler
from models.feedback_trainer import train_model
from utils.logger import log_experiment, get_all_logged_titles
from utils.loop_logic import predict_after_training
from models.classifier import predict_reward
from utils.result_logger import save_result
from utils.loop_runner import run_loop_once
from utils.paths import ALL_RESULTS_FILE, LOG_PATH

router = APIRouter()

@router.get("/")
async def root():
    return {"status": "ok", "message": "Research Support API Running"}

@router.get("/healthz")
async def healthz():
    return {"status": "healthy"}

training_queue: Queue[str] = Queue()
training_thread_started = False
training_lock = threading.Lock()
train_min_interval = int(os.getenv("TRAIN_MIN_INTERVAL", "0"))

def enqueue_training(reason: str):
    training_queue.put(reason)

def _run_training_once(reason: str):
    with training_lock:
        print(f"\\n🔄 [AUTO-TRAIN] New data detected: {reason}")
        result = train_model()
        if result:
            save_result("training", result)
            print("📁 Training results saved.")
        predict_after_training()

def training_worker():
    last_train_time = 0.0
    while True:
        reason = training_queue.get()
        if reason is None:
            break
        while True:
            try:
                training_queue.get_nowait()
            except Empty:
                break
        if train_min_interval > 0:
            elapsed = time.monotonic() - last_train_time
            if elapsed < train_min_interval:
                time.sleep(train_min_interval - elapsed)
        _run_training_once(reason)
        last_train_time = time.monotonic()

def start_training_worker():
    global training_thread_started
    if training_thread_started:
        return
    thread = threading.Thread(target=training_worker, daemon=True)
    thread.start()
    training_thread_started = True

@router.post("/train")
async def trigger_training():
    print("\\n🚀 [TRAIN] Triggering model training based on logs (queued)")
    enqueue_training("manual")
    return {"message": "Training enqueued"}

class IngestRequest(BaseModel):
    title: str
    text: str
    label: int

@router.post("/ingest")
async def ingest_data(request: IngestRequest):
    try:
        log_experiment(request.dict())
        print(f"📥 [INGEST] Data received and saved: {request.title[:50]}...")
        enqueue_training("ingest")
        return {"message": "Data ingested successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to ingest data: {e}")

class DuplicatesRequest(BaseModel):
    titles: list[str]

@router.post("/check_duplicates")
async def check_duplicates(request: DuplicatesRequest):
    client_titles = set(request.titles)
    logged_titles = get_all_logged_titles()
    duplicates = list(client_titles.intersection(logged_titles))
    return {"duplicates": duplicates}

@router.post("/seed")
async def seed_logs(n: int = 30):
    for i in range(n):
        log_entry = {
            "title": f"Synthetic Seed Paper #{i}",
            "text": f"[SEED] synthetic text #{i}. This is a simulated paper summary about agents and policies.",
            "label": 1 if random.random() > 0.5 else 0
        }
        log_experiment(log_entry)
    return {"message": f"Seeded {n} logs"}

@router.post("/loop")
async def run_loop_endpoint():
    result = run_loop_once()
    if "error" in result:
        raise HTTPException(status_code=500, detail=result["error"])
    return result

def start_scheduler():
    """Starts the automation scheduler."""
    def scheduled_loop():
        result = run_loop_once()
        if result.get("collected", 0) > 0:
            enqueue_training("scheduled_collection")

    def one_time_init():
        """Runs initialization tasks on deployment."""
        print("\\n🚀 [INIT] Starting deployment initialization")
        if LOG_PATH.exists() and LOG_PATH.stat().st_size > 0:
            print("✅ [INIT] Existing log data found.")
            print("🎓 [INIT] Starting initial model training...")
            trigger_training()
        else:
            print("⚠️ [INIT] No log data found - seed data with /seed endpoint.")
        print("📚 [INIT] Starting the first paper collection...")
        run_loop_once()
        print("✅ [INIT] Initialization complete!")

    scheduler = BackgroundScheduler()
    scheduler.add_job(scheduled_loop, 'interval', minutes=10, id='paper_collection')

    if os.getenv("REPLIT_DEPLOYMENT") == "1":
        from datetime import datetime, timedelta
        run_time = datetime.now() + timedelta(seconds=60)
        scheduler.add_job(one_time_init, 'date', run_date=run_time, id='one_time_init')
        print("📅 Deployment environment detected - scheduling automatic initialization in 60 seconds.")

    scheduler.start()
    print("⏰ Automation scheduler started.")
    print("   - Paper collection: every 10 minutes.")
    print("   - Model training: on new data.")
