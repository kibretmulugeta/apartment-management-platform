from fastapi import APIRouter, Request, Header, HTTPException, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.stripe_service import StripeService

router = APIRouter(prefix="/webhooks", tags=["Webhooks"])

@router.post("/stripe")
async def stripe_webhook(request: Request, stripe_signature: str = Header(None), db: Session = Depends(get_db)):
    """Idempotent Stripe Webhook endpoint."""
    payload = await request.json()
    event_id = payload.get("id")
    event_type = payload.get("type")

    if not event_id or not event_type:
        raise HTTPException(status_code=400, detail="Invalid Stripe webhook payload")

    result = StripeService.process_webhook_event(
        db=db,
        event_id=event_id,
        event_type=event_type,
        payload=payload
    )

    return result
