from typing import Optional, List
from pydantic import BaseModel
from decimal import Decimal
from datetime import datetime

class MaintenanceCommentSchema(BaseModel):
    id: str
    user_id: str
    comment: str
    created_at: datetime

    class Config:
        from_attributes = True

class MaintenanceAttachmentSchema(BaseModel):
    id: str
    url: str
    file_name: Optional[str] = None

    class Config:
        from_attributes = True

class MaintenanceCreate(BaseModel):
    property_id: str
    unit_id: str
    title: str
    description: str
    category: str = "PLUMBING"
    priority: str = "MEDIUM"

class MaintenanceStatusUpdate(BaseModel):
    status: str
    estimated_cost: Optional[Decimal] = None
    actual_cost: Optional[Decimal] = None
    comment: Optional[str] = None

class MaintenanceAssignRequest(BaseModel):
    staff_id: str
    notes: Optional[str] = None

class MaintenanceResponse(BaseModel):
    id: str
    organization_id: str
    property_id: str
    unit_id: str
    tenant_id: str
    title: str
    description: str
    category: str
    priority: str
    status: str
    estimated_cost: Optional[Decimal] = None
    actual_cost: Optional[Decimal] = None
    completed_at: Optional[datetime] = None
    comments: List[MaintenanceCommentSchema] = []
    attachments: List[MaintenanceAttachmentSchema] = []
    created_at: datetime

    class Config:
        from_attributes = True
