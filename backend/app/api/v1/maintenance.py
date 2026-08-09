from datetime import datetime
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.maintenance import MaintenanceRequest, MaintenanceAssignment, MaintenanceComment, MaintenanceAttachment, MaintenanceStatus, MaintenancePriority
from app.models.property import Unit
from app.schemas.maintenance import MaintenanceCreate, MaintenanceResponse, MaintenanceStatusUpdate, MaintenanceAssignRequest
from app.schemas.common import APIResponse
from app.api.dependencies import get_current_user, get_current_org_id, require_roles
from app.models.user import User

router = APIRouter(prefix="/maintenance", tags=["Maintenance"])

@router.post("/", response_model=APIResponse[MaintenanceResponse])
def create_maintenance_request(
    req_in: MaintenanceCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    unit = db.query(Unit).filter(Unit.id == req_in.unit_id).first()
    if not unit:
        raise HTTPException(status_code=404, detail="Unit not found")

    m_req = MaintenanceRequest(
        organization_id=unit.organization_id,
        property_id=req_in.property_id,
        unit_id=req_in.unit_id,
        tenant_id=current_user.id,
        title=req_in.title,
        description=req_in.description,
        category=req_in.category,
        priority=MaintenancePriority(req_in.priority),
        status=MaintenanceStatus.OPEN
    )
    db.add(m_req)
    db.commit()
    db.refresh(m_req)

    return APIResponse(success=True, message="Maintenance ticket created", data=MaintenanceResponse.model_validate(m_req))

@router.get("/my-requests", response_model=APIResponse[List[MaintenanceResponse]])
def get_tenant_requests(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    reqs = db.query(MaintenanceRequest).filter(MaintenanceRequest.tenant_id == current_user.id).order_by(MaintenanceRequest.created_at.desc()).all()
    return APIResponse(success=True, data=[MaintenanceResponse.model_validate(r) for r in reqs])

@router.get("/assigned-tech", response_model=APIResponse[List[MaintenanceResponse]])
def get_tech_assigned_requests(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Endpoints for Maintenance Staff to view jobs assigned to them."""
    assignments = db.query(MaintenanceAssignment).filter(MaintenanceAssignment.staff_id == current_user.id).all()
    req_ids = [a.request_id for a in assignments]
    reqs = db.query(MaintenanceRequest).filter(MaintenanceRequest.id.in_(req_ids)).all() if req_ids else []
    return APIResponse(success=True, data=[MaintenanceResponse.model_validate(r) for r in reqs])

@router.get("/", response_model=APIResponse[List[MaintenanceResponse]])
def list_org_maintenance(
    org_id: str = Depends(get_current_org_id),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(["ADMIN", "LANDLORD", "PROPERTY_MANAGER", "MAINTENANCE_STAFF"]))
):
    reqs = db.query(MaintenanceRequest).filter(MaintenanceRequest.organization_id == org_id).order_by(MaintenanceRequest.created_at.desc()).all()
    return APIResponse(success=True, data=[MaintenanceResponse.model_validate(r) for r in reqs])

@router.post("/{request_id}/assign", response_model=APIResponse[MaintenanceResponse])
def assign_maintenance_staff(
    request_id: str,
    assign_in: MaintenanceAssignRequest,
    org_id: str = Depends(get_current_org_id),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(["ADMIN", "LANDLORD", "PROPERTY_MANAGER"]))
):
    m_req = db.query(MaintenanceRequest).filter(MaintenanceRequest.id == request_id, MaintenanceRequest.organization_id == org_id).first()
    if not m_req:
        raise HTTPException(status_code=404, detail="Maintenance ticket not found")

    assignment = MaintenanceAssignment(
        request_id=m_req.id,
        staff_id=assign_in.staff_id,
        assigned_by_id=current_user.id,
        notes=assign_in.notes
    )
    db.add(assignment)
    m_req.status = MaintenanceStatus.ASSIGNED
    db.commit()
    db.refresh(m_req)

    return APIResponse(success=True, message="Maintenance staff assigned", data=MaintenanceResponse.model_validate(m_req))

@router.put("/{request_id}/status", response_model=APIResponse[MaintenanceResponse])
def update_maintenance_status(
    request_id: str,
    update_in: MaintenanceStatusUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    m_req = db.query(MaintenanceRequest).filter(MaintenanceRequest.id == request_id).first()
    if not m_req:
        raise HTTPException(status_code=404, detail="Maintenance ticket not found")

    m_req.status = MaintenanceStatus(update_in.status)
    if update_in.estimated_cost is not None:
        m_req.estimated_cost = update_in.estimated_cost
    if update_in.actual_cost is not None:
        m_req.actual_cost = update_in.actual_cost
    if update_in.status == "COMPLETED":
        m_req.completed_at = datetime.utcnow()

    if update_in.comment:
        comment = MaintenanceComment(
            request_id=m_req.id,
            user_id=current_user.id,
            comment=update_in.comment
        )
        db.add(comment)

    db.commit()
    db.refresh(m_req)
    return APIResponse(success=True, message="Maintenance status updated", data=MaintenanceResponse.model_validate(m_req))
