# utils/predictor.py
from pathlib import Path
import joblib
import os
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer

from utils.paths import model_symlink_path

# --- 전역 변수 설정 ---
# 모델과 벡터라이저를 메모리에 캐싱하여 반복적인 로드를 방지
cached_model = None
cached_vectorizer = None
cached_model_path = None
cached_model_mtime = None

MODEL_SYMLINK = model_symlink_path()

def load_model():
    """
    모델을 메모리에 로드하고 캐싱합니다.
    - 파일 경로가 변경되었거나 파일이 수정되었을 때만 다시 로드합니다.
    """
    global cached_model, cached_vectorizer, cached_model_path, cached_model_mtime

    # 심볼릭 링크를 통해 최신 모델 경로 확인
    if not MODEL_SYMLINK.exists():
        raise FileNotFoundError("모델 파일 링크(reward_latest.pkl)가 없습니다. /train 엔드포인트를 먼저 실행하세요.")

    current_model_path = Path(os.path.realpath(MODEL_SYMLINK))
    current_mtime = current_model_path.stat().st_mtime

    # 캐시된 모델이 최신 상태이면 그대로 반환
    if cached_model and cached_vectorizer and cached_model_path == current_model_path and cached_model_mtime == current_mtime:
        return cached_model, cached_vectorizer

    # 변경이 감지되면 모델을 다시 로드
    print(f"🔄 모델 변경 감지. '{current_model_path.name}' 로드 중...")
    try:
        model, vectorizer = joblib.load(current_model_path)

        # 캐시 업데이트
        cached_model = model
        cached_vectorizer = vectorizer
        cached_model_path = current_model_path
        cached_model_mtime = current_mtime

        print("✅ 모델 로드 및 캐싱 완료.")
        return model, vectorizer
    except Exception as e:
        print(f"🔥 모델 로드 실패: {e}")
        # 실패 시 캐시 초기화
        cached_model = cached_vectorizer = cached_model_path = cached_model_mtime = None
        raise e

def predict_reward(text: str):
    """
    주어진 텍스트에 대해 캐시된 모델을 사용하여 예측을 수행합니다.
    """
    text = (text or "").strip()
    if not text:
        return {"error": "empty text"}

    try:
        # 캐시된 모델을 가져오거나, 필요 시 새로 로드
        model, vectorizer = load_model()

        # 예측 수행
        text_vec = vectorizer.transform([text])
        prediction = model.predict(text_vec)
        proba = model.predict_proba(text_vec)

        return {
            "prediction": int(prediction[0]),
            "confidence": float(round(max(proba[0]), 4))
        }
    except FileNotFoundError as e:
        return {"error": str(e)}
    except Exception as e:
        return {"error": f"예측 중 오류 발생: {str(e)}"}
