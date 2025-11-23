import requests
import json

url = 'http://127.0.0.1:8001/api/chat/'
data = {'email': 'test@example.com', 'message': 'Hello'}
headers = {'Content-Type': 'application/json'}

try:
    response = requests.post(url, data=json.dumps(data), headers=headers)
    print('Status Code:', response.status_code)
    print('Response:', response.json())
except Exception as e:
    print('Error:', e)