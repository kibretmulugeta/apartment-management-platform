from sqlalchemy import Column, String, Boolean, ForeignKey, DateTime, Table
from sqlalchemy.orm import relationship
from app.models.base import BaseModel
from app.core.database import Base

user_roles_table = Table(
    'user_roles',
    Base.metadata,
    Column('user_id', String(36), ForeignKey('users.id', ondelete='CASCADE'), primary_key=True),
    Column('role_id', String(36), ForeignKey('roles.id', ondelete='CASCADE'), primary_key=True)
)

role_permissions_table = Table(
    'role_permissions',
    Base.metadata,
    Column('role_id', String(36), ForeignKey('roles.id', ondelete='CASCADE'), primary_key=True),
    Column('permission_id', String(36), ForeignKey('permissions.id', ondelete='CASCADE'), primary_key=True)
)

class Role(BaseModel):
    __tablename__ = 'roles'

    name = Column(String(50), unique=True, nullable=False, index=True) # ADMIN, LANDLORD, PROPERTY_MANAGER, TENANT, MAINTENANCE_STAFF
    description = Column(String(255), nullable=True)

    permissions = relationship('Permission', secondary=role_permissions_table, back_populates='roles')

class Permission(BaseModel):
    __tablename__ = 'permissions'

    name = Column(String(100), unique=True, nullable=False, index=True) # e.g. property:create, lease:approve
    description = Column(String(255), nullable=True)

    roles = relationship('Role', secondary=role_permissions_table, back_populates='permissions')

class User(BaseModel):
    __tablename__ = 'users'

    email = Column(String(255), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    phone_number = Column(String(50), nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    is_verified = Column(Boolean, default=False, nullable=False)
    avatar_url = Column(String(500), nullable=True)
    
    # Active selected organization ID for multi-tenant context
    current_org_id = Column(String(36), ForeignKey('organizations.id', ondelete='SET NULL'), nullable=True)

    roles = relationship('Role', secondary=user_roles_table)
    memberships = relationship('OrganizationMember', back_populates='user', cascade='all, delete-orphan')

    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"
