from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import date

from app.api.deps import get_db
from app.models.transaction import Transaction
from app.api.deps import get_current_user

router = APIRouter(prefix="/analytics", tags=["analytics"])

@router.get("/monthly-expenses")
def monthly_summary(
    year: int,
    month: int, 
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):
    if not 1 <= month <= 12:
        raise HTTPException(status_code=400, detail="Month must be between 1 and 12.")
    
    start = date(year, month, 1)
    end = date(year + (month == 12), month % 12 + 1, 1)

    total_income = (
        db.query(func.coalesce(func.sum(Transaction.amount), 0))
        .filter(
            Transaction.date >= start,
            Transaction.date < end,
            Transaction.amount > 0
        )
        .scalar()
    )

    total_expenses = (
        db.query(func.coalesce(func.sum(Transaction.amount), 0))
        .filter(Transaction.user_id == user.id)
        .filter(
            Transaction.date >= start,
            Transaction.date < end,
            Transaction.amount < 0
        )
        .scalar()
    )

    return {
        "year": year,
        "month": month,
        "income": float(total_income),
        "expenses": float(total_expenses),
        "net_savings": float(total_income + total_expenses)
    }

@router.get("/categories")
def category_breakdown(
    year: int,
    month: int,
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):
    if not 1 <= month <= 12:
        raise HTTPException(status_code=400, detail="Month must be between 1 and 12.")
    
    start = date(year, month, 1)
    end = date(year + (month == 12), month % 12 + 1, 1)

    results = (
        db.query(
            Transaction.category,
            func.coalesce(func.sum(Transaction.amount), 0).label("amount")
        )
        .filter(Transaction.user_id == user.id)
        .filter(
            Transaction.date >= start,
            Transaction.date < end,
            Transaction.amount < 0
        )
        .group_by(Transaction.category)
        .all()
    )

    breakdown = [
        {"category": category or "Other", "amount": float(amount)}
        for category, amount in results
    ]

    return {
        "year": year,
        "month": month,
        "breakdown": breakdown
    }