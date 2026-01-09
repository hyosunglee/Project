from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import json
from typing import Optional
from api.config import FEEDBACK_PATH

router = APIRouter()

class FeedbackRequest(BaseModel):
    paper_id: str
    summary_id: str
    rating: int
    comment: Optional[str] = None

@router.post("/feedback")
async def feedback(request: FeedbackRequest):
    try:
        entry = {
            "paper_id": request.paper_id,
            "summary_id": request.summary_id,
            "rating": request.rating,
            "comment": request.comment
        }

        with open(FEEDBACK_PATH, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\\n")

        return {"message": "Feedback received successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Feedback error: {str(e)}")
