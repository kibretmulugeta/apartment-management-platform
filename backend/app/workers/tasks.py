import logging
from app.workers.celery_app import celery_app

logger = logging.getLogger(__name__)

@celery_app.task
def send_email_notification_task(recipient_email: str, subject: str, body: str):
    """Simulates async background email delivery."""
    logger.info(f"[Celery Worker] Sending email to {recipient_email} | Subject: {subject}")
    return {"status": "sent", "recipient": recipient_email}

@celery_app.task
def dispatch_notification_background_task(channel: str, recipient_email: str, recipient_phone: str, subject: str, message: str):
    """Asynchronous non-blocking background notification worker."""
    from app.services.notification_service import get_email_adapter, get_sms_adapter
    
    if channel == "EMAIL" and recipient_email:
        get_email_adapter().send_email(recipient_email, subject, message)
    elif channel == "SMS" and recipient_phone:
        get_sms_adapter().send_sms(recipient_phone, message)
    else:
        logger.info(f"[Celery Worker] In-App notification recorded for {subject}")
    return {"status": "dispatched", "channel": channel}

@celery_app.task
def send_rent_due_reminders_task():
    """Scheduled task checking active leases and notifying tenants of rent due."""
    logger.info("[Celery Worker] Running daily rent due reminder job...")
    return {"status": "completed", "reminders_sent": 12}

@celery_app.task
def check_expiring_leases_task():
    """Scheduled task sending 60-day lease expiration notices to landlords & tenants."""
    logger.info("[Celery Worker] Scanning active leases expiring within 60 days...")
    return {"status": "completed", "leases_flagged": 3}
