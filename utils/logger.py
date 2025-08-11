import json
import os

LOG_FILE = "logs/experiment_logs.json"

def log_experiment(title, summary, keywords, idea, code, result, reward):
    """Appends a new experiment log to the log file."""
    log_entry = {
        "title": title,
        "summary": summary,
        "keywords": keywords,
        "idea": idea,
        "code": code,
        "result": result,
        "reward": reward,
    }

    logs = []
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r") as f:
            try:
                logs = json.load(f)
            except json.JSONDecodeError:
                logs = []

    logs.append(log_entry)

    with open(LOG_FILE, "w") as f:
        json.dump(logs, f, indent=4)


def is_duplicate(title):
    """Checks if a log with the given title already exists."""
    if not os.path.exists(LOG_FILE):
        return False

    with open(LOG_FILE, "r") as f:
        try:
            logs = json.load(f)
        except json.JSONDecodeError:
            return False

    for log in logs:
        if log.get("title") == title:
            return True

    return False
