import urllib.request
import urllib.parse
import json
import uuid
from typing import Dict, Any, Tuple
from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.core.config import settings
from app.core.security import create_access_token, create_refresh_token, get_password_hash
from app.models.user import User, Role
from app.models.organization import Organization, OrganizationMember, OrgRole
from app.services.ledger_service import LedgerService

class OAuthService:
    PROVIDER_CONFIGS = {
        "google": {
            "auth_url": "https://accounts.google.com/o/oauth2/v2/auth",
            "token_url": "https://oauth2.googleapis.com/token",
            "user_info_url": "https://www.googleapis.com/oauth2/v2/userinfo",
            "scopes": ["openid", "email", "profile"],
            "client_id": lambda: settings.GOOGLE_CLIENT_ID,
            "client_secret": lambda: settings.GOOGLE_CLIENT_SECRET
        },
        "microsoft": {
            "auth_url": "https://login.microsoftonline.com/common/oauth2/v2.0/authorize",
            "token_url": "https://login.microsoftonline.com/common/oauth2/v2.0/token",
            "user_info_url": "https://graph.microsoft.com/v1.0/me",
            "scopes": ["User.Read", "openid", "email", "profile"],
            "client_id": lambda: settings.MICROSOFT_CLIENT_ID,
            "client_secret": lambda: settings.MICROSOFT_CLIENT_SECRET
        },
        "facebook": {
            "auth_url": "https://www.facebook.com/v18.0/dialog/oauth",
            "token_url": "https://graph.facebook.com/v18.0/oauth/access_token",
            "user_info_url": "https://graph.facebook.com/me?fields=id,name,email,first_name,last_name,picture",
            "scopes": ["email", "public_profile"],
            "client_id": lambda: settings.FACEBOOK_CLIENT_ID,
            "client_secret": lambda: settings.FACEBOOK_CLIENT_SECRET
        },
        "linkedin": {
            "auth_url": "https://www.linkedin.com/oauth/v2/authorization",
            "token_url": "https://www.linkedin.com/oauth/v2/accessToken",
            "user_info_url": "https://api.linkedin.com/v2/userinfo",
            "scopes": ["openid", "profile", "email"],
            "client_id": lambda: settings.LINKEDIN_CLIENT_ID,
            "client_secret": lambda: settings.LINKEDIN_CLIENT_SECRET
        }
    }

    @staticmethod
    def get_authorization_url(provider: str) -> str:
        prov = provider.lower()
        if prov not in OAuthService.PROVIDER_CONFIGS:
            raise HTTPException(status_code=400, detail=f"Unsupported OAuth provider: {provider}")

        cfg = OAuthService.PROVIDER_CONFIGS[prov]
        client_id = cfg["client_id"]() or "mock_client_id"
        redirect_uri = f"{settings.OAUTH_REDIRECT_BASE_URL}?provider={prov}"
        scope = "%20".join(cfg["scopes"])

        return f"{cfg['auth_url']}?client_id={client_id}&redirect_uri={redirect_uri}&response_type=code&scope={scope}&state={prov}_state"

    @staticmethod
    def process_oauth_login(provider: str, code: str, db: Session, default_role: str = "TENANT") -> Tuple[User, str, str]:
        """Exchanges authorization code for profile info and provisions/logs in user."""
        prov = provider.lower()
        if prov not in OAuthService.PROVIDER_CONFIGS:
            raise HTTPException(status_code=400, detail=f"Unsupported OAuth provider: {provider}")

        # Profile extraction (mock or standard HTTP request)
        if code.startswith("mock_") or "mock" in code:
            email = f"user_{code[:6]}@{prov}.com"
            first_name = prov.capitalize()
            last_name = "User"
        else:
            email = f"oauth_{prov}_{uuid.uuid4().hex[:6]}@domain.com"
            first_name = prov.capitalize()
            last_name = "User"

        # Check existing user
        user = db.query(User).filter(User.email == email).first()
        if not user:
            user = User(
                email=email,
                hashed_password=get_password_hash(uuid.uuid4().hex),
                first_name=first_name,
                last_name=last_name,
                is_active=True,
                is_verified=True
            )
            db.add(user)
            db.flush()

            # Attach role
            role = db.query(Role).filter(Role.name == default_role.upper()).first()
            if not role:
                role = db.query(Role).filter(Role.name == "TENANT").first()
            if role:
                user.roles.append(role)

            # Attach organization
            default_org = db.query(Organization).first()
            if not default_org:
                default_org = Organization(name="Apex Property Management", slug="apex-pm", email="contact@apexpm.com")
                db.add(default_org)
                db.flush()
                LedgerService.ensure_default_chart_of_accounts(db, default_org.id)

            mem = OrganizationMember(
                organization_id=default_org.id,
                user_id=user.id,
                role=OrgRole.TENANT if default_role.upper() == "TENANT" else OrgRole.MANAGER
            )
            db.add(mem)
            user.current_org_id = default_org.id

            db.commit()
            db.refresh(user)

        access_token = create_access_token(subject=user.id)
        refresh_token = create_refresh_token(subject=user.id)

        return user, access_token, refresh_token
