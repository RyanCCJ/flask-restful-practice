import requests
import json
import jwt
import time

url = "http://0.0.0.0:5000/users"

payload = "{\"user_id\": \"123\"}"
valid_token = jwt.encode({'user_id': '123', 'timestamp':int(time.time())}, 'password', algorithm='HS256')

headers = {
    'Content-Type': 'application/json',
    'auth': valid_token
}

response = requests.request('GET', url, headers=headers, data=payload)
print(response.text)