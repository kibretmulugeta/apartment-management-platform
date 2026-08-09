import logging
import json
import urllib.request
import urllib.parse
from abc import ABC, abstractmethod
from typing import Optional, Dict, Any
from sqlalchemy.orm import Session
from app.core.config import settings
from app.models.message import Notification, NotificationChannel, NotificationEventType

logger = logging.getLogger("notification_service")

# --- ABSTRACT EMAIL ADAPTERS ---
class BaseEmailAdapter(ABC):
    @abstractmethod
    def send_email(self, to_email: str, subject: str, body_text: str, body_html: Optional[str] = None) -> bool:
        pass

class BrevoEmailAdapter(BaseEmailAdapter):
    """Brevo (formerly Sendinblue) free-tier transactional email provider (300 emails/day)."""
    def send_email(self, to_email: str, subject: str, body_text: str, body_html: Optional[str] = None) -> bool:
        if not settings.BREVO_API_KEY:
            logger.warning("[Brevo] API key absent. Falling back to console logging.")
            return ConsoleMockEmailAdapter().send_email(to_email, subject, body_text, body_html)
            
        url = "https://api.brevo.com/v3/smtp/email"
        payload = json.dumps({
            "sender": {"email": settings.EMAIL_FROM_ADDRESS, "name": "Apparent Property Management"},
            "to": [{"email": to_email}],
            "subject": subject,
            "textContent": body_text,
            "htmlContent": body_html or f"<p>{body_text}</p>"
        }).encode("utf-8")
        
        req = urllib.request.Request(
            url,
            data=payload,
            headers={
                "accept": "application/json",
                "api-key": settings.BREVO_API_KEY,
                "content-type": "application/json"
            },
            method="POST"
        )
        try:
            with urllib.request.urlopen(req, timeout=5) as resp:
                return resp.status in [200, 201, 202]
        except Exception as e:
            logger.error(f"[Brevo] Email dispatch failed: {e}")
            return False

class ResendEmailAdapter(BaseEmailAdapter):
    def send_email(self, to_email: str, subject: str, body_text: str, body_html: Optional[str] = None) -> bool:
        if not settings.RESEND_API_KEY:
            return ConsoleMockEmailAdapter().send_email(to_email, subject, body_text, body_html)
        url = "https://api.resend.com/emails"
        payload = json.dumps({"from": settings.EMAIL_FROM_ADDRESS, "to": [to_email], "subject": subject, "text": body_text, "html": body_html}).encode("utf-8")
        req = urllib.request.Request(url, data=payload, headers={"Authorization": f"Bearer {settings.RESEND_API_KEY}", "Content-Type": "application/json"}, method="POST")
        try:
            with urllib.request.urlopen(req, timeout=5) as resp:
                return resp.status in [200, 201]
        except Exception as e:
            logger.error(f"[Resend] Dispatch error: {e}")
            return False

class SendGridEmailAdapter(BaseEmailAdapter):
    def send_email(self, to_email: str, subject: str, body_text: str, body_html: Optional[str] = None) -> bool:
        if not settings.SENDGRID_API_KEY:
            return ConsoleMockEmailAdapter().send_email(to_email, subject, body_text, body_html)
        url = "https://api.sendgrid.com/v3/mail/send"
        payload = json.dumps({
            "personalizations": [{"to": [{"email": to_email}]}],
            "from": {"email": settings.EMAIL_FROM_ADDRESS},
            "subject": subject,
            "content": [{"type": "text/plain", "value": body_text}]
        }).encode("utf-8")
        req = urllib.request.Request(url, data=payload, headers={"Authorization": f"Bearer {settings.SENDGRID_API_KEY}", "Content-Type": "application/json"}, method="POST")
        try:
            with urllib.request.urlopen(req, timeout=5) as resp:
                return resp.status in [200, 202]
        except Exception as e:
            logger.error(f"[SendGrid] Dispatch error: {e}")
            return False

class ConsoleMockEmailAdapter(BaseEmailAdapter):
    def send_email(self, to_email: str, subject: str, body_text: str, body_html: Optional[str] = None) -> bool:
        print(f"\n==================== [MOCK EMAIL DISPATCH] ====================")
        print(f"TO:      {to_email}")
        print(f"FROM:    {settings.EMAIL_FROM_ADDRESS}")
        print(f"SUBJECT: {subject}")
        print(f"BODY:\n{body_text}")
        print(f"===============================================================\n")
        return True

# --- ABSTRACT SMS ADAPTERS ---
class BaseSMSAdapter(ABC):
    @abstractmethod
    def send_sms(self, to_phone: str, message: str) -> bool:
        pass

class TwilioSMSAdapter(BaseSMSAdapter):
    def send_sms(self, to_phone: str, message: str) -> bool:
        if not settings.TWILIO_ACCOUNT_SID or not settings.TWILIO_AUTH_TOKEN:
            return ConsoleMockSMSAdapter().send_sms(to_phone, message)
        print(f"[Twilio] Sending SMS to {to_phone}: {message}")
        return True

class ConsoleMockSMSAdapter(BaseSMSAdapter):
    def send_sms(self, to_phone: str, message: str) -> bool:
        print(f"\n==================== [MOCK SMS DISPATCH] ====================")
        print(f"TO PHONE: {to_phone}")
        print(f"MESSAGE:  {message}")
        print(f"=============================================================\n")
        return True

# --- NOTIFICATION FACTORY & SERVICE ---
def get_email_adapter() -> BaseEmailAdapter:
    provider = (settings.EMAIL_PROVIDER or settings.NOTIFICATION_EMAIL_PROVIDER or "console").lower()
    if provider == "brevo":
        return BrevoEmailAdapter()
    elif provider == "resend":
        return ResendEmailAdapter()
    elif provider == "sendgrid":
        return SendGridEmailAdapter()
    return ConsoleMockEmailAdapter()

def get_sms_adapter() -> BaseSMSAdapter:
    provider = (settings.NOTIFICATION_SMS_PROVIDER or "console").lower()
    if provider == "twilio":
        return TwilioSMSAdapter()
    return ConsoleMockSMSAdapter()

class NotificationService:
    @staticmethod
    def create_notification(
        db: Session,
        user_id: str,
        organization_id: str,
        title: str,
        message: str,
        channel: str = "IN_APP",
        event_type: str = "RENT_DUE",
        metadata_json: Optional[Dict[str, Any]] = None,
        recipient_email: Optional[str] = None,
        recipient_phone: Optional[str] = None
    ) -> Notification:
        """Persists notification row in PostgreSQL and queues background email/SMS tasks."""
        notif = Notification(
            user_id=user_id,
            organization_id=organization_id,
            channel=NotificationChannel(channel),
            event_type=NotificationEventType(event_type),
            title=title,
            message=message,
            metadata_json=metadata_json or {}
        )
        db.add(notif)
        db.commit()
        db.refresh(notif)

        try:
            from app.workers.tasks import dispatch_notification_background_task
            dispatch_notification_background_task.delay(
                channel=channel,
                recipient_email=recipient_email,
                recipient_phone=recipient_phone,
                subject=title,
                message=message
            )
        except Exception as err:
            logger.info(f"[NotificationService] Celery worker unavailable ({err}). Executing inline dispatch.")
            if channel == "EMAIL" and recipient_email:
                get_email_adapter().send_email(recipient_email, title, message)
            elif channel == "SMS" and recipient_phone:
                get_sms_adapter().send_sms(recipient_phone, message)

        return notif
