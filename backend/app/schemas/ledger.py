from typing import List, Optional
from pydantic import BaseModel
from decimal import Decimal
from datetime import datetime

class LedgerEntrySchema(BaseModel):
    id: str
    account_id: str
    account_code: Optional[str] = None
    account_name: Optional[str] = None
    entry_type: str # DEBIT or CREDIT
    amount: Decimal
    memo: Optional[str] = None

    class Config:
        from_attributes = True

class TransactionResponse(BaseModel):
    id: str
    organization_id: str
    reference: str
    description: str
    posted_at: datetime
    entries: List[LedgerEntrySchema] = []

    class Config:
        from_attributes = True

class FinancialSummary(BaseModel):
    total_revenue: Decimal
    total_expenses: Decimal
    net_income: Decimal
    outstanding_rent: Decimal
    occupied_units: int
    total_units: int
    occupancy_rate: float
