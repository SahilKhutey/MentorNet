import requests
try:
    res = requests.post("http://localhost:8000/api/v1/auth/signup", json={
        "email": "test_connection@example.com",
        "password": "password123",
        "role": "student"
    }, timeout=5)
    print(f"Status: {res.status_code}")
    print(f"Body: {res.text}")
except Exception as e:
    print(f"Error: {e}")
