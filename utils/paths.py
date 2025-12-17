from __future__ import annotations

from datetime import datetime
from pathlib import Path

# 프로젝트 루트 기준 데이터 디렉토리 정의
ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
RESULTS_DIR = DATA_DIR / "results"
MODELS_DIR = DATA_DIR / "models"
META_DIR = DATA_DIR / "meta"
BACKUP_DIR = ROOT / "backups"

# 공통 파일 경로
LOG_PATH = META_DIR / "logs.jsonl"
RETRAIN_BUFFER_PATH = META_DIR / "retrain_buffer.jsonl"
CHECKPOINT_LOG = META_DIR / "checkpoints.log"
STATS_FILE = META_DIR / "stats.json"
SUMMARY_LATEST = RESULTS_DIR / "summary_latest.json"
ALL_RESULTS_FILE = RESULTS_DIR / "all_results.jsonl"

# 디렉토리 생성
for directory in (DATA_DIR, RESULTS_DIR, MODELS_DIR, META_DIR, BACKUP_DIR):
    directory.mkdir(parents=True, exist_ok=True)


def daily_results_file(ts: datetime | None = None) -> Path:
    """오늘 날짜 기준 JSONL 결과 파일 경로를 반환합니다."""
    ts = ts or datetime.utcnow()
    return RESULTS_DIR / f"{ts.strftime('%Y-%m-%d')}.jsonl"


def model_symlink_path() -> Path:
    return MODELS_DIR / "reward_latest.pkl"
