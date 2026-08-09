from decimal import Decimal
import uuid
from datetime import datetime
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.ledger import Transaction, LedgerEntry, AccountChart, AccountType, EntryType

class LedgerService:
    @staticmethod
    def ensure_default_chart_of_accounts(db: Session, organization_id: str):
        """Initializes standard GAAP Chart of Accounts for a multi-tenant organization."""
        default_accounts = [
            ("1000", "Operating Cash Account", AccountType.ASSET),
            ("1100", "Accounts Receivable - Rent", AccountType.ASSET),
            ("2000", "Tenant Security Deposits Payable", AccountType.LIABILITY),
            ("4000", "Rental Income Revenue", AccountType.REVENUE),
            ("4100", "Late Fee Income", AccountType.REVENUE),
            ("4200", "Application Fee Revenue", AccountType.REVENUE),
            ("5000", "Property Maintenance & Repair Expense", AccountType.EXPENSE),
            ("5100", "Utilities Expense", AccountType.EXPENSE),
            ("5200", "Property Management Expense", AccountType.EXPENSE),
        ]
        
        for code, name, acc_type in default_accounts:
            existing = db.query(AccountChart).filter(
                AccountChart.organization_id == organization_id,
                AccountChart.code == code
            ).first()
            if not existing:
                account = AccountChart(
                    organization_id=organization_id,
                    code=code,
                    name=name,
                    account_type=acc_type
                )
                db.add(account)
        db.commit()

    @staticmethod
    def post_journal_entry(
        db: Session,
        organization_id: str,
        property_id: str,
        description: str,
        entries_data: list[dict] # list of {"account_code": "1000", "entry_type": "DEBIT"/"CREDIT", "amount": Decimal, "memo": str}
    ) -> Transaction:
        """Posts a balanced double-entry transaction inside an atomic database block."""
        # 1. Ensure accounts exist
        LedgerService.ensure_default_chart_of_accounts(db, organization_id)

        # 2. Verify debit = credit equality constraint
        total_debits = Decimal('0.00')
        total_credits = Decimal('0.00')
        
        for item in entries_data:
            amt = Decimal(str(item["amount"]))
            if item["entry_type"] == "DEBIT":
                total_debits += amt
            elif item["entry_type"] == "CREDIT":
                total_credits += amt
            else:
                raise HTTPException(status_code=400, detail="Invalid entry_type. Must be DEBIT or CREDIT.")

        if total_debits != total_credits:
            raise HTTPException(
                status_code=400,
                detail=f"Unbalanced journal entry! Debits ({total_debits}) != Credits ({total_credits})"
            )

        ref_code = f"TXN-{uuid.uuid4().hex[:8].upper()}"
        transaction = Transaction(
            organization_id=organization_id,
            property_id=property_id,
            reference=ref_code,
            description=description,
            posted_at=datetime.utcnow()
        )
        db.add(transaction)
        db.flush() # get transaction.id

        for item in entries_data:
            account = db.query(AccountChart).filter(
                AccountChart.organization_id == organization_id,
                AccountChart.code == item["account_code"]
            ).first()
            
            if not account:
                raise HTTPException(status_code=400, detail=f"Account code {item['account_code']} not found in Chart of Accounts.")
                
            entry = LedgerEntry(
                transaction_id=transaction.id,
                account_id=account.id,
                entry_type=EntryType(item["entry_type"]),
                amount=Decimal(str(item["amount"])),
                memo=item.get("memo", description)
            )
            db.add(entry)
            
        db.commit()
        db.refresh(transaction)
        return transaction

    @staticmethod
    def record_rent_payment(db: Session, organization_id: str, property_id: str, amount: Decimal, tenant_name: str):
        """Debit Cash (1000), Credit Rental Income (4000)."""
        entries = [
            {"account_code": "1000", "entry_type": "DEBIT", "amount": amount, "memo": f"Rent payment received from {tenant_name}"},
            {"account_code": "4000", "entry_type": "CREDIT", "amount": amount, "memo": f"Rental Income recognized for {tenant_name}"}
        ]
        return LedgerService.post_journal_entry(db, organization_id, property_id, f"Rent Payment - {tenant_name}", entries)

    @staticmethod
    def record_maintenance_expense(db: Session, organization_id: str, property_id: str, amount: Decimal, vendor: str, description: str):
        """Debit Maintenance Expense (5000), Credit Operating Cash (1000)."""
        entries = [
            {"account_code": "5000", "entry_type": "DEBIT", "amount": amount, "memo": f"Repair work by {vendor}: {description}"},
            {"account_code": "1000", "entry_type": "CREDIT", "amount": amount, "memo": f"Disbursement to {vendor}"}
        ]
        return LedgerService.post_journal_entry(db, organization_id, property_id, f"Expense - {vendor}", entries)
