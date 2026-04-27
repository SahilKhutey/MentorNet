import os
from sqlalchemy import create_engine, text

engine = create_engine('sqlite:///mentornet.db')
with engine.connect() as conn:
    print('--- USERS ---')
    result = conn.execute(text('SELECT id, name, email, username FROM users LIMIT 3'))
    for row in result:
        print(row)
    
    print('\n--- PROFILES ---')
    result = conn.execute(text('SELECT id, user_id, full_name FROM profiles LIMIT 3'))
    for row in result:
        print(row)
