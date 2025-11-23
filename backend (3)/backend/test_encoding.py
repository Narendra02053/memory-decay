from services.preprocess import preprocess_payload

base = {
    'topic_name': 'Test',
    'category': 'science',
    'domain': 'school',
    'category_type': 'concept',
    'study_time': 1.5,
    'review_count': 2,
    'confidence': 4,
    'difficulty': 'medium',
    'stress_level': 2,
    'sleep_hours': 7.5,
    'mood': 'calm',
    'distraction_level': 1,
    'recent_event': 'none',
    'attention_level': 4
}

print("Testing if encoding produces different values:")
print("=" * 60)

# Test domain values
print("\nDomain encoding (feature index 2):")
for domain in ['school', 'pu', 'college', 'university']:
    data = base.copy()
    data['domain'] = domain
    X = preprocess_payload(data)
    print(f"  {domain:12} -> {X[0][2]:.6f}")

# Test category_type values  
print("\nCategory type encoding (feature index 3):")
for cat_type in ['concept', 'formula', 'fact', 'procedure']:
    data = base.copy()
    data['category_type'] = cat_type
    X = preprocess_payload(data)
    print(f"  {cat_type:12} -> {X[0][3]:.6f}")

# Test difficulty values
print("\nDifficulty encoding (feature index 7):")
for diff in ['easy', 'medium', 'hard', 'very hard']:
    data = base.copy()
    data['difficulty'] = diff
    X = preprocess_payload(data)
    print(f"  {diff:12} -> {X[0][7]:.6f}")

# Test mood values
print("\nMood encoding (feature index 10):")
for mood in ['calm', 'stressed', 'focused', 'excited']:
    data = base.copy()
    data['mood'] = mood
    X = preprocess_payload(data)
    print(f"  {mood:12} -> {X[0][10]:.6f}")

print("\n" + "=" * 60)
print("If values are different, encoding is working correctly!")




