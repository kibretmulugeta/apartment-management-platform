from typing import Optional, List
from pydantic import BaseModel
from decimal import Decimal
from datetime import datetime

class PropertyImageSchema(BaseModel):
    id: str
    url: str
    caption: Optional[str] = None
    is_primary: bool

    class Config:
        from_attributes = True

class PropertyCreate(BaseModel):
    name: str
    description: Optional[str] = None
    property_type: str = "APARTMENT_COMPLEX"
    address: str
    city: str
    state: str
    postal_code: str
    country: str = "USA"
    pet_policy: Optional[str] = "Pets Allowed"
    parking_type: Optional[str] = "Assigned Garage"

class PropertyResponse(BaseModel):
    id: str
    organization_id: str
    name: str
    description: Optional[str] = None
    property_type: str
    address: str
    city: str
    state: str
    postal_code: str
    country: str
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    year_built: Optional[int] = None
    pet_policy: Optional[str] = None
    parking_type: Optional[str] = None
    is_featured: bool
    published: bool
    images: List[PropertyImageSchema] = []
    created_at: datetime

    class Config:
        from_attributes = True

class BuildingCreate(BaseModel):
    property_id: str
    name: str
    floors: int = 1
    notes: Optional[str] = None

class BuildingResponse(BaseModel):
    id: str
    property_id: str
    name: str
    floors: int
    notes: Optional[str] = None

    class Config:
        from_attributes = True
