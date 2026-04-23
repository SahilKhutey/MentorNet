import requests

BASE_URL = "http://localhost:8000/api/v1"

def test_privacy_isolation(mentor_token, student_token):
    print("\n🔐 Testing Privacy Isolation...")
    
    # Mentor trying to access other mentor's private analytics? (Hypothetical)
    # For now, let's test if a student can set availability (should fail)
    headers = {"Authorization": f"Bearer {student_token}"}
    res = requests.post(f"{BASE_URL}/schedule/availability", json=[], headers=headers)
    
    if res.status_code == 403:
        print("✅ RBAC Check: Students cannot set mentor availability.")
    else:
        print(f"❌ Privacy Breach: Student allowed to access mentor-only route! ({res.status_code})")

def test_search_latency(query):
    print(f"\n🔍 Testing Search Latency for: '{query}'")
    import time
    start = time.time()
    res = requests.get(f"{BASE_URL}/search/hybrid?q={query}")
    end = time.time()
    
    if res.status_code == 200:
        print(f"✅ Search returned {len(res.json())} results in {(end-start)*1000:.2f}ms")
    else:
        print(f"❌ Search failed: {res.text}")

def test_booking_interaction(student_token, mentor_id):
    print("\n📅 Testing Booking Interaction...")
    headers = {"Authorization": f"Bearer {student_token}"}
    
    # Assume we know a slot time
    res = requests.post(f"{BASE_URL}/schedule/book", json={
        "mentor_id": mentor_id,
        "start": "2026-05-01T10:00:00",
        "end": "2026-05-01T11:00:00"
    }, headers=headers)
    
    if res.status_code == 200:
        print("✅ Session booked successfully!")
    else:
        print(f"❌ Booking failed: {res.text}")

# Main test runner logic would go here
