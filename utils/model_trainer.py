import joblib, shutil, os
import json, time
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from pathlib import Path

LOG_PATH = "logs/experiment_log.json"  # 로그 경로
MODEL_DIR = "models"  # 모델 저장 폴더
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

    df["text"] = (df["paper_title"] + " " + df["idea"] + " " +
                  df["paper_summary"]).str.strip()

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


MODELS_DIR = "models"
LATEST_LINK = os.path.join(MODELS_DIR, "reward_latest.pkl")


def _save_versioned(pipeline):
    os.makedirs(MODELS_DIR, exist_ok=True)
    ts = time.strftime("%Y%m%d_%H%M%S")
    versioned = os.path.join(MODELS_DIR, f"reward_cls_{ts}.pkl")

    # 버전 파일 저장 (pipeline 하나만 저장)
    joblib.dump(pipeline, versioned)

    # 최신 링크/복사 갱신 (replit에서 symlink 실패 대비)
    try:
        if os.path.islink(LATEST_LINK) or os.path.exists(LATEST_LINK):
            os.remove(LATEST_LINK)
        os.symlink(os.path.basename(versioned), LATEST_LINK)
    except Exception:
        shutil.copyfile(versioned, LATEST_LINK)  # 링크 실패 시 파일 복사로 대체


ROOT = Path(__file__).resolve().parents[1]
MODELS_DIR = ROOT / "models"
LATEST = MODELS_DIR / "reward_latest.pkl"


def _coerce_to_pipeline(obj):
    if isinstance(obj, Pipeline):
        return obj
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
        clf = a if is_clf(a) else b
        return make_pipeline(TfidfVectorizer(), clf)
    if hasattr(obj, "fit") and hasattr(obj, "predict"):
        return make_pipeline(TfidfVectorizer(), obj)
    raise TypeError("Pipeline/튜플/분류기만 허용")


def save_pipeline(pipeline_or_tuple, keep: int = 5):
    MODELS_DIR.mkdir(parents=True, exist_ok=True)
    pipeline = _coerce_to_pipeline(pipeline_or_tuple)
    ts = time.strftime("%Y%m%d_%H%M%S")
    versioned = MODELS_DIR / f"reward_cls_{ts}.pkl"
    joblib.dump(pipeline, versioned)
    try:
        if LATEST.exists() or LATEST.is_symlink():
            LATEST.unlink()
        os.symlink(versioned.name, LATEST)
    except Exception:
        shutil.copyfile(versioned, LATEST)
    # 롤링 정리
    cands = sorted(MODELS_DIR.glob("reward_cls_*.pkl"),
                   key=lambda p: p.stat().st_mtime,
                   reverse=True)
    for p in cands[keep:]:
        try:
            p.unlink()
        except:
            pass


def load_feedback_df(path="feedback.jsonl"):
    rows = []
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                try:
                    o = json.loads(line)
                    rows.append({
                        "text":
                        o["text"],
                        "reward_bin":
                        int(o.get("label", o.get("prediction", 0)))
                    })
                except:
                    pass
    return pd.DataFrame(rows, columns=["text", "reward_bin"])


def train_model():
    import pandas as pd
    from sklearn.model_selection import train_test_split
    from sklearn.pipeline import make_pipeline
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.linear_model import LogisticRegression
    from sklearn.metrics import accuracy_score, f1_score

    # 0) 원본 로그 + 피드백 로드
    df_logs = load_logs()  # 기존 로그 (text, label/reward_bin 등)
    fb = load_feedback_df()  # feedback.jsonl → (text, reward_bin) 형태 권장

    # 1) 전처리 전에 합치기 (같은 규칙으로 한 번만 preprocess)
    if fb is not None and not fb.empty:
        # 혹시 feedback에 'label'로 들어왔다면 이름 맞춰줌
        if "reward_bin" not in fb.columns and "label" in fb.columns:
            fb = fb.rename(columns={"label": "reward_bin"})
        fb = fb[["text", "reward_bin"]]
        df = pd.concat([df_logs, fb], ignore_index=True)
    else:
        df = df_logs

    # 2) 공통 전처리
    df = preprocess(df)

    # 3) 정합성 체크
    if df is None or df.empty:
        print("❗ 학습 불가: 데이터가 없습니다. /seed·/ingest·/feedback으로 데이터를 쌓아주세요.")
        return
    if "text" not in df.columns or "reward_bin" not in df.columns:
        print("❗ 학습 불가: 필요한 컬럼(text, reward_bin)이 없습니다. preprocess()를 확인하세요.")
        return

    df = df.dropna(subset=["text", "reward_bin"])
    df["reward_bin"] = df["reward_bin"].astype(int)

    # 클래스 수/분포 점검 (stratify 안정화)
    if df["reward_bin"].nunique() < 2:
        print("❗ 학습 불가: 라벨이 한 가지뿐입니다. 0/1 둘 다 들어오게 /ingest·/feedback을 추가하세요.")
        return
    # 각 클래스 최소 2개 이상 권장 (stratify에 필요)
    if df["reward_bin"].value_counts().min() < 2:
        print("❗ 학습 불가: 각 클래스 최소 2개 이상 필요. 샘플을 더 넣어주세요.")
        return

    # 4) 데이터 분리
    X_train, X_test, y_train, y_test = train_test_split(
        df["text"],
        df["reward_bin"],
        test_size=0.2,
        random_state=42,
        stratify=df["reward_bin"])

    # 5) 파이프라인 학습
    model = make_pipeline(
        TfidfVectorizer(),
        LogisticRegression(max_iter=1000, class_weight="balanced"))
    model.fit(X_train, y_train)

    # 6) 평가(로그용)
    y_pred = model.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)
    print(f"✅ 모델 학습 완료 (정확도: {acc:.2f}, F1: {f1:.2f})")

    # 7) 저장 (항상 Pipeline로 저장)
    save_pipeline(model)


def train_model_from_logs():
    try:
        train_model()
    except Exception as e:
        print(f"🔥 학습 중 오류: {e}")


if __name__ == "__main__":
    train_model()
