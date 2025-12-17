from __future__ import annotations

import traceback
from typing import List, Tuple

from utils.logger import get_all_logged_titles, log_experiment
from utils.loop_logic import loop_logic
from utils.meta import record_checkpoint
from utils.result_logger import save_result

try:
    from utils.paper_fetcher import fetch_arxiv_papers
except Exception:
    fetch_arxiv_papers = None

SEARCH_KEYWORDS: List[str] = [
    "reinforcement learning",
    "deep learning",
    "neural networks",
    "computer vision",
    "natural language processing",
    "transformer models",
    "generative AI",
    "machine learning optimization",
    "graph neural networks",
    "meta learning",
]
keyword_counter = [0]


def _collect_papers() -> Tuple[list, list]:
    collected_papers = []
    papers = []

    if not fetch_arxiv_papers:
        return collected_papers, papers

    current_index = keyword_counter[0]
    current_keyword = SEARCH_KEYWORDS[current_index % len(SEARCH_KEYWORDS)]
    sort_mode = "relevance" if current_index % 2 == 0 else "submitted"
    keyword_counter[0] += 1

    try:
        papers = fetch_arxiv_papers(current_keyword, max_results=30, sort_by=sort_mode)
    except Exception as exc:  # noqa: BLE001
        record_checkpoint(f"paper fetch failed: {exc}", category="loop_error")
        return collected_papers, papers

    logged_titles = get_all_logged_titles()
    for paper in papers:
        title = paper.get("title", "untitled")
        summary = paper.get("summary", "No summary")
        if title in logged_titles:
            continue
        log_entry = {
            "title": title,
            "text": summary,
            "summary": summary,
            "source": "loop",
            "label": 1,
        }
        log_experiment(log_entry)
        collected_papers.append({"title": title, "summary": summary[:100]})
    return collected_papers, papers


def run_loop_once():
    """논문 수집 → 루프 로직 → 결과 저장 단일 사이클"""
    try:
        collected_papers, papers = _collect_papers()
        loop_logic()

        result_data = {
            "collected_count": len(collected_papers),
            "papers": collected_papers,
            "searched": len(papers) if papers else 0,
        }
        result_file = save_result("collection", result_data)
        record_checkpoint(f"loop success ({len(collected_papers)} new papers) -> {result_file}", category="loop")
        return {
            "message": "Loop 실행 완료",
            "collected": len(collected_papers),
            "result_file": str(result_file),
        }
    except Exception as exc:  # noqa: BLE001
        record_checkpoint(f"loop error: {exc}\n{traceback.format_exc()}", category="loop_error")
        return {
            "message": "Loop 실행 실패",
            "error": str(exc),
        }
