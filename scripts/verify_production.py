import requests
import time
import json

BASE_URL = "http://localhost:8000/api/v1"
HEALTH_URL = "http://localhost:8000/health"

def verify_system():
    print("--- MentorNet Production Verification ---")
    
    # 1. Health Check
    try:
        res = requests.get(HEALTH_URL, timeout=5)
        if res.status_code == 200:
            print(f"OK: API Health: {res.json()}")
        else:
            print(f"FAIL: API Health Failed: {res.status_code}")
    except Exception as e:
        print(f"ERROR: API Connection Error: {e}")
        return

    # 2. Semantic Search
    queries = ["Deep Learning expert", "React frontend developer", "Blockchain researcher"]
    for q in queries:
        start = time.time()
        res = requests.get(f"{BASE_URL}/search/semantic", params={"q": q, "limit": 5})
        end = time.time()
        if res.status_code == 200:
            results = res.json()
            print(f"OK: Semantic Search ('{q}'): {len(results)} results in {(end-start)*1000:.2f}ms")
            if len(results) > 0:
                print(f"   Top Match: {results[0]['name']} ({results[0]['field']})")
        else:
            print(f"FAIL: Semantic Search Failed for '{q}': {res.text}")

    # 3. Auth & Profile
    print("\nTesting User Authentication...")
    test_email = "user_0@example.com"
    test_pass = "password123"
    
    auth_res = requests.post(f"{BASE_URL}/auth/login", json={
        "email": test_email,
        "password": test_pass
    })
    
    if auth_res.status_code == 200:
        token = auth_res.json()["access_token"]
        print(f"OK: Login Successful for {test_email}")
        headers = {"Authorization": f"Bearer {token}"}
        
        me_res = requests.get(f"{BASE_URL}/profiles/me", headers=headers)
        if me_res.status_code == 200:
            profile = me_res.json()
            print(f"OK: Profile Retrieval: Found {profile['full_name']}")
        else:
            print(f"FAIL: Profile Retrieval Failed: {me_res.text}")
    else:
        print(f"FAIL: Login Failed for {test_email}: {auth_res.text}")

    print("\n--- Verification Complete ---")

if __name__ == "__main__":
    verify_system()
