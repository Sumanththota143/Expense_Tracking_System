from fastapi import FastAPI
from datetime import date
import fetch_db
from pydantic import BaseModel

app = FastAPI()


class Base(BaseModel):
    expense_date: str
    amount: float
    category: str
    notes: str


@app.get("/expenses/{exp_dt}")
def fetch_records_for_date(exp_dt: date):
    data = fetch_db.fetch_by_date(exp_dt)
    return data


@app.post("/update")
def add_update(expense: Base):
    fetch_db.delete_data_by_date(expense.expense_date)
    record = fetch_db.insert_data(
        expense.expense_date,
        expense.amount,
        expense.category,
        expense.notes
    )

    return record