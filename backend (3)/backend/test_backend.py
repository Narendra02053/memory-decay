import requests
import sys

try:
    response = requests.get("http://127.0.0.1:8000/", timeout=2)
    print("Backend is running!")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
    
    # Test prediction endpoint
    test_data = {
        "topic_name": "Test",
        "category": "science",
        "domain": "school",
        "category_type": "concept",
        "study_time": 1.5,
        "review_count": 2,
        "confidence": 4,
        "difficulty": "medium",
        "stress_level": 2,
        "sleep_hours": 7.5,
        "mood": "calm",
        "distraction_level": 1,
        "recent_event": "none",
        "attention_level": 4
    }
    
    pred_response = requests.post("http://127.0.0.1:8000/api/predict/", json=test_data, timeout=5)
    if pred_response.status_code == 200:
        print("\nPrediction endpoint working!")
        print(f"Prediction result: {pred_response.json()}")
    else:
        print(f"\nPrediction endpoint error: {pred_response.status_code}")
        print(f"Response: {pred_response.text}")
        
except requests.exceptions.ConnectionError:
    print("Backend is NOT running. Please start it first.")
    print("\nTo start the backend, run:")
    print("  python -m uvicorn app:app --host 127.0.0.1 --port 8000")
    sys.exit(1)
except Exception as e:
    print(f"Error: {e}")
    sys.exit(1)

