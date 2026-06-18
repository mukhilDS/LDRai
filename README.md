# LDRai — AI Relationship Companion for Long-Distance Couples

A memory-based AI companion that helps long-distance couples stay emotionally close through personalized daily check-ins, shared feeds, and AI-generated relationship insights.

**Live App:** https://ld-rai.vercel.app
**Live API Docs:** https://ldrai-production.up.railway.app/docs
**Demo Video:** https://www.loom.com/share/77cbe35673494d029e3d44781e435a0d

---

## What it does

Long-distance couples don't need another chat app. LDRai gives them a lightweight emotional ritual system that remembers what matters and turns daily check-ins into personalized support — not static question packs, but prompts shaped by real relationship data.

- **Authentication** — secure signup/login with JWT tokens and bcrypt password hashing
- **Partner pairing** — create or join a couple via a shareable invite code
- **Daily check-ins** — mood, stress, and miss-you scores logged per user
- **Shared feed** — see your partner's recent emotional state in real time
- **AI daily question** — personalized prompt generated from the last 7 days of check-in data
- **Weekly AI report** — a written insight into how your partner has been feeling, with a suggested action for you to take
- **Dashboard** — mood and stress trends with a rule-based relationship insight, no AI call needed for instant load

---

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | Next.js (React, TypeScript, Tailwind CSS) |
| Backend | FastAPI (Python) |
| Database | PostgreSQL via Supabase |
| AI | OpenAI API (gpt-4o-mini) |
| Auth | JWT + bcrypt |
| Frontend Deployment | Vercel |
| Backend Deployment | Railway |

---

## Architecture

```
Next.js Frontend (Vercel)
        ↕
FastAPI Backend (Railway)
        ↕
PostgreSQL Database (Supabase)
        ↕
OpenAI API (gpt-4o-mini)
```

---

## API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| POST | /auth/signup | No | Create account |
| POST | /auth/login | No | Login, get JWT token |
| POST | /couples/create | Yes | Create a couple, get invite code |
| POST | /couples/join/{code} | Yes | Join partner's couple via code |
| GET | /couples/status | Yes | Check if user has a partner yet |
| POST | /checkins/ | Yes | Submit daily check-in |
| GET | /checkins/today | Yes | Get today's check-in |
| GET | /checkins/feed | Yes | See partner's recent check-ins |
| GET | /ai/daily-question | Yes | Get AI-personalized daily question |
| GET | /ai/weekly-report | Yes | Get AI insight about partner's week |
| GET | /dashboard/stats | Yes | Get mood/stress trends + insight |

---

## How to run locally

### Backend

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

### Frontend

```bash
cd LDRai/frontend
npm install
npm run dev
```

Visit `http://localhost:3000`

---

## What's next (not built yet, intentionally)

These were scoped out of the MVP on purpose to ship faster. Kept here as a roadmap, not a promise:

- Memory timeline (relationship moments tagged and recalled by AI)
- AI-assisted appreciation letters
- Anniversary tracker
- Shared calendar and date planner
- Push notifications

---

Built by [Mukhil](https://linkedin.com/in/mukhil-mp) — seeking AI/backend engineering roles.
