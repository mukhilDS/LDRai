# LDRai — AI Relationship Companion for Long-Distance Couples

A memory-based AI companion that helps long-distance couples stay emotionally close through personalized daily check-ins, shared feeds, and AI-generated relationship insights.

**Live API:** https://ldrai-production.up.railway.app/docs

---

## What it does

Long-distance couples don't need another chat app. LDRai gives them a lightweight emotional ritual system that remembers what matters and turns daily check-ins into personalized support.

- **Daily check-ins** — mood, stress, and miss-you scores stored per user
- **Shared feed** — see your partner's recent emotional state in real time
- **AI daily question** — personalized prompt generated from the last 7 days of check-in data
- **Weekly AI report** — insight into how your partner has been feeling, with a suggested action
- **Dashboard** — mood and stress trends with a rule-based relationship insight

---

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | FastAPI (Python) |
| Database | PostgreSQL via Supabase |
| AI | OpenAI API (gpt-4o-mini) |
| Auth | JWT + bcrypt |
| Deployment | Railway |

---

## API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| POST | /auth/signup | No | Create account |
| POST | /auth/login | No | Login, get JWT token |
| POST | /couples/create | Yes | Create a couple, get invite code |
| POST | /couples/join/{code} | Yes | Join partner's couple |
| POST | /checkins/ | Yes | Submit daily check-in |
| GET | /checkins/today | Yes | Get today's check-in |
| GET | /checkins/feed | Yes | See partner's recent check-ins |
| GET | /ai/daily-question | Yes | Get AI-personalized daily question |
| GET | /ai/weekly-report | Yes | Get AI insight about partner's week |
| GET | /dashboard/stats | Yes | Get mood/stress trends + insight |

---

## How to run locally

```bash
git clone https://github.com/mukhilDS/LDRai.git
cd LDRai/backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Create a `.env` file in `backend/`:
```
DATABASE_URL=your_supabase_connection_string
SECRET_KEY=your_secret_key
OPENAI_API_KEY=your_openai_key
```

```bash
uvicorn main:app --reload
```

Visit `http://localhost:8000/docs`

---

## Architecture
React Frontend (coming soon)
↕
FastAPI Backend (Railway)
↕
PostgreSQL Database (Supabase)
↕
OpenAI API (gpt-4o-mini)

---

Built by [Mukhil](https://linkedin.com/in/mukhil-mp) — seeking AI/backend engineering roles.
