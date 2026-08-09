from sqlalchemy import Column, String, Text, Numeric, Integer, Boolean, ForeignKey, Enum as SQLEnum, DateTime
from sqlalchemy.orm import relationship
import enum
from app.models.base import BaseModel

class LeaseStatus(str, enum.Enum):
    DRAFT = "DRAFT"
    PENDING_SIGNATURE = "PENDING_SIGNATURE"
    ACTIVE = "ACTIVE"
    EXPIRING = "EXPIRING"
    EXPIRED = "EXPIRED"
    TERMINATED = "TERMINATED"

class Lease(BaseModel):
    __tablename__ = 'leases'

    organization_id = Column(String(36), ForeignKey('organizations.id', ondelete='CASCADE'), nullable=False, index=True)
    unit_id = Column(String(36), ForeignKey('units.id', ondelete='CASCADE'), nullable=False, index=True)
    tenant_id = Column(String(36), ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True)

    lease_number = Column(String(100), unique=True, nullable=False, index=True)
    status = Column(SQLEnum(LeaseStatus), default=LeaseStatus.DRAFT, nullable=False, index=True)
    
    start_date = Column(String(50), nullable=False)
    end_date = Column(String(50), nullable=False)
    rent_amount = Column(Numeric(10, 2), nullable=False)
    deposit_amount = Column(Numeric(10, 2), nullable=False)
    payment_due_day = Column(Integer, default=1) # 1st of every month
    
    document_url = Column(String(500), nullable=True)
    terms = Column(Text, nullable=True)

    unit = relationship('Unit', back_populates='leases')
    tenant = relationship('User')
    signatures = relationship('DigitalSignature', back_populates='lease', cascade='all, delete-orphan')
    payments = relationship('Payment', back_populates='lease')

class DigitalSignature(BaseModel):
    __tablename__ = 'digital_signatures'

    lease_id = Column(String(36), ForeignKey('leases.id', ondelete='CASCADE'), nullable=False, index=True)
    signer_id = Column(String(36), ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    signer_role = Column(String(50), nullable=False) # TENANT, LANDLORD
    signature_text = Column(String(255), nullable=False) # e.g. "John Doe"
    ip_address = Column(String(50), nullable=True)
    signed_at = Column(DateTime, nullable=False)

    lease = relationship('Lease', back_populates='signatures')
    signer = relationship('User')
