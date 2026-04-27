from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from app.core.dependencies import get_db, get_current_user
from app.services.resume_service import resume_service
import os
import uuid

router = APIRouter(prefix="/resumes", tags=["Resumes"])

UPLOAD_DIR = "uploads/resumes"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/upload")
async def upload_resume(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):
    user_id = str(user["sub"])
    
    # Save file
    file_ext = file.filename.split(".")[-1]
    file_name = f"{uuid.uuid4()}.{file_ext}"
    file_path = os.path.join(UPLOAD_DIR, file_name)
    
    with open(file_path, "wb") as f:
        content = await file.read()
        f.write(content)
        
    # Analyze
    analysis = resume_service.analyze_resume(db, user_id, file_path)
    return analysis

@router.get("/my")
def get_my_resumes(db: Session = Depends(get_db), user = Depends(get_current_user)):
    user_id = str(user["sub"])
    return db.query(Resume).filter(Resume.user_id == user_id).all()
