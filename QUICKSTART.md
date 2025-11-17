# 빠른 시작 가이드

## 현재 상태
서버가 포트 3000에서 실행 중이며 모든 기능이 정상 작동합니다.

## 주요 엔드포인트 테스트

### 1. 서버 상태 확인
```bash
curl http://localhost:3000/
curl http://localhost:3000/healthz
```

### 2. 테스트 데이터 생성
```bash
curl -X POST "http://localhost:3000/seed?n=30"
```

### 3. 모델 학습
```bash
curl -X POST http://localhost:3000/train
```

### 4. 예측 수행
```bash
curl -X POST http://localhost:3000/predict \
  -H "Content-Type: application/json" \
  -d '{"text":"새로운 강화학습 알고리즘에 대한 논문", "target":"reward", "explain":true}'
```

### 5. 데이터 추가
```bash
curl -X POST http://localhost:3000/ingest \
  -H "Content-Type: application/json" \
  -d '{"title":"연구 논문 제목", "text":"논문 요약 내용", "label": 1}'
```

### 6. 중복 확인
```bash
curl -X POST http://localhost:3000/check_duplicates \
  -H "Content-Type: application/json" \
  -d '{"titles":["논문 제목1", "논문 제목2"]}'
```

### 7. ArXiv에서 논문 자동 수집 (별도 터미널에서)
```bash
python collector.py
```

## 작동 흐름

1. **데이터 수집**: `/seed` 또는 `collector.py`로 논문 데이터 수집
2. **모델 학습**: `/train`으로 수집된 데이터 기반 학습
3. **예측**: `/predict`로 새로운 텍스트에 대해 reward 예측
4. **피드백 루프**: 예측 결과를 다시 학습 데이터로 활용

## 모델 관리

- 모델 파일: `models/reward_cls_YYYYMMDD_HHMMSS.pkl`
- 최신 모델: `models/reward_latest.pkl` (심볼릭 링크)
- 메트릭: `models/metrics_YYYYMMDD_HHMMSS.json`

## 로그 확인

- 실험 로그: `logs.jsonl`
- 재학습 버퍼: `retrain_buffer.jsonl`
