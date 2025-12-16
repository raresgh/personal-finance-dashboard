from pydantic import BaseModel
from datetime import date

class TransactionBase(BaseModel):
    date: date
    description: str
    amount: float

class TransactionCreate(TransactionBase):
    pass

class TransactionRead(TransactionBase):
    id: int
    category: str | None

    class Config:
        orm_mode = True
