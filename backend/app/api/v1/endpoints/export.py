from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session
from app.core.dependencies import get_db, get_current_user
from app.services.report_service import report_service
from fastapi.responses import StreamingResponse
import io

router = APIRouter(prefix="/export", tags=["Export"])

@router.get("/report")
def download_academic_report(
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):
    """
    Generates and returns a PDF academic report for the current user.
    """
    user_id = str(user["sub"])
    try:
        pdf_buffer = report_service.generate_academic_report_pdf(db, user_id)
        
        return StreamingResponse(
            pdf_buffer,
            media_type="application/pdf",
            headers={"Content-Disposition": f"attachment; filename=MentorNet_Report_{user_id}.pdf"}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate report: {str(e)}")

@router.get("/data")
def export_raw_data(
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):
    """
    Returns the user's data in raw JSON format (GDPR Compliance).
    """
    from app.services.export_service import export_service
    user_id = str(user["sub"])
    return export_service.generate_user_data_export(db, user_id)
