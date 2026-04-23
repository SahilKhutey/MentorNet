import requests

url = "http://localhost:8000/api/v1/recommendations/feed"
headers = {
    "Origin": "http://localhost:3000",
    "Access-Control-Request-Method": "GET",
}

# Preflight request
res_pre = requests.options(url, headers={**headers, "Access-Control-Request-Headers": "Authorization"}, timeout=5)
print(f"Preflight Status: {res_pre.status_code}")
print(f"Preflight Headers: {res_pre.headers}")

# Real request
res = requests.get(url, headers={"Origin": "http://localhost:3000"}, timeout=5)
print(f"Real Status: {res.status_code}")
print(f"Real Headers: {res.headers}")
