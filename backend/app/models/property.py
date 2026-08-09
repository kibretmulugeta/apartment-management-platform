from sqlalchemy import Column, String, Text, Numeric, Integer, Boolean, ForeignKey, Enum as SQLEnum, Float
from sqlalchemy.orm import relationship
import enum
from app.models.base import BaseModel

class PropertyType(str, enum.Enum):
    APARTMENT_COMPLEX = "APARTMENT_COMPLEX"
    MULTI_FAMILY = "MULTI_FAMILY"
    SINGLE_FAMILY = "SINGLE_FAMILY"
    CONDO = "CONDO"
    COMMERCIAL = "COMMERCIAL"

class UnitStatus(str, enum.Enum):
    AVAILABLE = "AVAILABLE"
    RESERVED = "RESERVED"
    APPLICATION_PENDING = "APPLICATION_PENDING"
    OCCUPIED = "OCCUPIED"
    MAINTENANCE = "MAINTENANCE"
    UNAVAILABLE = "UNAVAILABLE"

class Property(BaseModel):
    __tablename__ = 'properties'

    organization_id = Column(String(36), ForeignKey('organizations.id', ondelete='CASCADE'), nullable=False, index=True)
    name = Column(String(255), nullable=False, index=True)
    description = Column(Text, nullable=True)
    property_type = Column(SQLEnum(PropertyType), default=PropertyType.APARTMENT_COMPLEX, nullable=False)
    
    # Location
    address = Column(String(255), nullable=False)
    city = Column(String(100), nullable=False, index=True)
    state = Column(String(100), nullable=False)
    postal_code = Column(String(20), nullable=False)
    country = Column(String(100), default="USA")
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)

    # Features
    year_built = Column(Integer, nullable=True)
    total_floors = Column(Integer, default=1)
    pet_policy = Column(String(100), default="Pets Allowed")
    parking_type = Column(String(100), default="Garage / Assigned")
    is_featured = Column(Boolean, default=False, index=True)
    published = Column(Boolean, default=True, index=True)

    organization = relationship('Organization', back_populates='properties')
    buildings = relationship('Building', back_populates='property', cascade='all, delete-orphan')
    units = relationship('Unit', back_populates='property', cascade='all, delete-orphan')
    images = relationship('PropertyImage', back_populates='property', cascade='all, delete-orphan')
    documents = relationship('PropertyDocument', back_populates='property', cascade='all, delete-orphan')

class Building(BaseModel):
    __tablename__ = 'buildings'

    property_id = Column(String(36), ForeignKey('properties.id', ondelete='CASCADE'), nullable=False, index=True)
    name = Column(String(255), nullable=False) # e.g. Building A, East Wing
    floors = Column(Integer, default=1)
    notes = Column(Text, nullable=True)

    property = relationship('Property', back_populates='buildings')
    units = relationship('Unit', back_populates='building', cascade='all, delete-orphan')

class Unit(BaseModel):
    __tablename__ = 'units'

    organization_id = Column(String(36), ForeignKey('organizations.id', ondelete='CASCADE'), nullable=False, index=True)
    property_id = Column(String(36), ForeignKey('properties.id', ondelete='CASCADE'), nullable=False, index=True)
    building_id = Column(String(36), ForeignKey('buildings.id', ondelete='SET NULL'), nullable=True, index=True)

    unit_number = Column(String(50), nullable=False, index=True)
    floor = Column(Integer, default=1)
    bedrooms = Column(Integer, nullable=False, default=1)
    bathrooms = Column(Numeric(3, 1), nullable=False, default=1.0)
    square_feet = Column(Integer, nullable=True)
    rent_amount = Column(Numeric(10, 2), nullable=False)
    deposit_amount = Column(Numeric(10, 2), nullable=False)
    status = Column(SQLEnum(UnitStatus), default=UnitStatus.AVAILABLE, nullable=False, index=True)
    is_furnished = Column(Boolean, default=False)
    description = Column(Text, nullable=True)
    available_date = Column(String(50), nullable=True)

    property = relationship('Property', back_populates='units')
    building = relationship('Building', back_populates='units')
    amenities = relationship('UnitAmenity', back_populates='unit', cascade='all, delete-orphan')
    leases = relationship('Lease', back_populates='unit')
    applications = relationship('RentalApplication', back_populates='unit')

class UnitAmenity(BaseModel):
    __tablename__ = 'unit_amenities'

    unit_id = Column(String(36), ForeignKey('units.id', ondelete='CASCADE'), nullable=False, index=True)
    name = Column(String(100), nullable=False) # e.g., Air Conditioning, Balcony, In-unit Laundry

    unit = relationship('Unit', back_populates='amenities')

class PropertyImage(BaseModel):
    __tablename__ = 'property_images'

    property_id = Column(String(36), ForeignKey('properties.id', ondelete='CASCADE'), nullable=False, index=True)
    url = Column(String(500), nullable=False)
    caption = Column(String(255), nullable=True)
    is_primary = Column(Boolean, default=False)
    display_order = Column(Integer, default=0)

    property = relationship('Property', back_populates='images')

class PropertyDocument(BaseModel):
    __tablename__ = 'property_documents'

    property_id = Column(String(36), ForeignKey('properties.id', ondelete='CASCADE'), nullable=False, index=True)
    name = Column(String(255), nullable=False)
    file_key = Column(String(500), nullable=False)
    document_type = Column(String(100), default="GENERAL")

    property = relationship('Property', back_populates='documents')

class TourBooking(BaseModel):
    __tablename__ = 'tour_bookings'

    property_id = Column(String(36), ForeignKey('properties.id', ondelete='CASCADE'), nullable=False, index=True)
    unit_id = Column(String(36), ForeignKey('units.id', ondelete='SET NULL'), nullable=True)
    applicant_name = Column(String(255), nullable=False)
    applicant_email = Column(String(255), nullable=False)
    applicant_phone = Column(String(50), nullable=False)
    preferred_date = Column(String(50), nullable=False)
    preferred_time = Column(String(50), nullable=False)
    status = Column(String(50), default="PENDING") # PENDING, CONFIRMED, CANCELLED

class Favorite(BaseModel):
    __tablename__ = 'favorites'

    user_id = Column(String(36), ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True)
    property_id = Column(String(36), ForeignKey('properties.id', ondelete='CASCADE'), nullable=False, index=True)
