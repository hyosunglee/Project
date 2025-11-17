import arxiv
import time
from typing import List, Dict

def fetch_arxiv_papers(query: str, max_results: int = 10, retries: int = 3) -> List[Dict]:
    """
    ArXiv에서 논문을 수집합니다. 에러 처리 및 재시도 로직 포함.
    
    Args:
        query: 검색 쿼리
        max_results: 최대 결과 수
        retries: 실패 시 재시도 횟수
    
    Returns:
        논문 리스트 (각 논문은 title, summary, pdf_url 포함)
    """
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
            result_count = 0
            
            for result in client.results(search):
                result_count += 1
                try:
                    paper = {
                        "title": result.title.strip(),
                        "summary": result.summary.strip(),
                        "pdf_url": result.pdf_url,
                    }
                    papers.append(paper)
                    
                    if result_count <= 3:
                        print(f"  ✓ [{result_count}] {paper['title'][:60]}...")
                    
                except Exception as e:
                    print(f"  ⚠️ 논문 파싱 오류 (건너뜀): {e}")
                    continue
            
            if papers:
                print(f"✅ [ArXiv] 성공: {len(papers)}개 논문 수집됨")
            else:
                print(f"⚠️ [ArXiv] 검색 결과 없음")
            
            return papers
            
        except Exception as e:
            print(f"❌ [ArXiv] 시도 {attempt + 1}/{retries} 실패: {type(e).__name__}: {e}")
            
            if attempt < retries - 1:
                wait_time = 2 ** attempt
                print(f"   ⏳ {wait_time}초 후 재시도...")
                time.sleep(wait_time)
            else:
                print(f"💥 [ArXiv] 모든 재시도 실패. 빈 리스트 반환.")
                return []
    
    return []
