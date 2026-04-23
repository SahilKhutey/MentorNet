import sqlite3
import os

db_path = "backend/mentornet.db"
if os.path.exists(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    print("--- USERS ---")
    cursor.execute("SELECT id, email, role FROM users LIMIT 5")
    for row in cursor.fetchall():
        print(row)
        
    print("--- PROFILES ---")
    cursor.execute("SELECT id, user_id, full_name FROM profiles LIMIT 5")
    for row in cursor.fetchall():
        print(row)
        
    conn.close()
else:
    print(f"{db_path} not found")
