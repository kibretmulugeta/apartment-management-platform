from typing import Optional, List
from pydantic import BaseModel
from decimal import Decimal
from datetime import datetime

class ApplicationDocumentSchema(BaseModel):
    id: str
    name: str
    file_key: str
    doc_type: str

    class Config:
        from_attributes = True

class ApplicationCreate(BaseModel):
    unit_id: str
    desired_move_in: str
    lease_term_months: int = 12
    employer_name: Optional[str] = None
    job_title: Optional[str] = None
    monthly_income: Optional[Decimal] = None
    emergency_contact_name: Optional[str] = None
    emergency_contact_phone: Optional[str] = None
    additional_occupants: int = 0
    has_pets: Optional[str] = None
    notes: Optional[str] = None

class ApplicationResponse(BaseModel):
    id: str
    organization_id: str
    unit_id: str
    applicant_id: str
    status: str
    desired_move_in: str
    lease_term_months: int
    employer_name: Optional[str] = None
    job_title: Optional[str] = None
    monthly_income: Optional[Decimal] = None
    emergency_contact_name: Optional[str] = None
    emergency_contact_phone: Optional[str] = None
    additional_occupants: int
    has_pets: Optional[str] = None
    notes: Optional[str] = None
    documents: List[ApplicationDocumentSchema] = []
    created_at: datetime

    class Config:
        from_attributes = True
