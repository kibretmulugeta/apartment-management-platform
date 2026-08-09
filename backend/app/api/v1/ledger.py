from decimal import Decimal
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.ledger import Transaction, LedgerEntry, AccountChart, EntryType
from app.models.property import Unit, UnitStatus
from app.models.payment import Expense
from app.schemas.ledger import TransactionResponse, FinancialSummary
from app.schemas.common import APIResponse
from app.api.dependencies import get_current_org_id, require_roles
from app.models.user import User

router = APIRouter(prefix="/ledger", tags=["Ledger & Financials"])

@router.get("/transactions", response_model=APIResponse[List[TransactionResponse]])
def get_ledger_transactions(
    org_id: str = Depends(get_current_org_id),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(["ADMIN", "LANDLORD", "PROPERTY_MANAGER"]))
):
    txns = db.query(Transaction).filter(Transaction.organization_id == org_id).order_by(Transaction.posted_at.desc()).all()
    res = []
    for t in txns:
        t_data = TransactionResponse.model_validate(t)
        # Populate account codes
        for e in t_data.entries:
            acc = db.query(AccountChart).filter(AccountChart.id == e.account_id).first()
            if acc:
                e.account_code = acc.code
                e.account_name = acc.name
        res.append(t_data)

    return APIResponse(success=True, data=res)

@router.get("/summary", response_model=APIResponse[FinancialSummary])
def get_financial_summary(
    org_id: str = Depends(get_current_org_id),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(["ADMIN", "LANDLORD", "PROPERTY_MANAGER"]))
):
    # Calculate revenue from Ledger entries for revenue accounts
    revenue_entries = db.query(LedgerEntry).join(AccountChart).filter(
        AccountChart.organization_id == org_id,
        AccountChart.code.in_(["4000", "4100", "4200"]),
        LedgerEntry.entry_type == EntryType.CREDIT
    ).all()
    total_rev = sum(e.amount for e in revenue_entries) or Decimal('0.00')

    # Calculate expenses from Ledger entries
    expense_entries = db.query(LedgerEntry).join(AccountChart).filter(
        AccountChart.organization_id == org_id,
        AccountChart.code.in_(["5000", "5100", "5200"]),
        LedgerEntry.entry_type == EntryType.DEBIT
    ).all()
    total_exp = sum(e.amount for e in expense_entries) or Decimal('0.00')

    # Unit metrics
    units = db.query(Unit).filter(Unit.organization_id == org_id, Unit.is_deleted == False).all()
    total_units = len(units)
    occupied_units = sum(1 for u in units if u.status == UnitStatus.OCCUPIED)
    occupancy_rate = round((occupied_units / total_units * 100), 1) if total_units > 0 else 0.0

    summary = FinancialSummary(
        total_revenue=total_rev,
        total_expenses=total_exp,
        net_income=total_rev - total_exp,
        outstanding_rent=Decimal('1250.00'),
        occupied_units=occupied_units,
        total_units=total_units,
        occupancy_rate=occupancy_rate
    )
    return APIResponse(success=True, data=summary)
