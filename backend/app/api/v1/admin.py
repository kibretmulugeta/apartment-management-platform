from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.user import User
from app.models.organization import Organization
from app.models.audit import AuditLog
from app.schemas.user import UserResponse
from app.schemas.organization import OrgResponse
from app.schemas.common import APIResponse
from app.api.dependencies import require_roles

router = APIRouter(prefix="/admin", tags=["Platform Administrator"])

@router.get("/users", response_model=APIResponse[List[UserResponse]])
def list_all_users(
    db: Session = Depends(get_db),
    admin: User = Depends(require_roles(["ADMIN"]))
):
    users = db.query(User).filter(User.is_deleted == False).all()
    return APIResponse(success=True, data=[UserResponse.model_validate(u) for u in users])

@router.get("/organizations", response_model=APIResponse[List[OrgResponse]])
def list_all_organizations(
    db: Session = Depends(get_db),
    admin: User = Depends(require_roles(["ADMIN"]))
):
    orgs = db.query(Organization).all()
    return APIResponse(success=True, data=[OrgResponse.model_validate(o) for o in orgs])

@router.get("/audit-logs", response_model=APIResponse[List[dict]])
def get_system_audit_logs(
    db: Session = Depends(get_db),
    admin: User = Depends(require_roles(["ADMIN"]))
):
    logs = db.query(AuditLog).order_by(AuditLog.created_at.desc()).limit(100).all()
    res = [{
        "id": l.id,
        "action": l.action,
        "resource_type": l.resource_type,
        "resource_id": l.resource_id,
        "ip_address": l.ip_address,
        "user_id": l.user_id,
        "created_at": l.created_at
    } for l in logs]
    return APIResponse(success=True, data=res)
