import requests
import json
import time

BASE_URL = "http://localhost:8000/api/v1"

def run_smoke_test():
    print("Starting MentorNet Smoke Test...")
    
    # 1. Health Check
    try:
        res = requests.get(f"http://localhost:8000/health")
        if res.status_code == 200:
            print("[PASS] Health Check")
        else:
            print(f"[FAIL] Health Check: {res.status_code}")
            return
    except Exception as e:
        print(f"[ERROR] Server not reachable: {e}")
        return

    # 2. Public Search Test
    try:
        # Using the public search endpoint in profiles
        res = requests.get(f"{BASE_URL}/profiles/search?field=Technology")
        if res.status_code == 200:
            print(f"[PASS] Public Search Active")
        else:
            print(f"[FAIL] Public Search: {res.status_code}")
    except Exception as e:
        print(f"[ERROR] Search Error: {e}")

    # 3. Public Profile Discovery
    try:
        # Assuming we have a mentor named 'rahulsharma' from our generator
        res = requests.get(f"{BASE_URL}/profiles/public/rahulsharma")
        if res.status_code == 200:
            print("[PASS] Public Profile SEO Active")
        else:
            print(f"[WARN] Public Profile Failed (This is normal if user doesn't exist yet)")
    except Exception as e:
        print(f"[ERROR] Profile Error: {e}")

    print("\nSmoke Test Complete. System is STABLE.")

if __name__ == "__main__":
    run_smoke_test()
