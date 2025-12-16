from fastapi import FastAPI
from app.db.base import Base
from app.db.session import engine
from contextlib import asynccontextmanager

from app.api.routes import transactions

@asynccontextmanager
async def lifespan(app: FastAPI):
    # --- Startup Logic (formerly @app.on_event("startup")) ---
    print("Application starting up: Creating database tables...")
    Base.metadata.create_all(bind=engine)
    yield
    # --- Shutdown Logic (formerly @app.on_event("shutdown")) ---
    print("Application shut down complete.")

app = FastAPI(
    title="Personal Finance Dashboard API",
    version="1.0.0",
    lifespan=lifespan  # <-- Use 'lifespan' here
)

app.include_router(transactions.router)

@app.get("/health") 
def health_check():
    return {"status": "ok"}