### **✅ AI 코딩 에이전트 (`coder.py`) 및 API 설정 방법**  
아래 **단계별 가이드**를 따라 하면 **AI 코딩 에이전트**를 FastAPI와 연결하고, Flutter 또는 백엔드 코드를 자동 생성할 수 있습니다. 🚀  

---

## **📌 1. 프로젝트 폴더 구조 정리**
현재 진행 중인 프로젝트 구조에 맞춰 아래처럼 정리하세요.

```
ai_dev_system/
│── agents/
│   ├── __init__.py
│   ├── coder.py          👈 **AI 코딩 에이전트 (새로 추가!)**
│── api/
│   ├── __init__.py
│   ├── main.py          👈 **FastAPI 실행 코드**
│   ├── routes.py        👈 **FastAPI API 라우터 (수정)**
│── db/
│── Dockerfile
│── docker-compose.yml
│── requirements.txt
│── .env
```

---

## **📌 2. `agents/coder.py` 파일 추가 (AI 코딩 에이전트)**
📌 **파일 위치:** `ai_dev_system/agents/coder.py`  
📌 **역할:** GPT-4 기반으로 **Flutter & FastAPI 코드 생성**  

**✅ `agents/coder.py` 파일 생성 및 코드 추가**
```bash
nano ai_dev_system/agents/coder.py
```
🔹 **아래 코드 붙여넣기 & 저장 (`CTRL + X`, `Y`, `Enter`)**
```python
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage
import os

class AICoder:
    def __init__(self, model="gpt-4"):
        self.llm = ChatOpenAI(model_name=model, openai_api_key=os.getenv("OPENAI_API_KEY"))

    def generate_flutter_code(self, feature_description):
        """Flutter UI/기능 코드를 생성"""
        prompt = f"Flutter 앱에서 '{feature_description}' 기능을 구현하는 Dart 코드를 작성해줘."
        response = self.llm([HumanMessage(content=prompt)])
        return response.content

    def generate_backend_code(self, endpoint_description):
        """FastAPI 백엔드 API 엔드포인트 코드를 생성"""
        prompt = f"FastAPI에서 '{endpoint_description}' 엔드포인트를 만드는 Python 코드를 작성해줘."
        response = self.llm([HumanMessage(content=prompt)])
        return response.content
```
📌 **환경 변수 (`OPENAI_API_KEY`)를 사용하여 OpenAI API 키를 설정**

---

## **📌 3. `api/routes.py` 수정 (AI 코딩 API 추가)**
📌 **파일 위치:** `ai_dev_system/api/routes.py`  
📌 **역할:** **AI에게 Flutter/백엔드 코드 생성을 요청하는 API**

```bash
nano ai_dev_system/api/routes.py
```

🔹 **기존 `routes.py`에 아래 코드 추가**
```python
from fastapi import APIRouter, HTTPException
from agents.coder import AICoder

router = APIRouter()
coder = AICoder()

@router.post("/generate_code")
def generate_code(feature: str, platform: str):
    """AI가 Flutter 또는 FastAPI 코드를 생성"""
    if platform == "flutter":
        code = coder.generate_flutter_code(feature)
    elif platform == "backend":
        code = coder.generate_backend_code(feature)
    else:
        raise HTTPException(status_code=400, detail="지원하지 않는 플랫폼입니다. 'flutter' 또는 'backend'를 선택하세요.")
    
    return {"platform": platform, "code": code}
```
✅ **FastAPI에서 `/generate_code` 엔드포인트 추가됨**

---

## **📌 4. `.env` 파일 설정 (OpenAI API 키 추가)**
📌 **파일 위치:** `ai_dev_system/.env`  
📌 **역할:** OpenAI API 키를 환경 변수로 설정  

```bash
nano ai_dev_system/.env
```
🔹 **아래 내용 추가 (API 키 입력)**
```
OPENAI_API_KEY=your-openai-api-key-here
```
📌 **자신의 OpenAI API 키로 변경 후 저장**

---

## **📌 5. `Dockerfile` 수정 (`.env` 파일 반영)**
📌 **파일 위치:** `ai_dev_system/Dockerfile`  
📌 **역할:** `.env` 환경 변수를 FastAPI 컨테이너에서 사용할 수 있도록 설정  

```bash
nano ai_dev_system/Dockerfile
```
🔹 **아래 코드 추가**
```dockerfile
ENV OPENAI_API_KEY=${OPENAI_API_KEY}
```
✅ **Docker 컨테이너 실행 시 OpenAI API 키를 자동 로드**

---

## **📌 6. `requirements.txt` 업데이트**
📌 **LangChain과 OpenAI 라이브러리 추가**  

```bash
nano ai_dev_system/requirements.txt
```
🔹 **아래 패키지 추가**
```
fastapi
uvicorn
sqlalchemy
psycopg2-binary
langchain
openai
python-dotenv
```

---

## **📌 7. FastAPI 서버 실행 (Docker 빌드 & 실행)**
```bash
docker-compose down
docker-compose up --build
```
✅ **이제 FastAPI 서버가 실행되고 `/generate_code` API를 사용할 준비가 되었습니다!**

---

## **📌 8. API 테스트 (Flutter & 백엔드 코드 생성 요청)**
📌 **터미널에서 API 테스트**
```bash
curl -X POST "http://localhost:8000/generate_code" -H "Content-Type: application/json" \
     -d '{"feature": "로그인 화면 구현", "platform": "flutter"}'
```
✅ **성공하면 AI가 Flutter 코드를 생성하여 응답할 것!**

📌 **FastAPI 문서 (Swagger) 확인**
```
http://localhost:8000/docs
```
✅ **자동 생성된 API 문서를 확인하고 테스트 가능**

---

## **🔥 다음 단계**
1️⃣ **FastAPI에서 AI 코딩 API (`/generate_code`) 테스트**  
2️⃣ **Flutter 프로젝트를 생성하고, AI가 만든 코드를 실제로 적용**  
3️⃣ **광고 (Google AdMob) 연동 계획 논의**  

🚀 **이제 `/generate_code` API를 테스트하고 결과를 공유해 주세요!** 😊  
(필요한 추가 기능이나 개선 사항이 있으면 말씀해 주세요!)
