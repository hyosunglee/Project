import json
from pathlib import Path

from utils.paths import LOG_PATH

# Ensure the log file exists
LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
Path(LOG_PATH).touch(exist_ok=True)


def log_experiment(log_data: dict):
    """Logs a new experiment dictionary to the JSONL file."""
    if not isinstance(log_data, dict):
        raise TypeError("log_data must be a dictionary.")

    with open(LOG_PATH, "a", encoding="utf-8") as f:
        f.write(json.dumps(log_data, ensure_ascii=False) + "\n")


def get_all_logged_titles() -> set:
    """
    Reads the log file and returns a set of all 'title' fields.
    This is used for efficient duplicate checking.
    """
    titles = set()
    if not LOG_PATH.exists():
        return titles

    with open(LOG_PATH, "r", encoding="utf-8") as f:
        for line in f:
            try:
                log_entry = json.loads(line)
                if isinstance(log_entry, dict) and "title" in log_entry:
                    titles.add(log_entry["title"])
            except json.JSONDecodeError:
                # Ignore corrupted lines
                continue
    return titles
