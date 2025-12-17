import pandas as pd
from app.models.transaction import Transaction
from sqlalchemy.exc import IntegrityError
from decimal import Decimal
import hashlib
from app.services.users import get_or_create_user_by_external_id, create_user

def generate_transaction_hash(date, description, amount) -> str:
    raw_data = f"{date}|{description.lower().strip()}|{amount}"
    return hashlib.sha256(raw_data.encode('utf-8')).hexdigest()

def import_revolut_csv(file, db, user_id: str):
    df = pd.read_csv(file)

    imported = 0
    skipped = 0

    for _, row in df.iterrows():
        try:
            date = pd.to_datetime(row["Completed Date"], errors="coerce")
            if pd.isna(date):
                raise ValueError("Invalid date")
            
            transaction_hash = generate_transaction_hash(
                date=date.date(),
                description=str(row["Description"]),
                amount=Decimal(str(row["Amount"]))
            )

            user = get_or_create_user_by_external_id(db, user_id)

            transaction = Transaction(
                date=date.date(),
                description=str(row["Description"]),
                amount=Decimal(str(row["Amount"])),
                category=None,
                hash=transaction_hash,
                user_id=user.id
            )

            db.add(transaction)
            db.commit()

            imported += 1
        except IntegrityError:
            db.rollback()
            skipped += 1

        except Exception as e:
            db.rollback()
            skipped += 1
            print(f"Skipping row due to error: {e}")

    db.commit()

    return {"imported": imported, "skipped": skipped}