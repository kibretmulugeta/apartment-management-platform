from sqlalchemy import Column, String, Text, Numeric, ForeignKey, Enum as SQLEnum, DateTime
from sqlalchemy.orm import relationship
import enum
from app.models.base import BaseModel

class PaymentStatus(str, enum.Enum):
    PENDING = "PENDING"
    PROCESSING = "PROCESSING"
    SUCCEEDED = "SUCCEEDED"
    FAILED = "FAILED"
    REFUNDED = "REFUNDED"
    CANCELLED = "CANCELLED"

class PaymentType(str, enum.Enum):
    RENT = "RENT"
    SECURITY_DEPOSIT = "SECURITY_DEPOSIT"
    APPLICATION_FEE = "APPLICATION_FEE"
    LATE_FEE = "LATE_FEE"
    UTILITIES = "UTILITIES"
    MAINTENANCE = "MAINTENANCE"

class Payment(BaseModel):
    __tablename__ = 'payments'

    organization_id = Column(String(36), ForeignKey('organizations.id', ondelete='CASCADE'), nullable=False, index=True)
    lease_id = Column(String(36), ForeignKey('leases.id', ondelete='SET NULL'), nullable=True, index=True)
    payer_id = Column(String(36), ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True)

    payment_type = Column(SQLEnum(PaymentType), default=PaymentType.RENT, nullable=False, index=True)
    amount = Column(Numeric(10, 2), nullable=False)
    status = Column(SQLEnum(PaymentStatus), default=PaymentStatus.PENDING, nullable=False, index=True)
    
    stripe_payment_intent_id = Column(String(255), unique=True, nullable=True, index=True)
    stripe_charge_id = Column(String(255), nullable=True)
    payment_method_type = Column(String(50), default="card") # card, ach, cash
    
    description = Column(String(255), nullable=True)
    receipt_url = Column(String(500), nullable=True)

    lease = relationship('Lease', back_populates='payments')
    payer = relationship('User')

class Expense(BaseModel):
    __tablename__ = 'expenses'

    organization_id = Column(String(36), ForeignKey('organizations.id', ondelete='CASCADE'), nullable=False, index=True)
    property_id = Column(String(36), ForeignKey('properties.id', ondelete='CASCADE'), nullable=False, index=True)
    unit_id = Column(String(36), ForeignKey('units.id', ondelete='SET NULL'), nullable=True)
    
    category = Column(String(100), nullable=False) # REPAIRS, UTILITIES, MANAGEMENT, INSURANCE, TAXES
    vendor = Column(String(255), nullable=True)
    amount = Column(Numeric(10, 2), nullable=False)
    date = Column(String(50), nullable=False)
    description = Column(Text, nullable=True)
    receipt_key = Column(String(500), nullable=True)
