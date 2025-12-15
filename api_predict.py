# api_predict.py  ── Flask Blueprint 라우트 모음
from flask import Blueprint, request, jsonify
from utils.predictor import predict_reward
from utils.generator import generate_paper_summary
from utils.result_logger import save_result
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

        # 고신뢰도(80%+) 예측 시 자동 생성
        if result.get("prediction") == 1 and result.get("confidence", 0) >= 0.8:
            try:
                # 'text'를 프롬프트로 사용하여 요약 생성
                generated_data = generate_paper_summary(text)
                # 생성된 요약을 결과에 추가
                result["generated_summary"] = generated_data.get("generated_summary")
                # 생성된 결과도 로그에 저장
                save_result("generated_from_predict", {
                    "prompt": text[:100],
                    "summary": result["generated_summary"][:100]
                })
            except Exception as e:
                # 생성 중 오류가 발생해도 예측 결과는 반환하도록 처리
                result["generation_error"] = str(e)
        
        # 예측 결과 저장
        prediction_data = {
            "text": text[:100],  # 처음 100자만 저장
            "prediction": result.get("prediction"),
            "confidence": result.get("confidence")
        }
        save_result("prediction", prediction_data)
        
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
