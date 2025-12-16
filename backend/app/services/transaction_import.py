import pandas as pd
from app.models.transaction import Transaction
from decimal import Decimal

def import_revolut_csv(file, db):
    df = pd.read_csv(file)

    for _, row in df.iterrows():
        try:
            date = pd.to_datetime(row["Completed Date"], errors="coerce")
            if pd.isna(date):
                raise ValueError("Invalid date")

            transaction = Transaction(
                date=date.date(),
                description=str(row["Description"]),
                amount=Decimal(str(row["Amount"])),
                category=None,
            )

            db.add(transaction)

        except Exception as e:
            print(f"Skipping row due to error: {e}")

    db.commit()
