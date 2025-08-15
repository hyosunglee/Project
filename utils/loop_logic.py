import json
import os
from utils.trainer import train_model
from utils.predictor import predict_reward

LOW_CONF_THRESHOLD = 0.6
RETRAIN_TRIGGER_COUNT = 10

def load_logs(file_path="logs.jsonl"):
    if not os.path.exists(file_path):
        return []
    with open(file_path, "r") as f:
        return [json.loads(line) for line in f]

def save_for_retraining(logs, file_path="retrain_buffer.jsonl"):
    with open(file_path, "a") as f:
        for log in logs:
            f.write(json.dumps(log) + "\n")

def loop_logic():
    logs = load_logs()
    low_conf_samples = []

    for log in logs:
        result = predict_reward(log["text"])
        if result["confidence"] < LOW_CONF_THRESHOLD:
            log["confidence"] = result["confidence"]
            low_conf_samples.append(log)

    if len(low_conf_samples) >= RETRAIN_TRIGGER_COUNT:
        print(f"[loop] Retraining triggered: {len(low_conf_samples)} samples")
        save_for_retraining(low_conf_samples)
        train_model()
    else:
        print(f"[loop] Low confidence count: {len(low_conf_samples)} — no retrain")
