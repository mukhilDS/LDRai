from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import test_connection
from auth import router as auth_router
from couples import router as couples_router
from checkins import router as checkins_router
from ai import router as ai_router
from dashboard import router as dashboard_router


app = FastAPI()
allow_origins=[
    "http://localhost:3000",
    "http://localhost:3001",
    "https://ld-rai.vercel.app",
],

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://ldrai-frontend.vercel.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router, prefix="/auth")
app.include_router(couples_router, prefix="/couples")
app.include_router(checkins_router, prefix="/checkins")
app.include_router(ai_router, prefix="/ai")
app.include_router(dashboard_router, prefix="/dashboard")

@app.get("/")
def root():
    return {"message": "BondAI API is live"}

@app.get("/health")
def health_check():
    return {"status": "BondAI backend is running"}

@app.get("/db-test")
def db_test():
    result = test_connection()
    return {"database": "connected", "result": result[0]}