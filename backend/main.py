from fastapi import FastAPI
from database import test_connection
from auth import router as auth_router

app = FastAPI()
app.include_router(auth_router, prefix="/auth")

@app.get("/health")
def health_check():
    return {"status": "BondAI backend is running"}

@app.get("/db-test")
def db_test():
    result = test_connection()
    return {"database": "connected", "result": result[0]}