from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from database import get_db
from models import Checkin, CoupleMember
from couples import get_current_user
from models import User

router = APIRouter()

class CheckinRequest(BaseModel):
    mood: int
    stress: int
    miss_you: int

@router.post("/")
def create_checkin(request: CheckinRequest, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if not 1 <= request.mood <= 5:
        raise HTTPException(status_code=400, detail="Mood must be between 1 and 5")
    if not 1 <= request.stress <= 5:
        raise HTTPException(status_code=400, detail="Stress must be between 1 and 5")
    if not 1 <= request.miss_you <= 5:
        raise HTTPException(status_code=400, detail="Miss you must be between 1 and 5")

    member = db.query(CoupleMember).filter(CoupleMember.user_id == current_user.id).first()
    if not member:
        raise HTTPException(status_code=400, detail="You are not in a couple yet")

    checkin = Checkin(
        user_id=current_user.id,
        couple_id=member.couple_id,
        mood=request.mood,
        stress=request.stress,
        miss_you=request.miss_you
    )
    db.add(checkin)
    db.commit()
    db.refresh(checkin)

    return {
        "message": "Checked in successfully",
        "checkin_id": str(checkin.id),
        "mood": checkin.mood,
        "stress": checkin.stress,
        "miss_you": checkin.miss_you
    }

@router.get("/today")
def get_today_checkin(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    from datetime import date
    today = date.today()
    checkin = db.query(Checkin).filter(
        Checkin.user_id == current_user.id,
        Checkin.created_at >= today
    ).first()

    if not checkin:
        return {"checked_in": False}

    return {
        "checked_in": True,
        "mood": checkin.mood,
        "stress": checkin.stress,
        "miss_you": checkin.miss_you
    }