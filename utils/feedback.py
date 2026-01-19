# utils/feedback.py

import json
from typing import List, Dict
from datetime import datetime
from pathlib import Path
from api.config import FEEDBACK_PATH

def log_feedback(feedback_entry: dict) -> None:
    """
    Saves a structured feedback entry to a JSONL file.

    Args:
        feedback_entry: A dictionary containing the feedback data.

    Raises:
        ValueError: If required fields are missing.
        IOError: If there is an issue writing to the file.
    """
    required_fields = ["text", "prediction", "user_label", "correct"]
    if not all(field in feedback_entry for field in required_fields):
        missing = [field for field in required_fields if field not in feedback_entry]
        raise ValueError(f"Missing required fields: {', '.join(missing)}")

    # Add timestamp and ensure source is set
    feedback_entry["timestamp"] = datetime.utcnow().isoformat()
    feedback_entry.setdefault("source", "user")

    try:
        # Ensure the directory exists
        FEEDBACK_PATH.parent.mkdir(parents=True, exist_ok=True)
        with open(FEEDBACK_PATH, "a", encoding="utf-8") as f:
            f.write(json.dumps(feedback_entry, ensure_ascii=False) + "\n")
    except (IOError, TypeError) as e:
        # Log the error appropriately in a real application
        print(f"Error logging feedback: {e}")
        raise

def load_feedback() -> List[Dict]:
    """
    Loads all feedback entries from the JSONL file.

    Returns:
        A list of feedback entries.
    """
    if not FEEDBACK_PATH.exists():
        return []

    entries = []
    try:
        with open(FEEDBACK_PATH, "r", encoding="utf-8") as f:
            for line in f:
                try:
                    entries.append(json.loads(line))
                except json.JSONDecodeError:
                    # Skip corrupted lines
                    print(f"Warning: Could not decode line: {line.strip()}")
                    continue
        return entries
    except IOError as e:
        print(f"Error loading feedback: {e}")
        return []
