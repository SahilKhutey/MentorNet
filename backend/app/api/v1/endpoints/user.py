from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.dependencies import get_db, get_current_user
from app.services.user_service import delete_user_data, get_user_data_export

router = APIRouter(prefix="/user", tags=["User Privacy"])

@router.get("/me/export")
def export_my_data(db: Session = Depends(get_db), user_id: str = Depends(get_current_user)):
    """GDPR: Export all my personal data."""
    data = get_user_data_export(db, user_id)
    if not data:
        raise HTTPException(status_code=404, detail="User data not found")
    return data

@router.delete("/me/purge")
def purge_my_account(db: Session = Depends(get_db), user_id: str = Depends(get_current_user)):
    """GDPR: Permanently delete my account and all associated data."""
    success = delete_user_data(db, user_id)
    if not success:
        raise HTTPException(status_code=400, detail="Failed to purge account data")
    return {"message": "Account and all associated data have been permanently deleted."}
