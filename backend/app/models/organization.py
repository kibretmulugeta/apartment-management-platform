from sqlalchemy import Column, String, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship
import enum
from app.models.base import BaseModel

class OrgRole(str, enum.Enum):
    OWNER = "OWNER"
    LANDLORD = "LANDLORD"
    MANAGER = "MANAGER"
    TENANT = "TENANT"
    MAINTENANCE = "MAINTENANCE"

class Organization(BaseModel):
    __tablename__ = 'organizations'

    name = Column(String(255), nullable=False)
    slug = Column(String(255), unique=True, nullable=False, index=True)
    logo_url = Column(String(500), nullable=True)
    address = Column(String(255), nullable=True)
    city = Column(String(100), nullable=True)
    state = Column(String(100), nullable=True)
    postal_code = Column(String(20), nullable=True)
    country = Column(String(100), default="USA")
    phone = Column(String(50), nullable=True)
    email = Column(String(255), nullable=True)

    members = relationship('OrganizationMember', back_populates='organization', cascade='all, delete-orphan')
    properties = relationship('Property', back_populates='organization', cascade='all, delete-orphan')

class OrganizationMember(BaseModel):
    __tablename__ = 'organization_members'

    organization_id = Column(String(36), ForeignKey('organizations.id', ondelete='CASCADE'), nullable=False, index=True)
    user_id = Column(String(36), ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True)
    role = Column(SQLEnum(OrgRole), default=OrgRole.MANAGER, nullable=False)

    organization = relationship('Organization', back_populates='members')
    user = relationship('User', back_populates='memberships')
