import os
from flask import Flask, jsonify, request
import threading

# ==============================================================================
# App Initialization
# ==============================================================================
app = Flask(__name__)

# ==============================================================================
# Health Check Endpoint (always available)
# ==============================================================================
@app.route("/healthz")
def healthz():
    """Returns a unique signature to confirm the service is running."""
    return {"service": "predict-api", "ok": True, "version": "1.0"}

# ==============================================================================
# Safe Boot Logic
# ==============================================================================
# If SAFE_BOOT is enabled, we skip loading heavy modules and blueprints.
# This helps isolate startup crashes.
SAFE_BOOT = os.getenv("SAFE_BOOT", "0") == "1"

if not SAFE_BOOT:
    # --------------------------------------------------------------------------
    # Heavy Imports (only loaded when not in safe boot mode)
    # --------------------------------------------------------------------------
    import random
    from apscheduler.schedulers.background import BackgroundScheduler
    from utils.trainer import train_model
    from utils.logger import log_experiment, get_all_logged_titles
    from utils.loop_logic import loop_logic
    from api_predict import bp as predict_bp

    try:
        from utils.paper_fetcher import fetch_arxiv_papers
    except Exception:
        fetch_arxiv_papers = None

    # --------------------------------------------------------------------------
    # Register Blueprints
    # --------------------------------------------------------------------------
    app.register_blueprint(predict_bp)

    # --------------------------------------------------------------------------
    # Route Definitions
    # --------------------------------------------------------------------------
    @app.route("/")
    def home():
        print("🔗 '/' 경로에 접근 - 서버 정상 작동 확인됨")
        return "✅ 서버 작동 중입니다. /seed /train /predict /loop /ingest /check_duplicates /healthz 사용 가능"

    @app.route("/seed", methods=["POST"])
    def seed_logs():
        try:
            n = int(request.args.get("n", 30))
        except Exception:
            n = 30
        for i in range(n):
            log_entry = {
                "title": f"Synthetic Seed Paper #{i}",
                "text": f"[SEED] synthetic text #{i}. This is a simulated paper summary about agents and policies.",
                "label": 1 if random.random() > 0.5 else 0
            }
            log_experiment(log_entry)
        return jsonify({"message": f"Seeded {n} logs"}), 200

    @app.route("/loop", methods=["POST"])
    def run_loop_once():
        print("\n🌀 [LOOP] 논문 수집 및 실험 실행 시작")
        papers = []
        if fetch_arxiv_papers:
            try:
                papers = fetch_arxiv_papers("reinforcement learning", max_results=1)
            except Exception as e:
                print(f"⚠️ fetch_arxiv_papers 실패: {e}")
        if papers:
            paper = papers[0]
            title = paper.get('title', 'untitled')
            summary = paper.get("summary", "No summary")
            logged_titles = get_all_logged_titles()
            if title not in logged_titles:
                log_entry = {
                    "title": title, "summary": summary, "source": "loop", "label": 1
                }
                log_experiment(log_entry)
                print(f"✅ [LOOP] {title} 실험 및 로그 저장 완료")
            else:
                print(f"⚠️ [LOOP] 이미 처리한 논문: {title}")
        loop_logic()
        return jsonify({"message": "Loop 실행 완료"}), 200

    @app.route("/train", methods=["POST"])
    def trigger_training():
        print("\n🚀 [TRAIN] 로그 기반 모델 학습 트리거됨 (비동기 시작)")
        threading.Thread(target=train_model).start()
        return jsonify({"message": "Training started in background"}), 200

    @app.route("/ingest", methods=["POST"])
    def ingest_data():
        data = request.get_json()
        if not data or not isinstance(data, dict) or "title" not in data:
            return jsonify({"error": "Invalid payload, must be a JSON object with a 'title' field"}), 400
        try:
            log_experiment(data)
            print(f"📥 [INGEST] 데이터 수신 및 저장 완료: {data.get('title', 'N/A')[:50]}...")
            return jsonify({"message": "Data ingested successfully"}), 201
        except Exception as e:
            print(f"🔥 [INGEST] 데이터 저장 실패: {e}")
            return jsonify({"error": "Failed to ingest data"}), 500

    @app.route("/check_duplicates", methods=["POST"])
    def check_duplicates():
        data = request.get_json()
        if not data or "titles" not in data or not isinstance(data["titles"], list):
            return jsonify({"error": "Invalid payload, 'titles' field with a list of strings is required"}), 400
        client_titles = set(data["titles"])
        logged_titles = get_all_logged_titles()
        duplicates = list(client_titles.intersection(logged_titles))
        return jsonify({"duplicates": duplicates}), 200

    def start_scheduler():
        def scheduled_loop():
            with app.app_context():
                run_loop_once()
        scheduler = BackgroundScheduler()
        scheduler.add_job(scheduled_loop, 'interval', minutes=1)
        scheduler.start()
        print("⏰ 자동 스케줄러 시작됨 (1분 간격)")

# ==============================================================================
# Main execution block (for direct `python server.py` calls)
# ==============================================================================
if __name__ == "__main__":
    port = int(os.getenv("PORT", 3100))
    print(f"🔧 (dev mode) 서버 실행 중... http://0.0.0.0:{port}")
    app.run(host="0.0.0.0", port=port, debug=False, use_reloader=False)
