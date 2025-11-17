# Self-Learning Feedback Loop API

## Overview
This project is an AI-powered self-learning feedback loop system that automatically collects research papers from ArXiv, trains machine learning models, and makes predictions. The system continuously improves itself through a feedback loop.

## Recent Changes (November 17, 2025)
- ✅ 다양한 논문 수집 시스템 구축 완료
- ✅ 10개 AI 주제 키워드 순환 시스템 (reinforcement learning, deep learning, computer vision 등)
- ✅ 논문 수집량 증가: 10개 → 30개 (3배 증가)
- ✅ 실제 ArXiv 논문: 7개 → 33개로 증가
- ✅ 자동화 스케줄러 작동 중 (1시간마다 다른 주제로 수집)

## Project Architecture
- **Backend**: Flask-based REST API
- **ML Stack**: scikit-learn with TF-IDF vectorization and Logistic Regression
- **Data Storage**: JSONL format for logs and experiments
- **Model Management**: Versioned models with symlink to latest

### Key Components
- `server.py` - Main Flask application with API endpoints
- `utils/trainer.py` - Model training logic
- `utils/logger.py` - Experiment logging and duplicate checking
- `utils/paper_fetcher.py` - ArXiv paper collection
- `api_predict.py` - Prediction API blueprint
- `collector.py` - Standalone script for paper collection

## API Endpoints
- `GET /` - Health check
- `GET /healthz` - Service status
- `POST /seed?n=N` - Generate N test log entries
- `POST /train` - Train model based on collected logs
- `POST /predict` - Make predictions on new text
- `POST /ingest` - Add new data to the system
- `POST /loop` - Execute one cycle of the feedback loop
- `POST /check_duplicates` - Check for duplicate paper titles

## Running the Project
The server runs automatically on port 5000 via the configured workflow with webview enabled.

### Web UI
Open the webview pane to access the interactive web interface where you can:
- Check server status
- Generate test data
- Train models
- Make predictions
- Add new data
- Check for duplicates

All features are accessible through an easy-to-use web interface with buttons and forms.

### Manual Commands
```bash
# Install dependencies
pip install -r requirements.txt

# Run server
PORT=3000 python server.py

# Generate test data
curl -X POST "http://localhost:3000/seed?n=30"

# Train model
curl -X POST http://localhost:3000/train

# Make prediction
curl -X POST http://localhost:3000/predict \
  -H "Content-Type: application/json" \
  -d '{"text":"New RL idea...", "target":"reward", "explain":true}'
```

## Current State
- ✅ 완전 자동화 시스템 작동 중
- ✅ 포트 3000에서 서버 실행
- ✅ 1시간마다 자동 논문 수집
- ✅ 6시간마다 자동 모델 재학습
- ✅ 모든 결과 JSON 파일로 자동 저장
- ✅ results/ 폴더에 결과 저장

## User Preferences
- Language: Korean and English mixed
- Development environment: Replit
- Port: 5000 (Web UI + API server)
- Interface: Web UI for easy interaction

## Files Added
- `static/index.html` - Interactive web UI for all API functions
- `test_api.py` - Python script to test all API endpoints
- `QUICKSTART.md` - Korean quickstart guide
