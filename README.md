# Project — Predict API Bootstrap

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
