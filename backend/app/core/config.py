import os
from typing import List, Optional
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    PROJECT_NAME: str = "Apparent Property Management"
    API_V1_STR: str = "/api/v1"
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    LOG_LEVEL: str = "INFO"

    # Security
    SECRET_KEY: str = "supersecret-production-key-change-in-prod-32bytes-min!"
    JWT_SECRET: str = "supersecret-jwt-key-change-in-prod-32bytes-min!"
    JWT_REFRESH_SECRET: str = "supersecret-jwt-refresh-key-change-in-prod!"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # CORS
    BACKEND_CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:8000",
        "https://apartment-management-platform-eight.vercel.app",
        "https://apartment-management-platform-ofnz.vercel.app",
        "https://apartment-management-platform.vercel.app",
    ]


    # Database
    DATABASE_URL: str = f"sqlite:///{os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', 'apparent.db')).replace('\\\\', '/')}"
    
    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"

    # Stripe
    STRIPE_SECRET_KEY: str = "sk_test_51MockStripeSecretKeyForDev1234567890"
    STRIPE_PUBLISHABLE_KEY: str = "pk_test_51MockStripePublishableKeyForDev1234567890"
    STRIPE_WEBHOOK_SECRET: str = "whsec_MockStripeWebhookSecret1234567890"

    # Storage
    STORAGE_PROVIDER: str = "local" # 'local' or 's3'
    UPLOAD_DIR: str = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "uploads")
    S3_BUCKET: str = "apparent-documents"
    AWS_ACCESS_KEY_ID: Optional[str] = None
    AWS_SECRET_ACCESS_KEY: Optional[str] = None
    AWS_REGION: str = "us-east-1"

    # Email & Notification Providers
    EMAIL_PROVIDER: str = "console" # brevo, resend, sendgrid, ses, console
    NOTIFICATION_EMAIL_PROVIDER: str = "console"
    BREVO_API_KEY: Optional[str] = None
    RESEND_API_KEY: Optional[str] = None
    SENDGRID_API_KEY: Optional[str] = None
    EMAIL_FROM_ADDRESS: str = "notifications@apparentpm.com"

    # SMS Provider
    NOTIFICATION_SMS_PROVIDER: str = "console" # twilio, console
    TWILIO_ACCOUNT_SID: Optional[str] = None
    TWILIO_AUTH_TOKEN: Optional[str] = None
    TWILIO_PHONE_NUMBER: Optional[str] = None

    # Multi-Provider OAuth
    GOOGLE_CLIENT_ID: Optional[str] = None
    GOOGLE_CLIENT_SECRET: Optional[str] = None

    MICROSOFT_CLIENT_ID: Optional[str] = None
    MICROSOFT_CLIENT_SECRET: Optional[str] = None

    FACEBOOK_CLIENT_ID: Optional[str] = None
    FACEBOOK_CLIENT_SECRET: Optional[str] = None

    LINKEDIN_CLIENT_ID: Optional[str] = None
    LINKEDIN_CLIENT_SECRET: Optional[str] = None

    OAUTH_REDIRECT_BASE_URL: str = "http://localhost:3000/auth/callback"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

settings = Settings()
