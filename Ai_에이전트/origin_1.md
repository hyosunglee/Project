좋습니다. 리서치 기반으로 다음 단계에서 바로 구현해야 할 핵심 코드를 정리하고 제공드립니다.

✅ 현재 진행해야 할 우선 구현 모듈

1. 한국어 NLU 분석 (의도 및 엔티티 추출)
2. 대화 관리 및 응답 생성 (외부 API 연동 포인트 포함)
3. 테스트용 CLI 대화 Loop

⸻

1️⃣ NLU 분석 모듈 - analyze_input()

from konlpy.tag import Okt

okt = Okt()

def analyze_input(text):
    tokens = okt.morphs(text)
    intent = "unknown"
    entities = {}

    # 간단한 의도 규칙 기반 분류
    if any(word in tokens for word in ["날씨", "기온", "비", "눈"]):
        intent = "weather"
        for city in ["서울", "부산", "인천", "대전", "대구", "광주"]:
            if city in text:
                entities["location"] = city
                break
    elif any(word in tokens for word in ["안녕", "반가워", "하이"]):
        intent = "greeting"

    return intent, entities



⸻

2️⃣ 대화 관리 및 응답 생성 모듈 - generate_response()

import requests

# (필요시 API KEY 환경변수로 교체)
WEATHER_API_KEY = "YOUR_API_KEY"

def get_weather(location):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={WEATHER_API_KEY}&lang=kr&units=metric"
    res = requests.get(url)
    if res.status_code != 200:
        return "날씨 정보를 가져오지 못했습니다."
    data = res.json()
    description = data["weather"][0]["description"]
    temp = data["main"]["temp"]
    return f"{description}, {temp:.1f}°C"

def generate_response(intent, entities):
    if intent == "greeting":
        return "안녕하세요! 무엇을 도와드릴까요?"
    elif intent == "weather":
        loc = entities.get("location", "서울")  # 기본값 서울
        weather_info = get_weather(loc)
        return f"{loc}의 현재 날씨는 {weather_info}입니다."
    else:
        return "죄송해요, 무슨 뜻인지 잘 모르겠어요."



⸻

3️⃣ 테스트용 대화 Loop - run_agent()

def run_agent():
    print("Hyosung AI 에이전트 실행 (종료: 'exit')")
    while True:
        user_input = input("사용자: ")
        if user_input.lower() == 'exit':
            print("에이전트를 종료합니다.")
            break
        intent, entities = analyze_input(user_input)
        response = generate_response(intent, entities)
        print(f"에이전트: {response}")

if __name__ == "__main__":
    run_agent()



⸻

✅ 실행 후 기대 예시

사용자: 안녕
에이전트: 안녕하세요! 무엇을 도와드릴까요?

사용자: 서울 날씨 알려줘
에이전트: 서울의 현재 날씨는 맑음, 18.3°C입니다.



⸻

✅ 다음 확장 포인트 추천
	•	get_weather() 부분 → 날씨 외 API 연결 추가 가능 (뉴스, 주식, DB)
	•	intent → 기계학습 모델 연동 준비
	•	멀티턴 상태 관리 → 대화 히스토리 추가
	•	음성(STT/TTS) 연결

⸻

