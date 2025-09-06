# api_predict.py  ── Flask Blueprint 라우트 모음
from flask import Blueprint, request, jsonify
from utils.predictor import predict_reward
import json

bp = Blueprint("predict_bp", __name__)

FEEDBACK_PATH = "feedback.jsonl"


# ─────────────────────────────────────────
# 1) 예측 API (/predict)
# ─────────────────────────────────────────
@bp.route("/predict", methods=["POST"])
def predict():
    try:
        payload = request.get_json(force=True) or {}
        text = (payload.get("text") or "").strip()
        if not text:
            return jsonify({"error": "Missing 'text' field"}), 400

        result = predict_reward(text)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": f"inference error: {str(e)}"}), 500


# ─────────────────────────────────────────
# 2) 피드백 API (/feedback)
#    사용자가 예측 결과를 교정하고 피드백을 보내는 API
# ─────────────────────────────────────────
@bp.route("/feedback", methods=["POST"])
def feedback():
    try:
        data = request.get_json(force=True) or {}
        text = (data.get("text") or "").strip()
        prediction = data.get("prediction", None)
        correct = data.get("correct", None)

        if not text or prediction is None or correct is None:
            return jsonify(
                {"error": "fields required: text, prediction, correct"}), 400

        # label 정규화: 맞았다면 prediction 그대로, 틀렸다면 반전
        pred_int = int(prediction)
        lbl = pred_int if bool(correct) else (1 - pred_int)

        entry = {
            "text": text,
            "prediction": pred_int,
            "correct": bool(correct),
            "label": int(lbl)
        }

        with open(FEEDBACK_PATH, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")

        return jsonify({
            "message": "feedback received",
            "label": int(lbl)
        }), 200

    except Exception as e:
        return jsonify({"error": f"feedback error: {str(e)}"}), 500
