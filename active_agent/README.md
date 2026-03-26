# Active AI Agent for Mac Mini (M2)

이 프로젝트는 macOS(M2, 16GB) 환경에서 능동적으로 작동하는 AI 에이전트의 프로토타입입니다.

## 주요 기능
1. **모니터링 (Monitoring)**
    - 시스템의 메모리 사용량을 실시간으로 체크합니다 (`psutil`).
    - ArXiv에서 'AI Feedback Loop' 관련 최신 논문을 주기적으로 검색합니다.
2. **판단 (Judgment)**
    - 수집된 정보를 바탕으로 Gemini 1.5 Pro API를 호출하여 사용자에게 개입(알림)할 가치가 있는지 판단합니다.
    - 사용자의 맥락(AI 논문 작성 중, 게임 매니아)을 고려하여 판단합니다.
3. **개입 (Intervention)**
    - 가치가 있다고 판단되면 macOS의 시스템 알림(`osascript`)을 통해 사용자에게 메시지를 보냅니다.

## 설치 및 설정
### 1. 의존성 설치
```bash
pip install -r active_agent/requirements.txt
```

### 2. 환경 변수 설정
Gemini API를 사용하기 위해 `GEMINI_API_KEY` 환경 변수를 설정해야 합니다.
```bash
export GEMINI_API_KEY="your-google-api-key"
```

### 3. 사용자 맥락 설정
`active_agent/config/settings.py` 파일에서 사용자 맥락을 자신의 상황에 맞게 수정할 수 있습니다.

## 실행 방법
```bash
python3 active_agent/main.py
```

## 모듈 구조
- `monitor/`: 시스템 자원 및 연구 논문 수집.
- `brain/`: Gemini API 연동 및 판단 로직.
- `output/`: macOS 알림 전송.
- `config/`: 에이전트 설정.
- `main.py`: 전체 흐름을 제어하는 오케스트레이터.
