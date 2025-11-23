import requests

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
    ('school domain', {'domain': 'school'}),
    ('pu domain', {'domain': 'pu'}),
    ('college domain', {'domain': 'college'}),
    ('concept type', {'category_type': 'concept'}),
    ('formula type', {'category_type': 'formula'}),
    ('easy difficulty', {'difficulty': 'easy'}),
    ('hard difficulty', {'difficulty': 'hard'}),
    ('calm mood', {'mood': 'calm'}),
    ('stressed mood', {'mood': 'stressed'}),
    ('none event', {'recent_event': 'none'}),
    ('exam event', {'recent_event': 'exam'}),
]

print('Testing all categorical features...')
results = []

for name, changes in tests:
    data = base.copy()
    data.update(changes)
    try:
        r = requests.post('http://127.0.0.1:8000/api/predict/', json=data, timeout=30)
        pred = r.json()['prediction']
        results.append((name, pred))
        print(f'{name}: {pred}')
    except Exception as e:
        print(f'{name}: ERROR - {e}')

unique = len(set([r[1] for r in results]))
print(f'\nUnique predictions: {unique} out of {len(results)}')
print(f'All features affecting predictions: {unique > 1}')




