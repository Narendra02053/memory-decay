from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional
from services.prediction_service import predict_days_until_forget
from db.connection import get_prediction_col

router = APIRouter(prefix="/api/predict", tags=["Prediction"])

class MemoryInput(BaseModel):
    topic_name: str
    category: str
    domain: str
    category_type: str
    study_time: float
    review_count: int
    confidence: int
    difficulty: str
    stress_level: int
    sleep_hours: float
    mood: str
    distraction_level: int
    recent_event: Optional[str] = "None"
    attention_level: int

@router.post("/")
def predict_api(data: MemoryInput):
    try:
        payload = data.dict()
        
        # Validate that we have all required fields
        required_fields = [
            "category", "domain", "category_type", "study_time", 
            "review_count", "confidence", "difficulty", "stress_level",
            "sleep_hours", "mood", "distraction_level", "attention_level"
        ]
        missing = [f for f in required_fields if f not in payload or payload[f] is None or payload[f] == ""]
        if missing:
            return {
                "status": "error",
                "message": f"Missing required fields: {', '.join(missing)}",
                "prediction": None
            }
        
        # Ensure numeric fields are properly typed
        for field in ["study_time", "review_count", "confidence", "stress_level", 
                     "sleep_hours", "distraction_level", "attention_level"]:
            try:
                payload[field] = float(payload[field])
            except (ValueError, TypeError):
                return {
                    "status": "error",
                    "message": f"Invalid value for {field}: must be a number",
                    "prediction": None
                }
        
        # Make prediction
        result = predict_days_until_forget(payload)
        
        # Validate prediction result
        if result is None or (isinstance(result, float) and (result < 0 or result > 1000)):
            print(f"[PREDICT API] Warning: Unusual prediction value: {result}")

        # Try to save to MongoDB, but don't fail if it's not available
        try:
            pred_col = get_prediction_col()
            if pred_col:
                pred_col.insert_one({
                    **payload,
                    "prediction": result
                })
        except Exception as db_error:
            print(f"[PREDICT API] MongoDB save failed (non-critical): {db_error}")
            # Continue without saving to DB

        return {
            "status": "success",
            "prediction": result
        }
    except ValueError as ve:
        print(f"[PREDICT API] Validation error: {ve}")
        import traceback
        traceback.print_exc()
        return {
            "status": "error",
            "message": str(ve),
            "prediction": None
        }
    except Exception as e:
        print(f"[PREDICT API] Error: {e}")
        import traceback
        traceback.print_exc()
        return {
            "status": "error",
            "message": f"Prediction failed: {str(e)}",
            "prediction": None
        }
