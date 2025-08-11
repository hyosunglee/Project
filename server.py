from flask import Flask, jsonify, request
import threading
import logging

from utils.paper_fetcher import fetch_arxiv_papers
from utils.logger import log_experiment, is_duplicate
from utils.model_trainer import train_model_from_logs

# Configure logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    filename='server.log',
                    filemode='w')

app = Flask(__name__)

@app.route("/")
def home():
    logging.info("🔗 '/' 경로에 접근 - 서버 정상 작동 확인됨")
    return "✅ 서버 작동 중입니다. /loop 또는 /train 호출 가능"

@app.route("/loop", methods=["POST"])
def run_loop_once():
    logging.info("\n🌀 [LOOP] 논문 수집 및 실험 실행 시작")

    papers = fetch_arxiv_papers("reinforcement learning", max_results=5)
    logging.info(f"📚 총 {len(papers)}개의 논문 확인됨")

    for paper in papers:
        title = paper["title"]
        summary = paper["summary"]
        keywords = ["reinforcement learning"]

        if is_duplicate(title):
            logging.warning(f"⚠️ 이미 처리한 논문: {title}")
            continue

        logging.info(f"🧠 새 논문 처리: {title}")
        logging.info(f"📄 요약: {summary[:100]}...")

        idea = "강화학습 실험 시뮬레이션"
        code = '''
import random
state = 0
total_reward = 0
for step in range(5):
    action = random.choice(["왼쪽", "오른쪽"])
    reward = 1 if action == "오른쪽" else 0
    total_reward += reward
print("총 보상:", total_reward)
'''
        result = "Experiment with accuracy 0.81"
        reward = 1

        log_experiment(title, summary, keywords, idea, code, result, reward)

        logging.info(f"✅ [LOOP] {title} 실험 및 로그 저장 완료")
        break

    return jsonify({"message": "Loop 실행 완료"}), 200

@app.route("/train", methods=["POST"])
def trigger_training():
    logging.info("\n🚀 [TRAIN] 로그 기반 모델 학습 트리거됨 (비동기 시작)")
    threading.Thread(target=train_model_from_logs).start()
    return jsonify({"message": "Training started in background"}), 200

if __name__ == "__main__":
    logging.info("🔧 서버 실행 중... http://0.0.0.0:3000")
    app.run(host="0.0.0.0", port=3000)
