from flask import Flask, jsonify, request
import threading
import random
from apscheduler.schedulers.background import BackgroundScheduler

# 유틸
from utils.trainer import train_model
from utils.logger import log_experiment
from utils.loop_logic import loop_logic
try:
    from utils.paper_fetcher import fetch_arxiv_papers
except Exception:
    fetch_arxiv_papers = None  # 없는 환경 대비

from api_predict import bp as predict_bp

app = Flask(__name__)
app.register_blueprint(predict_bp)


@app.route("/")
def home():
    print("🔗 '/' 경로에 접근 - 서버 정상 작동 확인됨")
    return "✅ 서버 작동 중입니다. /seed /train /predict /loop 사용 가능"


@app.route("/seed", methods=["POST"])
def seed_logs():
    """개발용: 학습용 로그 더미를 N개 생성 (label 0/1 골고루)"""
    try:
        n = int(request.args.get("n", 30))
    except Exception:
        n = 30

    for i in range(n):
        text = f"[SEED] synthetic text #{i}. This is a simulated paper summary about agents and policies."
        label = 1 if random.random() > 0.5 else 0
        log_experiment(text, label)

    return jsonify({"message": f"Seeded {n} logs"}), 200


@app.route("/loop", methods=["POST"])
def run_loop_once():
    # The new loop logic is more complex, for now we just log a paper
    # and then trigger the active learning check.
    print("\n🌀 [LOOP] 논문 수집 및 실험 실행 시작")
    papers = []
    if fetch_arxiv_papers:
        try:
            papers = fetch_arxiv_papers("reinforcement learning", max_results=1)
        except Exception as e:
            print(f"⚠️ fetch_arxiv_papers 실패: {e}")

    if papers:
        paper = papers[0]
        log_experiment(paper.get("summary", "No summary"), 1)
        print(f"✅ [LOOP] {paper.get('title', 'untitled')} 실험 및 로그 저장 완료")

    # Now run the active learning logic
    loop_logic()

    return jsonify({"message": "Loop 실행 완료"}), 200


@app.route("/train", methods=["POST"])
def trigger_training():
    print("\n🚀 [TRAIN] 로그 기반 모델 학습 트리거됨 (비동기 시작)")
    threading.Thread(target=train_model).start()
    return jsonify({"message": "Training started in background"}), 200


def start_scheduler():
    def scheduled_loop():
        with app.app_context():
            run_loop_once()
    scheduler = BackgroundScheduler()
    scheduler.add_job(scheduled_loop, 'interval', minutes=1)
    scheduler.start()
    print("⏰ 자동 스케줄러 시작됨 (1분 간격)")


if __name__ == "__main__":
    print("🔧 서버 실행 중... http://0.0.0.0:3000")
    # I will not start the scheduler for now to avoid complexity during testing
    # start_scheduler()
    app.run(host="0.0.0.0", port=3000, debug=False, use_reloader=False)
