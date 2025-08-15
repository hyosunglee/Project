# utils/predictor.py

import pickle
import os
import joblib

def load_model():
    model_path = "models/reward_latest.pkl"
    if not os.path.exists(model_path):
        return None, None
    with open(model_path, "rb") as f:
        model, vectorizer = pickle.load(f)
    return model, vectorizer

def predict_reward(text):
    model, vectorizer = load_model()
    if model is None or vectorizer is None:
        return {
            "prediction": -1, # Or some other indicator of no model
            "confidence": 0.0
        }

    X = vectorizer.transform([text])
    prob = model.predict_proba(X)[0]
    pred_label = model.predict(X)[0]
    confidence = max(prob)

    return {
        "prediction": int(pred_label),




def predict_reward(text):
    with open("models/reward_latest.pkl", "rb") as f:
        pipeline = joblib.load(f)

    X = [text]
    prob = pipeline.predict_proba(X)
    pred = pipeline.predict(X)
    confidence = max(prob[0])

    return {
        "prediction": int(pred[0]),

        "confidence": round(float(confidence), 4)
    }
