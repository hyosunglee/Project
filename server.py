from flask import Flask, jsonify, request
import threading
import random
from apscheduler.schedulers.background import BackgroundScheduler

# 유틸
from utils.model_trainer import train_model_from_logs
from utils.logger import log_experiment, is_duplicate
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
    return "✅ 서버 작동 중입니다. /seed /train /predict 사용 가능"


@app.route("/seed", methods=["POST"])
def seed_logs():
    """개발용: 학습용 로그 더미를 N개 생성 (reward 0/1 골고루)"""
    try:
        n = int(request.args.get("n", 30))
    except Exception:
        n = 30

    for i in range(n):
        title = f"[SEED] synthetic #{i}"
        summary = "Simulated RL paper about agents and policies."
        idea = "Try epsilon-greedy vs softmax in small gridworld."
        code = "import random\nfor _ in range(5): pass\n"
        acc = random.uniform(0.40, 0.95)
        result = f"Experiment with accuracy {acc:.2f}"
        reward = 1 if random.random() > 0.5 else 0
        log_experiment(title, summary, ["seed"], idea, code, result, reward)

    return jsonify({"message": f"Seeded {n} logs"}), 200


@app.route("/loop", methods=["POST"])
def run_loop_once():
    return _loop_internal()


def _loop_internal():
    print("\n🌀 [LOOP] 논문 수집 및 실험 실행 시작")
    papers = []
    if fetch_arxiv_papers:
        try:
            papers = fetch_arxiv_papers("reinforcement learning", max_results=5)
        except Exception as e:
            print(f"⚠️ fetch_arxiv_papers 실패: {e}")

    print(f"📚 총 {len(papers)}개의 논문 확인됨")

    if not papers:
        # Fallback 1건이라도 기록
        title = "[FALLBACK] no paper fetched"
        summary = "Fallback entry because fetch_arxiv_papers returned 0."
        idea = "baseline heuristic"
        code = "pass"
        result = "Experiment with accuracy 0.72"
        reward = 0
        log_experiment(title, summary, ["fallback"], idea, code, result, reward)
        print("🧩 Fallback 로그 1건 저장")
    else:
        for paper in papers:
            title = paper.get("title", "untitled")
            summary = paper.get("summary", "")
            keywords = ["reinforcement learning"]

            if is_duplicate(title):
                print(f"⚠️ 이미 처리한 논문: {title}")
                continue

            idea = "강화학습 실험 시뮬레이션"
            code = (
                "import random\n"
                "state = 0\n"
                "total_reward = 0\n"
                "for step in range(5):\n"
                "    action = random.choice(['왼쪽','오른쪽'])\n"
                "    reward = 1 if action == '오른쪽' else 0\n"
                "    total_reward += reward\n"
                "print('총 보상:', total_reward)\n"
            )
            result = "Experiment with accuracy 0.81"
            reward = 1

            log_experiment(title, summary, keywords, idea, code, result, reward)
            print(f"✅ [LOOP] {title} 실험 및 로그 저장 완료")

    return jsonify({"message": "Loop 실행 완료"}), 200


@app.route("/train", methods=["POST"])
def trigger_training():
    print("\n🚀 [TRAIN] 로그 기반 모델 학습 트리거됨 (비동기 시작)")
    threading.Thread(target=train_model_from_logs).start()
    return jsonify({"message": "Training started in background"}), 200


def start_scheduler():
    def scheduled_loop():
        with app.app_context():
            _ = _loop_internal()
    scheduler = BackgroundScheduler()
    scheduler.add_job(scheduled_loop, 'interval', minutes=1)
    scheduler.start()
    print("⏰ 자동 스케줄러 시작됨 (1분 간격)")


if __name__ == "__main__":
    print("🔧 서버 실행 중... http://0.0.0.0:3000")
    start_scheduler()
    app.run(host="0.0.0.0", port=3000, debug=False, use_reloader=False)
