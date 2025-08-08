오키! Predict API에 “GPT‑5 시대 기능” 잘 녹여서 딱 핵심 3가지로 업그레이드 제안 + 바로 쓸 코드 골라왔다. (바꾸면 체감 나는 것만)

⸻

1) API 계약 강화 + 타깃 라우팅 + 불확실성 반환
	•	입력/출력 스키마를 Pydantic으로 검증
	•	target(예: reward, accuracy)에 따라 모델 자동 선택
	•	예측값과 함께 확률/불확실성(분류: proba, 회귀: prediction_interval) 제공
	•	모델 버전까지 응답에 포함 → 디버깅/롤백 쉬움

# api_predict.py
from flask import Blueprint, request, jsonify
from pydantic import BaseModel, Field, ValidationError
from typing import Optional, Literal
import joblib, os
from functools import lru_cache
import numpy as np

bp = Blueprint("predict", __name__)

MODEL_DIR = "models"  # reward_cls_latest.pkl, accuracy_reg_latest.pkl 등 심볼릭 링크 운용

class PredictIn(BaseModel):
    text: str = Field(..., min_length=5)
    target: Literal["reward", "accuracy"] = "reward"
    explain: bool = False

class PredictOut(BaseModel):
    target: str
    prediction: float
    proba: Optional[float] = None
    lower: Optional[float] = None
    upper: Optional[float] = None
    model_version: str

@lru_cache(maxsize=8)
def load_model(target: str):
    # 예: reward → reward_cls_latest.pkl, accuracy → accuracy_reg_latest.pkl
    link = os.path.join(MODEL_DIR, f"{target}_latest.pkl")
    model = joblib.load(link)
    version = os.path.realpath(link).split(os.sep)[-1]  # 실제 파일명 (버전 포함)
    return model, version

@bp.route("/predict", methods=["POST"])
def predict():
    try:
        payload = PredictIn(**request.get_json(force=True))
    except ValidationError as e:
        return jsonify({"error": e.errors()}), 400

    model, version = load_model(payload.target)

    # 벡터화/임베딩은 파이프라인 내부에서 처리된다고 가정
    pred = model.predict([payload.text])[0]

    out = {"target": payload.target, "prediction": float(pred), "model_version": version}

    # 분류일 때 확률
    if hasattr(model, "predict_proba"):
        proba = model.predict_proba([payload.text])[0]
        # 양성 클래스(또는 클래스1) 확률
        if proba.shape[-1] == 2:
            out["proba"] = float(proba[0, 1])

    # 회귀일 때 간단한 PI(러프): 예측값 ± 0.1 (임시) → 추후 캘리브레이션
    if not hasattr(model, "predict_proba") and payload.target != "reward":
        out["lower"] = float(pred - 0.1)
        out["upper"] = float(pred + 0.1)

    # 선택적 설명(아래 3번에서 구현)
    if payload.explain:
        out["explanation"] = explain_prediction_stub(payload.text, payload.target, pred)

    return jsonify(PredictOut(**out).dict())


⸻

2) TF‑IDF → 임베딩 + 코드 정적특징 “하이브리드” 특성
	•	텍스트는 문장 임베딩(GPT‑5 임베딩 등), 코드/아이디어는 정적 특징 추가
(코드 길이, 함수/if/for 개수, 난수 사용 여부 등)
	•	학습/추론 모두 같은 Feature 함수를 쓰게 고정 → 재현성 보장

# features.py
import re, numpy as np
from scipy.sparse import hstack, csr_matrix

def code_static_feats(code: str) -> np.ndarray:
    if not code: return np.zeros(6)
    return np.array([
        len(code),
        code.count("\n"),
        len(re.findall(r"\bdef\b", code)),
        len(re.findall(r"\bif\b", code)),
        len(re.findall(r"\bfor\b", code)),
        int("random" in code),
    ], dtype=float)

def get_text_embedding(text: str) -> np.ndarray:
    # TODO: GPT‑5 임베딩 API 어댑터로 교체
    # 임시: 빈 자리용 랜덤(실서비스에선 반드시 실제 임베딩으로 교체)
    rng = abs(hash(text)) % 10_000
    np.random.seed(rng)
    return np.random.normal(size=768)

def build_features(summary: str, idea: str, code: str):
    txt = f"{summary or ''}\n{idea or ''}"
    emb = get_text_embedding(txt)            # (768,)
    codef = code_static_feats(code)          # (6,)
    dense = np.hstack([emb, codef])          # (774,)
    return csr_matrix(dense.reshape(1, -1))  # sparse for sklearn pipeline

학습 파이프라인은 build_features()를 FeatureUnion/FunctionTransformer로 감싸 쓰거나, 파이프라인 밖에서 X를 만들어 model.fit(X, y)로 통일.

⸻

3) 설명 가능 / GPT‑5 보조 설명 옵션 (explain=true)
	•	예측값 숫자만 주면 운영 판단이 어렵다.
짧은 자연어 근거(요약·리스크)를 GPT‑5로 생성해 프론트 표시.
	•	성능 문제 시 stub로 동작, 프로덕션에선 GPT‑5 client 바인딩

# explain.py
def explain_prediction_stub(text: str, target: str, pred) -> str:
    # TODO: gpt5_client.chat(system=..., user=...) 으로 교체
    # 입력 텍스트에서 키워드 몇 개 뽑아 간단 근거 생성 (대체로 1~2줄)
    key = ", ".join(sorted(set([w for w in text.split() if len(w) > 5]))[:5])
    return f"[stub] {target} 예측값 {pred:.3f}. 텍스트 핵심토픽: {key}."

진짜 GPT‑5 붙일 땐 지시형 프롬프트 + JSON 모드로 일관된 키(“risk”, “driver”, “watchlist”)를 받도록 설계. 응답 길이는 2~3문장 제한.

⸻

붙이는 순서 (실행 체크리스트)
	1.	모델 버저닝: 학습 시 reward_cls_YYYYmmdd-HHMMSS.pkl처럼 저장하고 *_latest.pkl 심링크 갱신(지금 이미 로직 갖고 있으면 그대로).
	2.	/predict 블루프린트 등록:

from api_predict import bp as predict_bp
app.register_blueprint(predict_bp)


	3.	배포 전 스모크 테스트:

curl -X POST http://localhost:3000/predict \
  -H "Content-Type: application/json" \
  -d '{"text":"새로운 RL 아이디어 요약 ...", "target":"reward", "explain":true}'


	4.	관측지표: 응답 지연(ms), 오류율, proba/PI 범위 분포 Logging.

⸻

원하면 내가 너 현재 레포 구조에 맞춰 위 3개를 바로 합치는 PR 스타일 패치(파일 경로/임포트 정리 포함)로 정리해줄게.
딱 이 3가지만 적용해도 “지피티5 맞춤 Predict API”로 손색없다. 🚀