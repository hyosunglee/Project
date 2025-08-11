import os
import json
import time
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
import joblib

LOG_PATH = "logs/experiment_log.json"  # 로그 경로
MODEL_DIR = "models"                   # 모델 저장 폴더
LATEST_LINK = os.path.join(MODEL_DIR, "reward_latest.pkl")


def load_logs(path: str = LOG_PATH) -> pd.DataFrame:
    with open(path, "r") as f:
        data = json.load(f)
    return pd.DataFrame(data)


def preprocess(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    for col in ("paper_title", "idea", "paper_summary"):
        if col not in df.columns:
            df[col] = ""
        df[col] = df[col].fillna("").astype(str)

    df["text"] = (df["paper_title"] + " " + df["idea"] + " " + df["paper_summary"]).str.strip()

    def _to_bin_local(x):
        if x is None:
            return np.nan
        s = str(x).strip().lower()
        if s in {"1", "true", "yes", "y"}:
            return 1
        if s in {"0", "false", "no", "n"}:
            return 0
        try:
            return 1 if float(s) > 0 else 0
        except Exception:
            return np.nan

    df["reward_bin"] = df.get("reward", np.nan).apply(_to_bin_local)
    df = df.dropna(subset=["text", "reward_bin"]).copy()
    df["reward_bin"] = df["reward_bin"].astype(int)
    return df[["text", "reward_bin"]]


def _save_versioned(model):
    os.makedirs(MODEL_DIR, exist_ok=True)
    ts = time.strftime("%Y%m%d-%H%M%S")
    versioned = os.path.join(MODEL_DIR, f"reward_cls_{ts}.pkl")
    joblib.dump(model, versioned)
    # latest 심링크/복사
    try:
        if os.path.islink(LATEST_LINK) or os.path.exists(LATEST_LINK):
            os.unlink(LATEST_LINK)
        os.symlink(os.path.basename(versioned), LATEST_LINK)
    except OSError:
        joblib.dump(model, LATEST_LINK)
    print(f"📦 모델 저장: {versioned}")
    print(f"🔗 최신 모델 갱신: {LATEST_LINK}")


def train_model():
    df = load_logs()
    df = preprocess(df)

    if df.empty or df["reward_bin"].nunique() < 2:
        print("❗ 학습 불가: 샘플 부족 또는 라벨 단일. /seed 또는 /loop로 로그를 더 쌓아주세요.")
        return

    X_train, X_test, y_train, y_test = train_test_split(
        df["text"], df["reward_bin"], test_size=0.2, random_state=42, stratify=df["reward_bin"]
    )

    model = make_pipeline(
        TfidfVectorizer(),
        LogisticRegression(max_iter=1000, class_weight="balanced")
    )
    model.fit(X_train, y_train)
    acc = model.score(X_test, y_test)
    print(f"✅ 모델 학습 완료 (정확도: {acc:.2f})")

    _save_versioned(model)


def train_model_from_logs():
    try:
        train_model()
    except Exception as e:
        print(f"🔥 학습 중 오류: {e}")


if __name__ == "__main__":
    train_model()
