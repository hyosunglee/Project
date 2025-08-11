import os, json

LOG_PATH = "logs/experiment_log.json"
os.makedirs("logs", exist_ok=True)
if not os.path.exists(LOG_PATH):
    with open(LOG_PATH, "w") as f:
        json.dump([], f)

def _load():
    with open(LOG_PATH, "r") as f:
        return json.load(f)

def _save(data):
    with open(LOG_PATH, "w") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def is_duplicate(title: str) -> bool:
    try:
        logs = _load()
        return any(item.get("paper_title") == title for item in logs)
    except Exception:
        return False

def log_experiment(title, summary, keywords, idea, code, result, reward):
    logs = _load()
    logs.append({
        "paper_title": title,
        "paper_summary": summary,
        "keywords": keywords,
        "idea": idea,
        "code": code,
        "result": result,
        "reward": reward
    })
    _save(logs)
