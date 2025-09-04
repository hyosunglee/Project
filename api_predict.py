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
# 2) 리서치 → 학습 연결용 인입 API (/ingest)
#    요청: {"text": "...", "label": 0|1(옵션, 기본 1)}
#    저장: 프로젝트 루트의 logs.jsonl (JSON Lines)
# ─────────────────────────────────────────
LOG_PATH = "logs.jsonl"


@bp.route("/ingest", methods=["POST"])
def ingest():
    try:
        data = request.get_json(force=True) or {}
        text = (data.get("text") or "").strip()
        label_raw = data.get("label", 1)

        # label 정규화 (0/1 정수)
        try:
            label = int(label_raw)
        except Exception:
            label = 1
        label = 1 if label else 0

        if not text:
            return jsonify({"error": "text required"}), 400

        entry = {"text": text, "label": label}
        with open(LOG_PATH, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")

        return jsonify({"message": "ingested", "n": 1}), 200
    except Exception as e:
        return jsonify({"error": f"ingest error: {str(e)}"}), 500


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
