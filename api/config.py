import os
from pathlib import Path

PORT = os.getenv("PORT", 3000)
HOST = os.getenv("HOST", "0.0.0.0")
TIMEOUT = os.getenv("TIMEOUT", 60)
FEEDBACK_PATH = Path(os.getenv("FEEDBACK_PATH", "feedback/feedback_data.jsonl"))
