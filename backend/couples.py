from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import User, Couple, CoupleMember
from jose import jwt, JWTError
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import random
import string
import os

router = APIRouter()
security = HTTPBearer()

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(credentials.credentials, os.getenv("SECRET_KEY"), algorithms=["HS256"])
        user_id = payload.get("sub")
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=401, detail="User not found")
        return user
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

def generate_invite_code():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

@router.post("/create")
def create_couple(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    existing = db.query(CoupleMember).filter(CoupleMember.user_id == current_user.id).first()
    if existing:
        raise HTTPException(status_code=400, detail="You are already in a couple")
    
    invite_code = generate_invite_code()
    couple = Couple(invite_code=invite_code)
    db.add(couple)
    db.commit()
    db.refresh(couple)
    
    member = CoupleMember(couple_id=couple.id, user_id=current_user.id)
    db.add(member)
    db.commit()
    
    return {"couple_id": str(couple.id), "invite_code": invite_code}

@router.post("/join/{invite_code}")
def join_couple(invite_code: str, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    existing = db.query(CoupleMember).filter(CoupleMember.user_id == current_user.id).first()
    if existing:
        raise HTTPException(status_code=400, detail="You are already in a couple")
    
    couple = db.query(Couple).filter(Couple.invite_code == invite_code).first()
    if not couple:
        raise HTTPException(status_code=404, detail="Invite code not found")
    
    members = db.query(CoupleMember).filter(CoupleMember.couple_id == couple.id).count()
    if members >= 2:
        raise HTTPException(status_code=400, detail="Couple is already full")
    
    member = CoupleMember(couple_id=couple.id, user_id=current_user.id)
    db.add(member)
    db.commit()
    
    return {"message": "Joined couple", "couple_id": str(couple.id)}