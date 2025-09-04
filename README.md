### Project — Predict API Bootstrap


핵심 역할
	•	자동 실험 파이프라인 + 예측 API 자동화 시스템
	•	주요 흐름:
	1.	/seed: 테스트용 로그 데이터를 자동 생성
	2.	/train: 로그 기반으로 Reward 예측 모델 학습 (로지스틱 회귀)
	3.	models/reward_latest.pkl: 최신 버전 모델을 심볼릭 링크로 관리
	4.	/predict: 주어진 텍스트에 대해 학습된 모델이 reward 예측, 확률 반환

주요 구성 파일
	•	server.py — Flask 서버 엔트리, 라우팅 정의 (seed, train, predict, loop 등)
	•	utils/model_trainer.py — 데이터 로딩, 텍스트 + reward 추출, 모델 학습 + 저장
	•	utils/logger.py — 실험 로그(논문, 요약, 아이디어 등 포함) 기록 및 중복 체크
	•	api_predict.py — 예측 API, Pydantic 스키마 검증 및 결과 응답(stub 설명 포함)
	•	replit.nix / .replit / requirements.txt — Replit 및 로컬 환경 실행용 설정

동작 흐름
	•	개발/테스트: curl -X POST /seed?n=30 → /train → /predict
	•	운영 자동화: /loop 주기 실행 (논문 기반 실험 데이터 자동 수집)

⸻

요약

구성 요소	설명
서버 실행	Flask 기반, /seed, /train, /predict, /loop 제공
모델	Tfidf + LogisticRegression, 로그 기반 reward 예측
저장 구조	models/ 폴더, 모델 버저닝(reward_cls_TIMESTAMP.pkl) + reward_latest.pkl 심볼릭 링크
배포 환경	Replit 지원 (Nix 환경 세팅 포함), pip 타임아웃 문제 회피 대응


⸻



## Quickstart
1) **Replit**: `replit.nix` 저장 후 **Run**
2) **로컬**: Python 3.11 + `pip install -r requirements.txt`
3) 서버 실행: `python server.py`
4) 시드 주입: `POST /seed?n=30`
5) 학습: `POST /train`
6) 예측: `POST /predict {"text":"...","target":"reward","explain":true}`

### 엔드포인트
- `GET /` 헬스체크
- `POST /seed?n=N` 더미 로그 N건 생성(개발용)
- `POST /train` 로그 기반 모델 학습(버저닝+latest)
- `POST /predict` 예측(JSON 스키마 검증/확률/버전/설명 스텁)

### 명령어
curl -X POST "http://localhost:3000/seed?n=30"
curl -X POST http://localhost:3000/train
curl -X POST http://localhost:3000/predict \
  -H "Content-Type: application/json" \
  -d '{"text":"새로운 RL 아이디어와 실험 요약...", "target":"reward", "explain":true}'



### (운영 요령)

데이터 쌓기: /ingest(수집기에서 자동 호출)

주기 학습: 하루 1회 /train (또는 GitHub Actions/cron으로 밤마다)

예측 API: /predict

사람 교정: /feedback → 다음 학습 때 자동 반영

임계치 예시: LOW_CONF_THRESHOLD=0.6 잡으면 0.6 미만은 “재학습 후보”

