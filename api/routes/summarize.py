from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from models.summarizer import generate_paper_summary
from utils.result_logger import save_result
from typing import Optional

router = APIRouter()

class SummarizeRequest(BaseModel):
    paper_url: Optional[str] = None
    paper_id: Optional[str] = None
    language: Optional[str] = 'en'

@router.post("/summarize")
async def summarize(request: SummarizeRequest):
    """
    Generates a paper summary using the 'paper_url' or 'paper_id' from the request body.
    Returns a JSON object like {"summary": ..., "keywords": ..., "categories": ...} on success.
    """
    if not request.paper_url and not request.paper_id:
        raise HTTPException(status_code=400, detail="Either 'paper_url' or 'paper_id' must be provided.")

    # In a real implementation, you would fetch the paper content here
    # using the provided URL or ID. For now, we'll use a placeholder.
    prompt = f"Summarize the paper at {request.paper_url or request.paper_id} in {request.language}."

    try:
        # The generate_paper_summary function expects a simple prompt.
        # We'll need to adapt this in a real implementation.
        result = generate_paper_summary(prompt)

        # We'll also need to add keyword and category extraction.
        # For now, we'll return placeholder data.
        response = {
            "summary": result["generated_summary"],
            "keywords": ["placeholder", "keywords"],
            "categories": ["placeholder", "categories"]
        }

        save_result("summarization", response)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Generation error: {e}")
