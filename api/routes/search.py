from fastapi import APIRouter, HTTPException
import json
from pathlib import Path

router = APIRouter()

LOG_PATH = Path("logs.jsonl")

@router.get("/search")
async def search(q: str, page: int = 1, size: int = 10):
    if not LOG_PATH.exists():
        return {"results": [], "paging": {"total": 0, "page": page, "size": size}}

    results = []
    with open(LOG_PATH, "r", encoding="utf-8") as f:
        for line in f:
            try:
                paper = json.loads(line)
                if q.lower() in (paper.get("title", "") + paper.get("text", "")).lower():
                    results.append({
                        "title": paper.get("title"),
                        "author": paper.get("author", "N/A"),
                        "source_url": paper.get("url", "#"),
                        "summary_preview": (paper.get("text", "") or paper.get("summary", ""))[:150] + "..."
                    })
            except json.JSONDecodeError:
                continue

    total_results = len(results)
    start = (page - 1) * size
    end = start + size
    paginated_results = results[start:end]

    return {
        "results": paginated_results,
        "paging": {
            "total": total_results,
            "page": page,
            "size": size
        }
    }
