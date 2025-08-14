import os
import json
import time
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import accuracy_score, f1_score
from datetime import datetime
import pickle

LOG_PATH = "logs.jsonl"
RETRAIN_BUFFER_PATH = "retrain_buffer.jsonl"
MODEL_DIR = "models"

def load_logs(file_path):
    if not os.path.exists(file_path):
        return []
    with open(file_path, "r") as f:
        return [json.loads(line) for line in f]

def update_symlink(new_model_path):
    symlink_path = os.path.join(MODEL_DIR, "reward_latest.pkl")
    try:
        if os.path.exists(symlink_path):
            os.remove(symlink_path)
        os.symlink(new_model_path, symlink_path)
        print(f"[symlink] Updated to {new_model_path}")
    except Exception as e:
        print(f"[symlink] Failed: {e}")

def train_model():
    logs = load_logs(LOG_PATH) + load_logs(RETRAIN_BUFFER_PATH)

    if not logs:
        print("[train] No logs found to train on.")
        return

    texts = [x["text"] for x in logs]
    labels = [x["label"] for x in logs]

    if len(set(labels)) < 2:
        print("[train] Not enough class diversity to train.")
        return

    X_train, X_test, y_train, y_test = train_test_split(
        texts, labels, test_size=0.2, random_state=42, stratify=labels
    )

    vectorizer = TfidfVectorizer()
    X_train_vec = vectorizer.fit_transform(X_train)
    X_test_vec = vectorizer.transform(X_test)

    model = LogisticRegression()
    model.fit(X_train_vec, y_train)

    # 모델 저장
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    model_path = os.path.join(MODEL_DIR, f"reward_cls_{ts}.pkl")
    os.makedirs(MODEL_DIR, exist_ok=True)
    with open(model_path, "wb") as f:
        pickle.dump((model, vectorizer), f)

    # 심볼릭 링크 갱신
    update_symlink(model_path)

    # 메트릭 저장
    y_pred = model.predict(X_test_vec)
    metrics = {
        "model": model_path,
        "accuracy": round(accuracy_score(y_test, y_pred), 4),
        "f1_score": round(f1_score(y_test, y_pred), 4)
    }
    metrics_path = os.path.join(MODEL_DIR, f"metrics_{ts}.json")
    with open(metrics_path, "w") as f:
        json.dump(metrics, f, indent=2)

    print(f"[train] Model saved: {model_path}")
    print(f"[train] Metrics: {metrics}")
