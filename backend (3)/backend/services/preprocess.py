import pickle
import numpy as np
from pathlib import Path

# -----------------------------
# Load Models Folder
# -----------------------------
MODEL_DIR = Path(__file__).resolve().parent.parent / "models"


# -----------------------------
# SAFE PICKLE LOADER
# -----------------------------
def safe_load_pickle(path):
    with open(path, "rb") as f:
        return pickle.load(f)


# -----------------------------
# LOAD SAVED OBJECTS
# -----------------------------
LABEL_ENCODERS = safe_load_pickle(MODEL_DIR / "label_encoders.pkl")
SCALER = safe_load_pickle(MODEL_DIR / "scaler.pkl")


# -----------------------------
# COLUMNS THAT WERE ENCODED
# (Match your training notebook)
# -----------------------------
CATEGORICAL_COLS = [
    "category",
    "domain",
    "category_type",
    "difficulty",
    "mood",
    "recent_event",
]

NUMERIC_COLS = [
    "study_time",
    "review_count",
    "confidence",
    "stress_level",
    "sleep_hours",
    "distraction_level",
    "attention_level",
]

# NOTE: topic_name is skipped intentionally!


# -----------------------------
# SAFE ENCODER FOR CATEGORICAL VALUES
# -----------------------------
def safe_encode(col, value):
    encoder = LABEL_ENCODERS.get(col)

    if encoder is None:
        print(f"[WARN] No encoder for: {col}. Skipping.")
        return 0  # fallback

    if value in encoder.classes_:
        return encoder.transform([value])[0]

    # If unseen → add into encoder dynamically
    encoder.classes_ = np.append(encoder.classes_, [value])
    return encoder.transform([value])[0]


# -----------------------------
# FEATURE ORDER - Must match training order exactly
# This is the order from the scaler's feature_names_in_
# -----------------------------
FEATURE_ORDER = [
    "topic_name",
    "category",
    "domain", 
    "category_type",
    "study_time",
    "review_count",
    "confidence",
    "difficulty",
    "stress_level",
    "sleep_hours",
    "mood",
    "distraction_level",
    "recent_event",
    "attention_level",
]

# -----------------------------
# Deterministic encoding for categorical values
# Ensures different inputs produce different outputs
# -----------------------------

# Known categorical values and their unique encodings
# This ensures each value gets a unique, consistent numeric representation
CATEGORICAL_VALUE_MAPPINGS = {
    "category": {
        "science": 0, "mathematics": 1, "history": 2, "literature": 3,
        "language": 4, "arts": 5, "technology": 6, "business": 7, "other": 8
    },
    "domain": {
        "school": 0, "pu": 1, "college": 2, "university": 3,
        "online": 4, "self-study": 5
    },
    "category_type": {
        "concept": 0, "formula": 1, "fact": 2, "procedure": 3,
        "principle": 4, "theory": 5, "other": 6
    },
    "difficulty": {
        "easy": 0, "medium": 1, "hard": 2, "very hard": 3
    },
    "mood": {
        "calm": 0, "stressed": 1, "excited": 2, "tired": 3,
        "focused": 4, "anxious": 5, "confident": 6, "neutral": 7
    },
    "recent_event": {
        "none": 0, "exam": 1, "test": 2, "presentation": 3,
        "assignment": 4, "deadline": 5, "holiday": 6, "illness": 7, "other": 8
    }
}

def encode_string_deterministic(value: str, col_name: str, target_mean: float = 0.0, target_std: float = 1.0) -> float:
    """Convert string to a numeric value that matches training data distribution"""
    if not value or str(value).strip() == "":
        return target_mean
    
    value = str(value).lower().strip()
    
    # First, try to use predefined mapping if available
    if col_name in CATEGORICAL_VALUE_MAPPINGS:
        if value in CATEGORICAL_VALUE_MAPPINGS[col_name]:
            mapped_val = CATEGORICAL_VALUE_MAPPINGS[col_name][value]
            # Map to target distribution range
            # Spread values across the range: mean ± 2*std
            max_mapped = max(CATEGORICAL_VALUE_MAPPINGS[col_name].values())
            if max_mapped > 0:
                normalized = (mapped_val / max_mapped) * 2 - 1  # -1 to 1
            else:
                normalized = 0
            return float(target_mean + normalized * target_std * 2.0)
    
    # For unknown values, use a robust hash function
    # This ensures different strings get different values
    hash_val = 0
    prime = 31
    for char in value:
        hash_val = (hash_val * prime + ord(char)) % (2**31)
    
    # Map to target distribution with good spread
    normalized = (hash_val % 100000) / 100000.0  # 0 to 1
    result = target_mean + (normalized - 0.5) * target_std * 4.0
    return float(result)

