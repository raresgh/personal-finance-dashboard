from fastapi import FastAPI

app = FastAPI(
    title="Personal Finance Dashboard API",
    version="1.0.0",
)

@app.get("/health") 
def health_check():
    return {"status": "ok"}