import sys
import os
from decimal import Decimal
from datetime import datetime

sys.path.insert(0, os.path.dirname(__file__))

from app.core.database import SessionLocal, engine, Base
from app.core.security import get_password_hash
from app.models import (
    User, Role, Permission, Organization, OrganizationMember, OrgRole,
    Property, Building, Unit, UnitAmenity, PropertyImage, PropertyType, UnitStatus,
    RentalApplication, ApplicationStatus, Lease, LeaseStatus, Payment, PaymentType, PaymentStatus,
    MaintenanceRequest, MaintenancePriority, MaintenanceStatus, MaintenanceAssignment
)
from app.services.ledger_service import LedgerService

def seed_database():
    print("[SEED] Initializing Database Schema & Seeding Initial Data...")
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    try:
        # 1. Create Roles
        roles_data = [
            ("ADMIN", "Platform Administrator with global permissions"),
            ("LANDLORD", "Property Owner / Landlord"),
            ("PROPERTY_MANAGER", "Assigned Property Manager"),
            ("TENANT", "Resident Tenant"),
            ("MAINTENANCE_STAFF", "Maintenance Technician")
        ]
        role_objs = {}
        for r_name, r_desc in roles_data:
            role = db.query(Role).filter(Role.name == r_name).first()
            if not role:
                role = Role(name=r_name, description=r_desc)
                db.add(role)
            role_objs[r_name] = role
        db.flush()

        # 2. Create Organization
        org = db.query(Organization).filter(Organization.slug == "apex-pm").first()
        if not org:
            org = Organization(
                name="Apex Property Management",
                slug="apex-pm",
                address="100 Grand Avenue, Suite 400",
                city="San Francisco",
                state="CA",
                postal_code="94102",
                email="support@apexpm.com",
                phone="(415) 890-1234"
            )
            db.add(org)
            db.flush()
            
        LedgerService.ensure_default_chart_of_accounts(db, org.id)

        # 3. Create Seed Users
        users_seed = [
            ("admin@platform.com", "AdminPass123!", "Platform", "Admin", "ADMIN", OrgRole.OWNER),
            ("landlord@apexpm.com", "LandlordPass123!", "Robert", "Sterling", "LANDLORD", OrgRole.OWNER),
            ("manager@apexpm.com", "ManagerPass123!", "Sarah", "Jenkins", "PROPERTY_MANAGER", OrgRole.MANAGER),
            ("tenant@apexpm.com", "TenantPass123!", "Alex", "Morgan", "TENANT", OrgRole.TENANT),
            ("tech@apexpm.com", "TechPass123!", "Marcus", "Vance", "MAINTENANCE_STAFF", OrgRole.MAINTENANCE),
        ]
        user_objs = {}
        for email, pwd, fname, lname, role_name, org_role in users_seed:
            usr = db.query(User).filter(User.email == email).first()
            if not usr:
                usr = User(
                    email=email,
                    hashed_password=get_password_hash(pwd),
                    first_name=fname,
                    last_name=lname,
                    is_active=True,
                    is_verified=True,
                    current_org_id=org.id
                )
                usr.roles.append(role_objs[role_name])
                db.add(usr)
                db.flush()

                # Add Org membership
                mem = db.query(OrganizationMember).filter(
                    OrganizationMember.organization_id == org.id,
                    OrganizationMember.user_id == usr.id
                ).first()
                if not mem:
                    mem = OrganizationMember(organization_id=org.id, user_id=usr.id, role=org_role)
                    db.add(mem)

            user_objs[role_name] = usr
        db.flush()

        # 4. Create Sample Properties
        prop1 = db.query(Property).filter(Property.name == "The Grandview Luxury Apartments").first()
        if not prop1:
            prop1 = Property(
                organization_id=org.id,
                name="The Grandview Luxury Apartments",
                description="High-rise luxury residence featuring panoramic skyline views, rooftop lounge, and 24/7 concierge.",
                property_type=PropertyType.APARTMENT_COMPLEX,
                address="500 Skyline Blvd",
                city="San Francisco",
                state="CA",
                postal_code="94105",
                latitude=37.7749,
                longitude=-122.4194,
                year_built=2021,
                is_featured=True,
                published=True
            )
            db.add(prop1)
            db.flush()

            img1 = PropertyImage(
                property_id=prop1.id,
                url="https://images.unsplash.com/photo-1545324418-cc1a3fa10c00?auto=format&fit=crop&w=1000&q=80",
                caption="Main Building Exterior",
                is_primary=True
            )
            img2 = PropertyImage(
                property_id=prop1.id,
                url="https://images.unsplash.com/photo-1502672260266-1c1ef2d93688?auto=format&fit=crop&w=1000&q=80",
                caption="Modern Living Room",
                is_primary=False
            )
            db.add_all([img1, img2])

        prop2 = db.query(Property).filter(Property.name == "Bayview Urban Terraces").first()
        if not prop2:
            prop2 = Property(
                organization_id=org.id,
                name="Bayview Urban Terraces",
                description="Boutique townhouse complex near waterfront parks and tech transit hubs.",
                property_type=PropertyType.CONDO,
                address="220 Embarcadero Rd",
                city="San Francisco",
                state="CA",
                postal_code="94111",
                year_built=2019,
                is_featured=True,
                published=True
            )
            db.add(prop2)
            db.flush()

            img3 = PropertyImage(
                property_id=prop2.id,
                url="https://images.unsplash.com/photo-1512917774080-9991f1c4c750?auto=format&fit=crop&w=1000&q=80",
                caption="Exterior View",
                is_primary=True
            )
            db.add(img3)

        # 5. Create Units
        u1 = db.query(Unit).filter(Unit.property_id == prop1.id, Unit.unit_number == "14B").first()
        if not u1:
            u1 = Unit(
                organization_id=org.id,
                property_id=prop1.id,
                unit_number="14B",
                floor=14,
                bedrooms=2,
                bathrooms=Decimal('2.0'),
                square_feet=1150,
                rent_amount=Decimal('3450.00'),
                deposit_amount=Decimal('3450.00'),
                status=UnitStatus.OCCUPIED,
                is_furnished=True,
                description="Corner 2-bedroom unit with floor-to-ceiling windows and stainless steel kitchen."
            )
            db.add(u1)
            db.flush()
            
            for am in ["Central HVAC", "In-Unit Washer/Dryer", "Private Balcony", "Hardwood Floors"]:
                db.add(UnitAmenity(unit_id=u1.id, name=am))

        u2 = db.query(Unit).filter(Unit.property_id == prop1.id, Unit.unit_number == "8A").first()
        if not u2:
            u2 = Unit(
                organization_id=org.id,
                property_id=prop1.id,
                unit_number="8A",
                floor=8,
                bedrooms=1,
                bathrooms=Decimal('1.0'),
                square_feet=780,
                rent_amount=Decimal('2600.00'),
                deposit_amount=Decimal('2600.00'),
                status=UnitStatus.AVAILABLE,
                is_furnished=False,
                description="Spacious 1-bedroom suite ready for immediate move-in."
            )
            db.add(u2)
            db.flush()
            for am in ["Stainless Steel Appliances", "Quartz Countertops", "Walk-in Closet"]:
                db.add(UnitAmenity(unit_id=u2.id, name=am))

        # 6. Create Active Lease for Alex Morgan (Tenant)
        tenant_user = user_objs["TENANT"]
        lease = db.query(Lease).filter(Lease.unit_id == u1.id).first()
        if not lease:
            lease = Lease(
                organization_id=org.id,
                unit_id=u1.id,
                tenant_id=tenant_user.id,
                lease_number="LSE-2026-00891",
                status=LeaseStatus.ACTIVE,
                start_date="2026-01-01",
                end_date="2026-12-31",
                rent_amount=Decimal('3450.00'),
                deposit_amount=Decimal('3450.00'),
                payment_due_day=1,
                terms="12-month standard lease term. No smoking allowed inside premises."
            )
            db.add(lease)
            db.flush()

            # Record double-entry ledger rent payment!
            LedgerService.record_rent_payment(
                db=db,
                organization_id=org.id,
                property_id=prop1.id,
                amount=Decimal('3450.00'),
                tenant_name=tenant_user.full_name
            )

        # 7. Create Sample Maintenance Work Order
        tech_user = user_objs["MAINTENANCE_STAFF"]
        m_req = db.query(MaintenanceRequest).filter(MaintenanceRequest.unit_id == u1.id).first()
        if not m_req:
            m_req = MaintenanceRequest(
                organization_id=org.id,
                property_id=prop1.id,
                unit_id=u1.id,
                tenant_id=tenant_user.id,
                title="Kitchen Sink Minor Leak",
                description="Water slow drip coming from underneath main faucet pipe fixture.",
                category="PLUMBING",
                priority=MaintenancePriority.MEDIUM,
                status=MaintenanceStatus.ASSIGNED
            )
            db.add(m_req)
            db.flush()

            assign = MaintenanceAssignment(
                request_id=m_req.id,
                staff_id=tech_user.id,
                notes="Inspect pipe seal replacement gasket."
            )
            db.add(assign)

        db.commit()
        print("[SUCCESS] Database successfully seeded with full production test environment!")

    except Exception as e:
        db.rollback()
        print(f"[ERROR] Error seeding database: {e}")
        raise e
    finally:
        db.close()

if __name__ == "__main__":
    seed_database()
