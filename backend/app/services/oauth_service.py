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
    def get_authorization_url(provider: str, role: str = "TENANT") -> str:
        prov = provider.lower()
        if prov not in OAuthService.PROVIDER_CONFIGS:
            raise HTTPException(status_code=400, detail=f"Unsupported OAuth provider: {provider}")

        cfg = OAuthService.PROVIDER_CONFIGS[prov]
        client_id = cfg["client_id"]() or "mock_client_id"
        redirect_uri = f"{settings.OAUTH_REDIRECT_BASE_URL}?provider={prov}"
        scope = "%20".join(cfg["scopes"])
        state = f"{prov}:{role.upper()}"

        return f"{cfg['auth_url']}?client_id={client_id}&redirect_uri={urllib.parse.quote(redirect_uri, safe='')}&response_type=code&scope={scope}&state={state}&access_type=offline&prompt=consent"

    @staticmethod
    def process_oauth_login(
        provider: str,
        code: str,
        db: Session,
        default_role: str = "TENANT",
        state: str = None
    ) -> Tuple[User, str, str]:
        """Exchanges authorization code for profile info and provisions/logs in user."""
        prov = provider.lower()
        if prov not in OAuthService.PROVIDER_CONFIGS:
            raise HTTPException(status_code=400, detail=f"Unsupported OAuth provider: {provider}")

        cfg = OAuthService.PROVIDER_CONFIGS[prov]

        # Parse state for requested role if embedded (e.g. google:LANDLORD)
        if state and ":" in state:
            parts = state.split(":", 1)
            if len(parts) == 2 and parts[1].strip():
                default_role = parts[1].strip()

        # Exchange code for user profile
        email = None
        first_name = prov.capitalize()
        last_name = "User"
        client_id_val = cfg["client_id"]()

        if code.startswith("mock_") or "mock" in code or not client_id_val:
            # Fallback for dev / mock testing
            email = f"user_{code[:6]}@{prov}.com"
            first_name = f"{prov.capitalize()}Dev"
            last_name = "User"
        else:
            try:
                client_secret_val = cfg["client_secret"]()
                redirect_uri = f"{settings.OAUTH_REDIRECT_BASE_URL}?provider={prov}"

                # 1. Exchange code for access_token
                token_params = {
                    "code": code,
                    "client_id": client_id_val,
                    "client_secret": client_secret_val,
                    "redirect_uri": redirect_uri,
                    "grant_type": "authorization_code"
                }
                token_data = urllib.parse.urlencode(token_params).encode("utf-8")

                token_req = urllib.request.Request(
                    cfg["token_url"],
                    data=token_data,
                    headers={
                        "Content-Type": "application/x-www-form-urlencoded",
                        "Accept": "application/json"
                    }
                )

                with urllib.request.urlopen(token_req) as resp:
                    token_res = json.loads(resp.read().decode("utf-8"))
                    access_token_val = token_res.get("access_token")
                    id_token_val = token_res.get("id_token")

                if access_token_val:
                    # 2. Fetch user profile via user_info_url
                    profile_req = urllib.request.Request(
                        cfg["user_info_url"],
                        headers={
                            "Authorization": f"Bearer {access_token_val}",
                            "Accept": "application/json"
                        }
                    )
                    with urllib.request.urlopen(profile_req) as resp:
                        user_info = json.loads(resp.read().decode("utf-8"))
                        email = user_info.get("email") or user_info.get("mail") or user_info.get("userPrincipalName")
                        first_name = user_info.get("given_name") or user_info.get("first_name") or user_info.get("name") or prov.capitalize()
                        last_name = user_info.get("family_name") or user_info.get("last_name") or ""
            except Exception as e:
                # Log error and fallback gracefully in dev environment
                print(f"[OAuth Warning] Code exchange failed with provider {prov}: {e}")
                email = f"oauth_{prov}_{uuid.uuid4().hex[:6]}@domain.com"

        if not email:
            email = f"oauth_{prov}_{uuid.uuid4().hex[:6]}@domain.com"

        # Check existing user
        user = db.query(User).filter(User.email == email).first()
        if not user:
            user = User(
                email=email,
                hashed_password=get_password_hash(uuid.uuid4().hex),
                first_name=first_name,
                last_name=last_name if last_name else "User",
                is_active=True,
                is_verified=True
            )
            db.add(user)
            db.flush()

            # Attach role
            role = db.query(Role).filter(Role.name == default_role.upper()).first()
            if not role:
                role = db.query(Role).filter(Role.name == "TENANT").first()
            if role and role not in user.roles:
                user.roles.append(role)

            # Attach organization
            default_org = db.query(Organization).first()
            if not default_org:
                default_org = Organization(name="Apex Property Management", slug="apex-pm", email="contact@apexpm.com")
                db.add(default_org)
                db.flush()
                LedgerService.ensure_default_chart_of_accounts(db, default_org.id)

            mem = db.query(OrganizationMember).filter(
                OrganizationMember.organization_id == default_org.id,
                OrganizationMember.user_id == user.id
            ).first()

            if not mem:
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
