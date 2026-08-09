from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.application import RentalApplication, ApplicationStatus
from app.models.property import Unit, UnitStatus
from app.schemas.application import ApplicationCreate, ApplicationResponse
from app.schemas.common import APIResponse
from app.api.dependencies import get_current_user, get_current_org_id, require_roles
from app.models.user import User

router = APIRouter(prefix="/applications", tags=["Applications"])

@router.post("/", response_model=APIResponse[ApplicationResponse])
def submit_application(
    app_in: ApplicationCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    unit = db.query(Unit).filter(Unit.id == app_in.unit_id).first()
    if not unit:
        raise HTTPException(status_code=404, detail="Target unit not found")

    app = RentalApplication(
        organization_id=unit.organization_id,
        unit_id=unit.id,
        applicant_id=current_user.id,
        status=ApplicationStatus.SUBMITTED,
        desired_move_in=app_in.desired_move_in,
        lease_term_months=app_in.lease_term_months,
        employer_name=app_in.employer_name,
        job_title=app_in.job_title,
        monthly_income=app_in.monthly_income,
        emergency_contact_name=app_in.emergency_contact_name,
        emergency_contact_phone=app_in.emergency_contact_phone,
        additional_occupants=app_in.additional_occupants,
        has_pets=app_in.has_pets,
        notes=app_in.notes
    )
    db.add(app)
    
    unit.status = UnitStatus.APPLICATION_PENDING
    db.commit()
    db.refresh(app)

    return APIResponse(success=True, message="Application submitted successfully", data=ApplicationResponse.model_validate(app))

@router.get("/my-applications", response_model=APIResponse[List[ApplicationResponse]])
def get_my_applications(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    apps = db.query(RentalApplication).filter(RentalApplication.applicant_id == current_user.id).all()
    return APIResponse(success=True, data=[ApplicationResponse.model_validate(a) for a in apps])

@router.get("/", response_model=APIResponse[List[ApplicationResponse]])
def list_org_applications(
    org_id: str = Depends(get_current_org_id),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(["ADMIN", "LANDLORD", "PROPERTY_MANAGER"]))
):
    apps = db.query(RentalApplication).filter(RentalApplication.organization_id == org_id).all()
    return APIResponse(success=True, data=[ApplicationResponse.model_validate(a) for a in apps])

@router.put("/{application_id}/status", response_model=APIResponse[ApplicationResponse])
def update_application_status(
    application_id: str,
    new_status: str, # APPROVED, REJECTED, UNDER_REVIEW
    org_id: str = Depends(get_current_org_id),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(["ADMIN", "LANDLORD", "PROPERTY_MANAGER"]))
):
    app = db.query(RentalApplication).filter(RentalApplication.id == application_id, RentalApplication.organization_id == org_id).first()
    if not app:
        raise HTTPException(status_code=404, detail="Application not found")

    app.status = ApplicationStatus(new_status)
    if new_status == "APPROVED":
        app.unit.status = UnitStatus.RESERVED
    elif new_status == "REJECTED":
        app.unit.status = UnitStatus.AVAILABLE

    db.commit()
    db.refresh(app)
    return APIResponse(success=True, message=f"Application status set to {new_status}", data=ApplicationResponse.model_validate(app))
