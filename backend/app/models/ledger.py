from sqlalchemy import Column, String, Text, Numeric, ForeignKey, Enum as SQLEnum, DateTime, UniqueConstraint
from sqlalchemy.orm import relationship
import enum
from datetime import datetime
from app.models.base import BaseModel

class AccountType(str, enum.Enum):
    ASSET = "ASSET"              # Cash, Accounts Receivable
    LIABILITY = "LIABILITY"      # Tenant Security Deposits Payable
    EQUITY = "EQUITY"            # Owner Equity
    REVENUE = "REVENUE"          # Rental Income, Late Fee Revenue
    EXPENSE = "EXPENSE"          # Maintenance Expense, Utility Expense

class EntryType(str, enum.Enum):
    DEBIT = "DEBIT"
    CREDIT = "CREDIT"

class AccountChart(BaseModel):
    __tablename__ = 'account_charts'

    organization_id = Column(String(36), ForeignKey('organizations.id', ondelete='CASCADE'), nullable=False, index=True)
    code = Column(String(50), nullable=False) # e.g., 1000 (Cash), 4000 (Rental Income)
    name = Column(String(255), nullable=False)
    account_type = Column(SQLEnum(AccountType), nullable=False)
    description = Column(String(255), nullable=True)

    __table_args__ = (
        UniqueConstraint('organization_id', 'code', name='uq_org_account_code'),
    )

class Transaction(BaseModel):
    __tablename__ = 'transactions'

    organization_id = Column(String(36), ForeignKey('organizations.id', ondelete='CASCADE'), nullable=False, index=True)
    property_id = Column(String(36), ForeignKey('properties.id', ondelete='SET NULL'), nullable=True, index=True)
    reference = Column(String(100), unique=True, nullable=False, index=True) # e.g. TXN-2026-0001
    description = Column(String(255), nullable=False)
    posted_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    entries = relationship('LedgerEntry', back_populates='transaction', cascade='all, delete-orphan')

class LedgerEntry(BaseModel):
    __tablename__ = 'ledger_entries'

    transaction_id = Column(String(36), ForeignKey('transactions.id', ondelete='CASCADE'), nullable=False, index=True)
    account_id = Column(String(36), ForeignKey('account_charts.id', ondelete='CASCADE'), nullable=False, index=True)
    entry_type = Column(SQLEnum(EntryType), nullable=False)
    amount = Column(Numeric(12, 2), nullable=False)
    memo = Column(String(255), nullable=True)

    transaction = relationship('Transaction', back_populates='entries')
    account = relationship('AccountChart')

class StripeEventLog(BaseModel):
    __tablename__ = 'stripe_event_logs'

    event_id = Column(String(255), unique=True, nullable=False, index=True)
    event_type = Column(String(100), nullable=False)
    processed_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    payload_summary = Column(Text, nullable=True)
