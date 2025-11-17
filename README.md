# 자율 학습 AI 시스템

## 완전 자동화 시스템
- 논문 수집: 1시간마다 자동 실행
- 모델 학습: 6시간마다 자동 실행
- 모든 결과: JSON 파일로 자동 저장

## 결과 파일 위치
```
results/
├── collection_*.json      # 논문 수집 결과
├── training_*.json        # 모델 학습 결과  
├── prediction_*.json      # 예측 결과
└── all_results.jsonl      # 통합 결과 (모든 작업)
```

## 시스템 구조
```
logs.jsonl              # 수집된 모든 논문 데이터
models/                 # 학습된 모델 저장
  ├── reward_cls_*.pkl  # 버전별 모델
  └── reward_latest.pkl # 최신 모델 (심볼릭 링크)
```

## 자동 실행
서버가 시작되면 자동으로:
1. 초기 데이터 생성 (필요시)
2. 첫 모델 학습
3. 논문 수집 시작
4. 주기적 작업 스케줄링

## API (필요시)
```bash
curl http://localhost:3000/healthz        # 상태 확인
curl -X POST http://localhost:3000/loop   # 수동 논문 수집
curl -X POST http://localhost:3000/train  # 수동 학습
```

모든 작업은 자동으로 실행되며 결과는 `results/` 폴더에 JSON으로 저장됩니다.
