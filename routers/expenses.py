from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import func
from sqlalchemy.orm import Session

from database import get_db
from models import ExpenseDB
from schemas import Expense, ExpenseResponse, ExpensetotalResponse

router = APIRouter(
    prefix="/expense",
    tags=["Expenses"]
)

@router.post("/", status_code=201, response_model=ExpenseResponse)
def create_expense(expense: Expense, db: Session = Depends(get_db)):
    expense_db = ExpenseDB(
        purpose=expense.purpose,
        amount=expense.amount,
        category=expense.category,
        date=expense.date,
        status=expense.status
    )

    db.add(expense_db)
    db.commit()
    db.refresh(expense_db)
    return expense_db

@router.get("/", status_code=200, response_model=list[ExpenseResponse])
def get_expenses(db: Session = Depends(get_db)):
    expenses = db.query(ExpenseDB).all()
    return expenses

@router.get("/{expense_id}", status_code=200, response_model=ExpenseResponse)
def get_single_expense(expense_id: int, db: Session = Depends(get_db)):
    expense = db.query(ExpenseDB).filter(ExpenseDB.id == expense_id).first()
    if expense is None:
        raise HTTPException(
            status_code=404,
            detail="Expense not found"
        )
    return expense

@router.put("/{expense_id}", status_code=200, response_model=ExpenseResponse)
def update_expense(expense_id: int, expense: Expense, db: Session = Depends(get_db)):
    expense_db = db.query(ExpenseDB).filter(ExpenseDB.id == expense_id).first()
    if expense_db is None:
        raise HTTPException(
            status_code=404,
            detail="Expense not found"
        )
    expense_db.purpose = expense.purpose
    expense_db.amount = expense.amount
    expense_db.category = expense.category
    expense_db.date = expense.date
    expense_db.status = expense.status

    db.commit()
    db.refresh(expense_db)
    return expense_db

@router.delete("/{expense_id}", status_code=204)
def delete_expense(expense_id: int, db: Session = Depends(get_db)):
    expense_db = db.query(ExpenseDB).filter(ExpenseDB.id == expense_id).first()
    if expense_db is None:
        raise HTTPException(
            status_code=404,
            detail="Expense not found"
        )
    
    db.delete(expense_db)
    db.commit()


@router.get("/total", status_code=200, response_model=ExpensetotalResponse)
def get_total_expenses(db: Session = Depends(get_db)):
    total_expenses = db.query(func.sum(ExpenseDB.amount)).scalar()
    return {"total_expenses": total_expenses}
