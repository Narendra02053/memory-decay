import pickle
from pathlib import Path

try:
    model_dir = Path(__file__).resolve().parent / "models"
    with open(model_dir / "label_encoders.pkl", "rb") as f:
        encoders = pickle.load(f)
    
    print("=" * 50)
    print("VALID VALUES FOR CATEGORICAL FIELDS")
    print("=" * 50)
    
    print(f"\nEncoders type: {type(encoders)}")
    print(f"Encoders keys: {list(encoders.keys()) if isinstance(encoders, dict) else 'Not a dict'}")
    
    categorical_fields = ["category", "domain", "category_type", "difficulty", "mood", "recent_event"]
    
    for field in categorical_fields:
        if isinstance(encoders, dict):
            encoder = encoders.get(field)
        else:
            encoder = None
            
        if encoder and hasattr(encoder, 'classes_'):
            values = list(encoder.classes_)
            print(f"\n{field.upper()}:")
            print(f"  {', '.join(values)}")
            print(f"  Total: {len(values)} values")
        elif encoder:
            print(f"\n{field.upper()}: Found but no classes_ attribute")
            print(f"  Type: {type(encoder)}")
        else:
            print(f"\n{field.upper()}: Not found in encoders")
    
    print("\n" + "=" * 50)
    
except Exception as e:
    print("ERROR:", e)
    print("TYPE:", type(e))
    import traceback
    traceback.print_exc()
