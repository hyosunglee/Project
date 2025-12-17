#!/usr/bin/env python
"""
시스템 자동 초기화 스크립트
서버 시작 시 자동으로 초기 데이터 생성 및 학습 수행
"""
import os
import time
import requests
import json

from utils.paths import LOG_PATH, RESULTS_DIR

BASE_URL = f"http://localhost:{os.getenv('PORT', 3000)}"

def wait_for_server(max_wait=30):
    """서버가 준비될 때까지 대기"""
    print("⏳ 서버 시작 대기 중...")
    for i in range(max_wait):
        try:
            response = requests.get(f"{BASE_URL}/healthz", timeout=1)
            if response.status_code == 200:
                print("✅ 서버 준비 완료")
                return True
        except:
            time.sleep(1)
    return False

def check_logs_exist():
    """로그 파일이 있는지 확인"""
    return LOG_PATH.exists() and LOG_PATH.stat().st_size > 0

def initialize_system():
    """시스템 초기화"""
    print("\n🤖 자율 학습 시스템 자동 초기화")
    print("=" * 60)
    
    if not wait_for_server():
        print("❌ 서버 시작 실패")
        return False
    
    # 로그가 없으면 초기 데이터 생성
    if not check_logs_exist():
        print("\n📊 초기 데이터 생성 중...")
        try:
            response = requests.post(f"{BASE_URL}/seed?n=50")
            if response.status_code == 200:
                print("✅ 50개의 테스트 데이터 생성 완료")
            else:
                print(f"⚠️ 데이터 생성 실패: {response.status_code}")
        except Exception as e:
            print(f"❌ 오류: {e}")
            return False
    else:
        print("✅ 기존 로그 데이터 발견")
    
    # 초기 모델 학습
    print("\n🎓 초기 모델 학습 시작...")
    try:
        response = requests.post(f"{BASE_URL}/train")
        if response.status_code == 200:
            print("✅ 모델 학습 시작됨 (백그라운드)")
            time.sleep(3)  # 학습 완료 대기
        else:
            print(f"⚠️ 학습 시작 실패: {response.status_code}")
    except Exception as e:
        print(f"❌ 오류: {e}")
    
    # 첫 번째 논문 수집
    print("\n📚 초기 논문 수집 시작...")
    try:
        response = requests.post(f"{BASE_URL}/loop")
        if response.status_code == 200:
            print("✅ 논문 수집 완료")
        else:
            print(f"⚠️ 논문 수집 실패: {response.status_code}")
    except Exception as e:
        print(f"⚠️ 논문 수집 오류: {e}")
    
    print("\n" + "=" * 60)
    print("🎉 자동 초기화 완료!")
    print("\n자동화 스케줄:")
    print("  - 논문 수집: 1시간마다")
    print("  - 모델 재학습: 6시간마다")
    print("\n결과 저장 위치:")
    print(f"  - {RESULTS_DIR}/YYYY-MM-DD.jsonl (일별 수집/예측 로그)")
    print(f"  - {RESULTS_DIR}/summary_latest.json (마지막 요약)")
    print("\nAPI 엔드포인트: http://localhost:3000")
    print("=" * 60)
    
    return True

if __name__ == "__main__":
    initialize_system()
