import json
import re
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import logging

def extract_accuracy(result_str):
    match = re.search(r"accuracy\s*([0-9.]+)", result_str, re.IGNORECASE)
    if match:
        return float(match.group(1))
    return None


def train_model_from_logs():
    try:
        with open("logs/experiment_logs.json", "r") as f:
            logs = json.load(f)
    except FileNotFoundError:
        logging.error("❗ logs/experiment_logs.json not found. Run /loop to generate logs first.")
        return

    X_texts = []
    y = []

    for log in logs:
        acc = extract_accuracy(log.get("result", ""))
        if acc is None:
            continue

        input_text = f"{log.get('summary', '')} {log.get('idea', '')} {log.get('code', '')}"
        X_texts.append(input_text)
        y.append(acc)

    if len(X_texts) < 5:
        logging.warning("❗ Not enough data to train. At least 5 data points are needed.")
        return

    vectorizer = TfidfVectorizer(max_features=1000)
    X = vectorizer.fit_transform(X_texts)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = LinearRegression()
    model.fit(X_train, y_train)

    pred = model.predict(X_test)
    mse = mean_squared_error(y_test, pred)
    logging.info(f"✅ Model training complete. Test MSE: {mse:.4f}")
