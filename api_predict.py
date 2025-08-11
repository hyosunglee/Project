from flask import Blueprint, request, jsonify
from pydantic import BaseModel, Field, ValidationError
from typing import Optional, Literal
import joblib, os
from functools import lru_cache

bp = Blueprint("predict", __name__)
MODEL_DIR = "models"  # reward_latest.pkl 사용


class PredictIn(BaseModel):
    text: str = Field(..., min_length=5)
    target: Literal["reward"] = "reward"
    explain: bool = False


class PredictOut(BaseModel):
    target: str
    prediction: float
    proba: Optional[float] = None
    lower: Optional[float] = None
    upper: Optional[float] = None
    model_version: Optional[str] = None
    explanation: Optional[str] = None


def _explain_stub(text: str, target: str, pred) -> str:
    words = [w for w in text.split() if len(w) > 5]
    key = ", ".join(sorted(set(words))[:5])
    return f"[stub] {target}={pred:.3f}. 핵심토픽: {key}."


@lru_cache(maxsize=8)
def _load_model_path(target: str) -> str:
    return os.path.join(MODEL_DIR, f"{target}_latest.pkl")


@bp.route("/predict", methods=["POST"])
def predict():
    try:
        payload = PredictIn(**request.get_json(force=True))
    except ValidationError as e:
        return jsonify({"error": e.errors()}), 400

    link = _load_model_path(payload.target)
    if not os.path.exists(link) and not os.path.islink(link):
        return jsonify({"error": f"model not ready: {link} (먼저 /train 으로 학습하세요)"}), 503

    try:
        model = joblib.load(link)
        version = os.path.realpath(link).split(os.sep)[-1]
    except Exception as e:
        return jsonify({"error": f"failed to load model: {str(e)}"}), 500

    try:
        pred = model.predict([payload.text])[0]
        out = {
            "target": payload.target,
            "prediction": float(pred),
            "model_version": version,
        }
        if hasattr(model, "predict_proba"):
            proba = model.predict_proba([payload.text])[0]
            if proba.shape[-1] == 2:
                out["proba"] = float(proba[0, 1])
        else:
            out["lower"] = float(pred - 0.1)
            out["upper"] = float(pred + 0.1)

        if payload.explain:
            out["explanation"] = _explain_stub(payload.text, payload.target, pred)

        return jsonify(PredictOut(**out).dict()), 200
    except Exception as e:
        return jsonify({"error": f"inference error: {str(e)}"}), 500
