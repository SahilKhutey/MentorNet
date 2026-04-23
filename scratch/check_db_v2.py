import sqlite3
import os

db_path = "backend/mentornet.db"
if os.path.exists(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute("SELECT COUNT(*) FROM users")
    user_count = cursor.fetchone()[0]
    print(f"Total Users: {user_count}")
    
    cursor.execute("SELECT COUNT(*) FROM profiles")
    profile_count = cursor.fetchone()[0]
    print(f"Total Profiles: {profile_count}")
    
    print("\n--- Last 5 Users ---")
    cursor.execute("SELECT id, email FROM users ORDER BY id DESC LIMIT 5")
    for row in cursor.fetchall():
        print(row)
        
    print("\n--- Last 5 Profiles ---")
    cursor.execute("SELECT id, user_id, full_name FROM profiles ORDER BY id DESC LIMIT 5")
    for row in cursor.fetchall():
        print(row)
        
    conn.close()
else:
    print(f"{db_path} not found")
