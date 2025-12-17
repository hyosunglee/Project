import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict

from utils.paths import CHECKPOINT_LOG, STATS_FILE

CHECKPOINT_LOG.parent.mkdir(parents=True, exist_ok=True)
STATS_FILE.parent.mkdir(parents=True, exist_ok=True)


def _load_stats() -> Dict[str, Any]:
    if STATS_FILE.exists():
        try:
            return json.loads(STATS_FILE.read_text(encoding="utf-8"))
        except Exception:
            pass
    return {"counts": {}, "last_updated": None}


def _write_stats(stats: Dict[str, Any]):
    stats["last_updated"] = datetime.utcnow().isoformat()
    STATS_FILE.write_text(json.dumps(stats, ensure_ascii=False, indent=2), encoding="utf-8")


def increment_stat(group: str, key: str, amount: int = 1):
    stats = _load_stats()
    counts = stats.setdefault("counts", {})
    group_counts = counts.setdefault(group, {})
    group_counts[key] = group_counts.get(key, 0) + amount
    _write_stats(stats)


def record_checkpoint(message: str, category: str = "general"):
    ts = datetime.utcnow().isoformat()
    line = f"[{ts}] ({category}) {message}\n"
    with open(CHECKPOINT_LOG, "a", encoding="utf-8") as f:
        f.write(line)
