from sqlalchemy import Column, String, Text, Boolean, ForeignKey, DateTime, Enum as SQLEnum, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from app.models.base import BaseModel

class NotificationChannel(str, enum.Enum):
    IN_APP = "IN_APP"
    EMAIL = "EMAIL"
    SMS = "SMS"

class NotificationEventType(str, enum.Enum):
    RENT_DUE = "RENT_DUE"
    PAYMENT_RECEIVED = "PAYMENT_RECEIVED"
    LEASE_EXPIRING = "LEASE_EXPIRING"
    MAINTENANCE_UPDATED = "MAINTENANCE_UPDATED"
    APPLICATION_STATUS = "APPLICATION_STATUS"

class Conversation(BaseModel):
    __tablename__ = 'conversations'

    organization_id = Column(String(36), ForeignKey('organizations.id', ondelete='CASCADE'), nullable=False, index=True)
    tenant_id = Column(String(36), ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True)
    manager_id = Column(String(36), ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True)
    title = Column(String(255), nullable=True)

    messages = relationship('Message', back_populates='conversation', cascade='all, delete-orphan')
    tenant = relationship('User', foreign_keys=[tenant_id])
    manager = relationship('User', foreign_keys=[manager_id])

class Message(BaseModel):
    __tablename__ = 'messages'

    conversation_id = Column(String(36), ForeignKey('conversations.id', ondelete='CASCADE'), nullable=False, index=True)
    sender_id = Column(String(36), ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True)
    content = Column(Text, nullable=False)
    is_read = Column(Boolean, default=False, nullable=False)
    attachment_url = Column(String(500), nullable=True)

    conversation = relationship('Conversation', back_populates='messages')
    sender = relationship('User')

class Notification(BaseModel):
    __tablename__ = 'notifications'

    user_id = Column(String(36), ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True)
    organization_id = Column(String(36), ForeignKey('organizations.id', ondelete='CASCADE'), nullable=False, index=True)
    
    channel = Column(SQLEnum(NotificationChannel), default=NotificationChannel.IN_APP, nullable=False, index=True)
    event_type = Column(SQLEnum(NotificationEventType), default=NotificationEventType.RENT_DUE, nullable=False, index=True)
    
    title = Column(String(255), nullable=False)
    message = Column(Text, nullable=False)
    is_read = Column(Boolean, default=False, nullable=False)
    metadata_json = Column(JSON, nullable=True)

    user = relationship('User')
    organization = relationship('Organization')
