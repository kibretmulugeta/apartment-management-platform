import sys
import os
from decimal import Decimal

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from app.core.database import SessionLocal
from app.models import User, Organization, Property, Unit, Lease, AccountChart, LedgerEntry, EntryType, Notification
from app.services.ledger_service import LedgerService
from app.services.notification_service import NotificationService

def test_system_integrity():
    print("\n--- Running Autonomous Integration & Integrity Checks ---")
    db = SessionLocal()
    try:
        # 1. Verify Users & Roles
        users = db.query(User).all()
        print(f"[CHECK 1] Found {len(users)} seeded user accounts.")
        assert len(users) >= 4, "Missing seeded accounts!"

        # 2. Verify Multi-Tenant Organization
        org = db.query(Organization).filter(Organization.slug == "apex-pm").first()
        print(f"[CHECK 2] Organization: {org.name} (ID: {org.id})")
        assert org is not None, "Organization missing!"

        # 3. Verify Properties & Units
        properties = db.query(Property).filter(Property.organization_id == org.id).all()
        units = db.query(Unit).filter(Unit.organization_id == org.id).all()
        print(f"[CHECK 3] Found {len(properties)} properties and {len(units)} units in organization.")
        assert len(properties) >= 2, "Properties missing!"

        # 4. Verify Double-Entry Financial Ledger Balance
        revenue_entries = db.query(LedgerEntry).join(AccountChart).filter(
            AccountChart.organization_id == org.id,
            AccountChart.code == "4000",
            LedgerEntry.entry_type == EntryType.CREDIT
        ).all()
        total_credit_revenue = sum(e.amount for e in revenue_entries)
        
        cash_entries = db.query(LedgerEntry).join(AccountChart).filter(
            AccountChart.organization_id == org.id,
            AccountChart.code == "1000",
            LedgerEntry.entry_type == EntryType.DEBIT
        ).all()
        total_debit_cash = sum(e.amount for e in cash_entries)

        print(f"[CHECK 4] Double-Entry Ledger Equality: Total Debit Cash (${total_debit_cash}) == Total Credit Revenue (${total_credit_revenue})")
        assert total_debit_cash == total_credit_revenue, "Unbalanced ledger!"

        # 5. Verify Notification Queueing
        notif = NotificationService.create_notification(
            db=db,
            user_id=users[0].id,
            organization_id=org.id,
            title="System Initialization Complete",
            message="Autonomous database execution succeeded.",
            channel="IN_APP",
            event_type="RENT_DUE"
        )
        print(f"[CHECK 5] Created test notification ID: {notif.id}")
        assert notif.id is not None, "Notification failed to persist!"

        print("[SUCCESS] ALL 5 AUTONOMOUS SYSTEM INTEGRITY CHECKS PASSED PERFECTLY!\n")

    finally:
        db.close()

if __name__ == "__main__":
    test_system_integrity()
