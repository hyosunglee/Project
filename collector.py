import requests
import json
from utils.paper_fetcher import fetch_arxiv_papers

# 서버의 ingest 엔드포인트 URL
INGEST_URL = "http://localhost:3000/ingest"

def collect_and_ingest(query="reinforcement learning", max_results=5):
    """
    지정된 쿼리로 ArXiv에서 논문을 수집하고 서버의 /ingest 엔드포인트로 전송합니다.
    """
    print(f"🔍 '{query}' 관련 논문 수집 시작...")
    try:
        papers = fetch_arxiv_papers(query, max_results=max_results)
        if not papers:
            print("수집된 논문이 없습니다.")
            return
    except Exception as e:
        print(f"🔥 ArXiv에서 논문 수집 중 오류 발생: {e}")
        return

    print(f"✅ {len(papers)}개의 논문 수집 완료. 서버로 전송을 시작합니다.")

    for paper in papers:
        payload = {
            "text": f"{paper['title']}\n\n{paper['summary']}",
            "label": 1  # 기본 레이블을 1로 설정
        }

        try:
            response = requests.post(INGEST_URL, json=payload)
            response.raise_for_status()  # HTTP 오류 발생 시 예외 처리
            print(f"📤 논문 전송 성공: \"{paper['title'][:30]}...\"")
        except requests.exceptions.RequestException as e:
            print(f"🔥 서버로 데이터 전송 실패: {e}")
            print(f"🔴 실패한 논문: \"{paper['title'][:30]}...\"")

if __name__ == "__main__":
    # 스크립트를 직접 실행할 때 이 함수를 호출합니다.
    collect_and_ingest()
