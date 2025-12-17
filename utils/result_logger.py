import json
from datetime import datetime
from pathlib import Path

from utils.meta import increment_stat, record_checkpoint
from utils.paths import ALL_RESULTS_FILE, RESULTS_DIR, SUMMARY_LATEST, daily_results_file

RESULTS_DIR.mkdir(parents=True, exist_ok=True)


def _write_json(filepath: Path, payload: dict):
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)


def save_result(result_type: str, data: dict) -> Path:
    """
    결과를 저장하고 일별 JSONL, 통합 로그, 요약 파일을 관리합니다.

    Returns:
        Path: 단일 결과 JSON 파일 경로 (타임스탬프 포함)
    """
    now = datetime.utcnow()
    timestamp = now.strftime("%Y%m%d_%H%M%S")
    entry = {
        "timestamp": now.isoformat(),
        "type": result_type,
        "data": data,
    }

    # 1) 개별 JSON (기존 호환)
    result_file = RESULTS_DIR / f"{result_type}_{timestamp}.json"
    _write_json(result_file, entry)

    # 2) 일별 JSONL
    daily_file = daily_results_file(now)
    with open(daily_file, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")

    # 3) 통합 JSONL (전체 기록)
    with open(ALL_RESULTS_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")

    # 4) 요약 최신본
    if result_type == "summary":
        _write_json(SUMMARY_LATEST, entry)

    increment_stat("results", result_type)
    record_checkpoint(f"saved {result_type} -> {result_file}", category="results")

    return result_file
