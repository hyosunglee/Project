import json
import os
import sys
from datetime import datetime
from utils.trainer import train_model
from utils.predictor import predict_reward

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from virtue_engine import ResearchAssistantVirtueEngine, VirtueState

LOW_CONF_THRESHOLD = 0.6
HIGH_CONF_THRESHOLD = 0.8
RETRAIN_TRIGGER_COUNT = 10
RESULTS_DIR = "results"

virtue_engine = ResearchAssistantVirtueEngine()

def compute_research_context(logs, last_train_time=None):
    """현재 연구 상태를 기반으로 VirtueEngine 컨텍스트 계산"""
    total_logs = len(logs)
    
    if total_logs < 50:
        task_stage = "explore"
        info_density = total_logs / 100.0
    elif total_logs < 200:
        task_stage = "review"
        info_density = min(0.7, total_logs / 300.0)
    else:
        task_stage = "synthesise"
        info_density = min(1.0, total_logs / 500.0)
    
    if last_train_time:
        hours_since_train = (datetime.now() - last_train_time).total_seconds() / 3600
        deadline_hours = max(1, 6 - hours_since_train)
    else:
        deadline_hours = 24
    
    return {
        "task_stage": task_stage,
        "deadline_hours": deadline_hours,
        "information_density": info_density,
        "total_papers": total_logs
    }

def get_available_actions():
    """시스템에서 가능한 모든 액션 목록"""
    return [
        ("collect_more_papers", {"description": "ArXiv에서 새 논문 수집"}),
        ("summarise_current_findings", {"description": "현재 데이터 분석 및 요약"}),
        ("plan_next_steps", {"description": "다음 연구 단계 계획"}),
        ("write_draft_outline", {"description": "연구 결과 초안 작성"}),
        ("auto_generate_predictions", {"description": "자동 예측 생성"}),
    ]

def virtue_state_to_dict(state: VirtueState) -> dict:
    """VirtueState를 JSON 직렬화 가능한 dict로 변환"""
    return {
        "wisdom": round(state.wisdom, 4),
        "understanding": round(state.understanding, 4),
        "counsel": round(state.counsel, 4),
        "strength": round(state.strength, 4),
        "knowledge": round(state.knowledge, 4),
        "reverence": round(state.reverence, 4)
    }

def load_logs(file_path="logs.jsonl"):
    if not os.path.exists(file_path):
        return []
    with open(file_path, "r") as f:
        return [json.loads(line) for line in f]

def save_for_retraining(logs, file_path="retrain_buffer.jsonl"):
    with open(file_path, "a") as f:
        for log in logs:
            f.write(json.dumps(log) + "\n")

def save_prediction_results(predictions, low_conf_count, total_count, high_conf_details, virtue_info=None):
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
    
    if virtue_info:
        result["virtue_analysis"] = virtue_info
    
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
    
    context = compute_research_context(logs)
    virtue_state = virtue_engine.evaluate_context(context)
    
    print(f"🧭 [VirtueEngine] 현재 상태 분석:")
    print(f"   연구 단계: {context['task_stage']}")
    print(f"   정보 밀도: {context['information_density']:.2f}")
    print(f"   논문 수: {context['total_papers']}")
    
    state_dict = virtue_state_to_dict(virtue_state)
    top_virtues = sorted(state_dict.items(), key=lambda x: x[1], reverse=True)[:3]
    print(f"   주요 덕목: {', '.join(f'{v[0]}({v[1]:.2f})' for v in top_virtues)}")
    
    actions = get_available_actions()
    ranked_actions = virtue_engine.filter_actions(context, actions, virtue_state)
    
    print(f"   추천 액션 순위:")
    for i, (name, _) in enumerate(ranked_actions[:3], 1):
        print(f"     {i}. {name}")

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
    
    return {
        "context": context,
        "virtue_state": state_dict,
        "ranked_actions": [(name, payload.get("description", "")) for name, payload in ranked_actions],
        "low_conf_count": len(low_conf_samples)
    }

def predict_after_training():
    print("🔮 [학습 후 예측] 전체 데이터 예측 시작...")
    predictions, low_conf_samples, total, high_conf_details = run_predictions_on_logs()
    
    if predictions:
        logs = load_logs()
        context = compute_research_context(logs)
        virtue_state = virtue_engine.evaluate_context(context)
        state_dict = virtue_state_to_dict(virtue_state)
        
        actions = get_available_actions()
        ranked_actions = virtue_engine.filter_actions(context, actions, virtue_state)
        
        virtue_info = {
            "context": context,
            "virtue_state": state_dict,
            "recommended_actions": [(name, payload.get("description", "")) for name, payload in ranked_actions[:3]]
        }
        
        print(f"🧭 [VirtueEngine] 예측 시 덕목 상태:")
        top_virtues = sorted(state_dict.items(), key=lambda x: x[1], reverse=True)[:3]
        print(f"   주요 덕목: {', '.join(f'{v[0]}({v[1]:.2f})' for v in top_virtues)}")
        
        save_prediction_results(predictions, len(low_conf_samples), total, high_conf_details, virtue_info)
        return True
    else:
        print("[예측] 예측할 데이터 없음")
        return False
