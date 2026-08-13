import sys
import os
import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from app.core.database import SessionLocal, engine, Base
from app.services.oauth_service import OAuthService
from app.models.user import User, Role
from app.core.security import decode_token

# Ensure database tables exist for tests
Base.metadata.create_all(bind=engine)

def test_google_oauth_authorization_url():
    """Verify Google OAuth authorization URL structure and state encoding."""
    url = OAuthService.get_authorization_url("google", role="LANDLORD")
    assert "https://accounts.google.com/o/oauth2/v2/auth" in url
    assert "client_id=" in url
    assert "response_type=code" in url
    assert "scope=openid" in url
    assert "state=google%3ALANDLORD" in url or "state=google:LANDLORD" in url

def test_google_oauth_mock_login_and_provisioning():
    """Verify OAuth code processing, user creation, role assignment, and JWT token creation."""
    db = SessionLocal()
    try:
        mock_code = "mock_test_google_123"
        state = "google:LANDLORD"
        
        user, access_token, refresh_token = OAuthService.process_oauth_login(
            provider="google",
            code=mock_code,
            db=db,
            default_role="TENANT",
            state=state
        )

        assert user is not None
        assert user.id is not None
        assert user.email == f"user_{mock_code[:6]}@google.com"
        assert user.is_active is True
        assert user.is_verified is True

        # Check role assignment from state (LANDLORD)
        role_names = [r.name for r in user.roles]
        assert "LANDLORD" in role_names

        # Check organization assignment
        assert user.current_org_id is not None

        # Check JWT access token validity
        payload = decode_token(access_token)
        assert payload.get("sub") == user.id
        assert payload.get("type") == "access"

        print(f"\n[OAuth Test] Successfully authenticated user: {user.email} (ID: {user.id}, Role: {role_names})")
    finally:
        db.close()

if __name__ == "__main__":
    test_google_oauth_authorization_url()
    test_google_oauth_mock_login_and_provisioning()
    print("\n[SUCCESS] ALL OAUTH TESTS PASSED!")
