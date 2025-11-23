import pickle
from pathlib import Path
from .preprocess import preprocess_payload

BASE = Path(__file__).resolve().parent.parent
MODEL_FILE = BASE / "models" / "memory_model.pkl"

# Lazy load model - only load when first prediction is made
_MODEL = None

def _get_model():
    global _MODEL
    if _MODEL is None:
        print("[PREDICTION] Loading ML model...")
        with open(MODEL_FILE, "rb") as f:
            _MODEL = pickle.load(f)
        print("[PREDICTION] Model loaded successfully")
    return _MODEL

def predict_days_until_forget(data: dict) -> float:
    model = _get_model()
    X = preprocess_payload(data)
    result = model.predict(X)
    prediction_value = round(float(result[0]), 2)
    
    # Debug: Log input values to help verify different inputs produce different outputs
    print(f"[PREDICTION] Input - category: {data.get('category')}, difficulty: {data.get('difficulty')}, "
          f"study_time: {data.get('study_time')}, confidence: {data.get('confidence')}")
    print(f"[PREDICTION] Output: {prediction_value} days")
    
    return prediction_value
