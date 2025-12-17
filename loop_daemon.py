"""24/7 루프 실행기: 30분 간격으로 run_loop_once 수행"""
from __future__ import annotations

import os
import time
from datetime import datetime

from utils.loop_runner import run_loop_once
from utils.meta import record_checkpoint


def run_forever(interval_seconds: int = 1800):
    while True:
        start = datetime.utcnow()
        result = run_loop_once()
        if "error" in result:
            record_checkpoint(f"loop failed: {result['error']}", category="loop_error")
        else:
            record_checkpoint(
                f"loop ok (collected={result.get('collected', 0)}) in {(datetime.utcnow() - start).total_seconds():.1f}s",
                category="loop",
            )
        time.sleep(interval_seconds)


if __name__ == "__main__":
    interval = int(float(os.getenv("LOOP_INTERVAL", 1800)))
    run_forever(interval)
