from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from models.classifier import predict_reward
from models.summarizer import generate_paper_summary
from utils.result_logger import save_result

router = APIRouter()

class PredictRequest(BaseModel):
    text: str

@router.post("/predict")
async def predict(request: PredictRequest):
    try:
        text = request.text.strip()
        if not text:
            raise HTTPException(status_code=400, detail="Missing 'text' field")

        result = predict_reward(text)

        if result.get("prediction") == 1 and result.get("confidence", 0) >= 0.8:
            try:
                generated_data = generate_paper_summary(text)
                result["generated_summary"] = generated_data.get("generated_summary")
                save_result("generated_from_predict", {
                    "prompt": text[:100],
                    "summary": result["generated_summary"][:100]
                })
            except Exception as e:
                result["generation_error"] = str(e)

        prediction_data = {
            "text": text[:100],
            "prediction": result.get("prediction"),
            "confidence": result.get("confidence")
        }
        save_result("prediction", prediction_data)

        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Inference error: {str(e)}")
