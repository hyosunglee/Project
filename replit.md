# Self-Learning Feedback Loop API

## Overview
This project is an AI-powered self-learning feedback loop system that automatically collects research papers from ArXiv, trains machine learning models, and makes predictions. The system continuously improves itself through a feedback loop.

## Recent Changes (November 17, 2025)
- Installed Python 3.11 environment
- Set up all dependencies (Flask, scikit-learn, arxiv, etc.)
- Configured workflow to run server on port 3000
- Server is operational and accessible

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
The server runs automatically on port 3000 via the configured workflow.

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
- ✅ Server is running and functional on port 3000
- ✅ All dependencies installed (Flask, scikit-learn, arxiv, gunicorn, etc.)
- ✅ Ready for data collection and model training
- ✅ Workflow configured for automatic server startup
- ✅ All API endpoints tested and working
- ✅ Model training pipeline functional
- ✅ Prediction API operational
- ✅ Data ingestion and duplicate checking working

## User Preferences
- Language: Korean and English mixed
- Development environment: Replit
- Port: 3000 (API server)