def encode_topic_name(topic_name: str) -> float:
    """Convert topic name to a numeric value matching training distribution"""
    # Use a robust hash to ensure different topic names get different values
    if not topic_name or str(topic_name).strip() == "":
        return 48.62  # default mean
    
    topic_str = str(topic_name).strip()
    # Create a unique hash for each topic name
    hash_val = 0
    prime = 5381  # Large prime for better distribution
    for char in topic_str:
        hash_val = (hash_val * prime + ord(char)) % (2**31)
    
    # Map to training distribution: mean ~48.62, std ~28.31
    # Use modulo to get a value in a wide range, then map to distribution
    normalized = (hash_val % 100000) / 100000.0  # 0 to 1
    result = 48.62 + (normalized - 0.5) * 28.31 * 2.0  # Spread across mean ± 2*std
    return float(result)

# -----------------------------
# MAIN PREPROCESS FUNCTION
# -----------------------------
def preprocess_payload(payload: dict):
    """
    Preprocess input payload for prediction.
    Ensures different inputs produce different encoded values.
    """
    # Process features in the exact order that matches training
    feature_values = []
    
    for col in FEATURE_ORDER:
        if col not in payload:
            print(f"[WARN] Missing feature: {col}, using default value")
            feature_values.append(0.0)
            continue
            
        val = payload[col]
        
        # Handle None or empty values
        if val is None or (isinstance(val, str) and val.strip() == ""):
            if col in NUMERIC_COLS:
                feature_values.append(0.0)
            elif col == "topic_name":
                feature_values.append(encode_topic_name(""))
            else:
                feature_values.append(0.0)
            continue
        
        # Handle topic_name specially
        if col == "topic_name":
            feature_values.append(encode_topic_name(str(val)))
        
        # Encode categorical (if encoders exist)
        elif col in CATEGORICAL_COLS:
            encoder = LABEL_ENCODERS.get(col)
            if encoder and hasattr(encoder, 'classes_') and len(encoder.classes_) > 0:
                # Use encoder if available
                val_lower = str(val).lower().strip()
                if val_lower in encoder.classes_:
                    encoded_val = encoder.transform([val_lower])[0]
                    feature_values.append(float(encoded_val))
                else:
                    # Fallback: use deterministic encoding
                    feature_stats = {
                        "category": {"mean": 9.996, "std": 6.060},
                        "domain": {"mean": 5.311, "std": 2.550},
                        "category_type": {"mean": 0.364, "std": 0.481},
                        "difficulty": {"mean": 1.5, "std": 1.0},
                        "mood": {"mean": 2.0, "std": 1.5},
                        "recent_event": {"mean": 1.0, "std": 1.0},
                    }
                    stats = feature_stats.get(col, {"mean": 0.0, "std": 1.0})
                    encoded_val = encode_string_deterministic(val, col, stats["mean"], stats["std"])
                    feature_values.append(encoded_val)
            else:
                # No encoder available - use deterministic encoding matching training distribution
                # Use scaler statistics to match expected ranges
                feature_stats = {
                    "category": {"mean": 9.996, "std": 6.060},
                    "domain": {"mean": 5.311, "std": 2.550},
                    "category_type": {"mean": 0.364, "std": 0.481},
                    "difficulty": {"mean": 1.5, "std": 1.0},
                    "mood": {"mean": 2.0, "std": 1.5},
                    "recent_event": {"mean": 1.0, "std": 1.0},
                }
                stats = feature_stats.get(col, {"mean": 0.0, "std": 1.0})
                
                # Use improved encoding function that ensures uniqueness
                encoded_val = encode_string_deterministic(str(val), col, stats["mean"], stats["std"])
                feature_values.append(encoded_val)
        
        # Numeric values
        elif col in NUMERIC_COLS:
            try:
                feature_values.append(float(val))
            except (ValueError, TypeError):
                print(f"[WARN] Invalid numeric value for {col}: {val}, using 0.0")
                feature_values.append(0.0)
        
        else:
            print(f"[WARN] Unknown column type: {col}, using 0")
            feature_values.append(0.0)
    
    # Convert to numpy array with correct shape (1, 14)
    X = np.array([feature_values], dtype=float)
    
    # Verify we have the right number of features
    if X.shape[1] != 14:
        raise ValueError(f"Expected 14 features, got {X.shape[1]}")
    
    # Scale using the scaler (this should match training preprocessing)
    try:
        X_scaled = SCALER.transform(X)
        return X_scaled
    except Exception as e:
        print(f"[PREPROCESS] Scaling error: {e}")
        raise ValueError(f"Scaling failed: {e}. Expected {SCALER.n_features_in_} features, got {X.shape[1]}")
