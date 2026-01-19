from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from utils.feedback import log_feedback

router = APIRouter()

class FeedbackRequest(BaseModel):
    text: str
    prediction: int
    confidence: Optional[float] = None
    user_label: int
    correct: bool
    source: Optional[str] = "user"

@router.post("/feedback")
async def feedback(request: FeedbackRequest):
    try:
        log_feedback(request.dict())
        return {"message": "Feedback received successfully."}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Feedback error: {str(e)}")
