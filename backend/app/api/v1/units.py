from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.property import Unit, UnitAmenity, UnitStatus, Property
from app.schemas.unit import UnitCreate, UnitResponse
from app.schemas.common import APIResponse
from app.api.dependencies import get_current_user, get_current_org_id, require_roles
from app.models.user import User

router = APIRouter(prefix="/units", tags=["Units"])

@router.get("/public", response_model=APIResponse[List[UnitResponse]])
def get_public_units(
    property_id: Optional[str] = None,
    bedrooms: Optional[int] = None,
    db: Session = Depends(get_db)
):
    query = db.query(Unit).join(Property).filter(
        Property.published == True,
        Unit.is_deleted == False
    )
    if property_id:
        query = query.filter(Unit.property_id == property_id)
    if bedrooms:
        query = query.filter(Unit.bedrooms >= bedrooms)

    units = query.all()
    return APIResponse(success=True, data=[UnitResponse.model_validate(u) for u in units])

@router.get("/", response_model=APIResponse[List[UnitResponse]])
def list_org_units(
    property_id: Optional[str] = None,
    org_id: str = Depends(get_current_org_id),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(["ADMIN", "LANDLORD", "PROPERTY_MANAGER"]))
):
    query = db.query(Unit).filter(Unit.organization_id == org_id, Unit.is_deleted == False)
    if property_id:
        query = query.filter(Unit.property_id == property_id)

    units = query.all()
    return APIResponse(success=True, data=[UnitResponse.model_validate(u) for u in units])

@router.post("/", response_model=APIResponse[UnitResponse])
def create_unit(
    unit_in: UnitCreate,
    org_id: str = Depends(get_current_org_id),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(["ADMIN", "LANDLORD", "PROPERTY_MANAGER"]))
):
    unit = Unit(
        organization_id=org_id,
        property_id=unit_in.property_id,
        building_id=unit_in.building_id,
        unit_number=unit_in.unit_number,
        floor=unit_in.floor,
        bedrooms=unit_in.bedrooms,
        bathrooms=unit_in.bathrooms,
        square_feet=unit_in.square_feet,
        rent_amount=unit_in.rent_amount,
        deposit_amount=unit_in.deposit_amount,
        status=UnitStatus(unit_in.status),
        is_furnished=unit_in.is_furnished,
        description=unit_in.description,
        available_date=unit_in.available_date
    )
    db.add(unit)
    db.flush()

    for item in unit_in.amenities:
        amenity = UnitAmenity(unit_id=unit.id, name=item)
        db.add(amenity)

    db.commit()
    db.refresh(unit)
    return APIResponse(success=True, message="Unit created successfully", data=UnitResponse.model_validate(unit))

@router.put("/{unit_id}/status", response_model=APIResponse[UnitResponse])
def update_unit_status(
    unit_id: str,
    status_str: str,
    org_id: str = Depends(get_current_org_id),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(["ADMIN", "LANDLORD", "PROPERTY_MANAGER"]))
):
    unit = db.query(Unit).filter(Unit.id == unit_id, Unit.organization_id == org_id).first()
    if not unit:
        raise HTTPException(status_code=404, detail="Unit not found")

    unit.status = UnitStatus(status_str)
    db.commit()
    db.refresh(unit)
    return APIResponse(success=True, message="Unit status updated", data=UnitResponse.model_validate(unit))
