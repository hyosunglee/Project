

curl http://localhost:3000/           # 서버 상태
curl http://localhost:3000/healthz    # 헬스체크

# 논문 수집 (1회 실행)
curl -X POST http://localhost:3000/loop

# 모델 학습
curl -X POST http://localhost:3000/train

# 예측
curl -X POST http://localhost:3000/predict \
  -H "Content-Type: application/json" \
  -d '{"text":"your text here"}'

# 텍스트 생성
curl -X POST http://localhost:3000/generate \
  -H "Content-Type: application/json" \
  -d '{"prompt":"Research summary:"}'

# 테스트 데이터 생성
curl -X POST "http://localhost:3000/seed?n=30"

# 새 데이터 추가
curl -X POST http://localhost:3000/ingest \
  -H "Content-Type: application/json" \
  -d '{"text":"...", "label":1}'

# 중복 체크
curl -X POST http://localhost:3000/check_duplicates