from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Checkin, CoupleMember, User
from couples import get_current_user

router = APIRouter()

@router.get("/stats")
def get_dashboard(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    member = db.query(CoupleMember).filter(CoupleMember.user_id == current_user.id).first()
    if not member:
        raise HTTPException(status_code=400, detail="You are not in a couple yet")

    partner_member = db.query(CoupleMember).filter(
        CoupleMember.couple_id == member.couple_id,
        CoupleMember.user_id != current_user.id
    ).first()

    my_checkins = db.query(Checkin).filter(
        Checkin.user_id == current_user.id
    ).order_by(Checkin.created_at).limit(14).all()

    partner_checkins = db.query(Checkin).filter(
        Checkin.user_id == partner_member.user_id
    ).order_by(Checkin.created_at).limit(14).all() if partner_member else []

    partner_user = db.query(User).filter(
        User.id == partner_member.user_id
    ).first() if partner_member else None

    def avg(items, key):
        values = [getattr(c, key) for c in items]
        return round(sum(values) / len(values), 1) if values else 0

    my_avg_stress = avg(my_checkins, "stress")
    partner_avg_stress = avg(partner_checkins, "stress")
    my_avg_mood = avg(my_checkins, "mood")
    partner_avg_mood = avg(partner_checkins, "mood")
    partner_name = partner_user.name if partner_user else "your partner"

    # simple rule-based insight, no extra AI call needed
    if partner_avg_stress >= 3.5:
        insight = f"{partner_name}'s stress has been high this week. A small check-in message could mean a lot."
    elif partner_avg_mood <= 2.5:
        insight = f"{partner_name} has been having a tough week emotionally. Consider planning something small together."
    elif partner_avg_mood >= 4.0:
        insight = f"{partner_name} has been in a good place this week. A great time to make a new memory together."
    else:
        insight = f"{partner_name} has been steady this week. Keep showing up consistently — it matters."

    def format_checkins(checkins):
        return [
            {
                "date": c.created_at.strftime("%Y-%m-%d"),
                "mood": c.mood,
                "stress": c.stress,
                "miss_you": c.miss_you
            }
            for c in checkins
        ]

    return {
        "summary": {
            "my_total_checkins": len(my_checkins),
            "partner_total_checkins": len(partner_checkins),
            "my_avg_mood": my_avg_mood,
            "partner_avg_mood": partner_avg_mood,
            "my_avg_stress": my_avg_stress,
            "partner_avg_stress": partner_avg_stress,
        },
        "insight": insight,
        "chart_data": {
            "my_data": format_checkins(my_checkins),
            "partner_data": format_checkins(partner_checkins)
        }
    }