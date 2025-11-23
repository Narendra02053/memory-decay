import requests

print("=" * 60)
print("Testing if different inputs produce different outputs")
print("=" * 60)

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

tests = [
    # Test topic_name
    ('Topic: Math', {'topic_name': 'Math'}),
    ('Topic: History', {'topic_name': 'History'}),
    ('Topic: Physics', {'topic_name': 'Physics'}),
    
    # Test domain
    ('Domain: school', {'domain': 'school'}),
    ('Domain: pu', {'domain': 'pu'}),
    ('Domain: college', {'domain': 'college'}),
    
    # Test category_type
    ('Type: concept', {'category_type': 'concept'}),
    ('Type: formula', {'category_type': 'formula'}),
    ('Type: fact', {'category_type': 'fact'}),
    
    # Test difficulty
    ('Difficulty: easy', {'difficulty': 'easy'}),
    ('Difficulty: medium', {'difficulty': 'medium'}),
    ('Difficulty: hard', {'difficulty': 'hard'}),
    
    # Test mood
    ('Mood: calm', {'mood': 'calm'}),
    ('Mood: stressed', {'mood': 'stressed'}),
    ('Mood: focused', {'mood': 'focused'}),
    
    # Test recent_event
    ('Event: none', {'recent_event': 'none'}),
    ('Event: exam', {'recent_event': 'exam'}),
    ('Event: test', {'recent_event': 'test'}),
    
    # Test numeric fields
    ('Study time: 1.0', {'study_time': 1.0}),
    ('Study time: 3.0', {'study_time': 3.0}),
    ('Confidence: 2', {'confidence': 2}),
    ('Confidence: 5', {'confidence': 5}),
    ('Stress: 1', {'stress_level': 1}),
    ('Stress: 5', {'stress_level': 5}),
]

results = []
print("\nRunning tests...\n")

for name, changes in tests:
    data = base.copy()
    data.update(changes)
    try:
        r = requests.post('http://127.0.0.1:8000/api/predict/', json=data, timeout=30)
        pred = r.json()['prediction']
        results.append((name, pred, changes))
        print(f"{name:25} -> {pred:6.2f} days")
    except Exception as e:
        print(f"{name:25} -> ERROR: {e}")

print("\n" + "=" * 60)
unique_predictions = len(set([r[1] for r in results]))
total_tests = len(results)
print(f"Total tests: {total_tests}")
print(f"Unique predictions: {unique_predictions}")
print(f"Percentage unique: {(unique_predictions/total_tests)*100:.1f}%")
print("=" * 60)

if unique_predictions == total_tests:
    print("SUCCESS: All different inputs produce different outputs!")
elif unique_predictions > total_tests * 0.8:
    print("GOOD: Most inputs produce different outputs")
else:
    print("WARNING: Some inputs produce same outputs")

