import os
import json
from datetime import datetime

RESULTS_DIR = "results"
os.makedirs(RESULTS_DIR, exist_ok=True)

def save_result(result_type, data):
    """
    결과를 JSON 파일로 저장
    result_type: 'prediction', 'training', 'collection' 등
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{result_type}_{timestamp}.json"
    filepath = os.path.join(RESULTS_DIR, filename)
    
    result = {
        "timestamp": datetime.now().isoformat(),
        "type": result_type,
        "data": data
    }
    
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    
    # 통합 결과 파일에도 추가
    all_results_file = os.path.join(RESULTS_DIR, "all_results.jsonl")
    with open(all_results_file, "a", encoding="utf-8") as f:
        f.write(json.dumps(result, ensure_ascii=False) + "\n")
    
    return filepath
