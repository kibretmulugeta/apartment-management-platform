from sqlalchemy import Column, String, Text, Numeric, Integer, ForeignKey, Enum as SQLEnum, DateTime
from sqlalchemy.orm import relationship
import enum
from app.models.base import BaseModel

class ApplicationStatus(str, enum.Enum):
    DRAFT = "DRAFT"
    SUBMITTED = "SUBMITTED"
    UNDER_REVIEW = "UNDER_REVIEW"
    SCREENING = "SCREENING"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    WITHDRAWN = "WITHDRAWN"

class RentalApplication(BaseModel):
    __tablename__ = 'rental_applications'

    organization_id = Column(String(36), ForeignKey('organizations.id', ondelete='CASCADE'), nullable=False, index=True)
    unit_id = Column(String(36), ForeignKey('units.id', ondelete='CASCADE'), nullable=False, index=True)
    applicant_id = Column(String(36), ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True)

    status = Column(SQLEnum(ApplicationStatus), default=ApplicationStatus.SUBMITTED, nullable=False, index=True)
    desired_move_in = Column(String(50), nullable=False)
    lease_term_months = Column(Integer, default=12)
    
    # Financial details
    employer_name = Column(String(255), nullable=True)
    job_title = Column(String(100), nullable=True)
    monthly_income = Column(Numeric(10, 2), nullable=True)
    emergency_contact_name = Column(String(255), nullable=True)
    emergency_contact_phone = Column(String(50), nullable=True)

    additional_occupants = Column(Integer, default=0)
    has_pets = Column(String(255), nullable=True) # Description of pets or None
    notes = Column(Text, nullable=True)

    unit = relationship('Unit', back_populates='applications')
    applicant = relationship('User')
    documents = relationship('ApplicationDocument', back_populates='application', cascade='all, delete-orphan')

class ApplicationDocument(BaseModel):
    __tablename__ = 'application_documents'

    application_id = Column(String(36), ForeignKey('rental_applications.id', ondelete='CASCADE'), nullable=False, index=True)
    name = Column(String(255), nullable=False)
    file_key = Column(String(500), nullable=False)
    doc_type = Column(String(100), default="PAYSTUB") # PAYSTUB, ID_PROOF, TAX_RETURN

    application = relationship('RentalApplication', back_populates='documents')
