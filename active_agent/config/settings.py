import os

# Configuration for the Active AI Agent
# Default values or environment variables
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
USER_CONTEXT = "나는 현재 AI 논문을 쓰고 있고 게임을 좋아해. AI Feedback Loop에 관심이 많아."
MEMORY_THRESHOLD = 90.0
POLLING_INTERVAL_SECONDS = 3600 # 1 hour

# Notification settings
NOTIF_TITLE = "능동적 AI 에이전트"
