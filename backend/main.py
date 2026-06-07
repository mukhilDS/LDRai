from fastapi import FastAPI
from database import test_connection

app = FastAPI()

@app.get("/health")
def health_check():
    return {"status": "BondAI backend is running"}

@app.get("/db-test")
def db_test():
    result = test_connection()
    return {"database": "connected", "result": result[0]}