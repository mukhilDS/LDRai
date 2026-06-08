from fastapi import FastAPI
from database import test_connection
from auth import router as auth_router
from couples import router as couples_router
from checkins import router as checkins_router

app = FastAPI()
app.include_router(auth_router, prefix="/auth")
app.include_router(couples_router, prefix="/couples")
app.include_router(checkins_router, prefix="/checkins")


@app.get("/health")
def health_check():
    return {"status": "BondAI backend is running"}

@app.get("/db-test")
def db_test():
    result = test_connection()
    return {"database": "connected", "result": result[0]}

