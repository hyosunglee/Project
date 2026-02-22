

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




# Self‑Learning Feedback Loop API 프로젝트 개요

## Overview

The **Self‑Learning Feedback Loop API** is an AI‑powered system that automates the process of collecting research papers, training machine‑learning models and making predictions.  According to the project overview, it continuously pulls articles from the ArXiv database, applies training routines and uses the results to refine the next iteration [oai_citation:0‡raw.githubusercontent.com](https://raw.githubusercontent.com/hyosunglee/Project/main/replit.md#:~:text=,itself%20through%20a%20feedback%20loop).  This feedback loop enables the system to self‑improve over time, allowing users to focus on research insights rather than manual data gathering.

### Key goals

- **Automated paper collection:** The system periodically fetches new papers from ArXiv and maintains a growing log of research texts [oai_citation:1‡raw.githubusercontent.com](https://raw.githubusercontent.com/hyosunglee/Project/main/replit.md#:~:text=,%EC%9D%B4%EB%AF%B8%20%EC%88%98%EC%A7%91%EB%90%9C%20%EB%85%BC%EB%AC%B8%EC%9D%80%20%EC%9E%90%EB%8F%99%EC%9C%BC%EB%A1%9C%20%ED%95%84%ED%84%B0%EB%A7%81).
- **Self‑learning model training:** Collected logs are used to train a TF‑IDF–based logistic regression classifier and a GPT‑2 summarizer [oai_citation:2‡raw.githubusercontent.com](https://raw.githubusercontent.com/hyosunglee/Project/main/replit.md#:~:text=%23%23%20Project%20Architecture%20,models%20with%20symlink%20to%20latest).  The models are retrained on a schedule and after new data is ingested [oai_citation:3‡raw.githubusercontent.com](https://raw.githubusercontent.com/hyosunglee/Project/main/replit.md#:~:text=,%EC%9D%B4%EB%AF%B8%20%EC%88%98%EC%A7%91%EB%90%9C%20%EB%85%BC%EB%AC%B8%EC%9D%80%20%EC%9E%90%EB%8F%99%EC%9C%BC%EB%A1%9C%20%ED%95%84%ED%84%B0%EB%A7%81).
- **Prediction & summarisation:** Users can submit text to the API to obtain a reward prediction; for high‑confidence positive predictions (≥80 %) the system also generates a short summary using GPT‑2 [oai_citation:4‡raw.githubusercontent.com](https://raw.githubusercontent.com/hyosunglee/Project/main/api/routes/predict.py#:~:text=if%20result.get%28,100%5D).  Predictions and summaries are saved to results files for later review.

## Recent changes

The repository is actively maintained.  Recent updates highlight significant refactoring and feature improvements:

| 날짜 | 변경 내용 (요약) | 근거 |
|---|---|---|
| **2026‑01‑29** | Added a `Dockerfile` for containerized deployment.  The commit log from 29 Jan 2026 shows this change [oai_citation:5‡api.github.com](https://api.github.com/repos/hyosunglee/Project/commits/1415a7aea92531912260c2bc4693df87b8f3ef11#:~:text=,). | Commit history |
| **2026‑01‑09** | **System rebuild:** migration from Flask to FastAPI/uvicorn; restructured model modules (classifier, summarizer, feedback trainer); updated `generate_paper_summary()` to support `max_length` and `max_new_tokens`; verified the automatic generation pipeline (5/5 success); at this stage the system made 196 predictions, with 136 high‑confidence (>80 %) cases and generated five summaries [oai_citation:6‡raw.githubusercontent.com](https://raw.githubusercontent.com/hyosunglee/Project/main/replit.md#:~:text=,2%20%EC%9A%94%EC%95%BD%20%EC%83%9D%EC%84%B1). | Project notes |
| **2025‑12‑17** | Introduced an automated prediction‑to‑generation pipeline.  After training, the system now automatically predicts across the entire dataset and generates GPT‑2 summaries for the top high‑confidence predictions; results are saved to JSON files [oai_citation:7‡raw.githubusercontent.com](https://raw.githubusercontent.com/hyosunglee/Project/main/replit.md#:~:text=,wisdom%29%20%EB%B6%80%EC%8A%A4%ED%8C%85).  Integration with a “VirtueEngine” boosts the model based on complexity [oai_citation:8‡raw.githubusercontent.com](https://raw.githubusercontent.com/hyosunglee/Project/main/replit.md#:~:text=,wisdom%29%20%EB%B6%80%EC%8A%A4%ED%8C%85). | Project notes |
| **2025‑11‑17** | Improved the paper collection subsystem.  The ArXiv API client was rewritten, error logging and retry logic were added, and a new alternation strategy cycles between relevance‑sorted and newest papers [oai_citation:9‡raw.githubusercontent.com](https://raw.githubusercontent.com/hyosunglee/Project/main/replit.md#:~:text=,%EC%9D%B4%EB%AF%B8%20%EC%88%98%EC%A7%91%EB%90%9C%20%EB%85%BC%EB%AC%B8%EC%9D%80%20%EC%9E%90%EB%8F%99%EC%9C%BC%EB%A1%9C%20%ED%95%84%ED%84%B0%EB%A7%81).  The number of keywords increased from 10 to 30 and the system now collects 63 real papers.  A scheduler fetches papers on an hourly rotation and filters duplicates [oai_citation:10‡raw.githubusercontent.com](https://raw.githubusercontent.com/hyosunglee/Project/main/replit.md#:~:text=,%EC%9D%B4%EB%AF%B8%20%EC%88%98%EC%A7%91%EB%90%9C%20%EB%85%BC%EB%AC%B8%EC%9D%80%20%EC%9E%90%EB%8F%99%EC%9C%BC%EB%A1%9C%20%ED%95%84%ED%84%B0%EB%A7%81). | Project notes |

These updates demonstrate a clear progression toward a more robust, modular and automated research assistant.

## Architecture

The project is organised around a **FastAPI** backend and modular machine‑learning components:

- **Backend:** The API server uses FastAPI with Uvicorn; it exposes endpoints for health checks, seeding data, training, prediction and feedback loop control [oai_citation:11‡raw.githubusercontent.com](https://raw.githubusercontent.com/hyosunglee/Project/main/replit.md#:~:text=%23%23%20Project%20Architecture%20,models%20with%20symlink%20to%20latest).  The default API port is 3000 when running via the backend but a web‑based UI runs on port 5000 [oai_citation:12‡raw.githubusercontent.com](https://raw.githubusercontent.com/hyosunglee/Project/main/replit.md#:~:text=,configured%20workflow%20with%20webview%20enabled).

- **ML stack:** The classifier employs TF‑IDF vectorisation and a logistic regression model to predict whether a research idea will yield “reward”.  For text generation, a GPT‑2 based summarizer creates concise summaries of high‑confidence predictions [oai_citation:13‡raw.githubusercontent.com](https://raw.githubusercontent.com/hyosunglee/Project/main/replit.md#:~:text=%23%23%20Project%20Architecture%20,models%20with%20symlink%20to%20latest).

- **Data storage:** Logs and results are stored in JSON Lines (`.jsonl`) format.  Models are versioned, and a symlink points to the latest version [oai_citation:14‡raw.githubusercontent.com](https://raw.githubusercontent.com/hyosunglee/Project/main/replit.md#:~:text=%23%23%20Project%20Architecture%20,models%20with%20symlink%20to%20latest).

- **VirtueEngine:** A custom module evaluates the complexity, information density and timing of the current research corpus.  It influences the loop by selecting actions such as paper collection or summarisation [oai_citation:15‡raw.githubusercontent.com](https://raw.githubusercontent.com/hyosunglee/Project/main/utils/loop_logic.py#:~:text=,total_logs%20%3D%20len%28logs).

## Components and file structure

The repository contains several key modules and scripts:

- **`server.py`** – entry point that runs the FastAPI app via Uvicorn [oai_citation:16‡raw.githubusercontent.com](https://raw.githubusercontent.com/hyosunglee/Project/main/server.py#:~:text=import%20uvicorn%20from%20api,config%20import%20HOST%2C%20PORT).
- **`api/main.py`** – registers route modules for prediction, summarisation, feedback, search and legacy endpoints [oai_citation:17‡raw.githubusercontent.com](https://raw.githubusercontent.com/hyosunglee/Project/main/api/main.py#:~:text=from%20fastapi%20import%20FastAPI%20from,legacy%20import%20start_training_worker%2C%20start_scheduler).
- **`api/routes/legacy.py`** – provides classic endpoints for health checks, training, ingestion, seeding logs, running a loop cycle and duplicate detection [oai_citation:18‡raw.githubusercontent.com](https://raw.githubusercontent.com/hyosunglee/Project/main/api/routes/legacy.py#:~:text=%40router.get%28,Research%20Support%20API%20Running).
- **`api/routes/predict.py`** – handles prediction requests.  It calls the classifier and, when the result is positive with ≥80 % confidence, triggers the summarizer to produce a GPT‑2 summary [oai_citation:19‡raw.githubusercontent.com](https://raw.githubusercontent.com/hyosunglee/Project/main/api/routes/predict.py#:~:text=if%20result.get%28,100%5D).
- **`auto_initialize.py`** – automates start‑up: waits for the server, generates seed data if no logs exist, triggers initial training and paper collection, and prints the schedule [oai_citation:20‡raw.githubusercontent.com](https://raw.githubusercontent.com/hyosunglee/Project/main/auto_initialize.py#:~:text=print%28,%2A%2060).
- **`utils/loop_logic.py`** – central loop logic that determines actions based on research context and logs.  It computes information density, schedules retraining, runs predictions and records results [oai_citation:21‡raw.githubusercontent.com](https://raw.githubusercontent.com/hyosunglee/Project/main/utils/loop_logic.py#:~:text=HIGH_CONF_THRESHOLD%20%3D%200,10) [oai_citation:22‡raw.githubusercontent.com](https://raw.githubusercontent.com/hyosunglee/Project/main/utils/loop_logic.py#:~:text=def%20save_prediction_results,high_conf_details).

## API Endpoints

The API exposes both legacy and modern routes.  The table below summarises the main endpoints and their purposes [oai_citation:23‡raw.githubusercontent.com](https://raw.githubusercontent.com/hyosunglee/Project/main/replit.md#:~:text=%23%23%20API%20Endpoints%20,Check%20for%20duplicate%20paper%20titles):

| Endpoint | Method | Purpose |
|---|---|---|
| `/` | GET | Health check – returns service status [oai_citation:24‡raw.githubusercontent.com](https://raw.githubusercontent.com/hyosunglee/Project/main/api/routes/legacy.py#:~:text=%40router.get%28,Research%20Support%20API%20Running). |
| `/healthz` | GET | Additional status endpoint [oai_citation:25‡raw.githubusercontent.com](https://raw.githubusercontent.com/hyosunglee/Project/main/api/routes/legacy.py#:~:text=%40router.get%28,Research%20Support%20API%20Running). |
| `/seed` | POST | Generate **N** synthetic log entries to bootstrap training [oai_citation:26‡raw.githubusercontent.com](https://raw.githubusercontent.com/hyosunglee/Project/main/replit.md#:~:text=%23%23%20API%20Endpoints%20,Make%20predictions%20on%20new%20text). |
| `/train` | POST | Enqueue model training on current logs [oai_citation:27‡raw.githubusercontent.com](https://raw.githubusercontent.com/hyosunglee/Project/main/api/routes/legacy.py#:~:text=%40router.post%28,Training%20enqueued). |
| `/predict` | POST | Predict reward for input text; returns prediction and confidence.  When the confidence exceeds 0.8 and the prediction is positive, a GPT‑2 summary is generated [oai_citation:28‡raw.githubusercontent.com](https://raw.githubusercontent.com/hyosunglee/Project/main/api/routes/predict.py#:~:text=if%20result.get%28,100%5D). |
| `/ingest` | POST | Add new data (title, text, label) to the system [oai_citation:29‡raw.githubusercontent.com](https://raw.githubusercontent.com/hyosunglee/Project/main/api/routes/legacy.py#:~:text=%40router.post%28,Data%20ingested%20successfully). |
| `/loop` | POST | Execute one cycle of the self‑learning loop – collects papers, predicts and triggers retraining as needed [oai_citation:30‡raw.githubusercontent.com](https://raw.githubusercontent.com/hyosunglee/Project/main/api/routes/legacy.py#:~:text=%40router.post%28,return%20result). |
| `/check_duplicates` | POST | Check submitted titles against logged titles and return duplicates [oai_citation:31‡raw.githubusercontent.com](https://raw.githubusercontent.com/hyosunglee/Project/main/api/routes/legacy.py#:~:text=class%20DuplicatesRequest%28BaseModel%29%3A%20titles%3A%20list). |

The system also offers a **web‑based interface**.  Opening the `static/index.html` page via the Replit deployment allows users to execute these functions through buttons and forms [oai_citation:32‡raw.githubusercontent.com](https://raw.githubusercontent.com/hyosunglee/Project/main/replit.md#:~:text=,configured%20workflow%20with%20webview%20enabled).

## Running the project

To set up the Self‑Learning Feedback Loop API locally:

1. **Install dependencies:** Use `pip install -r requirements.txt` to install the required Python packages [oai_citation:33‡raw.githubusercontent.com](https://raw.githubusercontent.com/hyosunglee/Project/main/replit.md#:~:text=%60%60%60bash%20,r%20requirements.txt).
2. **Run the server:** Start the FastAPI server on the desired port (default 3000) using `PORT=3000 python server.py` [oai_citation:34‡raw.githubusercontent.com](https://raw.githubusercontent.com/hyosunglee/Project/main/replit.md#:~:text=,py).  A separate Replit configuration exposes a web UI on port 5000 [oai_citation:35‡raw.githubusercontent.com](https://raw.githubusercontent.com/hyosunglee/Project/main/replit.md#:~:text=,configured%20workflow%20with%20webview%20enabled).
3. **Bootstrap data:** If there are no logs, generate test data by sending a POST request to `/seed` with a chosen value for `n` [oai_citation:36‡raw.githubusercontent.com](https://raw.githubusercontent.com/hyosunglee/Project/main/replit.md#:~:text=,py).  The `auto_initialize.py` script automates this step and triggers initial training and paper collection [oai_citation:37‡raw.githubusercontent.com](https://raw.githubusercontent.com/hyosunglee/Project/main/auto_initialize.py#:~:text=,%E2%9C%85%20%EA%B8%B0%EC%A1%B4%20%EB%A1%9C%EA%B7%B8%20%EB%8D%B0%EC%9D%B4%ED%84%B0%20%EB%B0%9C%EA%B2%AC).
4. **Train the model:** Trigger training manually via `POST /train` or allow the loop to retrain on schedule [oai_citation:38‡raw.githubusercontent.com](https://raw.githubusercontent.com/hyosunglee/Project/main/api/routes/legacy.py#:~:text=%40router.post%28,Training%20enqueued).
5. **Make predictions:** Send a JSON payload like `{"text": "your text here"}` to `/predict` to receive a prediction and, if applicable, a summary [oai_citation:39‡raw.githubusercontent.com](https://raw.githubusercontent.com/hyosunglee/Project/main/replit.md#:~:text=,2%20%EC%9A%94%EC%95%BD%20%EC%83%9D%EC%84%B1).  An example curl command is shown in the README [oai_citation:40‡raw.githubusercontent.com](https://raw.githubusercontent.com/hyosunglee/Project/main/replit.md#:~:text=,2%20%EC%9A%94%EC%95%BD%20%EC%83%9D%EC%84%B1).

### Schedule and automation

The feedback loop is designed for continuous operation.  By default, the system runs paper collection every **hour** and retrains the model every **six hours**, while storing results in the `results/` directory [oai_citation:41‡raw.githubusercontent.com](https://raw.githubusercontent.com/hyosunglee/Project/main/replit.md#:~:text=%23%23%20Current%20State%20,%E2%9C%85%20results%2F%20%ED%8F%B4%EB%8D%94%EC%97%90%20%EA%B2%B0%EA%B3%BC%20%EC%A0%80%EC%9E%A5).  The `auto_initialize.py` script prints the schedule and indicates where JSON log and summary files are saved [oai_citation:42‡raw.githubusercontent.com](https://raw.githubusercontent.com/hyosunglee/Project/main/auto_initialize.py#:~:text=print%28,nAPI%20%EC%97%94%EB%93%9C%ED%8F%AC%EC%9D%B8%ED%8A%B8%3A%20http%3A%2F%2Flocalhost%3A3000).

## User preferences and additional files

The project is configured for a mixed Korean/English user base and runs optimally in a Replit environment.  The recommended web interface is served on port 5000, whereas the API server listens on port 3000 [oai_citation:43‡raw.githubusercontent.com](https://raw.githubusercontent.com/hyosunglee/Project/main/replit.md#:~:text=%23%23%20User%20Preferences%20,Web%20UI%20for%20easy%20interaction).  Additional files include:

- **`static/index.html`** – a simple web UI for interacting with all API functions [oai_citation:44‡raw.githubusercontent.com](https://raw.githubusercontent.com/hyosunglee/Project/main/replit.md#:~:text=%23%23%20Files%20Added%20,to%20test%20all%20API%20endpoints).
- **`test_api.py`** – a script for testing API endpoints [oai_citation:45‡raw.githubusercontent.com](https://raw.githubusercontent.com/hyosunglee/Project/main/replit.md#:~:text=%23%23%20Files%20Added%20,to%20test%20all%20API%20endpoints).
- **`QUICKSTART.md`** – a planned quick‑start guide (not yet present in the repository) [oai_citation:46‡raw.githubusercontent.com](https://raw.githubusercontent.com/hyosunglee/Project/main/replit.md#:~:text=%23%23%20Files%20Added%20,Korean%20quickstart%20guide).

## License

The project is released under the MIT License.  This permissive license allows reuse and modification provided that the copyright notice is preserved and the software is supplied “as is” without warranty [oai_citation:47‡raw.githubusercontent.com](https://raw.githubusercontent.com/hyosunglee/Project/main/LICENSE#:~:text=MIT%20License).

## Visual overview

Below is an abstract illustration representing the self‑learning feedback loop.  Circular arrows convey continuous improvement, while digital documents and data streams hint at automated paper collection and analysis.

![Abstract feedback loop illustration](file-service://file-Gg2MpaVWXifroRJ5vA8ijo)

## Conclusion

The Self‑Learning Feedback Loop API aims to streamline research workflows by automating paper collection, machine‑learning model training and high‑confidence summarisation.  Recent refactoring toward FastAPI, expanded data collection and integration of a VirtueEngine highlight the project’s commitment to scalability and improved research quality [oai_citation:48‡raw.githubusercontent.com](https://raw.githubusercontent.com/hyosunglee/Project/main/replit.md#:~:text=,2%20%EC%9A%94%EC%95%BD%20%EC%83%9D%EC%84%B1) [oai_citation:49‡raw.githubusercontent.com](https://raw.githubusercontent.com/hyosunglee/Project/main/replit.md#:~:text=,%EC%9D%B4%EB%AF%B8%20%EC%88%98%EC%A7%91%EB%90%9C%20%EB%85%BC%EB%AC%B8%EC%9D%80%20%EC%9E%90%EB%8F%99%EC%9C%BC%EB%A1%9C%20%ED%95%84%ED%84%B0%EB%A7%81).  With its open‑source MIT license and clear modular structure, the project invites contributions and offers a foundation for future enhancements such as more sophisticated classifiers, multilingual support and richer analysis of scientific texts.