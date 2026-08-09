from typing import Optional, List
from pydantic import BaseModel
from decimal import Decimal
from datetime import datetime

class UnitAmenitySchema(BaseModel):
    id: str
    name: str

    class Config:
        from_attributes = True

class UnitCreate(BaseModel):
    property_id: str
    building_id: Optional[str] = None
    unit_number: str
    floor: int = 1
    bedrooms: int = 1
    bathrooms: Decimal = Decimal('1.0')
    square_feet: Optional[int] = None
    rent_amount: Decimal
    deposit_amount: Decimal
    status: str = "AVAILABLE"
    is_furnished: bool = False
    description: Optional[str] = None
    available_date: Optional[str] = None
    amenities: List[str] = []

class UnitResponse(BaseModel):
    id: str
    organization_id: str
    property_id: str
    building_id: Optional[str] = None
    unit_number: str
    floor: int
    bedrooms: int
    bathrooms: Decimal
    square_feet: Optional[int] = None
    rent_amount: Decimal
    deposit_amount: Decimal
    status: str
    is_furnished: bool
    description: Optional[str] = None
    available_date: Optional[str] = None
    amenities: List[UnitAmenitySchema] = []
    created_at: datetime

    class Config:
        from_attributes = True
