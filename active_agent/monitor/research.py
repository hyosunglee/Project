import arxiv
import time
from typing import List, Dict

def search_ai_feedback_loop_papers(max_results: int = 5, retries: int = 3) -> List[Dict]:
    """
    Searches for 'AI Feedback Loop' related papers on arXiv.
    Self-contained implementation using the arxiv library.
    """
    query = '"AI Feedback Loop"'

    print(f"📡 [ArXiv] 검색 시작: '{query}' (최대 {max_results}개)")

    for attempt in range(retries):
        try:
            client = arxiv.Client(
                page_size=100,
                delay_seconds=3.0,
                num_retries=3
            )

            search = arxiv.Search(
                query=query,
                max_results=max_results,
                sort_by=arxiv.SortCriterion.SubmittedDate
            )

            papers = []
            for result in client.results(search):
                paper = {
                    "title": result.title.strip(),
                    "summary": result.summary.strip(),
                    "pdf_url": result.pdf_url,
                }
                papers.append(paper)

            if papers:
                print(f"✅ [ArXiv] 성공: {len(papers)}개 논문 수집됨")
            else:
                print(f"⚠️ [ArXiv] 검색 결과 없음")

            return papers

        except Exception as e:
            print(f"❌ [ArXiv] 시도 {attempt + 1}/{retries} 실패: {e}")
            if attempt < retries - 1:
                time.sleep(2 ** attempt)
            else:
                return []

    return []

if __name__ == "__main__":
    results = search_ai_feedback_loop_papers()
    for i, paper in enumerate(results):
        print(f"[{i+1}] {paper['title']}")
