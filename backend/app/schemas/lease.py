from typing import Optional, List
from pydantic import BaseModel
from decimal import Decimal
from datetime import datetime

class DigitalSignatureSchema(BaseModel):
    id: str
    signer_id: str
    signer_role: str
    signature_text: str
    signed_at: datetime

    class Config:
        from_attributes = True

class LeaseCreate(BaseModel):
    unit_id: str
    tenant_id: str
    start_date: str
    end_date: str
    rent_amount: Decimal
    deposit_amount: Decimal
    payment_due_day: int = 1
    terms: Optional[str] = None

class LeaseSignRequest(BaseModel):
    signature_text: str

class LeaseResponse(BaseModel):
    id: str
    organization_id: str
    unit_id: str
    tenant_id: str
    lease_number: str
    status: str
    start_date: str
    end_date: str
    rent_amount: Decimal
    deposit_amount: Decimal
    payment_due_day: int
    document_url: Optional[str] = None
    terms: Optional[str] = None
    signatures: List[DigitalSignatureSchema] = []
    created_at: datetime

    class Config:
        from_attributes = True
