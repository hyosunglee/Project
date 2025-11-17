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
@app.route("/")
def index():
    """API 상태 정보"""
    return jsonify({
        "service": "Self-Learning AI System",
        "status": "running",
        "automation": "enabled",
        "endpoints": ["/healthz", "/seed", "/train", "/predict", "/loop", "/ingest", "/check_duplicates"]
    })

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
    from utils.result_logger import save_result
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
    @app.route("/api")
    def api_info():
        print("🔗 '/api' 경로에 접근 - 서버 정상 작동 확인됨")
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

    # 키워드 순환을 위한 전역 변수
    SEARCH_KEYWORDS = [
        "reinforcement learning", "deep learning", "neural networks",
        "computer vision", "natural language processing", "transformer models",
        "generative AI", "machine learning optimization", "graph neural networks",
        "meta learning"
    ]
    keyword_counter = [0]  # 리스트로 감싸서 클로저 내에서 수정 가능하게
    
    @app.route("/loop", methods=["POST"])
    def run_loop_once():
        print("\n🌀 [LOOP] 논문 수집 및 실험 실행 시작")
        collected_papers = []
        papers = []
        if fetch_arxiv_papers:
            try:
                # 키워드 순환
                current_keyword = SEARCH_KEYWORDS[keyword_counter[0] % len(SEARCH_KEYWORDS)]
                keyword_counter[0] += 1
                print(f"🔍 검색 키워드: '{current_keyword}'")
                papers = fetch_arxiv_papers(current_keyword, max_results=30)
            except Exception as e:
                print(f"⚠️ fetch_arxiv_papers 실패: {e}")
        
        if papers:
            logged_titles = get_all_logged_titles()
            for paper in papers:
                title = paper.get('title', 'untitled')
                summary = paper.get("summary", "No summary")
                if title not in logged_titles:
                    log_entry = {
                        "title": title,
                        "text": summary,  # summary를 text로 저장
                        "summary": summary,
                        "source": "loop",
                        "label": 1
                    }
                    log_experiment(log_entry)
                    collected_papers.append({"title": title, "summary": summary[:100]})
                    print(f"✅ [LOOP] {title} 실험 및 로그 저장 완료")
        
        loop_logic()
        
        # 결과 저장
        result_data = {
            "collected_count": len(collected_papers),
            "papers": collected_papers
        }
        result_file = save_result("collection", result_data)
        print(f"📁 수집 결과 저장: {result_file}")
        
        return jsonify({"message": "Loop 실행 완료", "collected": len(collected_papers)}), 200

    @app.route("/train", methods=["POST"])
    def trigger_training():
        print("\n🚀 [TRAIN] 로그 기반 모델 학습 트리거됨 (비동기 시작)")
        
        def train_and_save():
            result = train_model()
            if result:
                save_result("training", result)
                print(f"📁 학습 결과 저장 완료")
        
        threading.Thread(target=train_and_save).start()
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
        """자동화 스케줄러 시작"""
        def scheduled_loop():
            with app.app_context():
                run_loop_once()
        
        def scheduled_train():
            """주기적으로 모델 재학습"""
            with app.app_context():
                print("\n🔄 [AUTO-TRAIN] 자동 재학습 시작")
                train_model()
        
        scheduler = BackgroundScheduler()
        
        # 논문 수집: 1시간마다
        scheduler.add_job(scheduled_loop, 'interval', hours=1, id='paper_collection')
        
        # 모델 재학습: 6시간마다
        scheduler.add_job(scheduled_train, 'interval', hours=6, id='model_training')
        
        scheduler.start()
        print("⏰ 자동 스케줄러 시작됨")
        print("   - 논문 수집: 1시간마다")
        print("   - 모델 학습: 6시간마다")

    # 스케줄러 시작
    start_scheduler()

# ==============================================================================
# Main execution block (for direct `python server.py` calls)
# ==============================================================================
if __name__ == "__main__":
    port = int(os.getenv("PORT", 3000))
    print(f"🤖 자율 학습 시스템 시작... http://0.0.0.0:{port}")
    app.run(host="0.0.0.0", port=port, debug=False, use_reloader=False)
