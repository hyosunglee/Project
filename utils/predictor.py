# utils/predictor.py
from pathlib import Path
import joblib
from sklearn.pipeline import Pipeline, make_pipeline
from sklearn.feature_extraction.text import TfidfVectorizer

ROOT = Path(__file__).resolve().parents[1]
MODELS_DIR = ROOT / "models"


def _resolve_model_path() -> Path:
    latest = MODELS_DIR / "reward_latest.pkl"
    if latest.exists():
        return latest
    cands = sorted(MODELS_DIR.glob("reward_cls_*.pkl"),
                   key=lambda p: p.stat().st_mtime,
                   reverse=True)
    if cands:
        return cands[0]
    cwd_latest = Path.cwd() / "models" / "reward_latest.pkl"
    if cwd_latest.exists():
        return cwd_latest
    raise FileNotFoundError("모델 파일이 없습니다. /train 먼저 실행하세요.")


def _to_pipeline(obj):
    """obj가 Pipeline이면 그대로, (vec, clf) 튜플이면 감싸서, 분류기 단독이면 TF-IDF 붙여서 Pipeline로 표준화."""
    if isinstance(obj, Pipeline):
        return obj
    # (a, b) 튜플 → 벡터라이저/분류기 판별
    if isinstance(obj, tuple) and len(obj) == 2:
        a, b = obj

        def is_vec(x):
            return hasattr(x, "fit") and hasattr(
                x, "transform") and not hasattr(x, "predict")

        def is_clf(x):
            return hasattr(x, "fit") and hasattr(x, "predict")

        if is_vec(a) and is_clf(b):
            return Pipeline([("vectorizer", a), ("clf", b)])
        if is_vec(b) and is_clf(a):
            return Pipeline([("vectorizer", b), ("clf", a)])
        # 모르겠으면 분류기처럼 보이는 걸 TF-IDF로 감싼다
        clf = a if is_clf(a) else b
        return make_pipeline(TfidfVectorizer(), clf)
    # 분류기 단독
    if hasattr(obj, "fit") and hasattr(obj, "predict"):
        return make_pipeline(TfidfVectorizer(), obj)
    raise TypeError("알 수 없는 모델 형식입니다. Pipeline/튜플/분류기만 지원.")


def predict_reward(text: str):
    text = (text or "").strip()
    if not text:
        return {"error": "empty text"}, 400
    path = _resolve_model_path()
    loaded = joblib.load(path)  # 튜플일 수도, 파이프라인일 수도 있음
    pipeline = _to_pipeline(loaded)  # 표준화
    prob = pipeline.predict_proba([text])
    pred = pipeline.predict([text])
    return {
        "prediction": int(pred[0]),
        "confidence": float(round(max(prob[0]), 4))
    }
