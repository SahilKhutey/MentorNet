from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.dependencies import get_db, get_current_user, require_role
from app.models.lab import Lab
from app.models.user import User

router = APIRouter(prefix="/enterprise", tags=["Enterprise"])

@router.post("/labs")
def create_lab(
    data: dict, 
    db: Session = Depends(get_db), 
    user = Depends(get_current_user) # PI must be authenticated
):
    lab = Lab(
        name=data["name"],
        pi_id=str(user["sub"]),
        institution=data["institution"],
        description=data.get("description")
    )
    db.add(lab)
    db.commit()
    db.refresh(lab)
    return lab

@router.get("/labs/my")
def get_my_labs(db: Session = Depends(get_db), user = Depends(get_current_user)):
    user_id = str(user["sub"])
    return db.query(Lab).filter(Lab.pi_id == user_id).all()

@router.post("/labs/{lab_id}/add-member")
def add_lab_member(
    lab_id: str,
    data: dict,
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):
    lab = db.query(Lab).filter(Lab.id == lab_id, Lab.pi_id == str(user["sub"])).first()
    if not lab:
        raise HTTPException(status_code=404, detail="Lab not found or unauthorized")
    
    member = db.query(User).filter(User.email == data["email"]).first()
    if not member:
        raise HTTPException(status_code=404, detail="User not found")
        
    lab.members.append(member)
    db.commit()
    return {"status": "success"}
