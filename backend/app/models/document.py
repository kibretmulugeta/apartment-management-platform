from sqlalchemy import Column, String, Text, ForeignKey, Numeric
from app.models.base import BaseModel

class Document(BaseModel):
    __tablename__ = 'documents'

    organization_id = Column(String(36), ForeignKey('organizations.id', ondelete='CASCADE'), nullable=False, index=True)
    uploader_id = Column(String(36), ForeignKey('users.id', ondelete='SET NULL'), nullable=True)
    name = Column(String(255), nullable=False)
    file_key = Column(String(500), nullable=False)
    file_size_bytes = Column(Numeric(12, 0), nullable=True)
    mime_type = Column(String(100), default="application/pdf")
    category = Column(String(100), default="GENERAL") # LEASE, TAX, INSURANCE, TENANT_ID
