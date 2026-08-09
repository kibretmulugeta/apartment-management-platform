from sqlalchemy import Column, String, Text, Numeric, ForeignKey, Enum as SQLEnum, DateTime
from sqlalchemy.orm import relationship
import enum
from app.models.base import BaseModel

class MaintenancePriority(str, enum.Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    URGENT = "URGENT"

class MaintenanceStatus(str, enum.Enum):
    OPEN = "OPEN"
    ASSIGNED = "ASSIGNED"
    IN_PROGRESS = "IN_PROGRESS"
    WAITING_FOR_PARTS = "WAITING_FOR_PARTS"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"

class MaintenanceRequest(BaseModel):
    __tablename__ = 'maintenance_requests'

    organization_id = Column(String(36), ForeignKey('organizations.id', ondelete='CASCADE'), nullable=False, index=True)
    property_id = Column(String(36), ForeignKey('properties.id', ondelete='CASCADE'), nullable=False, index=True)
    unit_id = Column(String(36), ForeignKey('units.id', ondelete='CASCADE'), nullable=False, index=True)
    tenant_id = Column(String(36), ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True)

    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    category = Column(String(100), default="PLUMBING") # PLUMBING, ELECTRICAL, HVAC, APPLIANCE, GENERAL
    priority = Column(SQLEnum(MaintenancePriority), default=MaintenancePriority.MEDIUM, nullable=False, index=True)
    status = Column(SQLEnum(MaintenanceStatus), default=MaintenanceStatus.OPEN, nullable=False, index=True)

    estimated_cost = Column(Numeric(10, 2), nullable=True)
    actual_cost = Column(Numeric(10, 2), nullable=True)
    completed_at = Column(DateTime, nullable=True)

    property = relationship('Property')
    unit = relationship('Unit')
    tenant = relationship('User', foreign_keys=[tenant_id])
    assignments = relationship('MaintenanceAssignment', back_populates='request', cascade='all, delete-orphan')
    comments = relationship('MaintenanceComment', back_populates='request', cascade='all, delete-orphan')
    attachments = relationship('MaintenanceAttachment', back_populates='request', cascade='all, delete-orphan')

class MaintenanceAssignment(BaseModel):
    __tablename__ = 'maintenance_assignments'

    request_id = Column(String(36), ForeignKey('maintenance_requests.id', ondelete='CASCADE'), nullable=False, index=True)
    staff_id = Column(String(36), ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True)
    assigned_by_id = Column(String(36), ForeignKey('users.id', ondelete='SET NULL'), nullable=True)
    notes = Column(Text, nullable=True)

    request = relationship('MaintenanceRequest', back_populates='assignments')
    staff = relationship('User', foreign_keys=[staff_id])

class MaintenanceComment(BaseModel):
    __tablename__ = 'maintenance_comments'

    request_id = Column(String(36), ForeignKey('maintenance_requests.id', ondelete='CASCADE'), nullable=False, index=True)
    user_id = Column(String(36), ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    comment = Column(Text, nullable=False)

    request = relationship('MaintenanceRequest', back_populates='comments')
    user = relationship('User')

class MaintenanceAttachment(BaseModel):
    __tablename__ = 'maintenance_attachments'

    request_id = Column(String(36), ForeignKey('maintenance_requests.id', ondelete='CASCADE'), nullable=False, index=True)
    url = Column(String(500), nullable=False)
    file_name = Column(String(255), nullable=True)

    request = relationship('MaintenanceRequest', back_populates='attachments')
