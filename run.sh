#!/usr/bin/env bash
set -euo pipefail

# 기본 설정
PORT="${PORT:-3000}"
LOG_DIR="${LOG_DIR:-logs}"
APP="server:app"        # gunicorn 대상 (server.py 안에 app 있어야 함)
THREADS="${THREADS:-4}"

mkdir -p "$LOG_DIR"

echo "[run] installing dependencies"
pip install -r requirements.txt

echo "[run] killing stale listeners on :$PORT"
fuser -k ${PORT}/tcp 2>/dev/null || true
pkill -f "debug_wsgi|wsgiref|debug_flask|gunicorn" 2>/dev/null || true

echo "[run] limiting BLAS threads"
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 MALLOC_ARENA_MAX=2

echo "[run] starting gunicorn on :$PORT"
PYTHONFAULTHANDLER=1 PYTHONUNBUFFERED=1 \
python -m gunicorn -w 1 -k gthread --threads ${THREADS} -t 120 \
  -b 0.0.0.0:${PORT} "$APP" \
  --log-level info --capture-output \
  --access-logfile "$LOG_DIR/access.log" --error-logfile "$LOG_DIR/error.log" &

PID=$!
echo "[run] pid=$PID"

# 건강검진: /healthz 30초 대기
echo -n "[run] waiting healthz "
for i in {1..30}; do
  if curl -sf --ipv4 "http://127.0.0.1:${PORT}/healthz" >/dev/null; then
    echo "OK"
    exit 0
  fi
  echo -n "."
  sleep 1
done

echo
echo "[run] health check failed, dumping last logs:"
tail -n 100 "$LOG_DIR/error.log" || true
exit 1
