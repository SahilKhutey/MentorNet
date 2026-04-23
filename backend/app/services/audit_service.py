from sqlalchemy.orm import Session
from app.models.enterprise import AuditLog
from fastapi import Request
import json

def log_action(db: Session, user_id: int, action: str, details: dict = None, request: Request = None):
    """
    Production-grade audit logger for enterprise compliance.
    """
    ip = request.client.host if request else "internal"
    
    log = AuditLog(
        user_id=user_id,
        action=action,
        details=details or {},
        ip_address=ip
    )
    
    db.add(log)
    db.commit()
    return log
