import uuid
from decimal import Decimal
from datetime import datetime
from sqlalchemy.orm import Session
from app.core.config import settings
from app.models.ledger import StripeEventLog
from app.models.payment import Payment, PaymentStatus
from app.services.ledger_service import LedgerService

class StripeService:
    @staticmethod
    def create_payment_intent(amount: Decimal, currency: str = "usd", metadata: dict = None) -> dict:
        """Simulates or calls Stripe PaymentIntent API."""
        intent_id = f"pi_dev_{uuid.uuid4().hex[:16]}"
        client_secret = f"{intent_id}_secret_{uuid.uuid4().hex[:12]}"
        return {
            "id": intent_id,
            "client_secret": client_secret,
            "amount": int(amount * 100),
            "currency": currency,
            "status": "requires_payment_method",
            "metadata": metadata or {}
        }

    @staticmethod
    def process_webhook_event(db: Session, event_id: str, event_type: str, payload: dict) -> dict:
        """Idempotent Stripe Webhook Handler using stripe_event_logs table."""
        # 1. Check if event_id has already been logged/processed
        existing_log = db.query(StripeEventLog).filter(StripeEventLog.event_id == event_id).first()
        if existing_log:
            return {"status": "ignored", "message": f"Webhook event {event_id} already processed cleanly."}

        # 2. Log event ID atomically to prevent duplicate processing
        log_entry = StripeEventLog(
            event_id=event_id,
            event_type=event_type,
            processed_at=datetime.utcnow(),
            payload_summary=str(payload)[:500]
        )
        db.add(log_entry)

        # 3. Process business logic based on event_type
        if event_type == "payment_intent.succeeded":
            intent = payload.get("data", {}).get("object", {})
            intent_id = intent.get("id")
            
            # Find associated payment
            payment = db.query(Payment).filter(Payment.stripe_payment_intent_id == intent_id).first()
            if payment and payment.status != PaymentStatus.SUCCEEDED:
                payment.status = PaymentStatus.SUCCEEDED
                
                # Automatically post double-entry ledger journal entry!
                if payment.lease:
                    property_id = payment.lease.unit.property_id
                    tenant_name = payment.payer.full_name
                else:
                    property_id = "general"
                    tenant_name = payment.payer.full_name

                LedgerService.record_rent_payment(
                    db=db,
                    organization_id=payment.organization_id,
                    property_id=property_id,
                    amount=payment.amount,
                    tenant_name=tenant_name
                )

        db.commit()
        return {"status": "processed", "event_id": event_id}
