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
    Base.metadata.drop_all(bind=engine)
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
            ("landlord2@apexpm.com", "LandlordPass123!", "Victoria", "Sterling", "LANDLORD", OrgRole.OWNER),
            ("manager@apexpm.com", "ManagerPass123!", "Sarah", "Jenkins", "PROPERTY_MANAGER", OrgRole.MANAGER),
            ("tenant@apexpm.com", "TenantPass123!", "Alex", "Morgan", "TENANT", OrgRole.TENANT),
            ("tenant2@apexpm.com", "TenantPass123!", "Elena", "Rostova", "TENANT", OrgRole.TENANT),
            ("tenant3@apexpm.com", "TenantPass123!", "David", "Kim", "TENANT", OrgRole.TENANT),
            ("tenant4@apexpm.com", "TenantPass123!", "Jordan", "Rivera", "TENANT", OrgRole.TENANT),
            ("tenant5@apexpm.com", "TenantPass123!", "Samantha", "Wright", "TENANT", OrgRole.TENANT),
            ("tech@apexpm.com", "TechPass123!", "Marcus", "Vance", "MAINTENANCE_STAFF", OrgRole.MAINTENANCE),
            ("tech2@apexpm.com", "TechPass123!", "Carlos", "Rodriguez", "MAINTENANCE_STAFF", OrgRole.MAINTENANCE),
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

            user_objs[email] = usr
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

        prop3 = db.query(Property).filter(Property.name == "Sunset Palms Villa & Suites").first()
        if not prop3:
            prop3 = Property(
                organization_id=org.id,
                name="Sunset Palms Villa & Suites",
                description="Resort-style luxury community featuring private cabanas, heated infinity pool, and lush tropical landscaping.",
                property_type=PropertyType.APARTMENT_COMPLEX,
                address="1200 Ocean Drive",
                city="Miami",
                state="FL",
                postal_code="33139",
                latitude=25.7781,
                longitude=-80.1313,
                year_built=2022,
                is_featured=True,
                published=True
            )
            db.add(prop3)
            db.flush()
            db.add(PropertyImage(
                property_id=prop3.id,
                url="https://images.unsplash.com/photo-1613977257363-707ba9348227?auto=format&fit=crop&w=1000&q=80",
                caption="Palm Villa Pool & Grounds",
                is_primary=True
            ))

        prop4 = db.query(Property).filter(Property.name == "Oakwood Heights Townhomes").first()
        if not prop4:
            prop4 = Property(
                organization_id=org.id,
                name="Oakwood Heights Townhomes",
                description="Modern eco-friendly townhomes with private attached garages and EV charging stations.",
                property_type=PropertyType.SINGLE_FAMILY,
                address="450 Oakwood Blvd",
                city="Austin",
                state="TX",
                postal_code="78701",
                year_built=2023,
                is_featured=True,
                published=True
            )
            db.add(prop4)
            db.flush()
            db.add(PropertyImage(
                property_id=prop4.id,
                url="https://images.unsplash.com/photo-1600585154340-be6161a56a0c?auto=format&fit=crop&w=1000&q=80",
                caption="Townhome Front Porch & Driveway",
                is_primary=True
            ))

        # 5. Create Units across properties
        units_to_create = [
            (prop1, "14B", 14, 2, Decimal('2.0'), 1150, Decimal('3450.00'), Decimal('3450.00'), UnitStatus.OCCUPIED, True, "Corner 2-bedroom unit with floor-to-ceiling windows."),
            (prop1, "8A", 8, 1, Decimal('1.0'), 780, Decimal('2600.00'), Decimal('2600.00'), UnitStatus.AVAILABLE, False, "Spacious 1-bedroom suite ready for move-in."),
            (prop1, "21A", 21, 3, Decimal('3.0'), 1850, Decimal('5900.00'), Decimal('5900.00'), UnitStatus.OCCUPIED, True, "Luxury Penthouse suite with wrap-around deck."),
            
            (prop2, "3B", 3, 2, Decimal('1.5'), 980, Decimal('3100.00'), Decimal('3100.00'), UnitStatus.AVAILABLE, False, "Waterfront view townhouse condo."),
            
            (prop3, "101", 1, 2, Decimal('2.0'), 1200, Decimal('3200.00'), Decimal('3200.00'), UnitStatus.OCCUPIED, True, "Tropical pool-view 2-bedroom villa unit."),
            (prop3, "102", 1, 3, Decimal('2.5'), 1500, Decimal('4500.00'), Decimal('4500.00'), UnitStatus.AVAILABLE, True, "Ground floor 3-bedroom suite with patio."),
            
            (prop4, "5A", 1, 3, Decimal('2.5'), 1650, Decimal('2950.00'), Decimal('2950.00'), UnitStatus.OCCUPIED, False, "Three-story eco townhome with private yard."),
            (prop4, "5B", 1, 2, Decimal('2.0'), 1300, Decimal('2450.00'), Decimal('2450.00'), UnitStatus.MAINTENANCE, False, "Townhome undergoing routine refresh."),
        ]

        unit_objs = {}
        for p, u_num, flr, bed, bath, sqft, rent, dep, stat, furn, desc in units_to_create:
            u = db.query(Unit).filter(Unit.property_id == p.id, Unit.unit_number == u_num).first()
            if not u:
                u = Unit(
                    organization_id=org.id,
                    property_id=p.id,
                    unit_number=u_num,
                    floor=flr,
                    bedrooms=bed,
                    bathrooms=bath,
                    square_feet=sqft,
                    rent_amount=rent,
                    deposit_amount=dep,
                    status=stat,
                    is_furnished=furn,
                    description=desc
                )
                db.add(u)
                db.flush()
                for am in ["Central HVAC", "In-Unit Washer/Dryer", "Stainless Appliances", "Balcony"]:
                    db.add(UnitAmenity(unit_id=u.id, name=am))
            unit_objs[f"{p.name}_{u_num}"] = u

        # 6. Create Active Leases & Ledger Records for Tenants
        u14b = unit_objs["The Grandview Luxury Apartments_14B"]
        u21a = unit_objs["The Grandview Luxury Apartments_21A"]
        u101 = unit_objs["Sunset Palms Villa & Suites_101"]
        u5a = unit_objs["Oakwood Heights Townhomes_5A"]

        leases_seed = [
            (u14b, user_objs["tenant@apexpm.com"], "LSE-2026-00891", Decimal('3450.00'), prop1.id),
            (u21a, user_objs["tenant2@apexpm.com"], "LSE-2026-00902", Decimal('5900.00'), prop1.id),
            (u101, user_objs["tenant3@apexpm.com"], "LSE-2026-00915", Decimal('3200.00'), prop3.id),
            (u5a, user_objs["tenant4@apexpm.com"], "LSE-2026-00928", Decimal('2950.00'), prop4.id),
        ]

        for u, t_user, l_num, rent_val, p_id in leases_seed:
            lease = db.query(Lease).filter(Lease.unit_id == u.id).first()
            if not lease:
                lease = Lease(
                    organization_id=org.id,
                    unit_id=u.id,
                    tenant_id=t_user.id,
                    lease_number=l_num,
                    status=LeaseStatus.ACTIVE,
                    start_date="2026-01-01",
                    end_date="2026-12-31",
                    rent_amount=rent_val,
                    deposit_amount=rent_val,
                    payment_due_day=1,
                    terms="12-month standard lease term. Professional cleaning required upon move out."
                )
                db.add(lease)
                db.flush()

                # Record Double-Entry Ledger Transactions
                LedgerService.record_rent_payment(
                    db=db,
                    organization_id=org.id,
                    property_id=p_id,
                    amount=rent_val,
                    tenant_name=t_user.full_name
                )

        # Record Operational Expenses in Ledger for realistic Financial Reports
        LedgerService.record_maintenance_expense(
            db=db,
            organization_id=org.id,
            property_id=prop1.id,
            amount=Decimal('850.00'),
            vendor="Bay Area Plumbing Solutions",
            description="Emergency Main Pipe Valve Gasket Replacement"
        )
        LedgerService.record_maintenance_expense(
            db=db,
            organization_id=org.id,
            property_id=prop3.id,
            amount=Decimal('1200.00'),
            vendor="Miami Ocean Pool & Palms Service",
            description="Monthly Infinity Pool Maintenance & Tropical Grounds Trim"
        )
        LedgerService.record_maintenance_expense(
            db=db,
            organization_id=org.id,
            property_id=prop4.id,
            amount=Decimal('450.00'),
            vendor="Austin Energy Utility Grid",
            description="Common Area Lighting & EV Charging Stations Power"
        )

        # 7. Create Maintenance Work Orders
        tech1 = user_objs["tech@apexpm.com"]
        tech2 = user_objs["tech2@apexpm.com"]

        m_tickets = [
            (prop1.id, u14b.id, user_objs["tenant@apexpm.com"].id, "Kitchen Sink Minor Leak", "Water slow drip coming from underneath main faucet pipe fixture.", "PLUMBING", MaintenancePriority.MEDIUM, MaintenanceStatus.ASSIGNED, tech1.id),
            (prop3.id, u101.id, user_objs["tenant3@apexpm.com"].id, "HVAC Cooling Fan Noise", "Air conditioning unit emitting slight humming noise during evening cycles.", "HVAC", MaintenancePriority.HIGH, MaintenanceStatus.IN_PROGRESS, tech2.id),
            (prop4.id, u5a.id, user_objs["tenant4@apexpm.com"].id, "Patio Sensor Light Check", "Exterior motion light needs new bulb replacement.", "ELECTRICAL", MaintenancePriority.LOW, MaintenanceStatus.COMPLETED, tech1.id),
        ]

        for p_id, un_id, tn_id, title, desc, cat, prio, stat, staff_id in m_tickets:
            m_req = db.query(MaintenanceRequest).filter(MaintenanceRequest.unit_id == un_id, MaintenanceRequest.title == title).first()
            if not m_req:
                m_req = MaintenanceRequest(
                    organization_id=org.id,
                    property_id=p_id,
                    unit_id=un_id,
                    tenant_id=tn_id,
                    title=title,
                    description=desc,
                    category=cat,
                    priority=prio,
                    status=stat
                )
                db.add(m_req)
                db.flush()

                assign = MaintenanceAssignment(
                    request_id=m_req.id,
                    staff_id=staff_id,
                    notes="Technician assigned for service check."
                )
                db.add(assign)

        # 8. Create Rental Applications for Available Units
        u8a = unit_objs["The Grandview Luxury Apartments_8A"]
        u102 = unit_objs["Sunset Palms Villa & Suites_102"]

        apps_seed = [
            (u8a.id, user_objs["tenant5@apexpm.com"].id, Decimal('115000.00'), "Tech Manager", ApplicationStatus.SUBMITTED),
            (u102.id, user_objs["tenant2@apexpm.com"].id, Decimal('140000.00'), "Financial Analyst", ApplicationStatus.APPROVED),
        ]

        for un_id, applicant_id, inc, emp, app_stat in apps_seed:
            app_obj = db.query(RentalApplication).filter(RentalApplication.unit_id == un_id, RentalApplication.applicant_id == applicant_id).first()
            if not app_obj:
                app_obj = RentalApplication(
                    organization_id=org.id,
                    unit_id=un_id,
                    applicant_id=applicant_id,
                    desired_move_in="2026-09-01",
                    lease_term_months=12,
                    monthly_income=inc / Decimal('12.0'),
                    employer_name=emp,
                    job_title=emp,
                    status=app_stat,
                    notes="Solid income history and top tier credit score verification."
                )
                db.add(app_obj)

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
