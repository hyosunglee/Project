import json
import os
from datetime import datetime
from utils.trainer import train_model
from utils.predictor import predict_reward

LOW_CONF_THRESHOLD = 0.6
HIGH_CONF_THRESHOLD = 0.8
RETRAIN_TRIGGER_COUNT = 10
RESULTS_DIR = "results"

def load_logs(file_path="logs.jsonl"):
    if not os.path.exists(file_path):
        return []
    with open(file_path, "r") as f:
        return [json.loads(line) for line in f]

def save_for_retraining(logs, file_path="retrain_buffer.jsonl"):
    with open(file_path, "a") as f:
        for log in logs:
            f.write(json.dumps(log) + "\n")

def save_prediction_results(predictions, low_conf_count, total_count, high_conf_details):
    os.makedirs(RESULTS_DIR, exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    high_conf_count = len(high_conf_details)
    
    result = {
        "timestamp": datetime.now().isoformat(),
        "type": "batch_prediction",
        "summary": {
            "total_predictions": total_count,
            "high_confidence_80": high_conf_count,
            "medium_confidence": total_count - low_conf_count - high_conf_count,
            "low_confidence": low_conf_count,
            "avg_confidence": round(sum(p["confidence"] for p in predictions) / len(predictions), 4) if predictions else 0,
            "low_threshold": LOW_CONF_THRESHOLD,
            "high_threshold": HIGH_CONF_THRESHOLD
        },
        "predictions": predictions,
        "high_confidence_details": high_conf_details
    }
    
    filepath = os.path.join(RESULTS_DIR, f"prediction_{ts}.json")
    with open(filepath, "w") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
    
    print(f"📊 [예측] 결과 저장: {filepath}")
    print(f"   - 총 {total_count}개 예측")
    print(f"   - 높은 신뢰도(80%+): {high_conf_count}개 (상세 내용 포함)")
    print(f"   - 낮은 신뢰도(<60%): {low_conf_count}개")
    
    return filepath

def run_predictions_on_logs():
    logs = load_logs()
    predictions = []
    low_conf_samples = []
    high_conf_details = []
    
    if not logs:
        print("[예측] 로그 데이터 없음")
        return [], [], 0, []
    
    for log in logs:
        text = log.get("text") or log.get("summary", "")
        if not text:
            continue
        
        result = predict_reward(text)
        
        pred_record = {
            "title": log.get("title", "")[:100],
            "text_preview": text[:200],
            "prediction": result["prediction"],
            "confidence": result["confidence"]
        }
        predictions.append(pred_record)
        
        if result["confidence"] >= HIGH_CONF_THRESHOLD:
            high_conf_record = {
                "title": log.get("title", ""),
                "text": text,
                "prediction": result["prediction"],
                "confidence": result["confidence"],
                "source": log.get("source", "unknown")
            }
            high_conf_details.append(high_conf_record)
        
        if result["confidence"] < LOW_CONF_THRESHOLD:
            log["confidence"] = result["confidence"]
            low_conf_samples.append(log)
    
    return predictions, low_conf_samples, len(predictions), high_conf_details

def loop_logic():
    logs = load_logs()
    low_conf_samples = []

    for log in logs:
        text = log.get("text") or log.get("summary", "")
        if not text:
            continue
            
        result = predict_reward(text)
        if result["confidence"] < LOW_CONF_THRESHOLD:
            log["confidence"] = result["confidence"]
            low_conf_samples.append(log)

    if len(low_conf_samples) >= RETRAIN_TRIGGER_COUNT:
        print(f"[loop] Retraining triggered: {len(low_conf_samples)} samples")
        save_for_retraining(low_conf_samples)
        train_model()
    else:
        print(f"[loop] Low confidence count: {len(low_conf_samples)} — no retrain")

def predict_after_training():
    print("🔮 [학습 후 예측] 전체 데이터 예측 시작...")
    predictions, low_conf_samples, total, high_conf_details = run_predictions_on_logs()
    
    if predictions:
        save_prediction_results(predictions, len(low_conf_samples), total, high_conf_details)
        return True
    else:
        print("[예측] 예측할 데이터 없음")
        return False
