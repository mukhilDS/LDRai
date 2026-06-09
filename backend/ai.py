from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Checkin, CoupleMember, User
from couples import get_current_user
from openai import OpenAI
from sqlalchemy import desc
import os

router = APIRouter()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@router.get("/daily-question")
def get_daily_question(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    member = db.query(CoupleMember).filter(CoupleMember.user_id == current_user.id).first()
    if not member:
        raise HTTPException(status_code=400, detail="You are not in a couple yet")

    checkins = db.query(Checkin).filter(
        Checkin.couple_id == member.couple_id
    ).order_by(desc(Checkin.created_at)).limit(7).all()

    if not checkins:
        raise HTTPException(status_code=400, detail="No check-ins yet")

    checkin_summary = "\n".join([
        f"Date: {c.created_at.strftime('%Y-%m-%d')}, Mood: {c.mood}/5, Stress: {c.stress}/5, Miss you: {c.miss_you}/5"
        for c in checkins
    ])

    prompt = f"""You are a thoughtful relationship coach for a long-distance couple.

Here are their check-ins from the last 7 days:
{checkin_summary}

Based on these emotional patterns, generate ONE warm, specific, open-ended question that will help them connect deeper today. 

Rules:
- One question only
- Make it feel personal, not generic
- Keep it under 30 words
- Do not explain the question, just ask it"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=100,
        temperature=0.7
    )

    question = response.choices[0].message.content.strip()

    return {
        "question": question,
        "based_on_checkins": len(checkins)
    }