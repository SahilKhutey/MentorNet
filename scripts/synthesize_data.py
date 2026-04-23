import random
import requests
import json

# --- CONFIG ---
BASE_URL = "http://localhost:8000/api/v1"
NUM_USERS = 1000 # Scaling to 1000 for verification as requested

FIELDS = [
    "Computer Science", "Artificial Intelligence", "Bioinformatics", 
    "Quantum Physics", "Robotics", "Neuroscience", "Economics"
]

INSTITUTIONS = [
    "MIT", "Stanford University", "Harvard", "Oxford", 
    "ETH Zurich", "Tsinghua University", "UC Berkeley"
]

SKILLS = [
    "Python", "PyTorch", "TensorFlow", "React", "Rust", "NLP", 
    "Computer Vision", "Blockchain", "Data Science", "SQL"
]

def generate_profile():
    field = random.choice(FIELDS)
    inst = random.choice(INSTITUTIONS)
    tags = random.sample(SKILLS, k=random.randint(3, 6))
    
    return {
        "full_name": f"Expert_{random.randint(1000, 9999)}",
        "bio": f"Expert researcher in {field} specializing in {', '.join(tags)} at {inst}.",
        "location": "Global",
        "institution": inst,
        "primary_field": field,
        "tags": tags
    }

def main():
    print(f"Starting synthesis of {NUM_USERS} profiles...")
    
    for i in range(NUM_USERS):
        email = f"user_{i}@example.com"
        password = "password123"
        role = "mentor" if i % 2 == 0 else "student"
        
        # 1. Signup or Login
        signup_res = requests.post(f"{BASE_URL}/auth/signup", json={
            "email": email,
            "password": password,
            "role": role
        })
        
        token = None
        if signup_res.status_code == 200:
            token = signup_res.json()["access_token"]
            print(f"Signed up {email}")
        else:
            # Try login
            login_res = requests.post(f"{BASE_URL}/auth/login", json={
                "email": email,
                "password": password
            })
            if login_res.status_code == 200:
                token = login_res.json()["access_token"]
                print(f"Logged in {email}")
            else:
                print(f"Failed to auth {email}: {signup_res.text} / {login_res.text}")
                continue
            
        headers = {"Authorization": f"Bearer {token}"}
        
        # 2. Create Profile
        profile_data = generate_profile()
        # Check if profile already exists
        me_res = requests.get(f"{BASE_URL}/profiles/me", headers=headers)
        if me_res.status_code == 200:
            print(f"Profile already exists for {email}")
            continue

        prof_res = requests.post(f"{BASE_URL}/profiles/create", json=profile_data, headers=headers)
        
        if prof_res.status_code == 200:
            print(f"Created {role} profile for {email}")
        else:
            print(f"Failed profile for {email}: {prof_res.text}")

    print("Synthesis complete!")

if __name__ == "__main__":
    main()
