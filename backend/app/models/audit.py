from sqlalchemy import Column, String, Text, ForeignKey, JSON
from app.models.base import BaseModel

class AuditLog(BaseModel):
    __tablename__ = 'audit_logs'

    organization_id = Column(String(36), ForeignKey('organizations.id', ondelete='SET NULL'), nullable=True, index=True)
    user_id = Column(String(36), ForeignKey('users.id', ondelete='SET NULL'), nullable=True, index=True)
    action = Column(String(100), nullable=False, index=True) # e.g., LEASE_SIGNED, PAYMENT_CREATED
    resource_type = Column(String(100), nullable=False)
    resource_id = Column(String(100), nullable=True)
    ip_address = Column(String(50), nullable=True)
    user_agent = Column(String(255), nullable=True)
    details = Column(JSON, nullable=True)
