#!/usr/bin/env python
"""
API 테스트 스크립트
모든 API 엔드포인트를 순차적으로 테스트합니다.
"""
import requests
import json
import sys

import os
BASE_URL = f"http://localhost:{os.getenv('PORT', 5000)}"

def print_section(title):
    print("\n" + "="*60)
    print(f"  {title}")
    print("="*60)

def print_response(response):
    print(f"Status: {response.status_code}")
    try:
        print(json.dumps(response.json(), indent=2, ensure_ascii=False))
    except:
        print(response.text)

def test_health():
    print_section("1. 서버 상태 확인")
    try:
        response = requests.get(f"{BASE_URL}/healthz")
        print_response(response)
        return response.status_code == 200
    except Exception as e:
        print(f"❌ 오류: {e}")
        return False

def test_seed(n=10):
    print_section(f"2. 테스트 데이터 {n}개 생성")
    try:
        response = requests.post(f"{BASE_URL}/seed?n={n}")
        print_response(response)
        return response.status_code == 200
    except Exception as e:
        print(f"❌ 오류: {e}")
        return False

def test_ingest():
    print_section("3. 데이터 추가 (ingest)")
    data = {
        "title": "Test Paper on Deep RL",
        "text": "이것은 심층 강화학습에 대한 테스트 논문입니다. Transformer 아키텍처를 사용합니다.",
        "label": 1
    }
    try:
        response = requests.post(f"{BASE_URL}/ingest", json=data)
        print_response(response)
        return response.status_code == 201
    except Exception as e:
        print(f"❌ 오류: {e}")
        return False

def test_train():
    print_section("4. 모델 학습")
    try:
        response = requests.post(f"{BASE_URL}/train")
        print_response(response)
        print("\n⏳ 학습이 백그라운드에서 진행됩니다. 몇 초 정도 소요됩니다.")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ 오류: {e}")
        return False

def test_predict():
    print_section("5. 예측")
    data = {
        "text": "강화학습 에이전트의 새로운 탐험 전략을 제안하는 논문입니다.",
        "target": "reward",
        "explain": True
    }
    try:
        response = requests.post(f"{BASE_URL}/predict", json=data)
        print_response(response)
        return response.status_code == 200
    except Exception as e:
        print(f"❌ 오류: {e}")
        return False

def test_check_duplicates():
    print_section("6. 중복 확인")
    data = {
        "titles": [
            "Test Paper on Deep RL",
            "Nonexistent Paper",
            "Synthetic Seed Paper #0"
        ]
    }
    try:
        response = requests.post(f"{BASE_URL}/check_duplicates", json=data)
        print_response(response)
        return response.status_code == 200
    except Exception as e:
        print(f"❌ 오류: {e}")
        return False

def main():
    print("\n🤖 Self-Learning AI System - API 테스트")
    print("━" * 60)
    
    results = []
    
    # 1. Health Check
    results.append(("서버 상태", test_health()))
    
    if not results[0][1]:
        print("\n❌ 서버가 실행되지 않았습니다. 먼저 서버를 시작하세요:")
        print("   python server.py")
        sys.exit(1)
    
    # 2. Seed Data
    results.append(("데이터 생성", test_seed(15)))
    
    # 3. Ingest Data
    results.append(("데이터 추가", test_ingest()))
    
    # 4. Train Model
    results.append(("모델 학습", test_train()))
    
    # Wait for training
    import time
    print("\n⏳ 학습 완료를 기다리는 중...")
    time.sleep(5)
    
    # 5. Predict
    results.append(("예측", test_predict()))
    
    # 6. Check Duplicates
    results.append(("중복 확인", test_check_duplicates()))
    
    # Summary
    print_section("테스트 결과 요약")
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ 성공" if result else "❌ 실패"
        print(f"{status} - {test_name}")
    
    print(f"\n총 {total}개 테스트 중 {passed}개 통과 ({passed/total*100:.0f}%)")
    
    if passed == total:
        print("\n🎉 모든 테스트를 통과했습니다!")
    else:
        print("\n⚠️  일부 테스트가 실패했습니다.")

if __name__ == "__main__":
    main()
