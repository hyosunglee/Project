"""/data 폴더 자동 백업 스크립트"""
from __future__ import annotations

import os
import zipfile
from datetime import datetime
from pathlib import Path

from utils.meta import record_checkpoint
from utils.paths import BACKUP_DIR, DATA_DIR

BACKUP_DIR.mkdir(parents=True, exist_ok=True)


def create_backup() -> Path:
    ts = datetime.utcnow().strftime("%Y-%m-%d")
    backup_path = BACKUP_DIR / f"backup_{ts}.zip"

    with zipfile.ZipFile(backup_path, "w", compression=zipfile.ZIP_DEFLATED) as zipf:
        for path in DATA_DIR.rglob("*"):
            if path.is_file():
                arcname = Path("data") / path.relative_to(DATA_DIR)
                zipf.write(path, arcname)

    record_checkpoint(f"backup created at {backup_path}", category="backup")
    return backup_path


def upload_backup(_backup_path: Path):
    """
    업로드 훅 (예: Google Drive/iCloud API). 환경 변수나 토큰이 주어지면
    이 함수에 업로드 로직을 추가하세요.
    """
    token = os.getenv("BACKUP_UPLOAD_TOKEN")
    if not token:
        print("ℹ️ 업로드 건너뜀: BACKUP_UPLOAD_TOKEN 미설정")
        return False

    # TODO: 실제 업로드 구현 추가 (클라우드 SDK 또는 HTTP API 호출)
    print("⚠️ 업로드 로직이 구현되지 않았습니다. TODO를 채워주세요.")
    return False


if __name__ == "__main__":
    path = create_backup()
    print(f"✅ 백업 생성 완료: {path}")
    upload_backup(path)
