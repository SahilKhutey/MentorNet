from sqlalchemy.orm import Session
from app.models.message import Message
from typing import List

def save_message(db: Session, sender_id: int, receiver_id: int, content: str):
    msg = Message(
        sender_id=sender_id,
        receiver_id=receiver_id,
        content=content
    )
    db.add(msg)
    db.commit()
    db.refresh(msg)
    return msg

def get_chat_history(db: Session, user_a: int, user_b: int, limit: int = 50):
    # Returning high-fidelity mock data for demo if DB is empty
    history = db.query(Message).filter(
        ((Message.sender_id == user_a) & (Message.receiver_id == user_b)) |
        ((Message.sender_id == user_b) & (Message.receiver_id == user_a))
    ).order_by(Message.timestamp.asc()).limit(limit).all()
    
    if not history:
        return [
            {"id": 1, "sender_id": user_b, "text": "Hey! I saw your request for system design mentorship.", "timestamp": "2024-04-26T10:00:00Z"},
            {"id": 2, "sender_id": "me", "text": "Yes! I'm struggling with Redis partition strategies.", "timestamp": "2024-04-26T10:05:00Z"},
            {"id": 3, "sender_id": user_b, "text": "Classic challenge. Let's look at consistent hashing.", "timestamp": "2024-04-26T10:06:00Z"}
        ]
    return [{"id": m.id, "sender_id": m.sender_id, "text": m.content, "timestamp": m.timestamp.isoformat()} for m in history]

def get_recent_chats(db: Session, user_id: str):
    # Simplified mock for demo
    return [
        {
            "id": 101, 
            "name": "Rahul Sharma", 
            "lastMessage": "Let's look at consistent hashing.", 
            "time": "2m ago",
            "online": True
        },
        {
            "id": 102, 
            "name": "Sarah Jenkins", 
            "lastMessage": "The resume looks great, just tweak the summary.", 
            "time": "1h ago",
            "online": False
        },
        {
            "id": 103, 
            "name": "David Chen", 
            "lastMessage": "Sent you the meeting link for tomorrow.", 
            "time": "3h ago",
            "online": True
        }
    ]
