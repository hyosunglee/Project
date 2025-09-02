# api_predict.py 상단
import joblib


def predict_reward(text):
    with open("models/reward_latest.pkl", "rb") as f:
        pipeline = joblib.load(f)

    X = [text]
    prob = pipeline.predict_proba(X)
    pred = pipeline.predict(X)
    confidence = max(prob[0])

    return {
        "prediction": int(pred[0]),
        "confidence": round(float(confidence), 4)
    }


from utils.predictor import predict_reward
from flask import Blueprint, request, jsonify

from pydantic import BaseModel, Field, ValidationError
from typing import Optional, Literal
from utils.predictor import predict_reward

bp = Blueprint("predict", __name__)


class PredictIn(BaseModel):
    text: str = Field(..., min_length=5)
    # The user's snippet had target and explain, I will keep them for now
    # but the new predict_reward function doesn't use them.
    target: Literal["reward"] = "reward"
    explain: bool = False


class PredictOut(BaseModel):
    prediction: int
    confidence: float


@bp.route("/predict", methods=["POST"])
def predict():
    try:
        payload = request.get_json(force=True)
        if "text" not in payload:
            return jsonify({"error": "Missing 'text' field"}), 400

        # payload["text"]로 접근해야 안전
        result = predict_reward(payload["text"])
        return jsonify(result)

    except Exception as e:
        # 에러 발생 시 예쁘게 응답
        return jsonify({"error": f"inference error: {str(e)}"}), 500

    if result["prediction"] == -1:
        return jsonify({"error": "model not ready"}), 503

    return jsonify(PredictOut(**result).dict()), 200
