from typing import Generator, Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import decode_token
from app.models.user import User
from app.models.organization import OrganizationMember

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

def get_current_user(
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    payload = decode_token(token)
    if not payload or payload.get("type") != "access":
        raise credentials_exception
        
    user_id: str = payload.get("sub")
    if user_id is None:
        raise credentials_exception
        
    user = db.query(User).filter(User.id == user_id, User.is_deleted == False).first()
    if user is None:
        raise credentials_exception
        
    if not user.is_active:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user")
        
    return user

def get_current_org_id(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> str:
    """Enforces multi-tenant isolation by obtaining the user's active organization ID."""
    if current_user.current_org_id:
        return current_user.current_org_id
        
    # Fallback to user's first organization membership
    membership = db.query(OrganizationMember).filter(OrganizationMember.user_id == current_user.id).first()
    if membership:
        return membership.organization_id
        
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="User does not belong to any organization."
    )

def require_roles(allowed_roles: list[str]):
    def role_checker(current_user: User = Depends(get_current_user)):
        user_role_names = [role.name for role in current_user.roles]
        # Admin overrides all
        if "ADMIN" in user_role_names:
            return current_user
            
        if not any(role in allowed_roles for role in user_role_names):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"User role lacks required permissions ({', '.join(allowed_roles)})"
            )
        return current_user
    return role_checker
