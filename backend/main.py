from fastapi import FastAPI

app = FastAPI()

@app.get("/health")
def health_check():
    return {"status": "BondAI backend is running"}