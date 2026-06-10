from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Checkin, CoupleMember, User
from couples import get_current_user
from openai import OpenAI
from sqlalchemy import desc
from datetime import datetime, timezone, timedelta
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
        f"Date: {c.created_at.strftime('%m-%d-%y')}, Mood: {c.mood}/5, Stress: {c.stress}/5, Miss you: {c.miss_you}/5"
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
        max_tokens=50,
        temperature=0.8
    )

    question = response.choices[0].message.content.strip()

    return {
        "question": question,
        "based_on_checkins": len(checkins)
    }

@router.get("/weekly-report")
def get_weekly_report(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    member = db.query(CoupleMember).filter(CoupleMember.user_id == current_user.id).first()
    if not member:
        raise HTTPException(status_code=400, detail="You are not in a couple yet")

    seven_days_ago = datetime.now(timezone.utc) - timedelta(days=7)

    partner_member = db.query(CoupleMember).filter(
    CoupleMember.couple_id == member.couple_id,
    CoupleMember.user_id != current_user.id
    ).first()

    if not partner_member:
        raise HTTPException(status_code=400, detail="Your partner hasn't joined yet")

    checkins = db.query(Checkin).filter(
        Checkin.user_id == partner_member.user_id,
        Checkin.created_at >= seven_days_ago
    ).order_by(desc(Checkin.created_at)).all()

    if not checkins:
        raise HTTPException(status_code=400, detail="No check-ins in the last 7 days")

    avg_mood = round(sum(c.mood for c in checkins) / len(checkins), 1)
    avg_stress = round(sum(c.stress for c in checkins) / len(checkins), 1)
    avg_miss_you = round(sum(c.miss_you for c in checkins) / len(checkins), 1)

    checkin_summary = "\n".join([
        f"Date: {c.created_at.strftime('%m-%d-%y')}, Mood: {c.mood}/5, Stress: {c.stress}/5, Miss you: {c.miss_you}/5"
        for c in checkins
    ])

    partner_user = db.query(User).filter(User.id == partner_member.user_id).first()
    partner_name = partner_user.name if partner_user else "your partner"

    prompt = f"""You are a relationship coach helping someone understand how their long-distance partner has been feeling.

    {partner_name}'s check-in data from the last 7 days:
    {checkin_summary}

    Averages: Mood {avg_mood}/5, Stress {avg_stress}/5, Miss You {avg_miss_you}/5

    Write a warm 3-sentence insight FOR the person reading this, about their partner:
    1. How {partner_name} has been feeling emotionally this week
    2. One pattern in {partner_name}'s data worth noticing
    3. One specific thing they could do FOR {partner_name} this week based on what they saw

    Keep it under 80 words. Speak directly to the reader, not about a couple abstractly."""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=150,
        temperature=0.7
    )

    summary = response.choices[0].message.content.strip()

    return {
        "week_summary": summary,
        "stats": {
            "avg_mood": avg_mood,
            "avg_stress": avg_stress,
            "avg_miss_you": avg_miss_you,
            "total_checkins": len(checkins)
        }
    }