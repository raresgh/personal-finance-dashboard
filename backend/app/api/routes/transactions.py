from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.services.transaction_import import import_revolut_csv
from app.models.transaction import Transaction
from app.schemas.transaction import TransactionCreate, TransactionRead
from app.api.deps import get_db
from app.api.deps import get_current_user

router = APIRouter(prefix="/transactions", tags=["transactions"])

@router.post("/upload")
def upload_transactions(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    user_id: str = Depends(get_current_user)
):
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="Invalid file type. Please upload a CSV file.")
    
    try:
        result = import_revolut_csv(file.file, db, user_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred while processing the file: {str(e)}")

    return {"detail": "Transactions uploaded successfully.", "result": result}

@router.get("/", response_model=list[TransactionRead])
def get_transactions(db: Session = Depends(get_db), user = Depends(get_current_user), limit: int = 100, offset: int = 0):
    return (
        db.query(Transaction)
        .filter(Transaction.user_id == user.id)
        .order_by(Transaction.date.desc())
        .offset(offset)
        .limit(limit)
        .all()
    )