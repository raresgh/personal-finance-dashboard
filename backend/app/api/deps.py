from app.db.session import SessionLocal
from fastapi import Header, HTTPException, Depends
from app.services.users import get_or_create_user_by_external_id
from sqlalchemy.orm import Session

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_user_id(x_user_id: str | None = Header(default=None)) -> str:
    if not x_user_id:
        raise HTTPException(status_code=400, detail="X-User-ID header missing")
    return x_user_id

def get_current_user(db: Session = Depends(get_db), external_id: str = Depends(get_user_id)):
    
    user = get_or_create_user_by_external_id(db, external_id)
    return user