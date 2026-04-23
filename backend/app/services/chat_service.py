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

def get_chat_history(db: Session, user_a: int, user_b: int, limit: int = 50) -> List[Message]:
    return db.query(Message).filter(
        ((Message.sender_id == user_a) & (Message.receiver_id == user_b)) |
        ((Message.sender_id == user_b) & (Message.receiver_id == user_a))
    ).order_by(Message.timestamp.desc()).limit(limit).all()

def get_recent_chats(db: Session, user_id: int):
    # This is a simplified version; ideally use distinct/group by for real production
    return db.query(Message).filter(
        (Message.sender_id == user_id) | (Message.receiver_id == user_id)
    ).order_by(Message.timestamp.desc()).limit(20).all()
