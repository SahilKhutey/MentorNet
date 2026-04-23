from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.core.dependencies import get_db, require_role
from app.models.profile import Profile
from app.models.enterprise import Organization

router = APIRouter(prefix="/enterprise", tags=["Enterprise"])

@router.get("/stats/{org_id}")
def get_organization_stats(org_id: int, db: Session = Depends(get_db)):
    """
    Returns aggregated mentorship stats for an entire institution.
    """
    total_users = db.query(Profile).filter(Profile.organization_id == org_id).count()
    mentors = db.query(Profile).filter(
        Profile.organization_id == org_id,
        Profile.profile_score > 50 # Example threshold for active mentors
    ).count()
    
    return {
        "organization_id": org_id,
        "total_active_users": total_users,
        "active_mentors": mentors,
        "matching_efficiency": "88%", # Mocked metric for enterprise demo
        "collaboration_index": "High"
    }

@router.get("/audit")
def view_audit_logs(limit: int = 100, db: Session = Depends(get_db), user = Depends(require_role("admin"))):
    """
    Admin-only access to system-wide audit logs.
    """
    from app.models.enterprise import AuditLog
    return db.query(AuditLog).order_by(AuditLog.timestamp.desc()).limit(limit).all()
