import arxiv

def fetch_arxiv_papers(query, max_results=10):
    """
    Fetches papers from arXiv based on a query.
    """
    search = arxiv.Search(
        query=query,
        max_results=max_results,
        sort_by=arxiv.SortCriterion.SubmittedDate
    )

    papers = []
    for result in search.results():
        papers.append({
            "title": result.title,
            "summary": result.summary,
            "pdf_url": result.pdf_url,
        })

    return papers
