
curl -X POST http://localhost:3000/loop

프로그램 실행 후 
위 명령어 shell에 삽입 




좋은 질문이야. 매번 curl로 수동 요청하는 건 개발자 체력 낭비지.
자동화는 크게 두 가지 방향으로 할 수 있어:

⸻

✅ 1. 서버 내부에서 주기적으로 /loop 실행 (추천)

Flask에 스케줄러를 붙이면 /loop 엔드포인트를 굳이 외부에서 호출 안 해도 서버 내부에서 주기적으로 실행 가능해.

🔧 방법: APScheduler 사용

pip install apscheduler

🔁 Flask에 주기적 작업 추가

main.py 또는 Flask 앱 코드 하단에 아래 추가:

from apscheduler.schedulers.background import BackgroundScheduler

def scheduled_loop():
    with app.app_context():
        print("\n⏰ [자동 LOOP] 주기적 실행 시작")
        run_loop_once()  # 직접 호출

# 스케줄러 설정
scheduler = BackgroundScheduler()
scheduler.add_job(scheduled_loop, 'interval', seconds=60)  # 60초마다 실행
scheduler.start()


⸻

✅ 2. 외부에서 정기적으로 /loop 호출하기 (단순함)

만약 서버에 POST /loop 요청을 외부에서 보내야 한다면:

💡 방법 A: crontab + curl

리눅스 환경이라면 crontab으로 curl 명령 자동 실행 가능

crontab -e

그리고 아래 추가 (예: 매 5분마다 실행):

*/5 * * * * curl -X POST http://localhost:3000/loop

💡 방법 B: 파이썬 스크립트 + schedule 라이브러리

pip install schedule

import schedule
import time
import requests

def post_loop():
    res = requests.post("http://localhost:3000/loop")
    print(f"[자동 요청] 상태 코드: {res.status_code}")

schedule.every(10).minutes.do(post_loop)

while True:
    schedule.run_pending()
    time.sleep(1)


⸻

✨ 추천 조합

목적	방식	설명
가장 간단한 자동화	Flask 안에 APScheduler 추가	별도 요청 없이 내부에서 실행
분산 시스템 or 외부 제어 필요	curl + crontab or requests.post()	REST API 구조 유지 가능


⸻

✅ 마무리

from flask import Flask, jsonify, request
import threading
from apscheduler.schedulers.background import BackgroundScheduler

# ===== 유틸 모듈 =====
from utils.idea_generator import extract_experiment_ideas
from utils.code_generator import generate_code
from utils.executor import simulate_experiment
from utils.paper_fetcher import fetch_arxiv_papers
from utils.logger import log_experiment, is_duplicate
from utils.log_reader import load_logs, preprocess_logs
from utils.model_trainer import train_model_from_logs

app = Flask(__name__)


@app.route("/")
def home():
    print("🔗 '/' 경로에 접근 - 서버 정상 작동 확인됨")
    return "✅ 서버 작동 중입니다. /loop 또는 /train 호출 가능"


@app.route("/loop", methods=["POST"])
def run_loop_once():
    return _loop_internal()


def _loop_internal():
    print("\n🌀 [LOOP] 논문 수집 및 실험 실행 시작")

    papers = fetch_arxiv_papers("reinforcement learning", max_results=5)
    print(f"📚 총 {len(papers)}개의 논문 확인됨")

    for paper in papers:
        title = paper["title"]
        summary = paper["summary"]
        keywords = ["reinforcement learning"]

        if is_duplicate(title):
            print(f"⚠️ 이미 처리한 논문: {title}")
            continue

        print(f"🧠 새 논문 처리: {title}")
        print(f"📄 요약: {summary[:100]}...")

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

        print(f"✅ [LOOP] {title} 실험 및 로그 저장 완료")
        break

    return jsonify({"message": "Loop 실행 완료"}), 200


@app.route("/train", methods=["POST"])
def trigger_training():
    print("\n🚀 [TRAIN] 로그 기반 모델 학습 트리거됨 (비동기 시작)")
    threading.Thread(target=train_model_from_logs).start()
    return jsonify({"message": "Training started in background"}), 200


# ===== APScheduler 설정 =====
def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(_loop_internal, 'interval', minutes=1)  # 매 1분마다 자동 실행
    scheduler.start()
    print("⏰ 자동 스케줄러 시작됨 (1분 간격)")


if __name__ == "__main__":
    print("🔧 서버 실행 중... http://0.0.0.0:3000")
    start_scheduler()
    app.run(host="0.0.0.0", port=3000)
