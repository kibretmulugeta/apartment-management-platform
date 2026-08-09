from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.property import Property, PropertyImage, PropertyType, TourBooking
from app.schemas.property import PropertyCreate, PropertyResponse, PropertyImageSchema
from app.schemas.common import APIResponse
from app.api.dependencies import get_current_user, get_current_org_id, require_roles
from app.models.user import User

router = APIRouter(prefix="/properties", tags=["Properties"])

@router.get("/public", response_model=APIResponse[List[PropertyResponse]])
def get_public_properties(
    city: Optional[str] = Query(None),
    min_price: Optional[float] = Query(None),
    max_price: Optional[float] = Query(None),
    bedrooms: Optional[int] = Query(None),
    property_type: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    """SEO-friendly public API for property search & discovery."""
    query = db.query(Property).filter(Property.published == True, Property.is_deleted == False)

    if city:
        query = query.filter(Property.city.ilike(f"%{city}%"))
    if property_type:
        query = query.filter(Property.property_type == property_type)

    properties = query.all()
    res = [PropertyResponse.model_validate(p) for p in properties]
    return APIResponse(success=True, data=res)

@router.get("/public/{property_id}", response_model=APIResponse[PropertyResponse])
def get_public_property_detail(property_id: str, db: Session = Depends(get_db)):
    prop = db.query(Property).filter(Property.id == property_id, Property.is_deleted == False).first()
    if not prop:
        raise HTTPException(status_code=404, detail="Property not found")
    return APIResponse(success=True, data=PropertyResponse.model_validate(prop))

@router.get("/", response_model=APIResponse[List[PropertyResponse]])
def list_org_properties(
    org_id: str = Depends(get_current_org_id),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(["ADMIN", "LANDLORD", "PROPERTY_MANAGER"]))
):
    """Multi-tenant protected endpoint for managing properties."""
    properties = db.query(Property).filter(
        Property.organization_id == org_id,
        Property.is_deleted == False
    ).all()
    return APIResponse(success=True, data=[PropertyResponse.model_validate(p) for p in properties])

@router.post("/", response_model=APIResponse[PropertyResponse])
def create_property(
    prop_in: PropertyCreate,
    org_id: str = Depends(get_current_org_id),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(["ADMIN", "LANDLORD", "PROPERTY_MANAGER"]))
):
    prop = Property(
        organization_id=org_id,
        name=prop_in.name,
        description=prop_in.description,
        property_type=PropertyType(prop_in.property_type),
        address=prop_in.address,
        city=prop_in.city,
        state=prop_in.state,
        postal_code=prop_in.postal_code,
        country=prop_in.country,
        pet_policy=prop_in.pet_policy,
        parking_type=prop_in.parking_type,
        published=True
    )
    db.add(prop)
    db.commit()
    db.refresh(prop)
    return APIResponse(success=True, message="Property created successfully", data=PropertyResponse.model_validate(prop))
