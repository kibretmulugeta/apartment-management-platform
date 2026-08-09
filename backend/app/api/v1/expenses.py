from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.payment import Expense
from app.schemas.payment import ExpenseCreate, ExpenseResponse
from app.schemas.common import APIResponse
from app.api.dependencies import get_current_org_id, require_roles
from app.services.ledger_service import LedgerService
from app.models.user import User

router = APIRouter(prefix="/expenses", tags=["Expenses"])

@router.get("/", response_model=APIResponse[List[ExpenseResponse]])
def list_org_expenses(
    org_id: str = Depends(get_current_org_id),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(["ADMIN", "LANDLORD", "PROPERTY_MANAGER"]))
):
    expenses = db.query(Expense).filter(Expense.organization_id == org_id).order_by(Expense.created_at.desc()).all()
    return APIResponse(success=True, data=[ExpenseResponse.model_validate(e) for e in expenses])

@router.post("/", response_model=APIResponse[ExpenseResponse])
def create_expense(
    exp_in: ExpenseCreate,
    org_id: str = Depends(get_current_org_id),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(["ADMIN", "LANDLORD", "PROPERTY_MANAGER"]))
):
    expense = Expense(
        organization_id=org_id,
        property_id=exp_in.property_id,
        unit_id=exp_in.unit_id,
        category=exp_in.category,
        vendor=exp_in.vendor,
        amount=exp_in.amount,
        date=exp_in.date,
        description=exp_in.description
    )
    db.add(expense)

    # Post to double-entry ledger!
    LedgerService.record_maintenance_expense(
        db=db,
        organization_id=org_id,
        property_id=exp_in.property_id,
        amount=exp_in.amount,
        vendor=exp_in.vendor or "Service Vendor",
        description=exp_in.description or exp_in.category
    )

    db.commit()
    db.refresh(expense)

    return APIResponse(success=True, message="Expense recorded and posted to ledger", data=ExpenseResponse.model_validate(expense))
