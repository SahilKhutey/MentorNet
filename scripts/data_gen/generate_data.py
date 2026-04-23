import csv
import random
from faker import Faker

fake = Faker()

NUM_MENTORS = 10000
NUM_STUDENTS = 10000

# -------------------- DATA POOLS --------------------

domains = [
    "Software Engineering", "Data Science", "AI/ML",
    "Product Management", "UI/UX Design",
    "Finance", "Marketing", "Cybersecurity", "HR"
]

skills_map = {
    "Software Engineering": ["React", "Node.js", "System Design", "Java", "AWS"],
    "Data Science": ["Python", "Pandas", "ML", "Statistics"],
    "AI/ML": ["Deep Learning", "NLP", "Transformers", "TensorFlow"],
    "Product Management": ["Roadmaps", "Analytics", "Agile", "UX"],
    "UI/UX Design": ["Figma", "Wireframing", "User Research"],
    "Finance": ["Stocks", "Valuation", "Excel"],
    "Marketing": ["SEO", "Content", "Ads"],
    "Cybersecurity": ["Ethical Hacking", "Network Security"],
    "HR": ["Recruitment", "Soft Skills"]
}

companies = [
    "Google", "Amazon", "Microsoft", "Flipkart",
    "Zomato", "Infosys", "TCS", "Startup"
]

education_pools = [
    "B.Tech IIT", "M.Tech IIT", "MBA IIM",
    "B.Des NID", "B.Tech NIT", "Self-Taught"
]

availability_options = ["Weekends", "Evenings", "Flexible"]

languages_list = ["English", "Hindi", "English,Hindi"]

# -------------------- HELPERS --------------------

def get_skills(domain):
    pool = skills_map[domain]
    count = random.randint(2, 4)
    skills = random.sample(pool, min(count, len(pool)))
    return "|".join(skills)

# -------------------- GENERATORS --------------------

def generate_mentor(mentor_id):
    domain = random.choice(domains)
    return {
        "id": mentor_id,
        "name": fake.name(),
        "role": "Mentor",
        "experience_years": random.randint(3, 20),
        "domain": domain,
        "skills": get_skills(domain),
        "company": random.choice(companies),
        "designation": fake.job(),
        "location": fake.city(),
        "country": "India",
        "education": random.choice(education_pools),
        "availability": random.choice(availability_options),
        "price_per_hour": random.randint(15, 120),
        "rating": round(random.uniform(4.2, 5.0), 1),
        "total_sessions": random.randint(20, 500),
        "languages": random.choice(languages_list),
        "bio": fake.sentence(),
        "linkedin": f"https://linkedin.com/in/{fake.user_name()}",
        "verified": random.random() > 0.3,
        "profile_image": f"https://i.pravatar.cc/150?img={mentor_id % 70}"
    }

def generate_student(student_id):
    domain = random.choice(domains)
    return {
        "id": student_id,
        "name": fake.name(),
        "role": "Student",
        "current_level": random.choice(["Beginner", "Intermediate", "Advanced"]),
        "target_domain": domain,
        "interests": get_skills(domain),
        "current_skills": get_skills(domain),
        "experience_years": random.randint(0, 5),
        "education": random.choice(["B.Tech", "BCA", "MBA", "Student"]),
        "location": fake.city(),
        "country": "India",
        "goals": fake.sentence(),
        "preferred_availability": random.choice(availability_options),
        "budget_per_hour": random.randint(5, 50),
        "languages": random.choice(languages_list),
        "linkedin": f"https://linkedin.com/in/{fake.user_name()}",
        "profile_image": f"https://i.pravatar.cc/150?img={(student_id + 30) % 70}"
    }

# -------------------- MAIN --------------------

if __name__ == "__main__":
    print("Generating mentors...")
    mentors = [generate_mentor(i + 1) for i in range(NUM_MENTORS)]
    
    print("Saving mentors.csv...")
    with open("mentors.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=mentors[0].keys())
        writer.writeheader()
        writer.writerows(mentors)
        
    print("Generating students...")
    students = [generate_student(i + 1) for i in range(NUM_STUDENTS)]
    
    print("Saving students.csv...")
    with open("students.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=students[0].keys())
        writer.writeheader()
        writer.writerows(students)
        
    print("Done! Generated 10k mentors and 10k students.")
