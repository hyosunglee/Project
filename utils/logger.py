import os
import json

LOG_PATH = "logs.jsonl"
# This check is a bit redundant if server.py also creates the dir, but it's safe.
if not os.path.exists(os.path.dirname(LOG_PATH)):
    # This will fail for root files, so let's be careful
    if os.path.dirname(LOG_PATH):
        os.makedirs(os.path.dirname(LOG_PATH))

if not os.path.exists(LOG_PATH):
    with open(LOG_PATH, "w") as f:
        pass # create empty file

def log_experiment(text, label):
    """Logs a new experiment to the JSONL file."""
    log_entry = {
        "text": text,
        "label": int(label)
    }
    with open(LOG_PATH, "a", encoding='utf-8') as f:
        f.write(json.dumps(log_entry, ensure_ascii=False) + "\n")
