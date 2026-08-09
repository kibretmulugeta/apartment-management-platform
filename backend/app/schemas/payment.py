from typing import Optional
from pydantic import BaseModel
from decimal import Decimal
from datetime import datetime

class PaymentIntentCreate(BaseModel):
    lease_id: Optional[str] = None
    amount: Decimal
    payment_type: str = "RENT"
    description: Optional[str] = None

class PaymentResponse(BaseModel):
    id: str
    organization_id: str
    lease_id: Optional[str] = None
    payer_id: str
    payment_type: str
    amount: Decimal
    status: str
    stripe_payment_intent_id: Optional[str] = None
    receipt_url: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True

class ExpenseCreate(BaseModel):
    property_id: str
    unit_id: Optional[str] = None
    category: str
    vendor: Optional[str] = None
    amount: Decimal
    date: str
    description: Optional[str] = None

class ExpenseResponse(BaseModel):
    id: str
    organization_id: str
    property_id: str
    unit_id: Optional[str] = None
    category: str
    vendor: Optional[str] = None
    amount: Decimal
    date: str
    description: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True
