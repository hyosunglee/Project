import json
import pickle
from datetime import datetime
from pathlib import Path
from typing import List

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, f1_score
from sklearn.model_selection import train_test_split

from utils.meta import increment_stat, record_checkpoint
from utils.paths import LOG_PATH, META_DIR, MODELS_DIR, RETRAIN_BUFFER_PATH, model_symlink_path


def load_logs(file_path: Path) -> List[dict]:
    if not file_path.exists():
        return []
    with open(file_path, "r", encoding="utf-8") as f:
        return [json.loads(line) for line in f]


def update_symlink(new_model_path: Path):
    symlink_path = model_symlink_path()
    try:
        if symlink_path.exists() or symlink_path.is_symlink():
            symlink_path.unlink()
        symlink_path.symlink_to(new_model_path)
        print(f"[symlink] Updated to {new_model_path}")
    except Exception as e:
        print(f"[symlink] Failed: {e}")


def train_model():
    logs = load_logs(LOG_PATH) + load_logs(RETRAIN_BUFFER_PATH)

    if not logs:
        print("[train] No logs found to train on.")
        return None

    # text 또는 summary 필드 사용
    texts = [x.get("text") or x.get("summary", "") for x in logs]
    labels = [x.get("label", 1) for x in logs]

    # 빈 텍스트 필터링
    valid_data = [(t, l) for t, l in zip(texts, labels) if t.strip()]
    if not valid_data:
        print("[train] No valid text data found.")
        return None

    texts, labels = zip(*valid_data)

    if len(set(labels)) < 2:
        print("[train] Not enough class diversity to train.")
        return None

    X_train, X_test, y_train, y_test = train_test_split(
        texts, labels, test_size=0.2, random_state=42, stratify=labels
    )

    vectorizer = TfidfVectorizer()
    X_train_vec = vectorizer.fit_transform(X_train)
    X_test_vec = vectorizer.transform(X_test)

    model = LogisticRegression()
    model.fit(X_train_vec, y_train)

    # 모델 저장
    ts = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    MODELS_DIR.mkdir(parents=True, exist_ok=True)
    model_path = MODELS_DIR / f"reward_v{ts}.pkl"
    with open(model_path, "wb") as f:
        pickle.dump((model, vectorizer), f)

    # 심볼릭 링크 갱신
    update_symlink(model_path)

    # 메트릭 저장
    y_pred = model.predict(X_test_vec)
    metrics = {
        "model": str(model_path),
        "timestamp": ts,
        "data_count": len(logs),
        "train_size": len(X_train),
        "test_size": len(X_test),
        "accuracy": round(float(accuracy_score(y_test, y_pred)), 4),
        "f1_score": round(float(f1_score(y_test, y_pred, zero_division=0.0)), 4),
    }
    metrics_path = META_DIR / f"metrics_{ts}.json"
    with open(metrics_path, "w", encoding="utf-8") as f:
        json.dump(metrics, f, indent=2)

    increment_stat("training", "runs")
    record_checkpoint(f"model saved at {model_path}", category="training")

    print(f"[train] Model saved: {model_path}")
    print(f"[train] Metrics: {metrics}")

    return metrics
