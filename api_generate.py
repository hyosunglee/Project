# api_generate.py
from flask import Blueprint, request, jsonify
from utils.generator import generate_paper_summary
from utils.result_logger import save_result  # 생성 결과도 저장한다면 사용

bp_generate = Blueprint("generate_bp", __name__)

@bp_generate.route("/generate", methods=["POST"])
def generate():
    """
    요청 body의 'prompt' 값을 이용해 논문 요약 텍스트를 생성한다.
    성공 시 {"prompt": ..., "generated_summary": ...} 형태의 JSON 반환.
    """
    data = request.get_json(force=True) or {}
    prompt = (data.get("prompt") or "").strip()
    if not prompt:
        return jsonify({"error": "Missing 'prompt' field"}), 400

    try:
        result = generate_paper_summary(prompt)
        # 결과를 JSON 파일로 저장하고 싶다면 주석 해제
        # save_result("generated", result)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": f"Generation error: {e}"}), 500
