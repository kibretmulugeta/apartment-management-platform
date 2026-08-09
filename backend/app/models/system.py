from sqlalchemy import Column, String, Text, ForeignKey, Boolean
from app.models.base import BaseModel

class Subscription(BaseModel):
    __tablename__ = 'subscriptions'

    organization_id = Column(String(36), ForeignKey('organizations.id', ondelete='CASCADE'), nullable=False, index=True)
    plan_name = Column(String(100), default="ENTERPRISE")
    status = Column(String(50), default="ACTIVE")
    stripe_customer_id = Column(String(255), nullable=True)
    stripe_subscription_id = Column(String(255), nullable=True)

class SystemSetting(BaseModel):
    __tablename__ = 'system_settings'

    key = Column(String(100), unique=True, nullable=False)
    value = Column(Text, nullable=False)
    description = Column(String(255), nullable=True)
