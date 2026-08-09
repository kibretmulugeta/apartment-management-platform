import uuid
from datetime import datetime
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.lease import Lease, LeaseStatus, DigitalSignature
from app.models.property import Unit, UnitStatus
from app.schemas.lease import LeaseCreate, LeaseResponse, LeaseSignRequest
from app.schemas.common import APIResponse
from app.api.dependencies import get_current_user, get_current_org_id, require_roles
from app.models.user import User

router = APIRouter(prefix="/leases", tags=["Leases"])

@router.post("/", response_model=APIResponse[LeaseResponse])
def create_lease(
    lease_in: LeaseCreate,
    org_id: str = Depends(get_current_org_id),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(["ADMIN", "LANDLORD", "PROPERTY_MANAGER"]))
):
    unit = db.query(Unit).filter(Unit.id == lease_in.unit_id, Unit.organization_id == org_id).first()
    if not unit:
        raise HTTPException(status_code=404, detail="Unit not found")

    lease_num = f"LSE-{datetime.utcnow().year}-{uuid.uuid4().hex[:6].upper()}"
    lease = Lease(
        organization_id=org_id,
        unit_id=lease_in.unit_id,
        tenant_id=lease_in.tenant_id,
        lease_number=lease_num,
        status=LeaseStatus.PENDING_SIGNATURE,
        start_date=lease_in.start_date,
        end_date=lease_in.end_date,
        rent_amount=lease_in.rent_amount,
        deposit_amount=lease_in.deposit_amount,
        payment_due_day=lease_in.payment_due_day,
        terms=lease_in.terms or "Standard Residential Lease Agreement. Rent is due on the 1st of every month."
    )
    db.add(lease)
    unit.status = UnitStatus.RESERVED
    db.commit()
    db.refresh(lease)

    return APIResponse(success=True, message="Lease generated successfully", data=LeaseResponse.model_validate(lease))

@router.get("/my-lease", response_model=APIResponse[Optional[LeaseResponse]])
def get_tenant_lease(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    lease = db.query(Lease).filter(Lease.tenant_id == current_user.id).order_by(Lease.created_at.desc()).first()
    if not lease:
        return APIResponse(success=True, data=None)
    return APIResponse(success=True, data=LeaseResponse.model_validate(lease))

@router.get("/", response_model=APIResponse[List[LeaseResponse]])
def list_org_leases(
    org_id: str = Depends(get_current_org_id),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(["ADMIN", "LANDLORD", "PROPERTY_MANAGER"]))
):
    leases = db.query(Lease).filter(Lease.organization_id == org_id).all()
    return APIResponse(success=True, data=[LeaseResponse.model_validate(l) for l in leases])

@router.post("/{lease_id}/sign", response_model=APIResponse[LeaseResponse])
def sign_lease(
    lease_id: str,
    sign_in: LeaseSignRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    lease = db.query(Lease).filter(Lease.id == lease_id).first()
    if not lease:
        raise HTTPException(status_code=404, detail="Lease document not found")

    sig = DigitalSignature(
        lease_id=lease.id,
        signer_id=current_user.id,
        signer_role="TENANT" if current_user.id == lease.tenant_id else "LANDLORD",
        signature_text=sign_in.signature_text,
        ip_address="127.0.0.1",
        signed_at=datetime.utcnow()
    )
    db.add(sig)
    
    lease.status = LeaseStatus.ACTIVE
    lease.unit.status = UnitStatus.OCCUPIED
    
    db.commit()
    db.refresh(lease)
    return APIResponse(success=True, message="Lease signed electronically", data=LeaseResponse.model_validate(lease))
