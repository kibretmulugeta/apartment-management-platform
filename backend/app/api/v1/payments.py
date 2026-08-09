from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.payment import Payment, PaymentStatus, PaymentType
from app.models.lease import Lease
from app.schemas.payment import PaymentIntentCreate, PaymentResponse
from app.schemas.common import APIResponse
from app.api.dependencies import get_current_user, get_current_org_id, require_roles
from app.services.stripe_service import StripeService
from app.services.ledger_service import LedgerService
from app.models.user import User

router = APIRouter(prefix="/payments", tags=["Payments"])

@router.post("/create-intent", response_model=APIResponse[dict])
def create_payment_intent(
    pay_in: PaymentIntentCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    lease = None
    org_id = current_user.current_org_id
    if pay_in.lease_id:
        lease = db.query(Lease).filter(Lease.id == pay_in.lease_id).first()
        if lease:
            org_id = lease.organization_id

    intent = StripeService.create_payment_intent(
        amount=pay_in.amount,
        metadata={"user_id": current_user.id, "lease_id": pay_in.lease_id}
    )

    # Store pending payment record
    payment = Payment(
        organization_id=org_id or "default_org",
        lease_id=pay_in.lease_id,
        payer_id=current_user.id,
        payment_type=PaymentType(pay_in.payment_type),
        amount=pay_in.amount,
        status=PaymentStatus.PENDING,
        stripe_payment_intent_id=intent["id"],
        description=pay_in.description or f"{pay_in.payment_type} payment"
    )
    db.add(payment)
    db.commit()

    return APIResponse(
        success=True,
        message="Stripe payment intent created",
        data={"client_secret": intent["client_secret"], "payment_intent_id": intent["id"]}
    )

@router.post("/confirm-simulate", response_model=APIResponse[PaymentResponse])
def confirm_simulated_payment(
    payment_intent_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Simulates immediate Stripe payment authorization & double-entry ledger posting for local dev testing."""
    payment = db.query(Payment).filter(Payment.stripe_payment_intent_id == payment_intent_id).first()
    if not payment:
        raise HTTPException(status_code=404, detail="Payment record not found")

    payment.status = PaymentStatus.SUCCEEDED
    payment.receipt_url = f"https://receipts.apparent.com/{payment.id}.pdf"
    
    # Automatically execute double-entry ledger transaction!
    property_id = payment.lease.unit.property_id if payment.lease else "general"
    LedgerService.record_rent_payment(
        db=db,
        organization_id=payment.organization_id,
        property_id=property_id,
        amount=payment.amount,
        tenant_name=current_user.full_name
    )

    db.commit()
    db.refresh(payment)

    return APIResponse(success=True, message="Payment succeeded and posted to ledger", data=PaymentResponse.model_validate(payment))

@router.get("/my-payments", response_model=APIResponse[List[PaymentResponse]])
def get_my_payments(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    payments = db.query(Payment).filter(Payment.payer_id == current_user.id).order_by(Payment.created_at.desc()).all()
    return APIResponse(success=True, data=[PaymentResponse.model_validate(p) for p in payments])

@router.get("/", response_model=APIResponse[List[PaymentResponse]])
def list_org_payments(
    org_id: str = Depends(get_current_org_id),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(["ADMIN", "LANDLORD", "PROPERTY_MANAGER"]))
):
    payments = db.query(Payment).filter(Payment.organization_id == org_id).order_by(Payment.created_at.desc()).all()
    return APIResponse(success=True, data=[PaymentResponse.model_validate(p) for p in payments])
