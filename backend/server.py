from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from datetime import date
import fetch_db
from pydantic import BaseModel


app = FastAPI()


# ============================================================
# REQUEST MODELS
# ============================================================

class ExpenseCreate(BaseModel):
    expense_date: str
    amount: float
    category: str
    notes: str


class ExpenseUpdate(BaseModel):
    expense_date: str
    amount: float
    category: str
    notes: str


# ============================================================
# FRONTEND
# ============================================================

app.mount(
    "/static",
    StaticFiles(directory="static"),
    name="static"
)


@app.get("/")
def home():
    return FileResponse("static/index.html")


# ============================================================
# GET EXPENSES FOR A DATE
# ============================================================

@app.get("/expenses/{exp_dt}")
def fetch_records_for_date(exp_dt: date):

    data = fetch_db.fetch_by_date(exp_dt)

    return data


# ============================================================
# GET ALL EXPENSES
# ============================================================

@app.get("/expenses")
def fetch_all_expenses():

    data = fetch_db.fetch_all_data()

    return data


# ============================================================
# GET ONE EXPENSE
# ============================================================

@app.get("/expense/{expense_id}")
def fetch_one_expense(expense_id: int):

    data = fetch_db.fetch_by_id(expense_id)

    if data is None:

        raise HTTPException(
            status_code=404,
            detail="Expense not found"
        )

    return data


# ============================================================
# ADD EXPENSE
# ============================================================

@app.post("/expenses")
def add_expense(
    expense: ExpenseCreate
):

    record = fetch_db.insert_data(
        expense.expense_date,
        expense.amount,
        expense.category,
        expense.notes
    )

    return record


# ============================================================
# UPDATE EXPENSE
# ============================================================

@app.put("/expenses/{expense_id}")
def update_expense(
    expense_id: int,
    expense: ExpenseUpdate
):

    record = fetch_db.update_data(
        expense_id,
        expense.expense_date,
        expense.amount,
        expense.category,
        expense.notes
    )

    if record is None:

        raise HTTPException(
            status_code=404,
            detail="Expense not found"
        )

    return record


# ============================================================
# DELETE ONE EXPENSE
# ============================================================

@app.delete("/expenses/{expense_id}")
def delete_expense(
    expense_id: int
):

    deleted = fetch_db.delete_data_by_id(
        expense_id
    )

    if not deleted:

        raise HTTPException(
            status_code=404,
            detail="Expense not found"
        )

    return {
        "message": "Expense deleted successfully",
        "id": expense_id
    }


# ============================================================
# EXPENSE SUMMARY
# ============================================================

@app.get("/summary")
def expense_summary(
    start_date: date,
    end_date: date
):

    return fetch_db.fetch_expenses_summary(
        start_date,
        end_date
    )


# ============================================================
# TOTAL EXPENSES
# ============================================================

@app.get("/summary/total")
def expense_total(
    start_date: date,
    end_date: date
):

    return fetch_db.fetch_total_expenses(
        start_date,
        end_date
    )
