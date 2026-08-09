from typing import Optional, List
from pydantic import BaseModel, EmailStr
from datetime import datetime

class RoleResponse(BaseModel):
    id: str
    name: str
    description: Optional[str] = None

    class Config:
        from_attributes = True

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    first_name: str
    last_name: str
    phone_number: Optional[str] = None
    role_name: str = "TENANT"

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int
    user: "UserResponse"

class UserResponse(BaseModel):
    id: str
    email: str
    first_name: str
    last_name: str
    phone_number: Optional[str] = None
    avatar_url: Optional[str] = None
    is_active: bool
    is_verified: bool
    current_org_id: Optional[str] = None
    roles: List[RoleResponse] = []
    created_at: datetime

    class Config:
        from_attributes = True

TokenResponse.model_rebuild()
