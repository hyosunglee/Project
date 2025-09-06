import requests
from utils.paper_fetcher import fetch_arxiv_papers

import os

# 서버 엔드포인트 URL 정의 (환경 변수 또는 기본값 사용)
PORT = os.getenv("PORT", 3100)
BASE_URL = f"http://localhost:{PORT}"
INGEST_URL = f"{BASE_URL}/ingest"
CHECK_DUPLICATES_URL = f"{BASE_URL}/check_duplicates"

def collect_and_ingest(query="reinforcement learning", max_results=10):
    """
    지정된 쿼리로 ArXiv에서 논문을 수집하고, 중복을 확인한 뒤 새 논문만 서버의 /ingest 엔드포인트로 전송합니다.
    """
    print(f"🔍 '{query}' 관련 최신 논문 {max_results}개 수집 시작...")
    try:
        papers = fetch_arxiv_papers(query, max_results=max_results)
        if not papers:
            print("수집된 논문이 없습니다.")
            return
    except Exception as e:
        print(f"🔥 ArXiv에서 논문 수집 중 오류 발생: {e}")
        return

    paper_titles = [paper['title'] for paper in papers]
    print(f"✅ {len(papers)}개 논문 후보 확인 완료. 서버에 중복 여부를 확인합니다.")

    # 서버에 중복 확인 요청
    try:
        response = requests.post(CHECK_DUPLICATES_URL, json={"titles": paper_titles})
        response.raise_for_status()
        duplicates = set(response.json().get("duplicates", []))
        print(f"ℹ️ {len(duplicates)}개의 중복 논문을 확인했습니다.")
    except requests.exceptions.RequestException as e:
        print(f"🔥 서버와 통신 실패 (중복 확인): {e}")
        return

    # 새 논문만 필터링
    new_papers = [paper for paper in papers if paper['title'] not in duplicates]

    if not new_papers:
        print("✅ 새로운 논문이 없습니다. 모든 논문이 최신 상태입니다.")
        return

    print(f"📤 {len(new_papers)}개의 새로운 논문을 서버로 전송합니다...")

    for paper in new_papers:
        # 서버로 전송할 상세 데이터 구조화
        payload = {
            "title": paper["title"],
            "summary": paper["summary"],
            "authors": [author.name for author in paper.get("authors", [])], # Example of richer data
            "pdf_url": paper["pdf_url"],
            "source": "collector_v2",
            "query": query,
            # 시뮬레이션된 필드 (프로토타입 아이디어 확장)
            "idea": "강화학습 에이전트의 탐험 전략 개선",
            "keywords": ["Reinforcement Learning", "Exploration", "Novelty"],
            "label": 1 # 기본 레이블
        }

        try:
            response = requests.post(INGEST_URL, json=payload)
            response.raise_for_status()
            print(f"  - 전송 성공: \"{paper['title'][:40]}...\"")
        except requests.exceptions.RequestException as e:
            print(f"🔥 데이터 전송 실패: {e}")
            print(f"  - 실패한 논문: \"{paper['title'][:40]}...\"")

if __name__ == "__main__":
    # 스크립트를 직접 실행할 때 이 함수를 호출합니다.
    collect_and_ingest()
